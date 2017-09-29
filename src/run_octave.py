# run octave from python (IO code )
# This code will run the IO code and produce the plots for RMSE and save the out put data
# Created by Bijan Fallah 
# info@bijan-fallah.com
# -----------------------------------------------------------------------------------
# DO not change any line here, it will be changed automatically by the io_scrpt.sh!!
# -----------------------------------------------------------------------------------

from oct2py import octave
import pandas as pd
import csv
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
from RMSE_MAPS_INGO import read_data_from_mistral as rdfm
from CCLM_OUTS import Plot_CCLM
import cartopy.crs as ccrs
#from Plot_RMSE_SPREAD_main import plot_rmse_spread as prs
# ============================================= NAMELIST ==========================================

SEAS='DJF'
NN=1000#number of observations should be read from previous funcions!!!!
month_length=20
SEAS='DJF'
Vari   = 'T_2M'
buffer=20
timesteps=10   # number of the seasons (years)
start_time=0
#name_2 = 'member_relax_3_big_00_' + Vari + '_ts_splitseas_1979_2015_' + SEAS + '.nc'
name_2 = 'tg_0.44deg_rot_v15.0_' + SEAS + '_1979_2015_remapbil.nc'
member=0
DIR="path_oi"
DIR_exp="path_dir"+"/"

# =================================================================================================
octave.run(DIR+"run_IO.m") # Running the Octave Interface from python!
# -------------------------------------------------------------------------------------------------


LAT = pd.read_csv(DIR_exp+"Trash/LAT.csv", header=None)
LON = pd.read_csv(DIR_exp+"Trash/LON.csv", header=None)
Forecast_3 = np.array(pd.read_csv(DIR_exp+'Trash/SEASON_MEAN1' + '_' + SEAS + '.csv', header=None))#Reading the Forecast values
t_f = np.zeros((month_length,Forecast_3.shape[0],Forecast_3.shape[1]))
for month in range(0, month_length):# Reading the ensemble forecast for each month!
    t_f[month,:,:] = pd.read_csv(DIR_exp+'Trash/SEASON_MEAN' + str(month) + '_' + SEAS + '.csv', header=None)
t_f = np.array(t_f)

## add correction to forecast :
# declare zero matrix which will be filled
result_IO = np.zeros((month_length,Forecast_3.shape[0],Forecast_3.shape[1]))
result = np.zeros((Forecast_3.shape[0],Forecast_3.shape[1]))
for i in range(0,month_length):
    fil=DIR + 'fi' + str(member) + str(i) +'.csv'
    result=np.array(list(csv.reader(open(fil,"rb"),delimiter=','))).astype('float')
    result_IO[i,:,:] = np.squeeze(t_f[i,:,:]) + result


# plot differences

pdf_name= 'last_m100_l20_'+str(member)+'.pdf'
#t_o, lat_o, lon_o, rlat_o, rlon_o =rdfm(dir='/work/bb1029/b324045/work5/03/member_relax_3_big_00/post/', # the observation (default run without shifting)
#                                            name=name_2,
#                                            var=Vari)
#t_o, lat_o, lon_o, rlat_o, rlon_o =rdfm(dir='NETCDFS_CCLM/03/member_relax_3_big_00/post/', # the observation (default run without shifting)
#                                            name=name_2,
#                                            var=Vari)
t_o, lat_o, lon_o, rlat_o, rlon_o =rdfm(dir='/NETCDFS_CCLM/eobs/', # the observation (default run without shifting)
                                        name=name_2,
                                        var=Vari)

dext_lon = t_o.shape[2] - (2 * buffer)
dext_lat = t_o.shape[1] - (2 * buffer)
start_lon=(buffer+4)
start_lat=(buffer-4)

##TODO: make it a function:
#def f(x):
#    if x==-9999:
#        return float('NaN')
#    else:
#        return x
#f2 = np.vectorize(f)
#t_o= f2(t_o)
#t_o=t_o.squeeze()
t_o = t_o.data
#t_o[np.isnan(t_o)] = np.nanmean(t_o)
##end todo         

