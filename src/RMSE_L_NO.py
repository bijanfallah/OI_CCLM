'''
Program to plot the changes of RMSE with respect to the changes in correlation length and number of observations
'''
# ============================== NAMELIST ======================================
MAX_L=60
month_length=30
SEAS1="JJA"
SEAS2="DJF"
NN=500
#COR_LEN=1
M=50 #Number of influential points
#DIR='/home/fallah/Documents/DATA_ASSIMILATION/Bijan/CODES/CCLM/Python_Codes/historical_runs_yearly/src/TEMP'
DIR1='/scratch/users/fallah/exp00_cor_length/1.0/20_'+SEAS1+'/'
DIR2='/scratch/users/fallah/exp00_cor_length/1.0/20_'+SEAS2+'/'
VAR='T_2M'
# ===============================================================================

pdf_name= '/scratch/users/fallah/exp00_cor_length/1.0/RMSE_L_'+ '_' + str(month_length) + '_' + str(NN) + '_' + str(M) + '_' + '.pdf'
import numpy as np
import csv
import os
#res= np.zeros((16,50))
#res= np.zeros((7,50))
res1= np.zeros((7,MAX_L))
res2= np.zeros((7,MAX_L))
k=0
#for i in range(500,2100,100):

for i in range(500,600,100):
    kk=0
    #for j in np.arange(0.1,3,0.3):
    #for j in ["0,1" ,  "0,4",  "0,7",  "1,0" ,  "1,3",  "1,6",  "1,9",  "2,11",  "2,41",  "2,71","3,1"]:
    #for j in ["0,01" ,  "0,06",  "0,11",  "0,16" ,  "0,21",  "0,26",  "0,31",  "0,36",  "0,41",  "0,46"]:
    for j in ["0,1",  "0,2",  "0,3",  "0,4",  "0,5",  "0,6",  "0,7",  "0,8",  "0,9",  "1,0" ,  "1,1", "1,2",  "1,3",  "1,4",  "1,5",  "1,6",  "1,7",  "1,8",  "1,9",  "2,0" ,  "2,1",  "2,2", "2,3",  "2,4",  "2,5",  "2,6",  "2,7",  "2,8",  "2,9",  "3,0" ,  "3,1",  "3,2",  "3,3", "3,4",  "3,5",
              "3,6", "3,7",  "3,8",  "3,9",  "4,0" ,  "4,1",  "4,2",  "4,3",  "4,4",
              "4,5",  "4,6",  "4,7",  "4,8",  "4,9",  "5,0" ,  "5,1",  "5,2",  "5,3",  "5,4",  "5,5",
              "5,6",  "5,7",  "5,8",  "5,9",  "6,0" ]:
        
        #names = 'TEMP/RMSE_last_m_' + SEAS + '_' + str(M) + '_' + str(j) + '_' + str(i) + '.pdf.csv'
        names1 = DIR1 + 'Sensitivity_no_members_' + str(j) + '_' +  str(i) + '_19_1.0_20/Trash/RMSE_RMSE_ANALYSIS_' + SEAS1 + '_' + str(M) + '_' + str(j) + '_' + str(i) + '_'+ VAR + '_' +'19.pdf19.csv'
        
        names2 = DIR2 + 'Sensitivity_no_members_' + str(j) + '_' +  str(i) + '_19_1.0_20/Trash/RMSE_RMSE_ANALYSIS_' + SEAS2 + '_' + str(M) + '_' + str(j) + '_' + str(i) + '_'+ VAR + '_' +'19.pdf19.csv' 
        
        result1 = np.array(list(csv.reader(open(names1, "rb"), delimiter=','))).astype('float')
	result2 = np.array(list(csv.reader(open(names2, "rb"), delimiter=','))).astype('float')
        res1[k,kk]=result1[0,1]
	res2[k,kk]=result2[0,1]
        
        kk=kk+1
    k=k+1



import matplotlib.pyplot as plt

fig, ax = plt.subplots()
fig.set_size_inches(14, 10)
#for i in range(16):
x=np.arange(.1,6.1,.1)
i=0
#for i in range(7):
#    ax.plot(x,res[i,:],'o-', label=str(i*100+500), lw=3, alpha=.7, ms=10)
#    ax.legend(loc='upper center', shadow=True)
ax.plot(x,res1[i,],'rd-', label=str("JJA"), lw=3, ms=10, alpha=.5)
ax.plot(x,res2[i,],'bo-', label=str("DJF"), lw=3, ms=10, alpha=.5)
plt.legend(loc=4, shadow=False,fontsize=32)
#if SEAS == 'DJF':
#ax.plot(x[16],min(res1[0,:]),'r*', label=str(500), lw=3,  ms=20) # JJA
#else:
#ax.plot(x[20],min(res2[0,:]),'b*', label=str(500), lw=3,  ms=20) # DJF

ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.set_title("", y=1.05)
ax.set_ylabel(r"$RMSE$", labelpad=5,size=32)
ax.set_xlabel(r"$L$", labelpad=5,size=32)

plt.xlim(0,(6.2))
#if SEAS == 'DJF':
 #   plt.ylim(0.6,1.4) #DJF
#else:
 #   plt.ylim(0.22,0.26) #JJA
plt.tick_params(axis='both', which='major', labelsize=22)
plt.savefig(pdf_name)
plt.close()
