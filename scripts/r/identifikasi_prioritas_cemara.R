## Identifikasi Spesies Prioritas -- Song Meter/Audiomoth CEMARA (PCMARA)
##
## Beda dari skrip UT2026 (analisis_lengkap_audio_UT2026.R): skrip ini
## dibuat khusus untuk 14 spesies burung air/pantai PRIORITAS (daftar
## di bawah, format "Nama ilmiah_Nama Inggris" -- cocok persis format
## label BirdNET) di lokasi CEMARA/PCMARA.
##
## SEGMENTASI CONFIDENCE DUA PITA (gantinya ambang tunggal):
##   Semua pemindaian (umum maupun prioritas) dijalankan dari ambang
##   bawah AMBANG_BAWAH = 0,10 (nilai default BirdNET terendah yang
##   wajar, supaya tidak ada yang lolos tak tercatat), lalu tiap
##   deteksi diberi label kategori_confidence:
##     - "Tinggi (0,9-1,0)"          -- confidence >= AMBANG_TINGGI
##     - "Perlu verifikasi (0,1-0,9)" -- AMBANG_BAWAH <= confidence < AMBANG_TINGGI
##   Trade-off yang disengaja (sama seperti sebelumnya, cuma sekarang
##   dipakai konsisten di SEMUA spesies, bukan cuma yang prioritas):
##   lebih banyak kandidat di pita "perlu verifikasi", tapi risiko
##   deteksi asli terlewat begitu saja jauh berkurang -- untuk
##   pemantauan burung target/dilindungi, false negative (lolos tak
##   tercatat) lebih mahal daripada false positive (kandidat salah
##   yang gampang dicoret manual).
##
## Bagian A -- identifikasi UMUM semua spesies (bukan cuma prioritas),
##   untuk gambaran komunitas burung keseluruhan, dipecah per pita.
## Bagian B -- pindaian KHUSUS 14 spesies prioritas, dipecah per pita.
## Bagian C -- spektrogram + oscillogram: untuk tiap spesies yang
##   terdeteksi, dibuat SATU contoh per pita yang tersedia (jadi kalau
##   satu spesies punya deteksi di kedua pita, ada 2 gambar -- supaya
##   bisa dibandingkan visual contoh "yakin" vs "perlu verifikasi").
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

AMBANG_BAWAH  <- 0.1   # ambang minimum pemindaian -- di bawah ini diabaikan sepenuhnya
AMBANG_TINGGI <- 0.9   # batas pemisah dua pita confidence (lihat catatan "SEGMENTASI" di atas)

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

# Label pita confidence -- dipakai konsisten di semua tabel/plot/spektrogram.
fmt_id <- function(x) gsub("\\.", ",", format(x, nsmall = 1))   # 0.9 -> "0,9" (desimal gaya Indonesia)
LABEL_TINGGI <- paste0("Tinggi (", fmt_id(AMBANG_TINGGI), "-1,0)")
LABEL_VERIFIKASI <- paste0("Perlu verifikasi (", fmt_id(AMBANG_BAWAH), "-", fmt_id(AMBANG_TINGGI), ")")
kategori_confidence <- function(x) ifelse(x >= AMBANG_TINGGI, LABEL_TINGGI, LABEL_VERIFIKASI)
tag_kategori <- function(x) ifelse(x >= AMBANG_TINGGI, "tinggi", "verifikasi")

message("Mencari file .wav di: ", base_path)
file_wav <- cari_file_wav(base_path)
if (length(file_wav) == 0) stop("Tidak ada file .wav ditemukan di: ", base_path)
message("Ditemukan ", length(file_wav), " file .wav.")

message("Memuat model BirdNET -- percobaan pertama bisa lama (unduh model)...")
model <- birdnet_model_protobuf()
message("Model siap.")

# ======================= BAGIAN A: IDENTIFIKASI UMUM ==========================
# Semua spesies (bukan cuma prioritas), dipindai dari AMBANG_BAWAH,
# lalu dipecah ke 2 pita confidence -- lihat catatan "SEGMENTASI" di atas.

message("\n########## BAGIAN A: IDENTIFIKASI UMUM (confidence >= ", AMBANG_BAWAH, ", 2 pita) ##########")

hasil_umum <- list()
gagal_umum <- list()

