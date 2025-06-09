#------------------------------------------------------------------------------
# Step 3: Loop through each file name and call JPO
#------------------------------------------------------------------------------
LOG_DIR="$BASEDIR/../Logs"
mkdir -p "$LOG_DIR"

for fileName in "${fileNames[@]}"; do
  fileName=$(echo "$fileName" | xargs)  
  inputFilePath="$INPUT_FOLDER/$fileName"

  if [[ -n "$fileName" && -f "$inputFilePath" ]]; then
    echo "Processing file: $inputFilePath"
    
    logFileName="${fileName%.*}_Log_$VDATE.log"
    logFilePath="$LOG_DIR/$logFileName"

    echo "------ LOG START FOR $fileName at $(date) ------" >> "$logFilePath"
    
    mql -c "set context user creator pass $MQLPWD; exec prog TRUSpecRightDataLoader -method createOrActiveBulkSupplierData \"$inputFilePath\";" >> "$logFilePath" 2>&1

    echo "------ LOG END FOR $fileName at $(date) --------" >> "$logFilePath"
  else
    echo "[WARNING] File not found or empty entry: $inputFilePath"
  fi
done
