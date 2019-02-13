#!/bin/bash
set +o posix

CMD_PATH="consul"
CONFIG_DIRECTORY="consul.d/client"
LOG_FILE="consul.log"
DAEMON_RUNNABLE="true"

# Fail fast with concise message when cwd does not exist
if ! [[ -d "$PWD" ]]; then
  echo "Error: The current working directory doesn't exist, cannot proceed." >&2
  exit 1
fi

quiet_cd() {
  cd "$@" >/dev/null || return
}

onwarn() {
  if [[ -t 2 ]] # check whether stderr is a tty.
  then
    echo -ne "\\033[4;31mWarn\\033[0m: " >&2 # highlight Warb with underline and red color
  else
    echo -n "Warn: " >&2
  fi
  if [[ $# -eq 0 ]]
  then
    cat >&2
  else
    echo "$*" >&2
  fi
}

onoe() {
  if [[ -t 2 ]] # check whether stderr is a tty.
  then
    echo -ne "\\033[4;31mError\\033[0m: " >&2 # highlight Error with underline and red color
  else
    echo -n "Error: " >&2
  fi
  if [[ $# -eq 0 ]]
  then
    cat >&2
  else
    echo "$*" >&2
  fi
}

odie() {
  onoe "$@"
  exit 1
}

SHELL_FILE_DIRECTORY="$(quiet_cd "${0%/*}/" && pwd -P)"

if [[ -f "${CMD_PATH}" ]]
then
  CMD_FULL_PATH="${CMD_PATH}"
else
  CMD_FULL_PATH="$SHELL_FILE_DIRECTORY/${CMD_PATH}"
fi

if [[ -d "${CONFIG_DIRECTORY}" ]]
then
  CONFIG_DIR_FULL_PATH="${CONFIG_DIRECTORY}"
else
  CONFIG_DIR_FULL_PATH="$SHELL_FILE_DIRECTORY/${CONFIG_DIRECTORY}"
fi

if [[ -f "${LOG_FILE}" ]]
then
  LOG_FILE_FULL_PATH="${LOG_FILE}"
else
  LOG_FILE_FULL_PATH="$SHELL_FILE_DIRECTORY/${LOG_FILE}"
fi

if ! [[ -f "${CMD_FULL_PATH}" ]]
then
  odie "Command $CMD_FULL_PATH not exists"
fi

if ! [[ -d "${CONFIG_DIR_FULL_PATH}" ]]
then
  odie "Directory $CONFIG_DIR_FULL_PATH not exists"
fi

if [[ -f "${LOG_FILE_FULL_PATH}" ]]
then
  onwarn "Log file $LOG_FILE_FULL_PATH exists"
fi


if [[ -n "$DAEMON_RUNNABLE" ]]
then
  echo "Daemon run"
  nohup ${CMD_FULL_PATH} agent -config-dir=${CONFIG_DIR_FULL_PATH} 2>&1 > ${LOG_FILE_FULL_PATH} &
else
  ${CMD_FULL_PATH} agent -config-dir=${CONFIG_DIR_FULL_PATH}
fi