t_o[t_o<-900]=float('NaN')
t_o[np.isnan(t_o)]=float('NaN')



forecast = result_IO
obs = t_o[0:month_length, buffer:buffer + dext_lat, buffer:buffer + dext_lon]
RMSE=np.zeros((forecast.shape[1],forecast.shape[2]))
RMSE_TIME_SERIES=np.zeros(forecast.shape[0])
RMSE_TIME_SERIES_Forecast=np.zeros(forecast.shape[0])
for i in range(0,forecast.shape[1]):
    for j in range(0,forecast.shape[2]):
        forecast_resh=np.squeeze(forecast[:,i,j])
        obs_resh=np.squeeze(obs[:,i,j])
        if (np.isnan(obs_resh).any()== False) and (np.isinf(obs_resh).any() == False) and (np.isnan(forecast_resh).any()== False) and (np.isinf(forecast_resh).any()== False):
            RMSE[i,j] = mean_squared_error(obs_resh, forecast_resh) ** 0.5 # Calculating the RMSEs for each grid point
        else:
            RMSE[i,j] = float('NaN')
        
for i in range(0,forecast.shape[0]):
    forecast_resh_ts=np.squeeze(forecast[i,:,:])
    obs_resh_ts=np.squeeze(obs[i,:,:])
    if (np.isnan(obs_resh_ts).any() == False) and (np.isinf(obs_resh_ts).any() == False) and (np.isnan(forecast_resh_ts).any()== False) and (np.isinf(forecast_resh_ts).any() == False):
        RMSE_TIME_SERIES[i] = mean_squared_error(obs_resh_ts, forecast_resh_ts) ** 0.5 #Calculating RMSEs for each month for Analysis
    else:
        RMSE_TIME_SERIES[i] = float('NaN')

for i in range(0,forecast.shape[0]):
    forecast_orig_ts=np.squeeze(t_f[i,:,:])
    obs_resh_ts=np.squeeze(obs[i,:,:])
    if (np.isnan(obs_resh_ts).any() == False) and (np.isinf(obs_resh_ts).any() == False) and (np.isnan(forecast_orig_ts).any()== False) and (np.isinf(forecast_orig_ts).any() == False):
        RMSE_TIME_SERIES_Forecast[i] = mean_squared_error(obs_resh_ts, forecast_orig_ts) ** 0.5 #Calculating RMSEs for each month for forecast
    else:
        RMSE_TIME_SERIES_Forecast[i] = float('NaN')


fig = plt.figure('1')
fig.set_size_inches(14, 10)


rp = ccrs.RotatedPole(pole_longitude=-165.0,# this number comes from int2clm settings
                          pole_latitude=46.0,# this number comes from int2clm settings
                          globe=ccrs.Globe(semimajor_axis=6370000,
                                           semiminor_axis=6370000))


pc = ccrs.PlateCarree()
ax = plt.axes(projection=rp)
ax.coastlines('50m', linewidth=0.8)
if SEAS[0] == "D":
#    v = np.linspace(0, .8, 9, endpoint=True)# the limits of the colorbar for winter
    v = np.linspace(0, 3.2, 9, endpoint=True)
else:
#    v = np.linspace(0, .8, 9, endpoint=True)# the limits of the colorbar for other seasons
    v = np.linspace(0, 3.2, 9, endpoint=True)

# Write the RMSE mean of the member in a file
import csv
from itertools import izip
names=DIR_exp+'Trash/'+'RMSE_'+pdf_name+str(member)+'.csv'
with open(names, 'wb') as f:
     writer = csv.writer(f)
     writer.writerow([NN,np.mean(RMSE)])
  
lats_f1=lat_o[buffer:buffer + dext_lat, buffer:buffer + dext_lon]
lons_f1=lon_o[buffer:buffer + dext_lat, buffer:buffer + dext_lon]
cs=plt.contourf(lons_f1, lats_f1, RMSE,v, transform=ccrs.PlateCarree(), cmap=plt.cm.terrain)
cb = plt.colorbar(cs)
cb.set_label('RMSE [K]', fontsize=20)
cb.ax.tick_params(labelsize=20)
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

