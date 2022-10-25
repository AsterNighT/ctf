#!/usr/bin/env python3
import librosa  # version: 0.8.1
import numpy as np  # version: 1.19.5
from PIL import Image, ImageSequence
import soundfile as sf

num_freqs = 32
quantize = 2
min_db = -60
max_db = 30
fft_window_size = 2048
frame_step_size = 512
window_function_type = 'hann'
red_pixel = [255, 0, 0]
white_pixel = [255, 255, 255]
sample_rate = 22050
# y, sample_rate = librosa.load("flag.mp3")  # sample rate is 22050 Hz

# spectrogram = (numpy.around(librosa.power_to_db(librosa.feature.melspectrogram(y, sample_rate, n_mels=num_freqs,
#                n_fft=fft_window_size, hop_length=frame_step_size, window=window_function_type)) / quantize) * quantize)

# gif_data = [numpy.kron(numpy.array([[red_pixel if freq % 2 and round(frame[freq // 2]) > threshold else white_pixel for threshold in list(range(
#     min_db, max_db + 1, quantize))[::-1]] for freq in range(num_freqs * 2 + 1)]), numpy.ones([quantize, quantize, 1])) for frame in spectrogram.transpose()]

# write_gif(gif_data, 'flag.gif', fps=sample_rate/frame_step_size)

gif = Image.open("./flag.gif")
data = np.array([np.array(frame.copy().convert('RGB').getdata(), dtype=np.uint8).reshape(
    frame.size[1], frame.size[0], 3) for frame in ImageSequence.Iterator(gif)])

before_kron = np.array([
    [
        [
            'r' if frame[outer][inner][1] == 0 else 'w' for inner in range(0, len(frame[outer]), 2)
        ] for outer in range(0, len(frame), 2)
    ] for frame in data
])

spectrogram = []

print(before_kron.shape)

for frame in before_kron:
    spectrogram_frame = []
    for freq in range(num_freqs * 2 + 1):
        if freq % 2 == 0:
            continue  # rubbish
        value = -30
        for i in range(len(frame)):
            if frame[i][freq] == 'r':
                value += (45-i)*2
                break
        spectrogram_frame.append(value)

    spectrogram.append(spectrogram_frame)


spectrogram = np.array(spectrogram)
print(spectrogram.shape)

spectrogram = spectrogram.transpose()
spectrogram = librosa.db_to_power(spectrogram)

audio = librosa.feature.inverse.mel_to_audio(spectrogram, sample_rate, 
                                             n_fft=fft_window_size, hop_length=frame_step_size, window=window_function_type)

sf.write("recover.wav", audio, sample_rate, sf.default_subtype('WAV'))
