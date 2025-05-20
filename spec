#!/bin/bash
###############################################################################
#     Script to Create or Active Supplier/Site in the SpecRight               #
#     Data:    May 2025                                                       #
#     Author : TCS                                                            #
#     Notes:                                                                  #
###############################################################################


###############################################################################
#    Step 1 : Run the JPO 
###############################################################################

VDATE=`date +%Y-\%m-\%d_\%H.\%M`
cronStartDate=`date`
FileDynamics=`date +%Y\%m\%d`

# get the directory the script file resides
BASEDIR=$(dirname "$0")

# write the script start date time stamp 
echo "-------------------------------- CRON RUN DETAILS ---------------------------------"
echo "Run Started At   : $cronStartDate "
echo "Base Folder At   : $BASEDIR "

#------------------------------------------------------------------------------
#    Step 1A : Read the config file entries for MQL connection
#------------------------------------------------------------------------------
export BootStrap=`grep BootStrap /apps/Aniket/Shell/Script/TRUDataLoader.config | cut -d "=" -f2`
export mqlUser=`grep mqlUser /apps/Aniket/Shell/Script/TRUDataLoader.config | cut -d "=" -f2`
export mqlPwd=`grep mqlPwd /apps/Aniket/Shell/Script/TRUDataLoader.config | cut -d "=" -f2`
export START_DATE=`grep START_DATE /apps/Aniket/Shell/Script/TRUDataLoader.config | cut -d "=" -f2`

echo "$BootStrap"
echo "$mqlUser"
echo "$mqlPwd"

mql -c "verb on; set context user creator pass Tru@2018x; temp query bus \"Business Unit\" * * where \"originated > '$START_DATE' && current=='Active'\" select id dump |;"

