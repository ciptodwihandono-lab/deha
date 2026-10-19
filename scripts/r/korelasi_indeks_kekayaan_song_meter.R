## Korelasi Indeks Akustik vs Kekayaan Spesies -- Song Meter Micro 2
##
## Analisis lanjutan #4 untuk laporan ilmiah: uji apakah indeks akustik
## (ACI/ADI/AEI/NDSI/BI/H) berkorelasi dengan kekayaan spesies hasil
## BirdNET per file -- semacam validasi apakah indeks akustik bisa
## dipakai sebagai proxy cepat untuk biodiversitas tanpa identifikasi
## spesies penuh.
##
## Korelasi Spearman dipakai (non-parametrik, tidak mengasumsikan
## hubungan linear/data normal -- lebih sesuai untuk data count seperti
## kekayaan spesies).
##
## Input : hasil_analisis_audio_UT2026/rekap_indeks_akustik_semua_lokasi.csv
##         hasil_analisis_audio_UT2026/rekap_identifikasi_spesies_semua_lokasi.csv
## Output: hasil_korelasi_indeks_kekayaan.csv (koefisien & p-value per indeks)
##         scatter_korelasi_indeks_kekayaan.png

library(ggplot2)

dir_hasil <- "F:/Audiomoth/hasil_analisis_audio_UT2026"   # sesuaikan kalau dir_output beda

df_indeks <- read.csv(file.path(dir_hasil, "rekap_indeks_akustik_semua_lokasi.csv"), stringsAsFactors = FALSE)

df_spesies <- read.csv(file.path(dir_hasil, "rekap_identifikasi_spesies_semua_lokasi.csv"), stringsAsFactors = FALSE)
df_spesies <- df_spesies[!is.na(df_spesies$nama_ilmiah), ]
df_spesies$kunci_jendela <- paste(df_spesies$kode_lokasi, df_spesies$nama_file, df_spesies$waktu_mulai_detik, sep = "||")
df_spesies <- df_spesies[order(df_spesies$kunci_jendela, -df_spesies$confidence), ]
df_spesies_bersih <- df_spesies[!duplicated(df_spesies$kunci_jendela), ]

kekayaan_per_file <- aggregate(nama_ilmiah ~ kode_lokasi + nama_file, data = df_spesies_bersih,
                                FUN = function(x) length(unique(x)))
names(kekayaan_per_file)[3] <- "kekayaan_spesies_file"

df_gabung <- merge(df_indeks, kekayaan_per_file, by = c("kode_lokasi", "nama_file"), all.x = TRUE)
df_gabung$kekayaan_spesies_file[is.na(df_gabung$kekayaan_spesies_file)] <- 0

variabel_indeks <- c("ACI", "ADI", "AEI", "NDSI", "BI", "H")

hasil_korelasi <- do.call(rbind, lapply(variabel_indeks, function(var) {
  uji <- suppressWarnings(cor.test(df_gabung[[var]], df_gabung$kekayaan_spesies_file, method = "spearman"))
  data.frame(
    indeks = var, rho_spearman = unname(uji$estimate), p_value = uji$p.value,
    signifikan_0.05 = uji$p.value < 0.05
  )
}))
hasil_korelasi <- hasil_korelasi[order(-abs(hasil_korelasi$rho_spearman)), ]

write.csv(hasil_korelasi, file.path(dir_hasil, "hasil_korelasi_indeks_kekayaan.csv"), row.names = FALSE)

df_panjang <- reshape(
  df_gabung[, c("kode_lokasi", "kekayaan_spesies_file", variabel_indeks)],
  varying = variabel_indeks, v.names = "nilai_indeks", timevar = "indeks",
  times = variabel_indeks, direction = "long"
)

p <- ggplot(df_panjang, aes(x = nilai_indeks, y = kekayaan_spesies_file)) +
  geom_point(aes(color = kode_lokasi), alpha = 0.4, size = 1) +
  geom_smooth(method = "loess", se = TRUE, color = "black", linewidth = 0.6) +
  facet_wrap(~indeks, scales = "free_x") +
  labs(title = "Korelasi Indeks Akustik vs Kekayaan Spesies per File",
       subtitle = "Kekayaan spesies = jumlah spesies unik terdeteksi BirdNET per file",
       x = "Nilai indeks", y = "Kekayaan spesies per file", color = "Lokasi") +
  theme_minimal()

ggsave(file.path(dir_hasil, "scatter_korelasi_indeks_kekayaan.png"), p, width = 11, height = 7, dpi = 150)

cat("=== SELESAI ===\n")
print(hasil_korelasi)
cat("\nFile tersimpan di:", dir_hasil, "\n")
