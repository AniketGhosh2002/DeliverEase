# ====================================================================
# Script Name  : getReferenceSpecs_ConfigTypes.tcl
# Purpose      : Read types from config file and for each type,
#                fetch Reference Specification relationships and
#                store them in separate text files (~ separated)
# ====================================================================

# ---- Step 1: Read type list from config file ----
set configFile "config.txt"
set typeLine ""
set typeList {}

if {[file exists $configFile]} {
    set fh [open $configFile r]
    while {[gets $fh line] >= 0} {
        if {[regexp {^TYPE=(.+)} $line -> typeVal]} {
            set typeLine $typeVal
            break
        }
    }
    close $fh
} else {
    puts "❌ Config file not found!"
    exit 1
}

if {$typeLine eq ""} {
    puts "❌ TYPE not defined in config.txt"
    exit 1
}

# Split types by comma and trim spaces
foreach t [split $typeLine ","] {
    set t [string trim $t]
    if {$t ne ""} {
        lappend typeList $t
    }
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
