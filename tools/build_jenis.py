"""Menyusun daftar jenis Indonesia per kelompok taksa untuk aplikasi Survei KEHATI.

Sumber:
  1. iNaturalist: jenis yang teramati di Indonesia (species_counts, place = Indonesia) beserta nama Indonesia
     (locale=id), nama Inggris, foto contoh, dan jumlah pengamatan.
  2. GBIF: catatan kejadian dengan country=ID (tanpa fosil dan spesimen hidup kebun raya/kebun binatang),
     dikelompokkan per jenis; ditambah taksonomi lengkap, kategori IUCN, dan nama Indonesia dari GBIF.
Hasil:
  apps/survei-kehati/data/jenis-<taksa>.json   (dipakai aplikasi)
  build/taxo-<taksa>.json                       (taksonomi lengkap, untuk embedding BioCLIP; tidak diterbitkan)
Hanya memakai pustaka bawaan Python.
"""
import json, os, sys, time, datetime, urllib.request, urllib.parse, urllib.error
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'apps', 'survei-kehati', 'data')
BUILD = os.path.join(ROOT, 'build')
TAXO_DIR = os.path.join(ROOT, 'tools', 'taxo')   # taksonomi lengkap per jenis (untuk teks BioCLIP), disimpan di repo
GBIF = 'https://api.gbif.org/v1'
INAT = 'https://api.inaturalist.org/v1'
UA = {'User-Agent': 'survei-kehati-checklist/1.1 (https://github.com/ciptodwihandono-lab/deha)'}
BASIS = ['HUMAN_OBSERVATION', 'PRESERVED_SPECIMEN', 'MACHINE_OBSERVATION', 'OBSERVATION', 'MATERIAL_SAMPLE', 'OCCURRENCE', 'MATERIAL_CITATION']
# kelompok aplikasi: takson GBIF [(nama, rank)], takson iNaturalist [(nama, rank)], batas jumlah jenis
GROUPS = [
    ('burung', [('Aves', 'CLASS')], [('Aves', 'class')], None),
    ('mamalia', [('Mammalia', 'CLASS')], [('Mammalia', 'class')], None),
    ('reptil', [('Squamata', 'ORDER'), ('Testudines', 'ORDER'), ('Crocodylia', 'ORDER')], [('Reptilia', 'class')], None),
    ('amfibi', [('Amphibia', 'CLASS')], [('Amphibia', 'class')], None),
    ('kupu', [(f, 'FAMILY') for f in ['Papilionidae', 'Pieridae', 'Nymphalidae', 'Lycaenidae', 'Hesperiidae', 'Riodinidae']], [('Papilionoidea', 'superfamily')], None),
    ('capung', [('Odonata', 'ORDER')], [('Odonata', 'order')], None),
    ('ikan', [('Actinopterygii', 'CLASS'), ('Elasmobranchii', 'CLASS')], [('Actinopterygii', 'class'), ('Elasmobranchii', 'subclass')], 9000),
    ('bentos', [('Decapoda', 'ORDER'), ('Gastropoda', 'CLASS'), ('Bivalvia', 'CLASS')], [('Decapoda', 'order'), ('Gastropoda', 'class'), ('Bivalvia', 'class')], 8000),
    ('tumbuhan', [('Tracheophyta', 'PHYLUM')], [('Tracheophyta', 'phylum')], 15000),
    ('serangga', [('Insecta', 'CLASS')], [('Insecta', 'class')], 6000),   # setelah kupu/capung: jenis yang sudah masuk dilewati
    ('lain', [('Arachnida', 'CLASS'), ('Fungi', 'KINGDOM'), ('Cnidaria', 'PHYLUM'), ('Echinodermata', 'PHYLUM'), ('Cephalopoda', 'CLASS')],
             [('Arachnida', 'class'), ('Fungi', 'kingdom'), ('Cnidaria', 'phylum'), ('Echinodermata', 'phylum'), ('Cephalopoda', 'class')], 6000),
]

