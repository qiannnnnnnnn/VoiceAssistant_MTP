import subprocess
from elevenlabs.client import ElevenLabs
import os
from elevenlabs import play

# 要不要把这个和record结合在一起

client = ElevenLabs(
    api_key="e0c5f7b856cf59ef10a4253335714486", # default ELEVEN_API_KEY
)

voice = client.clone(
    name="Qian",
    description="testing,female voice",
    files=["recordings/recorded_audio_2.wav"],
)

audio_generator = client.generate(text="Hi! I'm a cloned voice!", voice=voice)

# Check and create output folder if necessary
if not os.path.exists("output"):
    os.mkdir("output")

# Save the generated audio to the output folder
with open(os.path.join("output", "output_audio.mp3"), "wb") as f:
    for chunk in audio_generator:
        f.write(chunk)

# Modify pitch using ffmpeg
subprocess.call(["ffmpeg", "-i", os.path.join("output", "output_audio.mp3"), "-af", "asetrate=44100*1.1,atempo=0.9", os.path.join("output", "output_pitch_changed_1.wav")])
subprocess.call(["ffplay", os.path.join("output", "output_pitch_changed_1.wav")])

subprocess.call(["ffmpeg", "-i", os.path.join("output", "output_audio.mp3"), "-af", "asetrate=44100*1.1,atempo=1.5", os.path.join("output", "output_pitch_changed_2.wav")])
subprocess.call(["ffplay", os.path.join("output", "output_pitch_changed_2.wav")])


subprocess.call(["ffmpeg", "-i", os.path.join("output", "output_audio.mp3"), "-af", "asetrate=44100*1.1,atempo=0.5", os.path.join("output", "output_pitch_changed_3.wav")])
subprocess.call(["ffplay", os.path.join("output", "output_pitch_changed_3.wav")])