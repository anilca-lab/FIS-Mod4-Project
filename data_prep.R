# This script prepares the data files for processing in Python
# while reducing their size.
rm(list = ls())
library(dplyr)
library(stringr)
complaints_df <- read_csv('/Users/flatironschol/FIS-Projects/Module4/data/NYPD_Complaint_Data_Historic.csv')
offense_types_df <- complaints_df %>% select(KY_CD, OFNS_DESC, PD_CD, PD_DESC) %>% distinct()
borough_df <- complaints_df %>% select(BORO_NM, ADDR_PCT_CD) %>% distinct()
complaints_df <- complaints_df %>% select(CMPLNT_NUM, RPT_DT, ADDR_PCT_CD, KY_CD)
complaints_df <- complaints_df %>% mutate(YEAR = as.numeric(str_sub(RPT_DT,-4,-1)))
complaints_df <- complaints_df %>% select(-RPT_DT) %>% group_by(YEAR, ADDR_PCT_CD, KY_CD) %>% summarise(CMPLNTS = n())
write.csv(complaints_df, file='/Users/flatironschol/FIS-Projects/Module4/data/complaints_df.csv', row.names=FALSE)
write.csv(offense_types_df, file='/Users/flatironschol/FIS-Projects/Module4/data/offense_types_df.csv', row.names=FALSE)
write.csv(borough_df, file='/Users/flatironschol/FIS-Projects/Module4/data/borough_df.csv', row.names=FALSE)

rm(list = ls())
library(dplyr)
library(stringr)
arrests_df <- read_csv('/Users/flatironschol/FIS-Projects/Module4/data/NYPD_Arrests_Data__Historic_.csv')
arrests_df <- arrests_df %>% 
              mutate(YEAR = as.numeric(str_sub(ARREST_DATE,-4,-1)), 
                     MONTH = as.numeric(str_sub(ARREST_DATE,-7,-6))) %>% 
              select(ARREST_KEY, YEAR, MONTH, KY_CD, ARREST_PRECINCT, AGE_GROUP:PERP_RACE)
write.csv(arrests_df, file='/Users/flatironschol/FIS-Projects/Module4/data/arrests_df_ind.csv', row.names=FALSE)
arrests_df <- arrests_df %>%
              group_by(YEAR, ARREST_PRECINCT) %>%
              summarise(ARRESTS = n())
write.csv(arrests_df, file='/Users/flatironschol/FIS-Projects/Module4/FIS-Mod4-Project/data/arrests_df.csv', row.names=FALSE)

rm(list = ls())
library(dplyr)
library(readxl)
sqf_df = data.frame()
for (year in 2016:2018) {
  if (year <= 2014) {
    filename <- paste0('/Users/flatironschol/FIS-Projects/Module4/data/',year,'.csv',collapse='')
    df <- read_csv(filename)
    df <- df %>% mutate_if(is.numeric,as.character) %>% mutate_if(is.logical,as.character) %>% mutate(datestop = as.character(datestop), dob = as.character(dob))
  } else if (year <= 2016) {
    filename <- paste0('/Users/flatironschol/FIS-Projects/Module4/data/sqf-',year,'.csv',collapse='')
    df <- read_csv(filename)
    df <- df %>% mutate_if(is.numeric,as.character) %>% mutate_if(is.logical,as.character)
  } else {
    filename <- paste0('/Users/flatironschol/FIS-Projects/Module4/data/sqf-',year,'.xlsx',collapse='')
    df <- read_excel(filename)
    df <- df %>% mutate_if(is.numeric,as.character) %>% mutate_if(is.logical,as.character)
  }
  sqf_df <- bind_rows(sqf_df, df)
}
sqf_df <- sqf_df %>% 
          mutate(STOP_FRISK_ID = ifelse(is.na(STOP_FRISK_ID), as.numeric(ser_num), as.numeric(STOP_FRISK_ID)), 
                 YEAR2 = ifelse(is.na(YEAR2), as.numeric(year), as.numeric(YEAR2)), 
                 SUSPECT_ARRESTED_FLAG = ifelse(is.na(SUSPECT_ARRESTED_FLAG), arstmade, SUSPECT_ARRESTED_FLAG), 
                 STOP_LOCATION_PRECINCT = ifelse(is.na(STOP_LOCATION_PRECINCT), as.numeric(pct), as.numeric(STOP_LOCATION_PRECINCT))) %>% 
          select(STOP_FRISK_ID, YEAR2, STOP_LOCATION_PRECINCT, SUSPECT_ARRESTED_FLAG)
sqf_df <- sqf_df %>% 
          mutate(SUSPECT_ARRESTED_FLAG = recode(SUSPECT_ARRESTED_FLAG,
                                                "N" = 0,
                                                "Y" = 1)) %>%
          group_by(YEAR2, STOP_LOCATION_PRECINCT) %>%
          summarise(STOPS = n(), STOP_ARRESTS = sum(SUSPECT_ARRESTED_FLAG))
write.csv(sqf_df, file='/Users/flatironschol/FIS-Projects/Module4/FIS-Mod4-Project/data/sqf_df_1.csv', row.names=FALSE)

rm(list = ls())
library(dplyr)
population_df <- read_csv('/Users/flatironschol/FIS-Projects/Module4/data/NYC_Blocks_2010CensusData_Plus_Precincts.csv')
population_df <- population_df %>%
                 select(precinct, P0010001) %>%
                 group_by(precinct) %>%
                 summarise(POPULATION = sum(P0010001))
write.csv(population_df, file='/Users/flatironschol/FIS-Projects/Module4/FIS-Mod4-Project/data/population_df.csv', row.names=FALSE)