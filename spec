# ---------------------------------------------------------------------
# Reuse: readFile { MY_ENTRY }  -> Reads values from apps/Config.txt
# ---------------------------------------------------------------------
proc readFile {MY_ENTRY} {
    set configPath [file join "apps" "Config.txt"]

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
        if {[regexp "^$MY_ENTRY=(.*)" $line -> values]} {
            foreach val [split $values ","] {
                lappend valuesList [string trim $val]
            }
            break
        }
    }

    return $valuesList
}

# ---------------------------------------------------------------------
# Main: getReferenceDocFiles { input_dir }
# ---------------------------------------------------------------------
proc getReferenceDocFiles {input_dir} {
    # Check directory
    if {![file isdirectory $input_dir]} {
        error "Input directory not found: $input_dir"
    }

    # Read prefix entry from config
    set prefixList [readFile "REFERENCE_FILE_PREFIX"]
    if {[llength $prefixList] == 0} {
        error "No REFERENCE_FILE_PREFIX entry found in Config.txt"
    }

    # Get first prefix (you can extend to multiple prefixes if needed)
    set prefix [lindex $prefixList 0]

    # Get all files from directory
    set all_files [glob -nocomplain -directory $input_dir *]
    set matched_files {}

    # Loop and filter using prefix from config
    foreach file_path $all_files {
        set filename [file tail $file_path]
        if {[string match "${prefix}*" $filename]} {
            lappend matched_files $file_path
        }
    }

    return $matched_files
}
