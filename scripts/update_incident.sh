#!/bin/bash

incident_type=$1
location=$2
who_did_update=$3

# sql -s test01/yoominchoi1234A@//localhost:1521/XEPDB1 <<EOF
sqlplus / as sysdba <<EOF
UPDATE incidents SET incident_type='$incident_type', location='$location', timestamp=SYSDATE, who_did_update='$who_did_update' WHERE incident_id=(SELECT incident_id FROM incidents ORDER BY timestamp DESC FETCH FIRST 1 ROWS ONLY);
COMMIT;
EXIT;
EOF
