
import subprocess

def play_audio(file_path):
    # 构建播放命令
    command = ["ffplay", "-nodisp", "-autoexit", file_path]
    # 调用子进程执行命令
    subprocess.run(command)

if __name__ == "__main__":
    file_path = "recordings/neutral_audio.mp3"  # 音频文件路径
    play_audio(file_path)

