## Analisis Indeks Akustik Soundscape dari Data AudioMoth
##
## Data: rekaman .WAV mentah AudioMoth, satu subfolder per lokasi di
## dalam folder utama (default: F:/Audiomoth/UT 2026). Nama file
## mengikuti konvensi AudioMoth: YYYYMMDD_HHMMSS.WAV.
##
## Tiap lokasi diproses dan disimpan TERPISAH (CSV & grafik per
## lokasi), plus satu CSV rekap gabungan untuk referensi.
##
## Cara pakai: ubah bagian KONFIGURASI di bawah sesuai kebutuhan, lalu
## jalankan seluruh skrip (tombol "Source" di RStudio).

# ============================== KONFIGURASI =================================

base_path         <- "F:/Audiomoth/UT 2026"   # folder utama berisi subfolder per lokasi
dir_output         <- file.path(dirname(base_path), "hasil_analisis_akustik_UT2026")
durasi_segmen_detik <- 60   # rekaman dipecah per 60 detik sebelum hitung indeks
durasi_segmen_min   <- 30   # sisa potongan < 30 detik di akhir file dibuang

# ============================== PACKAGE ======================================

paket_dibutuhkan <- c("tuneR", "seewave", "soundecology", "lubridate", "ggplot2")
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

dir.create(dir_output, showWarnings = FALSE, recursive = TRUE)

# ============================== FUNGSI =======================================

# Cari semua file .wav, dikelompokkan per subfolder (lokasi) langsung di bawah base_path.
cari_file_wav <- function(base_path) {
  lokasi_dirs <- list.dirs(base_path, full.names = TRUE, recursive = FALSE)
  # list.dirs kadang menyertakan base_path itu sendiri -- buang supaya file
  # tidak terhitung dobel (sekali per lokasi, sekali lagi di bawah base_path).
  lokasi_dirs <- lokasi_dirs[normalizePath(lokasi_dirs, mustWork = FALSE) !=
                                normalizePath(base_path, mustWork = FALSE)]

  if (length(lokasi_dirs) == 0) {
    message("Tidak ada subfolder lokasi ditemukan -- semua file dianggap satu lokasi: ",
            basename(base_path))
    lokasi_dirs <- base_path
  }

  daftar <- lapply(lokasi_dirs, function(dir_lokasi) {
    file_wav <- list.files(dir_lokasi, pattern = "\\.wav$", ignore.case = TRUE,
                            recursive = TRUE, full.names = TRUE)
    if (length(file_wav) == 0) return(NULL)
    data.frame(
      kode_lokasi = basename(dir_lokasi),
      path_file = file_wav,
      stringsAsFactors = FALSE
    )
  })

  do.call(rbind, daftar)
}

# Parse timestamp dari nama file AudioMoth (format YYYYMMDD_HHMMSS).
parse_timestamp_audiomoth <- function(nama_file) {
  m <- regmatches(nama_file, regexpr("\\d{8}_\\d{6}", nama_file))
  if (length(m) == 0) return(as.POSIXct(NA))
  ymd_hms(m, tz = "UTC")
}

# Pecah Wave panjang jadi daftar segmen pendek (durasi_segmen detik).
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

# Hitung 6 indeks akustik untuk satu segmen Wave.
hitung_indeks_segmen <- function(wave_segmen) {
  aci <- suppressWarnings(acoustic_complexity(wave_segmen))
  adi <- suppressWarnings(acoustic_diversity(wave_segmen))
  aei <- suppressWarnings(acoustic_evenness(wave_segmen))
  ndsi_hasil <- suppressWarnings(ndsi(wave_segmen))
  bio <- suppressWarnings(bioacoustic_index(wave_segmen))
  entropi <- suppressWarnings(H(wave_segmen))

  data.frame(
    ACI = aci$AciTotAll_left,
    ADI = adi$adi_left,
    AEI = aei$aei_left,
    NDSI = ndsi_hasil$ndsi_left,
    BI = bio$left_area,
    H = entropi
  )
}

