import speech_recognition as sr
from gtts import gTTS
import os
import subprocess
from elevenlabs.client import ElevenLabs
from flask import redirect, url_for
import uuid
import time

#改好了暂时！！ clone voice

# Initialize the speech recognition
recognizer = sr.Recognizer()

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
        audio_filename = os.path.join("dialogues_weather", str(uuid.uuid4()) + ".wav")
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


def weather_dialogue(voice):
    # save all user's voice
    os.makedirs("dialogues_weather", exist_ok=True)

    # Generate a unique conversation ID
    dialog_id = str(uuid.uuid4())

    # Create a new folder with the conversation ID
    os.makedirs(os.path.join("dialogues_weather", dialog_id), exist_ok=True)

    start_time = time.time()
    while time.time() - start_time < 150:  # Interact for one minute
        # Listen for user input
        input_text, input_audio_file = listen()

        # Save the user's input audio
        if input_audio_file:
            os.rename(input_audio_file, os.path.join("dialogues_weather", dialog_id, "input.wav"))

            # Check if user requests music
            if "check" in input_text and "weather" in input_text:
                play_generated_audio("Currently checking the weather for Eindhoven. "
                                     "It seems to be a beautiful day with plenty of sunshine. "
                                     "It's perfect weather for wearing light and comfortable clothing. "
                                     "You might want to consider outdoor activities such as picnics, walks in the park, or cycling. "
                                     "Enjoy the lovely weather!", voice)
            elif "temperature" in input_text:
                play_generated_audio("The temperature is around 20 degrees Celsius, and there's hardly any wind. ",
                                     voice)
            elif "wind speed" in input_text:
                play_generated_audio("Checking the wind speed.There's hardly any wind.", voice)
            elif "rain" in input_text or "rainfall" in input_text:
                play_generated_audio("Checking rainfall.There is no rainfall today.", voice)
            elif "thank" in input_text:
                play_generated_audio("You're welcome. What else can I do for you?", voice)
            else:
                play_generated_audio("Sorry, I didn't understand your request.", voice)

    # Prompt the user for continuation
    play_generated_audio("Do you want to continue with another news action?",voice)

    # Listen for user response
    text, audio_file = listen()

    # Check if the user wants to continue
    if "yes" in text or "continue" in text:
        weather_dialogue(voice)
    else:
        play_generated_audio("Okay,have a nice day",voice)


def weather_task():
    # Initialize voice clone
    voice = client.clone(
        name="Participant",
        description="Participant's cloned voice ",
        files=["recordings/recorded_audio.wav"],  # the recordfile, need to change the record loop
    )

    # Welcome message
    play_generated_audio("Hello, I am your voice assistant Lumi. How can I assist you today?", voice)

    # Proceed with weather-related dialogue
    weather_dialogue(voice)

    # Goodbye message
    play_generated_audio("This round is done, please fill in the survey", voice)


if __name__ == "__main__":
    weather_task()
