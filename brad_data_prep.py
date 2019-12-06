#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: climatebrad
"""
import data_cleaner as dc
import data_modeler as dm

data = dc.concat_dict_of_dfs(dc.load_sqfs())
data = dm.engineer_features(data)
data.to_csv('data/df.csv')