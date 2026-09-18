# Analyze the processed point data and produce summary stats + a plot.
#
# Workflow: QGIS -> data/raw/*.geojson -> scripts/python/process_geodata.py
# -> data/processed/*.csv -> this script -> outputs/
#
# Run with: Rscript scripts/r/analyze_data.R

library(readr)
library(dplyr)
library(ggplot2)

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), "..", ".."))
input_path <- file.path(root, "data", "processed", "sample_processed.csv")
report_path <- file.path(root, "outputs", "reports", "summary.csv")
figure_path <- file.path(root, "outputs", "figures", "population_vs_distance.png")

data <- read_csv(input_path, show_col_types = FALSE)

summary_stats <- data %>%
  summarise(
    n_cities = n(),
    mean_population = mean(population),
    mean_distance_km = mean(distance_from_jakarta_km),
    max_distance_km = max(distance_from_jakarta_km)
  )

dir.create(dirname(report_path), recursive = TRUE, showWarnings = FALSE)
write_csv(summary_stats, report_path)

dir.create(dirname(figure_path), recursive = TRUE, showWarnings = FALSE)
plot <- ggplot(data, aes(x = distance_from_jakarta_km, y = population, label = name)) +
  geom_point(size = 3) +
  geom_text(vjust = -1) +
  labs(
    title = "Population vs. Distance from Jakarta",
    x = "Distance from Jakarta (km)",
    y = "Population"
  ) +
  theme_minimal()

ggsave(figure_path, plot = plot, width = 7, height = 5)

cat("Summary written to", report_path, "\n")
cat("Figure written to", figure_path, "\n")
