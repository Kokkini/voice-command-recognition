# voice-command-recognition

## Installation
Follow the instruction in [Huongdan_CMU_Sphinx_LUMI.doc](Huongdan_CMU_Sphinx_LUMI.doc) to install Sphinx

## Create training data
- Record a few samples of training data (for example: data/small_recs). Save them using the same naming format as the example. If the file is not a wav file with sample rate 16kHz, convert it using this command
```
ffmpeg -i OK_LUMI.mp3 -ar 16000 -ac 1 OK_LUMI.wav
```
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
- To detect command from a file (for example: test.wav), run the following command. The results are saved in test_cuts_1104
```
./detect.sh test.wav
```

## Detect from microphone
- To do live detection from the microphone, run the following command. It works best for mic that records at sample rate 16kHz. Different sample rates will result in lower accuracy. 
```
./detect_mic.sh
```

## Change the keywords to detect
- All possible keywords are listed in hotword.dict. If you don't want to detect some keywords, you can delete them from the file. For example, if you want to detect only OK LUMI, delete everything except the OK_LUMI line.
```
./detect.sh test.wav
```