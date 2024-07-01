#!/bin/bash


# sql -s TEST01/yoominchoi1234A@//localhost:1521/XEPDB1 <<EOF
sqlplus / as sysdba <<EOF
SET PAGESIZE 50
SET LINESIZE 200
SET FEEDBACK OFF
SET HEADING OFF
SELECT * FROM incidents ORDER BY timestamp DESC;
EXIT;
EOF
