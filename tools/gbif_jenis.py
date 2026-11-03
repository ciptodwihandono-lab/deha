"""Menyusun daftar jenis Indonesia per kelompok taksa dari GBIF untuk aplikasi Survei KEHATI.

Sumber: catatan kejadian (occurrence) GBIF dengan country=ID, tanpa fosil dan tanpa spesimen hidup
(kebun raya/kebun binatang), dikelompokkan per jenis (speciesKey). Untuk tiap jenis diambil nama ilmiah,
famili, nama daerah bahasa Indonesia dan Inggris (bila ada di GBIF), serta kategori IUCN.
Hasil: apps/survei-kehati/data/jenis-<taksa>.json. Hanya memakai pustaka bawaan Python.
"""
import json, os, sys, time, datetime, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

API = 'https://api.gbif.org/v1'
OUT = os.path.join(os.path.dirname(__file__), '..', 'apps', 'survei-kehati', 'data')
BASIS = ['HUMAN_OBSERVATION', 'PRESERVED_SPECIMEN', 'MACHINE_OBSERVATION', 'OBSERVATION', 'MATERIAL_SAMPLE', 'OCCURRENCE', 'MATERIAL_CITATION']
# (kelompok aplikasi, [(nama takson GBIF, rank)], batas jumlah jenis)
GROUPS = [
    ('burung', [('Aves', 'CLASS')], None),
    ('mamalia', [('Mammalia', 'CLASS')], None),
    ('reptil', [('Squamata', 'ORDER'), ('Testudines', 'ORDER'), ('Crocodylia', 'ORDER')], None),
    ('amfibi', [('Amphibia', 'CLASS')], None),
    ('kupu', [(f, 'FAMILY') for f in ['Papilionidae', 'Pieridae', 'Nymphalidae', 'Lycaenidae', 'Hesperiidae', 'Riodinidae']], None),
    ('capung', [('Odonata', 'ORDER')], None),
    ('ikan', [('Actinopterygii', 'CLASS'), ('Elasmobranchii', 'CLASS')], 9000),
    ('bentos', [('Decapoda', 'ORDER'), ('Gastropoda', 'CLASS'), ('Bivalvia', 'CLASS')], 8000),
    ('tumbuhan', [('Tracheophyta', 'PHYLUM')], 30000),
    ('serangga', [('Insecta', 'CLASS')], 8000),   # terakhir: jenis yang sudah masuk kupu/capung dilewati
]

def get(path, params=None, tries=5):
    url = API + path + ('?' + urllib.parse.urlencode(params, doseq=True) if params else '')
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'survei-kehati-checklist/1.0'}), timeout=60) as r:
                return json.load(r)
        except Exception as e:
            if i == tries - 1:
                print('GAGAL', url, e, file=sys.stderr); return None
            time.sleep(2 ** i)

def key_of(name, rank):
    r = get('/species/match', {'name': name, 'rank': rank, 'strict': 'true'})
    k = r and r.get('usageKey')
    print(f'  {name} ({rank}) -> {k}')
    return k

def species_counts(taxon_key):
    out, off = {}, 0
    while True:
        r = get('/occurrence/search', {'country': 'ID', 'taxonKey': taxon_key, 'basisOfRecord': BASIS, 'occurrenceStatus': 'PRESENT',
                                       'facet': 'speciesKey', 'facetLimit': 1000, 'facetOffset': off, 'limit': 0})
        counts = (r or {}).get('facets', [{}])[0].get('counts', []) if r and r.get('facets') else []
        for c in counts: out[int(c['name'])] = out.get(int(c['name']), 0) + c['count']
        if len(counts) < 1000: return out
        off += 1000

def detail(key):
    sp = get(f'/species/{key}') or {}
    if sp.get('rank') != 'SPECIES': return None
    ind = eng = ''
    v = get(f'/species/{key}/vernacularNames', {'limit': 200}) or {}
    for x in v.get('results', []):
        lang, nm = (x.get('language') or '').lower(), (x.get('vernacularName') or '').strip()
        if not nm: continue
        if lang in ('ind', 'id') and not ind: ind = nm
        if lang in ('eng', 'en') and not eng: eng = nm
    iucn = (get(f'/species/{key}/iucnRedListCategory') or {}).get('code', '') or ''
    if iucn in ('NE', 'NA'): iucn = ''
    return [sp.get('canonicalName') or sp.get('species') or '', ind[:60], (eng or sp.get('vernacularName') or '')[:60], sp.get('family') or '', iucn]

def main():
    os.makedirs(OUT, exist_ok=True)
    only = set(sys.argv[1:])
    seen = set()
    summary = {}
    for tax, taxa, cap in GROUPS:
        if only and tax not in only: continue
        print(f'== {tax}', flush=True)
        counts = {}
        for name, rank in taxa:
            k = key_of(name, rank)
            if k:
                for s, c in species_counts(k).items(): counts[s] = counts.get(s, 0) + c
        keys = [k for k, _ in sorted(counts.items(), key=lambda kv: -kv[1]) if k not in seen]
        if cap: keys = keys[:cap]
        print(f'  {len(keys)} jenis, mengambil rincian…', flush=True)
        t0 = time.time()
        with ThreadPoolExecutor(24) as ex: det = list(ex.map(detail, keys))
        rows = []
        for k, d in zip(keys, det):
            if d and d[0]:
                rows.append(d + [counts[k]]); seen.add(k)
        rows.sort(key=lambda r: -r[5])
        with open(os.path.join(OUT, f'jenis-{tax}.json'), 'w', encoding='utf-8') as f:
            json.dump({'tax': tax, 'sumber': 'GBIF.org, catatan kejadian di Indonesia (country=ID)', 'dibuat': datetime.date.today().isoformat(),
                       'kolom': ['nama_ilmiah', 'nama_indonesia', 'nama_inggris', 'famili', 'iucn', 'jumlah_catatan'], 'rows': rows}, f, ensure_ascii=False, separators=(',', ':'))
        summary[tax] = len(rows)
        print(f'  selesai {len(rows)} jenis dalam {time.time() - t0:.0f} dtk; nama Indonesia: {sum(1 for r in rows if r[1])}; IUCN: {sum(1 for r in rows if r[4])}', flush=True)
    print(json.dumps(summary))

if __name__ == '__main__':
    main()
