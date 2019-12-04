#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:22:12 2019

@author: flatironschol
"""
import pandas as pd

USE_COMPLAINT_COLS = ['RPT_DT','ADDR_PCT_CD','KY_CD',
                      'LAW_CAT_CD','SUSP_AGE_GROUP',
                      'SUSP_RACE', 'SUSP_SEX', 'Latitude', 'Longitude']

USE_ARREST_COLS = ['ARREST_DATE', 'ARREST_PRECINCT',
                   'KY_CD','LAW_CAT_CD','AGE_GROUP',
                   'PERP_RACE', 'PERP_SEX', 'Latitude', 'Longitude']

def create_complaint_df(datadir='../data', outcols=USE_COMPLAINT_COLS):
    """read and write clean complaint data csv
SOURCE: https://data.cityofnewyork.us/api/views/qgea-i56i/rows.csv?accessType=DOWNLOAD
ABOUT: https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Historic/qgea-i56i

RPT_DT = report date (we don't have as comprehensive coverage of CMPLNT_FR_DT)
ADDR_PCT_CD = precinct
KY_CD = offense id
    """
    complaints_df = pd.read_csv(f'{datadir}/NYPD_Complaint_Data_Historic.csv',
                                dtype={'CMPLNT_NUM' : 'Int64',
                                       'ADDR_PCT_CD' : 'Int64'},
                                na_values=['  "error" : true',
                                           '  "message" : "Internal error"',
                                           '  "status" : 500',
                                           '}'],
                            parse_dates=['RPT_DT'])
    complaints_df = complaints_df.dropna(subset = ['CMPLNT_NUM', 'RPT_DT', 'ADDR_PCT_CD', 'KY_CD', 'LAW_CAT_CD'])
    complaints_df.rename(columns={'ADDR_PCT_CD' : 'precinct'})
    complaints_df[outcols].to_csv(f'data/full_complaints_df.csv', index=False)
    return complaints_df[outcols]

def create_arrests_df(datadir='../data', outcols=USE_ARREST_COLS):
    """read and write clean arrests data csv
SOURCE: https://data.cityofnewyork.us/api/views/8h9b-rp9u/rows.csv?accessType=DOWNLOAD
ABOUT: https://data.cityofnewyork.us/Public-Safety/NYPD-Arrests-Data-Historic-/8h9b-rp9u
    """
    arrests_df = pd.read_csv(f'{datadir}/NYPD_Arrests_Data__Historic_.csv',
                         parse_dates=['ARREST_DATE'])
    arrests_df = arrests_df.replace({'LAW_CAT_CD': {'V':'VIOLATION', 'M': 'MISDEMEANOR', 'F': 'FELONY'}})
    arrests_df.rename(columns={'ARREST_PRECINCT' : 'precinct'})
    arrests_df[outcols].to_csv(f'data/full_arrests_df.csv', index=False)
    return arrests_df[outcols]

def create_population_df(datadir='../data'):
    """read and write clean population-by-precinct data csv
SOURCE: https://github.com/pinnnnnn/MAP_Spring_2016/blob/master/NYC_Blocks_2010CensusData_Plus_Precincts.csv
ABOUT: https://johnkeefe.net/nyc-police-precinct-and-census-data
    """
    population_df = pd.read_csv(f'{datadir}/NYC_Blocks_2010CensusData_Plus_Precincts.csv',
                                dtype={'precinct' : 'Int64'},
                                usecols=['precinct',
                                         'TRACT',
                                         'BLOCK',
                                         'INTPTLAT',
                                         'INTPTLON',
                                         'P0010001']).dropna()
    population_df = population_df.rename(columns={'P0010001' : 'population',
                                                  'INTPTLAT' : 'Latitude',
                                                  'INTPTLON' : 'Longitude'})
    population_df = population_df.groupby('precinct').agg({'Latitude':'mean',
                                                           'Longitude':'mean',
                                                           'population':'sum'})
    population_df.to_csv(f'data/full_population_df.csv')
    return population_df

# load separate data files
population_df = pd.read_csv('data/population_df.csv', )
complaints_df = pd.read_csv('data/complaints_df.csv')
arrests_df = pd.read_csv('data/arrests_df.csv')
sqf_df = pd.read_csv('data/sqf_df.csv')
# group complaints by year and precinct
complaints_df = complaints_df.groupby(['YEAR', 'ADDR_PCT_CD']).CMPLNTS.sum()
complaints_df = complaints_df.reset_index()
# merge complaints and population data by precinct (assume same population every year)
df = complaints_df.merge(population_df, how = 'outer',
                         left_on = 'ADDR_PCT_CD',
                         right_on = 'precinct',
                         indicator = True,
                         validate = 'many_to_one')
df = df.drop(df.loc[df.POPULATION == 0].index)
df = df.drop(['precinct', '_merge'], axis = 1)
# merge with arrests data by precinct and year
df = df.merge(arrests_df, how = 'outer',
              left_on = ['ADDR_PCT_CD', 'YEAR'],
              right_on = ['ARREST_PRECINCT', 'YEAR'],
              indicator = True,
              validate = 'one_to_one')
df = df.drop(df.loc[df.CMPLNTS.isna()].index)
df = df.drop(['ARREST_PRECINCT', '_merge'], axis = 1)
# merge with stop-and-frisk data by precinct and year
df = df.merge(sqf_df, how = 'outer',
              left_on = ['ADDR_PCT_CD', 'YEAR'],
              right_on = ['STOP_LOCATION_PRECINCT', 'YEAR2'],
              indicator = True,
              validate = 'one_to_one')
df = df.drop(df.loc[df.YEAR.isna()].index)
df = df.drop(['STOP_LOCATION_PRECINCT', 'YEAR2', '_merge'], axis = 1)
# write to file
df.to_csv('data/df.csv', index=False)
