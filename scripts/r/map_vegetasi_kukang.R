# Buat peta titik vegetasi kukang jawa, warna per kategori.
#
# Workflow: data/raw/observations/vegetasi_kukang_jawa.csv (isi koordinat)
# -> scripts/python/convert_coordinates.py -> data/processed/vegetasi_kukang_jawa.geojson
# -> this script -> outputs/figures/peta_vegetasi_kukang_kiarapayung.png
#
# Run with: Rscript scripts/r/map_vegetasi_kukang.R

library(sf)
library(dplyr)
library(ggplot2)

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), "..", ".."))
input_path <- file.path(root, "data", "processed", "vegetasi_kukang_jawa.geojson")
figure_path <- file.path(root, "outputs", "figures", "peta_vegetasi_kukang_kiarapayung.png")

titik <- st_read(input_path, quiet = TRUE)

warna_kategori <- c(
  pohon_pakan = "#2e7d32",
  pohon_tidur = "#8d6e63",
  belum_teridentifikasi = "#9e9e9e",
  lainnya = "#1565c0"
)

peta <- ggplot(titik) +
  geom_sf(aes(color = kategori), size = 3) +
  geom_sf_text(aes(label = titik), size = 2.8, nudge_y = 0.00005, check_overlap = TRUE) +
  scale_color_manual(values = warna_kategori, name = "Kategori") +
  labs(
    title = "Vegetasi Terkait Perjumpaan Kukang Jawa",
    subtitle = "Taman Kehati Kiarapayung -- identifikasi jenis masih tentatif dari foto"
  ) +
  theme_minimal() +
  theme(axis.text = element_blank(), axis.ticks = element_blank())

dir.create(dirname(figure_path), recursive = TRUE, showWarnings = FALSE)
ggsave(figure_path, plot = peta, width = 7, height = 7)

cat("Peta tersimpan di", figure_path, "\n")
