import speech_recognition as sr
from gtts import gTTS
import os
import subprocess
from elevenlabs.client import ElevenLabs
import uuid

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Initialize the ElevenLabs client
client = ElevenLabs(
    api_key="e0c5f7b856cf59ef10a4253335714486",  # Replace with your API key
)

# Clone the voice once
voice = client.clone(
    name="Qian",
    description="dialogue_voice test",
    files=["output/output_pitch_changed_1.mp3"],  # Use the provided audio file path
)


def play_generated_audio(text):
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


def music_dialogue():
    # save all user's voice
    os.makedirs("dialogues", exist_ok=True)

    rounds = 0
    while rounds < 3:  # Only perform 3 rounds
        # Generate a unique conversation ID
        dialog_id = str(uuid.uuid4())

        # Create a new folder with the conversation ID
        os.makedirs(os.path.join("dialogues", dialog_id), exist_ok=True)

        # Listen for user input
        input_text, input_audio_file = listen()

        # Save the user's input audio
        if input_audio_file:
            os.rename(input_audio_file, os.path.join("dialogues", dialog_id, "input.wav"))

        # Check if user requests music
        if "music" in input_text:
            # Play music based on user request
            play_generated_audio("Playing some pop music.")

            # Ask user for pause/next song
            play_generated_audio("Would you like to pause or play the next song?")

            # Listen for user response
            response_text, response_audio_file = listen()

            # Save user response audio
            if response_audio_file:
                os.rename(response_audio_file, os.path.join("dialogues", dialog_id, "response.wav"))

            # Handle user response (pause/next song)
            if "pause" in response_text:
                play_generated_audio("Pausing the music.")
            elif "next song" in response_text:
                play_generated_audio("Playing the next song.")
            elif "thank" in response_text:
                play_generated_audio("you are welcome, what can i do for you ")
            else:
                play_generated_audio("Sorry, I didn't understand your request.")

            rounds += 1  # Increment rounds only for music requests
        else:
            # Handle non-music requests
            play_generated_audio("Sorry, I don't understand. Can you repeat?")
            rounds += 1  # Increment rounds even

    # Ask if the user wants to continue
    play_generated_audio("Do you want to continue with another music action?")

    # Listen for user response
    text, audio_file = listen()

    # Check if the user wants to continue


def main():
    # Welcome message
    speak("Hello, I am your voice assistant Lumi. How can I assist you today?")

    # Proceed with music-related dialogue
    music_dialogue()

    # Goodbye message
    speak("Thank you for talking with me. I wish you a lovely day")


if __name__ == "__main__":
    main()
