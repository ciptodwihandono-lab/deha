# Peta Survei Pantai Cemara

Aplikasi pemetaan lapangan untuk HP, setara aplikasi GIS lapangan seperti
QField, SW Maps, atau Locus GIS, dalam bahasa Indonesia. Aplikasi ini
pendamping aplikasi formulir `apps/survei-pantai-cemara/`. Bekerja **tanpa
sinyal** setelah dibuka sekali, dan memperbarui diri sendiri saat ada sinyal.

Alamat: https://ciptodwihandono-lab.github.io/deha/peta/

## Fitur

**Peta dan peta offline**
- Peta dasar online: citra satelit Esri World Imagery atau OpenStreetMap.
  Bagian peta yang pernah tampil tersimpan otomatis (maksimal ±6000 tile).
- **Peta offline penuh**: impor file **MBTiles** atau **ZIP tile `{z}/{x}/{y}`**,
  format yang sama dengan QField/Locus. Tile disalin ke penyimpanan HP. Di luar
  cakupan peta offline, citra online atau yang tersimpan tetap tampil.
- Panel **Lapisan**: pilih peta dasar, impor peta offline, tampilkan atau
  sembunyikan objek, label kode, dan layer acuan.
- **Layer acuan**: batas kawasan atau rencana jalur dari GeoJSON/KML/GPX.

**GPS dan koordinat**
- Indikator kualitas GPS di bar atas (hijau ≤ 5 m, kuning ≤ 15 m, merah).
- Panel koordinat langsung: **UTM WGS 84** (mis. `48M 429923 mT 9870676 mU`),
  derajat desimal, atau derajat-menit-detik. Ketuk panel untuk berganti format.
- **Titik GPS rata-rata**: 10 bacaan berbobot 1/akurasi², bacaan > 20 m
  diabaikan. Ketelitian dan sebaran tercatat di atribut.
- Navigasi ke objek: jarak dan arah kompas (derajat dan U/TL/T/…) dengan garis
  panduan di peta.

**Digitasi**
- Titik, garis, dan area dengan ketuk peta atau **tanda silang di tengah layar**
  ("+ Titik tengah") untuk penempatan presisi.
- **Rekam** jalur GPS (titik > ±30 m diabaikan, layar dijaga menyala).
- **Ubah bentuk / geser titik**: seret titik sudut, ketuk untuk menghapus,
  ketuk peta untuk menyisipkan, dengan tombol urungkan.
- **Alat ukur** jarak, keliling, dan luas (tidak disimpan).

**Atribut dan foto**
- Tombol **Foto** di layar peta: kamera langsung terbuka, foto menjadi titik baru
  di posisi GPS (atau di tengah peta bila GPS belum siap), lalu formulirnya terbuka.
- Habitat (15 kelas berwarna), kode otomatis P/G/A###, nama lokasi, kondisi,
  ancaman, vegetasi dominan, deskripsi, catatan.
- **Foto lokasi** dari kamera atau galeri, diperkecil ke 2560 px, dengan GPS saat memotret.
- Tab **Objek**: ringkasan (jumlah, hektar, km, foto), tabel per habitat,
  pencarian, filter, dan jarak dari posisi Anda.

## Ekspor

- **Paket lengkap (ZIP)**:
  - Shapefile `shp/titik|garis|area` (WGS 84, atribut UTF-8, kolom UTM);
  - `peta_survei.geojson`, `peta_survei.kml`, `peta_survei.gpx`;
  - `objek.csv` (lat/lon dan UTM);
  - `foto/` dengan `Daftar_Foto.csv`;
  - cadangan `.json`.
- **Shapefile** saja (ZIP) dan **KMZ Google Earth** dengan foto di setiap objek.
- **Cadangan .json** untuk digabung di HP anggota tim lain.

## Membuat peta offline (QGIS)

1. Tambahkan citra di QGIS: XYZ Tiles Esri Satellite (lihat
   `docs/basemap_satelit_esri.md`), citra drone sendiri, atau Sentinel-2.
2. Perbesar peta ke area survei.
3. Processing Toolbox → Raster tools → **Generate XYZ tiles (MBTiles)**.
4. Extent: kanvas peta; zoom 12–17 (18 untuk detail; tiap tingkat ±4× lebih
   besar); format JPG, kualitas 75.
5. Pindahkan file `.mbtiles` ke HP, lalu di aplikasi pilih Lapisan → Impor peta offline.

Hormati ketentuan penyedia citra. Untuk laporan resmi, citra drone sendiri atau
Sentinel-2 (lisensi terbuka) paling aman.

## Catatan teknis

- `index.html` satu file, dengan `vendor/leaflet.js` (Leaflet 1.9.4, BSD-2) dan
  `vendor/sql-wasm.js|.wasm` (sql.js 1.10.3, MIT; dimuat hanya saat impor MBTiles).
- Penyimpanan:
  - data objek di `localStorage` (`peta-survei-v1`);
  - foto, layer acuan, dan tile peta offline di IndexedDB (`peta-survei-foto` v2:
    `foto`, `thumb`, `ref`, `maps`, `tiles`).
- UTM dihitung dengan seri Krüger. Hasil uji dibandingkan dengan pyproj
  (EPSG:32748) dan selisihnya < 1 cm. Shapefile tervalidasi dengan pyshp, dan
  cincin poligon searah jarum jam.
- Service worker `sw.js` hanya melayani file di folder ini dan tile online.
  Situs diterbitkan ke `/deha/peta/` oleh `.github/workflows/pages-survei.yml`.
