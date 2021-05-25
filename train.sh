#!/bin/bash

NEW_MODEL_DIR="new_model"
rm -R $NEW_MODEL_DIR
cp -r basemodel $NEW_MODEL_DIR
cp data/anno.fileids $NEW_MODEL_DIR/anno.fileids
cp data/anno.transcription $NEW_MODEL_DIR/anno.transcription
cp -r data/formated_data $NEW_MODEL_DIR/formated_data
cd $NEW_MODEL_DIR
./train.sh
cd ..
