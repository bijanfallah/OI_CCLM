#!/bin/bash

# ======================================================================================================================
# .______    __         __       ___      .__   __.     _______    ___       __       __          ___       __    __
# |   _  \  |  |       |  |     /   \     |  \ |  |    |   ____|  /   \     |  |     |  |        /   \     |  |  |  |
# |  |_)  | |  |       |  |    /  ^  \    |   \|  |    |  |__    /  ^  \    |  |     |  |       /  ^  \    |  |__|  |
# |   _  <  |  | .--.  |  |   /  /_\  \   |  . `  |    |   __|  /  /_\  \   |  |     |  |      /  /_\  \   |   __   |
# |  |_)  | |  | |  `--'  |  /  _____  \  |  |\   |    |  |    /  _____  \  |  `----.|  `----./  _____  \  |  |  |  |
# |______/  |__|  \______/  /__/     \__\ |__| \__|    |__|   /__/     \__\ |_______||_______/__/     \__\ |__|  |__|
#
#                                                info@bijan-fallah.com
# ======================================================================================================================


set -ex
# ====================================== NAMELIST ======================================================================
month_length=36
SEAS="JJA"
#SEAS="DJF"
NN=100
Var='T_2M'
#Var='TOT_PREC'
#COR_LEN=1
M=50 #Number of influential points
# path to the optiminterp exe files:
DIR_python='/scratch/users/fallah/OI_EOBS/OI_CCLM/src/'
# path to the codes:
DIR_OI='/scratch/users/fallah/OI_EOBS/OI_CCLM/inst/'
no_members=4 #----
buffer=20
inflation=1.0
# path to the work directory:
DIR_WORK='/daten/cady/EOBS/'
#std_err=0.1 # Standard deviation of the observation error (white noise)
mean_err=0.0 # mean of the observation error (white noise)
SNR=3 #

std_err=$(python -c "print((1.113/${SNR})**0.5)")
echo $std_err
first_name='EOBS_'${SNR}_${mean_err}

# ================================================================================================
if [ ! -d "${DIR_WORK}" ]; then
  mkdir ${DIR_WORK}
fi
if [ $SEAS = "DJF" ];then 
   COR_LEN=2.1
fi
if [ $SEAS = "JJA" ]; then
   COR_LEN=1.7 
fi
         

if [ ! -d "${DIR_WORK}${inflation}" ]; then
  mkdir ${DIR_WORK}${inflation}
fi

if [ ! -d "${DIR_WORK}${inflation}/${no_members}_${SEAS}" ]; then
  mkdir ${DIR_WORK}${inflation}/${no_members}_${SEAS}
fi
if [ ! -d "${DIR_WORK}${inflation}/${no_members}_${SEAS}/final_plot" ]; then
  mkdir ${DIR_WORK}${inflation}/${no_members}_${SEAS}/final_plot
fi

