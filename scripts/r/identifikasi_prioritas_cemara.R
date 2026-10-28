## Identifikasi Spesies Prioritas -- Song Meter/Audiomoth CEMARA (PCMARA)
##
## Beda dari skrip UT2026 (analisis_lengkap_audio_UT2026.R): skrip ini
## dibuat khusus untuk 14 spesies burung air/pantai PRIORITAS (daftar
## di bawah, format "Nama ilmiah_Nama Inggris" -- cocok persis format
## label BirdNET) di lokasi CEMARA/PCMARA.
##
## PENDEKATAN DUA AMBANG (penting -- beda dari skrip UT2026):
##   Bagian A -- identifikasi UMUM semua spesies, ambang confidence
##     standar 0,5 (sama seperti UT2026), untuk gambaran komunitas
##     burung keseluruhan.
##   Bagian B -- pindaian KHUSUS 14 spesies prioritas dengan ambang
##     JAUH LEBIH RENDAH (0,10, nilai default BirdNET terendah yang
##     wajar), supaya deteksi yang lemah tapi mungkin benar untuk
##     spesies target TIDAK terlewat begitu saja. Trade-off yang
##     disengaja: lebih banyak kandidat perlu diverifikasi manual
##     (dengar ulang klip / lihat spektrogram / bandingkan xeno-canto),
##     tapi risiko "spesies prioritas lewat tanpa tercatat" jauh
##     berkurang -- untuk pemantauan burung target/dilindungi, false
##     negative (lolos tak tercatat) lebih mahal daripada false
##     positive (kandidat salah yang gampang dicoret manual).
##
## Bagian C -- spektrogram + oscillogram untuk SETIAP spesies prioritas
##   yang punya minimal 1 deteksi (contoh confidence tertinggi),
##   supaya bisa langsung diverifikasi visual tanpa buka software lain.
##
## Cara pakai: cek KONFIGURASI di bawah (base_path, kode_lokasi), lalu
## Source seluruh skrip. Edit DAFTAR_PRIORITAS kalau daftar spesies
## berubah di kegiatan lain.

# ============================== KONFIGURASI =================================

base_path      <- "F:/Audiomoth/CEMARA/PCMARA/17-04-2026"   # folder berisi file .wav (cari rekursif)
kode_lokasi    <- "PCMARA"                                   # ganti sesuai kode lokasi yang dipakai tim
id_alat        <- "Audiomoth"                                 # ganti dengan SN alat kalau tahu

dir_output     <- file.path(dirname(base_path), paste0("hasil_identifikasi_", kode_lokasi))
dir_spektrogram <- file.path(dir_output, "spektrogram")

min_confidence_umum      <- 0.5    # Bagian A -- sama seperti analisis UT2026
min_confidence_prioritas <- 0.1    # Bagian B -- sengaja rendah, lihat catatan di atas

flim_khz <- c(0, 10)   # rentang frekuensi spektrogram (kHz) -- naikkan kalau ada spesies bersuara tinggi

# Daftar spesies prioritas: "Nama ilmiah_Nama Inggris" -- format ini
# PERSIS sama dengan kolom label mentah BirdNET (scientific_common),
# supaya pencocokan tidak meleset karena beda ejaan nama umum.
DAFTAR_PRIORITAS <- c(
  "Tringa nebularia_Common Greenshank",
  "Tringa totanus_Common Redshank",
  "Calidris ferruginea_Curlew Sandpiper",
  "Numenius arquata_Eurasian Curlew",
  "Charadrius leschenaultii_Greater Sand-Plover",
  "Charadrius mongolus_Lesser Sand-Plover",
  "Sternula albifrons_Little Tern",
  "Calidris ruficollis_Red-necked Stint",
  "Xenus cinereus_Terek Sandpiper",
  "Numenius phaeopus_Whimbrel",
  "Phylloscopus borealis_Arctic Warbler",
  "Eudynamys scolopaceus_Asian Koel",
  "Motacilla tschutschensis_Eastern Yellow Wagtail",
  "Glareola maldivarum_Oriental Pratincole"
)
nama_ilmiah_prioritas <- sub("_.*$", "", DAFTAR_PRIORITAS)

# ============================== PACKAGE ======================================

paket_dibutuhkan <- c("birdnetR", "tuneR", "seewave", "lubridate", "ggplot2")
paket_belum_ada <- paket_dibutuhkan[!paket_dibutuhkan %in% rownames(installed.packages())]
if (length(paket_belum_ada) > 0) {
  message("Menginstal package yang belum ada: ", paste(paket_belum_ada, collapse = ", "))
  install.packages(paket_belum_ada)
}