# Proses semua file satu lokasi: baca, pecah segmen, hitung indeks, simpan CSV.
proses_satu_lokasi <- function(kode_lokasi, file_df) {
  message("\n== Memproses lokasi: ", kode_lokasi, " (", nrow(file_df), " file) ==")

  hasil_semua <- list()
  gagal_semua <- list()

  for (i in seq_len(nrow(file_df))) {
    path_file <- file_df$path_file[i]
    nama_file <- basename(path_file)

    if (i %% 10 == 0 || i == nrow(file_df)) {
      message("  [", kode_lokasi, "] file ", i, "/", nrow(file_df))
    }

    waktu_file <- parse_timestamp_audiomoth(nama_file)

    hasil_file <- tryCatch({
      wave <- readWave(path_file)
      segmen_list <- pecah_segmen(wave, durasi_segmen_detik, durasi_segmen_min)

      baris_segmen <- lapply(segmen_list, function(seg) {
        indeks <- hitung_indeks_segmen(seg$wave)
        waktu_segmen <- waktu_file + seg$offset_detik
        cbind(
          data.frame(
            kode_lokasi = kode_lokasi,
            nama_file = nama_file,
            offset_detik = seg$offset_detik,
            timestamp = waktu_segmen,
            tanggal = as.Date(waktu_segmen),
            jam = hour(waktu_segmen)
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
    path_csv <- file.path(dir_output, paste0("hasil_indeks_akustik_", kode_lokasi, ".csv"))
    write.csv(df_hasil, path_csv, row.names = FALSE)
    message("  -> Disimpan: ", path_csv)
  }
  if (!is.null(df_gagal)) {
    path_csv_gagal <- file.path(dir_output, paste0("file_gagal_", kode_lokasi, ".csv"))
    write.csv(df_gagal, path_csv_gagal, row.names = FALSE)
    message("  -> ", nrow(df_gagal), " file gagal diproses, dicatat di: ", path_csv_gagal)
  }

  list(hasil = df_hasil, gagal = df_gagal)
}

# Grafik pola diel (rata-rata indeks per jam) untuk satu lokasi.
buat_plot_diel <- function(df, kode_lokasi) {
  df_panjang <- reshape(
    df, varying = c("ACI", "ADI", "AEI", "NDSI", "BI", "H"),
    v.names = "nilai", timevar = "indeks",
    times = c("ACI", "ADI", "AEI", "NDSI", "BI", "H"), direction = "long"
  )

  p <- ggplot(df_panjang, aes(x = jam, y = nilai)) +
    stat_summary(fun = mean, geom = "line", color = "#1565c0") +
    stat_summary(fun = mean, geom = "point", color = "#1565c0") +
    facet_wrap(~indeks, scales = "free_y") +
    labs(
      title = paste("Pola Diel Indeks Akustik --", kode_lokasi),
      x = "Jam (0-23)", y = "Rata-rata nilai indeks"
    ) +
    theme_minimal()

  ggsave(file.path(dir_output, paste0("plot_diel_", kode_lokasi, ".png")), p, width = 10, height = 6, dpi = 150)
}

# Grafik tren indeks dari waktu ke waktu untuk satu lokasi.
buat_plot_tren <- function(df, kode_lokasi) {
  df_panjang <- reshape(
    df, varying = c("ACI", "ADI", "AEI", "NDSI", "BI", "H"),
    v.names = "nilai", timevar = "indeks",
    times = c("ACI", "ADI", "AEI", "NDSI", "BI", "H"), direction = "long"
  )

  p <- ggplot(df_panjang, aes(x = timestamp, y = nilai)) +
    geom_line(color = "#2e7d32", alpha = 0.6) +
    geom_point(color = "#2e7d32", size = 0.8) +
    facet_wrap(~indeks, scales = "free_y") +
    labs(
      title = paste("Tren Indeks Akustik dari Waktu ke Waktu --", kode_lokasi),
      x = "Waktu", y = "Nilai indeks"
    ) +
    theme_minimal()

  ggsave(file.path(dir_output, paste0("plot_tren_", kode_lokasi, ".png")), p, width = 10, height = 6, dpi = 150)
}

# ============================== PROSES UTAMA =================================

file_df <- cari_file_wav(base_path)

if (is.null(file_df) || nrow(file_df) == 0) {
  stop("Tidak ada file .wav ditemukan di: ", base_path)
}

message("Total ", nrow(file_df), " file .wav ditemukan di ", length(unique(file_df$kode_lokasi)), " lokasi.")

daftar_lokasi <- unique(file_df$kode_lokasi)
hasil_gabungan <- list()
gagal_gabungan <- list()

for (lokasi in daftar_lokasi) {
  df_lokasi <- file_df[file_df$kode_lokasi == lokasi, ]
  hasil <- proses_satu_lokasi(lokasi, df_lokasi)

  if (!is.null(hasil$hasil)) {
    hasil_gabungan[[lokasi]] <- hasil$hasil
    buat_plot_diel(hasil$hasil, lokasi)
    buat_plot_tren(hasil$hasil, lokasi)
  }
  if (!is.null(hasil$gagal)) gagal_gabungan[[lokasi]] <- hasil$gagal
}

df_semua <- do.call(rbind, hasil_gabungan)
write.csv(df_semua, file.path(dir_output, "rekap_semua_lokasi.csv"), row.names = FALSE)

if (length(gagal_gabungan) > 0) {
  df_semua_gagal <- do.call(rbind, gagal_gabungan)
  write.csv(df_semua_gagal, file.path(dir_output, "rekap_file_gagal.csv"), row.names = FALSE)
}

# Grafik pembanding antar-lokasi (opsional, panel terpisah per lokasi)
if (length(unique(df_semua$kode_lokasi)) > 1) {
  p_banding <- ggplot(df_semua, aes(x = jam, y = ACI)) +
    stat_summary(fun = mean, geom = "line", color = "#c62828") +
    facet_wrap(~kode_lokasi) +
    labs(title = "Pembanding Pola Diel ACI Antar-Lokasi", x = "Jam (0-23)", y = "Rata-rata ACI") +
    theme_minimal()
  ggsave(file.path(dir_output, "plot_pembanding_lokasi_ACI.png"), p_banding, width = 10, height = 6, dpi = 150)
}

message("\n=== SELESAI ===")
message("Hasil tersimpan di: ", dir_output)
message(nrow(df_semua), " baris (file/segmen) berhasil diproses dari ", length(daftar_lokasi), " lokasi.")
