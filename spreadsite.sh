#! /bin/sh

rundir=/home/pdc/Sites/spreadsite.org/spreadsite
pidfile=../log/spreadsite.pid
outlog=../log/spreadsite.stdout.log
errlog=../log/spreadsite.stderr.log
settings=settings_production

cd $rundir

case $1 in
    start)
	date '+%Y-%m-%d:%H:%M:%S starting' >> $outlog
	date '+%Y-%m-%d:%H:%M:%S starting' >> $errlog
	./manage.py runfcgi protocol=fcgi \
		host=127.0.0.1 port=9001 method=prefork \
		workdir=$rundir \
		pidfile=$pidfile outlog=$outlog errlog=$errlog \
		--settings=settings_production \
	    && echo started
	date '+%Y-%m-%d:%H:%M:%S started' >> $outlog
	date '+%Y-%m-%d:%H:%M:%S started' >> $errlog
	;;
    stop)
	date '+%Y-%m-%d:%H:%M:%S stopping' >> $outlog
	date '+%Y-%m-%d:%H:%M:%S stopping' >> $errlog
	kill -HUP `cat $pidfile` && echo stopped
	date '+%Y-%m-%d:%H:%M:%S stopped' >> $outlog
	date '+%Y-%m-%d:%H:%M:%S stopped' >> $errlog
	;;
    *)
	echo $1: unknown command: must be one of start, stop >2
	exit 2
	;;
esac
