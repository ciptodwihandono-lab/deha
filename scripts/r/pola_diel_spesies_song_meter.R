## Pola Aktivitas Diel per Spesies -- Song Meter Micro 2 (BirdNET)
##
## Analisis lanjutan #2 untuk laporan ilmiah: heatmap jam aktif (0-23)
## untuk spesies-spesies dengan deteksi terbanyak, per lokasi -- untuk
## melihat pola aktivitas harian (mis. dawn chorus, aktivitas malam).
##
## Pembersihan data sama seperti rekap_spesies_song_meter.R: ambil
## kandidat confidence tertinggi per jendela 3 detik supaya tidak
## dihitung ganda untuk kandidat alternatif di jendela waktu yang sama.
##
## Input : hasil_analisis_audio_UT2026/rekap_identifikasi_spesies_semua_lokasi.csv
## Output: heatmap_diel_<lokasi>.png (top N spesies x jam)
##         pola_diel_spesies_<lokasi>.csv (tabel jumlah deteksi per spesies x jam)

library(ggplot2)

dir_hasil <- "F:/Audiomoth/hasil_analisis_audio_UT2026"   # sesuaikan kalau dir_output beda
path_input <- file.path(dir_hasil, "rekap_identifikasi_spesies_semua_lokasi.csv")
jumlah_top_spesies <- 20   # jumlah spesies teratas yang ditampilkan di heatmap

df <- read.csv(path_input, stringsAsFactors = FALSE)
df$timestamp <- as.POSIXct(df$timestamp, tz = "UTC")

# -- Bersihkan: buang jendela tanpa deteksi, ambil confidence tertinggi per jendela
df <- df[!is.na(df$nama_ilmiah), ]
df$kunci_jendela <- paste(df$kode_lokasi, df$nama_file, df$waktu_mulai_detik, sep = "||")
df <- df[order(df$kunci_jendela, -df$confidence), ]
df_bersih <- df[!duplicated(df$kunci_jendela), ]
df_bersih$jam <- as.integer(format(df_bersih$timestamp, "%H"))

daftar_lokasi <- unique(df_bersih$kode_lokasi)

for (lokasi in daftar_lokasi) {
  df_lokasi <- df_bersih[df_bersih$kode_lokasi == lokasi, ]

  # Pilih top N spesies berdasarkan total deteksi di lokasi ini
  total_per_spesies <- aggregate(confidence ~ nama_umum, data = df_lokasi, FUN = length)
  names(total_per_spesies)[2] <- "total"
  total_per_spesies <- total_per_spesies[order(-total_per_spesies$total), ]
  top_spesies <- head(total_per_spesies$nama_umum, jumlah_top_spesies)

  df_top <- df_lokasi[df_lokasi$nama_umum %in% top_spesies, ]

  # Tabel jumlah deteksi per spesies x jam (termasuk kombinasi 0, biar heatmap lengkap)
  tabel_diel <- aggregate(confidence ~ nama_umum + jam, data = df_top, FUN = length)
  names(tabel_diel)[3] <- "jumlah_deteksi"
  grid_lengkap <- expand.grid(nama_umum = top_spesies, jam = 0:23)
  tabel_diel <- merge(grid_lengkap, tabel_diel, by = c("nama_umum", "jam"), all.x = TRUE)
  tabel_diel$jumlah_deteksi[is.na(tabel_diel$jumlah_deteksi)] <- 0

  write.csv(tabel_diel, file.path(dir_hasil, paste0("pola_diel_spesies_", lokasi, ".csv")), row.names = FALSE)

  # Urutkan spesies di sumbu-y berdasarkan total deteksi (paling aktif di atas)
  tabel_diel$nama_umum <- factor(tabel_diel$nama_umum, levels = rev(top_spesies))

  p <- ggplot(tabel_diel, aes(x = jam, y = nama_umum, fill = jumlah_deteksi)) +
    geom_tile(color = "white", linewidth = 0.3) +
    scale_fill_gradient(low = "#fff7ec", high = "#7f0000") +
    scale_x_continuous(breaks = seq(0, 23, 3)) +
    labs(
      title = paste0("Pola Aktivitas Diel -- ", jumlah_top_spesies, " Spesies Teratas -- ", lokasi),
      subtitle = "1 deteksi per jendela 3 detik (confidence tertinggi)",
      x = "Jam (0-23)", y = NULL, fill = "Jumlah\ndeteksi"
    ) +
    theme_minimal() +
    theme(panel.grid = element_blank())

  ggsave(file.path(dir_hasil, paste0("heatmap_diel_", lokasi, ".png")), p, width = 10, height = 7, dpi = 150)
}

cat("=== SELESAI ===\n")
cat("Heatmap & tabel pola diel per spesies tersimpan di:", dir_hasil, "\n")
