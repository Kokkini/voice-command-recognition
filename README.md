# voice-command-recognition

## Installation
Follow the instruction in [Huongdan_CMU_Sphinx_LUMI.doc](Huongdan_CMU_Sphinx_LUMI.doc) to install Sphinx

## Create training data
- Record a few samples of training data (for example: data/small_recs). Save them using the same naming format as the example
- Format and annotate training data (this cut the training files into files with 1 command each then annotate those files in anno.fileids and anno.transcription)
```
cd data
python training_data_from_small_records.py -i small_recs -o formated_data
cd ..
```

## Train
- Return to the root directory of this repo and run the following command to train a new model. The new model will be saved in new_model.
```
./train.sh
```

## Detect
- To detect command from a file (for example: test.wav), run the following command. If you want to change the file to detect or the model to detect, 
change the variables AUDIO_INPUT_NAME and MODEL_DIR inside detect.sh. The results are saved in test_cuts_1104
```
./detect.sh
```
