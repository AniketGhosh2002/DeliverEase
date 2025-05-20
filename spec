#!/bin/bash
###############################################################################
#     Script to Create or Active Supplier/Site in the SpecRight               #
#     Data:    May 2025                                                       #
#     Author : TCS                                                            #
#     Notes:                                                                  #
###############################################################################

VDATE=`date +%Y-\%m-\%d_\%H.\%M`
cronStartDate=`date`
FileDynamics=`date +%Y\%m\%d`

BASEDIR=$(dirname "$0")

echo "-------------------------------- CRON RUN DETAILS ---------------------------------"
echo "Run Started At   : $cronStartDate "
echo "Base Folder At   : $BASEDIR "

#------------------------------------------------------------------------------
#    Step 1 : Read the config file entries for MQL connection
#------------------------------------------------------------------------------
export BootStrap=`grep BootStrap /apps/Aniket/Shell/Script/TRUDataLoader.config | cut -d "=" -f2`
export mqlUser=`grep mqlUser /apps/Aniket/Shell/Script/TRUDataLoader.config | cut -d "=" -f2`
export mqlPwd=`grep mqlPwd /apps/Aniket/Shell/Script/TRUDataLoader.config | cut -d "=" -f2`
export START_DATE=`grep START_DATE /apps/Aniket/Shell/Script/TRUDataLoader.config | cut -d "=" -f2`

echo "$BootStrap"
echo "$mqlUser"
echo "$mqlPwd"

mql -c "verb on; set context user creator pass Tru@2018x; temp query bus \"Business Unit\" * * where \"originated > '$START_DATE' && current=='Active'\" select id dump |;"

#------------------------------------------------------------------------------
#    Step 2: Capture the IDs of Business Units created after START_DATE
#------------------------------------------------------------------------------
echo "Fetching IDs of Business Units..."

id_output=$(mql -c "set context user creator pass Tru@2018x; temp query bus \"Business Unit\" * * where \"originated > '$START_DATE' && current=='Active'\" select id dump |;")

ids=$(echo "$id_output" | awk -F"|" '{print $4}' | grep -v "^$")

echo "Found IDs:"
echo "$ids"

#------------------------------------------------------------------------------
# Step 3: Loop through each ID and call the JPO method
#------------------------------------------------------------------------------
echo "Starting JPO Execution for each ID..."
for id in $ids; do
    echo "Processing ID: $id"
    
    mql -c "set context user creator pass Tru@2018x; exec prog TRUSpecRightDataLoader -method createOrActiveSupplierData \"$id\";"
    
    if [ $? -ne 0 ]; then
        echo "Error executing JPO for ID: $id"
    else
        echo "Successfully processed ID: $id"
    fi
done
