#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:22:12 2019

@author: flatironschol
"""
import pandas as pd
import data_cleaner as dc
import data_modeler as dm

data = dc.concat_dict_of_dfs(dc.load_sqfs())
data = dm.engineer_features(data)
