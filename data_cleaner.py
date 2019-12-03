#!/usr/bin/env python3
"""
@author: climatebrad
"""

import pandas as pd
import numpy as np


NA_VALUES = [' ', '12311900', '*', '**']
Y_N_COLS = ('arstmade', 'pistol', 'machgun', 'asltweap', 'riflshot', 'knifcuti', 'othrweap', 'wepfound')
"""
COL_RENAME = {'STOP_FRISK_ID',
 'STOP_FRISK_DATE' : 'datestop',
 'STOP_FRISK_TIME' : 'timestop',
 'YEAR2' : 'year',
 'MONTH2' : 'month',
 'DAY2' : 'day',
 'STOP_WAS_INITIATED',
 'RECORD_STATUS_CODE',
 'ISSUING_OFFICER_RANK',
 'ISSUING_OFFICER_COMMAND_CODE',
 'SUPERVISING_OFFICER_RANK',
 'SUPERVISING_OFFICER_COMMAND_CODE',
 'SUPERVISING_ACTION_CORRESPONDING_ACTIVITY_LOG_ENTRY_REVIEWED',
 'LOCATION_IN_OUT_CODE' : 'inout',
 'JURISDICTION_CODE',
 'JURISDICTION_DESCRIPTION',
 'OBSERVED_DURATION_MINUTES',
 'SUSPECTED_CRIME_DESCRIPTION',
 'STOP_DURATION_MINUTES',
 'OFFICER_EXPLAINED_STOP_FLAG',
 'OFFICER_NOT_EXPLAINED_STOP_DESCRIPTION',
 'OTHER_PERSON_STOPPED_FLAG',
 'SUSPECT_ARRESTED_FLAG',
 'SUSPECT_ARREST_OFFENSE',
 'SUMMONS_ISSUED_FLAG',
 'SUMMONS_OFFENSE_DESCRIPTION',
 'OFFICER_IN_UNIFORM_FLAG',
 'ID_CARD_IDENTIFIES_OFFICER_FLAG',
 'SHIELD_IDENTIFIES_OFFICER_FLAG',
 'VERBAL_IDENTIFIES_OFFICER_FLAG',
 'FRISKED_FLAG',
 'SEARCHED_FLAG',
 'OTHER_CONTRABAND_FLAG',
 'FIREARM_FLAG',
 'KNIFE_CUTTER_FLAG',
 'OTHER_WEAPON_FLAG',
 'WEAPON_FOUND_FLAG',
 'PHYSICAL_FORCE_CEW_FLAG',
 'PHYSICAL_FORCE_DRAW_POINT_FIREARM_FLAG',
 'PHYSICAL_FORCE_HANDCUFF_SUSPECT_FLAG',
 'PHYSICAL_FORCE_OC_SPRAY_USED_FLAG',
 'PHYSICAL_FORCE_OTHER_FLAG',
 'PHYSICAL_FORCE_RESTRAINT_USED_FLAG',
 'PHYSICAL_FORCE_VERBAL_INSTRUCTION_FLAG',
 'PHYSICAL_FORCE_WEAPON_IMPACT_FLAG',
 'BACKROUND_CIRCUMSTANCES_VIOLENT_CRIME_FLAG',
 'BACKROUND_CIRCUMSTANCES_SUSPECT_KNOWN_TO_CARRY_WEAPON_FLAG',
 'SUSPECTS_ACTIONS_CASING_FLAG',
 'SUSPECTS_ACTIONS_CONCEALED_POSSESSION_WEAPON_FLAG',
 'SUSPECTS_ACTIONS_DECRIPTION_FLAG',
 'SUSPECTS_ACTIONS_DRUG_TRANSACTIONS_FLAG',
 'SUSPECTS_ACTIONS_IDENTIFY_CRIME_PATTERN_FLAG',
 'SUSPECTS_ACTIONS_LOOKOUT_FLAG',
 'SUSPECTS_ACTIONS_OTHER_FLAG',
 'SUSPECTS_ACTIONS_PROXIMITY_TO_SCENE_FLAG',
 'SEARCH_BASIS_ADMISSION_FLAG',
 'SEARCH_BASIS_CONSENT_FLAG',
 'SEARCH_BASIS_HARD_OBJECT_FLAG',
 'SEARCH_BASIS_INCIDENTAL_TO_ARREST_FLAG',
 'SEARCH_BASIS_OTHER_FLAG',
 'SEARCH_BASIS_OUTLINE_FLAG',
 'DEMEANOR_CODE',
 'DEMEANOR_OF_PERSON_STOPPED',
 'SUSPECT_REPORTED_AGE',
 'SUSPECT_SEX',
 'SUSPECT_RACE_DESCRIPTION',
 'SUSPECT_HEIGHT',
 'SUSPECT_WEIGHT',
 'SUSPECT_BODY_BUILD_TYPE',
 'SUSPECT_EYE_COLOR',
 'SUSPECT_HAIR_COLOR',
 'SUSPECT_OTHER_DESCRIPTION',
 'STOP_LOCATION_PRECINCT',
 'STOP_LOCATION_SECTOR_CODE',
 'STOP_LOCATION_APARTMENT',
 'STOP_LOCATION_FULL_ADDRESS',
 'STOP_LOCATION_PREMISES_NAME',
 'STOP_LOCATION_STREET_NAME',
 'STOP_LOCATION_X' : 'xcoord',
 'STOP_LOCATION_Y' : 'ycoord',
 'STOP_LOCATION_ZIP_CODE' : 'zip',
 'STOP_LOCATION_PATROL_BORO_NAME',
 'STOP_LOCATION_BORO_NAME']

 'year',
 'pct',
 'ser_num',
 'datestop',
 'timestop',
 'recstat',
 'inout',
 'trhsloc',
 'perobs',
 'crimsusp',
 'perstop',
 'typeofid',
 'explnstp',
 'othpers',
 'arstmade',
 'arstoffn',
 'sumissue',
 'sumoffen',
 'compyear',
 'comppct',
 'offunif',
 'officrid',
 'frisked',
 'searched',
 'contrabn',
 'adtlrept',
 'pistol',
 'riflshot',
 'asltweap',
 'knifcuti',
 'machgun',
 'othrweap',
 'pf_hands',
 'pf_wall',
 'pf_grnd',
 'pf_drwep',
 'pf_ptwep',
 'pf_baton',
 'pf_hcuff',
 'pf_pepsp',
 'pf_other',
 'radio',
 'ac_rept',
 'ac_inves',
 'rf_vcrim',
 'rf_othsw',
 'ac_proxm',
 'rf_attir',
 'cs_objcs',
 'cs_descr',
 'cs_casng',
 'cs_lkout',
 'rf_vcact',
 'cs_cloth',
 'cs_drgtr',
 'ac_evasv',
 'ac_assoc',
 'cs_furtv',
 'rf_rfcmp',
 'ac_cgdir',
 'rf_verbl',
 'cs_vcrim',
 'cs_bulge',
 'cs_other',
 'ac_incid',
 'ac_time',
 'rf_knowl',
 'ac_stsnd',
 'ac_other',
 'sb_hdobj',
 'sb_outln',
 'sb_admis',
 'sb_other',
 'repcmd',
 'revcmd',
 'rf_furt',
 'rf_bulg',
 'offverb',
 'offshld',
 'forceuse',
 'sex',
 'race',
 'dob',
 'age',
 'ht_feet',
 'ht_inch',
 'weight',
 'haircolr',
 'eyecolor',
 'build',
 'othfeatr',
 'addrtyp',
 'rescode',
 'premtype',
 'premname',
 'addrnum',
 'stname',
 'stinter',
 'crossst',
 'aptnum',
 'city',
 'state',
 'zip',
 'addrpct',
 'sector',
 'beat',
 'xcoord',
 'ycoord',
 'dettypCM',
 'lineCM',
 'detailCM']
"""

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

