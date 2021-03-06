from __future__ import division
__author__ = 'Bijan'
'''
This is a function to plot CCLM outputs.

'''
from netCDF4 import Dataset as NetCDFFile
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_pdf import PdfPages
import os
import cartopy.crs as ccrs
import cartopy.feature
def rand_station_locations(N=50,sed=777):
    import requests
    import random
    import re
    #data = requests.get(
        #"http://www.ecad.eu/download/ensembles/data/ensembles_all_stations_v13.1.txt")  # read only 20 000 chars
    #    "http://www.ecad.eu/download/ensembles/data/Version14.0/ensembles_tg_stations_v14.0.txt") # new version!
    data = open("/scratch/users/fallah/OI_EOBS/OI_CCLM/ensembles_tg_stations_v14.0.txt")    
    Data = []

    pattern = re.compile(r"[^-\d]*([\-]{0,1}\d+\.\d+)[^-\d]*")
    results = []
    for line in data:
        
        line = line.decode().split("|")
        for i in line:
            match = pattern.match(i)
            if match:
                results.append(match.groups()[0])

    pairs = []
    i = 0
    end = len(results)

    while i < end - 1:
        pairs.append((results[i], results[i + 1]))
        i += 1

    # # Choose N random stations
    random.seed(sed)
    rand_obs_number = random.sample(range(0, 8900), 7000)
    k = 0
    lat={}
    lon={}

    for i in rand_obs_number:


        if 33 < float(pairs[i][0]) < 65 and -10 < float(pairs[i][1]) < 41: #TODO: make the limits smarter
            lat[k]= float(pairs[i][0])
            lon[k] = float(pairs[i][1])
            k = k + 1

    return(list(lat.values())[0:N],list(lon.values())[0:N])




if not os.path.exists('TEMP'):
    os.makedirs('TEMP')
os.chdir('TEMP')

def Plot_CCLM(dir_mistral='/scratch/b/b324045/cclm-sp_2.1/data/ext/',name='europe_0440.nc',bcolor='red',var='HSURF',flag='TRUE'
              ,color_map='TRUE', alph=1, grids='TRUE', grids_color='red', rand_obs='FALSE', NN=500):
    # type: (object, object, object, object, object, object, object, object, object) -> object
    # type: (object, object, object, object, object, object) -> object
    #CMD = 'scp $mistral:'+ dir_mistral+ name+' ./' # here I have commented as I copied the files on local
    CMD = 'wget users.met.fu-berlin.de/~BijanFallah/'+ dir_mistral+ name
    os.system(CMD)
    nc = NetCDFFile(name)
    os.remove(name)
    lats = nc.variables['lat'][:]
    lons = nc.variables['lon'][:]
    rlats = nc.variables['rlat'][:]  # extract/copy the data
    rlons = nc.variables['rlon'][:]
    t = nc.variables[var][:].squeeze()
    nc.close()
    fig = plt.figure('1')
    fig.set_size_inches(14, 10)
    #rp = ccrs.RotatedPole(pole_longitude=-162.0,
    #                      pole_latitude=39.25,
    #                      globe=ccrs.Globe(semimajor_axis=6370000,
    #                                          semiminor_axis=6370000))
    rp = ccrs.RotatedPole(pole_longitude=-165.0,
                          pole_latitude=46.0,
                          globe=ccrs.Globe(semimajor_axis=6370000,
                                           semiminor_axis=6370000))
    pc = ccrs.PlateCarree()
    ax = plt.axes(projection=rp)
    ax.coastlines('50m', linewidth=0.8)
    ax.add_feature(cartopy.feature.LAKES,
                   edgecolor='none', facecolor='lightblue',
                   linewidth=0.8)

    t[t < 0] = 0
    if flag=='TRUE':
        v = np.linspace(0, 3000, 11, endpoint=True)
        cs = plt.contourf(lons, lats, t, v, transform=ccrs.PlateCarree(), cmap=plt.cm.terrain)
        if color_map=='TRUE':
            cb = plt.colorbar(cs)
            cb.set_label('topography [m]', fontsize=20)
            cb.ax.tick_params(labelsize=20)
    ax.add_feature(cartopy.feature.OCEAN,
                   edgecolor='black', facecolor='lightblue',
                   linewidth=0.8)
    ax.gridlines()
    ax.text(-45.14, 15.24, r'$45\degree N$',
            fontsize=15)
    ax.text(-45.14, 35.73, r'$60\degree N$',
            fontsize=15)
    ax.text(-45.14, -3.73, r'$30\degree N$',
            fontsize=15)
    ax.text(-45.14, -20.73, r'$15\degree N$',
            fontsize=15)
    ax.text(-19.83, -35.69, r'$0\degree $',
            fontsize=15)
    ax.text(15.106, -35.69, r'$20\degree E$',
            fontsize=15)
    #ax.text(26, -29.69, r'$40\degree E$',
    #        fontsize=15)
    if grids=='TRUE':
        rlonss, rlatss = np.meshgrid(rlons,rlats)
        plt.scatter(rlonss, rlatss, marker='.', c=grids_color, s=2, alpha=.4)
    if rand_obs=='TRUE':
        s,t = rand_station_locations(NN, sed=777)

        #tt,ss=np.meshgrid(t.values(),s.values())
        from rotgrid import Rotgrid
        mapping = Rotgrid(-165.0,46.0,0,0)
        #TT=t.values()
        #SS=s.values()
        TT=t
        SS=s
        for i in range(0,NN):#just for sed -i
            (TT[i], SS[i]) = mapping.transform(TT[i], SS[i])
            plt.scatter(TT[i], SS[i], marker='+', c=grids_color, s=10, zorder=10)
           # print(TT[i],SS[i])

    plt.hlines(y=min(rlats), xmin=min(rlons), xmax=max(rlons), color=bcolor,linestyles= 'solid', linewidth=2, alpha=alph)
    plt.hlines(y=max(rlats), xmin=min(rlons), xmax=max(rlons), color=bcolor,linestyles= 'solid', linewidth=2, alpha=alph)
    plt.vlines(x=min(rlons), ymin=min(rlats), ymax=max(rlats), color=bcolor,linestyles= 'solid', linewidth=2, alpha=alph)
    plt.vlines(x=max(rlons), ymin=min(rlats), ymax=max(rlats), color=bcolor,linestyles= 'solid', linewidth=2, alpha=alph)
    xs, ys, zs = rp.transform_points(pc,
                                     np.array([-17, 105.0]),
                                     np.array([3, 60])).T
    ax.set_xlim(xs)
    ax.set_ylim(ys)

#os.chdir('../')
