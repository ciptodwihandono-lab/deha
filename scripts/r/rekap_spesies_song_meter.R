## Rekap Kekayaan & Keragaman Spesies -- Song Meter Micro 2 (BirdNET)
##
## Analisis lanjutan dari hasil analisis_lengkap_audio_UT2026.R. Membangun
## daftar spesies (checklist), kekayaan (richness), dan indeks keragaman
## Shannon-Wiener per lokasi -- fondasi tabel utama untuk laporan ilmiah.
##
## PEMBERSIHAN DATA: tiap jendela 3 detik BirdNET bisa punya lebih dari
## satu baris (beberapa kandidat spesies sekaligus untuk waktu yang sama).
## Di sini hanya kandidat dengan confidence TERTINGGI per jendela yang
## dipakai, supaya satu jendela waktu = satu deteksi spesies (presence),
## bukan dihitung berkali-kali untuk kandidat alternatif.
##
## CATATAN: status konservasi (IUCN/nasional) BELUM disertakan di sini
## karena belum ada tabel referensi status spesies di proyek ini (beda
## dengan data AWC burung pantai yang sumbernya sudah menyertakan status
## IUCN). Kalau mau ditambahkan, perlu tabel referensi terpisah (mis.
## checklist IUCN per nama ilmiah) -- kasih tahu kalau mau dibantu siapkan.
##
## Input : hasil_analisis_audio_UT2026/rekap_identifikasi_spesies_semua_lokasi.csv
## Output: rekap_spesies_<lokasi>.csv (per lokasi)
##         daftar_spesies_checklist.csv (semua lokasi, format wide)
##         ringkasan_kekayaan_spesies.csv (richness & Shannon-Wiener per lokasi)
##         plot_top_spesies_bersih_<lokasi>.png

library(ggplot2)

dir_hasil <- "F:/Audiomoth/hasil_analisis_audio_UT2026"   # sesuaikan kalau dir_output beda
path_input <- file.path(dir_hasil, "rekap_identifikasi_spesies_semua_lokasi.csv")

df <- read.csv(path_input, stringsAsFactors = FALSE)

# -- Bersihkan: buang jendela tanpa deteksi, ambil confidence tertinggi per jendela
df <- df[!is.na(df$nama_ilmiah), ]
df$kunci_jendela <- paste(df$kode_lokasi, df$nama_file, df$waktu_mulai_detik, sep = "||")
df <- df[order(df$kunci_jendela, -df$confidence), ]
df_bersih <- df[!duplicated(df$kunci_jendela), ]

cat("Baris mentah (sebelum bersih):", nrow(df), "\n")
cat("Baris bersih (1 deteksi per jendela):", nrow(df_bersih), "\n")

# -- Rekap per lokasi: jumlah deteksi per spesies
rekap_per_lokasi <- function(df_lokasi) {
  rekap <- aggregate(confidence ~ nama_ilmiah + nama_umum, data = df_lokasi, FUN = length)
  names(rekap)[3] <- "jumlah_deteksi"
  rekap$proporsi <- rekap$jumlah_deteksi / sum(rekap$jumlah_deteksi)
  rekap[order(-rekap$jumlah_deteksi), ]
}

daftar_lokasi <- unique(df_bersih$kode_lokasi)
rekap_semua <- list()

for (lokasi in daftar_lokasi) {
  df_lokasi <- df_bersih[df_bersih$kode_lokasi == lokasi, ]
  rekap <- rekap_per_lokasi(df_lokasi)
  rekap_semua[[lokasi]] <- rekap
  write.csv(rekap, file.path(dir_hasil, paste0("rekap_spesies_", lokasi, ".csv")), row.names = FALSE)

  top15 <- head(rekap, 15)
  p <- ggplot(top15, aes(x = reorder(nama_umum, jumlah_deteksi), y = jumlah_deteksi)) +
    geom_col(fill = "#1565c0") + coord_flip() +
    labs(title = paste("Top 15 Spesies (Bersih) --", lokasi),
         subtitle = "1 deteksi per jendela 3 detik (confidence tertinggi)",
         x = NULL, y = "Jumlah deteksi") +
    theme_minimal()
  ggsave(file.path(dir_hasil, paste0("plot_top_spesies_bersih_", lokasi, ".png")), p, width = 9, height = 6, dpi = 150)
}

# -- Checklist spesies format wide (lokasi jadi kolom, untuk tabel laporan)
checklist <- do.call(rbind, lapply(names(rekap_semua), function(lokasi) {
  d <- rekap_semua[[lokasi]]
  d$kode_lokasi <- lokasi
  d
}))
checklist_wide <- reshape(
  checklist[, c("nama_ilmiah", "nama_umum", "kode_lokasi", "jumlah_deteksi")],
  idvar = c("nama_ilmiah", "nama_umum"), timevar = "kode_lokasi", direction = "wide"
)
names(checklist_wide) <- gsub("jumlah_deteksi\\.", "jumlah_deteksi_", names(checklist_wide))
kolom_lokasi <- grep("^jumlah_deteksi_", names(checklist_wide), value = TRUE)
checklist_wide[kolom_lokasi][is.na(checklist_wide[kolom_lokasi])] <- 0
checklist_wide <- checklist_wide[order(checklist_wide$nama_ilmiah), ]
write.csv(checklist_wide, file.path(dir_hasil, "daftar_spesies_checklist.csv"), row.names = FALSE)

# -- Kekayaan (richness) & Shannon-Wiener per lokasi
hitung_diversitas <- function(rekap) {
  p <- rekap$jumlah_deteksi / sum(rekap$jumlah_deteksi)
  S <- nrow(rekap)
  H <- -sum(p * log(p))
  J <- if (S > 1) H / log(S) else NA
  data.frame(kekayaan_spesies = S, total_deteksi = sum(rekap$jumlah_deteksi), shannon_H = H, evenness_J = J)
}

ringkasan <- do.call(rbind, lapply(names(rekap_semua), function(lokasi) {
  cbind(kode_lokasi = lokasi, hitung_diversitas(rekap_semua[[lokasi]]))
}))
write.csv(ringkasan, file.path(dir_hasil, "ringkasan_kekayaan_spesies.csv"), row.names = FALSE)

cat("\n=== SELESAI ===\n")
print(ringkasan)
cat("\nFile tersimpan di:", dir_hasil, "\n")
