## Tabel Spesies Terdeteksi per Lokasi -- Nama Ilmiah, Indonesia, Inggris
##
## CATATAN PENTING soal nama Indonesia: BirdNET TIDAK punya nama umum
## Bahasa Indonesia (dicek langsung lewat available_languages() --
## daftar bahasa yang didukung: af, ar, cs, da, de, en_uk, en_us, es,
## fi, fr, hu, it, ja, ko, nl, no, pl, pt, ro, ru, sk, sl, sv, th, tr,
## uk, zh -- tidak ada "id"). Nama Inggris (nama_inggris) diambil apa
## adanya dari hasil BirdNET (kolom nama_umum).
##
## Nama Indonesia di sini dicocokkan dari tabel referensi 235 spesies
## burung air/pantai proyek AWC Indonesia 2026 (berdasarkan nama
## ilmiah). CAKUPAN TERBATAS: referensi itu khusus burung air/pantai,
## jadi spesies burung hutan/non-air (kemungkinan besar banyak di
## lokasi Sumbergondo, hutan dataran tinggi) TIDAK akan ketemu
## padanannya -- nama_indonesia akan kosong (NA), bukan ditebak. Untuk
## baris yang kosong, cek manual lewat aplikasi Burungnesia/eBird atau
## buku panduan lapangan (mis. MacKinnon "Burung-burung di Sumatera,
## Jawa, Bali, dan Kalimantan").
##
## Input : hasil_analisis_audio_UT2026/rekap_spesies_<lokasi>.csv
##         (dari rekap_spesies_song_meter.R -- jalankan itu dulu kalau
##         belum ada)
##         Referensi nama Indonesia diunduh otomatis dari repo GitHub
##         (butuh koneksi internet).
## Output: tabel_spesies_lengkap_<lokasi>.csv (per lokasi)
##         tabel_spesies_lengkap_semua_lokasi.csv (gabungan)

dir_hasil <- "F:/Audiomoth/hasil_analisis_audio_UT2026"   # sesuaikan kalau dir_output beda
url_referensi_id <- "https://raw.githubusercontent.com/ciptodwihandono-lab/deha/claude/claude-rc-9bhjno/data/processed/awc_rekap_semua_spesies.csv"

referensi <- read.csv(url_referensi_id, stringsAsFactors = FALSE)
referensi_id <- unique(referensi[, c("nama_ilmiah", "nama_indonesia")])

file_rekap <- list.files(dir_hasil, pattern = "^rekap_spesies_.*\\.csv$", full.names = TRUE)

if (length(file_rekap) == 0) {
  stop("Tidak ditemukan file rekap_spesies_<lokasi>.csv -- jalankan rekap_spesies_song_meter.R dulu.")
}

tabel_semua <- do.call(rbind, lapply(file_rekap, function(f) {
  lokasi <- sub("^rekap_spesies_(.*)\\.csv$", "\\1", basename(f))
  d <- read.csv(f, stringsAsFactors = FALSE)
  d <- merge(d, referensi_id, by = "nama_ilmiah", all.x = TRUE)
  data.frame(
    kode_lokasi = lokasi,
    nama_ilmiah = d$nama_ilmiah,
    nama_indonesia = d$nama_indonesia,
    nama_inggris = d$nama_umum,
    jumlah_deteksi = d$jumlah_deteksi,
    stringsAsFactors = FALSE
  )
}))

tabel_semua <- tabel_semua[order(tabel_semua$kode_lokasi, -tabel_semua$jumlah_deteksi), ]
write.csv(tabel_semua, file.path(dir_hasil, "tabel_spesies_lengkap_semua_lokasi.csv"), row.names = FALSE)

for (lokasi in unique(tabel_semua$kode_lokasi)) {
  write.csv(tabel_semua[tabel_semua$kode_lokasi == lokasi, ],
            file.path(dir_hasil, paste0("tabel_spesies_lengkap_", lokasi, ".csv")), row.names = FALSE)
}

n_total <- nrow(tabel_semua)
n_ada_nama_id <- sum(!is.na(tabel_semua$nama_indonesia))

cat("=== SELESAI ===\n")
cat(n_ada_nama_id, "dari", n_total, "baris punya nama Indonesia (cocok dengan referensi burung air/pantai AWC).\n")
cat(n_total - n_ada_nama_id, "baris TIDAK ketemu nama Indonesia -- kemungkinan besar spesies non-air/hutan, perlu dicek manual.\n")
cat("File tersimpan di:", dir_hasil, "\n")

cat("\nSpesies yang BELUM ada nama Indonesia:\n")
print(unique(tabel_semua[is.na(tabel_semua$nama_indonesia), c("nama_ilmiah", "nama_inggris")]))
