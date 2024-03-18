import subprocess
from elevenlabs.client import ElevenLabs
from elevenlabs import play

client = ElevenLabs(
    api_key="e0c5f7b856cf59ef10a4253335714486", # default ELEVEN_API_KEY
)

voice = client.clone(
    name="Qian",
    description="An old American male voice with a slight hoarseness in his throat. Perfect for news", # 可选
    files=["./recorded_audio.mp3"],
)

audio_generator = client.generate(text="Hi! I'm a cloned voice!", voice=voice)

with open("output_audio.mp3", "wb") as f:
    for chunk in audio_generator:
        f.write(chunk)

# using ffmpeg adjust the pich，asetrate=44100*1.1 表示将音频的采样率增加 10%，atempo=0.9 表示将音频的速度降低 10%，从而改变音频的音高
subprocess.call(["ffmpeg", "-i", "output_audio.mp3", "-af", "asetrate=44100*1.1,atempo=0.9", "output_pitch_changed.mp3"])
play("output_pitch_changed.mp3")
