# Panduan QGIS: Peta Lokasi Bird Banding KRMMA (dengan Citra Satelit)

Panduan untuk membangun ulang layout peta "gaya jurnal ilmiah" yang
sudah dibuat di Python (`scripts/python/peta_lokasi_bird_banding.py`),
tapi di QGIS komputermu sendiri -- supaya bisa pakai citra satelit asli
(tidak bisa diakses dari sandbox Claude).

## Bahan yang sudah disiapkan

- **Titik lokasi**: `data/raw/bird_banding/lokasi_bird_banding.geojson`
  (4 titik KRMMA01-04, siap drag-drop ke QGIS, sudah ada semua atribut:
  kode, nama lokasi, kecamatan, tanggal, waktu, catatan, nama file foto)
- **Foto lapangan**: `data/raw/bird_banding/photos/KRMMA*.jpg`
  (4 foto, nama file sudah sesuai kolom `nama_file_foto` di GeoJSON)

## Langkah 1 — Muat titik & basemap satelit

1. Buka QGIS → **Layer → Add Layer → Add Vector Layer** → pilih
   `lokasi_bird_banding.geojson`
2. Tambahkan basemap satelit: panel **Browser** → klik kanan **XYZ
   Tiles** → **New Connection** → Name `Esri Satellite`, URL:
   ```
   https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}
   ```
3. Double-click koneksi itu untuk memuatnya, taruh **di bawah** layer titik
4. Zoom ke area Gunung Anyar Tambak/Medokan Ayu (klik kanan layer titik
   → **Zoom to Layer**) — karena titiknya cuma berjarak ±150m, zoom
   sampai skala besar (mis. 1:1.000 - 1:2.000) untuk lihat detail jalur
   mangrove/tambaknya

## Langkah 2 — Styling titik

1. Klik kanan layer titik → **Properties → Symbology**
2. Pilih simbol **Triangle**, warna merah (`#c0392b`), outline putih
3. Tab **Labels** → Single Labels → field `kode_lokasi`, font tebal,
   warna merah, tambahkan **Buffer** putih supaya terbaca di atas citra

## Langkah 3 — Print Layout (layout akhir untuk dicetak/ekspor)

1. **Project → New Print Layout**, pilih ukuran A3 Landscape (karena
   ada 4 panel foto, A4 akan terlalu sempit)
2. **Add Item → Add Map** — gambar kotak peta utama di bagian
   atas/kiri layout, arahkan ke area klaster titik (ikuti tampilan
   citra satelit yang sudah di-zoom di Langkah 1)
3. **Add Item → Add Legend** — otomatis ambil dari layer yang aktif
   (atau edit manual item legenda, hapus yang tidak perlu)
4. **Add Item → Add Scale Bar** dan **Add Item → Add North Arrow** —
   taruh di pojok peta
5. **Add Item → Add Attribute Table** (opsional, untuk tabel koordinat
   otomatis dari atribut GeoJSON) — atau buat tabel manual dengan
   **Add Item → Add Table**

## Langkah 4 — Tambah panel foto (bagian yang beda dari peta biasa)

QGIS tidak punya "panel foto per titik" otomatis dalam satu layout
statis, jadi ditambahkan manual:

1. **Add Item → Add Picture**, gambar kotak di baris bawah layout
2. Di panel **Item Properties** sebelah kanan, bagian **Main
   Properties → Image Source**, klik tombol folder, pilih
   `data/raw/bird_banding/photos/KRMMA01.jpg`
3. Atur **Placement** ke "Zoom" atau "Fill" biar foto memenuhi kotak
   tanpa gepeng (sesuaikan rasio kotak dengan rasio foto ~4:3)
4. Ulangi untuk KRMMA02-1, KRMMA03, KRMMA04 di 3 kotak foto berikutnya
   sejajar di baris yang sama
5. Di bawah tiap kotak foto, **Add Item → Add Label**, isi teks manual
   (kode, lokasi, tanggal/waktu, catatan — bisa copy dari atribut di
   `lokasi_bird_banding.geojson`)

**Alternatif lebih otomatis (kalau titiknya nanti bertambah banyak)**:
pakai fitur **Atlas** QGIS (Layout → Atlas Settings, Coverage layer =
layer titik) supaya QGIS otomatis generate satu halaman per titik
(peta zoom ke titik itu + bisa tambah expression `@atlas_featurenumber`
untuk judul) -- cocok kalau nanti titik KRMMA bertambah jadi puluhan,
tidak perlu susun manual satu-satu.

## Langkah 5 — Ekspor

**Layout → Export as Image** (PNG, atur resolusi 300 dpi) atau
**Export as PDF** (lebih baik untuk kualitas cetak/lampiran dokumen resmi).

## Kalau sudah jadi

Kirim hasil ekspornya ke saya — saya bisa bantu cek, kasih masukan, atau
kalau perlu bantu susun ulang jadi versi final (tambah elemen yang
kurang, dsb) dari situ.
