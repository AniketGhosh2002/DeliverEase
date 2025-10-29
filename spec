# ====================================================================
# Author       : AGhosh05
# Purpose      : For every Type in the system, find all objects,
#                expand their Reference Specification relationships,
#                and store details in a text file
# ====================================================================


tcl;
eval {

set base_dir [pwd]  
set output_dir "$base_dir/../Output"
set configFile "$base_dir/../Config/LegacyDocConfig.txt"
set typeLine ""
set typeList {}
set success 0

if {![file exists $output_dir]} {
    file mkdir $output_dir
}

if {[file exists $configFile]} {
    set fh [open $configFile r]
    while {[gets $fh line] >= 0} {
        if {[regexp {^TYPES=(.+)} $line -> typeVal]} {
            set typeLine $typeVal
            break
        }
    }
    close $fh
} else {
    puts "Config file not found"
    exit 1
}

if {$typeLine eq ""} {
    puts "TYPES not defined in config.txt"
    exit 1
}

foreach t [split $typeLine ","] {
    set t [string trim $t]
    if {$t ne ""} {
        lappend typeList $t
    }
}

foreach typeName $typeList {

    set typeName [string trim $typeName]
    if {$typeName eq ""} { continue }

    puts "Processing Type: $typeName"
	
	set safeTypeName [string map {" " "_" "/" "_"} $typeName]
    set outputFile "$output_dir/ReferenceDoc_${safeTypeName}.txt"
    set out [open $outputFile w]

    set objectList [mql temp query bus "$typeName" * * select id dump ~;]

    if {$objectList eq ""} {
        puts "No objects found"
        close $out
        continue
    }

    foreach line [split $objectList "\n"] {
        if {[string trim $line] eq ""} { continue }
        set fields [split $line "~"]
        if {[llength $fields] < 4} { continue }

        set parentType  [string trim [lindex $fields 0]]
        set parentName  [string trim [lindex $fields 1]]
        set parentRev   [string trim [lindex $fields 2]]
        set parentId    [string trim [lindex $fields 3]]

        set expandResult [mql expand bus $parentId relationship "Reference Document" select bus type name revision attribute\[Title\] dump ~;]

        if {[string trim $expandResult] eq ""} {
            continue
        }
        foreach eLine [split $expandResult "\n"] {
            if {[string trim $eLine] eq ""} { continue }

            set eFields [split $eLine "~"]
            if {[llength $eFields] < 6} { continue }

			set refType   [string trim [lindex $eFields 6]]
            set refName   [string trim [lindex $eFields 7]]
            set refRev    [string trim [lindex $eFields 8]]
            set refTitle  [string trim [lindex $eFields 9]]

            puts $out "$parentType~$parentName~$parentRev~$parentId~$refType~$refName~$refRev~$refTitle"
			
			incr success
        }
		
    }
	puts "Fetched : $success"
	set success 0
	close $out
}

puts "Reference Documents extracted"

}
