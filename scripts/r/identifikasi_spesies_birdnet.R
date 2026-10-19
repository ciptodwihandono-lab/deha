## Identifikasi Spesies Otomatis dari Rekaman Song Meter Micro 2 (BirdNET)
##
## CATATAN PENTING soal xeno-canto.org: situs itu BUKAN alat identifikasi
## otomatis -- itu database referensi suara yang dicari manual per
## spesies/lokasi untuk didengarkan & dibandingkan. Model BirdNET yang
## dipakai skrip ini justru DILATIH memakai banyak data dari xeno-canto,
## jadi hasil identifikasi di sini sudah "mewarisi" referensi xeno-canto
## secara otomatis. Kalau nanti ada deteksi yang meragukan dan mau
## diverifikasi manual, baru buka xeno-canto.org, cari nama spesies hasil
## deteksi, dengarkan contoh rekamannya, bandingkan dengan rekamanmu.
##
## Package: birdnetR (wrapper R resmi dari tim BirdNET -- Cornell Lab /
## Chemnitz University, https://github.com/birdnet-team/birdnetR).
## Di balik layar package ini memanggil model Python lewat `reticulate`,
## jadi PERCOBAAN PERTAMA akan otomatis memasang Python + dependensinya
## (bisa makan waktu beberapa menit dan butuh koneksi internet) --
## biarkan saja berjalan, jangan ditutup di tengah proses.
##
## Data: rekaman .WAV Song Meter Micro 2 (SN 2MM27997), satu subfolder
## per lokasi di dalam F:/Audiomoth/UT 2026, durasi 1 menit per file.
## BirdNET otomatis memotong tiap file jadi jendela analisis 3 detik,
## jadi satu file 1 menit bisa menghasilkan banyak baris deteksi.
##
## PENTING -- soal nama kolom hasil: dokumentasi resmi package belum
## mencantumkan daftar lengkap nama kolom hasil (`as.data.frame()`),
## jadi skrip ini mencari kolom yang relevan secara otomatis (cari kata
## "confidence", "scientific", "common", "start", dst di nama kolom).
## Kalau deteksi otomatis gagal, skrip akan berhenti dengan pesan berisi
## daftar nama kolom asli, supaya bisa disesuaikan manual.
##
## Tiap lokasi diproses dan disimpan TERPISAH (CSV per lokasi), plus
## satu CSV rekap gabungan dan grafik top spesies per lokasi.

# ============================== KONFIGURASI =================================

base_path      <- "F:/Audiomoth/UT 2026"
dir_output     <- file.path(dirname(base_path), "hasil_identifikasi_spesies_UT2026")
id_alat        <- "2MM27997"
min_confidence <- 0.5   # 0-1, makin tinggi makin ketat (default package 0.1 = sangat longgar,
                         # banyak false positive -- 0.5 titik awal yang lebih aman untuk disaring)

# ============================== PACKAGE ======================================

if (!"birdnetR" %in% rownames(installed.packages())) {
  message("Menginstal package birdnetR (sekali saja)...")
  install.packages("birdnetR")
}
library(birdnetR)
library(ggplot2)

dir.create(dir_output, showWarnings = FALSE, recursive = TRUE)

message("Memuat model BirdNET -- percobaan pertama bisa lama (unduh Python & model)...")
model <- load_birdnet(type = "acoustic")
message("Model siap.")

# ============================== FUNGSI =======================================

# Cari semua file .wav per subfolder lokasi (sama seperti skrip indeks akustik).
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

# Cocokkan nama kolom hasil BirdNET secara fleksibel (karena nama kolom
# pasti dari dokumentasi belum bisa dipastikan 100%) lalu ganti jadi
# nama standar yang dipakai skrip ini.
standardisasi_kolom_birdnet <- function(df) {
  nama_asli <- names(df)
  cari_kolom <- function(pola) {
    idx <- grep(pola, nama_asli, ignore.case = TRUE)
    if (length(idx) == 0) NA_character_ else nama_asli[idx[1]]
  }

  peta <- list(
    file_asli = cari_kolom("^input$|file|path"),
    waktu_mulai = cari_kolom("start"),
    waktu_selesai = cari_kolom("end"),
    nama_ilmiah = cari_kolom("scientific"),
    nama_umum = cari_kolom("common"),
    confidence = cari_kolom("confidence|score")
  )

  wajib <- c("confidence")
  hilang_wajib <- wajib[is.na(unlist(peta[wajib]))]
  if (length(hilang_wajib) > 0) {
    stop(
      "Tidak menemukan kolom penting (", paste(hilang_wajib, collapse = ", "), ") secara otomatis.\n",
      "Kolom yang tersedia di hasil BirdNET: ", paste(nama_asli, collapse = ", "), "\n",
      "Sesuaikan fungsi standardisasi_kolom_birdnet() secara manual memakai daftar kolom di atas."
    )
  }

  hasil <- data.frame(row.names = seq_len(nrow(df)))
  for (nm in names(peta)) {
    hasil[[nm]] <- if (!is.na(peta[[nm]])) df[[peta[[nm]]]] else NA
  }

  if (anyNA(hasil$nama_ilmiah) && anyNA(hasil$nama_umum)) {
    message("  (Catatan: kolom nama_ilmiah/nama_umum tidak terdeteksi otomatis -- ",
            "cek kolom asli berikut dan sesuaikan manual: ", paste(nama_asli, collapse = ", "), ")")
  }

  hasil
}

