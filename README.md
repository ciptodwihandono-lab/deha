# deha

Proyek multi-tool untuk analisis geospasial, data science, dan riset
lingkungan/pertanian. Menggabungkan QGIS, Python, R, dan Node.js/TypeScript
dalam satu struktur yang saling terhubung.

## Struktur proyek

```
deha/
├── data/
│   ├── raw/          # data mentah (mis. export dari QGIS)
│   │   ├── boundaries/  # batas wilayah administrasi (provinsi/kab/kec/desa)
│   │   └── observations/  # observasi lapangan (mis. kukang jawa + vegetasi)
│   ├── processed/    # data hasil olahan Python
│   └── external/     # data dari sumber luar (API, download, dll.)
├── qgis/
│   ├── projects/     # file proyek QGIS (.qgz/.qgs)
│   └── styles/       # file style (.qml) yang dipakai berulang
├── scripts/
│   ├── python/       # pemrosesan data spasial (geopandas, rasterio, dll.)
│   └── r/            # analisis statistik dan visualisasi (tidyverse, sf)
├── notebooks/        # Jupyter notebook untuk eksplorasi data
├── outputs/
│   ├── figures/      # grafik/peta hasil analisis
│   └── reports/      # ringkasan/laporan hasil (CSV, dll.)
├── docs/             # dokumentasi tambahan proyek
└── src/              # aplikasi/tooling Node.js/TypeScript
```

## Alur kerja (contoh)

```
QGIS (digitasi/edit) → data/raw/*.geojson
    → scripts/python/process_geodata.py → data/processed/*.csv
        → scripts/r/analyze_data.R → outputs/figures/, outputs/reports/
```

Contoh yang sudah disiapkan: `data/raw/sample_points.geojson` (titik kota di
Indonesia) diproses `scripts/python/process_geodata.py` menjadi
`data/processed/sample_processed.csv`, lalu dianalisis
`scripts/r/analyze_data.R` menjadi ringkasan dan grafik di `outputs/`.

## Pemetaan seluruh Indonesia (batas wilayah)

Untuk proyek pemetaan skala nasional (provinsi/kabupaten/kecamatan/desa),
ada alur kerja kedua yang menghubungkan data batas wilayah, Python, dan R:

```
data/raw/boundaries/*.geojson (atau .gpkg untuk skala nasional)
    → scripts/python/prepare_boundaries.py → data/processed/*.geojson + .csv
        → scripts/r/map_indonesia.R → outputs/figures/*.png (peta choropleth)
```

Contoh yang sudah disiapkan: 13 kecamatan di Kota Yogyakarta
(`data/raw/boundaries/yogyakarta_kecamatan.geojson`) diproses jadi peta
kepadatan penduduk (data atribut simulasi) di
`outputs/figures/peta_kecamatan_yogyakarta.png`. Ini contoh skala kecil
untuk membuktikan alur kerjanya — lihat `data/raw/boundaries/README.md`
untuk sumber data resmi (BIG, GADM, Kemendagri) saat sudah siap memperluas
ke cakupan kecamatan/desa seluruh Indonesia.

## Observasi kukang jawa & vegetasi

Alur kerja ketiga untuk data survei satwa/vegetasi lapangan (koordinat dari
catatan lapangan + foto):

```
data/raw/observations/vegetasi_kukang_jawa.csv (isi koordinat_dms + foto)
    → scripts/python/convert_coordinates.py → data/processed/*.geojson
        → scripts/r/map_vegetasi_kukang.R → outputs/figures/*.png
```

Lihat `data/raw/observations/README.md` untuk format pengisian data dan
daftar spesies pohon pakan/pohon tidur kukang jawa sebagai acuan.

## Setup tiap tool

### Python

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 scripts/python/process_geodata.py
python3 scripts/python/prepare_boundaries.py
python3 scripts/python/convert_coordinates.py
```

### R / RStudio

```bash
Rscript scripts/r/install.R      # install dependency sekali saja
Rscript scripts/r/analyze_data.R
Rscript scripts/r/map_indonesia.R
Rscript scripts/r/map_vegetasi_kukang.R
```

Bisa juga dibuka langsung di RStudio dengan membuka folder proyek ini
sebagai working directory.

### QGIS

Lihat `qgis/README.md` untuk detail penyimpanan file proyek dan alur
kerjanya. QGIS dijalankan sebagai aplikasi desktop terpisah (unduh dari
https://qgis.org/download), tidak ada instalasi tambahan di repo ini.

### Node.js/TypeScript

```bash
npm install
npm run dev    # run src/index.ts directly
npm run build  # compile to dist/
npm start      # run compiled output
npm test       # run tests
```

## Kontak

**Cipto Dwi Handono**
Email: ciptodwihandono@gmail.com
HP: 0811369099
