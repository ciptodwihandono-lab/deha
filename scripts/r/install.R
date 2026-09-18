# Install R dependencies for this project.
# Run once with: Rscript scripts/r/install.R

packages <- c("readr", "dplyr", "ggplot2", "sf", "terra")

installed <- rownames(installed.packages())
to_install <- setdiff(packages, installed)

if (length(to_install) > 0) {
  install.packages(to_install, repos = "https://cloud.r-project.org")
}
