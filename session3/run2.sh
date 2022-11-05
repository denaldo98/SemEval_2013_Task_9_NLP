#! /bin/bash

BASEDIR=../
export PYTHONPATH=$BASEDIR/util

$BASEDIR/TaskData/util/corenlp-server.sh -quiet true -port 9000 -timeout 15000  &
sleep 1

python3 explore.py $BASEDIR/TaskData/data/train  > svo.check

kill `cat /tmp/corenlp-server.running`
sleep 1
