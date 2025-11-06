#!/usr/bin/tclsh
# ====================================================================
# Script Name  : ExtractReferenceDocs.tcl
# Author       : AGhosh05
# Purpose      : 
#   For every Type defined in the configuration file, 
#   find all objects, expand their "Reference Document" relationships,
#   and store parent-child details in text files.
# ====================================================================


tcl;

# ------------------------------------------------------------
# Procedure: readFile
# Purpose: Reads a given property entry from config and 
#          returns its comma-separated values as a list.
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# startTransaction / commitTransaction / abortTransaction
#   Wrapper functions for MQL transaction management.
#------------------------------------------------------------------------------
proc startTransaction {} {
	set errorCreate [ catch {mql start transaction historyoff triggeroff} ResultCreate ]
	if {$errorCreate != 0} {
		#puts "Error starting transaction: $ResultCreate"
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
		#puts "Error aborting transaction: $ResultCreate"
	}
}

# ------------------------------------------------------------
# Procedure: extractReferenceDocs
# Purpose: Expands reference document relationships for all
#          objects of specified types and writes results to output files.
# ------------------------------------------------------------
proc extractReferenceDocs {typeList output_dir success_log error_log} {

    foreach typeName $typeList {
        set typeName [string trim $typeName]
        if {$typeName eq ""} { continue }

        puts "Processing Type: $typeName"

        # Make a filesystem-safe filename
        set safeTypeName [string map {" " "_" "/" "_"} $typeName]
		set filePrefix   [lindex [readFile "OUTPUT.FILE.PREFIX"] 0]
        set outputFile "$output_dir/$filePrefix${safeTypeName}.txt"
        set out [open $outputFile w]
		set parentRel    [lindex [readFile "PARENT.RELATIONSHIP"] 0]
		set parentName   [lindex [readFile "PARENT.NAME"] 0]
		set parentRev    [lindex [readFile "PARENT.REVISION"] 0]
		set filterType   [lindex [readFile "EXCLUDE.TYPE"] 0]
		set excepType    [lindex [readFile "EXCEPTION.TYPE"] 0]
		set excepName    [lindex [readFile "EXCEPTION.NAME"] 0]
		
		if { "$typeName" == "$excepType" } {
			set parentName "$excepName"
		}

        #puts $out "Parent Type~Parent Name~Parent Revision~Parent Id~Ref Type~Ref Name~Ref Revision~Ref Title"
		
		# Start transaction for each entry
		set startTrans [startTransaction]
		
        # Fetch all business objects for this type
        if {[catch {mql temp query bus "$typeName" "$parentName" $parentRev where "from\[$parentRel\]==TRUE" select id dump ~;} objectList]} {
            puts $error_log "$typeName~Error: Failed to fetch objects for type"
			set abortTrans [abortTransaction]
            close $out
            continue
        }

        if {$objectList eq ""} {
            puts $error_log "$typeName~No objects found for type"
			set abortTrans [abortTransaction]
            close $out
            continue
        }
		
		

        set count 0
		set success 0

        # Loop over each object and expand relationships
        foreach line [split $objectList "\n"] {
			incr count 
            if {[string trim $line] eq ""} { continue }

            set fields [split $line "~"]
            if {[llength $fields] < 4} { continue }

            set parentType  [string trim [lindex $fields 0]]
            set parentName  [string trim [lindex $fields 1]]
            set parentRev   [string trim [lindex $fields 2]]
            set parentId    [string trim [lindex $fields 3]]
				
            # Expand Reference Document relationship
            if {[catch {mql expand bus $parentId relationship "$parentRel" select bus type name revision attribute\[Title\] dump ~;} expandResult]} {
                puts $error_log "$parentType~Expansion failed for $parentName"
				set abortTrans [abortTransaction]
                continue
            }

            if {[string trim $expandResult] eq ""} {
				puts $error_log "$parentType~No expansion found for $parentName"
				set abortTrans [abortTransaction]
                continue
            }
			

            # Parse expansion results
            foreach eLine [split $expandResult "\n"] {
                if {[string trim $eLine] eq ""} { continue }

                set eFields [split $eLine "~"]
                if {[llength $eFields] < 10} { continue }

                set refType   [string trim [lindex $eFields 6]]
                set refName   [string trim [lindex $eFields 7]]
                set refRev    [string trim [lindex $eFields 8]]
                set refTitle  [string trim [lindex $eFields 9]]
				
				if {"$refType" != "$filterType"} {
					puts $out "$parentType~$parentName~$parentRev~$parentId~$refType~$refName~$refRev~$refTitle"
					incr success
				}
                
            }
        }
		
		# Commit transaction and log output
		set commitTrans [commitTransaction]
			
        puts $success_log "Extracted $count objects for type: $typeName"
		puts $success_log "Objects with $parentRel relationship: $success"
        close $out
    }

    
}


# -----------------------------------------------------------------------------
# Trigger and History Control
#   Disables/enables triggers and history logging for performance and safety.
# -----------------------------------------------------------------------------
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

# ------------------------------------------------------------
# MAIN EXECUTION
# ------------------------------------------------------------
eval {
	set base_dir [pwd]
    set output_dir "$base_dir/../Output"
	
    # Ensure output directory exists
    if {![file exists $output_dir]} {
        file mkdir $output_dir
    }
	
	# Prepare logs directory
	set log_dir "$base_dir/../Logs"
	if {![file exists $log_dir]} {
		file mkdir $log_dir
	}
	
	# Create success log file
	set success_log [open "$log_dir/extraction_success_log.txt" w]

	# Create error log file
	set error_log [open "$log_dir/extraction_error_log.txt" w]
	puts $error_log "Parent Type~Comments"
	
	# Print start time
	set startTime "=== Extraction started at [clock format [clock seconds] -format {%b %d, %Y %I:%M:%S %p}] ==="
	puts $startTime
	puts $success_log "$startTime"

    # Read TYPES from config
    set typeList [readFile "TYPES"]
    if {[llength $typeList] == 0} {
        puts "Error: TYPES not defined in LegacyDocConfig.txt"
        exit 1
    }
	
	# Disable triggers and history
	set triggOff [setTriggerOff]
	set historyOff [setHistoryOff]

    extractReferenceDocs $typeList $output_dir $success_log $error_log
	
	
	# Close logs
	close $error_log

	# Re-enable triggers and history
	set triggOn [setTriggerOn]
	set historyOn [setHistoryOn]
	
    # Print end time
	set endTime "=== Extraction completed at [clock format [clock seconds] -format {%b %d, %Y %I:%M:%S %p}] ==="
	puts $endTime
	puts $success_log "$endTime"
	close $success_log
}
