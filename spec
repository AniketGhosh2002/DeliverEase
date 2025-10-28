# =====================================================================
# TCL Script: Process Legacy Documents for Reference Specifications
# =====================================================================

# --- Global Config ---
set base_dir "C:/ENOVIA/ReferenceSpecs"     ;# base folder path
set input_dir "$base_dir/output"
set success_log "$base_dir/success_log.txt"
set error_log "$base_dir/error_log.txt"

# --- Global Variables ---
set type_name "Legacy Document"
set rel_name "Extended Data"
set attr_doc_name "Legacy Doc Name"
set attr_doc_title "Legacy Doc Title"

# =====================================================================
# PROC: processFile - process a single input file
# =====================================================================
proc processFile {filePath} {
    global success_log error_log type_name rel_name attr_doc_name attr_doc_title

    puts "Processing file: $filePath"

    # Open input file
    set in [open $filePath r]
    set lines [split [read $in] "\n"]
    close $in

    # Loop through each line
    foreach line $lines {
        if {[string trim $line] eq ""} {
            continue
        }

        # Expected format: ParentID~ReferenceDocTitle~ReferenceDocName
        set parts [split $line "~"]
        if {[llength $parts] < 3} {
            puts "Skipping invalid line: $line"
            continue
        }

        set parent_id [lindex $parts 0]
        set ref_title [lindex $parts 1]
        set ref_name  [lindex $parts 2]

        # Start transaction
        catch {mql start transaction} transErr

        # --- Add new object ---
        set obj_name "auto_[clock milliseconds]"
        set add_cmd "add bus \"$type_name\" $obj_name -"
        set add_out [catch {mql $add_cmd} result]

        if {$add_out != 0} {
            puts $error_log "ADD FAILED for parent $parent_id : $result"
            mql abort transaction
            continue
        }

        # Extract the new object ID
        set obj_id [string trim [mql print bus \"$type_name\" \"$obj_name\" - select id dump]]
        if {$obj_id eq ""} {
            puts $error_log "Failed to fetch ID for $obj_name"
            mql abort transaction
            continue
        }

        # --- Modify attributes ---
        set mod_cmd "modify bus $obj_id attribute \"$attr_doc_name\" \"$ref_name\" attribute \"$attr_doc_title\" \"$ref_title\""
        set mod_out [catch {mql $mod_cmd} mod_result]
        if {$mod_out != 0} {
            puts $error_log "MOD FAILED for $obj_id : $mod_result"
            mql abort transaction
            continue
        }

        # --- Connect relationship ---
        set conn_cmd "connect bus $parent_id relationship \"$rel_name\" to $obj_id"
        set conn_out [catch {mql $conn_cmd} conn_result]
        if {$conn_out != 0} {
            puts $error_log "CONNECT FAILED for $parent_id -> $obj_id : $conn_result"
            mql abort transaction
            continue
        }

        # Commit transaction
        mql commit transaction

        # Log success
        puts $success_log "SUCCESS: Parent $parent_id connected to $obj_id (Doc: $ref_title)"
    }
}

# =====================================================================
# MAIN EXECUTION
# =====================================================================

# Open log files
set success_log_fd [open $success_log a]
set error_log_fd [open $error_log a]
puts $success_log_fd "\n=== START RUN [clock format [clock seconds]] ===\n"
puts $error_log_fd "\n=== START RUN [clock format [clock seconds]] ===\n"

# Loop through all files in the folder
set file_list [glob -nocomplain -directory $input_dir *]

foreach filePath $file_list {
    processFile $filePath
}

puts $success_log_fd "\n=== END RUN ===\n"
puts $error_log_fd "\n=== END RUN ===\n"

close $success_log_fd
close $error_log_fd

puts "Processing completed for all files in $input_dir"    }
}

puts "📋 Types to process: $typeList"

# ---- Step 2: Loop through each type ----
foreach typeName $typeList {
    puts "⚙️ Processing Type: $typeName"

    # Prepare output file for this type
    set safeTypeName [string map {" " "_" "/" "_"} $typeName]
    set outputFile "ReferenceSpecs_${safeTypeName}.txt"
    set out [open $outputFile w]
    puts $out "ParentType~ParentName~ParentRev~ParentID~ReferenceType~ReferenceName~ReferenceRev~ReferenceID"

    # ---- Step 3: Query all objects of the type ----
    set objectList [mql exec "temp query bus \"$typeName\" * * select id dump |"]

    if {[string trim $objectList] eq ""} {
        puts "⚠️ No objects found for Type: $typeName"
        close $out
        continue
    }

    # ---- Step 4: For each object, expand Reference Specification ----
    foreach line [split $objectList "\n"] {
        if {[string trim $line] eq ""} { continue }

        # Expected format: Type | Name | Rev | ID
        set fields [split $line "|"]
        if {[llength $fields] < 4} { continue }

        set parentType [string trim [lindex $fields 0]]
        set parentName [string trim [lindex $fields 1]]
        set parentRev  [string trim [lindex $fields 2]]
        set parentId   [string trim [lindex $fields 3]]

        set expandResult [mql exec "expand bus $parentId relationship \"Reference Specification\" select bus.id bus.name bus.type bus.revision dump |"]

        if {[string trim $expandResult] eq ""} { continue }

        foreach eLine [split $expandResult "\n"] {
            if {[string trim $eLine] eq ""} { continue }

            set eFields [split $eLine "|"]
            if {[llength $eFields] < 6} { continue }

            set refType [string trim [lindex $eFields 2]]
            set refName [string trim [lindex $eFields 3]]
            set refRev  [string trim [lindex $eFields 4]]
            set refId   [string trim [lindex $eFields 5]]

            puts $out "$parentType~$parentName~$parentRev~$parentId~$refType~$refName~$refRev~$refId"
        }
    }

    close $out
    puts "✅ Output generated: $outputFile"
}

puts "🎯 All types processed successfully!"
exit 0
