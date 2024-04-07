import subprocess
import os

# Function to change audio pitch without changing speed using FFmpeg
def change_pitch(input_data, output_file, pitch_factor):
    ffmpeg_command = ["ffmpeg", "-i", "-", "-af", f"rubberband=pitch={pitch_factor}", "-f", "wav", "-"]
    with subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE) as process:
        output_data, _ = process.communicate(input=input_data)
        with open(output_file, 'wb') as f:
            f.write(output_data)

# Load audio data
with open(os.path.join("output", "output_audio.mp3"), "rb") as f:
    audio_data = f.read()

# Change pitch without changing speed
change_pitch(audio_data, os.path.join("output", "output_pitch_changed_1.wav"), 2.0)
change_pitch(audio_data, os.path.join("output", "output_pitch_changed_2.wav"), 1.5)
change_pitch(audio_data, os.path.join("output", "output_pitch_changed_3.wav"), 0.5)
change_pitch(audio_data, os.path.join("output", "output_pitch_changed_5.wav"), 1)
