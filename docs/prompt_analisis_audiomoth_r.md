# Prompt: Analisis Indeks Akustik Soundscape dari Data Song Meter Micro 2 (R)

*Prompt siap pakai untuk AI assistant di RStudio (atau ChatGPT/Claude
versi lain), sudah terisi lengkap sesuai data Song Meter Micro 2 di
"F:/Audiomoth/UT 2026" -- tinggal salin teks di bawah ini apa adanya
ke AI assistant-mu. (Catatan: repo ini juga sudah punya skrip R jadi
siap pakai di `scripts/r/analisis_akustik_audiomoth.R`, jadi prompt ini
sifatnya cadangan/referensi kalau mau generate ulang atau modifikasi
lewat AI lain.)*

---

```
Saya punya data rekaman suara dari perekam Wildlife Acoustics Song
Meter Micro 2 untuk pemantauan keanekaragaman hayati (soundscape
ecology). Tolong buatkan skrip R lengkap untuk menghitung indeks
akustik dari rekaman tersebut.

KONTEKS DATA:
- Lokasi folder rekaman: "F:/Audiomoth/UT 2026" (path Windows asli:
  F:\Audiomoth\UT 2026 -- pakai forward slash di R supaya tidak perlu
  escape backslash; nama folder "Audiomoth" hanya penamaan folder
  pribadi, bukan nama alat -- alatnya Song Meter Micro 2)
- Format file: .WAV, nama file mengandung timestamp format
  YYYYMMDD_HHMMSS di suatu bagian nama file (boleh ada prefix ID/nama
  alat di depannya)
- Struktur folder: satu subfolder per lokasi/site di dalam
  "F:/Audiomoth/UT 2026" (nama subfolder = kode/nama lokasi). **Tiap
  lokasi harus diolah dan dilaporkan TERPISAH, jangan digabung jadi
  satu angka nasional/rata-rata semua lokasi.**
- Setting perekam (Song Meter Micro 2):
  - Sample rate: 32000 Hz
  - Gain: 18 dB
  - Panjang rekam maksimal: 1 menit per file
  - Duty cycle: rekam 1 menit, jeda 4 menit (siklus 5 menit), aktif
    00:00-23:59 (jadi sekitar 288 file/hari/lokasi)
  Karena tiap file sudah pendek (maks 1 menit), skrip tidak perlu logic
  pemecahan segmen yang rumit -- cukup antisipasi kalau suatu saat ada
  file lebih panjang dari 1 menit.

TUJUAN ANALISIS:
Hitung indeks akustik keragaman (acoustic diversity indices) standar
untuk tiap file rekaman, sebagai proxy aktivitas satwa/keragaman suara:
- ACI (Acoustic Complexity Index)
- ADI (Acoustic Diversity Index)
- AEI (Acoustic Evenness Index)
- NDSI (Normalized Difference Soundscape Index) -- rasio suara
  biofoni vs antropofoni
- BI (Bioacoustic Index)
- H (Acoustic Entropy / total entropy Shannon)

YANG DIBUTUHKAN DARI SKRIP:
1. Package R: pakai `soundecology`, `seewave`, dan `tuneR` (cek apakah
   sudah terinstal, kalau belum beri perintah install.packages()).
2. Fungsi untuk membaca semua file .WAV secara rekursif dari folder,
   lalu parse timestamp dari nama file (format YYYYMMDD_HHMMSS) jadi
   kolom POSIXct menggunakan `lubridate`.
3. Loop/fungsi yang menghitung keenam indeks di atas untuk tiap file,
   dibungkus try/catch supaya file korup/rusak tidak menghentikan
   seluruh proses (perekam kadang menghasilkan file WAV korup saat
   baterai lemah) -- file yang gagal dicatat terpisah, bukan
   menghentikan skrip.
4. Gabungkan hasil jadi satu data frame dengan kolom: nama_file,
   kode_lokasi (ambil otomatis dari nama subfolder), timestamp,
   tanggal, jam, lalu nilai keenam indeks.
5. Simpan hasil ke CSV -- **satu file CSV per lokasi** (mis.
   `hasil_indeks_akustik_[kode_lokasi].csv`), bukan satu CSV gabungan
   semua lokasi. Kalau mau tetap ada CSV gabungan untuk rekap, buat
   sebagai tambahan, bukan pengganti file per-lokasi.
6. Buat visualisasi pakai ggplot2, dibuat **terpisah per lokasi**
   (bukan satu grafik gabungan semua lokasi jadi satu garis rata-rata):
   a. Pola diel per lokasi (rata-rata tiap indeks per jam dalam sehari,
      0-23) -- untuk melihat puncak aktivitas suara (mis. chorus
      subuh/senja) di masing-masing lokasi.
   b. Tren indeks dari waktu ke waktu (time series harian) per lokasi.
   c. (Opsional) satu grafik pembanding antar-lokasi berdampingan
      (facet_wrap per lokasi di ggplot2) supaya tetap bisa dibandingkan
      visual, tapi tetap dengan panel terpisah per lokasi -- bukan
      dirata-rata jadi satu angka.
7. Tulis kode dengan komentar singkat per bagian, modular (fungsi
   terpisah untuk: baca file, hitung indeks, plot), dan tangani path
   file secara relatif memakai `here::here()` kalau project pakai
   RStudio Project / .Rproj.

CATATAN PENTING:
- Rekaman Song Meter Micro 2 saya sudah pendek (maks 1 menit per file,
  sesuai setting alat), jadi tidak wajib dipecah lagi. Tapi tetap
  tambahkan opsi parameter `durasi_segmen_detik` (default 60 detik)
  untuk jaga-jaga kalau suatu saat ada file lebih panjang, karena
  sebagian indeks akustik (ACI dkk) didesain untuk rekaman pendek.
- Kalau folder berisi file dalam jumlah besar (ratusan/ribuan), proses
  bisa lama -- tambahkan progress bar (`pbapply` atau cukup
  `cat()`/`message()` progress tiap N file) supaya saya tahu skrip
  masih berjalan, bukan macet.
- Jangan asumsikan jumlah lokasi/site -- deteksi otomatis dari struktur
  folder atau beri parameter yang bisa saya sesuaikan.
```

---

## Cara pakai

1. Salin seluruh blok kode di atas (dari `Saya punya data...` sampai
   akhir) -- tidak ada lagi bagian yang perlu diisi manual.
2. Tempel ke AI assistant di dalam RStudio (atau ChatGPT/Claude lain
   yang kamu pakai untuk menulis kode R).
3. Review kode yang dihasilkan sebelum dijalankan -- terutama path
   folder dan nama kolom, karena AI assistant generate berdasarkan
   asumsi dari isi prompt ini.

## Referensi package R yang relevan

- [`soundecology`](https://cran.r-project.org/package=soundecology) --
  indeks ACI, ADI, AEI, NDSI, BI siap pakai.
- [`seewave`](https://cran.r-project.org/package=seewave) -- analisis
  sinyal akustik umum, termasuk entropi (`H()`), spektrogram.
- [`tuneR`](https://cran.r-project.org/package=tuneR) -- baca/tulis
  file WAV di R.
- [`warbleR`](https://cran.r-project.org/package=warbleR) -- kalau
  nanti mau lanjut ke deteksi/klasifikasi panggilan spesies tertentu
  (bukan cuma indeks agregat).

Kalau hasil analisisnya nanti mau digabung ke proyek `deha` ini (mis.
dikaitkan dengan lokasi kukang jawa atau burung pantai), kasih tahu
saya datanya dan saya bantu integrasikan ke struktur
`data/raw/` / `scripts/r/` yang sudah ada.
