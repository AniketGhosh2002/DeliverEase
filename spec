#!/usr/bin/tclsh

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------

set reportFile "report.xls"   ;# Input report file
set allowedTypes {A C}        ;# Only these types will get an output file

# ---------------------------------------------------
# Read report file
# ---------------------------------------------------

if {![file exists $reportFile]} {
    puts "ERROR: Report file '$reportFile' not found."
    exit 1
}

set fp [open $reportFile r]
set lines [split [read $fp] "\n"]
close $fp

# Get header (first line)
set header [lindex $lines 0]

# Create a dict to hold type-wise rows
array set typeData {}

# ---------------------------------------------------
# Process each line after header
# ---------------------------------------------------
foreach line [lrange $lines 1 end] {

    if {[string trim $line] eq ""} {
        continue
    }

    # Split by whitespace or tab – adjust if needed
    set cols [regexp -inline -all {\S+} $line]

    set type [lindex $cols 0]

    # If type is allowed, store it
    if {[lsearch -exact $allowedTypes $type] != -1} {
        lappend typeData($type) $line
    }
}

# ---------------------------------------------------
# Write output file per allowed type
# ---------------------------------------------------
foreach type $allowedTypes {

    if {![info exists typeData($type)]} {
        puts "Skipping $type – NO entries found in report."
        continue
    }

    set outFile "${type}_output.txt"
    set outFp [open $outFile w]

    puts $outFp $header
    foreach row $typeData($type) {
        puts $outFp $row
    }

    close $outFp
    puts "Created: $outFile"
}

puts "\nDone!"
