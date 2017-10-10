# Program to show the maps of RMSE averaged over time
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import os
from netCDF4 import Dataset as NetCDFFile
import numpy as np
from CCLM_OUTS import Plot_CCLM
# option == 1 ->  shift 4 with default cclm domain and nboundlines = 3
# option == 2 ->  shift 4 with smaller cclm domain and nboundlines = 3
# option == 3 ->  shift 4 with smaller cclm domain and nboundlines = 6
# option == 4 ->  shift 4 with corrected smaller cclm domain and nboundlines = 3
# option == 5 ->  shift 4 with corrected smaller cclm domain and nboundlines = 4
# option == 6 ->  shift 4 with corrected smaller cclm domain and nboundlines = 6
# option == 7 ->  shift 4 with corrected smaller cclm domain and nboundlines = 9
# option == 8 ->  shift 4 with corrected bigger cclm domain and nboundlines = 3
from CCLM_OUTS import Plot_CCLM
#def f(x):
#   if x==-9999:
#      return float('NaN')
#   else:
#      return x
def read_data_from_mistral(dir='/work/bb1029/b324045/work1/work/member/post/',name='member_T_2M_ts_seasmean.nc',var='T_2M'):
    # type: (object, object, object) -> object
    #a function to read the data from mistral work

    """

    :rtype: object
    """
    #CMD = 'scp $mistral:' + dir + name + ' ./'
    CMD = 'wget users.met.fu-berlin.de/~BijanFallah/' + dir + name
    os.system(CMD)
    nc = NetCDFFile(name)
#    for name2, variable in nc.variables.items():
#        for attrname in variable.ncattrs():
#                    print(name2, variable, '-----------------',attrname)
#                    #print("{} -- {}".format(attrname, getattr(variable, attrname)))
    os.remove(name)
    lats = nc.variables['lat'][:]
    lons = nc.variables['lon'][:]
    t = nc.variables[var][:].squeeze()
    rlats = nc.variables['rlat'][:]  # extract/copy the data
    rlons = nc.variables['rlon'][:]
    #f2 = np.vectorize(f)
    #t= f2(t)
    #t=t.data
    t=t.squeeze()
    #print()
    nc.close()

    return(t, lats, lons, rlats, rlons)

