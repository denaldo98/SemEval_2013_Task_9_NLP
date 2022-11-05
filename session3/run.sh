#! /bin/bash

BASEDIR=../
export PYTHONPATH=$BASEDIR/util

$BASEDIR/TaskData/util/corenlp-server.sh -quiet true -port 9000 -timeout 15000  &
sleep 1

#python3 baseline-DDI.py $BASEDIR/TaskData/data/devel devel.out > devel.stats
python3 baseline-DDI.py $BASEDIR/TaskData/data/test test.out > test.stats

kill `cat /tmp/corenlp-server.running`
sleep 1
