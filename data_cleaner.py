#!/usr/bin/env python3
"""
@author: climatebrad
"""

import pandas as pd
import numpy as np

def sqf_excel_to_csv(dir, infile, outfile):
    """read in the sqf excel file and output csv file."""
    data = pd.read_excel(f'{dir}/{infile}', na_values='(null)')
    data.to_csv(f'{dir}/{outfile}.csv', index=False)

def load_sqf_03_to_08(dir):
    """Loads sqf data in format dir/<year>.csv into dict of dataframes
    where year in 2003 to 2008"""
    stop_frisks = {}
    for year in range(2003, 2009):
        print(f'Loading {year}...')
        df = pd.read_csv(f'{dir}/{year}.csv',
                         encoding='cp437',
                         na_values=[' ','12311900'],
                         dtype={'repcmd' : str,
                                'revcmd' : str,
                                'stname' : str,
                                'timestop' : str,
                                'pct' : 'int64',
                                'city' : 'category',
                                'sector' : 'category',
                                'post' : 'category',      # ignorable column
                                'dettypcm' : 'category',  # ignorable column
                                'officrid' : 'category',
                                })
        # fix 2006 column names
        df = df.rename(columns={'adrnum' : 'addrnum',
                                'adrpct': 'addrpct',
                                'dettyp_c' : 'dettypcm',
                                'rescod' : 'rescode',
                                'premtyp' : 'premtype',
                                'prenam' : 'premname',
                                'strintr' : 'stinter',
                                'strname' : 'stname',
                                'details_' : 'detailcm'})
        # drop some useless columns
        df = df.drop(columns=['detail1_','linecm','post','dettypecm'], errors='ignore')
        df.pct = df.pct.replace({999: np.nan})
        stop_frisks[year] = df
    return stop_frisks

def load_filespecs(dir, start=2003, end=2017):
    """Loads filespecs from files named '<year> SQF File Spec.xlsx' for years in 2003 to 2017 (inclusive)"""
    return {year : pd.read_excel(f'{dir}/{year} SQF File Spec.xlsx',
                                 header=3) for year in range(start, end + 1)}

def concat_dict_of_dfs(df_dict):
    """when we want to concatenate the years"""
    return pd.concat(df_dict.values(), sort=False, ignore_index=True)
