from flask import Flask, render_template, request
from dialogue import speak, listen, music_dialogue

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/handle_request', methods=['POST'])
def handle_request():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'speak':
            text = request.form['text']
            speak(text)
        elif action == 'listen':
            text, _ = listen()
            return text
        elif action == 'music_dialogue':
            music_dialogue()
        return "Request completed successfully"

if __name__ == '__main__':
    app.run(debug=True)
