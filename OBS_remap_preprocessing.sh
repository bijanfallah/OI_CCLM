#!/bin/bash
set -ex
dir='/home/bijan/Downloads'
cdo seasmean -daymean $dir/tg_0.44deg_rot_v15.0.nc tg_0.44deg_rot_v15.0
cdo splitseas tg_0.44deg_rot_v15.0 tg_0.44deg_rot_v15.0_
rm -f tg_0.44deg_rot_v15.0
cdo selyear,1979/2015 tg_0.44deg_rot_v15.0_DJF.nc tg_0.44deg_rot_v15.0_DJF_1979_2015.nc
cdo selyear,1979/2015 tg_0.44deg_rot_v15.0_JJA.nc tg_0.44deg_rot_v15.0_JJA_1979_2015.nc
rm -f tg_0.44deg_rot_v15.0_???.nc

cdo remapbil,grids tg_0.44deg_rot_v15.0_JJA_1979_2015.nc tg_0.44deg_rot_v15.0_JJA_1979_2015_remapbil.nc
cdo remapbil,grids tg_0.44deg_rot_v15.0_DJF_1979_2015.nc tg_0.44deg_rot_v15.0_DJF_1979_2015_remapbil.nc
rm -f tg_0.44deg_rot_v15.0_???_1979_2015.nc
echo 'finished remapping'

