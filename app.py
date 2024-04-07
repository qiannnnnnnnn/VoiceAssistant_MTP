from flask import Flask, render_template, request, jsonify, redirect, url_for
from record import record_audio
from news_task import news_task
from alarm_task import alarm_task
from weather_task import weather_task
from feedback import record_feedback
from flask_socketio import SocketIO

from elevenlabs.client import ElevenLabs
import os
import subprocess

app = Flask(__name__, template_folder="templates", static_folder="static")


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

    subprocess.call(["ffmpeg", "-i", os.path.join("output", "output_audio.mp3"), "-af", "rubberband=pitch=2.0", os.path.join("output", "output_pitch_changed_1.wav")])
    #subprocess.call(["ffplay", os.path.join("output", "output_pitch_changed_1.wav")])
    
    subprocess.call(["ffmpeg", "-i", os.path.join("output", "output_audio.mp3"), "-af", "rubberband=pitch=1.5", os.path.join("output", "output_pitch_changed_2.wav")])
    #subprocess.call(["ffplay", os.path.join("output", "output_pitch_changed_2.wav")])
    # 
    subprocess.call(["ffmpeg", "-i", os.path.join("output", "output_audio.mp3"), "-af", "rubberband=pitch=0.5", os.path.join("output", "output_pitch_changed_3.wav")])
    #subprocess.call(["ffplay", os.path.join("output", "output_pitch_changed_3.wav")])
'''

# Add questionnaire
@app.route('/survey')
def survey():
    app.logger.info("Loading survey page")
    return render_template('survey.html')

@app.route('/survey_alarm')
def survey_alarm():
    app.logger.info("Loading survey page")
    return render_template('survey_alarm.html')


@app.route('/survey_weather')
def survey_weather():
    app.logger.info("Loading survey page")
    return render_template('survey_weather.html')

@app.route('/alarm.html')
def alarm_page():
    return render_template('alarm.html')

@app.route('/weather.html')
def weather_page():
    return render_template('weather.html')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feedback.html')
def feedback_page():
    return render_template('feedback.html')


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

    news_task()
    return "done"

@app.route('/process_alarm_task',methods=['POST'])
def process_alarm_task():

    alarm_task()

    return "done"

@app.route('/process_weather_task',methods=['POST'])
def process_weather_task():

    weather_task()
    return "done"

@app.route('/feedback', methods=['POST'])
def feedback_record():
    feedback_dir = "feedback"
    try:
        audio_file = record_feedback(feedback_dir)
        return "Recording completed."
    except Exception as e:
        return "Error recording feedback.", 500


if __name__ == '__main__':
    app.run(debug=True)