plt.hlines(y=min(rlat_o), xmin=min(rlon_o), xmax=max(rlon_o), color='black',linestyles= 'dashed', linewidth=2)
plt.hlines(y=max(rlat_o), xmin=min(rlon_o), xmax=max(rlon_o), color='black',linestyles= 'dashed', linewidth=2)
plt.vlines(x=min(rlon_o), ymin=min(rlat_o), ymax=max(rlat_o), color='black',linestyles= 'dashed', linewidth=2)
plt.vlines(x=max(rlon_o), ymin=min(rlat_o), ymax=max(rlat_o), color='black',linestyles= 'dashed', linewidth=2)
plt.hlines(y=min(rlat_o[buffer:-buffer]), xmin=min(rlon_o[buffer:-buffer]), xmax=max(rlon_o[buffer:-buffer]), color='black', linewidth=4)
plt.hlines(y=max(rlat_o[buffer:-buffer]), xmin=min(rlon_o[buffer:-buffer]), xmax=max(rlon_o[buffer:-buffer]), color='black', linewidth=4)
plt.vlines(x=min(rlon_o[buffer:-buffer]), ymin=min(rlat_o[buffer:-buffer]), ymax=max(rlat_o[buffer:-buffer]), color='black', linewidth=4)
plt.vlines(x=max(rlon_o[buffer:-buffer]), ymin=min(rlat_o[buffer:-buffer]), ymax=max(rlat_o[buffer:-buffer]), color='black', linewidth=4)

Plot_CCLM(dir_mistral='/NETCDFS_CCLM/eobs/',name=name_2,bcolor='black',var=Vari,flag='FALSE',color_map='TRUE', alph=1, grids='FALSE', grids_color='red', rand_obs='TRUE', NN=NN)

xs, ys, zs = rp.transform_points(pc,
                                 np.array([-17, 105.0]),# Adjust for other domains!
                                 np.array([3, 60])).T   # Adjust for other domains!
ax.set_xlim(xs)
ax.set_ylim(ys)                                 
plt.ylim([min(rlat_o[buffer:-buffer]),max(rlat_o[buffer:-buffer])])
plt.xlim([min(rlon_o[buffer:-buffer]),max(rlon_o[buffer:-buffer])])  


#prs(PDF=DIR_exp+'Trash/'+pdf_name,vari="RMSE",VAL=RMSE,x=forecast.shape[1],y=forecast.shape[2])



plt.savefig(DIR_exp+'Trash/'+pdf_name)
plt.close()

# RMSE time-series

fig = plt.figure('2')
fig.set_size_inches(14, 10)
#plt.plot(RMSE_TIME_SERIES, 'o-', c='green')
#plt.xlabel('$time$', size=35)
plt.ylabel('$RMSE$', size=35)
plt.title('Boxplot of seasonal RMSEs averaged over the domain', size=30 , y=1.02)
#plt.ylim([0,.45])

names=DIR_exp+'Trash/'+pdf_name+str(member)+'_Analysis.csv'
with open(names, 'wb') as f:
     writer = csv.writer(f)
     writer.writerow(RMSE_TIME_SERIES)
#names_1 = '/home/fallah/Documents/DATA_ASSIMILATION/Bijan/CODES/CCLM/Python_Codes/historical_runs_yearly/src/TEMP/Figure08_RMSE_T_2M.pdf_Forecast.csv'
#fore = np.array(list(csv.reader(open(names_1,"rb"),delimiter=','))).astype('float')
plt.boxplot([RMSE_TIME_SERIES,RMSE_TIME_SERIES_Forecast.transpose(), ])
plt.xticks([1, 2], ['$Analysis$', '$Forecast$'], size=35)
#plt.ylim([0,.45])
plt.savefig(DIR_exp+'Trash/'+pdf_name + str(member)+'_ts.pdf')
plt.close()
