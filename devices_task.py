import speech_recognition as sr
from gtts import gTTS
import os
import subprocess
from elevenlabs.client import ElevenLabs
from flask import redirect, url_for
import uuid

# Initialize the speech recognition
recognizer = sr.Recognizer()

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

def play_generated_audio(text, voice_name="en-US"):
    try:
        tts = gTTS(text=text, lang=voice_name)
        tts.save("generated_audio.mp3")  # 保存生成的音频文件

        # 使用pydub加载并播放音频文件
        audio = AudioSegment.from_mp3("generated_audio.mp3")
        play(audio)
    except Exception as e:
        print("Error while playing audio:", e)



def tts_init(text, lang="en"):
    return gTTS(text=text, lang=lang)


def speak(text):
    engine = tts_init(text)
    engine.save("output.mp3")
    os.system("mpg321 output.mp3")


def listen():
    """Records audio from the microphone, saves it to a file, and performs speech recognition."""
    with sr.Microphone() as source:
        print("Speak now:")
        recognizer.adjust_for_ambient_noise(source)  # Adapt to ambient noise
        audio = recognizer.listen(source)  # Capture audio data

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language="en-US")
        print("You said:", text)

        # Save the recorded audio to a file
        audio_filename = os.path.join("dialogues", str(uuid.uuid4()) + ".wav")
        with open(audio_filename, "wb") as f:
            f.write(audio.get_wav_data())

        return text.lower(), audio_filename
    except sr.UnknownValueError:
        print("Sorry, I didn't understand what you said.")
        return "", ""
    except sr.RequestError as e:
        print("Could not get results from Google Speech Recognition service; {0}".format(e))
        return "", ""
    except Exception as e:
        print("Error while processing audio:", e)
        return "", ""


import os
import uuid
import time

def devices_dialogue():
    # save all user's voice
    os.makedirs("dialogues_task3", exist_ok=True)

    # Generate a unique conversation ID
    dialog_id = str(uuid.uuid4())

    # Create a new folder with the conversation ID
    os.makedirs(os.path.join("dialogues_task3", dialog_id), exist_ok=True)

    start_time = time.time()
    while time.time() - start_time < 3:  # Interact for one minute
        # Listen for user input
        input_text, input_audio_file = listen()

        # Save the user's input audio
        if input_audio_file:
            os.rename(input_audio_file, os.path.join("dialogues_task3", dialog_id, "input.wav"))

        # Check if user requests music
        if "turn" in input_text:
            play_generated_audio("Alright, I've turned off the lights in the bedroom. "
                                 "Would you like me to control other devices")
        elif "set" in input_text:
            play_generated_audio("Got it. The living room temperature has been set to 21 degrees. "
                                 "Let me know if you need any further adjustments or if there's anything else I can assist you with.")
        elif "lock" in input_text:
            play_generated_audio("Front door successfully locked. Your home is now secure. "
                                 "If you need to grant access to someone or perform any other tasks, feel free to let me know.")

        elif "thank" in input_text:
            play_generated_audio("You're welcome. What else can I do for you?")
        else:
            play_generated_audio("Sorry, I didn't understand your request.")

    # Prompt the user for continuation
    play_generated_audio("Do you want to continue with controlling other devices")

    # Listen for user response
    text, audio_file = listen()

    # Check if the user wants to continue
    if "yes" in text or "continue" in text:
        devices_dialogue()
    else:
        play_generated_audio("Okay")


def devices_task():
    # Welcome message
    play_generated_audio("Hello, I am your voice assistant Lumi. How can I assist you today?")

    # Proceed with music-related dialogue
    devices_dialogue()

    # Goodbye message
    play_generated_audio("This round is done, please fill in the survey")



if __name__ == "__main__":
    devices_task()