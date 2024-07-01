#!/bin/bash

incident_type=$1
location=$2
who_did_update=$3

# sql -s test01/yoominchoi1234A@//localhost:1521/XEPDB1 <<EOF
sqlplus sys@localhost:1521/freepdb1 as sysdba <<EOF
INSERT INTO incidents (incident_type, location, who_did_update) VALUES ('$incident_type', '$location', '$who_did_update');
COMMIT;
EXIT;
EOF
