#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 10:05:08 2019
@author: Alex Priestley


#############
Reads FSM2 output from _prf and _smp and _ave files and writes to pandas
dataframes, and saves as csv files
#############
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

"""
Read in prf filename, start and end dates, and max number of snow layers
"""
filename = 'safran_CdP_1819_prf' #input('Enter the FSM2 prf filename: ')
time_start =  '20180731' #input('Enter the start date (yyyymmdd): ')
time_end = '20190507' #input('Enter the end date (yyyyddmm): ')
time_start = dt.datetime.strptime(time_start,'%Y%m%d')
time_end = dt.datetime.strptime(time_end,'%Y%m%d')
smax=10  #input('Enter the maximum number of snow layers on this FSM2 run: ')
year1=np.float('2018') #input('Enter the year of start of winter (YYYY): ')
year2=np.float('2019') #input('Enter the year of finish of winter (YYYY): ')
'''
create index - change FREQ to your data frequency:
https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases
'''
index = pd.date_range(time_start,time_end,freq= 'H') 

'''
read in smp filename ENTER YOUR FILEPATH FOR LOADTXT
'''
filename2 = 'safran_CdP_1819_smp' #input('Enter the FSM2 smp filename: ')

snd = np.loadtxt('/home/s0814684/FSM/FSM2-master/'+str(filename2)+'',usecols=[4]) # snow depth
swe = np.loadtxt('/home/s0814684/FSM/FSM2-master/'+str(filename2)+'',usecols=[5]) # snow water equivalent

DSN = pd.DataFrame() # create dataframes 
DSN['snd']=snd
DSN.index=index

WSN = pd.DataFrame()
WSN['swe']=swe
WSN.index=index



'''
open prf file and write to array - !!!ENTER YOUR FILEPATH HERE!!!
'''
profile = []
with open('/home/s0814684/FSM/FSM2-master/'+str(filename)+'') as file:
    for line in file: 
        line = line.strip()
        line = line.split()
        profile.append(line)

'''
read snow layers and write to array
'''
snowlayers=[]

for n in range(len(profile)):
    ln = profile[n]
    ln=[float(i) for i in ln]
    if ln[0]==year1 or ln[0]==year2:
        nsnow=ln[3]
        if nsnow==0:
            snowlayers=np.append(snowlayers,profile[n])
        if nsnow >= 1:
            snowlayers=np.append(snowlayers,profile[n])
            for m in range(1,int(nsnow)+1):
                snowlayers=np.append(snowlayers,profile[m+n])
            
        
                    

snowlayers=[float(i) for i in snowlayers] # convert from strings to numbers to allow arithmetic
'''
create list of snow layer column names for df
'''
layers=[] 
for i in range(1,smax+1):
    layer = ['layer'+str(i)+'']
    layers=np.append(layers,layer)
'''
read snow grainsize from snowlayers and write to df
'''
count=0

rgr = pd.DataFrame(index=index,columns=(layers))
for j in range(len(snowlayers)):
    if snowlayers[j]==year1 or snowlayers[j]==year2:
        nsnow=snowlayers[j+3]
        if nsnow==0:
            count+=1
        if nsnow>=1:
            for n in range(int(nsnow)):
               rgr.iloc[count,n]=snowlayers[(j+8)+(6*n)]   
            count+=1
            
rgr_mm=rgr*1000 # get grain size in mm
        
layers2=np.append(layers,'nsnow')

''' 
create dfs for density and snow layer thickness/depth and write to them
'''
lyr_dens = pd.DataFrame(index=index,columns=(layers))
lyr_snd = pd.DataFrame(index=index,columns=(layers2))
lyr_snd2 = pd.DataFrame(index=index,columns=(layers2))
lyr_Ds = pd.DataFrame(index=index,columns=(layers))
lyr_Ds2 = pd.DataFrame(index=index,columns=(layers))
count = 0

for j in range(len(snowlayers)):
    if snowlayers[j]==year1 or snowlayers[j]==year2:
        nsnow=snowlayers[j+3]
        cum_snd = 0
        if nsnow==0:
            lyr_snd.iloc[count,smax]=0
            count+=1
        if nsnow>=1:
            for n in range(int(nsnow)):
                sliq=snowlayers[(j+10)+(6*n)]
                sice=snowlayers[(j+9)+(6*n)]
                Ds=snowlayers[(j+6)+(6*n)]
                dense=(sliq+sice)/Ds
                lyr_dens.iloc[count,n]=dense
                lyr_Ds.iloc[count,n]=Ds
                cum_snd+=Ds
                lyr_snd.iloc[count,n] = cum_snd
                lyr_snd.iloc[count,smax] = nsnow
            count+=1
            
'''           
correct snow layer heights and thicknesses to be right way up in terms of depth
'''
for n in range(len(lyr_snd)):
    n_snow=lyr_snd.iloc[n,10]
    if n_snow==np.nan:
        n_snow=0
    forwards = []
    for i in range(int(n_snow)):
        forwards=np.append(forwards,i)
    backwards=[]
    for i in range(int(n_snow)-1,-1,-1):
        backwards=np.append(backwards,i)
    for  m in range(int(n_snow)):
        depth = lyr_snd.iloc[n,int(backwards[m])]
        thickness = lyr_Ds.iloc[n,int(backwards[m])]
        lyr_snd2.iloc[n,int(forwards[m])]=depth
        lyr_Ds2.iloc[n,int(forwards[m])]=thickness

#remove nsnow column from lyr_snd
lyr_snd2 = lyr_snd2.drop(columns=["nsnow"]) 
#save files as csv

lyr_snd2.to_csv('/home/s0814684/FSM/snowtools/fsm_data/layer_height.csv',sep=',') # csv of height of each lyr interface
lyr_Ds2.to_csv('/home/s0814684/FSM/snowtools/fsm_data/SNOWDZ.csv',sep=',') # csv of snow layer thickness
rgr_mm.to_csv('/home/s0814684/FSM/snowtools/fsm_data/rgr_mm.csv',sep=',') # csv of grainsize in mm
lyr_dens.to_csv('/home/s0814684/FSM/snowtools/fsm_data/SNOWRO.csv',sep=',') # csv of layer snow density


DSN.to_csv('/home/s0814684/FSM/snowtools/fsm_data/DSN.csv',sep=',') # snow depth
WSN.to_csv('/home/s0814684/FSM/snowtools/fsm_data/WSN.csv',sep=',') # snow water equivalent



  #
#plt.figure(figsize=(9,9))
#
#for n in range(len(layers)):
#    plt.scatter(index, lyr_snd2.iloc[:,n], c=lyr_dens.iloc[:,n],vmin=100,vmax=500,cmap='winter')
#    
#    
#plt.colorbar().set_label('Snow Density (kg/m^2)')  
#plt.ylabel('Snow depth (m)')
#axes = plt.gca()
#axes.set_ylim([0,None])
#plt.gcf().autofmt_xdate()  
#plt.show()
#
#
#
#plt.figure(figsize=(9,9))
#for n in range(len(layers)):
#    plt.scatter(index, lyr_snd2.iloc[:,n], c=rgr_mm.iloc[:,n],vmin=0,vmax=2,cmap='gnuplot2')
#plt.colorbar().set_label('Snow grainsize (mm)')  
#plt.ylabel('Snow depth (m)')
#plt.gcf().autofmt_xdate()  
#plt.show()  












