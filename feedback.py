import os
import pyaudio
import wave
from flask import current_app as app

def record_feedback(output_dir="feedback", duration=30, sample_rate=44100, channels=1, chunk=1024, format=pyaudio.paInt16):
    with app.app_context():  # 创建应用程序上下文
        # 检查输出目录是否存在，如果不存在则创建它
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        audio = pyaudio.PyAudio()

        # 打开一个新的流来录制音频
        stream = audio.open(format=format,
                            channels=channels,
                            rate=sample_rate,
                            input=True,
                            frames_per_buffer=chunk)

        app.logger.info("Recording...")

        frames = []

        # 录制指定时长的音频
        for _ in range(0, int(sample_rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)

        print("Finished recording.")

        # 停止并关闭流
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # 查找下一个可用的文件名
        i = 1
        while True:
            filename = os.path.join(output_dir, f"feedback_{i}.wav")
            if not os.path.exists(filename):
                break
            i += 1

        # 将录制的音频保存到 WAV 文件
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(audio.get_sample_size(format))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))

        print(f"Feedback saved as: {filename}")

