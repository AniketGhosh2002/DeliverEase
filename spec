# Read parent names and revisions from config
set parentNames [readFile "PARENT.NAME"]
set parentRevs  [readFile "PARENT.REVISION"]

# Handle * or empty entries
if {[llength $parentNames] == 0 || ([llength $parentNames] == 1 && [lindex $parentNames 0] in {"*" ""})} {
    set parentNames [list "*"]
}

if {[llength $parentRevs] == 0 || ([llength $parentRevs] == 1 && [lindex $parentRevs 0] in {"*" ""})} {
    set parentRevs [list "*"]
}

# Start transaction for each entry
set startTrans [startTransaction]

# Loop through all combinations of parent name and revision
foreach pName $parentNames {
    foreach pRev $parentRevs {

        puts "Processing $typeName — Parent: $pName Rev: $pRev"

        # Fetch all business objects for this type and parent combination
        if {[catch {
            mql temp query bus "$typeName" "$pName" "$pRev" \
                where "from\[$parentRel\]==TRUE" \
                select id dump ~;
        } objectList]} {
            puts $error_log "$typeName~Error: Failed to fetch objects for Parent=$pName Rev=$pRev"
            set abortTrans [abortTransaction]
            continue
        }

        if {[string trim $objectList] eq ""} {
            puts $error_log "$typeName~No objects found for Parent=$pName Rev=$pRev"
            continue
        }

        set count 0
        set success 0

        foreach line [split $objectList "\n"] {
            incr count
            if {[string trim $line] eq ""} { continue }

            set fields [split $line "~"]
            if {[llength $fields] < 4} { continue }

            set parentType  [string trim [lindex $fields 0]]
            set parentName  [string trim [lindex $fields 1]]
            set parentRev   [string trim [lindex $fields 2]]
            set parentId    [string trim [lindex $fields 3]]

            if {[catch {mql expand bus $parentId relationship "$parentRel" select bus type name revision attribute\[Title\] dump ~;} expandResult]} {
                puts $error_log "$parentType~Expansion failed for $parentName"
                continue
            }

            if {[string trim $expandResult] eq ""} {
                puts $error_log "$parentType~No Reference Documents for $parentName"
                continue
            }

            foreach eLine [split $expandResult "\n"] {
                if {[string trim $eLine] eq ""} { continue }
                set eFields [split $eLine "~"]
                if {[llength $eFields] < 10} { continue }

                set refType   [string trim [lindex $eFields 6]]
                set refName   [string trim [lindex $eFields 7]]
                set refRev    [string trim [lindex $eFields 8]]
                set refTitle  [string trim [lindex $eFields 9]]

                puts $out "$parentType~$parentName~$parentRev~$parentId~$refType~$refName~$refRev~$refTitle"
                incr success
            }
        }

        puts $success_log "Extracted $count objects for $typeName ($pName - $pRev)"
        puts $success_log "Objects with $parentRel: $success"
    }
}

set commitTrans [commitTransaction]
