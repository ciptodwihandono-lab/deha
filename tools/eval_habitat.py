"""Uji tebakan habitat AI (CLIP ViT-B/32, sama dengan Survei KEHATI) pada foto Wikimedia Commons.
Membandingkan daftar kalimat (prompt) lama dan baru. Label benar diambil dari kata kunci pencarian."""
import io, json, sys, time, urllib.error, urllib.parse, urllib.request
import numpy as np, torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

UA = {'User-Agent': 'kehati-habitat-eval/1.0 (GitHub Actions; research test)'}
TPL = ['a photo of {}.', 'a landscape photo of {}.', 'a field survey photo showing {}.']
OLD = {'MG': ['a mangrove forest'], 'MF': ['a muddy tidal mudflat'], 'PP': ['a sandy beach'],
       'VP': ['coastal vegetation with casuarina trees and pandanus'], 'TB': ['an aquaculture fish pond'], 'SW': ['a rice paddy field'],
       'KB': ['a farm field or garden'], 'KS': ['a coconut or oil palm plantation'], 'PM': ['houses in a village'],
       'SG': ['a river or canal'], 'RW': ['a swamp or flooded wetland'], 'SM': ['shrubs and bushes'], 'HT': ['a forest'], 'LT': ['bare open land']}
NEW = json.load(open('tools/ail_prompts_new.json'))['hab']
QUERIES = {  # kelas benar: kata kunci pencarian Commons
  'HT': ['tropical rainforest Borneo', 'hutan hujan tropis Kalimantan', 'rainforest interior Sumatra', 'lowland rainforest Malaysia'],
  'MG': ['mangrove Indonesia', 'mangrove forest roots', 'hutan mangrove'],
  'KS': ['oil palm plantation', 'perkebunan kelapa sawit'],
  'SW': ['sawah padi', 'rice paddy Bali'],
  'PP': ['pantai pasir Indonesia', 'tropical sandy beach'],
  'MF': ['mudflat low tide', 'tidal flat mud'],
  'SG': ['sungai Kalimantan', 'river rainforest Borneo'],
  'RW': ['swamp wetland Sumatra', 'rawa'],
  'SM': ['shrubland bushes', 'semak belukar'],
  'TB': ['tambak udang', 'shrimp pond aquaculture'],
  'PM': ['desa Indonesia rumah', 'village houses Java'],
}
def get(req, tries=5):
  for t in range(tries):
    try: return urllib.request.urlopen(req, timeout=30).read()
    except urllib.error.HTTPError as e:
      if e.code != 429 or t == tries - 1: raise
      time.sleep(5 * (t + 1))
def search(q, n=6):
  time.sleep(1.5)
  u = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({'action': 'query', 'generator': 'search', 'gsrsearch': q + ' filetype:bitmap', 'gsrnamespace': 6, 'gsrlimit': n, 'prop': 'imageinfo', 'iiprop': 'url|mime', 'iiurlwidth': 480, 'format': 'json'})
  d = json.loads(get(urllib.request.Request(u, headers=UA)))
  return [p['imageinfo'][0]['thumburl'] for p in (d.get('query', {}).get('pages', {}) or {}).values() if p.get('imageinfo') and p['imageinfo'][0].get('mime') == 'image/jpeg']
imgs = []
for k, qs in QUERIES.items():
  for q in qs:
    try:
      for url in search(q):
        try:
          b = get(urllib.request.Request(url, headers=UA))
          imgs.append((k, q, url.rsplit('/', 1)[-1][:60], Image.open(io.BytesIO(b)).convert('RGB'))); time.sleep(0.5)
        except Exception as e: print('skip', url, e)
    except Exception as e: print('search fail', q, e)
print('foto:', len(imgs), {k: sum(1 for x in imgs if x[0] == k) for k in QUERIES})
m = CLIPModel.from_pretrained('openai/clip-vit-base-patch32').eval(); proc = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')
def temb(groups):
  keys, vecs = [], []
  for k, ps in groups.items():
    with torch.no_grad():
      x = proc(text=[tp.format(p) for p in ps for tp in TPL], return_tensors='pt', padding=True)
      t = m.text_projection(m.text_model(input_ids=x['input_ids'], attention_mask=x['attention_mask']).pooler_output)
    t = t / t.norm(dim=-1, keepdim=True); v = t.mean(0); keys.append(k); vecs.append((v / v.norm()).numpy())
  return keys, np.stack(vecs)
