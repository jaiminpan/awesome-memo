#!/bin/bash
## Using after source env.sh

prog=$0
RETVAL=0

BIN_PATH=/opt/appsoft/druid-0.9.2/bin

start() {
		echo -n $"Starting $prog: "

		${BIN_PATH}/historical.sh start
		${BIN_PATH}/coordinator.sh start
		${BIN_PATH}/broker.sh start
		${BIN_PATH}/middleManager.sh start
		${BIN_PATH}/overlord.sh start

		return $RETVAL
}

stop() {
		echo $"Stoping $prog: "

		${BIN_PATH}/overlord.sh stop
		${BIN_PATH}/middleManager.sh stop
		${BIN_PATH}/broker.sh stop
		${BIN_PATH}/coordinator.sh stop
		${BIN_PATH}/historical.sh stop
}

status() {
		echo $"Status $prog: "

		echo -n "historical: "
		${BIN_PATH}/historical.sh status

		echo -n "coordinator: "
		${BIN_PATH}/coordinator.sh status

		echo -n "broker: "
		${BIN_PATH}/broker.sh status

		echo -n "middleManager: "
		${BIN_PATH}/middleManager.sh status

		echo -n "overlord: "
		${BIN_PATH}/overlord.sh status

		return $RETVAL
}

restart() {
		stop
		start
}

echo "Using conf: " $DRUID_CONF_DIR

case "$1" in
		start)
				start
				;;
		stop)
				stop
				;;
		status)
				status
				;;
		restart)
				restart
				;;
		*)
				echo $"Usage: $prog {start|stop|restart|status}"
				RETVAL=2
esac

exit $RETVAL
