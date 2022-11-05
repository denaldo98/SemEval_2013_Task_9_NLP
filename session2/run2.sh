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
python3 train-crf.py
# run CRF model
echo "Running CRF model..."
python3 predict.py
# evaluate CRF results
echo "Evaluating CRF results..."
python3 $BASEDIR/util/evaluator.py $BASEDIR/data/devel ./devel-CRFs


# run CRF model on TEST
#echo "Running CRF model on TEST..."
#python3 predict.py model.crf < test.feat > test-CRF.out
# evaluate CRF results
#echo "Evaluating CRF results on TEST..."
#python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/test test-CRF.out > test-CRF.stats




