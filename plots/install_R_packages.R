# Optional: pre-install the R packages required by the plotting notebooks.
#
# The notebooks under plots/ already install any missing package automatically on
# first run, so running this script is optional. Use it if you prefer to install
# everything up-front (e.g. to avoid re-downloading each time).
#
# Usage:
#   conda activate plots
#   Rscript plots/install_R_packages.R

cran_packages <- c(
  "ggplot2", "dplyr", "glue", "RColorBrewer",
  "dendextend", "patchwork", "circlize", "rstatix",
  "reshape2", "ggbreak", "stringr", "tidyr", "plotly",
  "ggforce", "purrr", "gplots", "jsonlite",
  "aricode", "readr", "ade4", "gridExtra", "cluster"
)

bioc_packages <- c("ggtree", "ggtreeExtra")

install.packages(cran_packages)

if (!requireNamespace("BiocManager", quietly = TRUE)) {
  install.packages("BiocManager")
}
BiocManager::install(bioc_packages, update = FALSE, ask = FALSE)

cat("All R packages for plots/ installed.\n")
