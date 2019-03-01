library(tidyverse)
#setwd("/Users/hantangzhou/OneDrive/Columbia University in the City of New York/STAT GR5702/Final Project/edav_project")
data <- read_csv('Rodent_Inspection_new.csv')

clean = 0
if(clean == 1){
  data <- data %>% select(-JOB_TICKET_OR_WORK_ORDER_ID, -JOB_ID, -LOCATION, -JOB_PROGRESS, -BOROUGH, -X_COORD, 
                        -Y_COORD, -APPROVED_DATE, -ID)

  data <- data %>% select(-BBL, -LOT, -BLOCK, -HOUSE_NUMBER, -STREET_NAME)

  data <- na_if(data, 0)
  data <- na_if(data, 111111)

  data <- data %>% drop_na()

  data <- tibble::rowid_to_column(data, "ID")

  sample <- sample_n(data, 0.2 * nrow(data))

  write_csv(sample, "Rodent_Inspection_Lite.csv")
}

