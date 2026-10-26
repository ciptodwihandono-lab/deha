# Aplikasi Survei Lanjutan KEE Mangrove Pantai Cemara

Aplikasi formulir lapangan untuk HP. Formulirnya mengikuti
`Paket_Dokumen_Final_Monitoring_Pantai_Cemara_Okt2026.pdf` (Form A–F4). Bekerja **tanpa sinyal**
setelah dibuka sekali, dan semua data tersimpan di HP.

## Isi aplikasi

| Tab | Isi |
| --- | --- |
| **Form** | Tombol catat cepat (temuan ancaman C3, perjumpaan primata F6) dan 12 formulir: A, B1, B2, C1, C2, D1, D2, E1, E2, F2, F3, F4. Setiap lembar punya kepala lembar dan tabel baris. Lembar lama dari form yang tidak dipakai lagi (Kamera Jebak F1, KEHATI desa G1) tetap bisa dibuka dan diekspor |
| **Rekap** | Tabel ala tally sheet: jenis × waktu, sektor, aktivitas, titik, atau tanggal, dengan garis tally, Total, dan Maks (perkiraan populasi). Untuk B1, B3, B4, F4, F5, F6, F7, E2. Bisa diunduh CSV atau dicetak/simpan PDF |
| **Data** | Nama pencatat, ekspor ZIP (CSV per tabel + cadangan .json), bagikan ke WhatsApp/Drive, gabungkan data tim |

Fitur lapangan:

- **Koordinat otomatis**: setiap lembar dan baris data baru langsung mengambil
  posisi GPS HP (desimal + akurasi). Tombol **Ambil GPS** mengulangnya di tempat
  yang tepat; koordinat juga bisa diketik manual.
- Kolom **Hari ke-** di Form A terisi otomatis H1–H4 untuk 28–31 Okt 2026.
- **Track GPS** (Form A, C1, F3, tidak wajib) bisa diisi dua cara:
  **Rekam GPS HP** saat berjalan, atau **Unggah GPX/KML** hasil Garmin atau
  aplikasi lain (OsmAnd, Avenza, Locus). Untuk keduanya, panjang transek dan, untuk batas
  area, luas (ha) dihitung otomatis; nama file track, jam mulai, dan jam
  selesai ikut terisi. Titik dengan akurasi lebih buruk dari ±30 m dan
  loncatan kecil di bawah 4 m diabaikan. Layar dibuat tetap menyala selama
  merekam; mengunci layar atau pindah aplikasi menghentikan perekaman titik.
- Tombol **Kini** mengisi jam saat ini.
- **Ambil foto lokasi** di setiap lembar dan **Ambil foto** di setiap baris membuka kamera HP; foto disimpan di aplikasi
  (diperkecil ke 2560 px) dengan nama, jam, dan koordinat GPS otomatis (bila GPS
  tidak menjawab, foto memakai koordinat baris).
  Ekspor ZIP memuat folder `foto/` beserta `Daftar_Foto.csv` dan
  `titik_foto.geojson`. File cadangan .json tidak memuat foto.
- Kode formulir (PN/PT/MS/ST, MM/IS/TB/TG, dll.) tampil sebagai tombol, tidak perlu mengetik.
- Daftar nama burung pantai dan ikan muncul sebagai saran saat mengetik.
- **Simpan + baris baru** membawa sektor dan aktivitas ke baris berikutnya (B1).
- Total individu per jenis langsung terlihat di Form B1.
- Kepadatan Uca/m² (D2) dihitung otomatis.
- Peringatan untuk nilai di luar kisaran wajar (pH, suhu, salinitas, % tutupan, arah kompas).
- Tema **Malam** (merah redup) untuk VES dan spotlight buaya.

## Cara memasang di HP

1. Aktifkan GitHub Pages sekali: repo → **Settings → Pages → Source: GitHub Actions**.
   Workflow `.github/workflows/pages-survei.yml` menerbitkan folder ini setiap
   ada perubahan di branch utama repo (atau jalankan manual dari tab Actions).
2. Buka alamat Pages di Chrome HP **saat masih ada sinyal**, lalu pilih menu ⋮ →
   **Tambahkan ke layar utama**.
3. Izinkan akses lokasi saat pertama kali menekan "Ambil GPS".

Setelah itu aplikasi bisa dibuka dari layar utama walau tanpa sinyal.
Hosting statis lain (Netlify Drop, server kantor) juga bisa: unggah isi folder
ini apa adanya. GPS dan mode offline hanya jalan lewat `https://`.

## Pembaruan otomatis

Aplikasi selalu dibuka dari simpanan di HP (cepat, juga tanpa sinyal). Saat
ada sinyal, aplikasi memeriksa server ketika dibuka, ketika kembali ke
aplikasi, dan tiap 15 menit. Bila `index.html` atau file lain di folder ini
berubah di GitHub Pages, versi baru diunduh dan aplikasi memuat ulang sendiri.
Bila sedang mengisi lembar atau merekam track, yang muncul hanya tombol
**Perbarui** agar pekerjaan tidak terganggu. Tidak perlu instal ulang dan
tidak perlu menaikkan nomor versi apa pun. Data survei tidak terpengaruh.

## Menjaga data tetap aman

Data tersimpan di browser HP masing-masing. **Setiap malam** buka tab Data →
**Bagikan ZIP** dan kirim ke WhatsApp/Drive. Jangan menghapus data browser
Chrome sebelum ekspor.

Untuk menyatukan data tim: satu orang membuka tab Data → **Pilih file
cadangan…** dan memilih file `.json` dari anggota lain. Lembar yang sama tidak
akan terduplikasi.

## Format ekspor

ZIP berisi satu CSV per tabel, mis. `Form_B1_hitung.csv`, `Form_D1_air.csv`:

- satu baris per baris data; kolom kepala lembar diberi awalan `h_`;
- koordinat dipecah menjadi `_lat`, `_lon`, `_akurasi_m` (siap dimuat ke QGIS
  sebagai *delimited text*, CRS EPSG:4326);
- angka memakai titik desimal; pilihan ganda dipisah `; `;
- kode tetap sama dengan formulir kertas (mis. `IS`, `PT`);
- `Status_Kegiatan.csv` dan `Jadwal.csv` hanya ada bila pernah diisi di versi sebelumnya;
- folder `track/` berisi satu file `.gpx` per track dan
  `semua_track.geojson` (garis + poligon area) untuk langsung dibuka di QGIS.

File CSV bisa disimpan ke `data/raw/observations/` untuk diolah dengan skrip
Python/R di repo ini.

## Versi aplikasi Android (APK)

Untuk aplikasi Android sungguhan (bukan pintasan web), lihat
`apps/android/README.md`. Tautan unduh APK terbaru:
https://github.com/ciptodwihandono-lab/deha/releases/download/apk-latest/survei-cemara.apk
