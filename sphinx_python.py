import os
from pocketsphinx import AudioFile, get_model_path, get_data_path
from scipy.io import wavfile

def truncate(data, rate, start, end):
    start = int(start*rate)
    end = min(len(data), int(end*rate))
    return data[start:end]

model_path = "my_rec_model"
output_dir = "detected"
audio_file = "ok_lumi_var.wav"
fps = 100
config = {
    'verbose': False,
    'audio_file': audio_file,
    'buffer_size': 2048,
    'no_search': False,
    'full_utt': False,
    'hmm': os.path.join(model_path, 'en-us-adapt'),
    'lm': False,
    'dict': os.path.join(model_path, 'cmudict-en-us.dict'),
    'kws': os.path.join(model_path, 'hotword.dict'),
    'frate': fps
    # 'time': True
}

audio = AudioFile(**config)
os.makedirs(output_dir, exist_ok=True)
[rate, data] = wavfile.read(audio_file)
for k, phrase in enumerate(audio):
    print('-' * 28)
    print('| %5s  |  %3s   | %4s   |   %4s   |' % ('start', 'end', 'prob', 'word'))
    print('-' * 28)
    for i, s in enumerate(phrase.seg()):
        # print(s.confidence)
        start = s.start_frame / fps
        end = s.end_frame / fps
        piece = truncate(data, rate, start, end)
        file_name = f"{s.word} {k} {i}.wav"
        wavfile.write(os.path.join(output_dir, file_name), rate, piece)
        print('| %4ss | %4ss | %.4f | %8s |' % (start, end, audio.get_logmath().exp(s.prob), s.word))
        
    print('-' * 28)
