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
sqf_df <- read_csv('/Users/flatironschol/FIS-Projects/Module4/data/sqf_df.csv')
sqf_df <- sqf_df %>% 
          mutate(STOP_FRISK_ID = ifelse(is.na(STOP_FRISK_ID), ser_num, STOP_FRISK_ID), 
                 YEAR2 = ifelse(is.na(YEAR2), year, YEAR2), 
                 SUSPECT_ARRESTED_FLAG = ifelse(is.na(SUSPECT_ARRESTED_FLAG), arstmade, SUSPECT_ARRESTED_FLAG), 
                 STOP_LOCATION_PRECINCT = ifelse(is.na(STOP_LOCATION_PRECINCT), pct, SUSPECT_ARRESTED_FLAG)) %>% 
          select(STOP_FRISK_ID, YEAR2, STOP_LOCATION_PRECINCT, SUSPECT_ARRESTED_FLAG)
sqf_df <- sqf_df %>% 
          mutate(SUSPECT_ARRESTED_FLAG = recode(SUSPECT_ARRESTED_FLAG,
                                                "N" = 0,
                                                "Y" = 1)) %>%
          group_by(YEAR2, STOP_LOCATION_PRECINCT) %>%
          summarise(STOPS = n(), STOP_ARRESTS = sum(SUSPECT_ARRESTED_FLAG))
write.csv(sqf_df, file='/Users/flatironschol/FIS-Projects/Module4/FIS-Mod4-Project/data/sqf_df.csv', row.names=FALSE)