# ###################################################################################
# Purpose of TCL Script - To Extract all Supplier/Impacted Site name present in TRU	#
#         				  and create batch files for bulk load in SpecRight			#
#  Developed By 		- Aniket Ghosh TCS				  							#
# ###################################################################################

tcl;
eval {

set output [split [mql temp que bus "Organization" * * select name dump ~;] "\n"]
set inputFileList_dir "/apps/Aniket"
set inputFileList_path "$inputFileList_dir/inputFileList.txt"
set input_dir "$inputFileList_dir/input"
set batch_size 100
set total_lines [llength $output]
set file_index 1
set inputFileList_id [open $inputFileList_path "w"]

file mkdir $input_dir
file mkdir $inputFileList_dir

for {set i 0} {$i < $total_lines} {incr i $batch_size} {

    set batch [lrange $output $i [expr {$i + $batch_size - 1}]]
    set batch_filename [format "batch_%03d.txt" $file_index]
	
    set full_batch_path "$input_dir/$batch_filename"
	puts $inputFileList_id $batch_filename
	
    set batch_file_id [open $full_batch_path "w"]
	
    foreach line $batch {
        set names [split $line "~"]
        set last_name [string trim [lindex $names end]]
        puts $batch_file_id $last_name
    }
	
    close $batch_file_id
    incr file_index
}
close $inputFileList_id
}
