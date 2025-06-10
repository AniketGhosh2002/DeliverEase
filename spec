#!/bin/bash
###############################################################################
#     Script to Create or Activate Supplier/Site in SpecRight                 #
#     Date:    May 2025                                                       #
#     Author : TCS                                                            #
###############################################################################
 
# Setup date/time variables
VDATE=$(date +%Y-%m-%d_%H.%M)
cronStartDate=$(date)
FileDynamics=$(date +%m%d%Y)
 
# Setup base and log directory
BASEDIR=$(dirname "$0")
LOGDIR="$BASEDIR/../Logs"
mkdir -p "$LOGDIR"
LOGFILE="$LOGDIR/CreateOrActivateSupplier_$VDATE.log"
 
# Start logging
{
echo "-------------------------------- CRON RUN DETAILS ---------------------------------"
echo "Run Started At   : $cronStartDate"
 
#------------------------------------------------------------------------------
# Step 1: Read the CronRun file entry
#------------------------------------------------------------------------------
echo ""
echo "Step 1: Reading CronRun file..."
export MQLPWD=$(mql -t -c "execute program PwdMgr -method getPwd 'creator';")
STARTDATE=$(cat "$BASEDIR/../Config/CronRun.GO")
echo "Start Date for Processing: $STARTDATE"
 
#------------------------------------------------------------------------------
# Step 2: Call the JPO method
#------------------------------------------------------------------------------
echo ""
echo "Step 2: Executing createOrActiveSupplierData with Start Date..."
mql -c "set context user creator pass $MQLPWD; exec prog TRUSpecRightDataLoader -method createOrActiveSupplierData \"$STARTDATE\";"
 
#------------------------------------------------------------------------------
# Step 3: Update the CronRun with execution time
#------------------------------------------------------------------------------
echo ""
echo "Step 3: Updating CronRun.GO with current timestamp..."
date +%m"/"%d"/"%Y" "%r >  $BASEDIR/../Config/CronRun.GO
echo "Updated CronRun.GO successfully."
 
echo ""
echo "Script completed at: $(date)"
 
} >> "$LOGFILE" 2>&1
