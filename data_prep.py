#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:22:12 2019

@author: flatironschol
"""
import pandas as pd
# load separate data files
population_df = pd.read_csv('data/population_df.csv')
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
