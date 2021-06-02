import argparse
# from audiomentations.augmentations.transforms import AddShortNoises
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS
from scipy.io import wavfile
import os
from audiomentations import * #Compose, AddGaussianNoise, TimeStretch, PitchShift, Shift, Gain, LoudnessNormalization
import numpy as np
import librosa
from tqdm import tqdm
import soundfile as sf

rate = 16000

augment = Compose([
    PolarityInversion(p=0.5),
    LoudnessNormalization(min_lufs_in_db=-31, max_lufs_in_db=-13, p=1.0),
    AddBackgroundNoise("data/background_noises", min_snr_in_db=3, max_snr_in_db=30, p=1.0),
    Gain(min_gain_in_db=-6, max_gain_in_db=12, p=1.0),
    AddGaussianSNR(max_SNR=0.1, p=1.0),
    # TimeStretch(min_rate=0.8, max_rate=1.25, p=0.5, leave_length_unchanged=False),
    # PitchShift(min_semitones=-3, max_semitones=3, p=0.5),
    # ClippingDistortion(max_percentile_threshold=10, p=0.5), #Distort signal by clipping a random percentage of points
])

# Generate 2 seconds of dummy audio for the sake of example
# samples = np.random.uniform(low=-0.2, high=0.2, size=(32000,)).astype(np.float32)
infile = "bat_den.wav"
# [rate, samples] = aIO.read_audio_file(infile)
samples, rate = librosa.load(infile, sr=None)
# samples = samples.astype(np.float32)
# samples = np.sin(np.linspace(0, 440 * 2 * np.pi, 40000)).astype(np.float32)
# Augment/transform/perturb the audio data
outdir = "augmented"
os.makedirs(outdir, exist_ok=True)
for i in tqdm(range(10)):
    augmented_samples = augment(samples=samples, sample_rate=rate)
    # wavfile.write(f"{outdir}/sample_{i}.wav", rate, augmented_samples)
    # librosa.output.write_wav(f"{outdir}/sample_{i}.wav", augmented_samples, rate)
    sf.write(f"{outdir}/sample_{i}.wav", augmented_samples, rate, 'PCM_24')
    