# QGIS

- `projects/` — simpan file proyek QGIS (`.qgz`/`.qgs`) di sini.
- `styles/` — simpan file style (`.qml`) yang dipakai berulang di beberapa layer/proyek.

## Alur kerja

1. Digitasi atau edit data spasial di QGIS, lalu export layer ke `data/raw/`
   dalam format GeoJSON atau Shapefile.
2. Jalankan `scripts/python/process_geodata.py` untuk membaca dan mengolah
   data tersebut, hasilnya disimpan ke `data/processed/`.
3. Jalankan `scripts/r/analyze_data.R` untuk analisis statistik lanjutan dan
   membuat grafik dari data yang sudah diproses, hasilnya masuk ke `outputs/`.
4. Hasil olahan (CSV/GeoJSON baru) bisa di-import kembali ke QGIS untuk
   divisualisasikan sebagai peta.

## Instalasi

Unduh QGIS versi LTR terbaru dari https://qgis.org/download — tidak ada
dependency tambahan yang perlu diinstal di repo ini untuk QGIS sendiri,
karena ia dijalankan sebagai aplikasi desktop terpisah.
