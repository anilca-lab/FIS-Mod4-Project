#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:22:12 2019
The following is a part of the FIS Mod4 Project and provides
data visualizations to provide the context to our aim to examine 
the relationship between stop-question-frisk
and policy effectiveness using data from the NYPD. They also
explore the data.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import data_modeler as dm
import matplotlib.ticker

sns.set_context("talk")
sns.set_style("white")

# Crime rate over time
population_list = [8.0233, 7.9844, 7.9396, 7.9043, 7.9087, 7.9458, 7.9911, 8.1937, 8.2927, 8.3835, 8.4586, 8.5211, 8.5825, 8.6154, 8.6227, 8.3987]
basics_df = pd.DataFrame({'year': range(2003,2019), 'population': population_list})
offenses = ['violation-offenses', 'misdemeanor-offenses', \
            'non-seven-major-felony-offenses', 'seven-major-felony-offenses']
for offense in offenses:
    file = f'data/{offense}-2000-2018.xls'
    df = pd.read_excel(file).T.reset_index()
    if offense == 'violation-offenses':
        df = df[[2,5]]
        df = df.rename(columns = {2: 'year', 5: offense})
    elif offense == 'misdemeanor-offenses':
        df = df[[2,20]]
        df = df.rename(columns = {2: 'year', 20: offense})
    elif offense == 'non-seven-major-felony-offenses':
        df = df[[3,12]]
        df = df.rename(columns = {3: 'year', 12: offense})
    elif offense == 'seven-major-felony-offenses':
        df = df[[3,11]]
        df = df.rename(columns = {3: 'year', 11: offense})
    df = df.drop(index = 0)
    df = df.astype('float64')
    basics_df = basics_df.merge(df, on = 'year', how = 'inner')
for offense in offenses:
    basics_df[offense] = basics_df[offense] / (10 * basics_df.population)
fig, ax1 = plt.subplots(1, 1, figsize = (10, 6))
for offense in offenses:
    sns.lineplot(x = 'year', y = offense, data = basics_df, ax = ax1, legend = 'full')
ax1.set_xticks(range(2003, 2019, 1))
ax1.set_xticklabels(range(2003, 2019, 1), rotation=90)
ax1.set_xlabel('')
ax1.set_ylim(0, 9000)
ax1.set_ylabel('Reported offenses per 100,000 population')
ax1.set_title('Declining Crime Rates in NYC')
plt.legend(offenses)
plt.show()

# Number of stops over time
stops_list = [160851, 313523, 398191, 506491, 472096, 540302, 581168, 601285, 685724, 532911, 191851, 45787, 22565, 12404, 11629, 11008]
innocent_stops_list = [140442, 278933, 352348, 457163, 410936, 474387, 510742, 518849, 605328, 473644, 169252, 37744, 18353, 9394, 7833, 7645]
basics_df = basics_df.merge(pd.DataFrame({'year': range(2003, 2019), 'stops': stops_list}))
basics_df = basics_df.merge(pd.DataFrame({'year': range(2003, 2019), 'innocent_stops': innocent_stops_list}))
basics_df['stops'] = basics_df.stops / (10*basics_df.population)
basics_df['stop_arrests'] = (basics_df.stops) - (basics_df.innocent_stops / (10*basics_df.population))
fig, ax2 = plt.subplots(1, 1, figsize = (10, 6))
sns.lineplot(x = 'year', y = 'stops', data = basics_df, ax = ax2)
sns.lineplot(x = 'year', y = 'stop_arrests', data = basics_df, ax = ax2)
ax2.set_xticks(range(2003, 2019, 1))
ax2.set_xticklabels(range(2003, 2019, 1), rotation=90)
ax2.set_xlabel('')
ax2.set_ylim(0, 9000)
ax2.set_ylabel('Stops per 100,000 population')
ax2.set_title('In 2013, Stop-Question-Frisk Downsized in NYC')
plt.legend(['Stops', 'Stop arrests'])
plt.show()

# Relationship between stop rates and crime rates across precincts and time
df = dm.load_dataframe()
fig, ax3 = plt.subplots(1, 1, figsize=(10, 6))
sns.scatterplot(x = 'stoprate', y='crimerate', hue='policy', data=df, ax=ax3)
ax3.set(xscale="log", yscale="log")
# fix tick labels
ax3.set_yticks((20, 30, 50, 100))
ax3.set_xticks((1, 10, 100))
ax3.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax3.get_xaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())
ax3.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax3.get_yaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())
ax3.set_xlabel('Stops per 1,000 population')
ax3.set_ylabel('Reported offenses\nper 1,000 population')
ax3.set_title('Stop Rate and Crime Rate Vary\nover Time and across Precincts')
handles, labels = ax3.get_legend_handles_labels()
ax3.legend(handles=handles[::-1], labels=labels[::-2])
leg = ax3.get_legend()
for t, l in zip(leg.texts, ['before 2013','after 2013']): t.set_text(l)
plt.show()

# Relationship between arrest rates and crime rates across precincts and time
fig, ax4 = plt.subplots(1, 1, figsize=(10, 6))
ax4 = sns.scatterplot(x='nonstop_arrestrate', y='crimerate', hue='policy', data=df, ax=ax4)
ax4.set(xscale="log", yscale="log")
ax4.set_xlabel('Arrests per 1,000 population')
ax4.set_ylabel('Reported offenses\nper 1,000 population')
ax4.set_title('Crime and Arrest Rates are Highly\nCorrelated across Time and across Precincts')

ax4.set_yticks((20, 30,40, 60, 100))
ax4.set_xticks((10, 100))
ax4.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax4.get_xaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())
ax4.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax4.get_yaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())

handles, labels = ax4.get_legend_handles_labels()
ax4.legend(handles=handles[::-1], labels=labels[::-2])
leg = ax4.get_legend()
for t, l in zip(leg.texts, ['before 2013','after 2013']): t.set_text(l)
plt.show()

