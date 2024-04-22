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

# call elevenlabs Api
client = ElevenLabs(
    api_key="7fd8bbe38e87e100e7a0991940b869d8",  # Replace with your API key
)



"""
def play_generated_audio(text, voice):
    try:
        audio_generator = client.generate(text=text, voice=voice)

        # Use subprocess.Popen() to play the generated audio
        #ffplay_process = subprocess.Popen(["ffplay", "vn", "-"], stdin=subprocess.PIPE,
                                         # stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ffplay_command = ["ffplay","-autoexit","-nodisp","-i","pipe:0"]
        ffplay_process = subprocess.Popen(ffplay_command,stdin=subprocess.PIPE,
                                          stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
                                          shell=True)
        
        # Write audio stream to ffplay process's standard input
        for chunk in audio_generator:
            ffplay_process.stdin.write(chunk)

        # Close standard input, wait for audio playback to finish
        ffplay_process.stdin.close()
        ffplay_process.wait()
    except Exception as e:
        print("Error while playing audio:", e)
"""

#pygame 
def play_generated_audio(text, voice, volume=1.0):
    try:
        audio_generator = client.generate(text=text, voice=voice)

        audio_bytes = b"".join(audio_generator)

        # Initialize Pygame
        pygame.mixer.init()

        # Load audio
        audio_stream = BytesIO(audio_bytes)
        pygame.mixer.music.load(audio_stream)

        # Set volume
        pygame.mixer.music.set_volume(volume)

        # Play audio
        pygame.mixer.music.play()

        # Wait for the audio to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

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
        dialogues_dir = "dialogues_news"
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


def news_dialogue(voice):                                                                                                                                                                                                           
    # save all user's voice
    os.makedirs("dialogues_news", exist_ok=True)

    # Generate a unique conversation ID
    dialog_id = str(uuid.uuid4())

    # Create a new folder with the conversation ID
    dialog_folder_path = os.path.join("dialogues_news", dialog_id)
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
        if "football" in input_text:
            play_generated_audio("Updating the news.The race for the Premier League football title is heating up!"
                                 " Manchester City gained an advantage after both Arsenal and Liverpool lost their matches in April."
                                 "However, with several games remaining in the season, the title race is far from over. "
                                 "Arsenal and Liverpool are still very much in contention.",voice,volume=0.3)
        elif "tennis" in input_text:
            play_generated_audio("Moving on to the next news segment. Emma Raducanu is set to face Angelique Kerber in the first round of the Stuttgart Open after her heroics in the Billy Jean King Cup. "
                                 "Kerber, at age 35, will leverage her experience on clay courts, winning the Stuttgart Open twice. "
                                 "Raducanu, aged at just 19,  hungry to prove herself on different surfaces after her US Open triumph on hard court",voice,volume=0.3)
        elif "marathon" in input_text:
            play_generated_audio(
                " United co-owner Sir Jim Ratcliffe competed in two separate races on Sunday."
                "The 71-year-old lined up for his eighth London Marathon in the morning and then faced a race against time to watch his side face Coventry in the FA Cup semi-final at Wembley in the afternoon."
                "The British billionaire is an avid runner and has completed more than 30 marathons worldwide, "
                "while his chemical group Ineos supported Kenya's Eliud Kipchoge in his successful bid to become the first person to break the two-hour mark for a marathon in October 2019.", voice, volume=0.3)
        elif "golf" in input_text:
            play_generated_audio("Nelly Korda equalled an LPGA record by winning her fifth tournament in a row as she claimed "
                                 "the first women's major of the year at the Chevron Championship.Her three-under 69 on a gusty day "
                                 "in Texas saw her finish on 13 under to win her second major by two shots.",voice,volume=0.3)

        elif "thank" in input_text:
            play_generated_audio("You're welcome. What else can I do for you?",voice,volume=0.3)
        elif "stop" in input_text:
            play_generated_audio("Okay, stopping now.", voice, volume=0.3)
            return  # 终止函数执行
        else:
            play_generated_audio("Sorry,I didn't catch that. Could you please ask a question about the sports news?",voice,volume=0.3)

    # Prompt the user for continuation
    play_generated_audio("Is there anything else I can do for you?",voice,volume=0.3)

    # Listen for user response
    text, audio_file = listen()

    # Check if the user wants to continue
    if "yes" in text or "continue" in text:
        news_dialogue(voice)
    else:
        play_generated_audio("Okay,have a nice day",voice,volume=0.3)

def news_task():
    # Neural Voice
    #voice = "BzGBcwax6fZdL0A0cNrE"
    voice = "bTs5u126Wd7y2pljrAbG"

    # Welcome message
    play_generated_audio("Hello, I am your voice assistant Lumi. How can I assist you today?",voice, volume=0.3)

    # Proceed with music-related dialogue
    news_dialogue(voice)

    # Goodbye message
    play_generated_audio("This round is done, please click the go to survey button to fill in the survey",voice,volume=0.3)



if __name__ == "__main__":
    news_task()


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