DIR_WORK=${DIR_WORK}/${inflation}/${no_members}_${SEAS}/
while [ $NN -lt 5001 ]; do
# COR_LEN=1
# while [ $COR_LEN -lt 20 ]; do
     member=3    # -------------------------------------------------------
     while [ $member -lt $no_members ]; do
         NAME=${first_name}
         NAME_it=${NAME}_${COR_LEN}_${NN}_
         NAME=${NAME}_${COR_LEN}_${NN}_${member}_${inflation}_${no_members}

         if [ ! -d "${DIR_WORK}${NAME}" ]; then
          mkdir ${DIR_WORK}${NAME}
         fi
         cp ${DIR_python}/*py ${DIR_WORK}${NAME}/
         cp ${DIR_python}/Plot_final_results.py ${DIR_WORK}/
         cp ${DIR_python}/CCLM_OUTS.py ${DIR_WORK}/
         cp ${DIR_python}/RMSE_MAPS_INGO.py ${DIR_WORK}/
         cp ${DIR_python}/rotgrid.py ${DIR_WORK}/
         cp ${DIR_python}/Plot_RMSEs_timeseries.py ${DIR_WORK}/
         cp -rf ${DIR_OI} ${DIR_WORK}${NAME}/
         XX="$DIR_WORK$NAME/Stations$NAME"

         # ===========================================   MAKE PSEUDO  ======================================================
         sed -i "s/NN=600/NN=$NN/g" ${DIR_WORK}${NAME}/make_pseudo_obs.py
         echo $SEAS
         sed -i "s/DJF/$SEAS/g" ${DIR_WORK}${NAME}/make_pseudo_obs.py
         sed -i "s/month_length=20/month_length=$month_length/g" ${DIR_WORK}${NAME}/make_pseudo_obs.py
         sed -i "s/T_2M/$Var/g" ${DIR_WORK}${NAME}/make_pseudo_obs.py
         sed -i "s/buffer=20/buffer=$buffer/g" ${DIR_WORK}${NAME}/make_pseudo_obs.py
         sed -i "s/NO=20/NO=$no_members/g" ${DIR_WORK}${NAME}/make_pseudo_obs.py
         var1=$(echo "path_dir")
         #var1=$(echo ${DIR_python})
         var2=$(echo ${DIR_WORK}${NAME})
         sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/make_pseudo_obs.py
         sed -i "s/.3, month_length/$std_err, month_length/g" ${DIR_WORK}${NAME}/make_pseudo_obs.py
	 sed -i "s/.normal(0/.normal($mean_err/g" ${DIR_WORK}${NAME}/make_pseudo_obs.py
         # ========================================== END MEKE PSEUDO ======================================================

         # ======================================= Create INPUT FILES ======================================================
         sed -i "s/T_2M/$Var/g" ${DIR_WORK}${NAME}/Create_Input_FIles.py
         sed -i "s/NN=1000#number/NN=$NN#number/g" ${DIR_WORK}${NAME}/Create_Input_FIles.py
         sed -i "s/month_length=20/month_length=$month_length/g" ${DIR_WORK}${NAME}/Create_Input_FIles.py
         sed -i "s/"DJF"/"$SEAS"/g" ${DIR_WORK}${NAME}/Create_Input_FIles.py
         sed -i "s/members=20/members=$no_members/g" ${DIR_WORK}${NAME}/Create_Input_FIles.py
         var1=$(echo "path_dir")
         #var1=$(echo ${DIR_python})
         var2=$(echo ${DIR_WORK}${NAME})
         sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/Create_Input_FIles.py
         sed -i "s/inflation=1.0/inflation=$inflation/g" ${DIR_WORK}${NAME}/Create_Input_FIles.py
         # ====================================  END Create INPUT FILES  ===================================================


         #sed -i "s/NN=500);/NN=$NN);/g" ${DIR_WORK}/${NAME}/CCLM_OUTS.py
         sed -i "s/'RMSE_Patterns_'/'RMSE_Patterns_$NAME'/g" ${DIR_WORK}${NAME}/RMSE_MAPS_INGO.py

         sed -i "s/month_length=20/month_length=$month_length/g" ${DIR_WORK}${NAME}/RMSE_MAPS_INGO.py
         sed -i "s/"DJF"/"$SEAS"/g" ${DIR_WORK}${NAME}/RMSE_MAPS_INGO.py

         sed -i "s/Stations/Stations$NAME/g" ${DIR_WORK}${NAME}/PLOT_Stations.py


         sed -i "s/T_2M/$Var/g" ${DIR_WORK}${NAME}/PLOT_Stations.py


         sed -i "s/T_2M/$Var/g" ${DIR_WORK}${NAME}/run_octave.py
         sed -i "s/T_2M/$Var/g" ${DIR_WORK}${NAME}/RMSE_MAPS_INGO.py

         if [ ${Var} = 'TOT_PREC' ];then
            sed -i "s/[K]/mm/g" ${DIR_WORK}${NAME}/RMSE_MAPS_INGO.py

         fi


         sed -i "s/NN=1000/NN=$NN/g" ${DIR_WORK}${NAME}/PLOT_Stations.py
         sed -i "s/DJF/$SEAS/g" ${DIR_WORK}${NAME}/run_octave.py
         sed -i "s/NN=1000#number/NN=$NN#number/g" ${DIR_WORK}${NAME}/run_octave.py
         sed -i "s/month_length=20/month_length=$month_length/g" ${DIR_WORK}${NAME}/run_octave.py
         var1=$(echo "path_oi")
         var2=$(echo ${DIR_WORK}${NAME}/inst/)
         sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/run_octave.py
		 var1=$(echo "path_dir")
         #var1=$(echo ${DIR_python})
         var2=$(echo ${DIR_WORK}${NAME})
         sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/run_octave.py

         sed -i "s/member=0/member=$member/g" ${DIR_WORK}${NAME}/run_octave.py
         sed -i "s/'last_m100_l20/'RMSE_ANALYSIS_${SEAS}_${M}_${COR_LEN}_${NN}_${Var}/g" ${DIR_WORK}${NAME}/run_octave.py
         sed -i "s/buffer=20/buffer=$buffer/g" ${DIR_WORK}${NAME}/run_octave.py


         # ------------------------------------------  Plot_final_results.py -------------------------------------------
         sed -i "s/T_2M/$Var/g" ${DIR_WORK}/Plot_final_results.py
         sed -i "s/DJF/$SEAS/g" ${DIR_WORK}/Plot_final_results.py
         sed -i "s/NN=1000#number/NN=$NN#number/g" ${DIR_WORK}/Plot_final_results.py
         sed -i "s/month_length=20/month_length=$month_length/g" ${DIR_WORK}/Plot_final_results.py
         var1=$(echo ${DIR_OI}optiminterp/inst/)
         var2=$(echo ${DIR_WORK}/optiminterp/inst/)
         sed -i "s%$var1%$var2%g" ${DIR_WORK}/Plot_final_results.py
         var1=$(echo "python_dir")
         #var1=$(echo ${DIR_python})
         var2=$(echo ${DIR_WORK})
         sed -i "s%$var1%$var2%g" ${DIR_WORK}/Plot_final_results.py
         sed -i "s/no_members=20/no_members=$no_members/g" ${DIR_WORK}/Plot_final_results.py
         sed -i "s/'last_m100_l20/'RMSE_ANALYSIS_${SEAS}_${M}_${COR_LEN}_${NN}_${Var}/g" ${DIR_WORK}/Plot_final_results.py
         sed -i "s/buffer=20/buffer=$buffer/g" ${DIR_WORK}/Plot_final_results.py
         sed -i "s/NAMES/${NAME}/g" ${DIR_WORK}/Plot_final_results.py
         n="333333"
         var1=$(echo ${n})
         var2=$(echo ${DIR_WORK}${NAME_it})
         sed -i "s%$var1%$var2%g" ${DIR_WORK}/Plot_final_results.py
         
         n="path_dir"
         var1=$(echo ${n})
         var2=$(echo ${DIR_WORK}/)
         sed -i "s%$var1%$var2%g" ${DIR_WORK}/Plot_final_results.py
         
         
         
         sed -i "s/inflation=1.1/inflation=$inflation/g" ${DIR_WORK}/Plot_final_results.py

         #------------------------------------------- Plot_RMSEs_timeseries.py -----------------------------------------
         sed -i "s/T_2M/$Var/g" ${DIR_WORK}/Plot_RMSEs_timeseries.py
         sed -i "s/DJF/$SEAS/g" ${DIR_WORK}/Plot_RMSEs_timeseries.py
         sed -i "s/month_length=20/month_length=$month_length/g" ${DIR_WORK}/Plot_RMSEs_timeseries.py
         sed -i "s/no_members=20/no_members=$no_members/g" ${DIR_WORK}/Plot_RMSEs_timeseries.py
         var1=$(echo "path_dir")
         #var1=$(echo ${DIR_python})
         var2=$(echo ${DIR_WORK})
         sed -i "s%$var1%$var2%g" ${DIR_WORK}/Plot_RMSEs_timeseries.py
         sed -i "s/NAMES/${NAME}/g" ${DIR_WORK}/Plot_RMSEs_timeseries.py
         sed -i "s/buffer=20/buffer=$buffer/g" ${DIR_WORK}/Plot_RMSEs_timeseries.py
         #------------------------------------------- run_IO.m -------------------------------------------------------------
         
         
         sed -i "s/lenx = 20;/lenx = $COR_LEN/g" ${DIR_WORK}${NAME}/inst/run_IO.m
         sed -i "s/leny = 20;/leny = $COR_LEN/g" ${DIR_WORK}${NAME}/inst/run_IO.m
         sed -i "s/m    = 50/m    = $M/g" ${DIR_WORK}${NAME}/inst/run_IO.m
         var1=$(echo "python_dir")
         #var1=$(echo ${DIR_python})
         var2=$(echo ${DIR_WORK}${NAME})
         sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/inst/run_IO.m
         month=`expr $month_length - 1`
         sed -i "s/i=0:11/i=0:$month/g" ${DIR_WORK}${NAME}/inst/run_IO.m
         #sed -i "s/historical_runs/historical_runs_yearly_ensemble/g" ${DIR_WORK}${NAME}/optiminterp/inst/run_IO.m
         sed -i "s/INPUT.csv/INPUT${member}.csv/g" ${DIR_WORK}${NAME}/inst/run_IO.m
         sed -i "s/'fi'/'fi${member}'/g" ${DIR_WORK}${NAME}/inst/run_IO.m
         sed -i "s/'vari'/'vari${member}'/g" ${DIR_WORK}${NAME}/inst/run_IO.m

         # ====================================    Plot_RMSE_SPREAD_main.py ============================================
         sed -i "s/T_2M/$Var/g" ${DIR_WORK}${NAME}/Plot_RMSE_SPREAD_main.py
         sed -i "s/NN=1000#number/NN=$NN#number/g" ${DIR_WORK}${NAME}/Plot_RMSE_SPREAD_main.py
         sed -i "s/timesteps=10/timesteps=$month_length/g" ${DIR_WORK}${NAME}/Plot_RMSE_SPREAD_main.py
         sed -i "s/DJF/$SEAS/g" ${DIR_WORK}${NAME}/Plot_RMSE_SPREAD_main.py
         sed -i "s/buffer=20/buffer=$buffer/g" ${DIR_WORK}${NAME}/Plot_RMSE_SPREAD_main.py
		 var1=$(echo "path_dir")
         #var1=$(echo ${DIR_python})
         var2=$(echo ${DIR_WORK}${NAME})
         sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/Plot_RMSE_SPREAD_main.py

         sed -i "s/no_members=20/no_members=$no_members/g" ${DIR_WORK}${NAME}/Plot_RMSE_SPREAD_main.py

         # ===============================================================================================
         # ==============================  Python calls: =================================================

         #python ${DIR_WORK}${NAME}/PLOT_Stations.py
         python2 ${DIR_WORK}${NAME}/Plot_RMSE_SPREAD_main.py
         python2 ${DIR_WORK}${NAME}/make_pseudo_obs.py
         python2 ${DIR_WORK}${NAME}/Create_Input_FIles.py
         python2 ${DIR_WORK}${NAME}/run_octave.py
         

         # ===============================================================================================
         

         member=`expr $member + 1`
     done
  #   python2 ${DIR_WORK}/Plot_final_results.py # Plot final results
  #  python ${DIR_WORK}/Plot_RMSEs_timeseries.py
#     COR_LEN=`expr $COR_LEN + 1`
#     echo ${COR_LEN}
# done

  	NN=`expr $NN + 100`
    echo $NN
done





