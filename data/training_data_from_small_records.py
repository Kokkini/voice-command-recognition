"""
Input: a dir of wav file containing a series of commands, each about 1s apart from one another. NAME FORMAT: TAWST_DDEFN-<anything>.wav
Output: a directory of wav files, each containing 1 command, an anno and a transcript file
"""

import argparse
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS
from scipy.io import wavfile
import os
import shutil
from audiomentations import *
import numpy as np
import librosa
from tqdm import tqdm
import soundfile as sf
import pyrubberband


args = argparse.ArgumentParser()
args.add_argument('-i', help="input dir")
args.add_argument('-o', help='output directory')
# args.add_argument('-prefix', help='prefix of outputfile')
args = args.parse_args()

augment = Compose([
    PolarityInversion(p=0.5),
    LoudnessNormalization(min_lufs_in_db=-31, max_lufs_in_db=-13, p=1.0),
    # AddBackgroundNoise("background_noises", min_snr_in_db=3, max_snr_in_db=50, p=1.0),
    Gain(min_gain_in_db=-6, max_gain_in_db=12, p=1.0),
    # AddGaussianSNR(max_SNR=0.1, p=1.0),
    # TimeStretch(min_rate=0.8, max_rate=1.25, p=0.5, leave_length_unchanged=False),
    # PitchShift(min_semitones=-3, max_semitones=3, p=0.5),
    # ClippingDistortion(max_percentile_threshold=10, p=0.5), #Distort signal by clipping a random percentage of points
])

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


def augment_from_dir(indir, num_replica=10):
    for file in tqdm(os.listdir(indir)):
        if not file.endswith(".wav"): continue
        filename, ext = os.path.splitext(file)
        samples, rate = librosa.load(os.path.join(indir, file), sr=None)
        for i in range(num_replica):
            augmented_samples = augment(samples=samples, sample_rate=rate)
            augmented_samples = pyrubberband.pitch_shift(augmented_samples, rate, np.random.normal(0,1.5))
            augmented_samples = pyrubberband.time_stretch(augmented_samples, rate, np.random.uniform(0.8, 1.25))
            # wavfile.write(f"{indir}/{filename}a{i}.wav", rate, augmented_samples)
            sf.write(f"{indir}/{filename}a{i}.wav", augmented_samples, rate, 'PCM_24')

def annotate(indir):
    fileids = []
    transcript = []
    for file in os.listdir(indir):
        if not file.endswith(".wav"): continue
        cmd = get_cmd_from_file_name(file)
        file_path = os.path.join(indir, file[:-4])
        fileids.append(file_path + "\n")
        transcript.append(f"<s> {cmd} </s> ({file_path})\n")
    with open("anno.fileids", "w") as f:
        f.writelines(fileids)
    with open("anno.transcription", "w") as f:
        f.writelines(transcript)

if __name__ == "__main__":
    if os.path.exists(args.o):
        shutil.rmtree(args.o)
    split_dir(args.i, args.o)
    augment_from_dir(args.o, num_replica=30)
    annotate(args.o)