import time
import speech_recognition as sr
from elevenlabs.client import ElevenLabs
from elevenlabs import play

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

def listen():
    """Listens for user input using the microphone and returns recognized text."""
    with sr.Microphone() as source:
        print("Speak now:")
        recognizer.adjust_for_ambient_noise(source)  # Adapt to ambient noise
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language="en-US")
        print("You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't understand what you said.")
        return ""
    except sr.RequestError as e:
        print("Could not get results from Google Speech Recognition service; {0}".format(e))
        return ""

def generate_and_play_audio(text, voice):
    """Generates audio using ElevenLabs for the given text and plays it."""
    client = ElevenLabs(api_key="e0c5f7b856cf59ef10a4253335714486")

    # audio using elevenLabs
    audio = client.generate(text=text, voice=voice)

    play(audio)

def main():
    client = ElevenLabs(api_key="e0c5f7b856cf59ef10a4253335714486")
    voice = client.clone(
        name="Qian",
        description="An old American male voice with a slight hoarseness in his throat. Perfect for news",
        files=["./recorded_audio.mp3"],
    )

    # Welcome message
    generate_and_play_audio("Hello, I am your voice assistant,LUMI. How can I assist you today?", voice)

    time.sleep(3)

    generate_and_play_audio("Sure, I will set an alarm for 8 AM.", voice)

    time.sleep(3)

    generate_and_play_audio("The alarm is currently set for 8 AM.", voice)

if __name__ == "__main__":
    main()
