BASEDIR=../TaskData
export PYTHONPATH=$BASEDIR/util

$BASEDIR/util/corenlp-server.sh -quiet true -port 9000 -timeout 15000  &
sleep 1

python3.10 parse_data.py $BASEDIR/data/train train
python3.10 parse_data.py $BASEDIR/data/devel devel


kill `cat /tmp/corenlp-server.running`



