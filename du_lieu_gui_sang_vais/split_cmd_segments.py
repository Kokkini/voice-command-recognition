"""
Input: a wav file containing a series of commands, each about 1s apart from one another
Output: a directory of wav files, each containing 1 command
"""

import argparse
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS
from scipy.io import wavfile
import os

args = argparse.ArgumentParser()
args.add_argument('-i', help="input wav file")
args.add_argument('-o', help='output directory')
args.add_argument('-prefix', help='prefix of outputfile')
args = args.parse_args()

def truncate(data, rate, start, end):
    start = int(start*rate)
    end = min(len(data), int(end*rate))
    return data[start:end]

def split(infile, outdir, prefix, plot=False):
    os.makedirs(outdir, exist_ok=True)
    [rate, data] = aIO.read_audio_file(infile)
    segments = aS.silence_removal(data, rate, 0.020, 0.020, smooth_window = 1.0, weight = 0.3, plot=plot)
    for i, seg in enumerate(segments):
        outfile = os.path.join(outdir, f'{prefix}{i}.wav')
        seg_data = truncate(data, rate, seg[0], seg[1])
        wavfile.write(outfile, rate, seg_data)

if __name__ == "__main__":
    split(args.i, args.o, args.prefix, True)