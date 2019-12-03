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

def create_complaint_df(datadir, outcols=USE_COMPLAINT_COLS):
    """read and write clean complaint data csv"""
    complaints_df = pd.read_csv(f'{datadir}/NYPD_Complaint_Data_Historic.csv', dtype={'CMPLNT_NUM' : 'Int64'},
                            na_values=['  "error" : true',
                                       '  "message" : "Internal error"',
                                       '  "status" : 500',
                                       '}'],
                            parse_dates=['RPT_DT'])
    complaints_df = complaints_df.dropna(subset = ['CMPLNT_NUM', 'RPT_DT', 'ADDR_PCT_CD', 'KY_CD', 'LAW_CAT_CD'])

    complaints_df[outcols].to_csv(f'data/full_complaints_df.csv', index=False)
    return complaints_df[outcols]

def create_arrests_df(datadir, outcols=USE_ARREST_COLS):
    """read and write clean arrests data csv"""
    arrests_df = pd.read_csv('../data/NYPD_Arrests_Data__Historic_.csv',
                         parse_dates=['ARREST_DATE'])
    arrests_df = arrests_df.replace({'LAW_CAT_CD': {'V':'VIOLATION', 'M': 'MISDEMEANOR', 'F': 'FELONY'}})

    arrests_df[outcols].to_csv(f'data/full_arrests_df.csv', index=False)
    return arrests_df[outcols]


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
