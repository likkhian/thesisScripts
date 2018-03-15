# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 19:56:26 2018

@author: likkhian
"""

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import datetime
import glob
import pandas as pd

directory='C:/Users/likkhian/SkyDrive/Thesis/wrfhydro_output/'
files_2000=['frxst_pts_out_2000_01','frxst_pts_out_2000_02','frxst_pts_out_2000_03']
files_eas0c=['frxst_pts_out_eas0c_01','frxst_pts_out_eas0c_02','frxst_pts_out_eas0c_03']

def readtable(fileloc):
    df=pd.read_table(fileloc,delimiter=",",header=None)
    df.columns=['s in simulation','datetime','stationID','lon','lat', \
    'discharge m3s','discharge ft3s','depth']
    df['datetime']=pd.to_datetime(df['datetime'])
    return df
def makefilename(var):
    return directory+var+'.txt'
def combine_files(file_list):
    df=readtable(makefilename(file_list[0]))
    df2 = pd.concat([df,readtable(makefilename(file_list[1]))])
    df3 = pd.concat([df2,readtable(makefilename(file_list[2]))])
    return df3

df=combine_files(files_eas0c)
df.describe()
print(df[['stationID','lon','lat']].iloc[:17])

stationNames=('Tan Chau','Neak Loung','Phnom Penh','Prek Kdam','Kampong Cham', \
'Kratie','Stung Treng','Pakse','Khong Chiam','Mukdahan','Thakhek','Nongkhai', \
'Chiang Khan','Vientiane','Paksane','Luang Prabang','ChiangSaen')
stations=df['stationID'].unique()
for index,ii in enumerate(stations):
    plt.plot(df.loc[df['stationID']==ii]['datetime'],df.loc[df['stationID']==ii]['discharge m3s'],label=stationNames[ii])
    print('{},{:.2f}'.format(stationNames[ii],np.mean(df.loc[df['stationID']==ii]['discharge m3s'])))
plt.title('Station reading m3s')
plt.legend(loc='upper left')
plt.show()