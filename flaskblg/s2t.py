# from deepspeech import Model
import numpy as np
import os
import wave

# from IPython.display import Audio
# from IPython.display import clear_output

model_file_path = 'deepspeech-0.8.2-models.pbmm'
lm_file_path = 'deepspeech-0.8.2-models.scorer'

beam_width = 100
lm_alpha = 0.93
lm_beta = 1.18

model = Model(model_file_path)
model.enableExternalScorer(lm_file_path)

model.setScorerAlphaBeta(lm_alpha, lm_beta)
model.setBeamWidth(beam_width)
stream = model.createStream()


def read_audio_file(filename):
    with wave.open(filename, 'rb') as w:
        rate = w.getframerate()
        frames = w.getnframes()
        buffer = w.readframes(frames)

    return buffer, rate


def real_time_transcription(audio_file):
    buffer, rate = read_audio_file(audio_file)
    offset = 0
    batch_size = 8196
    text = ''

    while offset < len(buffer):
        end_offset = offset + batch_size
        chunk = buffer[offset:end_offset]
        data16 = np.frombuffer(chunk, dtype=np.int16)

        stream.feedAudioContent(data16)
        text1 = stream.intermediateDecode()

        text = text1
        offset = end_offset
    return text
