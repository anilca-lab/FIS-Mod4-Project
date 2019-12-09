#!/usr/bin/env python3
"""
@authors: climatebrad, anilca-lab
"""

import pandas as pd
import numpy as np


NA_VALUES = (' ', '12311900', '*', '**', '(nul' ,'(n', '(', '(nu')
Y_N_COLS = ('arstmade', 'pistol', 'machgun', 'asltweap',
            'riflshot', 'knifcuti', 'othrweap', 'wepfound',
            'cs_lkout', 'cs_objcs', 'cs_casng', 'cs_cloth', 'cs_descr',
            'cs_drgtr', 'cs_furtv', 'cs_vcrim', 'cs_bulge', 'cs_other',
            'sb_outln', 'sb_other', 'sb_hdobj', 'sb_admis',
            'ac_time', 'ac_rept', 'ac_stsnd', 'ac_proxm',
            'ac_assoc', 'ac_evasv', 'ac_incid', 'ac_cgdir', 'ac_inves', 'ac_other',
            'rf_furt', 'rf_bulg', 'rf_vcrim', 'rf_vcact', 'rf_verbl', 'rf_othsw', 'rf_attir', 'rf_knowl',
            'pf_hands', 'pf_wall', 'pf_grnd', 'pf_drwep', 'pf_ptwep', 'pf_baton', 'pf_hcuff',
            'pf_pepsp', 'pf_other', 'radio', 'rf_rfcmp',
            'othpers', 'explnstp', 'offunif', 'frisked', 'searched', 'contrabn', 'adtlrept',
            'sumissue', )

CAT_COLS =  ('city',
             'sector',
             'post',      # ignorable column
             'dettypcm',  
             'officrid',
             'rescode',
             'offverb',
             'offshld',
             'forceuse',
             'sex',
             'race',
             'haircolr',
             'eyecolor',
             'build',
             'typeofid',
             'recstat',
             'inout',
             'trhsloc',
             'addrtyp',
             'month',
             'day')

IGNORE_COLS = ('detail1_', 
               'linecm', 
               'post', 
               'comppct',
               'compyear',
               'state')

UNMATCHED_2017_COLS = ('ISSUING_OFFICER_RANK',
 'SUPERVISING_OFFICER_RANK',
 'JURISDICTION_DESCRIPTION',
 'OFFICER_NOT_EXPLAINED_STOP_DESCRIPTION',
 'SUPERVISING_ACTION_CORRESPONDING_ACTIVITY_LOG_ENTRY_REVIEWED',
 'PHYSICAL_FORCE_CEW_FLAG',
 'PHYSICAL_FORCE_VERBAL_INSTRUCTION_FLAG',
 'SEARCH_BASIS_CONSENT_FLAG',
 'DEMEANOR_OF_PERSON_STOPPED',
 'STOP_LOCATION_PATROL_BORO_NAME',
 'BACKROUND_CIRCUMSTANCES_SUSPECT_KNOWN_TO_CARRY_WEAPON_FLAG',
 'SUSPECTS_ACTIONS_CONCEALED_POSSESSION_WEAPON_FLAG',
 'SUSPECTS_ACTIONS_IDENTIFY_CRIME_PATTERN_FLAG',
 'SEARCH_BASIS_INCIDENTAL_TO_ARREST_FLAG',
 'FIREARM_FLAG',
 'PHYSICAL_FORCE_DRAW_POINT_FIREARM_FLAG',
 'PHYSICAL_FORCE_RESTRAINT_USED_FLAG',
 'STOP_LOCATION_FULL_ADDRESS')

