This VoiceAssistant_MTP is part of my Master thesis Project.

# Lumi Voice Assistant

Lumi is a web-based voice user interface (VUI) developed with the Flask framework, Python, and JavaScript. Designed for a smart home context, Lumi acts as a voice assistant with three different types of voices: non-cloned, half-cloned, and fully-cloned. This project allows participants to interact with Lumi through various smart home tasks such as discussing sports news, controlling home devices, and receiving weather updates.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Voice Recording and Cloning](#voice-recording-and-cloning)
  - [Interactions with VUI](#interactions-with-vui)
- [System Architecture](#system-architecture)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/your-repo-name.git
    ```
2. Change to the repository directory:
    ```sh
    cd your-repo-name
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Voice Recording and Cloning

Participants begin by reading a text paragraph for 30 seconds, recorded using local computer microphones. These recordings serve as source material for voice cloning using the ElevenLabs voice clone API. The cloned voice is manipulated to produce variations using the PyAudio Python library:

- **Non-Cloned Voice**: A middle-aged person with an American accent, without gender-specific characteristics.
- **Half-Cloned Voice**: The pitch of the cloned voice is increased by 2.33 semitones using PyAudio.
- **Fully-Cloned Voice**: A replica of the voice recorded from the participant using ElevenLabs.

These voices are used to produce speech for communication with participants in each round.

### Interactions with VUI

Participants interact with the Lumi voice assistant through three tasks related to the smart home environment:

1. Discussing sports news.
2. Controlling home devices.
3. Receiving weather updates.

The dialogues are structured around these topics, each including 8 to 15 responses. Lumi uses Google Cloud services for speech recognition and ElevenLabs text-to-speech APIs to respond appropriately based on the extracted keywords.

## System Architecture

Lumi's development utilized the Flask framework to connect front-end HTML web pages with back-end programs. This setup allows participants to interact with Lumi via web pages and microphones on their local computers. The key components include:

- **Voice Recording**: Uses PyAudio for recording participants' speech.
- **Voice Cloning**: Utilizes ElevenLabs API for voice cloning and PyAudio for pitch modification.
- **Speech Recognition**: Employs Google Cloud services for speech-to-text conversion.
- **Text-to-Speech**: Uses ElevenLabs API for generating responses.
- **Face Expression Recognition**: Implements face-api.js for detecting and recognizing facial expressions using the webcam.

The web application consists of nine sub-web pages, including interaction and questionnaire pages. Interactions are saved as audio files, and questionnaire responses are collected via LimeSurvey. The final page records one-minute feedback from participants using PyAudio.

![System Architecture of Lumi](figures/plot_MTP/lumi_structure.png)

## Contributing

We welcome contributions! Please read our [contributing guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
