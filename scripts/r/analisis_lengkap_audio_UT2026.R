## Analisis Lengkap Audio Song Meter Micro 2 -- Indeks Akustik + Identifikasi Spesies
##
## Skrip gabungan: sekali Source, dua hasil sekaligus.
##   BAGIAN A -- Indeks akustik soundscape (ACI/ADI/AEI/NDSI/BI/H) per segmen rekaman.
##   BAGIAN B -- Identifikasi spesies otomatis (BirdNET) per rekaman.
##
## CATATAN soal xeno-canto.org: situs itu BUKAN alat identifikasi
## otomatis -- cuma database referensi suara untuk dibandingkan dengar
## manual. Model BirdNET di BAGIAN B justru dilatih memakai banyak data
## dari xeno-canto, jadi hasilnya sudah "mewarisi" referensi itu.
##
## Data & alat: rekaman .WAV Wildlife Acoustics Song Meter Micro 2
## (SN 2MM27997), satu subfolder per lokasi di dalam folder utama.
## Setting lapangan: 32000 Hz, gain 18 dB, rekam maks 1 menit/file,
## duty cycle rekam 1 menit / jeda 4 menit, aktif 00:00-23:59.
##
## Tiap lokasi diproses dan disimpan TERPISAH untuk kedua analisis
## (CSV & grafik per lokasi), plus rekap gabungan masing-masing.
##
## Cara pakai: cek bagian KONFIGURASI di bawah, lalu Source seluruh skrip.

# ============================== KONFIGURASI =================================

base_path           <- "F:/Audiomoth/UT 2026"   # folder utama berisi subfolder per lokasi
dir_output           <- file.path(dirname(base_path), "hasil_analisis_audio_UT2026")
id_alat              <- "2MM27997"              # SN Song Meter Micro 2

# -- Bagian A: indeks akustik
durasi_segmen_detik  <- 60   # = panjang rekam maksimal alat (1 menit)
durasi_segmen_min    <- 30   # sisa potongan < 30 detik di akhir file dibuang

# -- Bagian B: identifikasi spesies
min_confidence       <- 0.5  # 0-1, ambang keyakinan BirdNET (default package 0.1 = sangat longgar)

# ============================== PACKAGE ======================================

paket_dibutuhkan <- c("tuneR", "seewave", "soundecology", "lubridate", "ggplot2", "birdnetR")
paket_belum_ada <- paket_dibutuhkan[!paket_dibutuhkan %in% rownames(installed.packages())]
if (length(paket_belum_ada) > 0) {
  message("Menginstal package yang belum ada: ", paste(paket_belum_ada, collapse = ", "))
  install.packages(paket_belum_ada)
}

library(tuneR)
library(seewave)
library(soundecology)
library(lubridate)
library(ggplot2)
library(birdnetR)

dir.create(dir_output, showWarnings = FALSE, recursive = TRUE)

# ============================== FUNGSI BERSAMA ===============================

# Cari semua file .wav, dikelompokkan per subfolder (lokasi) langsung di bawah base_path.
cari_file_wav <- function(base_path) {
  lokasi_dirs <- list.dirs(base_path, full.names = TRUE, recursive = FALSE)
  lokasi_dirs <- lokasi_dirs[normalizePath(lokasi_dirs, mustWork = FALSE) !=
                                normalizePath(base_path, mustWork = FALSE)]

  if (length(lokasi_dirs) == 0) {
    message("Tidak ada subfolder lokasi -- semua file dianggap satu lokasi: ", basename(base_path))
    lokasi_dirs <- base_path
  }

  daftar <- lapply(lokasi_dirs, function(dir_lokasi) {
    file_wav <- list.files(dir_lokasi, pattern = "\\.wav$", ignore.case = TRUE,
                            recursive = TRUE, full.names = TRUE)
    if (length(file_wav) == 0) return(NULL)
    data.frame(kode_lokasi = basename(dir_lokasi), path_file = file_wav, stringsAsFactors = FALSE)
  })

  do.call(rbind, daftar)
}

