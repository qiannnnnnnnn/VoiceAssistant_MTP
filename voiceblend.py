import pydub
from pydub.playback import play
#from speech_synthesis import SpeechSynthesis
from gtts import gTTS

# 混合声音
voice1 = pydub.AudioSegment.from_file("recordings/recorded_audio_1.wav")
voice2 = pydub.AudioSegment.from_file("recordings/neutral_audio.mp3")
mixed_voice = voice1.overlay(voice2)

# 将混合声音保存为 new_voice.wav
mixed_voice.export("new_voice.wav")

play(mixed_voice)