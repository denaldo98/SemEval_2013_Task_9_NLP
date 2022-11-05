#! /bin/bash

BASEDIR=../TaskData

# convert datasets to feature vectors
echo "Extracting features..."
python3 extract-features.py $BASEDIR/data/train/ > train.feat
python3 extract-features.py $BASEDIR/data/devel/ > devel.feat

# TEST
#python3 extract-features.py $BASEDIR/data/test/ > test.feat

# train CRF model
echo "Training CRF model..."
python3 train-crf.py model.crf < train.feat
# run CRF model
echo "Running CRF model..."
python3 predict.py model.crf < devel.feat > devel-CRF.out
# evaluate CRF results
echo "Evaluating CRF results..."
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/devel devel-CRF.out > devel-CRF.stats


# run CRF model on TEST
echo "Running CRF model on TEST..."
python3 predict.py model.crf < test.feat > test-CRF.out
# evaluate CRF results
echo "Evaluating CRF results on TEST..."
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/test test-CRF.out > test-CRF.stats




# train MEM model
echo "Training MEM model..."
cat train.feat | cut -f5- | grep -v ^$ > train.mem.feat
./megam-64.opt -nobias -nc -repeat 4 multiclass train.mem.feat > model.mem
rm train.mem.feat
# run MEM model
echo "Running MEM model..."
python3 predict.py model.mem < devel.feat > devel-MEM.out
# evaluate MEM results
echo "Evaluating MEM results..."
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/devel devel-MEM.out > devel-MEM.stats


# run MEM model on Test
echo "Running MEM model..."
python3 predict.py model.mem < test.feat > test-MEM.out
# evaluate MEM results on Test
echo "Evaluating MEM results..."
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/test test-MEM.out > test-MEM.stats
