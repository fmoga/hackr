PIDFILE=`pwd`/django.pid

if [ -f $PIDFILE ]; then
  kill -9 `cat -- $PIDFILE`
  rm -f -- $PIDFILE
fi
