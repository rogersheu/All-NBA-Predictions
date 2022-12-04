palette_initialization <- function() {
  n <- 60
  #qual_col_pals <- brewer.pal.info[brewer.pal.info$category == 'qual',]
  #col_vector <- unlist(mapply(brewer.pal, qual_col_pals$maxcolors, rownames(qual_col_pals)))
  palette <- distinctColorPalette(n)
  col_vector <- unname(distinctColorPalette(n))

  return(col_vector)
  #pie(rep(1,n), col=sample(col_vector, n))
}
