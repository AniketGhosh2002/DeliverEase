#!/bin/bash
###############################################################################
#     Script to Create or Activate Supplier/Site in SpecRight                 #
#     Date:    June 2025                                                       #
#     Author : TCS                                                            #
###############################################################################
 
VDATE=$(date +%Y-%m-%d_%H.%M)
cronStartDate=$(date)
FileDynamics=$(date +%m%d%Y)
 
echo "-------------------------------- CRON RUN DETAILS ---------------------------------"
echo "Run Started At   : $cronStartDate"
 
#------------------------------------------------------------------------------
# Step 1: Setup
#------------------------------------------------------------------------------
BASEDIR=$(dirname "$0")
LOG_DIR="$BASEDIR/../Log"
echo "$LOG_DIR"
CONFIG_FILE="$BASEDIR/../Config/inputFileList.txt"
INPUT_FOLDER="$BASEDIR/../Config/input"
MQLPWD=$(mql -t -c "execute program PwdMgr -method getPwd 'creator';")
 
if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Input config file not found: $CONFIG_FILE"
  exit 1
fi
 
#------------------------------------------------------------------------------
# Step 2: Read all file names into array
#------------------------------------------------------------------------------
mapfile -t fileNames < "$CONFIG_FILE"
 
#------------------------------------------------------------------------------
# Step 3: Loop through each file name and call JPO
#------------------------------------------------------------------------------

mkdir -p "$LOG_DIR"

for fileName in "${fileNames[@]}"; do
  fileName=$(echo "$fileName" | xargs)  
  inputFilePath="$INPUT_FOLDER/$fileName"

  if [[ -n "$fileName" && -f "$inputFilePath" ]]; then
    echo "Processing file: $inputFilePath"
    
    logFileName="${fileName%.*}_Log_$VDATE.log"
	errorFileName = "${fileName%.*}_Error_Log_$VDATE.log"
    logFilePath="$LOG_DIR/$logFileName"
	echo "$logFilePath"
	errorFilePath="$LOG_DIR/$errorFileName"
	echo "$errorFilePath"

    echo "------ LOG START FOR $fileName at $(date) ------" 
    
    mql -c "set context user creator pass $MQLPWD; exec prog TRUSpecRightDataLoader -method createOrActiveBulkSupplierData \"$inputFilePath\" \"$logFilePath\" \"$errorFilePath\";"
	echo ""
    echo "------ LOG END FOR $fileName at $(date) --------" 
	echo ""
  else
    echo "[WARNING] File not found or empty entry: $inputFilePath"
  fi
done
 
#------------------------------------------------------------------------------
# Step 4: Update CronRun Time
#------------------------------------------------------------------------------
date +%m"/"%d"/"%Y" "%r > $BASEDIR/../Config/CronRunBulk.GO
echo "Script completed at: $(date)"
