tcl;

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
        if {[string trim $line] eq "" || [string match "#*" $line]} {
            continue
        }
        if {[regexp "^$propEntry=(.*)" $line -> values]} {
            foreach val [split $values ","] {
                lappend valuesList [string trim $val]
            }
            break
        }
    }

    return $valuesList
}

proc getReferenceDocFiles {input_dir} {
    if {![file isdirectory $input_dir]} {
        error "Input directory not found: $input_dir"
    }

    set prefixList [readFile "OUTPUT.FILE.PREFIX"]
    if {[llength $prefixList] == 0} {
        error "No OUTPUT.FILE.PREFIX entry found in Config.txt"
    }

    set prefix [lindex $prefixList 0]

    set all_files [glob -nocomplain -directory $input_dir *]
    set matched_files {}

    foreach file_path $all_files {
        set filename [file tail $file_path]
        if {[string match "${prefix}*" $filename]} {
            lappend matched_files $file_path
        }
    }

    return $matched_files
}

proc startTransaction {} {
	set errorCreate [ catch {mql start transaction historyoff triggeroff} ResultCreate ]
	if {$errorCreate == 0} {
		#puts $ResultCreate
		} else {
		#puts $ResultCreate
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
	if {$errorCreate == 0} {
		#puts $ResultCreate
		} else {
		#puts $ResultCreate
	}
}

proc processFile {filePath log_dir error_log} {

    puts "Processing file: $filePath"

    set in [open $filePath r]
    set lines [split [read $in] "\n"]
    close $in
	
	set filename [file tail $filePath]
	set prefixList [readFile "LOG.FILE.PREFIX"]
    if {[llength $prefixList] == 0} {
        error "No LOG.FILE.PREFIX entry found in Config.txt"
    }
    set prefix [lindex $prefixList 0]
    set success_log [open "$log_dir/$prefix[file rootname $filename].txt" w]
	puts $success_log "Parent Type~Parent Name~Parent Revision~Object Type~Object Name~Object Revision~Object Id"
	
	foreach line $lines {
        if {[string trim $line] eq ""} {
            continue
        }

        set parts [split $line "~"]
        if {[llength $parts] < 7} {
            puts "Skipping invalid line: $line"
            continue
        }
		
		set startTrans [startTransaction]
		set parent_type [lindex $parts 0]
		set parent_name [lindex $parts 1]
		set parent_rev  [lindex $parts 2]
        set parent_id   [lindex $parts 3]
        set ref_name    [lindex $parts 5]
        set ref_title   [lindex $parts 7]
		set obj_type    [lindex [readFile "OBJECT.TYPE"] 0]
		set obj_name    "auto_[clock milliseconds]"
		set obj_rev     [lindex [readFile "OBJECT.REVISION"] 0]
		set obj_pol     [lindex [readFile "OBJECT.POLICY"] 0]
		set obj_vault   [lindex [readFile "OBJECT.VAULT"] 0]
		set obj_proj    [lindex [readFile "OBJECT.PROJECT"] 0]
		set obj_org     [lindex [readFile "OBJECT.ORGANIZATION"] 0]
		set obj_rel     [lindex [readFile "OBJECT.RELATIONSHIP"] 0]

        set add_cmd "mql add bus \"$obj_type\" $obj_name $obj_rev policy \"$obj_pol\" vault \"$obj_vault\" project \"$obj_proj\" organization \"$obj_org\""
		set add_out [catch {eval $add_cmd} result]
		set print_cmd "mql print bus \"$obj_type\" $obj_name $obj_rev select id dump"
		set print_out [catch {eval $print_cmd} result]	
        set obj_id [string trim $result]
        if {$obj_id eq ""} {
            puts $error_log "$parent_type~$parent_name~$parent_rev~Failed to fetch ID for $obj_name"
            set abortTrans [abortTransaction]
            continue
        }
		
		set mod_cmd "mql modify bus $obj_id \"Legacy Doc Name\" \"$ref_name\" \"Legacy Doc Title\" \"$ref_title\""
        set mod_out [catch {eval $mod_cmd} mod_result]
        if {$mod_out != 0} {
            puts $error_log "$parent_type~$parent_name~$parent_rev~Update failed for $obj_id : $mod_result"
            set abortTrans [abortTransaction]
            continue
        }

        set conn_cmd "mql connect bus $parent_id relationship \"$obj_rel\" to $obj_id"
        set conn_out [catch {eval $conn_cmd} conn_result]
        if {$conn_out != 0} {
            puts $error_log "$parent_type~$parent_name~$parent_rev~Connection failed for $parent_id to $obj_id : $conn_result"
            set abortTrans [abortTransaction]
            continue
        }
		
		
		set commitTrans [commitTransaction]
		
		puts $success_log "$parent_type~$parent_name~$parent_rev~$obj_type~$obj_name~$obj_rev~$obj_id"
	}
	
	close $success_log

}

proc setTriggerOff {} {
	set errorCreate [ catch {mql trigg off} ResultCreate ]
	if {$errorCreate == 0} {
		puts $ResultCreate
	} else {
		puts $ResultCreate
	}
}

proc setTriggerOn { } {
	set errorCreate [ catch {mql trigg on} ResultCreate ]
	if {$errorCreate == 0} {
		puts $ResultCreate
	} else {
		puts $ResultCreate
	}
}
proc setHistoryOff {} {
	set errorCreate [ catch {mql history off} ResultCreate ]
	if {$errorCreate == 0} {
		puts $ResultCreate
	} else {
		puts $ResultCreate
	}
}
	
proc setHistoryOn {} {
	set errorCreate [ catch {mql history on} ResultCreate ]
	if {$errorCreate == 0} {
		puts $ResultCreate
	} else {
		puts $ResultCreate
	}
}

eval {

	set base_dir [pwd]
	set input_dir "$base_dir/../Output"
	if {![file exists $input_dir]} {
		puts "Input directory missing"
		exit 1
	}
	set log_dir "$base_dir/../Logs"
	if {![file exists $log_dir]} {
		file mkdir $log_dir
	}
	set error_log [open "$log_dir/error_log.txt" w]
	puts $error_log "Parent Type~Parent name~Parent Revision~Comments"
	set startTime "=== Migration started at [clock format [clock seconds] -format {%b %d, %Y %I:%M:%S %p}] ==="
	puts $startTime
	set triggOff [setTriggerOff]
	set historyOff [setHistoryOff]
	set inputFileList [getReferenceDocFiles $input_dir]
	foreach filePath $inputFileList {
		processFile $filePath $log_dir $error_log
	}
	close $error_log
	set triggOn [setTriggerOn]
	set historyOn [setHistoryOn]
	set endTime "=== Migration completed at [clock format [clock seconds] -format {%b %d, %Y %I:%M:%S %p}] ==="
	puts $endTime
}
