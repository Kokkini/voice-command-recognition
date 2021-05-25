"""
From the output of pocketsphinx_continous, get the segment and cut the original 
wav file into detected segments
"""
import os
from numpy.lib.function_base import piecewise
from scipy.io import wavfile
import argparse

args = argparse.ArgumentParser()
args.add_argument('-audio', help="input audio file")
args.add_argument('-detection', help='output of pocketsphinx_continous')
args.add_argument('-o', help="output directory")
args = args.parse_args()

def truncate(data, rate, start, end):
    start = int(start*rate)
    end = min(len(data), int(end*rate))
    return data[start:end]

def get_segments_from_detection(detection_file):
    with open(detection_file) as f:
        content = f.readlines()
    segments = []
    for line in content:
        pieces = line.split()
        try:
            start = float(pieces[-3])
            end = float(pieces[-2])
            confidence = float(pieces[-1])
            segments.append([" ".join(pieces[:-3]), start, end, confidence])
        except:
            continue
    return segments
            

output_dir = args.o #"cuts_tat_den_test"
audio_file = args.audio #"tat_den_test.wav"
detection_file = args.detection #"detection3.txt"

# segments = [[1.450, 2.270], [4.790, 5.320], [3.040, 3.890], [6.510, 7.300], [8.090, 8.530], [9.780, 10.550], [11.660, 12.280], [15.120, 15.840], [11.490, 11.920]]
segments = get_segments_from_detection(detection_file)
os.makedirs(output_dir, exist_ok=True)
[rate, data] = wavfile.read(audio_file)
print(rate)
segments = sorted(segments, key=lambda x: x[1])
# for i, (word, start, end, confidence) in enumerate(segments):
#     print(word, start, end, confidence)
#     piece = truncate(data, rate, start, end)
#     filename = os.path.join(output_dir, f"{i}-{word}-{start}.wav")
#     wavfile.write(filename, rate, piece)
confidence_boost = {
    "TAWST DDEFN": 0.02
}
for seg in segments:
    print(seg)
    seg[-1] += confidence_boost.get(seg[0], 0)

print()

for seg in segments:
    print(seg)
    
i = 0
while i < len(segments):
    word, start, end, confidence = segments[i]
    if i+1 < len(segments):
        word, start, end, confidence = segments[i]
        word2, start2, end2, confidence2 = segments[i+1]
        if (end - start2) / (end2 - start) > 0.4:
            if confidence2 > confidence:
                word, start, end, confidence = segments[i+1]
            i+=1
    
    print(word, start, end, confidence)
    piece = truncate(data, rate, start, end)
    filename = os.path.join(output_dir, f"{i}-{word}-{start}.wav")
    wavfile.write(filename, rate, piece)
    i+=1


    