def get(base, path, params=None, tries=6, pause=0):
    url = base + path + ('?' + urllib.parse.urlencode(params, doseq=True) if params else '')
    for i in range(tries):
        try:
            if pause: time.sleep(pause)
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429 and e.code < 500: return None   # mis. 404 = jenis belum dinilai IUCN: bukan galat, jangan diulang
            if i == tries - 1:
                print('GAGAL', url, e, file=sys.stderr); return None
            time.sleep(min(30, 2 ** (i + 1)))
        except Exception as e:
            if i == tries - 1:
                print('GAGAL', url, e, file=sys.stderr); return None
            time.sleep(min(30, 2 ** (i + 1)))

# ---------- iNaturalist ----------
def inat_place():
    r = get(INAT, '/places/autocomplete', {'q': 'Indonesia', 'per_page': 20}, pause=1) or {}
    for p in r.get('results', []):
        if p.get('admin_level') == 0 and p.get('name') == 'Indonesia':
            return p['id']
    return 6966

def inat_taxon(name, rank):
    r = get(INAT, '/taxa', {'q': name, 'rank': rank, 'per_page': 30}, pause=1) or {}
    for t in r.get('results', []):
        if t.get('name') == name and t.get('rank') == rank:
            return t['id']
    return None

def inat_species(place, taxon_id, locale):
    # Nama Indonesia: locale=id dengan preferred_place Indonesia. Nama Inggris: locale=en TANPA preferred_place,
    # karena dengan preferred_place iNaturalist memberi nama lokal Indonesia walau locale=en.
    out, page = {}, 1
    while True:
        r = get(INAT, '/observations/species_counts', {'place_id': place, 'taxon_id': taxon_id, 'verifiable': 'true', 'rank': 'species',
                                                      'locale': locale, **({'preferred_place_id': place} if locale == 'id' else {}), 'per_page': 500, 'page': page}, pause=1.1) or {}
        res = r.get('results', [])
        for x in res:
            t = x.get('taxon') or {}
            if t.get('rank') != 'species' or not t.get('name'): continue
            ph = (t.get('default_photo') or {}).get('square_url') or ''
            out[t['name']] = {'n': x.get('count', 0), 'name': (t.get('preferred_common_name') or '').strip(), 'photo': ph, 'id': t.get('id')}
        total = r.get('total_results', 0)
        if not res or page * 500 >= min(total, 10000): return out
        page += 1

# ---------- GBIF ----------
def gbif_key(name, rank):
    r = get(GBIF, '/species/match', {'name': name, 'rank': rank, 'strict': 'true'})
    return r and r.get('usageKey')

def gbif_counts(taxon_key):
    out, off = {}, 0
    while True:
        r = get(GBIF, '/occurrence/search', {'country': 'ID', 'taxonKey': taxon_key, 'basisOfRecord': BASIS, 'occurrenceStatus': 'PRESENT',
                                             'facet': 'speciesKey', 'facetLimit': 1000, 'facetOffset': off, 'limit': 0})
        counts = (r or {}).get('facets', [{}])[0].get('counts', []) if r and r.get('facets') else []
        for c in counts: out[int(c['name'])] = out.get(int(c['name']), 0) + c['count']
        if len(counts) < 1000: return out
        off += 1000

TAXO = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus']
LIGHT = {'tumbuhan', 'serangga', 'lain'}   # kelompok besar: cukup satu permintaan per jenis (tanpa nama daerah GBIF dan IUCN)
CUR = {'light': False}
def gbif_detail(key):
    sp = get(GBIF, f'/species/{key}') or {}
    if sp.get('rank') != 'SPECIES': return None
    if CUR['light']:
        return {'sci': sp.get('canonicalName') or sp.get('species') or '', 'ind': '', 'eng': '', 'iucn': '', **{k: sp.get(k) or '' for k in TAXO}}
    ind = eng = ''
    v = get(GBIF, f'/species/{key}/vernacularNames', {'limit': 200}) or {}
    for x in v.get('results', []):
        lang, nm = (x.get('language') or '').lower(), (x.get('vernacularName') or '').strip()
        if nm and lang in ('ind', 'id') and not ind: ind = nm
        if nm and lang in ('eng', 'en') and not eng: eng = nm
    iucn = (get(GBIF, f'/species/{key}/iucnRedListCategory') or {}).get('code', '') or ''
    if iucn in ('NE', 'NA'): iucn = ''
    return {'sci': sp.get('canonicalName') or sp.get('species') or '', 'ind': ind, 'eng': eng, 'iucn': iucn, **{k: sp.get(k) or '' for k in TAXO}}

