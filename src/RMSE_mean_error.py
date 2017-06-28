'''
Program to plot the changes of RMSE with respect to the changes in correlation length and number of observations
'''
# ============================== NAMELIST ======================================

month_length=10
SEAS1="JJA"
SEAS2="DJF"
NN=500
#COR_LEN=1
M=50 #Number of influential points
#DIR='/home/fallah/Documents/DATA_ASSIMILATION/Bijan/CODES/CCLM/Python_Codes/historical_runs_yearly/src/TEMP'
DIR1='/var/autofs/daten/cady/DATA_ASSIMILATION_TESTS_mean_of_error_JJA/OI_CCLM/src/test/1.0/20_'+SEAS1+'/'
DIR2='/var/autofs/daten/cady/DATA_ASSIMILATION_TESTS_mean_of_error_DJF/OI_CCLM/src/test/1.0/20_'+SEAS2+'/'
VAR='T_2M'
buffer = 20
# ===============================================================================

pdf_name= '/daten/cady/DATA_ASSIMILATION_TESTS_mean_of_error_JJA/RMSE_L_'+ '_' + str(month_length) + '_' + str(NN) + '_' + str(M) + '_' + '.pdf'
import numpy as np
import csv
import os
import os.path
from RMSE_MAPS_INGO import read_data_from_mistral as rdfm

from itertools import izip


from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
from CCLM_OUTS import Plot_CCLM
from RMSE_MAPS_INGO import read_data_from_mistral as rdfm
MAX_L=len(np.arange(0.0,1.01,0.01))
import pandas as pd
#res= np.zeros((16,50))
#res= np.zeros((7,50))
res1= np.zeros((7,MAX_L))
res2= np.zeros((7,MAX_L))
k=0
#for i in range(500,2100,100):

for i in range(500,600,100):
    kk=0
    for j in np.arange(0.0,1.01,0.01):
    #for j in ["0,1" ,  "0,4",  "0,7",  "1,0" ,  "1,3",  "1,6",  "1,9",  "2,11",  "2,41",  "2,71","3,1"]:
    #for j in ["0,01" ,  "0,06",  "0,11",  "0,16" ,  "0,21",  "0,26",  "0,31",  "0,36",  "0,41",  "0,46"]:
    #for j in ["0,1",  "0,2",  "0,3",  "0,4",  "0,5",  "0,6",  "0,7",  "0,8",  "0,9",  "1,0" ,  "1,1", "1,2",  "1,3",  "1,4",  "1,5",  "1,6",  "1,7",  "1,8",  "1,9",  "2,0" ,  "2,1",  "2,2", "2,3",  "2,4",  "2,5",  "2,6",  "2,7",  "2,8",  "2,9",  "3,0" ,  "3,1",  "3,2",  "3,3", "3,4",  "3,5",
     #         "3,6", "3,7",  "3,8",  "3,9",  "4,0" ,  "4,1",  "4,2",  "4,3",  "4,4",
     #         "4,5",  "4,6",  "4,7",  "4,8",  "4,9",  "5,0" ,  "5,1",  "5,2",  "5,3",  "5,4",  "5,5",
     #         "5,6",  "5,7",  "5,8",  "5,9",  "6,0" ]:
        
        #names = 'TEMP/RMSE_last_m_' + SEAS + '_' + str(M) + '_' + str(j) + '_' + str(i) + '.pdf.csv'
        
        names1 = DIR1 + 'test01_0.3_' + str(j) + '.0_1.7_' +  str(i) + '_19_1.0_20/Trash/RMSE_RMSE_ANALYSIS_' + SEAS1 + '_' + str(M) + '_1.7' + '_' + str(i) + '_'+ VAR + '_' +'19.pdf19.csv'
        if os.path.exists(names1):
            result1 = np.array(list(csv.reader(open(names1, "rb"), delimiter=','))).astype('float')
	else:
            names1 = DIR1 + 'test01_0.3_' + str(j) + '_1.7_' +  str(i) + '_19_1.0_20/Trash/RMSE_RMSE_ANALYSIS_' + SEAS1 + '_' + str(M) + '_1.7' + '_' + str(i) + '_'+ VAR + '_' +'19.pdf19.csv'
            result1 = np.array(list(csv.reader(open(names1, "rb"), delimiter=','))).astype('float') 
			
			
	names2 = DIR2 + 'test01_0.3_' + str(j) + '.0_2.1_' +  str(i) + '_19_1.0_20/Trash/RMSE_RMSE_ANALYSIS_' + SEAS2 + '_' + str(M) + '_2.1'  + '_' + str(i) + '_'+ VAR + '_' +'19.pdf19.csv' 
	if os.path.exists(names2):
            result2 = np.array(list(csv.reader(open(names2, "rb"), delimiter=','))).astype('float')
	else:
            names2 = DIR2 + 'test01_0.3_' + str(j) + '_2.1_' +  str(i) + '_19_1.0_20/Trash/RMSE_RMSE_ANALYSIS_' + SEAS2 + '_' + str(M) + '_2.1'  + '_' + str(i) + '_'+ VAR + '_' +'19.pdf19.csv' 
            result2 = np.array(list(csv.reader(open(names2, "rb"), delimiter=','))).astype('float')
		    
			
        
        
	
        res1[k,kk]=result1[0,1]
	res2[k,kk]=result2[0,1]
        
        kk=kk+1
    k=k+1

# ----- here read and import the forecast RMSE for JJA and DJF ----