with torch.no_grad():
  I = torch.cat([m.visual_projection(m.vision_model(pixel_values=proc(images=[x[3] for x in imgs[i:i + 16]], return_tensors='pt')['pixel_values']).pooler_output) for i in range(0, len(imgs), 16)])
I = (I / I.norm(dim=-1, keepdim=True)).numpy()
def evaluate(name, groups, fam):
  keys, T = temb(groups); S = I @ T.T * 100; P = np.exp(S - S.max(1, keepdims=True)); P /= P.sum(1, keepdims=True)
  ok = 0; per = {}; conf = {}
  for (k, q, fn, _), p in zip(imgs, P):
    pk = keys[int(p.argmax())]; good = fam(pk) == k; ok += good; per.setdefault(k, [0, 0]); per[k][0] += good; per[k][1] += 1
    if not good: conf[(k, pk)] = conf.get((k, pk), 0) + 1
  print(f'\n== {name}: benar {ok}/{len(imgs)} = {ok / len(imgs):.0%}')
  for k, (a, n) in per.items(): print(f'  {k}: {a}/{n}')
  print('  salah tebak terbanyak:', sorted(conf.items(), key=lambda x: -x[1])[:10])
  return P, keys
evaluate('LAMA', OLD, lambda k: k)
FOREST = {'HT', 'HS', 'HG'}
P, keys = evaluate('BARU', NEW, lambda k: 'HT' if k in FOREST else k)
# Aturan cek-silang vegetasi (sama dengan aplikasi)
VG = json.load(open('tools/ail_prompts_new.json'))['veg']
vk, VT = temb({x[0] or '(kosong)': [x[1]] for x in VG})
SV = I @ VT.T * 100; PV = np.exp(SV - SV.max(1, keepdims=True)); PV /= PV.sum(1, keepdims=True)
vi = {k: i for i, k in enumerate(vk)}
def rule(p, pv):
  top = keys[int(p.argmax())]
  mg = pv[vi['Mangrove (Avicennia/Rhizophora)']] + pv[vi['Nipah']]
  fo = pv[vi['Pohon hutan besar']] + pv[vi['Liana / rotan']] + pv[vi['Paku-pakuan']]
  if top in FOREST and mg >= 0.45: return 'MG'
  if top == 'MG' and mg < 0.15 and fo >= 0.3: return 'HT'
  return top
ok = 0; per = {}
for (k, q, fn, _), p, pv in zip(imgs, P, PV):
  t = rule(p, pv); t = 'HT' if t in FOREST else t; g = t == k; ok += g; per.setdefault(k, [0, 0]); per[k][0] += g; per[k][1] += 1
print(f'\n== BARU + cek vegetasi: benar {ok}/{len(imgs)} = {ok / len(imgs):.0%}')
for k, (a, n) in per.items(): print(f'  {k}: {a}/{n}')
print('\nRincian HT (hutan) versi baru:')
for (k, q, fn, _), p in zip(imgs, P):
  if k in ('HT', 'MG'): print(f'  [{k}] {fn[:40]:40s} -> ' + ', '.join(f'{keys[i]} {p[i]:.2f}' for i in np.argsort(-p)[:3]))
for g in ('veg', 'sub'):
  G = json.load(open('tools/ail_prompts_new.json'))[g]
  gk, GT = temb({x[0] or '(kosong)': (x[1] if isinstance(x[1], list) else [x[1]]) for x in G})
  S = I @ GT.T * 100; Pg = np.exp(S - S.max(1, keepdims=True)); Pg /= Pg.sum(1, keepdims=True)
  print(f'\n{g} teratas per kelas habitat (rata-rata):')
  for k in QUERIES:
    idx = [i for i, x in enumerate(imgs) if x[0] == k]
    if idx: avg = Pg[idx].mean(0); print(f'  {k}: ' + ', '.join(f'{gk[i]} {avg[i]:.2f}' for i in np.argsort(-avg)[:3]))
