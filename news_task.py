import speech_recognition as sr
from gtts import gTTS
import os
import subprocess
from elevenlabs.client import ElevenLabs
from flask import redirect, url_for
import uuid

# Initialize the speech recognition
recognizer = sr.Recognizer()

# call elevenlab Api
client = ElevenLabs(
    api_key="e0c5f7b856cf59ef10a4253335714486",  # Replace with your API key
)

'''
生成次数用完了暂时先这样，不克隆新的
# Clone the voice once
voice = client.clone(
    name="Qian",
    description="dialogue_voice test",
    files=["output/output_pitch_changed_1.mp3"],  # Use the provided audio file path
)
'''

voice_name = "Qian_pitch1"


def play_generated_audio(text, voice_name="Qian"):
    try:
        audio_generator = client.generate(text=text, voice=voice_name)

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


import os
import uuid
import time

def news_dialogue():
    # save all user's voice
    os.makedirs("dialogues", exist_ok=True)

    # Generate a unique conversation ID
    dialog_id = str(uuid.uuid4())

    # Create a new folder with the conversation ID
    os.makedirs(os.path.join("dialogues", dialog_id), exist_ok=True)

    start_time = time.time()
    while time.time() - start_time < 1:  # Interact for one minute
        # Listen for user input
        input_text, input_audio_file = listen()

        # Save the user's input audio
        if input_audio_file:
            os.rename(input_audio_file, os.path.join("dialogues", dialog_id, "input.wav"))

        # Check if user says news/podcast
        if "news" in input_text:
            play_generated_audio("In today's headlines, tensions escalated in the Middle East "
                                 "as diplomatic talks broke down between neighboring nations. "
                                 "Meanwhile, scientists announced a groundbreaking discovery in renewable energy technology,"
                                 " offering hope for a greener future. In other news, "
                                 "the stock market saw significant fluctuations, prompting investors to reassess their portfolios. "
                                 "Stay tuned for further updates on these developing stories and more.")
        elif "pause" in input_text:
            play_generated_audio(
                "Pausing the current news update. Stay tuned as we'll resume shortly after this brief pause.")
        elif "next" in input_text:
            play_generated_audio("Moving on to the next news segment. Stay informed with our continuous coverage.")
        elif "thank" in input_text:
            play_generated_audio("You're welcome. What else can I do for you?")
        else:
            play_generated_audio("Sorry,I didn't catch that. Could you please ask a question about the news?")

    # Prompt the user for continuation
    play_generated_audio("Do you want to continue with another news action?")

    # Listen for user response
    text, audio_file = listen()

    # Check if the user wants to continue
    if "yes" in text or "continue" in text:
        news_dialogue()
    else:
        play_generated_audio("Okay,have a nice day")


def news_task():

    # Welcome message
    play_generated_audio("Hello, I am your voice assistant Lumi. How can I assist you today?")

    # Proceed with music-related dialogue
    news_dialogue()

    # Goodbye message
    play_generated_audio("This round is done, please fill in the survey")



if __name__ == "__main__":
    news_task()