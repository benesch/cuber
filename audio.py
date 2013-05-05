import pyaudio

__all__ = ['open', 'close', 'CHUNK']

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
ADJUST = 1

audio = None

def open():
    global audio

    if audio is not None:
        audio.terminate()
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    return stream

def close(stream):
    stream.stop_stream()
    stream.close()
    audio.terminate()
    audio = None