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

## Pemetaan seluruh Indonesia (kecamatan/desa)

Untuk proyek pemetaan skala nasional, lihat
`data/raw/boundaries/README.md` untuk daftar sumber data resmi (BIG, GADM,
Kemendagri) dan cara memasukkannya ke proyek ini. Contoh alur kerja skala
kecil (kecamatan di Kota Yogyakarta) sudah tersedia di
`scripts/python/prepare_boundaries.py` dan `scripts/r/map_indonesia.R` —
struktur yang sama tinggal dipakai ulang saat data nasional sudah tersedia.

Saran praktis untuk skala nasional:

- Gunakan format **GeoPackage (.gpkg)** untuk data batas wilayah, bukan
  GeoJSON — jauh lebih efisien untuk ribuan/puluhan ribu polygon.
- Simpan data mentah nasional di `data/raw/boundaries/` (file besar
  di-gitignore, lihat catatan di sana).
- Sederhanakan geometri (`ms_simplify` di R atau `simplify()` di
  geopandas) sebelum divisualisasikan agar rendering peta tetap cepat.
- Pisahkan proses per provinsi jika data desa nasional terlalu besar untuk
  diproses sekaligus.
