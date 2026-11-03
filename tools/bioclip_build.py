"""Menyiapkan identifikasi jenis dari foto (seperti saran iNaturalist) untuk Survei KEHATI, berjalan di HP tanpa sinyal.

Model: BioCLIP (imageomics/bioclip, lisensi MIT), CLIP ViT-B/16 yang dilatih pada TreeOfLife-10M.
  1. Encoder gambar diekspor ke ONNX lalu dikuantisasi 8-bit -> apps/survei-kehati/model/bioclip/onnx/vision_model_quantized.onnx
     (format yang dimuat transformers.js sebagai CLIPVisionModelWithProjection; hanya dibuat bila belum ada).
  2. Embedding teks setiap jenis di data/jenis-<taksa>.json (taksonomi lengkap + nama Inggris, sesuai cara BioCLIP)
     dihitung di sini dan disimpan 8-bit per baris -> data/emb-<taksa>.bin, urutan sama dengan daftar jenis.
     Format: 'KEMB', uint32 N, uint32 D, float32 skala[N], int8 vektor[N*D] (little-endian).
  3. Uji ketepatan: foto contoh iNaturalist dari sebagian jenis diidentifikasi dengan model ONNX 8-bit dan embedding 8-bit
     (sama seperti di HP); hasil top-1/top-5 dicetak di log.
"""
import io, json, os, random, struct, sys, time, urllib.request, urllib.error
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
APP = os.path.join(ROOT, 'apps', 'survei-kehati')
DATA = os.path.join(APP, 'data')
MODEL = os.path.join(APP, 'model', 'bioclip')
BUILD = os.path.join(ROOT, 'build')
TAXO_DIR = os.path.join(ROOT, 'tools', 'taxo')   # taksonomi lengkap per jenis (untuk teks BioCLIP), disimpan di repo
MEAN = np.array([0.48145466, 0.4578275, 0.40821073], dtype=np.float32)
STD = np.array([0.26862954, 0.26130258, 0.27577711], dtype=np.float32)

def load_model():
    import open_clip, torch
    model, _, preprocess = open_clip.create_model_and_transforms('hf-hub:imageomics/bioclip')
    model.eval()
    tok = open_clip.get_tokenizer('hf-hub:imageomics/bioclip')
    return model, preprocess, tok, torch

def export_vision(model, torch):
    q = os.path.join(MODEL, 'onnx', 'vision_model_quantized.onnx')
    if os.path.exists(q):
        print('model ONNX sudah ada:', os.path.getsize(q) // 1048576, 'MB'); return q
    os.makedirs(os.path.dirname(q), exist_ok=True)
    import torch.nn.functional as F
    class V(torch.nn.Module):
        def __init__(self, m): super().__init__(); self.m = m
        def forward(self, pixel_values): return F.normalize(self.m.encode_image(pixel_values), dim=-1)
    fp = os.path.join(BUILD, 'vision_model.onnx')
    torch.onnx.export(V(model), torch.randn(1, 3, 224, 224), fp, input_names=['pixel_values'], output_names=['image_embeds'],
                      dynamic_axes={'pixel_values': {0: 'batch'}, 'image_embeds': {0: 'batch'}}, opset_version=17, dynamo=False)
    from onnxruntime.quantization import quantize_dynamic, QuantType
    quantize_dynamic(fp, q, weight_type=QuantType.QUInt8)
    size = os.path.getsize(q)
    print('model ONNX 8-bit:', size // 1048576, 'MB')
    if size > 99 * 1048576: sys.exit('model terlalu besar untuk GitHub (>99 MB)')
    with open(os.path.join(MODEL, 'config.json'), 'w') as f:
        json.dump({'model_type': 'clip', 'architectures': ['CLIPModel'], 'projection_dim': 512,
                   'vision_config': {'model_type': 'clip_vision_model', 'image_size': 224, 'patch_size': 16, 'hidden_size': 768},
                   'text_config': {'model_type': 'clip_text_model'}, '_sumber': 'imageomics/bioclip (MIT), diekspor untuk Survei KEHATI'}, f, indent=1)
    with open(os.path.join(MODEL, 'preprocessor_config.json'), 'w') as f:
        json.dump({'crop_size': {'height': 224, 'width': 224}, 'do_center_crop': True, 'do_normalize': True, 'do_rescale': True, 'do_resize': True,
                   'do_convert_rgb': True, 'image_mean': MEAN.tolist(), 'image_std': STD.tolist(), 'resample': 3, 'rescale_factor': 1 / 255,
                   'size': {'shortest_edge': 224}, 'feature_extractor_type': 'CLIPFeatureExtractor', 'image_processor_type': 'CLIPImageProcessor'}, f, indent=1)
    return q

def prompt(t):
    sci, eng, kingdom, phylum, cls, order, family, genus = t
    epithet = sci.split(' ', 1)[1] if ' ' in sci else sci
    taxo = ' '.join(x for x in [kingdom, phylum, cls, order, family, genus or sci.split(' ')[0], epithet] if x)
    return f'a photo of {taxo} with common name {eng}.' if eng else f'a photo of {taxo}.'

def text_embeddings(model, tok, torch, taxo):
    out = []
    with torch.no_grad():
        for i in range(0, len(taxo), 256):
            e = model.encode_text(tok([prompt(t) for t in taxo[i:i + 256]]))
            out.append(torch.nn.functional.normalize(e, dim=-1).numpy())
    return np.concatenate(out).astype(np.float32)

def write_emb(path, E):
    scale = np.maximum(np.abs(E).max(axis=1), 1e-8) / 127.0
    q = np.clip(np.round(E / scale[:, None]), -127, 127).astype(np.int8)
    with open(path, 'wb') as f:
        f.write(b'KEMB'); f.write(struct.pack('<II', *E.shape)); f.write(scale.astype('<f4').tobytes()); f.write(q.tobytes())
    return (q.astype(np.float32) * scale[:, None])

def preprocess_like_web(img):
    """Sama dengan CLIPImageProcessor di transformers.js: sisi terpendek 224 (bicubic), potong tengah 224, normalisasi."""
    from PIL import Image
    img = img.convert('RGB'); w, h = img.size; k = 224 / min(w, h)
    img = img.resize((max(224, round(w * k)), max(224, round(h * k))), Image.BICUBIC)
    w, h = img.size; l, t = (w - 224) // 2, (h - 224) // 2
    a = np.asarray(img.crop((l, t, l + 224, t + 224)), dtype=np.float32) / 255.0
    return ((a - MEAN) / STD).transpose(2, 0, 1)[None]

def fetch(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'survei-kehati/1.0'}), timeout=60) as r: return r.read()
        except Exception: time.sleep(2)
    return None

