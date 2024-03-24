import speech_recognition as sr
import pyttsx3
import os
import subprocess

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Initialize the TTS engine
engine = pyttsx3.init()

# Set the custom voice file
engine.setProperty('voice', os.path.join('output', 'output_pitch_changed_1.mp3'))

def play_generated_audio(text, audio_file):
    try:
        # 使用 subprocess.Popen() 播放生成的音频
        ffplay_process = subprocess.Popen(["ffplay", "-autoexit", "-nodisp", "-"], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 将音频流写入 ffplay 进程的标准输入
        with open(audio_file, "rb") as f:
            for chunk in f.read(4096):
                ffplay_process.stdin.write(chunk)

        # 关闭标准输入，等待音频播放完毕
        ffplay_process.stdin.close()
        ffplay_process.wait()
    except Exception as e:
        print("Error while playing audio:", e)

def tts_init(text, lang="en"):
    # Use the custom voice provided by pyttsx3
    return engine.say(text)

def speak(text):
    engine.runAndWait()

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

def music_dialogue():
    rounds = 0
    while rounds < 3:  # 只进行 3 轮对话
        # 听取用户输入
        text = listen()

        # 检查用户是否请求播放音乐
        if "music" in text:
            # 根据用户请求播放音乐
            play_generated_audio("Playing some pop music.", "output/output_pitch_changed_1.mp3")

            # 询问用户是否暂停音乐或播放下一首歌曲
            speak("Would you like to pause or play the next song?")

            # 听取用户输入
            text = listen()

            # 检查用户的响应
            if "pause" in text:
                speak("Pausing the music.")
            elif "next song" in text:
                speak("Playing the next song.")
            else:
                speak("Sorry, I didn't understand your request.")

            rounds += 1
        else:
            # 如果请求与播放音乐无关，则提供友好提示
            speak("Sorry, I don't understand. Can you repeat?")
            rounds += 1  # 在无法识别用户输入时也增加 rounds 的计数

    # 询问用户是否要继续互动
    speak("Do you want to continue with another music action?")

    # 听取用户输入
    text = listen()

    # 检查用户是否要继续
    if "yes" in text:
        music_dialogue()  # 重新启动函数以继续互动
    else:
        speak("Okay, goodbye!")


def main():
    # 欢迎消息
    speak("Hello, I am your voice assistant Lumi. How can I assist you today?")

    # 进行与音乐相关的对话
    music_dialogue()

    # 再见消息
    speak("Thank you for talking with me. I wish you a lovely day ahead!")


if __name__ == "__main__":
    main()