# Parse timestamp dari nama file (format YYYYMMDD_HHMMSS, di mana pun posisinya).
parse_timestamp_dari_nama <- function(nama_file) {
  m <- regmatches(nama_file, regexpr("\\d{8}_\\d{6}", nama_file))
  if (length(m) == 0) return(as.POSIXct(NA))
  ymd_hms(m, tz = "UTC")
}

# =========================== BAGIAN A: INDEKS AKUSTIK =========================

pecah_segmen <- function(wave, durasi_segmen, durasi_min) {
  durasi_total <- length(wave@left) / wave@samp.rate
  if (durasi_total <= durasi_segmen) {
    return(list(list(wave = wave, offset_detik = 0)))
  }

  n_segmen <- floor(durasi_total / durasi_segmen)
  sisa <- durasi_total - n_segmen * durasi_segmen
  segmen <- lapply(seq_len(n_segmen) - 1, function(i) {
    from <- i * durasi_segmen
    to <- from + durasi_segmen
    list(wave = extractWave(wave, from = from, to = to, xunit = "time", interact = FALSE),
         offset_detik = from)
  })

  if (sisa >= durasi_min) {
    from <- n_segmen * durasi_segmen
    segmen <- c(segmen, list(list(
      wave = extractWave(wave, from = from, to = durasi_total, xunit = "time", interact = FALSE),
      offset_detik = from
    )))
  }

  segmen
}

hitung_indeks_segmen <- function(wave_segmen) {
  aci <- suppressWarnings(acoustic_complexity(wave_segmen))
  adi <- suppressWarnings(acoustic_diversity(wave_segmen))
  aei <- suppressWarnings(acoustic_evenness(wave_segmen))
  ndsi_hasil <- suppressWarnings(ndsi(wave_segmen))
  bio <- suppressWarnings(bioacoustic_index(wave_segmen))
  entropi <- suppressWarnings(H(wave_segmen))

  data.frame(
    ACI = aci$AciTotAll_left, ADI = adi$adi_left, AEI = aei$aei_left,
    NDSI = ndsi_hasil$ndsi_left, BI = bio$left_area, H = entropi
  )
}

proses_indeks_lokasi <- function(kode_lokasi, file_df) {
  message("\n== [Indeks akustik] Lokasi: ", kode_lokasi, " (", nrow(file_df), " file) ==")

  hasil_semua <- list()
  gagal_semua <- list()

  for (i in seq_len(nrow(file_df))) {
    path_file <- file_df$path_file[i]
    nama_file <- basename(path_file)
    if (i %% 10 == 0 || i == nrow(file_df)) message("  [", kode_lokasi, "] file ", i, "/", nrow(file_df))

    waktu_file <- parse_timestamp_dari_nama(nama_file)

    hasil_file <- tryCatch({
      wave <- readWave(path_file)
      segmen_list <- pecah_segmen(wave, durasi_segmen_detik, durasi_segmen_min)

      baris_segmen <- lapply(segmen_list, function(seg) {
        indeks <- hitung_indeks_segmen(seg$wave)
        waktu_segmen <- waktu_file + seg$offset_detik
        cbind(
          data.frame(
            kode_lokasi = kode_lokasi, id_alat = id_alat, nama_file = nama_file,
            offset_detik = seg$offset_detik, timestamp = waktu_segmen,
            tanggal = as.Date(waktu_segmen), jam = hour(waktu_segmen)
          ),
          indeks
        )
      })
      do.call(rbind, baris_segmen)
    }, error = function(e) {
      message("    GAGAL: ", nama_file, " -- ", conditionMessage(e))
      gagal_semua[[length(gagal_semua) + 1]] <<- data.frame(
        kode_lokasi = kode_lokasi, nama_file = nama_file, pesan_error = conditionMessage(e)
      )
      NULL
    })

    if (!is.null(hasil_file)) hasil_semua[[length(hasil_semua) + 1]] <- hasil_file
  }

  df_hasil <- do.call(rbind, hasil_semua)
  df_gagal <- if (length(gagal_semua) > 0) do.call(rbind, gagal_semua) else NULL

  if (!is.null(df_hasil)) {
    write.csv(df_hasil, file.path(dir_output, paste0("hasil_indeks_akustik_", kode_lokasi, ".csv")), row.names = FALSE)
  }
  if (!is.null(df_gagal)) {
    write.csv(df_gagal, file.path(dir_output, paste0("indeks_file_gagal_", kode_lokasi, ".csv")), row.names = FALSE)
  }

  list(hasil = df_hasil, gagal = df_gagal)
}