# Proses satu lokasi: panggil BirdNET sekali untuk semua file lokasi itu.
proses_satu_lokasi <- function(kode_lokasi, file_df) {
  message("\n== Memproses lokasi: ", kode_lokasi, " (", nrow(file_df), " file) ==")

  hasil <- tryCatch({
    prediksi <- predict(model, files = file_df$path_file,
                         min_confidence = min_confidence, progress = "progress")
    df_mentah <- as.data.frame(prediksi)
    df_standar <- standardisasi_kolom_birdnet(df_mentah)
    df_standar$kode_lokasi <- kode_lokasi
    df_standar$id_alat <- id_alat
    df_standar
  }, error = function(e) {
    message("  GAGAL memproses lokasi ", kode_lokasi, ": ", conditionMessage(e))
    NULL
  })

  if (!is.null(hasil)) {
    path_csv <- file.path(dir_output, paste0("hasil_identifikasi_spesies_", kode_lokasi, ".csv"))
    write.csv(hasil, path_csv, row.names = FALSE)
    message("  -> ", nrow(hasil), " deteksi disimpan: ", path_csv)
  }

  hasil
}

# Grafik top 15 spesies (jumlah deteksi) untuk satu lokasi.
buat_plot_top_spesies <- function(df, kode_lokasi) {
  if (is.null(df) || nrow(df) == 0 || all(is.na(df$nama_umum))) return(invisible(NULL))

  rekap <- aggregate(confidence ~ nama_umum, data = df, FUN = length)
  names(rekap) <- c("nama_umum", "jumlah_deteksi")
  rekap <- rekap[order(-rekap$jumlah_deteksi), ]
  top15 <- head(rekap, 15)

  p <- ggplot(top15, aes(x = reorder(nama_umum, jumlah_deteksi), y = jumlah_deteksi)) +
    geom_col(fill = "#1565c0") +
    coord_flip() +
    labs(
      title = paste("Top 15 Spesies Terdeteksi --", kode_lokasi),
      subtitle = paste0("min_confidence = ", min_confidence),
      x = NULL, y = "Jumlah deteksi"
    ) +
    theme_minimal()

  ggsave(file.path(dir_output, paste0("plot_top_spesies_", kode_lokasi, ".png")),
         p, width = 9, height = 6, dpi = 150)
}

# ============================== PROSES UTAMA =================================

file_df <- cari_file_wav(base_path)
if (is.null(file_df) || nrow(file_df) == 0) stop("Tidak ada file .wav ditemukan di: ", base_path)

message("Total ", nrow(file_df), " file .wav di ", length(unique(file_df$kode_lokasi)), " lokasi.")

daftar_lokasi <- unique(file_df$kode_lokasi)
hasil_gabungan <- list()

for (lokasi in daftar_lokasi) {
  df_lokasi <- file_df[file_df$kode_lokasi == lokasi, ]
  hasil <- proses_satu_lokasi(lokasi, df_lokasi)
  if (!is.null(hasil)) {
    hasil_gabungan[[lokasi]] <- hasil
    buat_plot_top_spesies(hasil, lokasi)
  }
}

df_semua <- do.call(rbind, hasil_gabungan)
write.csv(df_semua, file.path(dir_output, "rekap_semua_lokasi.csv"), row.names = FALSE)

message("\n=== SELESAI ===")
message("Hasil tersimpan di: ", dir_output)
message(nrow(df_semua), " deteksi dari ", length(daftar_lokasi), " lokasi (ambang confidence >= ", min_confidence, ").")
message("Kalau ada deteksi yang mau diverifikasi manual, cari nama spesiesnya di https://xeno-canto.org/ untuk dengarkan referensi suaranya.")
