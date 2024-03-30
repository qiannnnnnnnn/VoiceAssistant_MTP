from flask import Flask, render_template, request, jsonify, redirect, url_for
from record import record_audio
from music_task import music_task
from alarm_task import alarm_task
from weather_task import weather_task
from flask_socketio import SocketIO

from elevenlabs.client import ElevenLabs
import os
import subprocess

app = Flask(__name__, template_folder="templates", static_folder="static")
socketio = SocketIO(app)

'''
暂时用不到
def clone_voice(audio_file):
    client = ElevenLabs(
        api_key="e0c5f7b856cf59ef10a4253335714486", 
    )

    voice = client.clone(
        name="Qian",
        description="testing,female voice",
        files=[audio_file],
    )

    audio_generator = client.generate(text="Hi! I'm a cloned voice!", voice=voice)

    # Check and create output folder if necessary
    if not os.path.exists("output"):
        os.mkdir("output")

    # Save the generated audio to the output folder
    with open(os.path.join("output", "output_audio.mp3"), "wb") as f:
        for chunk in audio_generator:
            f.write(chunk)

    # Modify pitch using ffmpeg
    subprocess.call(["ffmpeg", "-i", os.path.join("output", "output_audio.mp3"), "-af", "asetrate=44100*1.1,atempo=0.9", os.path.join("output", "output_pitch_changed_1.wav")])
    subprocess.call(["ffplay", os.path.join("output", "output_pitch_changed_1.wav")])

    subprocess.call(["ffmpeg", "-i", os.path.join("output", "output_audio.mp3"), "-af", "asetrate=44100*1.1,atempo=1.5", os.path.join("output", "output_pitch_changed_2.wav")])
    subprocess.call(["ffplay", os.path.join("output", "output_pitch_changed_2.wav")])

    subprocess.call(["ffmpeg", "-i", os.path.join("output", "output_audio.mp3"), "-af", "asetrate=44100*1.1,atempo=0.5", os.path.join("output", "output_pitch_changed_3.wav")])
    subprocess.call(["ffplay", os.path.join("output", "output_pitch_changed_3.wav")])
'''


# Add questionnaire
@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/submit_survey', methods=['POST'])
def submit_survey():
    # 获取问卷数据
    survey_data = request.form
    # 在这里对问卷数据进行处理，例如保存到数据库中

    # 重定向到下一个对话
    return redirect(url_for('next_dialogue'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record_voice', methods=['POST'])
def record_voice():
    app.logger.info("Received POST request to /record_voice")
    output_dir = "recordings"
    try:
        audio_file = record_audio(output_dir)
        app.logger.info("Recording completed. Audio file saved at: %s", audio_file)
        return "Recording completed."
    except Exception as e:
        app.logger.error("Error recording audio: %s", str(e))
        return "Error recording audio.", 500


@app.route('/process_voice', methods=['POST'])
def process_voice():
    app.logger.info("Received POST request to /process_voice")
    # 发送音乐任务开始消息
    socketio.emit('task_started', {'task': 'music'})
    music_task()
    socketio.emit('task_completed', {'task': 'music'})

    # 发送闹钟任务开始消息
    socketio.emit('task_started', {'task': 'alarm'})
    alarm_task()
    socketio.emit('task_completed', {'task': 'alarm'})

    # 发送天气任务开始消息
    socketio.emit('task_started', {'task': 'weather'})
    weather_task()
    socketio.emit('task_completed', {'task': 'weather'})


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)