COL_RENAME = {'STOP_FRISK_ID' : 'ser_num',
 'STOP_FRISK_DATE' : 'datestop',
 'STOP_FRISK_TIME' : 'timestop',
 'Stop Frisk Time' : 'timestop',
 'YEAR2' : 'year',
 'MONTH2' : 'month',
 'DAY2' : 'day',
 'RECORD_STATUS_CODE' : 'recstat',
 'ISSUING_OFFICER_COMMAND_CODE' : 'repcmd',
 'SUPERVISING_OFFICER_COMMAND_CODE' : 'revcmd',
 'LOCATION_IN_OUT_CODE' : 'inout',
 'OBSERVED_DURATION_MINUTES' : 'perobs',
 'SUSPECTED_CRIME_DESCRIPTION' : 'crimsusp',
 'STOP_DURATION_MINUTES' : 'perstop',
 'OFFICER_EXPLAINED_STOP_FLAG' : 'explnstp',
 'OTHER_PERSON_STOPPED_FLAG' : 'othpers',
 'SUSPECT_ARRESTED_FLAG' : 'arstmade',
 'SUSPECT_ARREST_OFFENSE' : 'arstoffn',
 'SUMMONS_ISSUED_FLAG' : 'sumissue',
 'SUMMONS_OFFENSE_DESCRIPTION' : 'sumoffen',
 'OFFICER_IN_UNIFORM_FLAG' : 'offunif',
 'ID_CARD_IDENTIFIES_OFFICER_FLAG' : 'officrid',
 'SHIELD_IDENTIFIES_OFFICER_FLAG' : 'offshld',
 'VERBAL_IDENTIFIES_OFFICER_FLAG' : 'offverb',
 'FRISKED_FLAG' : 'frisked',
 'SEARCHED_FLAG' : 'searched',
 'OTHER_CONTRABAND_FLAG' : 'contrabn',
 'KNIFE_CUTTER_FLAG' : 'knifcuti',
 'OTHER_WEAPON_FLAG' : 'othrweap',
 'WEAPON_FOUND_FLAG' : 'wepfound',
 'PHYSICAL_FORCE_HANDCUFF_SUSPECT_FLAG' : 'pf_hcuff',
 'PHYSICAL_FORCE_OC_SPRAY_USED_FLAG' : 'pf_pepsp',
 'PHYSICAL_FORCE_OTHER_FLAG' : 'pf_other',
 'PHYSICAL_FORCE_WEAPON_IMPACT_FLAG' : 'pf_baton',
 'BACKROUND_CIRCUMSTANCES_VIOLENT_CRIME_FLAG' : 'cs_vcrim',
 'SUSPECTS_ACTIONS_CASING_FLAG' : 'cs_casng',
 'SUSPECTS_ACTIONS_DECRIPTION_FLAG' : 'cs_descr',
 'SUSPECTS_ACTIONS_DRUG_TRANSACTIONS_FLAG' : 'cs_drgtr',
 'SUSPECTS_ACTIONS_LOOKOUT_FLAG' : 'cs_lkout',
 'SUSPECTS_ACTIONS_OTHER_FLAG' : 'cs_other',
 'SUSPECTS_ACTIONS_PROXIMITY_TO_SCENE_FLAG' : 'ac_proxm',
 'SEARCH_BASIS_ADMISSION_FLAG' : 'sb_admis',
 'SEARCH_BASIS_HARD_OBJECT_FLAG' : 'sb_hdobj',
 'SEARCH_BASIS_OTHER_FLAG' : 'sb_other',
 'SEARCH_BASIS_OUTLINE_FLAG' : 'sb_outln',
 'DEMEANOR_CODE' : 'dettypcm',
 'SUSPECT_REPORTED_AGE' : 'age',
 'SUSPECT_SEX' : 'sex',
 'SUSPECT_RACE_DESCRIPTION' : 'race',
 'SUSPECT_WEIGHT' : 'weight',
 'SUSPECT_BODY_BUILD_TYPE' : 'build',
 'SUSPECT_EYE_COLOR' : 'eyecolor',
 'SUSPECT_HAIR_COLOR' : 'haircolr',
 'SUSPECT_OTHER_DESCRIPTION' : 'othfeatr',
 'STOP_LOCATION_PRECINCT' : 'pct',
 'STOP_LOCATION_SECTOR_CODE' : 'sector',
 'STOP_LOCATION_APARTMENT' : 'aptnum',
 'STOP_LOCATION_PREMISES_NAME' : 'premname',
 'STOP_LOCATION_STREET_NAME' : 'stname',
 'STOP_LOCATION_X' : 'xcoord',
 'STOP_LOCATION_Y' : 'ycoord',
 'STOP_LOCATION_ZIP_CODE' : 'zip',
 'STOP_LOCATION_BORO_NAME' : 'city',
 'JURISDICTION_CODE' : 'trhsloc'}

# imperfect mapping of build, haircolr, eyecolor for 2017 -> 2016 earlier
REPLACE_DICT = {
    'build' : {'THN' : 'T',
               'MED' : 'M',
               'HEA' : 'H',
               'XXX' : 'Z'},
    'haircolr' : {'BLK' : 'BK',
                  'BRO' : 'BR',
                  'BLD' : 'BA',
                  'XXX' : 'XX',
                  'BLN' : 'BL',
                  'GRY' : 'GY'},
    'eyecolor' : {'BRO' : 'BR',
                'BLK' : 'BK',
                'ZZZ' : 'XX',
                'BLU' : 'BL',
                'HAZ' : 'HA',
                'GRN' : 'GR',
                'GRY' : 'GY',
                'OTH' : 'Z'},
    'sex' : {'MALE' : 'M',
             'FEMALE' : 'F'}
}


