# deha

Proyek multi-tool untuk analisis geospasial, data science, dan riset
lingkungan/pertanian. Menggabungkan QGIS, Python, R, dan Node.js/TypeScript
dalam satu struktur yang saling terhubung.

## Struktur proyek

```
deha/
├── data/
│   ├── raw/          # data mentah (mis. export dari QGIS)
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

## Setup tiap tool

### Python

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 scripts/python/process_geodata.py
```

### R / RStudio

```bash
Rscript scripts/r/install.R      # install dependency sekali saja
Rscript scripts/r/analyze_data.R
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
