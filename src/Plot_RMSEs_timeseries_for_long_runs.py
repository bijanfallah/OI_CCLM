# Program to plot the RMSEs time-series of Forecast quantities for each member
# ------------------------ Import----------------------------------------------
from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import sem
from RMSE_MAPS_INGO import read_data_from_mistral as rdfm
# -----------------------------------------------------------------------------

# ------------------------ Namelist -------------------------------------------

NN=500
#SEAS='DJF'
SEAS='JJA'
Vari   = 'T_2M'
#Vari   = 'TOT_PREC'
month_length=30   # number of the seasons (years)
start_time=0
here = "."+"/"
no_members=4
buffer=20

# -----------------------------------------------------------------------------
name_2 = 'member_relax_3_big_00_' + Vari + '_ts_splitseas_1979_2010_' + SEAS + '.nc'
t_o, lat_o, lon_o, rlat_o, rlon_o =rdfm(dir='NETCDFS_CCLM/03/member_relax_3_big_00/post/', # the observation (default run without shifting)
                                            name=name_2,
                                            var=Vari)
name_2 = 'member_relax_1_big_04_' + Vari + '_ts_splitseas_1979_2010_' + SEAS + '.nc'
t_1, lat_1, lon_1, rlat_1, rlon_1 =rdfm(dir='NETCDFS_CCLM/01/member_relax_1_big_04/post/', 
                                            name=name_2,
                                            var=Vari)
name_2 = 'member_relax_2_big_04_' + Vari + '_ts_splitseas_1979_2010_' + SEAS + '.nc'
t_2, lat_2, lon_2, rlat_2, rlon_2 =rdfm(dir='NETCDFS_CCLM/02/member_relax_2_big_04/post/', 
                                            name=name_2,
                                            var=Vari)
name_2 = 'member_relax_3_big_04_' + Vari + '_ts_splitseas_1979_2010_' + SEAS + '.nc'
t_3, lat_3, lon_3, rlat_3, rlon_3 =rdfm(dir='NETCDFS_CCLM/03/member_relax_3_big_04/post/', 
                                            name=name_2,
                                            var=Vari)
name_2 = 'member_relax_4_big_04_' + Vari + '_ts_splitseas_1979_2010_' + SEAS + '.nc'
t_4, lat_4, lon_4, rlat_4, rlon_4 =rdfm(dir='NETCDFS_CCLM/04/member_relax_4_big_04/post/', 
                                            name=name_2,
                                            var=Vari)



time_series = np.zeros((month_length,no_members))
time_series_min    = np.zeros(month_length)
time_series_max    = np.zeros(month_length)
time_series_mean   = np.zeros(month_length)
time_series_Nature = np.zeros(month_length)
#for ii in range(0,month_length):
#    counter = 0
#    for kk in range(1,6):
#        for jj in range(1,5):
#            if counter < no_members:
#                dumm2 = genfromtxt(here+'NAMES'+'/'+"Trash/Forecast_" + str(ii) +"_" + str(jj) + "_"+ str(kk) + "_" + SEAS + ".csv", delimiter=",")
#                time_series[ii,counter] = np.mean(dumm2)
#            counter = counter + 1

dext_lon = np.array(t_o.shape[2] - (2 * buffer))
dext_lat = np.array(t_o.shape[1] - (2 * buffer))
print buffer, t_o.shape, t_1.shape
#print dext_lon+buffer, dext_lat+buffer

#print(t_1.reshape(t_1.shape[0],t_1.shape[1]*t_1.shape[2]).mean(axis=1))
d0 = t_1[:,buffer+4:buffer+4+ dext_lat, buffer-4:buffer-4+ dext_lon].shape[0]
d1 = t_1[:,buffer+4:buffer+4+ dext_lat, buffer-4:buffer-4+ dext_lon].shape[1]
d2 = t_1[:,buffer+4:buffer+4+ dext_lat, buffer-4:buffer-4+ dext_lon].shape[2]
time_series[:,0]   =   np.mean(t_1[:,buffer+4:buffer+4+ dext_lat, buffer-4:buffer-4+ dext_lon].reshape(d0,d1*d2),axis=1)
time_series[:,1]   =   np.mean(t_2[:,buffer-4:buffer-4+ dext_lat, buffer-4:buffer-4+ dext_lon].reshape(d0,d1*d2),axis=1)
time_series[:,2]   =   np.mean(t_3[:,buffer-4:buffer-4+ dext_lat, buffer+4:buffer+4+ dext_lon].reshape(d0,d1*d2),axis=1)
time_series[:,3]   =   np.mean(t_4[:,buffer+4:buffer+4+ dext_lat, buffer+4:buffer+4+ dext_lon].reshape(d0,d1*d2),axis=1)
time_series_Nature = np.mean(t_o[:,buffer:buffer + dext_lat, buffer:buffer + dext_lon].reshape(d0,d1*d2),axis=1)
time = range(1,month_length +1)
time_series_mean = np.mean(time_series,1)
time_series_max  = np.max(time_series,1) 
time_series_min  = np.min(time_series,1)

# ------------ ploting -------------------------------------------------------
from pylab import *
fig = plt.figure(111)
fig.set_size_inches(14, 10)
plt.fill_between(time, time_series_max,
                 time_series_min, color='darkgray') #color="#3F5D7D")
plt.plot(time, time_series_mean, color="black", lw=2, alpha=0.7)
plt.plot(time, time_series_Nature, color="black",linestyle='--',dashes=(5, 2), lw=2)
plt.xlabel("Time", fontsize=30,fontname="Times New Roman")
plt.ylabel(Vari, fontsize=30,fontname="Times New Roman")
plt.tick_params(axis='both', which='major', labelsize=10)
xlim([.5,month_length+0.5])
#fig.set_xticklabels(tick_labels.astype(int))
plt.savefig(here+''+"Time_series_"+Vari+'_'+SEAS+".pdf", bbox_inches="tight");
plt.close()