def sqf_excel_to_csv(infile, outfile, dirname='../data/stop_frisk'):
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

def y_n_to_1_0(col, yes_value='Y', set_na=True):
    """convert Y/N column to 1/0 column. set_na keeps blanks as NaN, if false sets to 0"""
    out_col = pd.Series(np.where(col.isin([yes_value, '1']), 1, 0), col.index).astype('int8')
    if set_na:
        out_col[col.isna()] = np.NaN
    return out_col



def y_n_to_1_0_cols(data, cols=Y_N_COLS, yes_value='Y', set_na=True):
    """convert Y/N columns to 1/0 columns. set_na keeps blanks as NaN, if false sets to 0"""
    for y_n_col in Y_N_COLS:
        if y_n_col in data:
            data[y_n_col] = y_n_to_1_0(data[y_n_col], yes_value, set_na)

def height_to_feet_inch(data, height_col):
    """Convert the height_col column to ht_feet, ht_inch
    'SUSPECT_HEIGHT' : '{ht_feet}.{ht_inch}'"""
    # note there are some spurious entries in the SUSPECT_HEIGHT column
    data[['ht_feet', 'ht_inch']] = data[height_col].str.split('.', 1, expand=True)
    # sometimes SUSPECT_HEIGHT is just '5' should go to '5', '0'
    data.loc[data.ht_inch.isna() & data.ht_feet.notna(), 'ht_inch'] = 0
    # convert to int
    data.ht_feet = data.ht_feet.apply(pd.to_numeric).astype('Int64')
    data.ht_inch = data.ht_inch.apply(pd.to_numeric).astype('Int64')
    # deal with junk entries
    data.loc[(data.ht_feet < 3) | (data.ht_feet > 7), ['ht_feet', 'ht_inch']] = np.nan
    data.loc[(data.ht_inch > 11), 'ht_inch'] = 0
    data = data.drop(columns=height_col)
    return data

def convert_17_18_data(data):
    """Convert the 2017-2018 data into the 2003-2016 standard
we can convert these:
'STOP_WAS_INITIATED' : { 'Based on Radio Run' :'radio', 'Based on C/W on Scene' : 'ac_rept'}
'JURISDICTION_CODE' : (if 'A' : NaN else 'trhsloc'),

these we'd have to consider adding to the other years as combined columns:
'FIREARM_FLAG' : 'pistol' | 'riflshot' | 'asltweap' | 'machgun',
'PHYSICAL_FORCE_DRAW_POINT_FIREARM_FLAG' : 'pf_ptwep' | 'pf_drwep',
'PHYSICAL_FORCE_RESTRAINT_USED_FLAG' : 'pf_hands' | 'pf_wall' | 'pf_grnd',
'STOP_LOCATION_FULL_ADDRESS' : 'addrnum' + 'stname' + 'stinter' + 'crossst'
    """
    data = data.copy().rename(columns=COL_RENAME)
    
    # convert STOP_WAS_INITIATED
    data['radio'] = data.STOP_WAS_INITIATED.map(lambda x: 'Y' if x=='Based on Radio Run' else 'N')
    data['ac_rept'] = data.STOP_WAS_INITIATED.map(lambda x: 'Y' if x=='Based on C/W on Scene' else 'N')
    data = data.drop(columns='STOP_WAS_INITIATED')
    
    # convert JURISDICTION CODE
    data.trhsloc = data.trhsloc.map(lambda x: np.NaN if x=='A' else x)
    
    data = height_to_feet_inch(data, 'SUSPECT_HEIGHT')
    
    data = data.replace(REPLACE_DICT)
    data = data.drop(columns=list(UNMATCHED_2017_COLS))
    
    # this should be in the add_datetimestop function
    data['datetimestop'] = pd.to_datetime(data.datestop \
                                          + ' ' + data.timestop,
                                          errors='coerce')
    data = data.drop(columns=['datestop', 'timestop'])
    
    # fix column datatypes
    dtypes = get_dtypes()
    dtypes = {key : dtypes.get(key) for key in data.columns if dtypes.get(key)}
    data = data.astype(dtypes, errors='ignore')
    
    return data

def load_full_sqf(dirname='../data/stop_frisk'):
    """Load the cleaned 2003-2018 dataframe"""
    return pd.read_pickle(f'{dirname}/stop_frisks.pkl')

