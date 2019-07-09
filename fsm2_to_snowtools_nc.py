#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 12:32:39 2019

@author: Alex Priestley


This script creates a netcdf file from FSM2 model output which is  (work in progress...) compatible 
with CEN snowtools python tools
"""

from netCDF4 import Dataset
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from netCDF4 import date2num

'''
!!! adjust your paths as necessary !!!
'''
#load in csv files

snowro = pd.read_csv("/home/s0814684/FSM/snowtools/fsm_data/SNOWRO.csv",
                       index_col = 0,low_memory=False)

'''
snowtools needs missing values to be set as 9.97e+36 for some reason to work...
'''
                      
snowro.fillna(997.e+34,inplace=True)

wsn = pd.read_csv("/home/s0814684/FSM/snowtools/fsm_data/WSN.csv", index_col = 0,
                       low_memory=False)
wsn.fillna(997.e+34,inplace=True)

dsn = pd.read_csv("/home/s0814684/FSM/snowtools/fsm_data/DSN.csv", index_col = 0,
                       low_memory=False)
dsn.fillna(997.e+34,inplace=True)

snowdz = pd.read_csv("/home/s0814684/FSM/snowtools/fsm_data/SNOWDZ.csv", index_col = 0,
                       low_memory=False)
snowdz.fillna(997.e+34,inplace=True)

# create netcdf file
dataset = Dataset('/home/s0814684/FSM/snowtools/fsm_data/snow1819.nc','w', format='NETCDF4_CLASSIC')

#create dimensions of netcdf file (to match CEN format)

Number_of_points = dataset.createDimension('Number_of_points',1)
Number_of_Tile = dataset.createDimension('Number_of_Tile',1)
snow_layer = dataset.createDimension('snow_layer',10)
time = dataset.createDimension('time',None)


#create attributes
dataset.title='FSM2_data_1819'


# create time variable 
time=dataset.createVariable('time',np.float64, ('time',))
time.standard_name='time'
time.units='hours since 2018-07-31'
time.calendar = 'standard'
time.axis='T'

# create data variables
SNOWRO = dataset.createVariable('SNOWRO',np.float64,('time','snow_layer','Number_of_points'))#,
                                #fill_value=997.e+34)
SNOWRO.long_name='Snow_density'
SNOWRO.units='Kg/m3'
SNOWRO.missing_value=1.e+20

SNOWDZ = dataset.createVariable('SNOWDZ',np.float64,('time','snow_layer','Number_of_points'))#,
                                #fill_value=997.e+34)
SNOWDZ.long_name = 'Snow layer thickness'
SNOWDZ.units='m'
SNOWDZ.missing_value=1.e+20

DSN_T_ISBA = dataset.createVariable('DSN_T_ISBA',np.float64,('time','Number_of_Tile','Number_of_points'))#,
                                    #fill_value=997.e+34)
DSN_T_ISBA.long_name='total_snow_depth'
DSN_T_ISBA.units='m'
DSN_T_ISBA.missing_value=1.e+20

WSN_T_ISBA = dataset.createVariable('WSN_T_ISBA',np.float64,('time','Number_of_Tile','Number_of_points'))#,
                                    #fill_value=997.e+34)
WSN_T_ISBA.long_name='total_snow_reservoir'
WSN_T_ISBA.units='kg/m2'
WSN_T_ISBA.missing_value=1.e+20

'''
write dataframes to netcdf variables
'''
DSN_T_ISBA[:,:]= dsn  
SNOWDZ[:,:] = snowdz
SNOWRO[:,:] = snowro
WSN_T_ISBA[:,:]= wsn


'''
insert your data start time and interval here
'''

dates = []
for n in range(SNOWRO.shape[0]):
    dates.append(datetime(2018, 7, 31) + n * timedelta(hours=1))

time[:] = date2num(dates, units = time.units, calendar = 'standard')

'''
write netcdf file
'''
dataset.close()