def main():
    os.makedirs(BUILD, exist_ok=True)
    model, preprocess, tok, torch = load_model()
    qpath = export_vision(model, torch)
    index, deq = {}, {}
    for fn in sorted(os.listdir(DATA)):
        if not (fn.startswith('jenis-') and fn.endswith('.json')): continue
        tax = fn[6:-5]
        rows = json.load(open(os.path.join(DATA, fn), encoding='utf-8'))['rows']
        tp = os.path.join(TAXO_DIR, f'taxo-{tax}.json')
        taxo = json.load(open(tp, encoding='utf-8')) if os.path.exists(tp) else [[r[0], r[2], '', '', '', '', r[3], ''] for r in rows]
        assert [t[0] for t in taxo] == [r[0] for r in rows], f'urutan taxo-{tax} tidak sama dengan jenis-{tax}'
        t0 = time.time(); E = text_embeddings(model, tok, torch, taxo)
        deq[tax] = (write_emb(os.path.join(DATA, f'emb-{tax}.bin'), E), rows)
        index[tax] = {'n': len(rows), 'dim': int(E.shape[1]), 'mb': round(os.path.getsize(os.path.join(DATA, f'emb-{tax}.bin')) / 1048576, 1)}
        print(f'embedding {tax}: {len(rows)} jenis, {time.time() - t0:.0f} dtk', flush=True)
    logit = float(model.logit_scale.exp().item())
    # Uji ketepatan dengan model 8-bit (seperti di HP) memakai foto contoh iNaturalist, diambil acak dari semua jenis
    # bertanda foto. Diuji juga bobot "jenis umum di Indonesia" (seperti 'teramati di sekitar' iNaturalist):
    # skor = kemiripan x skala logit + beta x ln(1 + catatan GBIF + 3 x pengamatan iNat).
    import onnxruntime as ort
    from PIL import Image
    sess = ort.InferenceSession(qpath, providers=['CPUExecutionProvider'])
    random.seed(7)
    betas = [0.0, 0.5, 1.0, 1.5, 2.0]
    report, tot = {}, {b: [0, 0, 0] for b in betas}
    for tax in ['burung', 'mamalia', 'reptil', 'amfibi', 'kupu', 'capung', 'ikan', 'bentos', 'tumbuhan', 'serangga']:
        if tax not in deq: continue
        E, rows = deq[tax]
        prior = np.log1p(np.array([r[5] + 3 * r[6] for r in rows], dtype=np.float32))
        cand = [i for i, r in enumerate(rows) if r[7]]
        sample = random.sample(cand, min(40, len(cand)))
        res = {b: [0, 0, 0] for b in betas}
        for i in sample:
            img = fetch(rows[i][7].replace('/square.', '/medium.'))
            if not img: continue
            try: x = preprocess_like_web(Image.open(io.BytesIO(img)))
            except Exception: continue
            sim = (E @ sess.run(None, {'pixel_values': x})[0][0]) * logit
            for b in betas:
                order = np.argsort(-(sim + b * prior))[:5]
                r = res[b]; r[0] += 1; r[1] += int(order[0] == i); r[2] += int(i in order)
        for b in betas:
            for k in range(3): tot[b][k] += res[b][k]
        report[tax] = {str(b): f'top-1 {res[b][1]}/{res[b][0]}, top-5 {res[b][2]}/{res[b][0]}' for b in betas}
        print(f'uji {tax}: ' + ' | '.join(f'beta {b}: {v}' for b, v in report[tax].items()), flush=True)
    best = max(betas, key=lambda b: (tot[b][1] + 0.5 * tot[b][2], -b)) if any(t[0] for t in tot.values()) else 0.0
    report['total'] = {str(b): f'top-1 {tot[b][1]}/{tot[b][0]}, top-5 {tot[b][2]}/{tot[b][0]}' for b in betas}
    report['beta_terpilih'] = best
    print('total:', report['total'], '-> beta', best, flush=True)
    json.dump({'model': 'bioclip', 'logit_scale': logit, 'prior_beta': best, 'taksa': index}, open(os.path.join(DATA, 'emb-index.json'), 'w'), indent=1)
    json.dump(report, open(os.path.join(DATA, 'uji-identifikasi.json'), 'w'), indent=1, ensure_ascii=False)

if __name__ == '__main__':
    main()
