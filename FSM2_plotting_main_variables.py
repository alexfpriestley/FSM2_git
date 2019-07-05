#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 12:04:15 2019

@author: Alex Priestley
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt



SNOWRO = pd.read_csv("/home/s0814684/FSM/snowtools/fsm_data/SNOWRO.csv",
                       index_col = 0,low_memory=False)

WSN = pd.read_csv("/home/s0814684/FSM/snowtools/fsm_data/WSN.csv", index_col = 0,
                       low_memory=False)

DSN = pd.read_csv("/home/s0814684/FSM/snowtools/fsm_data/DSN.csv", index_col = 0,
                       low_memory=False)

SNOWDZ = pd.read_csv("/home/s0814684/FSM/snowtools/fsm_data/SNOWDZ.csv", index_col = 0,
                       low_memory=False)




'''
Enter start and end of your data for creating an index for plots (the index from the dataframe doesn't seem to 
work with plt)
'''
time_start =  '20180731' #input('Enter the start date (yyyymmdd): ')
time_end = '20190507' #input('Enter the end date (yyyyddmm): ')
time_start = dt.datetime.strptime(time_start,'%Y%m%d')
time_end = dt.datetime.strptime(time_end,'%Y%m%d')

'''
Change freq to match the interval of your data:
https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases
'''
index = pd.date_range(time_start,time_end, freq='H')

# merge into one df called snow for 1d variables (bulk quantities)
snow = pd.DataFrame()
snow['WSN']=WSN['WSN_T_ISBA']
snow['DSN']=DSN['DSN_T_ISBA']
snow.index=index

'''
plot swe and snd on one chart
'''

ax1 = snow['WSN'].plot(label='Snow Water Equivalent (kg/m3)',color='b')
ax1.set_ylabel('SWE')
lines, labels = ax1.get_legend_handles_labels()

ax2 = ax1.twinx()
ax2.set_ylabel('Snow depth')
ax2.spines['right'].set_position(('axes', 1.0))
snow['DSN'].plot(ax=ax2,label='Snow depth (m)',color='r')
line, label = ax2.get_legend_handles_labels()
lines += line
labels += label

ax1.legend(lines,labels,loc=0)

'''
plot layer variables on scatter plots, colouring by density or grain size
'''









