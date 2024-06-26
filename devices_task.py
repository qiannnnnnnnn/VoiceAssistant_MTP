import speech_recognition as sr
from gtts import gTTS
import os
from elevenlabs.client import ElevenLabs
import uuid
import time
import random
import pygame
from io import BytesIO

# Initialize the speech recognition
recognizer = sr.Recognizer()

# call elevenlab Api
client = ElevenLabs(
    api_key="59cb581fecab89d49359c7c0c1fa5cf5",
)

# pygame
def play_generated_audio(text, voice):
    try:
        audio_generator = client.generate(text=text, voice=voice)

        audio_bytes = b"".join(audio_generator)
        # load audio
        pygame.mixer.init()
        pygame.mixer.music.load(BytesIO(audio_bytes))

        # play
        pygame.mixer.music.play()

        # wait for the audio to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print("Eror while playing audio:", e)


def tts_init(text, lang="en"):
    return gTTS(text=text, lang=lang)


def speak(text):
    engine = tts_init(text)
    engine.save("output.mp3")
    os.system("mpg321 output.mp3")


def listen():
    """Records audio from the microphone, saves it to a file, and performs speech recognition."""

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak now:")
        recognizer.adjust_for_ambient_noise(source)  # Adapt to ambient noise
        audio = recognizer.listen(source)  # Capture audio data

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language="en-US")
        print("You said:", text)

        # Save the recorded audio to a file
        dialogues_dir = "dialogues_devices"
        if not os.path.exists(dialogues_dir):
            os.makedirs(dialogues_dir)

        # Generate a unique filename
        while True:
            timestamp = int(time.time() * 1000)
            random_component = random.randint(0, 9999)
            audio_filename = os.path.join(dialogues_dir, f"{timestamp}_{random_component}.wav")
            if not os.path.exists(audio_filename):
                break

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
    dialog_folder_path = os.path.join("dialogues_devices", dialog_id)
    os.makedirs(dialog_folder_path, exist_ok=True)

    start_time = time.time()
    while time.time() - start_time < 100:  # Interact time, in seconds
        # Listen for user input
        input_text, input_audio_file = listen()

        # Save the user's input audio
        if input_audio_file:
            timestamp = int(time.time() * 1000)
            unique_input_filename = os.path.join(dialog_folder_path, f"input_{timestamp}.wav")
            os.rename(input_audio_file, unique_input_filename)

        # Check if user says news/podcast
        if "turn" in input_text:
            play_generated_audio("Alright, The bedroom lights are off now, "
                                 "setting a cozy vibe for your night's rest."
                                 " If you need more help with other devices around your home, "
                                 "just let me know. Wishing you a tranquil and refreshing night ahead!", voice)
        elif "temperature" in input_text:
            play_generated_audio("Understood, the living room temperature has been adjusted to ensure your comfort. "
                                 "If there's anything else you want to adjust or if there are other tasks you have in mind,"
                                 " just let me know. I'm here to assist you with anything you need, anytime.",
                                 voice)
        elif "alarm" in input_text:
            play_generated_audio(
                "Your alarm is all set and ready to kickstart your day with productivity!"
                " If you need assistance or reminders as you go about your day, don't hesitate to reach out. "
                "I'm here to support you at every turn, ensuring a smooth and successful day ahead!", voice)
        elif "lock" in input_text:
            play_generated_audio("The front door is securely locked, ensuring your home's safety and peace of mind. "
                                 "If you need to grant access to someone or have any other tasks in mind, don't hesitate to reach out."
                                 " I'm available round the clock to assist you with anything you need, whenever you need it.",
                                 voice)
        elif "thank" in input_text:
            play_generated_audio("You're welcome. What else can I do for you?", voice)
        elif "stop" in input_text:
            play_generated_audio("Okay, stopping now.", voice)
            return  # 终止函数执行
        else:
            play_generated_audio("Sorry,I didn't catch that. Could you please ask a question about the devices at your home?", voice)

    # Prompt the user for continuation
    play_generated_audio("Is there anything else I can do for you?", voice)

    # Listen for user response
    text, audio_file = listen()

    # Check if the user wants to continue
    if "yes" in text or "continue" in text:
        devices_dialogue(voice)
    else:
        play_generated_audio("Okay,have a nice day", voice)


def devices_task():
    # Voice 50%
    voice = client.clone(
        name="Participant_50%",
        description="Participant's cloned voice, similarity 50%, 2 semitones were changed ",
        files=["recordings/pitch_changed.wav"],  # Use the provided audio file path
    )
    # Welcome message
    play_generated_audio("Hello, I am your voice assistant Lumi. How can I assist you today?",voice)

    # Proceed with music-related dialogue
    devices_dialogue(voice)

    # Goodbye message
    play_generated_audio("This round is done, please click the go to survey  button to fill in the survey",voice)


if __name__ == "__main__":
    devices_task()


'''
  # Cloned voice
    voice = client.clone(
        name="Participant",
        description="Participant's cloned voice ",
        files=["recordings/recorded_audio.wav"],  # the recordfile, need to change the record loop
    )
    # Neutral Voice
    # voice = "BzGBcwax6fZdL0A0cNrE"
    voice = "bTs5u126Wd7y2pljrAbG"

    # Voice 50%
    voice = client.clone(
        name="Participant_50%",
        description="Participant's cloned voice, similarity 50%, 4 semitones were changed ",
        files=["recordings/pitch_changed.wav"],  # Use the provided audio file path
    )
'''