#!/usr/bin/env bash
#
# Runs Stanford CoreNLP server

# set this path to the directory where you decompressed StanfordCore
STANFORDDIR=stanford-corenlp-4.5.0


echo java -mx5g -cp \"$STANFORDDIR/*\" edu.stanford.nlp.pipeline.StanfordCoreNLPServer $*
java -mx5g -cp "$STANFORDDIR/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer $* &
echo $! > /tmp/corenlp-server.running
wait
rm /tmp/corenlp-server.running