for (i in seq_along(file_wav)) {
  path_file <- file_wav[i]
  nama_file <- basename(path_file)
  if (i %% 10 == 0 || i == length(file_wav)) message("  file ", i, "/", length(file_wav))

  waktu_file <- parse_timestamp_dari_nama(nama_file)

  hasil_file <- tryCatch({
    deteksi <- predict_species_from_audio_file(model, path_file, min_confidence = AMBANG_BAWAH)
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
df_u_bersih <- NULL
rekap_umum <- NULL

if (!is.null(df_umum)) {
  df_umum$kategori_confidence <- kategori_confidence(df_umum$confidence)
  write.csv(df_umum, file.path(dir_output, paste0("hasil_identifikasi_umum_", kode_lokasi, ".csv")), row.names = FALSE)
  message("-> ", nrow(df_umum), " deteksi umum (confidence >= ", AMBANG_BAWAH, ") disimpan (",
          sum(df_umum$confidence >= AMBANG_TINGGI), " di pita tinggi, ",
          sum(df_umum$confidence < AMBANG_TINGGI), " di pita perlu-verifikasi).")

  # Rekap ringkas semua spesies (1 label tertinggi per jendela, sama
  # seperti rekap_spesies_song_meter.R -- lihat catatan metodologis itu
  # kalau mau tahu alasannya)
  df_u <- df_umum
  df_u$kunci_jendela <- paste(df_u$nama_file, df_u$waktu_mulai_detik, sep = "||")
  df_u <- df_u[order(df_u$kunci_jendela, -df_u$confidence), ]
  df_u_bersih <- df_u[!duplicated(df_u$kunci_jendela), ]

  rekap_umum <- aggregate(confidence ~ nama_ilmiah + nama_umum, data = df_u_bersih, FUN = length)
  names(rekap_umum)[3] <- "jumlah_deteksi"
  rekap_umum$jumlah_tinggi <- sapply(rekap_umum$nama_ilmiah, function(sp)
    sum(df_u_bersih$nama_ilmiah == sp & df_u_bersih$confidence >= AMBANG_TINGGI))
  rekap_umum$jumlah_perlu_verifikasi <- rekap_umum$jumlah_deteksi - rekap_umum$jumlah_tinggi
  rekap_umum <- rekap_umum[order(-rekap_umum$jumlah_deteksi), ]
  write.csv(rekap_umum, file.path(dir_output, paste0("rekap_spesies_umum_", kode_lokasi, ".csv")), row.names = FALSE)

  top20 <- head(rekap_umum, 20)
  df_plot_panjang <- reshape(
    top20[, c("nama_umum", "jumlah_tinggi", "jumlah_perlu_verifikasi")],
    varying = c("jumlah_tinggi", "jumlah_perlu_verifikasi"), v.names = "jumlah",
    timevar = "kategori_confidence", times = c(LABEL_TINGGI, LABEL_VERIFIKASI),
    direction = "long"
  )
  p <- ggplot(df_plot_panjang, aes(x = reorder(nama_umum, jumlah, sum), y = jumlah, fill = kategori_confidence)) +
    geom_col() + coord_flip() +
    scale_fill_manual(values = setNames(c("#1565c0", "#90caf9"), c(LABEL_TINGGI, LABEL_VERIFIKASI))) +
    labs(title = paste("Top 20 Spesies Terdeteksi (Umum) --", kode_lokasi),
         subtitle = paste0("confidence >= ", AMBANG_BAWAH, "; 1 label tertinggi per jendela; dipecah per pita"),
         x = NULL, y = "Jumlah deteksi", fill = "Pita confidence") +
    theme_minimal()
  ggsave(file.path(dir_output, paste0("plot_top_spesies_umum_", kode_lokasi, ".png")), p, width = 10, height = 7, dpi = 150)
} else {
  message("-> Tidak ada deteksi umum di atas ambang ", AMBANG_BAWAH, ".")
}

if (length(gagal_umum) > 0) {
  write.csv(do.call(rbind, gagal_umum), file.path(dir_output, paste0("file_gagal_", kode_lokasi, ".csv")), row.names = FALSE)
}

# ======================= BAGIAN B: PINDAIAN SPESIES PRIORITAS ==================
# Filter cuma 14 spesies target, dari AMBANG_BAWAH, dipecah ke 2 pita
# confidence -- lihat catatan "SEGMENTASI" di atas.

message("\n########## BAGIAN B: PINDAIAN PRIORITAS (confidence >= ", AMBANG_BAWAH,
        ", ", length(DAFTAR_PRIORITAS), " spesies target, 2 pita) ##########")

hasil_prioritas <- list()

for (i in seq_along(file_wav)) {
  path_file <- file_wav[i]
  nama_file <- basename(path_file)
  if (i %% 10 == 0 || i == length(file_wav)) message("  file ", i, "/", length(file_wav))

  waktu_file <- parse_timestamp_dari_nama(nama_file)

  hasil_file <- tryCatch({
    deteksi <- predict_species_from_audio_file(model, path_file, min_confidence = AMBANG_BAWAH)
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
  df_prioritas$kategori_confidence <- kategori_confidence(df_prioritas$confidence)
  df_prioritas <- df_prioritas[order(df_prioritas$nama_ilmiah, -df_prioritas$confidence), ]
  write.csv(df_prioritas, file.path(dir_output, paste0("deteksi_spesies_prioritas_", kode_lokasi, ".csv")), row.names = FALSE)
  message("-> ", nrow(df_prioritas), " kandidat deteksi spesies prioritas (confidence >= ", AMBANG_BAWAH, ") -- ",
          sum(df_prioritas$confidence >= AMBANG_TINGGI), " di pita TINGGI, ",
          sum(df_prioritas$confidence < AMBANG_TINGGI), " di pita PERLU VERIFIKASI.")
} else {
  message("-> TIDAK ADA kandidat deteksi untuk ke-14 spesies prioritas, bahkan di ambang serendah ", AMBANG_BAWAH, ".")
}

# Tabel ringkas status tiap spesies prioritas (ada/tidak, jumlah per
# pita, confidence tertinggi) -- langsung siap tempel ke laporan.
ringkasan_prioritas <- do.call(rbind, lapply(DAFTAR_PRIORITAS, function(label) {
  ilmiah <- sub("_.*$", "", label)
  umum <- sub("^[^_]*_", "", label)
  if (is.null(df_prioritas)) {
    n <- 0L; n_tinggi <- 0L; n_verif <- 0L; conf_max <- NA_real_
  } else {
    sub_df <- df_prioritas[df_prioritas$nama_ilmiah == ilmiah, ]
    n <- nrow(sub_df)
    n_tinggi <- sum(sub_df$confidence >= AMBANG_TINGGI)
    n_verif <- n - n_tinggi
    conf_max <- if (n > 0) max(sub_df$confidence) else NA_real_
  }
  data.frame(
    nama_ilmiah = ilmiah, nama_inggris = umum,
    terdeteksi = n > 0,
    jumlah_tinggi = n_tinggi,
    jumlah_perlu_verifikasi = n_verif,
    jumlah_deteksi = n,
    confidence_tertinggi = conf_max,
    stringsAsFactors = FALSE
  )
}))
ringkasan_prioritas <- ringkasan_prioritas[order(-ringkasan_prioritas$jumlah_tinggi, -ringkasan_prioritas$jumlah_deteksi), ]
write.csv(ringkasan_prioritas, file.path(dir_output, paste0("ringkasan_status_spesies_prioritas_", kode_lokasi, ".csv")), row.names = FALSE)

cat("\n=== RINGKASAN SPESIES PRIORITAS (per pita confidence) ===\n")
print(ringkasan_prioritas)

# ======================= BAGIAN C: SPEKTROGRAM ===============
# Untuk tiap spesies yang terdeteksi, SATU contoh (confidence
# tertinggi) per pita yang tersedia -- jadi spesies dengan deteksi di
# kedua pita dapat 2 gambar (perbandingan visual "yakin" vs "perlu
# verifikasi"); spesies dengan deteksi di 1 pita saja dapat 1 gambar.

message("\n########## BAGIAN C: SPEKTROGRAM ##########")

n_spektrogram_fallback <- 10  # kalau tidak ada deteksi prioritas, buat spektrogram top-N spesies umum sbg sanity check

bersihkan_nama_file <- function(x) gsub("[^A-Za-z0-9_.-]", "_", x)

# df_sumber: harus sudah punya kolom nama_ilmiah, nama_umum, nama_file,
# waktu_mulai_detik, confidence, kategori_confidence.
buat_spektrogram_dari_contoh <- function(df_sumber, subfolder = NULL) {
  dir_out <- if (is.null(subfolder)) dir_spektrogram else file.path(dir_spektrogram, subfolder)
  dir.create(dir_out, showWarnings = FALSE, recursive = TRUE)
  durasi_klip <- 3  # detik, sesuai lebar jendela analisis BirdNET
  gagal_spektro <- list()

  # 1 contoh terbaik per (spesies, pita)
  contoh <- df_sumber[order(-df_sumber$confidence), ]
  contoh <- contoh[!duplicated(paste(contoh$nama_ilmiah, contoh$kategori_confidence)), ]

  for (i in seq_len(nrow(contoh))) {
    baris <- contoh[i, ]
    message("  [", i, "/", nrow(contoh), "] ", baris$nama_ilmiah, " -- ", baris$kategori_confidence,
            " (confidence ", round(baris$confidence, 3), ")")

    tryCatch({
      path_file <- file_wav[basename(file_wav) == baris$nama_file][1]
      if (is.na(path_file)) stop("File audio tidak ditemukan: ", baris$nama_file)

      from <- baris$waktu_mulai_detik
      to <- from + durasi_klip
      wave <- readWave(path_file, from = from, to = to, units = "seconds")

      nama_png <- paste0(bersihkan_nama_file(baris$nama_ilmiah), "_", tag_kategori(baris$confidence), ".png")
      path_png <- file.path(dir_out, nama_png)
      judul <- paste0(baris$nama_ilmiah, " (", baris$nama_umum, ") -- ", baris$kategori_confidence, "\n",
                       kode_lokasi, " -- ", baris$nama_file, " @ ", from, "-", to, "s",
                       " -- confidence ", round(baris$confidence, 3))

      png(path_png, width = 1000, height = 600, res = 120)
      spectro(wave, flim = flim_khz, main = judul, scale = FALSE, osc = TRUE)
      dev.off()
    }, error = function(e) {
      message("    GAGAL: ", conditionMessage(e))
      gagal_spektro[[length(gagal_spektro) + 1]] <<- data.frame(
        nama_ilmiah = baris$nama_ilmiah, kategori_confidence = baris$kategori_confidence,
        nama_file = baris$nama_file, pesan_error = conditionMessage(e)
      )
    })
  }

  if (length(gagal_spektro) > 0) {
    write.csv(do.call(rbind, gagal_spektro), file.path(dir_output, "spektrogram_gagal.csv"), row.names = FALSE)
  }
  message("Spektrogram tersimpan di: ", dir_out)
}

if (!is.null(df_prioritas) && nrow(df_prioritas) > 0) {
  message("Membuat spektrogram untuk ", length(unique(df_prioritas$nama_ilmiah)),
          " spesies prioritas yang terdeteksi (1 gambar per pita confidence per spesies)...")
  buat_spektrogram_dari_contoh(df_prioritas)
} else {
  message("Tidak ada deteksi prioritas -- sebagai gantinya, buat spektrogram top-",
          n_spektrogram_fallback, " spesies UMUM (dari Bagian A) sebagai sanity check visual.")
  if (is.null(df_u_bersih) || nrow(df_u_bersih) == 0) {
    message("  Bagian A juga tidak punya deteksi apa pun -- tidak ada bahan spektrogram sama sekali.",
            " Ini pertanda kuat ada masalah di luar daftar spesies prioritas (lihat file_gagal_",
            kode_lokasi, ".csv, atau cek manual apakah file .wav bisa dibuka/berisi suara).")
  } else {
    top_spesies <- head(rekap_umum$nama_ilmiah, n_spektrogram_fallback)
    contoh_fallback <- df_u_bersih[df_u_bersih$nama_ilmiah %in% top_spesies, ]
    buat_spektrogram_dari_contoh(contoh_fallback, subfolder = "umum_fallback")
  }
}

cat("\n=== SELESAI ===\n")
cat("Semua hasil tersimpan di:", dir_output, "\n")
cat("File penting untuk laporan:\n")
cat("  - ringkasan_status_spesies_prioritas_", kode_lokasi, ".csv -- status tiap spesies target, per pita confidence\n", sep = "")
cat("  - deteksi_spesies_prioritas_", kode_lokasi, ".csv -- semua kandidat + kolom kategori_confidence (VERIFIKASI MANUAL dulu sebelum dipakai jadi klaim final, terutama pita 'perlu verifikasi')\n", sep = "")
cat("  - rekap_spesies_umum_", kode_lokasi, ".csv -- gambaran komunitas burung keseluruhan, per pita\n", sep = "")
cat("  - spektrogram/*_tinggi.png dan *_verifikasi.png -- verifikasi visual tiap spesies & pita yang terdeteksi\n")
cat("    (kalau tidak ada deteksi prioritas: spektrogram/umum_fallback/*.png -- top spesies umum sbg sanity check)\n")
cat("\nIngat: pita '", LABEL_VERIFIKASI, "' WAJIB didengar ulang/dicek spektrogramnya dulu sebelum",
    " dianggap deteksi pasti -- pita ini sengaja dibuat lebar supaya tidak ada deteksi yang lolos",
    " tak tercatat, bukan berarti semuanya pasti benar.\n", sep = "")
