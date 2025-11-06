#!/usr/bin/tclsh
# ====================================================================
#  Script Name : ReferenceDocAutomation.tcl
#  Description : Automates creation of "Legacy Document" objects in ENOVIA
#                from input reference files, modifies attributes, and connects
#                them to parent objects using configured relationships.
#  Author      : Aniket Ghosh
#  Notes       : Reads configuration from LegacyDocConfig.txt
#                and processes files from the ../Output directory.
# ====================================================================

tcl;

# ------------------------------------------------------------------------------
# readFile
#   Reads a specific property entry from the config file (key=value)
#   and returns its comma-separated values as a list.
# ------------------------------------------------------------------------------
proc readFile {propEntry} {
    set configPath [file join "/apps/Aniket/ReferenceDocMigration/Config" "LegacyDocConfig.txt"]

    if {![file exists $configPath]} {
        error "Config file not found: $configPath"
    }

    set fh [open $configPath r]
    set lines [split [read $fh] "\n"]
    close $fh

    set valuesList {}

    foreach line $lines {
        # Skip empty lines or comment lines starting with #
        if {[string trim $line] eq "" || [string match "#*" $line]} {
            continue
        }

        # Match the desired property and extract values
        if {[regexp "^$propEntry=(.*)" $line -> values]} {
            foreach val [split $values ","] {
                lappend valuesList [string trim $val]
            }
            break
        }
    }

    return $valuesList
}

# ------------------------------------------------------------------------------
# getReferenceDocFiles
#   Scans input directory for files matching the prefix defined in config file.
# ------------------------------------------------------------------------------
proc getReferenceDocFiles {input_dir} {
    if {![file isdirectory $input_dir]} {
        error "Input directory not found: $input_dir"
    }

    # Get prefix from config file (key = OUTPUT.FILE.PREFIX)
    set prefixList [readFile "OUTPUT.FILE.PREFIX"]
    if {[llength $prefixList] == 0} {
        error "No OUTPUT.FILE.PREFIX entry found in Config.txt"
    }
    set prefix [lindex $prefixList 0]

    set all_files [glob -nocomplain -directory $input_dir *]
    set matched_files {}

    # Collect only files that match the prefix
    foreach file_path $all_files {
        set filename [file tail $file_path]
        if {[string match "${prefix}*" $filename]} {
            lappend matched_files $file_path
        }
    }

    return $matched_files
}

#------------------------------------------------------------------------------
# startTransaction / commitTransaction / abortTransaction
#   Wrapper functions for MQL transaction management.
#------------------------------------------------------------------------------
proc startTransaction {} {
	set errorCreate [ catch {mql start transaction historyoff triggeroff} ResultCreate ]
	if {$errorCreate != 0} {
		puts "Error starting transaction: $ResultCreate"
	}
}

proc commitTransaction {} {
	set errorCreate [ catch {mql commit transaction} ResultCreate ]
	if {$errorCreate == 0} {
		return 0
	} else {
		return $ResultCreate
	}
}

proc abortTransaction {} {
	set errorCreate [ catch {mql abort transaction} ResultCreate ]
	if {$errorCreate != 0} {
		puts "Error aborting transaction: $ResultCreate"
	}
}

