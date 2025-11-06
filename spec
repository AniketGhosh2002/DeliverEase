# Prepare success log for this file
set filename [file tail $filePath]

# Get LOG prefix from config
set prefixList [readFile "LOG.FILE.PREFIX"]
if {[llength $prefixList] == 0} {
    error "No LOG.FILE.PREFIX entry found in Config.txt"
}
set logPrefix [lindex $prefixList 0]

# Remove OUTPUT.FILE.PREFIX from filename (if exists)
set outPrefixList [readFile "OUTPUT.FILE.PREFIX"]
set outPrefix [expr {[llength $outPrefixList] > 0 ? [lindex $outPrefixList 0] : ""}]
set cleanName [string map [list $outPrefix ""] [file rootname $filename]]

# Add current timestamp to filename
set timeStr [clock format [clock seconds] -format "%Y%m%d_%H%M%S"]

# Build final log filename
set logFileName "$logPrefix${cleanName}_$timeStr.txt"

# Open log file
set output_log [open "$log_dir/$logFileName" w]
