from pydub import AudioSegment
from pydub.playback import play
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS
from scipy.io import wavfile
import copy
import os
import random
import traceback
import numpy as np

import argparse

args = argparse.ArgumentParser()
args.add_argument("-mode", help="0: remove leading and trailing silence, 1: normalize loudness, 2: randomly change loudness")
args.add_argument("-f", action="store_true", help="if set, process 1 file instead of a whole region directory")
args.add_argument("-i", help="input region dir")
args.add_argument("-o", help="output region dir")
args = args.parse_args()

def truncate(data, rate, start, end):
    start = int(start*rate)
    end = min(len(data), int(end*rate))
    return data[start:end]

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def remove_head_tail_silence(data, rate, plot=False):
    bridge_duration = 0.2
    data = copy.deepcopy(data)
    abs_data = np.abs(data)
    segments = aS.silence_removal(data, rate, 0.020, 0.020, smooth_window = 1.0, weight = 0.3, plot=plot)
    if len(segments) == 0:
        return data
    segments = sorted(segments)
    # get the loudest segment
    loudness = []
    for a, b in segments:
        loudness.append(np.max(abs_data[int(a*rate):int(b*rate)]))
    loudest_index = np.argmax(loudness)
    start, end = segments[loudest_index]
    for i in range(loudest_index+1, len(segments)):
        if segments[i][0] - end < bridge_duration:
            end = segments[i][1]
        else:
            break
    for i in range(0, loudest_index):
        if start - segments[i][1] < bridge_duration:
            start = segments[i][0]
        else:
            break
    return truncate(data, rate, start, end)

def remove_head_tail_silence_from_file(infile, outfile, min_duration=2, plot=False):
    [Fs, x] = aIO.read_audio_file(infile)
    if len(x) < min_duration * Fs:
        raise Exception("input data too short")
    x = remove_head_tail_silence(x, Fs, plot)
    wavfile.write(outfile, Fs, x)

def randomize_loudness_from_file(infile, outfile):
    audio = AudioSegment.from_wav(infile)
    # normalize
    audio = match_target_amplitude(audio, -30.0)
    num_dB = random.randint(-15, 15)
    audio = audio + num_dB
    audio.export(outfile, format='wav')

def normalize_loudness_from_file(infile, outfile):
    audio = AudioSegment.from_wav(infile)
    audio = match_target_amplitude(audio, -30.0)
    audio.export(outfile, format='wav')

if __name__ == "__main__":
    if args.f:
        infile = args.i
        outfile = args.o
        if args.mode == "0":
            remove_head_tail_silence_from_file(infile, outfile, 0, True)
        elif args.mode == "1":
            normalize_loudness_from_file(infile, outfile)
        elif args.mode == "2":
            randomize_loudness_from_file(infile, outfile)
    else:
        os.makedirs(args.o, exist_ok=True)
        for distance in os.listdir(args.i):
            distance_dir = os.path.join(args.i, distance)
            if not os.path.isdir(distance_dir): continue
            distance_dir_out = os.path.join(args.o, distance)
            os.makedirs(distance_dir_out, exist_ok=True)
            for person in os.listdir(distance_dir):
                person_dir = os.path.join(distance_dir, person)
                if not os.path.isdir(person_dir): continue
                person_dir_out = os.path.join(distance_dir_out, person)
                os.makedirs(person_dir_out, exist_ok=True)
                for file in os.listdir(person_dir):
                    ext = file.split(".")[1]
                    if ext != "wav": continue
                    infile = os.path.join(person_dir, file)
                    outfile = os.path.join(person_dir_out, file)
                    print(infile)
                    try:
                        if args.mode == "0":
                            remove_head_tail_silence_from_file(infile, outfile)
                        elif args.mode == "1":
                            normalize_loudness_from_file(infile, outfile)
                        elif args.mode == "2":
                            randomize_loudness_from_file(infile, outfile)
                    except:
                        print("failed on:", infile)
                        traceback.print_exc()