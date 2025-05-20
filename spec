echo "Working"

VDATE=`date +%Y-\%m-\%d_\%H.\%M`
cronStartDate=`date`
FileDynamics=`date +%m\%d\%Y`

START_DATE = "5/216/2025 7:40:00 AM"

echo `$VDATE`

mql -c "verb on; set context user creator pass Tru@2018x;temp query bus \"Business Unit\" * * where \"originated > '5/16/2025 7:40:00 AM' && current=='Active'\" select id;"

