#!/bin/bash
###############################################################################
# Cron Job Script to Run TRUSpecRightDataLoader Every Hour                   #
# No Bootstrap Version                                                       #
###############################################################################

# Timestamp and directory
NOW=$(date '+%Y-%m-%d %H:%M:%S')
CONFIG_FILE="/apps/SpecRightChanges/Aniket/shellScript/Config/TRUDataLoader.config"
LOG_FILE="/apps/SpecRightChanges/Aniket/shellScript/Log/TRUSpecRightDataLoader_$(date +%Y%m%d_%H%M).log"

# Read config
START_DATE=$(grep -w START_DATE "$CONFIG_FILE" | cut -d '=' -f2)
MQLUSER=$(grep -w MQLUSER "$CONFIG_FILE" | cut -d '=' -f2)
MQLPWD=$(grep -w MQLPWD "$CONFIG_FILE" | cut -d '=' -f2)

# Check for missing values
if [[ -z "$START_DATE" || -z "$MQLUSER" || -z "$MQLPWD" ]]; then
  echo "[ERROR] Missing required config values." | tee -a "$LOG_FILE"
  exit 1
fi

# Log start
echo "====================================" >> "$LOG_FILE"
echo "CRON EXECUTION at $NOW" >> "$LOG_FILE"
echo "Running TRUSpecRightDataLoader with START_DATE: $START_DATE" >> "$LOG_FILE"

# Execute JPO
"verb on; set context user  $MQLUSER pass $MQLPWD ; temp que bus "Business Unit" * * where "originated > '05/16/2025 7:40:01 AM' && current==Active" select id; exec prog TRUSpecRightDataLoader -method createOrActiveSupplierData \"$START_DATE\";" >> "$LOG_FILE" 2>&1
RESULT=$?

# Log result
if [[ $RESULT -eq 0 ]]; then
  echo "[INFO] JPO executed successfully." >> "$LOG_FILE"
else
  echo "[ERROR] JPO execution failed with code $RESULT." >> "$LOG_FILE"
fi


