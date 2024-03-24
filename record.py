import os
import pyaudio
import wave


def record_audio(output_dir, duration=30, sample_rate=44100, channels=1, chunk=1024, format=pyaudio.paInt16):
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


if __name__ == "__main__":
    # Define the output directory
    output_dir = "recordings"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Record audio for 30 seconds (you can adjust the duration if needed)
    wav_filename = record_audio(output_dir, duration=30)

    print(f"Audio recorded and saved as {wav_filename}")
