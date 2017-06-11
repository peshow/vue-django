#!/usr/bin/env sh
#
DIR=/var/spool/cron/
CRON_FILE=/etc/crontab

cd $DIR
for file in $(ls);do
    echo user:$file
    cat $file
done

cron_record=$(egrep "^([0-9*-\/]\s+){5}" $CRON_FILE &> /dev/null)

if [ "$?" == "0" ];then
    echo user:$CRON_FILE
    egrep "^([0-9*-\/]\s+){5}" $CRON_FILE
fi
