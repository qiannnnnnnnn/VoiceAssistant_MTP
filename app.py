from flask import Flask, render_template, request, jsonify, redirect, url_for
from record import record_audio,change_pitch
from news_task import news_task
from alarm_task import alarm_task
from weather_task import weather_task
from feedback import record_feedback
from devices_task import devices_task
from flask_socketio import SocketIO
from flask import Flask, request, send_file
import record


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
        name="Participant",
        description="participant's original voice",
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


   # Two semitones
    subprocess.call(["ffmpeg", "-i", os.path.join("output", "output_audio.mp3"), atempo=1.1892071150027210667977499790004,asetrate=44100*1.1892071150027210667977499790004", 
    os.path.join("output", "output_pitch_changed_1.wav")])
    #subprocess.call(["ffplay", os.path.join("output", "output_pitch_changed_1.wav")])
    
    # Three semitones
    subprocess.call(["ffmpeg", "-i", os.path.join("output", "output_audio.mp3"), atempo=1.4142135623730950488016887242097,asetrate=44100*1.4142135623730950488016887242097,
    os.path.join("output", "output_pitch_changed_2.wav")])
    #subprocess.call(["ffplay", os.path.join("output", "output_pitch_changed_2.wav")])
    
    # Four semitones
    subprocess.call(["ffmpeg", "-i", os.path.join("output", "output_audio.mp3"), atempo=1.6588743236448599122977960769231,asetrate=44100*1.6588743236448599122977960769231",
    os.path.join("output", "output_pitch_changed_3.wav")])
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
@app.route('/survey_devices')
def survey_devices():
    app.logger.info("Loading survey page")
    return render_template('survey_devices.html')


@app.route('/alarm.html')
def alarm_page():
    return render_template('alarm.html')


@app.route('/news.html')
def news_page():
    return render_template('news.html')

@app.route('/weather.html')
def weather_page():
    return render_template('weather.html')

@app.route('/devices.html')
def devices_page():
    return render_template('devices.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feedback.html')
def feedback_page():
    return render_template('feedback.html')


from flask import jsonify  # 导入 jsonify

'''
@app.route('/process_voice', methods=['POST'])
def process_voice():
    app.logger.info("Received POST request to /process_voice")

    # 执行 news_task() 函数
    news_task()

    # 返回一个表示成功的 JSON 响应
    return jsonify({"success": True})
'''

@app.route('/record_voice', methods=['POST'])
def record_voice():
    output_dir = "recordings"
    try:
        filename = request.form.get('filename', 'recorded_audio.wav')
        audio_file = record_audio(output_dir, filename)
        pitch_changed_file = change_pitch(audio_file, os.path.join(output_dir, "pitch_changed.wav"), 1.1892)

        if pitch_changed_file:
            print("Modified audio saved at:", pitch_changed_file)

            # 调用 process_voice() 函数来处理录音后的自动任务执行
            # process_voice()  # 将这行代码移到这里

            return send_file(pitch_changed_file, as_attachment=True)
        else:
            return "Error changing pitch.", 500
    except Exception as e:
        print("Error recording audio:", e)
        return "Error recording audio.", 500



'''
@app.route('/process_alarm_task',methods=['POST'])
def process_alarm_task():

    alarm_task()

    return "done"
'''


@app.route('/process_news_task',methods=['POST'])
def process_news_task():

    news_task()
    return "done"


@app.route('/process_weather_task',methods=['POST'])
def process_weather_task():

    weather_task()
    return "done"

@app.route('/process_devices_task',methods=['POST'])
def process_devices_task():

    devices_task()
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

