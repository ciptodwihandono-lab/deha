## Perbandingan Antar Lokasi -- Song Meter Micro 2
##
## Analisis lanjutan #3 untuk laporan ilmiah: uji statistik (Wilcoxon
## rank-sum / Mann-Whitney U -- non-parametrik, tidak perlu asumsi
## normalitas) untuk membandingkan indeks akustik dan kekayaan spesies
## per file antara lokasi.
##
## Kekayaan spesies per file dihitung dari hasil BirdNET yang sudah
## dibersihkan (confidence tertinggi per jendela 3 detik), lalu
## digabung dengan tabel indeks akustik berdasarkan kode_lokasi+nama_file.
## File tanpa deteksi spesies dihitung kekayaan = 0 (bukan dibuang).
##
## Input : hasil_analisis_audio_UT2026/rekap_indeks_akustik_semua_lokasi.csv
##         hasil_analisis_audio_UT2026/rekap_identifikasi_spesies_semua_lokasi.csv
## Output: hasil_uji_perbandingan_lokasi.csv (tabel ringkasan uji per variabel)
##         boxplot_perbandingan_lokasi.png

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

daftar_lokasi <- unique(df_gabung$kode_lokasi)
if (length(daftar_lokasi) != 2) {
  message("Catatan: uji Wilcoxon di sini didesain untuk 2 lokasi -- ditemukan ", length(daftar_lokasi), " lokasi.")
}

variabel_uji <- c("ACI", "ADI", "AEI", "NDSI", "BI", "H", "kekayaan_spesies_file")

hasil_uji <- do.call(rbind, lapply(variabel_uji, function(var) {
  nilai_a <- df_gabung[df_gabung$kode_lokasi == daftar_lokasi[1], var]
  nilai_b <- df_gabung[df_gabung$kode_lokasi == daftar_lokasi[2], var]
  uji <- wilcox.test(nilai_a, nilai_b)
  data.frame(
    variabel = var,
    lokasi_1 = daftar_lokasi[1], median_lokasi_1 = median(nilai_a, na.rm = TRUE),
    lokasi_2 = daftar_lokasi[2], median_lokasi_2 = median(nilai_b, na.rm = TRUE),
    statistik_W = unname(uji$statistic), p_value = uji$p.value,
    signifikan_0.05 = uji$p.value < 0.05
  )
}))

write.csv(hasil_uji, file.path(dir_hasil, "hasil_uji_perbandingan_lokasi.csv"), row.names = FALSE)

df_panjang <- reshape(
  df_gabung[, c("kode_lokasi", variabel_uji)],
  varying = variabel_uji, v.names = "nilai", timevar = "variabel",
  times = variabel_uji, direction = "long"
)

p <- ggplot(df_panjang, aes(x = kode_lokasi, y = nilai, fill = kode_lokasi)) +
  geom_boxplot(alpha = 0.7, outlier.size = 0.8) +
  facet_wrap(~variabel, scales = "free_y") +
  labs(title = "Perbandingan Indeks Akustik & Kekayaan Spesies Antar Lokasi",
       x = NULL, y = NULL) +
  theme_minimal() +
  theme(legend.position = "none")

ggsave(file.path(dir_hasil, "boxplot_perbandingan_lokasi.png"), p, width = 11, height = 7, dpi = 150)

cat("=== SELESAI ===\n")
print(hasil_uji)
cat("\nFile tersimpan di:", dir_hasil, "\n")
