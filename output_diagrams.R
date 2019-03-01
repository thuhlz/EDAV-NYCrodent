library(tidyverse)
setwd("/Users/hantangzhou/OneDrive/Columbia University in the City of New York/STAT GR5702/Final Project/edav_project")
data <- read_csv('Rodent_Inspection_Lite.csv')

chartTest <- function(data, chart_type){
  # distinct zip and distinct year
  zip_list <- as.list(data$ZIP_CODE)
  zip_list <- unique(zip_list)
  year_list <- format(as.Date(data$INSPECTION_DATE, format="%d/%m/%Y"),"%Y")
  year_list <- unique(year_list)
  
  for(year in year_list){
    year_data <- data %>% filter( format(as.Date(INSPECTION_DATE, format="%d/%m/%Y"),"%Y") == year)
    for(zip in zip_list){
      year_zip_data <- year_data %>% filter(ZIP_CODE == zip)
      filename <- ""
      filename <- paste(chart_type, toString(zip), sep = "_")
      filename <- paste(filename, toString(year), sep="_")
      filename <- paste(filename, ".jpg", sep="")
      
      ######################
      # replace with the proper plot function
      
      ggplot(data=year_zip_data, aes(x=INSPECTION_TYPE)) + geom_bar()
      
      ######################
      
      ggsave(filename)
    }
  }
}

chartTest(data, "hist")


