#!/bin/bash

AUDIO_INPUT_NAME="ok_lumi_test"
MODEL_DIR="my_more_data_model"


TEMP_FILE="somethingrandom483bndh3.txt"
HOTWORD_FILE="hotword.dict"

AUDIO_FILE="${AUDIO_INPUT_NAME}.wav"
OUTPUT_DIR="${AUDIO_INPUT_NAME}_cuts_1104"

rm -R $OUTPUT_DIR
pocketsphinx_continuous -hmm $MODEL_DIR/en-us-adapt -dict $MODEL_DIR/cmudict-en-us.dict -kws $HOTWORD_FILE -time yes -infile $AUDIO_FILE > $TEMP_FILE
cat $TEMP_FILE
python truncate_file.py -audio $AUDIO_FILE -detection $TEMP_FILE -o $OUTPUT_DIR