def y_n_to_1_0(col, yes_value='Y'):
    """convert Y/N column to 1/0 column"""
    out_col = pd.Series(np.where(col.isin(yes_value, '1'), 1, 0), col.index)
    out_col[col.isna()] = np.NaN
    return out_col

def y_n_to_1_0_cols(data, cols=Y_N_COLS, yes_value='Y'):
    """convert Y/N columns to 1/0 columns"""
    for y_n_col in Y_N_COLS:
        if y_n_col in data:
            data[y_n_col] = y_n_to_1_0(data[y_n_col])

def load_sqf(dirname, year):
    """Load and clean sqf csv file by year."""
    print(f'Loading {year}...')
    # '*' is a na_value for the beat variable
    # '12311900' is a na_value for DOB
    data = pd.read_csv(f'{dirname}/{year}.csv',
                       encoding='cp437',
                       na_values=NA_VALUES,
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
    # convert yes-no columns to 1-0
    y_n_to_1_0_cols(data)
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
    """Concatenate date and time fields into a datetime field. Edits dataframe in place"""
    data['datetimestop'] = pd.to_datetime(data.datestop.str.zfill(8) \
                                          + data.timestop.apply(format_time),
                                          format='%m%d%Y%H:%M',
                                          errors='coerce')

def add_datetimestops(data_dict):
    """update the dataframes in a data_dict with datetimestop field."""
    for year in data_dict:
        print(f'Processing {year}...')
        add_datetimestop(data_dict[year])
    print('Done.')

def load_filespecs(dirname, start=2003, end=2017):
    """Loads filespecs from files named '<year> SQF File Spec.xlsx'
    for years in 2003 to 2017 (inclusive)"""
    return {year : pd.read_excel(f'{dirname}/{year} SQF File Spec.xlsx',
                                 header=3) for year in range(start, end + 1)}

def concat_dict_of_dfs(df_dict):
    """when we want to concatenate the years"""
    return pd.concat(df_dict.values(), sort=False, ignore_index=True)