buat_plot_diel <- function(df, kode_lokasi) {
  df_panjang <- reshape(df, varying = c("ACI", "ADI", "AEI", "NDSI", "BI", "H"), v.names = "nilai",
                         timevar = "indeks", times = c("ACI", "ADI", "AEI", "NDSI", "BI", "H"), direction = "long")
  p <- ggplot(df_panjang, aes(x = jam, y = nilai)) +
    stat_summary(fun = mean, geom = "line", color = "#1565c0") +
    stat_summary(fun = mean, geom = "point", color = "#1565c0") +
    facet_wrap(~indeks, scales = "free_y") +
    labs(title = paste("Pola Diel Indeks Akustik --", kode_lokasi), x = "Jam (0-23)", y = "Rata-rata nilai indeks") +
    theme_minimal()
  ggsave(file.path(dir_output, paste0("plot_diel_", kode_lokasi, ".png")), p, width = 10, height = 6, dpi = 150)
}

buat_plot_tren <- function(df, kode_lokasi) {
  df_panjang <- reshape(df, varying = c("ACI", "ADI", "AEI", "NDSI", "BI", "H"), v.names = "nilai",
                         timevar = "indeks", times = c("ACI", "ADI", "AEI", "NDSI", "BI", "H"), direction = "long")
  p <- ggplot(df_panjang, aes(x = timestamp, y = nilai)) +
    geom_line(color = "#2e7d32", alpha = 0.6) +
    geom_point(color = "#2e7d32", size = 0.8) +
    facet_wrap(~indeks, scales = "free_y") +
    labs(title = paste("Tren Indeks Akustik dari Waktu ke Waktu --", kode_lokasi), x = "Waktu", y = "Nilai indeks") +
    theme_minimal()
  ggsave(file.path(dir_output, paste0("plot_tren_", kode_lokasi, ".png")), p, width = 10, height = 6, dpi = 150)
}

# ======================= BAGIAN B: IDENTIFIKASI SPESIES ========================
# Kolom hasil predict_species_from_audio_file() terkonfirmasi lewat tes
# langsung di data asli: start, end, scientific_name, common_name, confidence
# (satu panggilan = satu file, keep_empty=TRUE menyisakan baris NA untuk
# jendela 3 detik yang tidak ada deteksi di atas ambang min_confidence).

proses_spesies_lokasi <- function(kode_lokasi, file_df, model) {
  message("\n== [Identifikasi spesies] Lokasi: ", kode_lokasi, " (", nrow(file_df), " file) ==")

  hasil_semua <- list()
  gagal_semua <- list()

  for (i in seq_len(nrow(file_df))) {
    path_file <- file_df$path_file[i]
    nama_file <- basename(path_file)
    if (i %% 10 == 0 || i == nrow(file_df)) message("  [", kode_lokasi, "] file ", i, "/", nrow(file_df))

    waktu_file <- parse_timestamp_dari_nama(nama_file)

    hasil_file <- tryCatch({
      deteksi <- predict_species_from_audio_file(model, path_file, min_confidence = min_confidence)
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
      gagal_semua[[length(gagal_semua) + 1]] <<- data.frame(
        kode_lokasi = kode_lokasi, nama_file = nama_file, pesan_error = conditionMessage(e)
      )
      NULL
    })

    if (!is.null(hasil_file)) hasil_semua[[length(hasil_semua) + 1]] <- hasil_file
  }

  df_hasil <- do.call(rbind, hasil_semua)
  df_gagal <- if (length(gagal_semua) > 0) do.call(rbind, gagal_semua) else NULL

  if (!is.null(df_hasil)) {
    write.csv(df_hasil, file.path(dir_output, paste0("hasil_identifikasi_spesies_", kode_lokasi, ".csv")), row.names = FALSE)
    message("  -> ", sum(!is.na(df_hasil$nama_ilmiah)), " deteksi spesies (dari ", nrow(df_hasil), " jendela 3-detik) disimpan.")
  }
  if (!is.null(df_gagal)) {
    write.csv(df_gagal, file.path(dir_output, paste0("spesies_file_gagal_", kode_lokasi, ".csv")), row.names = FALSE)
  }

  df_hasil
}

