#!/bin/bash

USER=massung1
PYENV_ROOT="/home/$USER/.pyenv"
PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

APPDIR="/home/$USER/metapy-demos"
PIDFILE=tmp/pids/nlp_app.pid
CONFIGFILE=contrib/nlp_app.cfg
META_CONFIG=nlp-config.toml

restart() {
  pushd $APPDIR > /dev/null
  source meta-pyenv/bin/activate
  if [ -e $PIDFILE ] && kill -0 $(cat $PIDFILE)
  then
    echo "Gunicorn is running, reloading..."
    kill -HUP $(cat $PIDFILE)
  else
    echo "Starting new gunicorn process..."
    gunicorn -c $CONFIGFILE "nlp_server:server('$META_CONFIG')"
  fi
  echo "Done!"
  popd > /dev/null
}

stop() {
  pushd $APPDIR > /dev/null
  if [ -e $PIDFILE ] && kill -0 $(cat $PIDFILE)
  then
    echo "Stopping gunicorn..."
    kill -QUIT $(cat $PIDFILE)
  fi
  echo "Done!"
  popd > /dev/null
}

case "$1" in
  start)
    restart
    ;;
  restart)
    restart
    ;;
  stop)
    stop
    ;;
  *)
    echo "Usage: {start|stop|restart}"
    exit 1
    ;;
esac
