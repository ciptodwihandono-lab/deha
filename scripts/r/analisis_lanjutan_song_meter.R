## Analisis Lanjutan: Kurva Akumulasi Spesies, Sensitivitas Ambang
## Confidence, dan Pola NDSI (Biofoni-Antropofoni) -- Song Meter Micro 2
##
## Gabungan 3 analisis metodologis untuk laporan ilmiah:
##   BAGIAN 1 -- Kurva akumulasi spesies per lokasi (apakah durasi
##               survei sudah cukup menangkap kekayaan spesies?).
##   BAGIAN 2 -- Sensitivitas kekayaan spesies terhadap ambang confidence
##               BirdNET.
##   BAGIAN 3 -- Pola NDSI (proxy biofoni vs antropofoni) per jam.
##
## KETERBATASAN PENTING (baca dulu sebelum pakai hasil BAGIAN 2):
## Data di rekap_identifikasi_spesies_semua_lokasi.csv dihasilkan dari
## proses BirdNET dengan min_confidence = 0.5 (lihat
## analisis_lengkap_audio_UT2026.R) -- deteksi dengan confidence di
## BAWAH 0.5 TIDAK PERNAH tersimpan sama sekali, bukan cuma difilter
## belakangan. Jadi uji sensitivitas di sini HANYA valid untuk ambang
## >= 0.5. Kalau mau uji ambang lebih rendah (mis. 0.1-0.4), proses
## BirdNET awal perlu diulang dengan min_confidence lebih rendah dulu.
##
## KETERBATASAN BAGIAN 3: NDSI yang dipakai di sini adalah nilai
## gabungan (sudah dihitung package soundecology), BUKAN komponen
## biofoni/antropofoni yang dipisah -- skrip indeks akustik awal tidak
## menyimpan komponen itu secara terpisah. NDSI tinggi = dominan suara
## alami, NDSI rendah/negatif = dominan suara antropogenik, tapi
## proporsi pastinya tidak bisa dihitung dari data yang tersimpan saat
## ini.
##
## Input : hasil_analisis_audio_UT2026/rekap_identifikasi_spesies_semua_lokasi.csv
##         hasil_analisis_audio_UT2026/rekap_indeks_akustik_semua_lokasi.csv
## Output: kurva_akumulasi_spesies.png + .csv
##         sensitivitas_ambang_confidence.png + .csv
##         pola_ndsi_per_jam.png + .csv

library(ggplot2)

dir_hasil <- "F:/Audiomoth/hasil_analisis_audio_UT2026"   # sesuaikan kalau dir_output beda

# ==================== BACA & BERSIHKAN DATA SPESIES =========================

df_spesies_mentah <- read.csv(file.path(dir_hasil, "rekap_identifikasi_spesies_semua_lokasi.csv"), stringsAsFactors = FALSE)
df_spesies_mentah <- df_spesies_mentah[!is.na(df_spesies_mentah$nama_ilmiah), ]
df_spesies_mentah$timestamp <- as.POSIXct(df_spesies_mentah$timestamp, tz = "UTC")
df_spesies_mentah$tanggal <- as.Date(df_spesies_mentah$timestamp)

# Versi bersih (1 deteksi per jendela, confidence tertinggi) -- dipakai Bagian 1
df_spesies_mentah$kunci_jendela <- paste(df_spesies_mentah$kode_lokasi, df_spesies_mentah$nama_file,
                                          df_spesies_mentah$waktu_mulai_detik, sep = "||")
df_urut <- df_spesies_mentah[order(df_spesies_mentah$kunci_jendela, -df_spesies_mentah$confidence), ]
df_bersih <- df_urut[!duplicated(df_urut$kunci_jendela), ]

daftar_lokasi <- unique(df_bersih$kode_lokasi)

# ==================== BAGIAN 1: KURVA AKUMULASI SPESIES =====================

akumulasi_semua <- do.call(rbind, lapply(daftar_lokasi, function(lokasi) {
  d <- df_bersih[df_bersih$kode_lokasi == lokasi, ]
  tanggal_urut <- sort(unique(d$tanggal))

  spesies_terlihat <- character(0)
  baris <- lapply(seq_along(tanggal_urut), function(i) {
    spesies_hari_ini <- unique(d$nama_ilmiah[d$tanggal == tanggal_urut[i]])
    spesies_terlihat <<- union(spesies_terlihat, spesies_hari_ini)
    data.frame(kode_lokasi = lokasi, hari_ke = i, tanggal = tanggal_urut[i],
               kekayaan_kumulatif = length(spesies_terlihat))
  })
  do.call(rbind, baris)
}))

