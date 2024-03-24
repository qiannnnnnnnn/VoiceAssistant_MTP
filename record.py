import os
import pyaudio
import wave
from flask import current_app as app

def record_audio(output_dir, duration=30, sample_rate=44100, channels=1, chunk=1024, format=pyaudio.paInt16):
    audio = pyaudio.PyAudio()

    # Open a new stream to record audio
    stream = audio.open(format=format,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk)

    app.logger.info("Recording...")

    frames = []

    # Record audio for the specified duration
    for _ in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    app.logger.info("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Find the next available filename
    i = 1
    while True:
        filename = os.path.join(output_dir, f"recorded_audio_{i}.wav")
        if not os.path.exists(filename):
            break
        i += 1

    # Save the recorded audio to a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    return filename
