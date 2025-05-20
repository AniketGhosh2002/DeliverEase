echo "Working..."
VDATE=$(date +%Y-%m-%d_%H.%M)
cronStartDate=$(date)
FileDynamics=$(date +%m%d%Y)
CONFIG_FILE="/apps/SpecRightChanges/Aniket/shellScript/Config/TRUDataLoader.config"
LOG_FILE="/apps/SpecRightChanges/Aniket/shellScript/Log/TRUSpecRightDataLoader_$(date +%Y%m%d_%H%M).log"
START_DATE="5/16/2025 7:40:00 AM"
echo "VDATE: $VDATE"
echo "Start Date: $START_DATE"
echo "$CONFIG_FILE"
echo "$LOG_FILE"
mql -c "verb on; set context user creator pass Tru@2018x; temp query bus \"Business Unit\" * * where \"originated > '$START_DATE' && current=='Active'\" select id;"
ID_LIST=$(mql -c "verb on; set context user creator pass Tru@2018x; temp query bus \"Business Unit\" * * where \"originated > '$START_DATE' && current=='Active'\" select id dump |;")
echo "$ID_LIST" | while IFS="|" read -r TYPE NAME REV ID; do
  if [[ "$ID" != "" && "$ID" != "id" ]]; then
    echo "Executing for ID: $ID" >> "$LOG_FILE"
    mql -c "verb on; set context user creator pass Tru@2018x; exec prog TRUSpecRightDataLoader -method createOrActiveSupplierData \"$ID\";" >> "$LOG_FILE" 2>&1
    echo "Completed: $ID" >> "$LOG_FILE"
  fi
done
