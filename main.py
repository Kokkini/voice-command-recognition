# from pocketsphinx import Decoder
# import pyaudio
# from datetime import datetime
# import os

# pocketsphinx_dir = "/Users/quang/Documents/startup/lumi/ok_lumi/pocketsphinx-python/pocketsphinx"
# p = pyaudio.PyAudio()
# stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=20480)
# stream.start_stream()

# model_dir = os.path.join(pocketsphinx_dir, 'model')

# ps_config = Decoder.default_config()
# ps_config.set_string('-hmm', os.path.join(model_dir, 'en-us'))
# ps_config.set_string('-dict', "/Users/quang/Documents/startup/lumi/ok_lumi/hotwords.dict")
# ps_config.set_string('-keyphrase', 'shop assist')
# ps_config.set_float('-kws_threshold', 1e-30)

# decoder = Decoder(ps_config)
# decoder.start_utt()

# while True:
#     buf = stream.read(1024)
#     if buf:
#         decoder.process_raw(buf, False, False)
#     else:
#         break
#     if decoder.hyp() is not None:
#         print([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in decoder.seg()])
#         print("Detected %s at %s" % (decoder.hyp().hypstr, str(datetime.now().time())))
#         decoder.end_utt()
#         print("detected")
#         # PERFORM COOL TASK

from __future__ import print_function
import os
from pocketsphinx import Pocketsphinx, get_model_path, get_data_path

model_path = "my_rec_model"
audio_file = "ok_lumi.wav"
# data_path = get_data_path()

print(model_path)
# print(data_path)

config = {
    'verbose': False,
    'hmm': os.path.join(model_path, 'en-us-adapt'),
    # 'lm': os.path.join(model_path, 'en-us.lm.bin'),
    'lm': False,
    'dict': os.path.join(model_path, 'cmudict-en-us.dict'),
    'kws': os.path.join(model_path, 'hotword.dict'),
    'frate': 100
}

ps = Pocketsphinx(**config)
# audio_file = os.path.join(data_path, 'goforward.raw')

ps.decode(
    audio_file=audio_file,
    buffer_size=2048,
    no_search=False,
    full_utt=False
)

print(ps.segments()) # => ['<s>', '<sil>', 'go', 'forward', 'ten', 'meters', '</s>']
print('Detailed segments:', *ps.segments(detailed=True), sep='\n') # => [
#     word, prob, start_frame, end_frame
#     ('<s>', 0, 0, 24)
#     ('<sil>', -3778, 25, 45)
#     ('go', -27, 46, 63)
#     ('forward', -38, 64, 116)
#     ('ten', -14105, 117, 152)
#     ('meters', -2152, 153, 211)
#     ('</s>', 0, 212, 260)
# ]

fps = 1
print('-' * 28)
print('| %5s  |  %3s   | %4s   |   %4s   |' % ('start', 'end', 'prob', 'word'))
print('-' * 28)
for i, s in enumerate(ps.segments(detailed=True)):
    # print(s.confidence)
    word, prob, start_frame, end_frame = s
    start = start_frame / fps
    end = end_frame / fps
    # piece = truncate(data, rate, start, end)
    # file_name = f"{s.word} {k} {i}.wav"
    # wavfile.write(os.path.join(output_dir, file_name), rate, piece)
    print('| %4ss | %4ss | %.4f | %8s |' % (start, end, ps.get_logmath().exp(prob), word))
    
print('-' * 28)


print(ps.hypothesis())  # => go forward ten meters
print(ps.probability()) # => -32079
print(ps.score())       # => -7066
print(ps.confidence())  # => 0.04042641466841839

print(*ps.best(count=10), sep='\n') # => [
#     ('go forward ten meters', -28034)
#     ('go for word ten meters', -28570)
#     ('go forward and majors', -28670)
#     ('go forward and meters', -28681)
#     ('go forward and readers', -28685)
#     ('go forward ten readers', -28688)
#     ('go forward ten leaders', -28695)
#     ('go forward can meters', -28695)
#     ('go forward and leaders', -28706)
#     ('go for work ten meters', -28722)
# ]