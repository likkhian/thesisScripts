# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 14:32:40 2018
Uses the high res basin mask from wrfhydro input to create a
mask of basin on 9km resolution
@author: likkhian
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

fulldom=xr.open_dataset('/Users/likkhian/OneDrive/Thesis/HydrologySection/wrfhydroInputs/Fulldom_hiresD.nc')

#wrf=xr.open_dataset('/Users/likkhian/Desktop/wrfpost_run_2000_01_d02.nc')
wrf=xr.open_dataset('/Users/likkhian/Desktop/wrfout_d02_0054-12-31_00:00:00')
#plt.figure(2)
#plt.pcolormesh(wrf.LANDMASK[0,:,:])
#plt.colorbar()
def basinmaker(fulldom,wrf,trimmed=True):
    if(trimmed):
        basns=np.flipud(fulldom.basn_msk.data[50:-50,50:-50])
    else:
        basns=np.flipud(fulldom.basn_msk.data)
        ti,la,lo=np.shape(wrf.LANDMASK.data)
    lla,llo=np.shape(basns)
    new_basns=np.zeros([la,lo])
    for ii in range(0,lla-10,10):
        for jj in range(0,llo-10,10):
            iii=int(ii/10)
            jjj=int(jj/10)
            if(np.any(basns[ii:ii+10,jj:jj+10] > 0)):
                new_basns[iii,jjj]=1
    return new_basns

#plt.figure(3)
#plt.pcolormesh(new_basns)
#plt.colorbar()

def shader(starty,endy,startx,endx):
    for ii in range(starty,endy):
        for jj in range(startx,endx):
            if(wrf.LANDMASK.data[0,ii,jj]==1):
                new_basns[ii,jj]=1
#    plt.pcolormesh(wrf.LANDMASK[0,:,:]+new_basns)
    plt.subplot(projection=ccrs.PlateCarree())
    plt.pcolormesh(wrf.lon,wrf.lat,wrf.LANDMASK[0,:,:]+new_basns)
    plt.title('Drainage basin for Lower Mekong River')
    ax=plt.gca()
    gl=ax.gridlines(draw_labels=True)
    gl.xlabels_top=False
    gl.ylabels_right=False
    gl.ylocator = mticker.FixedLocator([5, 7, 9, 11, 13, 15, 17, 19, 21])
    gl.xlocator = mticker.FixedLocator([95, 97, 99, 101, 103, 105, 107, 109, 111])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    ax.coastlines()
    ax.add_feature(cfeature.RIVERS)
    plt.tight_layout()

new_basns=basinmaker(fulldom,wrf,trimmed=False)    

#coloring in the mekong delta region
#shader(20,48,101,135)
#shader(20,49,101,134)
#shader(20,50,101,132)
#shader(20,51,101,130)
#shader(20,52,101,128)
#shader(20,53,101,125)
#shader(20,54,101,123)
#shader(20,55,101,121)
#shader(20,56,101,120)
#shader(156,169,48,69)

#new_basn_msk = xr.DataArray(new_basns,coords={'lon':wrf.lon,'lat':wrf.lat},name='new_basn_msk')
lons=wrf.XLONG[0,0,:].data
lats=wrf.XLAT[0,:,0].data
new_basn_msk = xr.DataArray(new_basns,coords={'lon':lons,'lat':lats},name='new_basn_msk')
new2=new_basn_msk.to_dataset()
#new2.to_netcdf('/Users/likkhian/Desktop/new_basn_msk_hydromain.nc')