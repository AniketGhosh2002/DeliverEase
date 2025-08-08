tcl;
eval {

# Base directory = where the TCL is running
set base_dir [pwd]  

# Define paths relative to base dir
set input_dir "$base_dir/input"
set inputFileList_path "$base_dir/inputFileList.txt"
set error_file_path "$base_dir/errorFile.txt"

# Create directories if not present
if {![file exists $input_dir]} {
    file mkdir $input_dir
}

# Query MQL
set output [split [mql temp que bus "Organization" * * where "current==Active" select id attribute\[Entity Type\].value attribute\[Region\].value attribute\[Organization Phone Number\].value name dump ~;] "\n"]

set batch_size 1000
set total_lines [llength $output]
set file_index 1

# Open main files
set inputFileList_id [open $inputFileList_path "w"]
set error_file_id [open $error_file_path "w"]

for {set i 0} {$i < $total_lines} {incr i $batch_size} {
    set batch [lrange $output $i [expr {$i + $batch_size - 1}]]
    set batch_filename [format "batch_%03d.txt" $file_index]
    set full_batch_path "$input_dir/$batch_filename"

    puts $inputFileList_id $batch_filename
    set batch_file_id [open $full_batch_path "w"]

    foreach line $batch {
        set fields [split $line "~"]
		set objectId   [string trim [lindex $fields 3]]
        set entityType [string trim [lindex $fields 4]]
        set region     [string trim [lindex $fields 5]]
        set phone      [string trim [lindex $fields 6]]
        set name       [string trim [lindex $fields 7]]

        # Collect all error reasons
        set errors {}
        if {$entityType eq ""} {
            lappend errors "Missing Entity Type"
        }
        if {$region eq ""} {
            lappend errors "Missing Region"
        }
		if {$name eq ""} {
            lappend errors "Missing Name"
        }
        if {[string length $phone] > 40} {
            lappend errors "Phone Number too long ([string length $phone] chars)"
        }

        # Write to error or batch file
        if {[llength $errors] > 0} {
            puts $error_file_id "$objectId - $name - [join $errors {; }]"
        } else {
            puts $batch_file_id $name
        }
    }

    close $batch_file_id
    incr file_index
}

close $inputFileList_id
close $error_file_id
}
