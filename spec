#!/bin/bash
###############################################################################
#     Script to Create or Activate Supplier/Site in SpecRight                 #
#     Date:    May 2025                                                       #
#     Author : TCS                                                            #
###############################################################################

VDATE=`date +%Y-\%m-\%d_\%H.\%M`
cronStartDate=`date`
FileDynamics=`date +%m\%d\%Y`

echo "-------------------------------- CRON RUN DETAILS ---------------------------------"
echo "Run Started At   : $cronStartDate"


#------------------------------------------------------------------------------
# Step 1: Read the CronRun file entry
#------------------------------------------------------------------------------
BASEDIR=$(dirname "$0")
export MQLPWD=`mql -t -c "execute program PwdMgr -method getPwd 'creator';"`
FILEPATH="$BASEDIR/../Config/input/input.txt"
echo "$FILEPATH"

#------------------------------------------------------------------------------
# Step 2: Call the JPO method
#------------------------------------------------------------------------------

mql -c "set context user creator pass $MQLPWD; exec prog TRUSpecRightDataLoader -method createOrActiveBulkSupplierData "$FILEPATH";"

#------------------------------------------------------------------------------
# Step 3: Update the CronRun with execution time
#------------------------------------------------------------------------------

date +%m"/"%d"/"%Y" "%r >  $BASEDIR/../Config/CronRunBulk.GO
