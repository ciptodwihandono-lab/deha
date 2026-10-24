# Peta Survei Pantai Cemara

Aplikasi pemetaan lapangan untuk HP (pendamping aplikasi formulir
`apps/survei-pantai-cemara/`). Bekerja **tanpa sinyal** setelah dibuka sekali
dan memperbarui diri sendiri saat ada sinyal.

Alamat: https://ciptodwihandono-lab.github.io/deha/peta/

## Fitur

- **Peta dasar**: citra satelit Esri World Imagery, OpenStreetMap, atau polos.
  Potongan peta yang pernah tampil disimpan otomatis (maks. ±6000 tile) dan
  tetap tampil tanpa sinyal. Sebelum ke lapangan, buka dan geser area survei
  pada beberapa tingkat zoom saat masih ada sinyal.
- **Posisi saya**: titik biru dengan lingkar akurasi; tombol ◎ untuk mengikuti posisi.
- **+ Tandai**:
  - *Titik di posisi saya (GPS)*: mengambil bacaan GPS terbaik (maks. 15 detik,
    berhenti lebih cepat bila akurasi ≤ 5 m).
  - *Titik dengan ketuk peta*, *Garis*, dan *Area* (ketuk sudut-sudutnya; panjang
    dan luas tampil langsung, ada tombol Urungkan).
- **Rekam jalur**: merekam jalur GPS saat berjalan (titik > ±30 m diabaikan,
  layar dijaga menyala); setelah berhenti tersimpan sebagai garis dan bisa
  dijadikan area.
- **Atribut setiap objek**: habitat (15 kelas, warna di peta), kode otomatis
  (P001/G001/A001), nama lokasi, kondisi, ancaman, vegetasi dominan, deskripsi
  habitat, catatan, dan **foto lokasi** (kamera/galeri; nama, jam, dan GPS otomatis).
- **Daftar**: ringkasan per habitat (jumlah objek, luas area, panjang garis),
  pencarian, dan filter habitat.
- **Layer acuan**: tampilkan batas kawasan atau rencana jalur dari file
  GeoJSON/KML/GPX sebagai garis putus-putus kuning.

## Ekspor

- **ZIP (QGIS)**: `peta_survei.geojson` (titik, garis, area + atribut, CRS
  EPSG:4326), `objek.csv` (lat/lon pusat objek), `peta_survei.gpx`,
  `peta_survei.kml`, `foto/` + `Daftar_Foto.csv`, dan cadangan `.json`.
- **KMZ Google Earth**: dibuka langsung di Google Earth; objek dikelompokkan
  per habitat dengan warna yang sama dan foto tampil di setiap objek.
- **Cadangan .json**: untuk digabung di HP anggota tim lain (tab Data →
  Gabungkan data tim). File foto tidak ikut di .json.

## Catatan teknis

- Satu file `index.html` + `vendor/leaflet.js` (Leaflet 1.9.4, lisensi BSD-2,
  lihat `vendor/LICENSE-leaflet.txt`), tanpa build.
- Data objek di `localStorage` (`peta-survei-v1`), foto dan layer acuan di
  IndexedDB (`peta-survei-foto`).
- Service worker `sw.js` hanya melayani file di folder ini dan tile peta;
  diterbitkan ke `/deha/peta/` oleh `.github/workflows/pages-survei.yml`.
