import speech_recognition as sr
from gtts import gTTS
import os
import subprocess
from elevenlabs.client import ElevenLabs
from flask import redirect, url_for
import uuid
import time

## blend voice !

# Initialize the speech recognition
recognizer = sr.Recognizer()

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play


# call elevenlab Api
client = ElevenLabs(
    api_key="7fd8bbe38e87e100e7a0991940b869d8",  # Replace with your API key
)

def play_generated_audio(text, voice):
    try:
        audio_generator = client.generate(text=text, voice=voice)

        # Use subprocess.Popen() to play the generated audio
        ffplay_process = subprocess.Popen(["ffplay", "-autoexit", "-nodisp", "-"], stdin=subprocess.PIPE,
                                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Write audio stream to ffplay process's standard input
        for chunk in audio_generator:
            ffplay_process.stdin.write(chunk)

        # Close standard input, wait for audio playback to finish
        ffplay_process.stdin.close()
        ffplay_process.wait()
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



def devices_dialogue(voice):
    # save all user's voice
    os.makedirs("dialogues_devices", exist_ok=True)

    # Generate a unique conversation ID
    dialog_id = str(uuid.uuid4())

    # Create a new folder with the conversation ID
    os.makedirs(os.path.join("dialogues_devices", dialog_id), exist_ok=True)

    start_time = time.time()
    while time.time() - start_time < 150:  # Interact for one minute
        # Listen for user input
        input_text, input_audio_file = listen()

        # Save the user's input audio
        if input_audio_file:
            os.rename(input_audio_file, os.path.join("dialogues_devices", dialog_id, "input.wav"))

        # Check if user requests music
        if "turn" in input_text:
            play_generated_audio("Alright, I've turned off the lights in the bedroom,have a good night. If you need, you can also ask me to control other devices",voice)

        elif "set" in input_text:
            play_generated_audio("Got it. The living room temperature has been set to 21 degrees. Let me know if you need any further adjustments or if there's anything else I can assist you with.",voice)

        elif "lock" in input_text:
            play_generated_audio("Front door successfully locked. Your home is now secure.If you need to grant access to someone or perform any other tasks, feel free to let me know.",voice)

        elif "alarm" in input_text:
            play_generated_audio("Alarm successfully set. Get ready for a productive day ahead!",voice)

        elif "snooze" in input_text:
            play_generated_audio("Snoozing the alarm. Enjoy a few more moments of rest.",voice)

        elif "stop" in input_text in input_text:
            play_generated_audio("Alarm stopped. Have a wonderful day!",voice)

        elif "thank" in input_text:
            play_generated_audio("You're welcome. What else can I do for you?",voice)
        else:
            play_generated_audio("Sorry, I didn't understand your request.",voice)

    # Prompt the user for continuation
    play_generated_audio("Do you want to continue with controlling other devices",voice)

    # Listen for user response
    text, audio_file = listen()

    # Check if the user wants to continue
    if "yes" in text or "continue" in text:
        devices_dialogue(voice)
    else:
        play_generated_audio("Okay",voice)


def devices_task():
    # Voice 50%
    voice = client.clone(
        name="Participant_50%",
        description="Participant's cloned voice, similarity 50%, 4 semitones were changed ",
        files=["recordings/output_changed.wav"],  # Use the provided audio file path
    )
    # Welcome message
    play_generated_audio("Hello, I am your voice assistant Lumi. How can I assist you today?")

    # Proceed with music-related dialogue
    devices_dialogue(voice)

    # Goodbye message
    play_generated_audio("This round is done, please fill in the survey")



if __name__ == "__main__":
    devices_task()