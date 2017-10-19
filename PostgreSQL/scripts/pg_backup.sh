#!/bin/env bash

TARGET_DAY=`date -d '0 days' +%Y%m%d`


TARGET_DIR=/data/appdatas/pg_base/base${TARGET_DAY}
LOG_DIR=/data/applogs/pg_base/${TARGET_DAY}.log

if [ ! -d "${TARGET_DIR}" ]; then
    mkdir "${TARGET_DIR}" && pg_basebackup -D "${TARGET_DIR}" -Ft -Xf -v -P -h 10.81.5.1 -p 15432 > $LOG_DIR 2>&1
fi