# ------------------------------------------------------------------------------
# processFile
#   Reads each ReferenceSpec file, creates a Legacy Document object, 
#   sets attributes, connects to parent, and logs success/error.
# ------------------------------------------------------------------------------
proc processFile {filePath log_dir success_log error_log} {

    puts "Processing file: $filePath"

    # Read input file content
    set in [open $filePath r]
    set lines [split [read $in] "\n"]
    close $in
	
	# Prepare success log for this file
	set filename [file tail $filePath]
	set prefixList [readFile "LOG.FILE.PREFIX"]
    if {[llength $prefixList] == 0} {
        error "No LOG.FILE.PREFIX entry found in Config.txt"
    }
    set prefix [lindex $prefixList 0]
    set output_log [open "$log_dir/$prefix[file rootname $filename].txt" w]
	set parentRel  [lindex [readFile "PARENT.RELATIONSHIP"] 0]
	puts $output_log "Parent Type~Parent Name~Parent Revision~$parentRel Type~$parentRel Name~$parentRel Revision~Object Type~Object Name~Object Revision~Comments"
	puts $error_log "------------------------Error log for $filename------------------------"
	puts $error_log "Parent Type~Parent name~Parent Revision~$parentRel Type~$parentRel Name~$parentRel Revision~Object Type~Object Name~Object Revision~Comments"
	puts $success_log "------------------------Success log for $filename------------------------"
	set success 0
			
	foreach line $lines {
        if {[string trim $line] eq ""} {
            continue
        }

        # Expecting at least 7 fields in the line
        set parts [split $line "~"]
        if {[llength $parts] < 7} {
            puts "Skipping invalid line: $line"
            continue
        }
		
		# Start transaction for each entry
		set startTrans [startTransaction]

        # Extract parent and reference details
		set parent_type [lindex $parts 0]
		set parent_name [lindex $parts 1]
		set parent_rev  [lindex $parts 2]
        set parent_id   [lindex $parts 3]
		set ref_type    [lindex $parts 4]
        set ref_name    [lindex $parts 5]
		set ref_rev     [lindex $parts 6]
        set ref_title   [lindex $parts 7]

        # Fetch object-related configuration values
		set obj_type    [lindex [readFile "OBJECT.TYPE"] 0]
		set obj_name    "auto_[clock milliseconds]"
		set obj_rev     [lindex [readFile "OBJECT.REVISION"] 0]
		set obj_pol     [lindex [readFile "OBJECT.POLICY"] 0]
		set obj_vault   [lindex [readFile "OBJECT.VAULT"] 0]
		set obj_proj    [lindex [readFile "OBJECT.PROJECT"] 0]
		set obj_org     [lindex [readFile "OBJECT.ORGANIZATION"] 0]
		set obj_rel     [lindex [readFile "OBJECT.RELATIONSHIP"] 0]

        # Add new business object
        set add_cmd "mql add bus \"$obj_type\" $obj_name $obj_rev policy \"$obj_pol\" vault \"$obj_vault\" project \"$obj_proj\" organization \"$obj_org\""
		set add_out [catch {eval $add_cmd} result]

        # Get new object ID
		set print_cmd "mql print bus \"$obj_type\" $obj_name $obj_rev select id dump"
		set print_out [catch {eval $print_cmd} result]	
        set obj_id [string trim $result]
        if {$obj_id eq ""} {
			puts $output_log "$parent_type~$parent_name~$parent_rev~$ref_type~$ref_name~$ref_name~$obj_type~$obj_name~$obj_rev~Failed"
            puts $error_log "$parent_type~$parent_name~$parent_rev~$ref_type~$ref_name~$ref_name~$obj_type~$obj_name~$obj_rev~Failed to fetch ID for $obj_name"
            set abortTrans [abortTransaction]
            continue
        }
		
		# Modify object attributes
		set mod_cmd "mql modify bus $obj_id \"Legacy Doc Type\" \"$ref_type\" \"Legacy Doc Name\" \"$ref_name\" \"Legacy Doc Title\" \"$ref_title\""
        set mod_out [catch {eval $mod_cmd} mod_result]
        if {$mod_out != 0} {
			puts $output_log "$parent_type~$parent_name~$parent_rev~$ref_type~$ref_name~$ref_name~$obj_type~$obj_name~$obj_rev~Failed"
            puts $error_log "$parent_type~$parent_name~$parent_rev~$ref_type~$ref_name~$ref_name~$obj_type~$obj_name~$obj_rev~Update failed for $obj_id : $mod_result"
            set abortTrans [abortTransaction]
            continue
        }

        # Connect the created object to the parent
        set conn_cmd "mql connect bus $parent_id relationship \"$obj_rel\" to $obj_id"
        set conn_out [catch {eval $conn_cmd} conn_result]
        if {$conn_out != 0} {
			puts $output_log "$parent_type~$parent_name~$parent_rev~$ref_type~$ref_name~$ref_name~$obj_type~$obj_name~$obj_rev~Failed"
            puts $error_log "$parent_type~$parent_name~$parent_rev~$ref_type~$ref_name~$ref_name~$obj_type~$obj_name~$obj_rev~Connection failed for $parent_id to $obj_id : $conn_result"
            set abortTrans [abortTransaction]
            continue
        }
		
		# Commit transaction and log success
		set commitTrans [commitTransaction]
		puts $output_log "$parent_type~$parent_name~$parent_rev~$ref_type~$ref_name~$ref_name~$obj_type~$obj_name~$obj_rev~Success"
		incr success
	}
	
	puts $success_log "Objects connected with $obj_rel relationship: $success"
	close $output_log
}

# ------------------------------------------------------------------------------
# Trigger and History Control
#   Disables/enables triggers and history logging for performance and safety.
# ------------------------------------------------------------------------------
proc setTriggerOff {} {
	set errorCreate [ catch {mql trigg off} ResultCreate ]
	puts $ResultCreate
}

proc setTriggerOn {} {
	set errorCreate [ catch {mql trigg on} ResultCreate ]
	puts $ResultCreate
}

proc setHistoryOff {} {
	set errorCreate [ catch {mql history off} ResultCreate ]
	puts $ResultCreate
}

proc setHistoryOn {} {
	set errorCreate [ catch {mql history on} ResultCreate ]
	puts $ResultCreate
}

# ------------------------------------------------------------------------------
# MAIN EXECUTION 
# ------------------------------------------------------------------------------
eval {

	set base_dir [pwd]
	set input_dir "$base_dir/../Output"

	# Validate input directory
	if {![file exists $input_dir]} {
		puts "Input directory missing"
		exit 1
	}

	# Prepare logs directory
	set log_dir "$base_dir/../Logs"
	if {![file exists $log_dir]} {
		file mkdir $log_dir
	}
	
	set pTime "[clock milliseconds]"
	
	# Create success log file
	set success_log [open "$log_dir/migration_success_log_$pTime.txt" w]

	# Create error log file
	set error_log [open "$log_dir/migration_error_log_$pTime.txt" w]

	# Print start time
	set startTime "=== Migration started at [clock format [clock seconds] -format {%b %d, %Y %I:%M:%S %p}] ==="
	puts $startTime
	puts $success_log $startTime

	# Disable triggers and history
	set triggOff [setTriggerOff]
	set historyOff [setHistoryOff]

	# Get input files and process each one
	set inputFileList [getReferenceDocFiles $input_dir]
	foreach filePath $inputFileList {
		processFile $filePath $log_dir $success_log $error_log $pTime
	}

	# Close logs
	close $error_log

	# Re-enable triggers and history
	set triggOn [setTriggerOn]
	set historyOn [setHistoryOn]

	# Print end time
	set endTime "=== Migration completed at [clock format [clock seconds] -format {%b %d, %Y %I:%M:%S %p}] ==="
	puts $endTime
	puts $success_log $endTime
	close $success_log
}
