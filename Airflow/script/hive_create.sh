#!/bin/bash

TEMPFILE=`mktemp`
echo $TEMPFILE

TARGET=$1

CURID=$RANDOM
YEAR=`date -d '1 days ago' +%Y`
MONTH=`date -d '1 days ago' +%m`
DAY=`date -d '1 days ago' +%d`


CMDDATA="alter table content_r1 add partition (y='$YEAR', m='$MONTH', d='$DAY') location 'hdfs://mwa/mw/data/tracking/v4/C/$YEAR/$MONTH/$DAY'; alter table request_r1 add partition (y='$YEAR', m='$MONTH', d='$DAY') location 'hdfs://mwa/mw/data/tracking/v4/I/$YEAR/$MONTH/$DAY';
"


#CMDDATA="alter table test_txt add partition (y='$YEAR', m='$MONTH', d='$MIN') location 'hdfs://mwa/mw/data/test/C/$YEAR/$MONTH/$MIN';"


echo $CMDDATA > $TEMPFILE

scp -r $TEMPFILE hive@$TARGET:/tmp/airflow_job.$CURID.sh

ssh hive@$TARGET "hive -f /tmp/airflow_job.$CURID.sh"

exit $?