def gbif_match(sci):
    r = get(GBIF, '/species/match', {'name': sci, 'rank': 'SPECIES'}) or {}
    if r.get('matchType') in (None, 'NONE') or r.get('rank') != 'SPECIES': return None
    key = r.get('acceptedUsageKey') or r.get('usageKey')
    return key

def refresh_names(place, tax, itaxa, d, out_file):
    """Perbarui nama Indonesia/Inggris dari iNaturalist tanpa mengubah urutan baris (embedding tetap cocok)."""
    ids, ens = {}, {}
    for name, rank in itaxa:
        tid = inat_taxon(name, rank)
        if tid: ids.update(inat_species(place, tid, 'id')); ens.update(inat_species(place, tid, 'en'))
    n = 0
    for r in d['rows']:
        ia, ie = ids.get(r[0], {}), ens.get(r[0], {})
        nid, nen = (ia.get('name') or '').strip(), (ie.get('name') or '').strip()
        if nen: r[2] = nen[:70]
        if nid and nid.lower() != (nen or r[2]).lower(): r[1] = nid[:70]; n += 1
        elif r[1] and r[2] and r[1].lower() == r[2].lower() and nen and nen.lower() != r[1].lower(): pass
    with open(out_file, 'w', encoding='utf-8') as f: json.dump(d, f, ensure_ascii=False, separators=(',', ':'))
    print(f'  {tax}: nama Indonesia {sum(1 for r in d["rows"] if r[1])} dari {len(d["rows"])} jenis', flush=True)

