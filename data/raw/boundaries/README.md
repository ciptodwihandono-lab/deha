# Data batas wilayah (boundaries)

## Contoh yang sudah disiapkan

- `diy_kabupaten.geojson` — 5 kabupaten/kota di Provinsi DI Yogyakarta.
- `yogyakarta_kecamatan.geojson` — 13 kecamatan di Kota Yogyakarta.

Sumber: [thetrisatria/geojson-indonesia](https://github.com/thetrisatria/geojson-indonesia)
(geometri berbasis OpenStreetMap, disederhanakan). Dipakai sebagai bukti alur
kerja skala kecil sebelum diperluas ke seluruh Indonesia.

**Catatan:** file di atas hanya contoh kecil untuk latihan alur kerja
(QGIS/Python/R). Jangan dipakai sebagai data resmi untuk publikasi.

## Sumber data resmi untuk cakupan seluruh Indonesia

Data batas kecamatan/desa untuk seluruh Indonesia berukuran besar (ribuan
hingga puluhan ribu polygon) dan sebaiknya diunduh langsung dari sumber
resmi berikut, lalu diletakkan di folder ini (tidak lewat sandbox ini karena
domainnya diblokir oleh kebijakan jaringan sandbox):

1. **BIG (Badan Informasi Geospasial)** — https://tanahair.indonesia.go.id/
   Portal resmi RBI (Rupa Bumi Indonesia), tersedia batas administrasi
   sampai level desa/kelurahan. Perlu registrasi akun gratis.
2. **Kemendagri — Permendagri kode wilayah** — kode & nama wilayah
   administrasi resmi (provinsi/kabupaten/kecamatan/desa), berguna untuk
   join atribut ke geometri. Lihat juga rekap tidak resmi di
   https://github.com/yusufsyaifudin/wilayah-indonesia (kode wilayah saja,
   tanpa geometri).
3. **GADM** — https://gadm.org/download_country.html (pilih "Indonesia")
   Batas administrasi hingga level kecamatan (level 3), format GeoPackage/
   Shapefile. Lisensi non-komersial, bukan sumber resmi pemerintah.

## Cara memasukkan data nasional ke proyek ini

1. Unduh data dari salah satu sumber di atas (disarankan format
   GeoPackage `.gpkg`, lebih efisien daripada GeoJSON untuk data besar).
2. Simpan di folder ini, mis. `data/raw/boundaries/indonesia_kecamatan.gpkg`.
3. Sesuaikan `INPUT_PATH` di `scripts/python/prepare_boundaries.py` dan
   `input_path` di `scripts/r/map_indonesia.R` ke file tersebut.
4. File besar (>50MB) sebaiknya tidak di-commit ke git biasa — gunakan
   Git LFS, atau simpan di penyimpanan terpisah dan cukup dokumentasikan
   sumbernya di sini.
