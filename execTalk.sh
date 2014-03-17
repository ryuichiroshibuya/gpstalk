#!/bin/bash -x
. /home/pi/.bash_profile
DATE=$(date "+%Y%m%d%H%M")
BASE=$(cd $(dirname $0);pwd)
SQLFILE=logs/sample_${DATE}.sql

cd $BASE
./setGPS.sh $(python getGPS.py) > ${SQLFILE}
./jsay $(cat ${SQLFILE} | psql -At pgis)
