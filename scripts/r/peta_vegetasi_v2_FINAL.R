# Buat peta vegetasi kukang jawa LANGSUNG dari file Excel -- tanpa Python,
# tanpa git, tanpa folder "deha", dan TANPA Rtools (tidak pakai package
# yang butuh kompilasi seperti sf/terra). Cukup ganti path di bawah sesuai
# lokasi file Excel Anda, lalu jalankan seluruh script ini.
#
# Cara jalankan: buka file ini di RStudio, klik "Source" (atau tombol
# Ctrl+Shift+Enter / Cmd+Shift+Enter), atau select-all lalu Run.
#
# Kalau package di bawah belum terinstall, jalankan sekali saja:
#   install.packages(c("readxl", "dplyr", "ggplot2"))

library(readxl)
library(dplyr)
library(ggplot2)

# --- GANTI DUA BARIS DI BAWAH INI kalau lokasi/nama filenya beda ---
folder <- "C:/Users/Cipto Dwi Handono/OneDrive/Dokumen/Kukang Jawa, Kiarapayung/Kukang Jawa"
nama_file_excel <- "Data_Vegetasi_Kukang_Kiarapayung.xlsx"
# --------------------------------------------------------------------

file_excel <- file.path(folder, nama_file_excel)

data <- read_excel(file_excel, sheet = "Vegetasi Kukang", skip = 3)

data <- data %>%
  rename(
    titik = Titik,
    tipe = Tipe,
    nama_ilmiah = `Nama Ilmiah (tentatif)`,
    keyakinan = `Tingkat Keyakinan`,
    lat = Latitude,
    lon = Longitude
  ) %>%
  mutate(kategori = if_else(grepl("Bambu", tipe, ignore.case = TRUE), "Bambu (pohon tidur)", "Pohon"))

peta <- ggplot(data, aes(x = lon, y = lat)) +
  geom_point(aes(color = kategori), size = 4) +
  geom_text(aes(label = titik), size = 3, vjust = -1.1) +
  scale_color_manual(values = c("Pohon" = "#2e7d32", "Bambu (pohon tidur)" = "#8d6e63")) +
  coord_fixed() +
  labs(
    title = "Vegetasi Terkait Perjumpaan Kukang Jawa",
    subtitle = "Taman Kehati Kiarapayung -- identifikasi jenis masih tentatif dari foto",
    x = "Longitude", y = "Latitude", color = "Kategori"
  ) +
  theme_minimal()

output_path <- file.path(folder, "Peta_Vegetasi_Kukang_Kiarapayung.png")
ggsave(output_path, plot = peta, width = 7, height = 7)

cat("Peta tersimpan di:", output_path, "\n")
