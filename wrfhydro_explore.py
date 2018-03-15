# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 20:41:55 2017

@author: likkhian
"""

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import datetime
import glob
import pandas as pd
#fulldom=xr.open_dataset('C:/Users/likkhian/Desktop/fulldom/Fulldom_hires5.nc')
#print(fulldom)
#plt.pcolormesh(fulldom.STREAMORDER)
#geo=xr.open_dataset('C:/Users/likkhian/Desktop/fulldom/geo_em.d02.nc')
#plt.pcolormesh(geo.HGT_M[0,:,:])
#wrfin=xr.open_dataset('C:/Users/likkhian/Desktop/fulldom/wrfinput_d02')
#
#fulldom=xr.open_dataset('C:/Users/likkhian/Desktop/fulldom/Fulldom_hires4.nc')
#ref=xr.open_dataset('C:/Users/likkhian/Desktop/fulldom/Fulldom_hires_netcdf_file.nc')
##x={'x' : fulldom.x.data}
##y={'y' : fulldom.y.data}
#x=fulldom.x.data
#y=fulldom.y.data
#CHANNELGRID=np.float64(fulldom.CHANNELGRID)
#FLOWACC=np.float64(fulldom.FLOWACC)
#LAKEGRID=np.float64(fulldom.LAKEGRID)
#LATITUDE=np.float64(fulldom.LATITUDE)
#LONGITUDE=np.float64(fulldom.LONGITUDE)
#OVROUGHRTFAC=np.float64(fulldom.OVROUGHRTFAC)
#RETDEPRTFAC=np.float64(fulldom.RETDEPRTFAC)
#landuse=np.float64(fulldom.landuse)
#STREAMORDER=fulldom.STREAMORDER
#TOPOGRAPHY=fulldom.TOPOGRAPHY
#frxst_pts=fulldom.frxst_pts
#gw_basns=fulldom.gw_basns
#FLOWDIRECTION=fulldom.FLOWDIRECTION

#fulldom2=xr.Dataset(data_vars=[CHANNELGRID,FLOWACC,LAKEGRID,LATITUDE,LONGITUDE,OVROUGHRTFAC,RETDEPRTFAC, \
#landuse,STREAMORDER,TOPOGRAPHY,frxst_pts,gw_basns,FLOWDIRECTION], coords=x,y)
#fulldom2=xr.Dataset({'x':(['x'],x),'y':(['y'],y),'CHANNELGRID':(['y','x'],CHANNELGRID),'FLOWACC':(['y','x'],FLOWACC),'LAKEGRID':(['y','x'],LAKEGRID),'LATITUDE':(['y','x'],LATITUDE),'LONGITUDE':(['y','x'],LONGITUDE),'OVROUGHRTFAC':(['y','x'],OVROUGHRTFAC),'RETDEPRTFAC':(['y','x'],RETDEPRTFAC),'STREAMORDER':(['y','x'],STREAMORDER),'TOPOGRAPHY':(['y','x'],TOPOGRAPHY),'FLOWDIRECTION':(['y','x'],FLOWDIRECTION),'frxst_pts':(['y','x'],frxst_pts),'gw_basns':(['y','x'],gw_basns),'landuse':(['y','x'],landuse)})
#'x':(['y'],x),'y':(['x'],y),
#
#fulldom2.to_netcdf('C:/Users/likkhian/Desktop/fulldom/Fulldom_hires6.nc')

#open and save as ANSI
with open('C:/Users/likkhian/Desktop/fulldom/hydrooutputs/qstrmvolrt_accum44.txt') as f1:
    dirty1=f1.read().split()
    qstrm=[float(l.strip()) for l in dirty1]
    print(len(qstrm))
    
base=datetime.datetime(2090,1,1)
time=np.array([base + datetime.timedelta(hours=i) for i in range(len(qstrm))])


#stationNames=('ChiangSaen','Luang Prabang','Chiang Khan','Vientiane','Nongkhai', \
#'Paksane', 'Thakhek', 'Mukdahan', 'Khongchiam', 'Pakse', 'Stung Treng', 'Kratie', \
#'Kampong Cham', 'Prek Kdam', 'Phnom Penh', 'Neak Loung', 'Tan Chau', 'Chau Doc')
stationNames=('Tan Chau','Neak Loung','Phnom Penh','Prek Kdam','Kampong Cham', \
'Kratie','Stung Treng','Pakse','Khong Chiam','Mukdahan','Thakhek','Nongkhai', \
'Chiang Khan','Vientiane','Paksane','Luang Prabang','ChiangSaen')
#directory='C:/Users/likkhian/Desktop/fulldom/hydrooutputs/'
directory='C:/Users/likkhian/SkyDrive/Thesis/wrfhydro_output/'
fileloc=directory+'frxst_pts_out_2000_01.txt'
print(fileloc)
df=pd.read_table(fileloc,delimiter=",",header=None)
df.columns=['s in simulation','datetime','stationID','lon','lat', \
'discharge m3s','discharge ft3s','depth']
df['datetime']=pd.to_datetime(df['datetime'])
#print(df.head())
#print(df.tail())

#find extra dates
df['datetime'].value_counts().loc[df['datetime'].value_counts()<17].sort_index().resample('D',how='sum').dropna()
stations=df['stationID'].unique()
#print(stations)
#print(df.lon.unique())
#print(df.lat.unique())

idd=16
plt.figure(3)
plt.plot(df.loc[df['stationID']==idd]['datetime'],df.loc[df['stationID']==idd]['discharge m3s'],label=stationNames[idd])
#plt.plot(df.loc[df['stationID']==13]['datetime'][48:],df.loc[df['stationID']==13]['discharge m3s'][48:],label=stationNames[13])

for index,ii in enumerate(stations):
    plt.plot(df.loc[df['stationID']==ii]['datetime'][48:],df.loc[df['stationID']==ii]['discharge m3s'][48:],label=stationNames[ii])
    print('{},{:.2f}'.format(stationNames[ii],np.mean(df.loc[df['stationID']==ii]['discharge m3s'][48:])))
plt.title('Station reading m3s')
plt.legend(loc='upper left')
plt.show()

#fulldom=xr.open_dataset('C:/Users/likkhian/Desktop/fulldom/Fulldom_hires6.nc')
#print(fulldom)
#y,x = np.where(fulldom.frxst_pts >= 0)
#print(x,y)
#print(fulldom.LATITUDE[y,0])
#print(fulldom.LONGITUDE[0,x])
#
#channel=xr.open_dataset('C:/Users/likkhian/Desktop/fulldom/hydrooutputs/201510010000.CHRTOUT_GRID2')
#for i in range(len(y)):
#    print(fulldom.LATITUDE[y[i],x[i]].data,fulldom.LONGITUDE[y[i],x[i]].data)
#    print(channel.streamflow[0,1800-y[i]-1,x[i]].data,x[i],1800-y[i]-1)
#print(channel.streamflow)

ldasout=xr.open_dataset('C:/Users/likkhian/Desktop/fulldom/hydrooutputs/2090122500.LDASOUT_DOMAIN2')
variables=['ACCPRCP','ACCECAN','ACCETRAN','ACCEDIR','UGDRNOFF','SFCRNOFF']
for ii in variables:
    print('{}={:.8e}'.format(ii,np.float(np.sum((ldasout[ii]>0)*ldasout[ii]))/1000*9000*9000))

fulldom=xr.open_dataset('C:/Users/likkhian/Desktop/fulldom/Fulldom_hiresD.nc')
jxrt,ixrt=np.shape(fulldom.frxst_pts)
print('count,direction,lon,lat,i,j')
count=0
for j in range(jxrt):
    for i in range(ixrt):
        if (fulldom.CHANNELGRID[jxrt-1-j,i] == 0):
            count=count+1
            print('{},{},{:.5f},{:.5f},{},{}'.format(count,float(fulldom.FLOWDIRECTION[j,i]),\
            float(fulldom.LONGITUDE[jxrt-1-j,i]),float(fulldom.LATITUDE[jxrt-1-j,i]),i,j))
            if (count>15):
                break
print(count)