buat_plot_top_spesies <- function(df, kode_lokasi) {
  if (is.null(df) || nrow(df) == 0 || all(is.na(df$nama_umum))) return(invisible(NULL))
  rekap <- aggregate(confidence ~ nama_umum, data = df, FUN = length)
  names(rekap) <- c("nama_umum", "jumlah_deteksi")
  rekap <- rekap[order(-rekap$jumlah_deteksi), ]
  top15 <- head(rekap, 15)

  p <- ggplot(top15, aes(x = reorder(nama_umum, jumlah_deteksi), y = jumlah_deteksi)) +
    geom_col(fill = "#1565c0") + coord_flip() +
    labs(title = paste("Top 15 Spesies Terdeteksi --", kode_lokasi),
         subtitle = paste0("min_confidence = ", min_confidence), x = NULL, y = "Jumlah deteksi") +
    theme_minimal()
  ggsave(file.path(dir_output, paste0("plot_top_spesies_", kode_lokasi, ".png")), p, width = 9, height = 6, dpi = 150)
}

# ============================== PROSES UTAMA =================================

file_df <- cari_file_wav(base_path)
if (is.null(file_df) || nrow(file_df) == 0) stop("Tidak ada file .wav ditemukan di: ", base_path)

message("Total ", nrow(file_df), " file .wav di ", length(unique(file_df$kode_lokasi)), " lokasi.")
daftar_lokasi <- unique(file_df$kode_lokasi)

message("\n########## BAGIAN A: INDEKS AKUSTIK ##########")
indeks_gabungan <- list()
for (lokasi in daftar_lokasi) {
  df_lokasi <- file_df[file_df$kode_lokasi == lokasi, ]
  hasil <- proses_indeks_lokasi(lokasi, df_lokasi)
  if (!is.null(hasil$hasil)) {
    indeks_gabungan[[lokasi]] <- hasil$hasil
    buat_plot_diel(hasil$hasil, lokasi)
    buat_plot_tren(hasil$hasil, lokasi)
  }
}
df_indeks_semua <- do.call(rbind, indeks_gabungan)
if (!is.null(df_indeks_semua)) {
  write.csv(df_indeks_semua, file.path(dir_output, "rekap_indeks_akustik_semua_lokasi.csv"), row.names = FALSE)
}

message("\n########## BAGIAN B: IDENTIFIKASI SPESIES (BirdNET) ##########")
message("Memuat model BirdNET -- percobaan pertama bisa mengunduh file model dulu...")
model_birdnet <- birdnet_model_protobuf()
message("Model siap.")

spesies_gabungan <- list()
for (lokasi in daftar_lokasi) {
  df_lokasi <- file_df[file_df$kode_lokasi == lokasi, ]
  hasil <- proses_spesies_lokasi(lokasi, df_lokasi, model_birdnet)
  if (!is.null(hasil)) {
    spesies_gabungan[[lokasi]] <- hasil
    buat_plot_top_spesies(hasil, lokasi)
  }
}
df_spesies_semua <- do.call(rbind, spesies_gabungan)
if (!is.null(df_spesies_semua)) {
  write.csv(df_spesies_semua, file.path(dir_output, "rekap_identifikasi_spesies_semua_lokasi.csv"), row.names = FALSE)
}

message("\n=== SELESAI ===")
message("Semua hasil (indeks akustik + identifikasi spesies) tersimpan di: ", dir_output)
message("Indeks akustik: ", if (is.null(df_indeks_semua)) 0 else nrow(df_indeks_semua), " baris dari ", length(daftar_lokasi), " lokasi.")
message("Identifikasi spesies: ", if (is.null(df_spesies_semua)) 0 else nrow(df_spesies_semua), " deteksi (confidence >= ", min_confidence, ").")
message("Deteksi yang meragukan bisa diverifikasi manual di https://xeno-canto.org/")
