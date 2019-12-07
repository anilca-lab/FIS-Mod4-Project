#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: climatebrad, anilca-lab
"""
import pandas as pd

USE_COMPLAINT_COLS = ['date','pct','KY_CD',
                      'LAW_CAT_CD','SUSP_AGE_GROUP',
                      'SUSP_RACE', 'SUSP_SEX', 'Latitude', 'Longitude']

USE_ARREST_COLS = ['date', 'pct',
                   'KY_CD','LAW_CAT_CD','AGE_GROUP',
                   'PERP_RACE', 'PERP_SEX', 'Latitude', 'Longitude']

def create_complaints_df(datadir='../data', outcols=USE_COMPLAINT_COLS):
    """read and write clean complaint data csv
SOURCE: https://data.cityofnewyork.us/api/views/qgea-i56i/rows.csv?accessType=DOWNLOAD
ABOUT: https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Historic/qgea-i56i

RPT_DT = report date (we don't have as comprehensive coverage of CMPLNT_FR_DT)
ADDR_PCT_CD = precinct
KY_CD = offense id

we should do better management of datatypes
    """
    complaints_df = pd.read_csv(f'{datadir}/NYPD_Complaint_Data_Historic.csv',
                                dtype={'CMPLNT_NUM' : 'Int64',
                                       'ADDR_PCT_CD' : 'Int64',
                                       'LAW_CAT_CD' : 'category',
                                       'SUSP_RACE' : 'category',
                                       'SUSP_SEX' : 'category',
                                       'SUSP_AGE_GROUP' : 'category',
                                       'PARKS_NM' : 'str',
                                       'HOUSING_PSA' : 'str'},
                                na_values=['  "error" : true',
                                           '  "message" : "Internal error"',
                                           '  "status" : 500',
                                           '}'],
                            parse_dates=['RPT_DT'])
    complaints_df = complaints_df.dropna(subset = ['CMPLNT_NUM', 'RPT_DT', 'ADDR_PCT_CD', 'KY_CD', 'LAW_CAT_CD'])
    complaints_df = complaints_df.rename(columns={'ADDR_PCT_CD' : 'pct',
                                                  'RPT_DT' : 'date'})
    complaints_df[outcols].to_csv(f'data/full_complaints_df.csv', index=False)
    return complaints_df[outcols]

def create_arrests_df(datadir='../data', outcols=USE_ARREST_COLS):
    """read and write clean arrests data csv
SOURCE: https://data.cityofnewyork.us/api/views/8h9b-rp9u/rows.csv?accessType=DOWNLOAD
ABOUT: https://data.cityofnewyork.us/Public-Safety/NYPD-Arrests-Data-Historic-/8h9b-rp9u
    """
    arrests_df = pd.read_csv(f'{datadir}/NYPD_Arrests_Data__Historic_.csv',
                         parse_dates=['ARREST_DATE'])
    arrests_df = arrests_df.replace({'LAW_CAT_CD': {'V':'VIOLATION',
                                                    'M': 'MISDEMEANOR', 
                                                    'F': 'FELONY'}})
    arrests_df = arrests_df.rename(columns={'ARREST_PRECINCT' : 'pct',
                                           'ARREST_DATE' : 'date'})
    arrests_df[outcols].to_csv(f'data/full_arrests_df.csv', index=False)
    return arrests_df[outcols]

def load_data_df(filename, datadir='data'):
    """load dataframe from file"""
    return pd.read_csv(f'{datadir}/full_{filename}_df.csv',
                       parse_dates=['date'])

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
    population_df = population_df.rename(columns={'precinct' : 'pct'})
    population_df.to_csv(f'data/full_population_df.csv', index=False)
    return population_df

def aggregate_stop_frisks(stop_frisks):
    data = stop_frisks[['year', 'pct', 'arstmade']].groupby(['year', 'pct']) \
                                                   .agg({'arstmade' : ['count','sum']}) \
                                                   .reset_index()
    data.columns = ['year','pct','stops','stop_arrests']
    return data

def aggregate_arrests(arrests):
    pass

def aggregate_complaints(complaints):
    pass

def aggregate_data(stop_frisks, arrests, complaints, population):
    """create aggregate df"""
    stop_frisks = stop_frisks[['year','pct']].groupby(by=['year','pct'])