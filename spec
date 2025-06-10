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
STARTDATE=`cat $BASEDIR/../Config/CronRun.GO`
echo "$STARTDATE"

#------------------------------------------------------------------------------
# Step 2: Call the JPO method
#------------------------------------------------------------------------------

mql -c "set context user creator pass $MQLPWD; exec prog TRUSpecRightDataLoader -method createOrActiveSupplierData \"$STARTDATE\";"

#------------------------------------------------------------------------------
# Step 3: Update the CronRun with execution time
#------------------------------------------------------------------------------

date +%m"/"%d"/"%Y" "%r >  $BASEDIR/../Config/CronRun.GO
