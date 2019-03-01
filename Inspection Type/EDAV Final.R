library(tidyverse)
setwd("/Users/hantangzhou/OneDrive/Columbia University in the City of New York/STAT GR5702/Final Project/edav_project")
data <- read_csv('Rodent_Inspection.csv')
#data_original <- read_csv('Rodent_Inspection.csv')

# clean up sample data
#data <- data %>% mutate(INSPECTION_DATE = str_sub(INSPECTION_DATE, start = 1, end = 10))
#data <- data %>% mutate(APPROVED_DATE = str_sub(APPROVED_DATE, start = 1, end = 10))
#data <- data %>% mutate(INSPECTION_DATE = as.Date(x = INSPECTION_DATE, format = "%m/%d/%Y"))
#data <- data %>% mutate(APPROVED_DATE = as.Date(x = APPROVED_DATE, format = "%m/%d/%Y"))
write_csv(data, "Rodent_Inspection_modified.csv")

# bar chart of total inspection
bar_chart <- ggplot(data, aes(fill=BOROUGH, INSPECTION_TYPE)) + geom_bar() + 
  theme(axis.text.x = element_text(size = 8, angle=45)) +
  ggtitle("Number of Inspection In New York City") + ylab("Count") + xlab("Inspection Type")
bar_chart

# facet bar chart of 
facet_bar_chart <- ggplot(data, aes(INSPECTION_TYPE, fill = INSPECTION_TYPE, color = INSPECTION_TYPE)) + geom_bar() + 
  facet_wrap(~BOROUGH) + theme(axis.text.x = element_text(size = 0, angle=60), legend.position = c(0.85, 0.2)) + 
  ggtitle("Number of Inspection In New York City By Borough") + ylab("Count") + xlab("Inspection Type")
facet_bar_chart


# drawing the map by zip
library(choroplethr)
library(choroplethrMaps)
library(choroplethrZip)
data(zip.regions)

total_data <- data %>% group_by(ZIP_CODE) %>% summarize(value = n())
total_data <-  total_data %>% mutate(region = as.character(ZIP_CODE))
total_data <-  total_data %>% select(-ZIP_CODE)
total_data <- filter( total_data,  total_data$region %in% pull(zip.regions,1))
total_map <- zip_choropleth( total_data, zip_zoom =  total_data$region,
                             title      = "New York City Rodent Inspections By Zip",
                             legend     = "Total Inspections")
total_map


# represent the inspection by time
total_density <- ggplot(data=data, aes(INSPECTION_DATE, fill = INSPECTION_TYPE)) + geom_histogram()
total_density

total_density_borough <- ggplot(data=data, aes(INSPECTION_DATE, fill = INSPECTION_TYPE)) + geom_histogram() + 
  facet_wrap(~BOROUGH) + theme(axis.text.x = element_text(size = 8, angle=60), legend.position = c(0.85, 0.2))
total_density_borough

