## Spektrogram per Spesies & Lokasi -- Song Meter Micro 2
##
## Untuk tiap spesies yang terdeteksi di tiap lokasi, ambil contoh
## deteksi dengan confidence TERTINGGI, potong klip dari file WAV
## aslinya (sesuai jendela waktu deteksi BirdNET, default 3 detik),
## lalu buat spektrogram -- berguna untuk verifikasi visual manual
## (bandingkan pola suara ke referensi xeno-canto atau literatur),
## terutama untuk spesies yang ditandai MENCURIGAKAN di
## validasi_sebaran_geografis_song_meter.R (mis. kasus Takur Warna-warni).
##
## Hanya 1 contoh terbaik per (lokasi, spesies) yang dibuat -- bukan
## tiap deteksi -- karena totalnya puluhan ribu baris deteksi, 1 contoh
## representatif per spesies sudah cukup untuk verifikasi visual.
##
## Input : hasil_analisis_audio_UT2026/rekap_identifikasi_spesies_semua_lokasi.csv
##         File .wav asli di base_path (F:/Audiomoth/UT 2026)
## Output: hasil_analisis_audio_UT2026/spektrogram/<lokasi>/<nama_ilmiah>.png
##         spektrogram_gagal.csv (kalau ada yang gagal dibuat)

library(tuneR)
library(seewave)

base_path <- "F:/Audiomoth/UT 2026"              # folder utama berisi subfolder per lokasi
dir_hasil <- "F:/Audiomoth/hasil_analisis_audio_UT2026"   # sesuaikan kalau dir_output beda
dir_spektrogram <- file.path(dir_hasil, "spektrogram")
durasi_klip <- 3   # detik, sesuai lebar jendela analisis BirdNET
flim_khz <- c(0, 10)   # rentang frekuensi yang ditampilkan (kHz) -- naikkan kalau spesiesmu bersuara tinggi

df <- read.csv(file.path(dir_hasil, "rekap_identifikasi_spesies_semua_lokasi.csv"), stringsAsFactors = FALSE)
df <- df[!is.na(df$nama_ilmiah), ]

# Ambil 1 contoh terbaik (confidence tertinggi) per kombinasi lokasi+spesies
df <- df[order(-df$confidence), ]
contoh_terbaik <- df[!duplicated(paste(df$kode_lokasi, df$nama_ilmiah)), ]

cat("Akan membuat", nrow(contoh_terbaik), "spektrogram (1 per spesies per lokasi)...\n")

# Indeks file .wav per lokasi (sekali scan per lokasi, bukan per baris -- lebih cepat)
file_index <- list()
for (lokasi in unique(contoh_terbaik$kode_lokasi)) {
  dir_lokasi <- file.path(base_path, lokasi)
  file_index[[lokasi]] <- list.files(dir_lokasi, pattern = "\\.wav$", ignore.case = TRUE,
                                      recursive = TRUE, full.names = TRUE)
}

cari_path_file <- function(kode_lokasi, nama_file) {
  kandidat <- file_index[[kode_lokasi]]
  cocok <- kandidat[basename(kandidat) == nama_file]
  if (length(cocok) == 0) return(NA_character_)
  cocok[1]
}

bersihkan_nama_file <- function(x) gsub("[^A-Za-z0-9_.-]", "_", x)

gagal <- list()

for (i in seq_len(nrow(contoh_terbaik))) {
  baris <- contoh_terbaik[i, ]
  if (i %% 10 == 0) cat("  ", i, "/", nrow(contoh_terbaik), "\n")

  berhasil <- tryCatch({
    path_file <- cari_path_file(baris$kode_lokasi, baris$nama_file)
    if (is.na(path_file)) stop("File audio tidak ditemukan: ", baris$nama_file)

    from <- baris$waktu_mulai_detik
    to <- from + durasi_klip
    wave <- readWave(path_file, from = from, to = to, units = "seconds")

    dir_lokasi_out <- file.path(dir_spektrogram, baris$kode_lokasi)
    dir.create(dir_lokasi_out, showWarnings = FALSE, recursive = TRUE)
    path_png <- file.path(dir_lokasi_out, paste0(bersihkan_nama_file(baris$nama_ilmiah), ".png"))

    judul <- paste0(baris$nama_ilmiah, " (", baris$nama_umum, ")\n",
                     baris$kode_lokasi, " -- ", baris$nama_file, " @ ", from, "-", to, "s",
                     " -- confidence ", round(baris$confidence, 2))

    png(path_png, width = 1000, height = 600, res = 120)
    spectro(wave, flim = flim_khz, main = judul, scale = FALSE, osc = TRUE)
    dev.off()
    TRUE
  }, error = function(e) {
    message("  GAGAL: ", baris$kode_lokasi, " / ", baris$nama_ilmiah, " -- ", conditionMessage(e))
    gagal[[length(gagal) + 1]] <<- data.frame(
      kode_lokasi = baris$kode_lokasi, nama_ilmiah = baris$nama_ilmiah,
      nama_file = baris$nama_file, pesan_error = conditionMessage(e)
    )
    FALSE
  })
}

if (length(gagal) > 0) {
  df_gagal <- do.call(rbind, gagal)
  write.csv(df_gagal, file.path(dir_hasil, "spektrogram_gagal.csv"), row.names = FALSE)
  cat("\n", nrow(df_gagal), "spektrogram gagal dibuat -- lihat spektrogram_gagal.csv\n")
}

cat("\n=== SELESAI ===\n")
cat("Spektrogram tersimpan di:", dir_spektrogram, "(satu subfolder per lokasi)\n")
