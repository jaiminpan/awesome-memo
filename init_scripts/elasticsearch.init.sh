#!/bin/sh
#
# chkconfig: 345 99 01
# description: elastic
#
# File : elastic
#
# Description: Starts and stops the elastic server
#


ES_HOME=/data/appsoft/elastic

EXEC_BIN=${ES_HOME}/bin/elasticsearch

OPTIONS='-d'

PID_PATH=${ES_HOME}/config/elasitc.pid

PS_NAME=org.elasticsearch.bootstrap.Elasticsearch

EXEC_USER=elastic

# Source function library.
INITD=/etc/rc.d/init.d
source $INITD/functions

# Find the name of the script
NAME=`basename $0`
if [ ${NAME:0:1} = "S" -o ${NAME:0:1} = "K" ]
then
    NAME=${NAME:3}
fi

# For SELinux we need to use 'runuser' not 'su'
if [ -x /sbin/runuser ]
then
    SU=runuser
else
    SU=su
fi

start(){
    echo -n "Starting ${NAME} service: "
    $SU -l ${EXEC_USER} -c "${EXEC_BIN} ${OPTIONS} -p ${PID_PATH}"
    ret=$?
    if [ $ret -eq 0 ]
    then
        echo_success
    else
        echo_failure
        script_result=1
    fi
    echo
}

stop(){
    echo -n "Stopping ${NAME} service: "
    $SU -l ${EXEC_USER} -c "cat ${PID_PATH} | xargs kill"
    ret=$?
    if [ $ret -eq 0 ]
    then
        echo_success
    else
        echo_failure
        script_result=1
    fi
    echo
}

hardstop(){
    echo -n "Stopping (hard) ${NAME} service: "
    $SU -l ${EXEC_USER} -c "cat ${PID_PATH} | xargs kill -9"
    ret=$?
    if [ $ret -eq 0 ]
    then
        echo_success
    else
        echo_failure
        script_result=1
    fi
    echo
}

status(){
    c_pid=`ps -ef | grep $PS_NAME | grep -v grep | awk '{print $2}'`
    if [ "$c_pid" = "" ] ; then
      echo "Stopped"
      exit 3
    else
      echo "Running $c_pid"
      exit 0
    fi
}

# See how we were called.  
case "$1" in

  start|stop|status|hardstop)
    $1
    ;;
  *)
    echo "Usage: $0 {start|stop|hardstop|status}"
    exit 2
    ;;
esac

exit $script_result