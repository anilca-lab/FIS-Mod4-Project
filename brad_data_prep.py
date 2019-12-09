#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: climatebrad, anilca-lab
"""
import numpy as np
import pandas as pd

COMPLAINTS_PARAMS = {
    'infilename' : 'NYPD_Complaint_Data_Historic.csv',
    'outfilename' : 'full_complaints_df',
    'read_csv_params'  : {    
        'usecols' : ['CMPLNT_NUM', 'ADDR_PCT_CD', 'RPT_DT', 'KY_CD', 'PD_CD',
                      'LAW_CAT_CD',
                      'SUSP_AGE_GROUP', 'SUSP_RACE', 'SUSP_SEX', 
                      'VIC_AGE_GROUP', 'VIC_RACE', 'VIC_SEX',
                      'Latitude', 'Longitude'],
        'dtype' : {'CMPLNT_NUM' : 'Int64',
                    'ADDR_PCT_CD' : 'category',
                    'KY_CD' : 'category',
                    'PD_CD' : 'category',
                    'LAW_CAT_CD' : 'category',
                    'SUSP_RACE' : 'category',
                    'SUSP_SEX' : 'category',
                    'SUSP_AGE_GROUP' : 'category',
                    'VIC_AGE_GROUP' : 'category',
                    'VIC_RACE' : 'category',
                    'VIC_SEX' : 'category'
                  },
        'na_values' : ['  "error" : true',
                       '  "message" : "Internal error"',
                       '  "status" : 500',
                       '}'],
        'parse_dates' : ['RPT_DT']
    },
    'drop_na_cols' : ['CMPLNT_NUM', 'RPT_DT', 'ADDR_PCT_CD', 'KY_CD', 'LAW_CAT_CD'],
    'rename_cols' : {
        'ADDR_PCT_CD' : 'pct',
        'RPT_DT' : 'date'
    },
    'set_cats' : {
        'VIC_AGE_GROUP' : ['25-44', '45-64', '18-24', 'UNKNOWN', '<18', '65+'],
        'SUSP_AGE_GROUP' : ['25-44', '45-64', '18-24', 'UNKNOWN', '<18', '65+']
    }
}

ARRESTS_PARAMS = {
    'infilename' : 'NYPD_Arrests_Data__Historic_.csv',
    'outfilename' : 'full_arrests_df',
    'read_csv_params' : {
        'usecols' : [
            'ARREST_PRECINCT', 'ARREST_DATE',
            'KY_CD', 'LAW_CAT_CD', 'AGE_GROUP',
            'PERP_RACE', 'PERP_SEX', 'Latitude', 'Longitude'],
        'dtype' : {
            'ARREST_PRECINCT' : 'category',
            'KY_CD' : 'category',
            'LAW_CAT_CD' : 'category',
            'AGE_GROUP' : 'category',
            'PERP_RACE' : 'category',
            'PERP_SEX' : 'category'
        },
        'na_values' : [],
        'parse_dates' : ['ARREST_DATE']
    },
    'drop_na_cols' : ['ARREST_PRECINCT', 'ARREST_DATE'],
    'rename_cols' : {
        'ARREST_PRECINCT' : 'pct',
        'ARREST_DATE' : 'date'},
    'replace_cols' : {
        'LAW_CAT_CD': {
            'V' : 'VIOLATION',
            'M' : 'MISDEMEANOR', 
            'F' : 'FELONY'}},
    'set_cats' : {
        'LAW_CAT_CD' : ['VIOLATION', 'MISDEMEANOR', 'FELONY'],
        'AGE_GROUP' : ['25-44', '45-64', '18-24', 'UNKNOWN', '<18', '65+'],
    },

}
    
def create_df_from_csv(datadir, infilename, outfilename, read_csv_params, **params):
    """
    loads and processes dataframe from csv, saves dataframe to outfilename.
required:
datadir : directory for reading in raw csv and outputting processed csv
infilename : filename of input csv
outfilename : filename of output csv
read_csv_params : dict of parameters to pass to pd.read_csv 
  highly recommended: na_values, parse_dates, usecols, dtype

named keyword arguments:
drop_na_cols : list of cols for which to drop rows if those cols are NaN
rename_cols : dict of cols to rename before output
replace_cols : dict to pass to df.replace()
filter_cats : dict of category-type cols -
  key is colname, value is list of valid values for that category
  all non-valid values are replaced with np.NaN
"""
    df = pd.read_csv(f'{datadir}/{infilename}', **read_csv_params )
    if params.get('drop_na_cols'):
        df = df.dropna(subset=params['drop_na_cols'])
    if params.get('rename_cols'):
        df = df.rename(columns=params['rename_cols'])
    if params.get('replace_cols'):
        df = df.replace(params['replace_cols'])
    for set_cat, valids in params.get('set_cats', {}).items():
        df.loc[~df[set_cat].isin(valids), set_cat] = np.NaN
        # recalculate the category list
        df[set_cat] = df[set_cat].astype('object').astype('category')
    df.to_csv(f'{datadir}/{outfilename}.csv', index=False)
    df.to_pickle(f'{datadir}/{outfilename}.pkl')
    return df
    
def create_complaints_df(datadir='../data', params=COMPLAINTS_PARAMS):
    """read and write clean complaint data csv
