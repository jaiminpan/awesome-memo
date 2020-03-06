#!/bin/bash

# consul service api

CONSUL_NODE="127.0.0.1:8500"
SERVICE_NAME=${CURRENT_SERVICE_NAME}

########################################## info() #################################
info() {
  echo "****************************"
  echo "CONSUL_NODE=$CONSUL_NODE"
  echo "SERVICE_NAME=$SERVICE_NAME"

  SERVICE_IDS=`curl http://${CONSUL_NODE}/v1/agent/services | python -m json.tool | grep ID | awk '{print $2}'|sed 's/["|,]//g' | grep ${SERVICE_NAME}`

  echo "SERVICE_IDS=$SERVICE_IDS"
  echo "****************************"
}

########################################## pause() #################################
pause() {
  SERVICE_IDS=`curl http://${CONSUL_NODE}/v1/agent/services | python -m json.tool | grep ID | awk '{print $2}'|sed 's/["|,]//g' | grep ${SERVICE_NAME}`
  for SERVICE_ID in ${SERVICE_IDS}
  do
    echo "Service \"${SERVICE_ID}\" pause "
    curl -s -XPUT "http://$CONSUL_NODE/v1/agent/service/maintenance/${SERVICE_ID}?enable=true&reason=${SERVICE_NAME}_deploying"
  done
}

########################################## resume() #################################
resume() {
  SERVICE_IDS=`curl http://${CONSUL_NODE}/v1/agent/services | python -m json.tool | grep ID | awk '{print $2}'|sed 's/["|,]//g' | grep ${SERVICE_NAME}`
  for SERVICE_ID in ${SERVICE_IDS}
  do
    echo "Service \"${SERVICE_ID}\" resume "
    curl -s -XPUT "http://$CONSUL_NODE/v1/agent/service/maintenance/${SERVICE_ID}?enable=false"
  done
}

case "$1" in

   'info')
     info
     ;;
   'pause')
     pause
     ;;
   'resume')
     resume
     ;;
  *)
     echo "Usage: $0 {pause|resume|info}"
     exit 1
esac
exit 0