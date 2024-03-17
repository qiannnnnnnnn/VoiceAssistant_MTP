from elevenlabs.client import ElevenLabs
from elevenlabs import play

client = ElevenLabs(
  api_key="e0c5f7b856cf59ef10a4253335714486", # Defaults to ELEVEN_API_KEY
)

voice = client.clone(
    name="Qian",
    description="An old American male voice with a slight hoarseness in his throat. Perfect for news", # Optional
    files=["./recorded_audio.mp3"],
)

audio = client.generate(text="Hi! I'm a cloned voice!", voice=voice)

play(audio)
