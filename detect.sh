#!/bin/bash

INPUT_FILE=$1
AUDIO_INPUT_NAME="${INPUT_FILE%.*}"
EXTENSION="${INPUT_FILE##*.}"
if [ "$EXTENSION" == "mp3" ]; then
    ffmpeg -i "${AUDIO_INPUT_NAME}.mp3" -ar 16000 -ac 1 "${AUDIO_INPUT_NAME}.wav"
fi
MODEL_DIR="new_model"


TEMP_FILE="somethingrandom483bndh3.txt"
HOTWORD_FILE="hotword.dict"

AUDIO_FILE="${AUDIO_INPUT_NAME}.wav"
OUTPUT_DIR="${AUDIO_INPUT_NAME}_cuts_1104"

rm -R $OUTPUT_DIR
pocketsphinx_continuous -hmm $MODEL_DIR/en-us-adapt -dict $MODEL_DIR/cmudict-en-us.dict -kws $HOTWORD_FILE -time yes -infile $AUDIO_FILE > $TEMP_FILE
cat $TEMP_FILE
python truncate_file.py -audio $AUDIO_FILE -detection $TEMP_FILE -o $OUTPUT_DIR
