#!/usr/bin/env python3
"""
@author: climatebrad
"""

import pandas as pd
import numpy as np

def sqf_excel_to_csv(dirname, infile, outfile):
    """read in the sqf excel file and output csv file."""
    data = pd.read_excel(f'{dir}/{infile}', na_values='(null)')
    data.to_csv(f'{dirname}/{outfile}.csv', index=False)

def format_time(t_str):
    """make sure timestops have colon between hour and minute"""
    if t_str == t_str: # skip NaN
        t_str = t_str.zfill(4)
        if t_str[2] != ':':
            return t_str[:2] + ':' + t_str[2:]
        return t_str
    return t_str

def load_sqf(dirname, year):
    """Load and clean sqf csv file by year."""
    print(f'Loading {year}...')
    # '*' is a na_value for the beat variable
    # '12311900' is a na_value for DOB
    data = pd.read_csv(f'{dirname}/{year}.csv',
                       encoding='cp437',
                       na_values=[' ', '12311900', '*', '**'],
                       dtype={'repcmd' : str,
                              'revcmd' : str,
                              'stname' : str,
                              'datestop' : str,
                              'timestop' : str,
                              'sumoffen' : str,
                              'addrnum' : str,
                              'othfeatr' : str,
                              'recstat' : str,
                              'pct' : 'Int64',
                              'city' : 'category',
                              'sector' : 'category',
                              'post' : 'category',      # ignorable column
                              'dettypcm' : 'category',  # ignorable column
                              'officrid' : 'category',
                              })
    # fix 2006 column names
    data = data.rename(columns={'adrnum' : 'addrnum',
                                'adrpct': 'addrpct',
                                'dettyp_c' : 'dettypcm',
                                'rescod' : 'rescode',
                                'premtyp' : 'premtype',
                                'prenam' : 'premname',
                                'strintr' : 'stinter',
                                'strname' : 'stname',
                                'details_' : 'detailcm'})
    # drop some useless columns
    data = data.drop(columns=['detail1_', 'linecm', 'post', 'dettypecm'], errors='ignore')
    # 999 is a na_value for the precinct variable
    data.pct = data.pct.replace({999: np.nan})
    return data

def load_sqfs(dirname, start=2003, end=2008):
    """Loads sqf data in format dir/<year>.csv into dict of dataframes
    Currently works for years in 2003 to 2011"""
    stop_frisks = {}
    for year in range(start, end + 1):
        stop_frisks[year] = load_sqf(dirname, year)
    print("Done.")
    return stop_frisks

def add_datetimestop(data):
    """Concatenate date and time fields into a datetime field."""
    data['datetimestop'] = pd.to_datetime(data.datestop.str.zfill(8) \
                                          + data.timestop.apply(format_time),
                                          format='%m%d%Y%H:%M',
                                          errors='coerce')
    return data

def add_datetimestops(data_dict):
    """update the dataframes in a data_dict with datetimestop field"""
    for year in data_dict:
        data_dict[year] = add_datetimestop(data_dict[year])

def load_filespecs(dirname, start=2003, end=2017):
    """Loads filespecs from files named '<year> SQF File Spec.xlsx'
    for years in 2003 to 2017 (inclusive)"""
    return {year : pd.read_excel(f'{dirname}/{year} SQF File Spec.xlsx',
                                 header=3) for year in range(start, end + 1)}

def concat_dict_of_dfs(df_dict):
    """when we want to concatenate the years"""
    return pd.concat(df_dict.values(), sort=False, ignore_index=True)