library(birdnetR)
library(tuneR)
library(seewave)
library(lubridate)
library(ggplot2)

dir.create(dir_output, showWarnings = FALSE, recursive = TRUE)
dir.create(dir_spektrogram, showWarnings = FALSE, recursive = TRUE)

# ============================== FUNGSI =======================================

cari_file_wav <- function(path) {
  file_wav <- list.files(path, pattern = "\\.wav$", ignore.case = TRUE,
                          recursive = TRUE, full.names = TRUE)
  file_wav
}

# Sama seperti skrip UT2026 -- parse timestamp dari nama file kalau
# formatnya YYYYMMDD_HHMMSS. Kalau nama file Audiomoth kamu beda format
# (mis. cuma HHMMSS atau epoch Unix), fungsi ini akan return NA dan
# kolom timestamp kosong -- tidak menghentikan analisis, cuma hilang
# info jam pastinya.
parse_timestamp_dari_nama <- function(nama_file) {
  m <- regmatches(nama_file, regexpr("\\d{8}_\\d{6}", nama_file))
  if (length(m) == 0) return(as.POSIXct(NA))
  ymd_hms(m, tz = "UTC")
}

message("Mencari file .wav di: ", base_path)
file_wav <- cari_file_wav(base_path)
if (length(file_wav) == 0) stop("Tidak ada file .wav ditemukan di: ", base_path)
message("Ditemukan ", length(file_wav), " file .wav.")

message("Memuat model BirdNET -- percobaan pertama bisa lama (unduh model)...")
model <- birdnet_model_protobuf()
message("Model siap.")

# ======================= BAGIAN A: IDENTIFIKASI UMUM ==========================
# Sama seperti Bagian B di analisis_lengkap_audio_UT2026.R -- ambang
# confidence standar 0,5, semua spesies (bukan cuma prioritas).

message("\n########## BAGIAN A: IDENTIFIKASI UMUM (confidence >= ", min_confidence_umum, ") ##########")

hasil_umum <- list()
gagal_umum <- list()

for (i in seq_along(file_wav)) {
  path_file <- file_wav[i]
  nama_file <- basename(path_file)
  if (i %% 10 == 0 || i == length(file_wav)) message("  file ", i, "/", length(file_wav))

  waktu_file <- parse_timestamp_dari_nama(nama_file)

  hasil_file <- tryCatch({
    deteksi <- predict_species_from_audio_file(model, path_file, min_confidence = min_confidence_umum)
    if (nrow(deteksi) == 0) return(NULL)
    data.frame(
      kode_lokasi = kode_lokasi, id_alat = id_alat, nama_file = nama_file,
      waktu_mulai_detik = deteksi$start, waktu_selesai_detik = deteksi$end,
      timestamp = waktu_file + deteksi$start,
      nama_ilmiah = deteksi$scientific_name, nama_umum = deteksi$common_name,
      confidence = deteksi$confidence,
      stringsAsFactors = FALSE
    )
  }, error = function(e) {
    message("    GAGAL: ", nama_file, " -- ", conditionMessage(e))
    gagal_umum[[length(gagal_umum) + 1]] <<- data.frame(
      nama_file = nama_file, pesan_error = conditionMessage(e)
    )
    NULL
  })

  if (!is.null(hasil_file)) hasil_umum[[length(hasil_umum) + 1]] <- hasil_file
}

df_umum <- do.call(rbind, hasil_umum)
if (!is.null(df_umum)) {
  write.csv(df_umum, file.path(dir_output, paste0("hasil_identifikasi_umum_", kode_lokasi, ".csv")), row.names = FALSE)
  message("-> ", nrow(df_umum), " deteksi umum (confidence >= ", min_confidence_umum, ") disimpan.")

  # Rekap ringkas semua spesies (1 label tertinggi per jendela, sama
  # seperti rekap_spesies_song_meter.R -- lihat catatan metodologis itu
  # kalau mau tahu alasannya)
  df_u <- df_umum
  df_u$kunci_jendela <- paste(df_u$nama_file, df_u$waktu_mulai_detik, sep = "||")
  df_u <- df_u[order(df_u$kunci_jendela, -df_u$confidence), ]
  df_u_bersih <- df_u[!duplicated(df_u$kunci_jendela), ]
  rekap_umum <- aggregate(confidence ~ nama_ilmiah + nama_umum, data = df_u_bersih, FUN = length)
  names(rekap_umum)[3] <- "jumlah_deteksi"
  rekap_umum <- rekap_umum[order(-rekap_umum$jumlah_deteksi), ]
  write.csv(rekap_umum, file.path(dir_output, paste0("rekap_spesies_umum_", kode_lokasi, ".csv")), row.names = FALSE)

  p <- ggplot(head(rekap_umum, 20), aes(x = reorder(nama_umum, jumlah_deteksi), y = jumlah_deteksi)) +
    geom_col(fill = "#1565c0") + coord_flip() +
    labs(title = paste("Top 20 Spesies Terdeteksi (Umum) --", kode_lokasi),
         subtitle = paste0("min_confidence = ", min_confidence_umum, "; 1 label tertinggi per jendela"),
         x = NULL, y = "Jumlah deteksi") +
    theme_minimal()
  ggsave(file.path(dir_output, paste0("plot_top_spesies_umum_", kode_lokasi, ".png")), p, width = 9, height = 7, dpi = 150)
} else {
  message("-> Tidak ada deteksi umum di atas ambang ", min_confidence_umum, ".")
}

