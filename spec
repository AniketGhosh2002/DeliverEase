tcl;
eval {
 
set base_dir [pwd]  
set supplier_site_path "$base_dir/SupplierSiteFile.csv"
 
# ------------------------------------------------
# STEP 1: Process Active Supplier / Impacted Sites
# ------------------------------------------------
set output [split [mql temp que bus "Organization" * * where "current==Active" select id current attribute\[Entity Type\].value attribute\[Organization Phone Number\].value attribute\[Organization Fax Number\].value attribute\[Postal Code\].value attribute\[State/Region\].value attribute\[Alternate Name\].value attribute\[City\].value attribute\[Country\].value attribute\[Web Site\].value attribute\[Region\].value dump ==;] "\n"]
 
set supplier_site_id [open $supplier_site_path "w"]
 
puts $supplier_site_id "\"Type\",\"Name\",\"Revision\",\"Object Id\",\"Region\",\"State/Region\",\"Entity Type\",\"Organization Phone Number\",\"Organization Fax Number\",\"Postal Code\",\"Web Site\",\"Alternate Name\",\"City\",\"Country\",\"Validation Comment\""
 
proc csv_escape {field} {
    regsub -all {"} $field {""} field
    return "\"$field\""
}
 
foreach line $output {
    set fields              [split $line "=="]
	set type            [string trim [lindex $fields 0]]
	set name            [string trim [lindex $fields 1]]
	set rev             [string trim [lindex $fields 2]]
    set objectId        [string trim [lindex $fields 3]]
	set current         [string trim [lindex $fields 4]]
    set entityType      [string trim [lindex $fields 5]]
    set phone           [string trim [lindex $fields 6]]
	set fax             [string trim [lindex $fields 7]]
	set pin             [string trim [lindex $fields 8]]
	set state           [string trim [lindex $fields 9]]
	set alternateName   [string trim [lindex $fields 10]]
	set city            [string trim [lindex $fields 11]]
	set country         [string trim [lindex $fields 12]]
	set website         [string trim [lindex $fields 13]]
	set region1         [string trim [lindex $fields 14]]
	set region2         [string trim [lindex $fields 15]]
	set region3         [string trim [lindex $fields 16]]
	set region4         [string trim [lindex $fields 17]]
	set region5         [string trim [lindex $fields 18]]
 
	set allowedRegions {"Global" "North America" "Latin America" "Asia Pacific" "EMEA"}
	set allowedEntityTypes {"Other" "Supplier: Manufacturer" "Supplier: Distributor" "Business Location" "R&D" "Laboratory" "Co-packers" "Marketing Company" "Internal Manufacturing" "External Packaging" "External Manufacturing" "Distribution Center" "Company"}
 
    set errors {}
    if {$entityType eq ""} {
        lappend errors "Missing Entity Type"
    } elseif {[lsearch -exact $allowedEntityTypes $entityType] == -1} {
		lappend errors "Invalid Entity Type: $entityType"
	}
    if {$region1 eq ""} {
		lappend errors "Missing Region"
	} elseif {[lsearch -exact $allowedRegions $region] == -1} {
		lappend errors "Invalid Region: $region"
	}
    if {$name eq ""} {
        lappend errors "Missing Name for Object Id - $objectId"
    }
	if {[string length $name] > 255} {
        lappend errors "Name too long ([string length $name] chars)"
    }
	if {[string length $state] > 255} {
        lappend errors "State too long ([string length $state] chars)"
    }
    if {[string length $phone] > 40} {
        lappend errors "Phone Number too long ([string length $phone] chars)"
    }
	if {[string length $fax] > 40} {
        lappend errors "Fax Number too long ([string length $fax] chars)"
    }
	if {[string length $pin] > 20} {
        lappend errors "Postal Code too long ([string length $pin] chars)"
    }
	if {[string length $website] > 255} {
        lappend errors "Web Site too long ([string length $website] chars)"
    }
	if {[string length $alternateName] > 255} {
        lappend errors "Alternate Name too long ([string length $alternateName] chars)"
    }
	if {[string length $city] > 255} {
        lappend errors "City too long ([string length $city] chars)"
    }
	if {[string length $country] > 255} {
        lappend errors "Country too long ([string length $country] chars)"
    }
 
	set validationComment [join $errors {; }]
 
	# Write CSV row
	puts $supplier_site_id [join [list \
    [csv_escape $type] \
    [csv_escape $name] \
    [csv_escape $rev] \
    [csv_escape $objectId] \
    [csv_escape $region] \
    [csv_escape $state] \
    [csv_escape $entityType] \
    [csv_escape $phone] \
    [csv_escape $fax] \
    [csv_escape $pin] \
    [csv_escape $website] \
    [csv_escape $alternateName] \
    [csv_escape $city] \
    [csv_escape $country] \
    [csv_escape $validationComment] \ ] ","]
}
 
close $supplier_site_id

}
