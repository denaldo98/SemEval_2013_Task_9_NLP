#!/usr/bin/env python3

import pycrfsuite
import sys
from contextlib import redirect_stdout

def instances(fi):
    xseq = []
    yseq = []
    
    for line in fi:
        line = line.strip('\n')
        if not line:
            # An empty line means the end of a sentence.
            # Return accumulated sequences, and reinitialize.
            yield xseq, yseq
            xseq = []
            yseq = []
            continue

        # Split the line with TAB characters.
        fields = line.split('\t')
        
        # Append the item features to the item sequence.
        # fields are:  0=sid, 1=form, 2=span_start, 3=span_end, 4=tag, 5...N = features
        item = fields[5:]        
        xseq.append(item)
        
        # Append the label to the label sequence.
        yseq.append(fields[4])


if __name__ == '__main__':

    c2_coeffs = [0.1, 0.01, 1e-03, 1e-04, 1e-05]
    deltas = [1e-02, 1e-03, 1e-04, 1e-03, 1e-06]
    min_freqs = [2, 6, 12]
    max_iters = [100, 1000, 1500]
    cal_etas = [1e-05, 1e-03, 0.5]

    for freq in min_freqs:
        for c2 in c2_coeffs:
            for delta in deltas:
                for max_itr in max_iters:
                    for eta in cal_etas:

                        modelfile = "crf_models/" + "model" + "" + "freq:" + str(freq) + "" + "c2:" + str(c2) + "" + "delta:" + str(delta) + "" + "maxitr:" + str(max_itr) + "_" + "eta:" + str(eta) +  ".crf"
                        #modelfile = "crf_models/model.crf"

                        # Create a Trainer object.
                        trainer = pycrfsuite.Trainer()
                                                
                        # Read training instances from STDIN, and append them to the trainer.
                        with open('train.feat', 'r') as f:
                            training = f
                            for xseq, yseq in instances(training):
                                #for xseq, yseq in instances(sys.stdin):
                                trainer.append(xseq, yseq, 0)

                    # trainer.select('l2sgd', 'crf1d')
                        #trainer.set('feature.minfreq', 1)
                        #trainer.set('c2', 0.1)

                        # Use L2-regularized SGD and 1st-order dyad features.
                        trainer.select('l2sgd', 'crf1d')
                        trainer.set('feature.minfreq', freq)
                        trainer.set('c2', c2)
                        trainer.set('delta', delta)
                        trainer.set('max_iterations', max_itr)
                        trainer.set('calibration.eta', eta)

                        print("Obtain the list of possible parameters for L2-regularizer")
                        print(trainer.params())

                        print("Training with following parameters: ")
                        for name in trainer.params():
                            print (name, trainer.get(name), trainer.help(name), file=sys.stderr)
                                                
                        # Start training and dump model to modelfile
                        trainer.train(modelfile, -1)