def main():
    os.makedirs(OUT, exist_ok=True); os.makedirs(BUILD, exist_ok=True); os.makedirs(TAXO_DIR, exist_ok=True)
    only = set(sys.argv[1:])
    place = inat_place(); print('iNaturalist place Indonesia =', place, flush=True)
    seen, summary, seen_sci = set(), {}, set()
    force = os.environ.get('JENIS_ULANG') == '1'
    for tax, gtaxa, itaxa, cap in GROUPS:
        out_file = os.path.join(OUT, f'jenis-{tax}.json')
        if (only and tax not in only) or (not force and os.path.exists(out_file) and os.path.exists(os.path.join(TAXO_DIR, f'taxo-{tax}.json'))):
            if os.path.exists(out_file):   # kelompok yang sudah ada dilewati; namanya dicatat agar tidak terulang (mis. kupu di serangga)
                d = json.load(open(out_file, encoding='utf-8'))
                seen_sci.update(r[0] for r in d['rows'])
                if os.environ.get('JENIS_NAMA', '1') == '1' and not (only and tax not in only):
                    refresh_names(place, tax, itaxa, d, out_file)
            print(f'== {tax}: sudah ada, dilewati (nama diperbarui)', flush=True); continue
        CUR['light'] = tax in LIGHT
        t0 = time.time(); print(f'== {tax}', flush=True)
        # iNaturalist (nama Indonesia + Inggris + foto)
        inat_id, inat_en = {}, {}
        for name, rank in itaxa:
            tid = inat_taxon(name, rank); print(f'  iNat {name} -> {tid}', flush=True)
            if not tid: continue
            inat_id.update(inat_species(place, tid, 'id')); inat_en.update(inat_species(place, tid, 'en'))
        # GBIF
        counts = {}
        for name, rank in gtaxa:
            k = gbif_key(name, rank); print(f'  GBIF {name} -> {k}', flush=True)
            if k:
                for s, c in gbif_counts(k).items(): counts[s] = counts.get(s, 0) + c
        keys = [k for k, _ in sorted(counts.items(), key=lambda kv: -kv[1]) if k not in seen]
        if cap: keys = keys[:cap]
        print(f'  GBIF {len(keys)} jenis, iNat {len(inat_en)} jenis; mengambil rincian…', flush=True)
        with ThreadPoolExecutor(24) as ex:
            det = []
            for i, d in enumerate(ex.map(gbif_detail, keys)):
                det.append(d)
                if i and i % 2000 == 0: print(f'    {i}/{len(keys)} jenis, {time.time() - t0:.0f} dtk', flush=True)
        by_sci = {}
        for k, d in zip(keys, det):
            if d and d['sci']: d['gbif'] = counts[k]; d['key'] = k; by_sci[d['sci']] = d
        # Jenis yang hanya ada di iNaturalist: cocokkan ke GBIF untuk taksonomi
        extra = [s for s in inat_en if s not in by_sci]
        with ThreadPoolExecutor(16) as ex: mk = list(ex.map(gbif_match, extra))
        mk_keys = [k for k in mk if k and k not in seen]
        with ThreadPoolExecutor(24) as ex: det2 = list(ex.map(gbif_detail, mk_keys))
        for k, d in zip(mk_keys, det2):
            if d and d['sci'] and d['sci'] not in by_sci: d['gbif'] = counts.get(k, 0); d['key'] = k; by_sci[d['sci']] = d
        key_sci = {d['key']: sci for sci, d in by_sci.items()}
        alias = {}   # nama terima GBIF -> nama yang dipakai iNaturalist (bila berbeda/sinonim)
        for sn, k in zip(extra, mk):
            if k and k in key_sci and key_sci[k] != sn: alias.setdefault(key_sci[k], sn)
        rows, taxo = [], []
        for sci, d in by_sci.items():
            if d['key'] in seen or sci in seen_sci: continue
            isci = sci if sci in inat_en else alias.get(sci, sci)
            ia, ie = inat_id.get(isci, {}), inat_en.get(isci, {})
            en = ie.get('name') or d['eng']
            idn = ia.get('name') if ia.get('name') and ia.get('name') != ie.get('name') else d['ind']
            rows.append([sci, (idn or '')[:70], (en or '')[:70], d['family'], d['iucn'], d['gbif'], ie.get('n', 0), ie.get('photo', '')])
            taxo.append([sci, en or '', d['kingdom'], d['phylum'], d['class'], d['order'], d['family'], d['genus']])
            seen.add(d['key'])
        order = sorted(range(len(rows)), key=lambda i: -(rows[i][5] + 3 * rows[i][6]))
        rows = [rows[i] for i in order]; taxo = [taxo[i] for i in order]
        with open(os.path.join(OUT, f'jenis-{tax}.json'), 'w', encoding='utf-8') as f:
            json.dump({'tax': tax, 'sumber': 'GBIF.org (catatan di Indonesia) dan iNaturalist (pengamatan di Indonesia)', 'dibuat': datetime.date.today().isoformat(),
                       'kolom': ['nama_ilmiah', 'nama_indonesia', 'nama_inggris', 'famili', 'iucn', 'catatan_gbif', 'pengamatan_inat', 'foto_inat'], 'rows': rows},
                      f, ensure_ascii=False, separators=(',', ':'))
        with open(os.path.join(TAXO_DIR, f'taxo-{tax}.json'), 'w', encoding='utf-8') as f:
            json.dump(taxo, f, ensure_ascii=False, separators=(',', ':'))
        summary[tax] = len(rows)
        print(f'  selesai {len(rows)} jenis dalam {time.time() - t0:.0f} dtk; nama Indonesia {sum(1 for r in rows if r[1])}; IUCN {sum(1 for r in rows if r[4])}; foto {sum(1 for r in rows if r[7])}', flush=True)
    print(json.dumps(summary))

if __name__ == '__main__':
    main()