def get_dtypes(on_input=True):
    """Return full dict of dtypes, for on_input or output."""
    dtypes = {'repcmd' : str,
              'revcmd' : str,
              'stname' : str,
              'datestop' : str,
              'timestop' : str,
              'sumoffen' : str,
              'addrnum' : str,
              'othfeatr' : str,
              'recstat' : str,
              'pct' : 'Int64',
              'ht_feet' : 'Int64',
              'ht_inch' : 'Int64',
              'beat' : 'Int64',
              'addrpct' : 'Int64',
              'year' : 'Int64'
              }
    for col in Y_N_COLS:
        if on_input:
            dtypes.update({col : 'category'})
        else:
            dtypes.update({col : 'int8'})
    for col in CAT_COLS:
        dtypes.update({col : 'category'})
    if not on_input:
        for key in IGNORE_COLS + ('datestop', 'timestop'):
            if key in dtypes:
                dtypes.pop(key)
                
    return dtypes
        
def load_sqf(year, dirname='../data/stop_frisk', convert=True):
    """Load and clean sqf csv file by year. 
    convert=True if 2017, 2018 should be converted to pre-2017 format."""
    print(f'Loading {year}...')
    # '*' is a na_value for the beat variable
    # '12311900' is a na_value for DOB
    
    if year in (2017, 2018):
        data = pd.read_csv(f'{dirname}/{year}.csv',
                           encoding='cp437',
                           dtype = {'SUSPECT_HEIGHT' : str,
                                    'PHYSICAL_FORCE_OC_SPRAY_USED_FLAG' : 'str',
                                    'PHYSICAL_FORCE_WEAPON_IMPACT_FLAG' : 'str'},
                           na_values=NA_VALUES,
                           usecols = lambda x : x not in IGNORE_COLS
                          )
        if convert:
            data = convert_17_18_data(data)
    else:      
        data = pd.read_csv(f'{dirname}/{year}.csv',
                           encoding='cp437',
                           na_values=NA_VALUES,
                           dtype=get_dtypes())
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
        # 999 is a na_value for the precinct variable
        data = add_datetimestop(data)
    if convert or year < 2017: 
        data.pct = data.pct.replace({999: np.nan, 208760: np.nan})
        data.columns = data.columns.str.lower()
        data = data.dropna(subset=['pct'])
        
        # convert yes-no columns to 1-0
        y_n_to_1_0_cols(data)
    return data

def load_sqfs(start=2003, end=2018, dirname='../data/stop_frisk'):
    """Loads sqf data in format dir/<year>.csv into dict of dataframes
    Currently works for years in 2003 to 2016"""
    stop_frisks = {}
    for year in range(start, end + 1):
        stop_frisks[year] = load_sqf(year, dirname)
    print("Done.")
    return stop_frisks

def add_datetimestop(data):
    """Concatenate date and time fields into a datetime field. Edits dataframe in place"""
    data['datetimestop'] = pd.to_datetime(data.datestop.str.zfill(8) \
                                          + data.timestop.apply(format_time),
                                          format='%m%d%Y%H:%M',
                                          errors='coerce')
    data = data.drop(columns=['datestop', 'timestop'])
    return data

def add_datetimestops(data_dict):
    """update the dataframes in a data_dict with datetimestop field."""
    for year in data_dict:
        print(f'Processing {year}...')
        add_datetimestop(data_dict[year])
    print('Done.')

def load_filespecs(start=2003, end=2017, dirname='../data/stop_frisk/filespecs'):
    """Loads filespecs from files named '<year> SQF File Spec.xlsx'
    for years in 2003 to 2017 (inclusive)"""
    return {year : pd.read_excel(f'{dirname}/{year} SQF File Spec.xlsx',
                                 header=3) for year in range(start, end + 1)}

def add_all_columns(data):
    """Make sure dataframe data has all the possible columns with the correct datatypes."""
    dtypes = get_dtypes(on_input=False)
    newcols = { col : dtype for col, dtype in dtypes.items() if col not in data}
    newcols = { col : np.NaN for col in newcols}
    data = data.assign(**newcols)
    data = data.fillna({col : 0 for col in Y_N_COLS})
    data = data.astype(dtypes)
    return data
    
def concat_dict_of_dfs(df_dict):
    """when we want to concatenate the years"""
    # we should probably be using merge instead of concat, which is better at handling categorical columns
    df_dict = {year : add_all_columns(data) for year, data in df_dict.items()}
    data = pd.concat(df_dict.values(), sort=False, ignore_index=True)
    dtypes = get_dtypes(on_input=False)
    data = data.astype(dtypes)
    return data


def clean_and_save_full_sqfs(indirname='../data/stop_frisk', outdirname='../data'):
    """Create and save full stop-and-frisks data from raw files"""
    data = concat_dict_of_dfs(load_sqfs(dirname=indirname))
    data.to_pickle(f'{outdirname}/full_stop_frisks_df.pkl')
    return data