SOURCE: https://data.cityofnewyork.us/api/views/qgea-i56i/rows.csv?accessType=DOWNLOAD
ABOUT: https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Historic/qgea-i56i

RPT_DT = report date (we don't have as comprehensive coverage of CMPLNT_FR_DT)
ADDR_PCT_CD = precinct
KY_CD = offense id

we should do better management of datatypes.
    """
    params = params.copy()
    complaints_df = create_df_from_csv(datadir, 
                                       params.pop('infilename'), 
                                       params.pop('outfilename'),
                                       params.pop('read_csv_params'),
                                       **params
                                      )
    return complaints_df

def create_arrests_df(datadir='../data', params=ARRESTS_PARAMS):
    """read and write clean arrests data csv
SOURCE: https://data.cityofnewyork.us/api/views/8h9b-rp9u/rows.csv?accessType=DOWNLOAD
ABOUT: https://data.cityofnewyork.us/Public-Safety/NYPD-Arrests-Data-Historic-/8h9b-rp9u
    """
    params = params.copy()
    arrests_df = create_df_from_csv(datadir, 
                                       params.pop('infilename'), 
                                       params.pop('outfilename'),
                                       params.pop('read_csv_params'),
                                       **params
                                      )
    return arrests_df

# TODO: use params to load data df properly
def load_data_df(filename, datadir='data', parse_dates=['date']):
    """load dataframe from file named full_{filename}_df.csv"""
    return pd.read_csv(f'{datadir}/full_{filename}_df.csv',
                       parse_dates=parse_dates)

def load_population_df(datadir='data'):
    """load full_population_df.csv into df"""
    return load_data_df('population', datadir, parse_dates=False)

def load_data_df_from_pickle(filename, datadir='../data'):
    """load dataframe name full_{filename}_df.pkl from pickle"""
    return pd.read_pickle(f'{datadir}/full_{filename}_df.pkl')

def load_complaints_df(datadir='../data'):
    """load complaints data from the pickle"""
    return load_data_df_from_pickle('complaints', datadir)

def load_arrests_df(datadir='../data'):
    """load arrests data from the pickle"""
    return load_data_df_from_pickle('arrests', datadir)

def load_stop_frisks_df(datadir='../data/stop_frisk'):
    return load_data_df_from_pickle('stop_frisks', datadir)

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
                                                           'population':'sum'}).reset_index()
    population_df = population_df.rename(columns={'precinct' : 'pct'})
    population_df.to_csv(f'data/full_population_df.csv', index=False)
    return population_df

def aggregate_stop_frisks(stop_frisks):
    """Return stops and stop-arrest count by year and precinct."""
    data = stop_frisks[['year', 'pct', 'arstmade']].groupby(['year', 'pct']) \
                                                   .agg({'arstmade' : ['count','sum']}) \
                                                   .reset_index()
    data.columns = ['year','pct','stops','stop_arrests']
    data = data.astype({'stop_arrests' : 'int64'})
    return data

def count_by_year_and_pct(data, dataname):
    """Return count of rows by year and precinct (pct)."""
    return data.groupby([
                         data.date.dt.year, 
                         'pct'
                        ]).size().reset_index(name=dataname).rename(columns={'date' : 'year'})

def aggregate_arrests(arrests):
    """Return arrest count by year and precinct."""
    return count_by_year_and_pct(arrests, 'arrests')

def aggregate_complaints(complaints):
    """Return reported crime count by year and precinct."""
    return count_by_year_and_pct(complaints, 'crimes')



# TODO: concatenate results into one df
def aggregate_data(stop_frisks, arrests, complaints, population):
    """create aggregate df"""
    stop_ct = aggregate_stop_frisks(stop_frisks)
    arrest_ct = aggregate_arrests(arrests)
    crime_ct = aggregate_complaints(complaints)
    return stop_ct.merge(arrest_ct.astype({'year' : 'int64', 'pct' : 'int64'}), 
                       on=['year', 'pct'], how='inner') \
                 .merge(crime_ct.astype({'year' : 'int64', 'pct' : 'int64'}), 
                       on=['year', 'pct'], how='inner') \
                 .merge(population.astype({'pct' : 'int64'}),
                       on=['pct'], how='inner')

def load_and_aggregate_data():
    """One-line function to load and aggregate data."""
    data = aggregate_data(load_stop_frisks_df(),
                          load_arrests_df(),
                          load_complaints_df(),
                          load_population_df())
    data.to_csv(f'data/full_df.csv', index=False)
    return data