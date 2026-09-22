# Optional: pre-install the R packages required by the plotting notebooks, at the
# exact versions used to generate the article figures.
#
# The notebooks under plots/ install any missing package automatically on first run,
# so this script is optional. Use it if you prefer to install everything up-front at
# the pinned versions below.
#
# Usage:
#   conda activate plots
#   Rscript plots/install_R_packages.R

options(repos = c(CRAN = "https://cloud.r-project.org"))

# CRAN packages at the versions used for the figures
cran_packages <- list(
  ade4         = "1.7-23",
  aricode      = "1.0.3",
  circlize     = "0.4.16",
  cluster      = "2.1.8",
  dendextend   = "1.19.1",
  dplyr        = "1.1.4",
  ggbreak      = "0.1.6",
  ggforce      = "0.5.0",
  ggplot2      = "4.0.0",
  glue         = "1.8.0",
  gplots       = "3.2.0",
  gridExtra    = "2.3",
  jsonlite     = "2.0.0",
  patchwork    = "1.3.2",
  plotly       = "4.12.0",
  purrr        = "1.1.0",
  RColorBrewer = "1.1-3",
  readr        = "2.2.0",
  reshape2     = "1.4.4",
  rstatix      = "1.0.0",
  stringr      = "1.5.2",
  tidyr        = "1.3.1"
)

# Bioconductor packages at the versions used for the figures. Bioconductor pins
# per-package versions via its release version; ggtree 3.10.1 / ggtreeExtra 1.16.0
# belong to the Bioconductor 3.20 release.
bioc_version <- "3.20"
bioc_packages <- c("ggtree", "ggtreeExtra")

if (!requireNamespace("remotes", quietly = TRUE)) {
  install.packages("remotes")
}

installed <- rownames(installed.packages())

for (pkg in names(cran_packages)) {
  if (!pkg %in% installed) {
    message("Installing ", pkg, " ", cran_packages[[pkg]])
    remotes::install_version(pkg, version = cran_packages[[pkg]], quiet = TRUE)
  } else {
    message("Already installed: ", pkg)
  }
}

if (!requireNamespace("BiocManager", quietly = TRUE)) {
  install.packages("BiocManager")
}
message("Installing Bioconductor ", bioc_version, " packages: ",
        paste(bioc_packages, collapse = ", "))
BiocManager::install(bioc_packages, version = bioc_version,
                     update = FALSE, ask = FALSE)

cat("All R packages for plots/ installed.\n")
