"""
Input: a dir of wav file containing a series of commands, each about 1s apart from one another. NAME FORMAT: TAWST_DDEFN-<anything>.wav
Output: a directory of wav files, each containing 1 command, an anno and a transcript file
"""

import argparse
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS
from scipy.io import wavfile
import os

args = argparse.ArgumentParser()
args.add_argument('-i', help="input dir")
args.add_argument('-o', help='output directory')
# args.add_argument('-prefix', help='prefix of outputfile')
args = args.parse_args()

def truncate(data, rate, start, end):
    start = int(start*rate)
    end = min(len(data), int(end*rate))
    return data[start:end]

def get_cmd_from_file_name(filename):
    filename = filename[:-4] # remove .wav extension
    cmd = filename.split("-")[0]
    cmd = " ".join(cmd.split("_"))
    return cmd

def split(infile, outdir, plot=False):
    os.makedirs(outdir, exist_ok=True)
    [rate, data] = aIO.read_audio_file(infile)
    segments = aS.silence_removal(data, rate, 0.020, 0.020, smooth_window = 1.0, weight = 0.3, plot=plot)
    basename = os.path.basename(os.path.normpath(infile))
    for i, seg in enumerate(segments):
        outfile = os.path.join(outdir, f'{basename[:-4]}-{i}.wav')
        seg_data = truncate(data, rate, seg[0], seg[1])
        wavfile.write(outfile, rate, seg_data)

def split_dir(indir, outdir, plot=False):
    os.makedirs(outdir, exist_ok=True)
    for file in os.listdir(indir):
        if not file.endswith(".wav"): continue
        split(os.path.join(indir, file), outdir, plot)

def annotate(indir):
    fileids = []
    transcript = []
    for file in os.listdir(indir):
        if not file.endswith(".wav"): continue
        cmd = get_cmd_from_file_name(file)
        file_path = os.path.join(indir, file)
        fileids.append(file_path + "\n")
        transcript.append(f"<s> {cmd} </s> ({file_path})\n")
    with open("anno.fileids", "w") as f:
        f.writelines(fileids)
    with open("anno.transcription", "w") as f:
        f.writelines(transcript)

if __name__ == "__main__":
    split_dir(args.i, args.o)
    annotate(args.o)