if (length(gagal_umum) > 0) {
  write.csv(do.call(rbind, gagal_umum), file.path(dir_output, paste0("file_gagal_", kode_lokasi, ".csv")), row.names = FALSE)
}

# ======================= BAGIAN B: PINDAIAN SPESIES PRIORITAS ==================
# Ambang RENDAH (min_confidence_prioritas), filter cuma 14 spesies
# target -- lihat catatan "PENDEKATAN DUA AMBANG" di atas.

message("\n########## BAGIAN B: PINDAIAN PRIORITAS (confidence >= ", min_confidence_prioritas,
        ", ", length(DAFTAR_PRIORITAS), " spesies target) ##########")

hasil_prioritas <- list()

for (i in seq_along(file_wav)) {
  path_file <- file_wav[i]
  nama_file <- basename(path_file)
  if (i %% 10 == 0 || i == length(file_wav)) message("  file ", i, "/", length(file_wav))

  waktu_file <- parse_timestamp_dari_nama(nama_file)

  hasil_file <- tryCatch({
    deteksi <- predict_species_from_audio_file(model, path_file, min_confidence = min_confidence_prioritas)
    if (nrow(deteksi) == 0) return(NULL)
    deteksi <- deteksi[deteksi$scientific_name %in% nama_ilmiah_prioritas, ]
    if (nrow(deteksi) == 0) return(NULL)
    data.frame(
      kode_lokasi = kode_lokasi, id_alat = id_alat, nama_file = nama_file,
      waktu_mulai_detik = deteksi$start, waktu_selesai_detik = deteksi$end,
      timestamp = waktu_file + deteksi$start,
      nama_ilmiah = deteksi$scientific_name, nama_umum = deteksi$common_name,
      confidence = deteksi$confidence,
      stringsAsFactors = FALSE
    )
  }, error = function(e) {
    NULL  # file gagal sudah tercatat di Bagian A, tidak perlu dobel di sini
  })

  if (!is.null(hasil_file)) hasil_prioritas[[length(hasil_prioritas) + 1]] <- hasil_file
}

df_prioritas <- do.call(rbind, hasil_prioritas)

if (!is.null(df_prioritas)) {
  df_prioritas <- df_prioritas[order(df_prioritas$nama_ilmiah, -df_prioritas$confidence), ]
  write.csv(df_prioritas, file.path(dir_output, paste0("deteksi_spesies_prioritas_", kode_lokasi, ".csv")), row.names = FALSE)
  message("-> ", nrow(df_prioritas), " kandidat deteksi spesies prioritas (confidence >= ",
          min_confidence_prioritas, ") -- PERLU VERIFIKASI MANUAL, terutama yang confidence rendah.")
} else {
  message("-> TIDAK ADA kandidat deteksi untuk ke-14 spesies prioritas, bahkan di ambang serendah ",
          min_confidence_prioritas, ".")
}

# Tabel ringkas status tiap spesies prioritas (ada/tidak ada deteksi,
# jumlah, confidence tertinggi) -- langsung siap tempel ke laporan.
ringkasan_prioritas <- do.call(rbind, lapply(DAFTAR_PRIORITAS, function(label) {
  ilmiah <- sub("_.*$", "", label)
  umum <- sub("^[^_]*_", "", label)
  if (is.null(df_prioritas)) {
    n <- 0L
    conf_max <- NA_real_
  } else {
    sub_df <- df_prioritas[df_prioritas$nama_ilmiah == ilmiah, ]
    n <- nrow(sub_df)
    conf_max <- if (n > 0) max(sub_df$confidence) else NA_real_
  }
  data.frame(
    nama_ilmiah = ilmiah, nama_inggris = umum,
    terdeteksi = n > 0,
    jumlah_deteksi = n,
    confidence_tertinggi = conf_max,
    stringsAsFactors = FALSE
  )
}))
ringkasan_prioritas <- ringkasan_prioritas[order(-ringkasan_prioritas$terdeteksi, -ringkasan_prioritas$jumlah_deteksi), ]
write.csv(ringkasan_prioritas, file.path(dir_output, paste0("ringkasan_status_spesies_prioritas_", kode_lokasi, ".csv")), row.names = FALSE)

