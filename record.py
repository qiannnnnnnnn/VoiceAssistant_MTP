import pyaudio
import wave
import subprocess

def record_audio(filename, duration=30, sample_rate=44100, channels=1, chunk=1024, format=pyaudio.paInt16):
    """
    Record audio from the microphone and save it to a WAV file.

    Parameters:
    - filename: The filename to save the recorded audio to.
    - duration: The duration of the recording in seconds (default is 5 seconds).
    - sample_rate: The sample rate of the recording (default is 44100 Hz).
    - channels: The number of audio channels (default is 2 for stereo).
    - chunk: The number of frames per buffer (default is 1024).
    - format: The audio data format (default is 16-bit PCM).

    Returns:
    - None
    """
    audio = pyaudio.PyAudio()

    # Open a new stream to record audio
    stream = audio.open(format=format,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk)

    print("Recording...")

    frames = []

    # Record audio for the specified duration
    for _ in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

def convert_to_mp3(input_filename, output_filename):
    """
    Convert WAV audio file to MP3 format using FFmpeg.

    Parameters:
    - input_filename: The filename of the input WAV file.
    - output_filename: The filename to save the converted MP3 file to.

    Returns:
    - None
    """
    subprocess.run(['ffmpeg', '-i', input_filename, '-codec:a', 'libmp3lame', output_filename])

if __name__ == "__main__":
    # Define the filenames
    wav_filename = "recorded_audio.wav"
    mp3_filename = "recorded_audio.mp3"

    # Record audio for 5 seconds (you can adjust the duration if needed)
    record_audio(wav_filename, duration=5)

    # Convert the WAV file to MP3 format
    convert_to_mp3(wav_filename, mp3_filename)

    print(f"Audio recorded and saved as {mp3_filename}")
