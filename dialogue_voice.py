import speech_recognition as sr
from gtts import gTTS
import os
import subprocess
from elevenlabs.client import ElevenLabs

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Initialize the ElevenLabs client
client = ElevenLabs(
    api_key="e0c5f7b856cf59ef10a4253335714486",  # 替换为您的 API 密钥
)

# Define a function to play audio generated using ElevenLabs
def play_generated_audio(text, audio_file):
    try:
        voice = client.clone(
            name="Qian",
            description="An old American male voice with a slight hoarseness in his throat. Perfect for news",
            files=[audio_file],  # 使用提供的音频文件路径
        )

        audio_generator = client.generate(text=text, voice=voice)

        # 使用 subprocess.Popen() 播放生成的音频
        ffplay_process = subprocess.Popen(["ffplay", "-autoexit", "-nodisp", "-"], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 将音频流写入 ffplay 进程的标准输入
        for chunk in audio_generator:
            ffplay_process.stdin.write(chunk)

        # 关闭标准输入，等待音频播放完毕
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
            play_generated_audio("Would you like to pause or play the next song?", "output/output_pitch_changed_1.mp3")

            # 听取用户输入
            text = listen()

            # 检查用户的响应
            if "pause" in text:
                play_generated_audio("Pausing the music.", "output/output_pitch_changed_1.mp3")
            elif "next song" in text:
                play_generated_audio("Playing the next song.", "output/output_pitch_changed_1.mp3")
            else:
                play_generated_audio("Sorry, I didn't understand your request.", "output/output_pitch_changed_1.mp3")

            rounds += 1
        else:
            # 如果请求与播放音乐无关，则提供友好提示
            play_generated_audio("Sorry, I don't understand. Can you repeat?", "output/output_pitch_changed_1.mp3")
            rounds += 1  # 在无法识别用户输入时也增加 rounds 的计数

    # 询问用户是否要继续互动
    play_generated_audio("Do you want to continue with another music action?", "output/output_pitch_changed_1.mp3")

    # 听取用户输入
    text = listen()

    # 检查用户是否要继续
    if "yes" in text:
        music_dialogue()  # 重新启动函数以继续互动
    else:
        play_generated_audio("Okay, goodbye!", "output/output_pitch_changed_1.mp3")


def main():
    # 欢迎消息
    speak("Hello, I am your voice assistant Lumi. How can I assist you today?")

    # 进行与音乐相关的对话
    music_dialogue()

    # 再见消息
    speak("Thank you for talking with me. I wish you a lovely day ahead!")


if __name__ == "__main__":
    main()
