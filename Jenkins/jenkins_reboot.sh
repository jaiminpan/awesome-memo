#!/bin/bash

###jdk
JAVA_HOME="/usr/local/java/jdk1.8.0_112"

APP_HOME="/home/java/{PROJ_DIR}"

PROFILE_ENV="prod"

PIP=`ls -l ${APP_HOME}/* |grep jar$ |head -1  |awk '{print $9}' | awk -F '/' '{print $5}' `
# PIP=`ls ${APP_HOME}/*  |grep jar$ | awk -F '/' '{print $5}' `

### get jar
APP_MAINCLASS="$PIP" 

JAVA_OPTS="-ms512m -mx512m -Xmn256m -Djava.awt.headless=true -XX:MaxPermSize=128m -Dfile.encoding=UTF-8 "

psid=0

##########################################checkpid()#################################
checkpid() {
   if [ -d $APP_HOME ] ;then
   echo "the $APP_HOME  has exist "
   else
   mkdir -p $APP_HOME
   fi

   javaps=`$JAVA_HOME/bin/jps -l | grep $APP_MAINCLASS`
   if [ -n "$javaps" ]; then
      psid=`echo $javaps | awk '{print $1}'`
   else
      psid=0  ####[ $psid -ne 0 ]
   fi

echo "checkpid:"+$psid
}

##########################################start()#################################
start() {
   checkpid
   if [ $psid -ne 0 ]; then
      echo "================================"
      echo "warn: $APP_MAINCLASS already started! (pid=$psid)"
      echo "================================"
   else
      echo -n "Starting $APP_MAINCLASS ..."
      cd $APP_HOME && nohup $JAVA_HOME/bin/java $JAVA_OPTS -jar $APP_HOME/$APP_MAINCLASS --spring.profiles.active=${PROFILE_ENV}> /dev/null 2>&1 &
      checkpid
      if [ $psid -ne 0 ]; then
         echo "(pid=$psid) [start OK]"
      else
         echo "[start Failed]"
         start
      fi
   fi
}


##########################################stoppid()#################################
stop() {
   checkpid
   if [ $psid -ne 0 ]; then
      echo -n "Stopping $APP_MAINCLASS ...(pid=$psid) "
      kill   $psid
      if [ $? -eq 0 ]; then
         echo "[stop OK]"
      else
         echo "[stop Failed]"
      fi

      checkpid
      if [ $psid -ne 0 ]; then
         stop   ###�~L�~A�~G~M�~]~@
      fi
   else
      echo "================================"
      echo "warn: $APP_MAINCLASS is not running"
      echo "================================"
   fi
}

##########################################backup()#################################
backup() {

   if [ ! -d $APP_HOME/backup ] ;then
     mkdir -p $APP_HOME/backup
   fi

   echo "********** Begin backup******************"
   echo "DELETE jar from $APP_HOME/backup"
   find $APP_HOME/backup -type f -name '*.jar' -delete
   echo "COPY $APP_HOME/$APP_MAINCLASS -> $APP_HOME/backup"
   cp $APP_HOME/$APP_MAINCLASS $APP_HOME/backup
   echo "********** End backup ******************"
}

##########################################status()#################################
status() {
   checkpid
   if [ $psid -ne 0 ];  then
      echo "$APP_MAINCLASS is running! (pid=$psid) and run time is :"
      ps -p  $psid -o pid,etime,uid,gid
   else
      echo "$APP_MAINCLASS is not running"
   fi
}

########################################## info() #################################
info() {
   echo "System Information:"
   echo "****************************"
   echo `head -n 1 /etc/issue`
   echo `uname -a`
   echo
   echo "JAVA_HOME=$JAVA_HOME"
   echo `$JAVA_HOME/bin/java -version`
   echo
   echo "APP_HOME=$APP_HOME"
   echo "APP_MAINCLASS=$APP_MAINCLASS"
   echo "****************************"
}

########################################## main() #################################

case "$1" in
   'start')
      start
      ;;
   'stop')
     stop
     ;;
   'restart')
     stop
     start
     ;;
   'status')
     status
     ;;
   'info')
     info
     ;;
   'backup')
     backup
     ;;
  *)
     echo "Usage: $0 {start|stop|restart|status|info|backup}"
     exit 1
esac
exit 0