write.csv(akumulasi_semua, file.path(dir_hasil, "kurva_akumulasi_spesies.csv"), row.names = FALSE)

p1 <- ggplot(akumulasi_semua, aes(x = hari_ke, y = kekayaan_kumulatif, color = kode_lokasi)) +
  geom_line(linewidth = 0.9) + geom_point(size = 1.5) +
  labs(title = "Kurva Akumulasi Spesies per Lokasi",
       subtitle = "Kekayaan spesies kumulatif seiring bertambahnya hari survei",
       x = "Hari survei ke-", y = "Jumlah spesies kumulatif", color = "Lokasi") +
  theme_minimal()
ggsave(file.path(dir_hasil, "kurva_akumulasi_spesies.png"), p1, width = 9, height = 6, dpi = 150)

# ==================== BAGIAN 2: SENSITIVITAS AMBANG CONFIDENCE ==============
# PENTING: hanya valid untuk ambang >= 0.5 (lihat catatan keterbatasan di atas).

ambang_uji <- c(0.5, 0.6, 0.7, 0.8, 0.9)

sensitivitas <- do.call(rbind, lapply(daftar_lokasi, function(lokasi) {
  d <- df_spesies_mentah[df_spesies_mentah$kode_lokasi == lokasi, ]
  do.call(rbind, lapply(ambang_uji, function(ambang) {
    d_ambang <- d[d$confidence >= ambang, ]
    data.frame(
      kode_lokasi = lokasi, ambang_confidence = ambang,
      kekayaan_spesies = length(unique(d_ambang$nama_ilmiah)),
      jumlah_deteksi = nrow(d_ambang)
    )
  }))
}))

write.csv(sensitivitas, file.path(dir_hasil, "sensitivitas_ambang_confidence.csv"), row.names = FALSE)

p2 <- ggplot(sensitivitas, aes(x = ambang_confidence, y = kekayaan_spesies, color = kode_lokasi)) +
  geom_line(linewidth = 0.9) + geom_point(size = 2) +
  scale_x_continuous(breaks = ambang_uji) +
  labs(title = "Sensitivitas Kekayaan Spesies terhadap Ambang Confidence BirdNET",
       subtitle = "Hanya diuji untuk ambang >= 0.5 (lihat catatan keterbatasan di skrip)",
       x = "Ambang confidence", y = "Kekayaan spesies", color = "Lokasi") +
  theme_minimal()
ggsave(file.path(dir_hasil, "sensitivitas_ambang_confidence.png"), p2, width = 9, height = 6, dpi = 150)

# ==================== BAGIAN 3: POLA NDSI PER JAM ============================

df_indeks <- read.csv(file.path(dir_hasil, "rekap_indeks_akustik_semua_lokasi.csv"), stringsAsFactors = FALSE)

ndsi_per_jam <- aggregate(NDSI ~ kode_lokasi + jam, data = df_indeks, FUN = mean)
write.csv(ndsi_per_jam, file.path(dir_hasil, "pola_ndsi_per_jam.csv"), row.names = FALSE)

p3 <- ggplot(ndsi_per_jam, aes(x = jam, y = NDSI, color = kode_lokasi)) +
  geom_line(linewidth = 0.9) + geom_point(size = 1.5) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "grey50") +
  scale_x_continuous(breaks = seq(0, 23, 3)) +
  labs(title = "Pola NDSI per Jam (Proxy Biofoni vs Antropofoni)",
       subtitle = "NDSI tinggi = dominan suara alami, NDSI rendah/negatif = dominan suara antropogenik",
       x = "Jam (0-23)", y = "Rata-rata NDSI", color = "Lokasi") +
  theme_minimal()
ggsave(file.path(dir_hasil, "pola_ndsi_per_jam.png"), p3, width = 9, height = 6, dpi = 150)

cat("=== SELESAI ===\n")
cat("File tersimpan di:", dir_hasil, "\n")
cat("\nCatatan: sensitivitas ambang confidence hanya valid >= 0.5 (data di bawah itu tidak pernah tersimpan).\n")
cat("Catatan: NDSI di Bagian 3 adalah nilai gabungan, bukan komponen biofoni/antropofoni terpisah.\n")