Forecast_3_JJA = np.array(pd.read_csv(DIR1+'test01_0.3_5.0_1.7_500_19_1.0_20'+'/'+'Trash/SEASON_MEAN1' + '_' + SEAS1 + '.csv', header=None))#Reading the Forecast values JJA
Forecast_3_DJF = np.array(pd.read_csv(DIR2+'test01_0.3_5.0_2.1_500_19_1.0_20'+'/'+'Trash/SEASON_MEAN1' + '_' + SEAS2 + '.csv', header=None))#Reading the Forecast values DJF
t_f_JJA = np.zeros((month_length,Forecast_3_JJA.shape[0],Forecast_3_JJA.shape[1]))
t_f_DJF = t_f_JJA-t_f_JJA
for month in range(0, month_length):# Reading the ensemble forecast for each month!
    t_f_JJA[month,:,:] = pd.read_csv(DIR1+'test01_0.3_5.0_1.7_500_19_1.0_20'+'/'+'Trash/SEASON_MEAN' + str(month) + '_' + SEAS1 + '.csv', header=None)
    t_f_DJF[month,:,:] = pd.read_csv(DIR2+'test01_0.3_5.0_2.1_500_19_1.0_20'+'/'+'Trash/SEASON_MEAN' + str(month) + '_' + SEAS2 + '.csv', header=None)
t_f_JJA = np.array(t_f_JJA)
t_f_DJF = np.array(t_f_DJF)

name_1 = 'member_relax_3_big_00_' + VAR + '_ts_splitseas_1990_1999_' + SEAS1 + '.nc'
t_o_JJA, lat_o, lon_o, rlat_o, rlon_o =rdfm(dir='NETCDFS_CCLM/03/member_relax_3_big_00/post/',
                                        name=name_1,
                                        var=VAR)

name_2 = 'member_relax_3_big_00_' + VAR + '_ts_splitseas_1990_1999_' + SEAS2 + '.nc'
t_o_DJF, lat_o, lon_o, rlat_o, rlon_o =rdfm(dir='NETCDFS_CCLM/03/member_relax_3_big_00/post/',
                                        name=name_2,
                                        var=VAR)

dext_lon = t_o_DJF.shape[2] - (2 * buffer)
dext_lat = t_o_DJF.shape[1] - (2 * buffer)
start_lon=(buffer+4)
start_lat=(buffer-4)

obs_JJA = t_o_JJA[0:10, buffer:buffer + dext_lat, buffer:buffer + dext_lon]
RMSE_TIME_SERIES_Forecast_JJA=np.zeros(obs_JJA.shape[0])
obs_DJF = t_o_DJF[0:10, buffer:buffer + dext_lat, buffer:buffer + dext_lon]
RMSE_TIME_SERIES_Forecast_DJF=np.zeros(obs_DJF.shape[0])

for i in range(0,obs_JJA.shape[0]):
    print i	
    forecast_orig_ts_JJA=np.squeeze(t_f_JJA[i,:,:])
    obs_resh_ts_JJA=np.squeeze(obs_JJA[i,:,:])
    RMSE_TIME_SERIES_Forecast_JJA[i] = mean_squared_error(obs_resh_ts_JJA, forecast_orig_ts_JJA) ** 0.5 #Calculating RMSEs for each month for forecast
    forecast_orig_ts_DJF=np.squeeze(t_f_DJF[i,:,:])
    obs_resh_ts_DJF=np.squeeze(obs_DJF[i,:,:])
    RMSE_TIME_SERIES_Forecast_DJF[i] = mean_squared_error(obs_resh_ts_DJF, forecast_orig_ts_DJF) ** 0.5
    	
   # print np.max(obs_resh_ts[:,1]),np.max(forecast_orig_ts_JJA[:,1])
# ----- ------------------------------------------------------ ----



import matplotlib.pyplot as plt

fig, ax = plt.subplots()
fig.set_size_inches(14, 10)
#for i in range(16):
x=np.arange(0.0,1.01,0.01)
i=0
#for i in range(7):
#    ax.plot(x,res[i,:],'o-', label=str(i*100+500), lw=3, alpha=.7, ms=10)
#    ax.legend(loc='upper center', shadow=True)
ax.plot(x,res1[i,],'rd-', label=str("JJA"), lw=3, ms=10, alpha=.5)
ax.plot(2,np.mean(RMSE_TIME_SERIES_Forecast_JJA),'kd')
print RMSE_TIME_SERIES_Forecast_JJA
ax.plot(x,res2[i,],'bo-', label=str("DJF"), lw=3, ms=10, alpha=.5)
ax.plot(2,np.mean(RMSE_TIME_SERIES_Forecast_DJF),'ko')
#ax.boxplot(RMSE_TIME_SERIES_Forecast_DJF)
plt.legend(loc=4, shadow=False,fontsize=32)
#if SEAS == 'DJF':
#ax.plot(x[16],min(res1[0,:]),'r*', label=str(500), lw=3,  ms=20) # JJA
#else:
#ax.plot(x[20],min(res2[0,:]),'b*', label=str(500), lw=3,  ms=20) # DJF

ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.set_title("", y=1.05)
ax.set_ylabel(r"$RMSE$", labelpad=5,size=32)
ax.set_xlabel(r"$\sigma_{Obs. Err.}$", labelpad=5,size=32)

#plt.xlim(0,(6.2))
#plt.ylim(0.12,(0.2))
#if SEAS == 'DJF':
 #   plt.ylim(0.6,1.4) #DJF
#else:
 #   plt.ylim(0.22,0.26) #JJA
plt.tick_params(axis='both', which='major', labelsize=22)
plt.savefig(pdf_name)
plt.close()
