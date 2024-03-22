import speech_recognition as sr
from gtts import gTTS
import os
from dialogue import alarm_dialogue, weather_dialogue, music_dialogue


# Initialize the speech recognition engine
recognizer = sr.Recognizer()

def tts_init(text, lang="en"):
    """Initializes the gTTS engine with the provided text and language."""
    return gTTS(text=text, lang=lang)

def speak(text):
    """Converts text to speech and plays it."""
    engine = tts_init(text)
    engine.save("output.mp3")
    os.system("mpg321 output.mp3")

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

def main():
    # Welcome message
    speak("Hello, I am your voice assistant. How can I assist you today?")

    # Carry out alarm-related dialogue
    alarm_dialogue()

    # Carry out weather-related dialogue
    weather_dialogue()

    # Carry out music-related dialogue
    music_dialogue()

    # Goodbye message
    speak("Thank you for using the voice assistant. Goodbye!")

if __name__ == "__main__":
    main()
