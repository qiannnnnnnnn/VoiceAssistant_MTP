import speech_recognition as sr
from gtts import gTTS
import os

# Define music-related responses
music_responses = {
    "Play some music": "Sure, what kind of music would you like to play?",
    "Pause the music": "Sure, I will pause the music.",
    "Resume the music": "Sure, I will resume the music."
}


# Define weather-related responses
weather_responses = {
    "What's the weather like today?": "It's sunny in Beijing today, with a high of 25 degrees Celsius and a low of 10 degrees Celsius.",
    "Will it rain tomorrow?": "There is a chance of light rain in Beijing tomorrow. Please bring an umbrella.",
    "What's the weather like recently?": "The weather in Beijing has been dry recently. Please remember to drink plenty of water."
}

# Define alarm-related responses
alarm_responses = {
    "Set an alarm for 8 AM": "Sure, I will set an alarm for 8 AM.",
    "What time is the alarm set for?": "The alarm is currently set for 8 AM."
}

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
        print("You said:", text)  # 添加这一行用于输出识别到的文本
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't understand what you said.")
        return ""
    except sr.RequestError as e:
        print("Could not get results from Google Speech Recognition service; {0}".format(e))
        return ""


def music_dialogue():
    rounds = 0
    while rounds < 3:  # Only carry out 3 rounds of dialogue
        # Listen for user input
        text = listen()

        # Check if the user requested to play music
        if "music" in text:
            # Respond accordingly
            speak("Playing some pop music.")

            # Ask if user wants to pause or play next song
            speak("Would you like to pause the music or play the next song?")

            # Listen for user input
            text = listen()

            # Check user's response
            if "pause" in text:
                speak("Pausing the music.")
            elif "next song" in text:
                speak("Playing the next song.")
            else:
                speak("Sorry, I didn't understand your request.")

            rounds += 1
        else:
            # If the request is not related to playing music, provide a friendly message
            speak("Sorry, I currently only understand 'play some pop music' requests. Can you please repeat?")

    # Ask user if they want to continue the interaction
    speak("Do you want to continue with another music-related action?")

    # Listen for user input
    text = listen()

    # Check if the user wants to continue
    if "yes" in text:
        music_dialogue()  # Restart the function to continue the interaction
    else:
        speak("Okay, goodbye!")

def weather_dialogue():
    rounds = 0
    while rounds < 3:  # Only carry out 3 rounds of dialogue
        # Listen for user input
        text = listen()

        # Check if the user requested weather information
        if "weather" in text:
            # Respond accordingly
            speak("The weather in Beijing has been dry recently. Please remember to drink plenty of water.")
            rounds += 1
        else:
            # If the request is not related to weather, provide a friendly message
            speak("Sorry, I currently only understand 'weather' requests. Can you please repeat?")

    # Ask user if they want to continue the interaction
    speak("Do you want to continue with another weather-related action?")

    # Listen for user input
    text = listen()

    # Check if the user wants to continue
    if "yes" in text:
        weather_dialogue()  # Restart the function to continue the interaction
    else:
        speak("Okay, goodbye!")

def alarm_dialogue():
    rounds = 0
    while rounds < 3:  # Only carry out 3 rounds of dialogue
        # Listen for user input
        text = listen()

        # Check if the user requested to set an alarm
        if "alarm" in text:
            # Respond accordingly
            speak("Sure, I will set an alarm for 8 AM.")
            rounds += 1
        else:
            # If the request is not related to alarm, provide a friendly message
            speak("Sorry, I currently only understand 'alarm' requests. Can you please repeat?")

    # Ask user if they want to continue the interaction
    speak("Do you want to continue with another alarm-related action?")

    # Listen for user input
    text = listen()

    # Check if the user wants to continue
    if "yes" in text:
        alarm_dialogue()  # Restart the function to continue the interaction
    else:
        speak("Okay, goodbye!")