cat("\n=== RINGKASAN SPESIES PRIORITAS ===\n")
print(ringkasan_prioritas)

# ======================= BAGIAN C: SPEKTROGRAM SPESIES PRIORITAS ===============
# 1 contoh terbaik (confidence tertinggi) per spesies prioritas yang
# punya minimal 1 deteksi -- sama pola seperti spektrogram_per_spesies_song_meter.R.

message("\n########## BAGIAN C: SPEKTROGRAM SPESIES PRIORITAS ##########")

if (is.null(df_prioritas) || nrow(df_prioritas) == 0) {
  message("Tidak ada deteksi prioritas -- lewati pembuatan spektrogram.")
} else {
  contoh_terbaik <- df_prioritas[order(-df_prioritas$confidence), ]
  contoh_terbaik <- contoh_terbaik[!duplicated(contoh_terbaik$nama_ilmiah), ]

  durasi_klip <- 3  # detik, sesuai lebar jendela analisis BirdNET
  bersihkan_nama_file <- function(x) gsub("[^A-Za-z0-9_.-]", "_", x)
  gagal_spektro <- list()

  for (i in seq_len(nrow(contoh_terbaik))) {
    baris <- contoh_terbaik[i, ]
    message("  [", i, "/", nrow(contoh_terbaik), "] ", baris$nama_ilmiah,
            " (confidence ", round(baris$confidence, 3), ")")

    tryCatch({
      path_file <- file_wav[basename(file_wav) == baris$nama_file][1]
      if (is.na(path_file)) stop("File audio tidak ditemukan: ", baris$nama_file)

      from <- baris$waktu_mulai_detik
      to <- from + durasi_klip
      wave <- readWave(path_file, from = from, to = to, units = "seconds")

      path_png <- file.path(dir_spektrogram, paste0(bersihkan_nama_file(baris$nama_ilmiah), ".png"))
      judul <- paste0(baris$nama_ilmiah, " (", baris$nama_umum, ")\n",
                       kode_lokasi, " -- ", baris$nama_file, " @ ", from, "-", to, "s",
                       " -- confidence ", round(baris$confidence, 3))

      png(path_png, width = 1000, height = 600, res = 120)
      spectro(wave, flim = flim_khz, main = judul, scale = FALSE, osc = TRUE)
      dev.off()
    }, error = function(e) {
      message("    GAGAL: ", conditionMessage(e))
      gagal_spektro[[length(gagal_spektro) + 1]] <<- data.frame(
        nama_ilmiah = baris$nama_ilmiah, nama_file = baris$nama_file,
        pesan_error = conditionMessage(e)
      )
    })
  }

  if (length(gagal_spektro) > 0) {
    write.csv(do.call(rbind, gagal_spektro), file.path(dir_output, "spektrogram_prioritas_gagal.csv"), row.names = FALSE)
  }
  message("Spektrogram tersimpan di: ", dir_spektrogram)
}

cat("\n=== SELESAI ===\n")
cat("Semua hasil tersimpan di:", dir_output, "\n")
cat("File penting untuk laporan:\n")
cat("  - ringkasan_status_spesies_prioritas_", kode_lokasi, ".csv -- status tiap spesies target\n", sep = "")
cat("  - deteksi_spesies_prioritas_", kode_lokasi, ".csv -- semua kandidat (VERIFIKASI MANUAL dulu sebelum dipakai jadi klaim final)\n", sep = "")
cat("  - rekap_spesies_umum_", kode_lokasi, ".csv -- gambaran komunitas burung keseluruhan\n", sep = "")
cat("  - spektrogram/*.png -- verifikasi visual tiap spesies prioritas yang terdeteksi\n")
cat("\nIngat: kandidat di Bagian B pakai ambang confidence rendah (", min_confidence_prioritas,
    ") supaya tidak ada yang lolos tak tercatat -- WAJIB didengar ulang/dicek spektrogramnya dulu",
    " sebelum dianggap deteksi pasti, terutama yang confidence-nya di bawah ~0,3.\n", sep = "")
