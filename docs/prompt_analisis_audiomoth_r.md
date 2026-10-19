# Prompt: Analisis Indeks Akustik Soundscape dari Data AudioMoth (R)

*Prompt siap pakai untuk AI assistant di RStudio (atau ChatGPT/Claude
versi lain), ditulis berdasarkan konteks proyek biodiversitas di repo
`deha`. Isi bagian [DALAM KURUNG SIKU] sebelum paste, lalu tempel
seluruh teks di bawah ini ke AI assistant-mu.*

---

```
Saya punya data rekaman suara dari perangkat AudioMoth untuk pemantauan
keanekaragaman hayati (soundscape ecology). Tolong buatkan skrip R
lengkap untuk menghitung indeks akustik dari rekaman tersebut.

KONTEKS DATA:
- Lokasi folder rekaman: [ISI PATH FOLDER, mis. "data/raw/audiomoth/"]
- Format file: .WAV mentah dari AudioMoth, nama file mengikuti konvensi
  bawaan AudioMoth: YYYYMMDD_HHMMSS.WAV (contoh: 20260115_060000.WAV)
- Struktur folder: [JELASKAN, mis. "satu folder per lokasi/site, nama
  folder = kode lokasi" ATAU "semua file dalam satu folder, lokasi
  dibedakan dari prefix nama file"]
- Durasi tiap rekaman: [ISI, mis. "60 detik per file" atau "durasi
  bervariasi, mis. rekaman kontinu per jam"]
- Sample rate: [ISI JIKA TAHU, mis. "48000 Hz" -- kalau tidak tahu,
  minta skrip membaca otomatis dari header WAV]

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
   seluruh proses (AudioMoth kadang menghasilkan file WAV korup saat
   baterai lemah) -- file yang gagal dicatat terpisah, bukan
   menghentikan skrip.
4. Gabungkan hasil jadi satu data frame: nama_file, timestamp, tanggal,
   jam, [kode_lokasi jika ada dari struktur folder], lalu nilai keenam
   indeks.
5. Simpan hasil ke CSV.
6. Buat 2 visualisasi pakai ggplot2:
   a. Pola diel (rata-rata tiap indeks per jam dalam sehari, 0-23) --
      untuk melihat puncak aktivitas suara (mis. chorus subuh/senja).
   b. Tren indeks dari waktu ke waktu (time series harian), dengan
      garis terpisah per lokasi kalau ada lebih dari satu lokasi.
7. Tulis kode dengan komentar singkat per bagian, modular (fungsi
   terpisah untuk: baca file, hitung indeks, plot), dan tangani path
   file secara relatif memakai `here::here()` kalau project pakai
   RStudio Project / .Rproj.

CATATAN PENTING:
- Rekaman AudioMoth bisa berdurasi panjang (kontinu per jam) -- kalau
  durasi file lebih dari ~2-3 menit, pecah dulu jadi segmen pendek
  (mis. per 1 menit) sebelum hitung indeks, karena sebagian indeks
  akustik (ACI dkk) didesain untuk rekaman pendek. Tolong tambahkan
  opsi parameter `durasi_segmen_detik` di skrip untuk ini.
- Kalau folder berisi file dalam jumlah besar (ratusan/ribuan), proses
  bisa lama -- tambahkan progress bar (`pbapply` atau cukup
  `cat()`/`message()` progress tiap N file) supaya saya tahu skrip
  masih berjalan, bukan macet.
- Jangan asumsikan jumlah lokasi/site -- deteksi otomatis dari struktur
  folder atau beri parameter yang bisa saya sesuaikan.
```

---

## Cara pakai

1. Isi bagian `[DALAM KURUNG SIKU]` di atas sesuai struktur data
   AudioMoth-mu (lokasi folder, apakah per-lokasi, durasi rekaman).
2. Salin seluruh blok kode di atas (dari `Saya punya data...` sampai
   akhir).
3. Tempel ke AI assistant di dalam RStudio (atau ChatGPT/Claude lain
   yang kamu pakai untuk menulis kode R).
4. Review kode yang dihasilkan sebelum dijalankan -- terutama path
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
