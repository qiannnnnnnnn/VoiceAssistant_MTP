from flask import Flask, render_template, request
from voiceassistant import main as voice_assistant_main

# Initialize variables to store recognized text and assistant response
recognized_text = ""
assistant_response = ""

app = Flask(__name__, template_folder='templates')

@app.route("/", methods=["GET", "POST"])
def index():
    global recognized_text, assistant_response
    if request.method == "POST":
        recognized_text = request.form["recognized_text"]
        assistant_response = handle_user_request(recognized_text)  # Call your dialogue function

    return render_template("index.html", recognized_text=recognized_text, assistant_response=assistant_response)

# Replace this with your dialogue management functions
def handle_user_request(text):
    # Call the main function of voice assistant from Voiceassistant.py
    return voice_assistant_main()

if __name__ == "__main__":
    app.run(debug=True)
