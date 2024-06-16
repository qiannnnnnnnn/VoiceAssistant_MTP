import os
import pyaudio
import wave


def record_audio(output_dir, filename, duration=30, sample_rate=44100, channels=1, chunk=1024, format=pyaudio.paInt16):
    audio = pyaudio.PyAudio()

    # Open a new stream to record audio
    stream = audio.open(format=format,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk)

    frames = []

    # Record audio for the specified duration
    for _ in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a WAV file
    file_path = os.path.join(output_dir, filename)
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    return file_path

from pydub import AudioSegment

def change_pitch(input_file, output_file, pitch_factor):
    try:
        audio = AudioSegment.from_file(input_file)
        semitone_shift = pitch_factor * 100

        pitched_audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * (2 ** (semitone_shift / 1200.0)))
        })
        pitched_audio.export(output_file, format="wav")

        return output_file
    except Exception as e:
        print("Error occurred while changing pitch:", e)
        return None



