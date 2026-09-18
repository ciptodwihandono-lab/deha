# Buat peta choropleth dari data batas wilayah + atribut.
#
# Contoh skala kecil (kecamatan di Kota Yogyakarta) sebagai bukti alur kerja.
# Untuk skala nasional, ganti input dengan boundary seluruh Indonesia (lihat
# data/raw/boundaries/README.md) -- kode di bawah tidak perlu diubah selama
# nama kolom (kecamatan, kepadatan_penduduk) tetap konsisten.
#
# Workflow: data/raw/boundaries/*.geojson -> scripts/python/prepare_boundaries.py
# -> data/processed/*.geojson -> this script -> outputs/
#
# Run with: Rscript scripts/r/map_indonesia.R

library(sf)
library(dplyr)
library(ggplot2)

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), "..", ".."))
input_path <- file.path(root, "data", "processed", "kecamatan_yogyakarta.geojson")
figure_path <- file.path(root, "outputs", "figures", "peta_kecamatan_yogyakarta.png")

boundaries <- st_read(input_path, quiet = TRUE)

peta <- ggplot(boundaries) +
  geom_sf(aes(fill = kepadatan_penduduk), color = "white", linewidth = 0.2) +
  scale_fill_viridis_c(name = "Kepadatan\nPenduduk", option = "magma") +
  labs(
    title = "Kepadatan Penduduk per Kecamatan - Kota Yogyakarta",
    subtitle = "Contoh peta tematik (data atribut simulasi)"
  ) +
  theme_minimal() +
  theme(axis.text = element_blank(), axis.ticks = element_blank())

dir.create(dirname(figure_path), recursive = TRUE, showWarnings = FALSE)
ggsave(figure_path, plot = peta, width = 7, height = 7)

cat("Peta tersimpan di", figure_path, "\n")
