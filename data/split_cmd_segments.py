"""
Input: a wav file containing a series of commands, each about 1s apart from one another
Output: a directory of wav files, each containing 1 command
"""

import argparse
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS
from scipy.io import wavfile
import os
from audiomentations import *
import numpy as np
import librosa
from tqdm import tqdm

args = argparse.ArgumentParser()
args.add_argument('-i', help="input wav file")
args.add_argument('-o', help='output directory')
args.add_argument('-prefix', help='prefix of outputfile')
args = args.parse_args()

augment = Compose([
    PolarityInversion(p=0.5),
    LoudnessNormalization(min_lufs_in_db=-31, max_lufs_in_db=-13, p=1.0),
    AddBackgroundNoise("background_noises", min_snr_in_db=3, max_snr_in_db=30, p=1.0),
    Gain(min_gain_in_db=-6, max_gain_in_db=12, p=1.0),
    AddGaussianSNR(max_SNR=0.1, p=1.0),
    TimeStretch(min_rate=0.8, max_rate=1.25, p=0.5, leave_length_unchanged=False),
    PitchShift(min_semitones=-1, max_semitones=1, p=0.5),
    ClippingDistortion(max_percentile_threshold=10, p=0.5), #Distort signal by clipping a random percentage of points
])

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

def augment_from_dir(indir, num_replica=10):
    for file in os.listdir(indir):
        if not file.endswith(".wav"): continue
        filename, ext = os.path.splitext(file)
        samples, rate = librosa.load(os.path.join(indir, file), sr=None)
        for i in tqdm(range(10)):
            augmented_samples = augment(samples=samples, sample_rate=rate)
            wavfile.write(f"{indir}/{filename}a{i}.wav", rate, augmented_samples)

if __name__ == "__main__":
    split(args.i, args.o, args.prefix, True)
    # augment_from_dir(args.o, num_replica=10)