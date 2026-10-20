## Validasi Sebaran Geografis Spesies Terdeteksi -- Song Meter Micro 2
##
## Memakai model lokasi BirdNET sendiri (birdnet_model_meta +
## predict_species_at_location_and_time) untuk menyaring deteksi yang
## tidak masuk akal secara geografis -- mis. kasus Takur Warna-warni
## (Psilopogon mystacophanos) yang sebarannya ke arah Sumatra/Kalimantan,
## bukan Jawa, tapi sempat terdeteksi BirdNET di lokasi Jawa Timur
## (dikonfirmasi: spesies itu TIDAK ada di 369 spesies plausible BirdNET
## untuk koordinat Gunung Anyar Tambak).
##
## CARA KERJA: untuk tiap lokasi, BirdNET menghitung daftar spesies yang
## "plausible" muncul di koordinat itu (model dilatih dari data sebaran
## global, mis. eBird). Spesies yang terdeteksi tapi TIDAK masuk daftar
## plausible itu ditandai MENCURIGAKAN -- kemungkinan salah identifikasi
## (confusable call dengan spesies sejenis), BUKAN otomatis dianggap
## pasti salah. Tetap perlu verifikasi manual (dengar ulang klipnya,
## bandingkan ke referensi xeno-canto) sebelum disimpulkan.
##
## Dipanggil TANPA parameter `week` (musim) secara sengaja -- supaya
## tidak terlalu ketat menyaring spesies migran yang mungkin memang
## sedang lewat saat perekaman, daftar plausible di sini mencakup
## kemungkinan sepanjang tahun, bukan musim tertentu saja.
##
## PENTING: isi LOKASI_KOORDINAT di bawah dengan kode_lokasi PERSIS
## seperti yang muncul di nama file rekap_spesies_<kode_lokasi>.csv
## (cek nama file hasil kalau tidak sama persis dengan nama lokasi di
## bawah -- sesuaikan dengan nama subfolder asli di F:/Audiomoth/UT 2026).
##
## Input : hasil_analisis_audio_UT2026/rekap_spesies_<lokasi>.csv
##         (dari rekap_spesies_song_meter.R -- jalankan itu dulu kalau
##         belum ada)
## Output: validasi_sebaran_geografis_<lokasi>.csv (per lokasi)
##         validasi_sebaran_geografis_semua_lokasi.csv (gabungan)
##         ringkasan_spesies_mencurigakan.csv (cuma yang perlu dicek manual)

library(birdnetR)

dir_hasil <- "F:/Audiomoth/hasil_analisis_audio_UT2026"   # sesuaikan kalau dir_output beda

# -- PENTING: kode_lokasi di sini harus PERSIS sama dengan nama di file
#    rekap_spesies_<kode_lokasi>.csv
LOKASI_KOORDINAT <- list(
  "Gunung Anyar Tambak" = c(lat = -7.32956474, lon = 112.82117646),
  "Sumbergondo" = c(lat = -7.80261544, lon = 112.55330048)
)

model_meta <- birdnet_model_meta()

parse_label <- function(df_label) {
  bagian <- strsplit(df_label$label, "_", fixed = TRUE)
  data.frame(
    nama_ilmiah = sapply(bagian, `[`, 1),
    nama_inggris_geo = sapply(bagian, function(x) paste(x[-1], collapse = "_")),
    confidence_geo = df_label$confidence,
    stringsAsFactors = FALSE
  )
}

hasil_semua <- list()
mencurigakan_semua <- list()

for (kode_lokasi in names(LOKASI_KOORDINAT)) {
  path_rekap <- file.path(dir_hasil, paste0("rekap_spesies_", kode_lokasi, ".csv"))
  if (!file.exists(path_rekap)) {
    message("Lewati '", kode_lokasi, "': file ", path_rekap, " tidak ditemukan -- cek ejaan kode_lokasi.")
    next
  }

  koord <- LOKASI_KOORDINAT[[kode_lokasi]]
  message("Mengambil daftar spesies plausible untuk: ", kode_lokasi,
          " (", unname(koord["lat"]), ", ", unname(koord["lon"]), ")")
  plausible_mentah <- predict_species_at_location_and_time(
    model_meta, latitude = unname(koord["lat"]), longitude = unname(koord["lon"])
  )
  plausible <- parse_label(plausible_mentah)

  terdeteksi <- read.csv(path_rekap, stringsAsFactors = FALSE)
  gabung <- merge(terdeteksi, plausible[, c("nama_ilmiah", "confidence_geo")], by = "nama_ilmiah", all.x = TRUE)
  gabung$status_sebaran <- ifelse(is.na(gabung$confidence_geo),
                                   "MENCURIGAKAN - tidak masuk daftar plausible BirdNET di lokasi ini",
                                   "Sesuai")
  gabung$kode_lokasi <- kode_lokasi
  gabung <- gabung[order(gabung$status_sebaran, -gabung$jumlah_deteksi), ]

  write.csv(gabung, file.path(dir_hasil, paste0("validasi_sebaran_geografis_", kode_lokasi, ".csv")), row.names = FALSE)
  hasil_semua[[kode_lokasi]] <- gabung

  mencurigakan <- gabung[grepl("^MENCURIGAKAN", gabung$status_sebaran), ]
  if (nrow(mencurigakan) > 0) mencurigakan_semua[[kode_lokasi]] <- mencurigakan
}

df_semua <- do.call(rbind, hasil_semua)
write.csv(df_semua, file.path(dir_hasil, "validasi_sebaran_geografis_semua_lokasi.csv"), row.names = FALSE)

df_mencurigakan <- NULL
if (length(mencurigakan_semua) > 0) {
  df_mencurigakan <- do.call(rbind, mencurigakan_semua)
  write.csv(df_mencurigakan, file.path(dir_hasil, "ringkasan_spesies_mencurigakan.csv"), row.names = FALSE)
}

cat("\n=== SELESAI ===\n")
cat("Total baris dicek:", nrow(df_semua), "\n")
if (!is.null(df_mencurigakan)) {
  cat(nrow(df_mencurigakan), "spesies MENCURIGAKAN (sebaran tidak sesuai menurut BirdNET) -- perlu verifikasi manual:\n")
  print(df_mencurigakan[, c("kode_lokasi", "nama_ilmiah", "nama_umum", "jumlah_deteksi")])
} else {
  cat("Tidak ada spesies yang ditandai mencurigakan.\n")
}
cat("\nFile tersimpan di:", dir_hasil, "\n")
cat("Catatan: status MENCURIGAKAN bukan berarti pasti salah -- tetap perlu verifikasi manual")
cat(" (dengar ulang klip asli, bandingkan ke xeno-canto) sebelum dianggap salah identifikasi.\n")
