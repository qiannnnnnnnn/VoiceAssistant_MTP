const listenButton = document.getElementById('listenButton');
const responseDiv = document.getElementById('response');

listenButton.addEventListener('click', async () => {
  // Simulate voice input by making an API call to your python backend
  // This part requires further implementation based on your backend setup
  const response = await fetch('/api/listen');
  const text = await response.text();
  responseDiv.textContent = text;
});


document.getElementById("startButton").addEventListener("click", function() {
    startRecording();
});

// Function to handle the start of recording
function startRecording() {
    console.log("Recording started."); // 添加这行日志，用于检查函数是否被调用

    // 创建文本元素
    var textElement = document.createElement('p');
    textElement.innerHTML = "Hi! I'm Lumi, your voice assistant.<br>I'll be guiding you through a short experiment that should take about 10 minutes.<br><br>Here's how it will go:<br><br>1. I'll present you with a short text to read.<br>2. We'll then move on to three tasks. In each task, you'll give me instructions by voice, telling me what you want me to accomplish.<br>3. Throughout the experiment, I'll ask you to share how you're feeling.<br>4. Finally, you'll have the chance to record your overall experience.<br><br>Let's Begin!";
    textElement.style.textAlign = "justify";
    textElement.style.fontSize = "30px";
    textElement.style.fontFamily = "San Francisco, system-ui";
    textElement.style.maxWidth = "600px";
    textElement.style.margin = "0 auto";
    textElement.style.color = "#666";
    document.body.appendChild(textElement);


    // Show the recognizing button
    document.getElementById("recognizingButton").style.display = "inline";

    // Perform AJAX request to start recording
    fetch('/record_voice', {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            console.log("Recording started.");
            // Once recording is started, proceed with processing the voice
            processVoice();
            // 移除前面的文本元素
            document.body.removeChild(textElement);
            // 显示音乐指令文本
            document.getElementById("musicInstructions").style.display = "block";
        } else {
            console.error("Failed to start recording.");
        }
    })
    .catch(error => {
        console.error("Error starting recording:", error);
    });
}



// websocket.js

const socket = io();
socket.on('task_started', function(data) {
    if (data.task === 'music') {
        document.getElementById('musicInstructions').style.display = 'block';
        document.getElementById('alarmInstructions').style.display = 'none';
        document.getElementById('weatherInstructions').style.display = 'none';
    } else if (data.task === 'alarm') {
        document.getElementById('musicInstructions').style.display = 'none';
        document.getElementById('alarmInstructions').style.display = 'block';
        document.getElementById('weatherInstructions').style.display = 'none';
    } else if (data.task === 'weather') {
        document.getElementById('musicInstructions').style.display = 'none';
        document.getElementById('alarmInstructions').style.display = 'none';
        document.getElementById('weatherInstructions').style.display = 'block';
    }
});

socket.on('task_completed', function(data) {
     console.log('WebSocketconnented');
    const task = data.task;
    if (task === 'music' || task === 'alarm' || task === 'weather') {
        hideInstructions();
    }
});

function hideInstructions() {
    document.getElementById('musicInstructions').style.display = 'none';
    document.getElementById('alarmInstructions').style.display = 'none';
    document.getElementById('weatherInstructions').style.display = 'none';
}




// Function to process voice after recording
function processVoice() {
    // Perform AJAX request to process voice
    fetch('/process_voice', {
        method: 'POST'
    })
    .then(response => response.text())
    .then(data => {
        // Display response in the designated div
        document.getElementById("responseText").innerText = data;

        // Reset button text and hide recognizing button
        document.getElementById("recognizingButton").style.display = "none";

        // 显示音乐指令文本
        document.getElementById("musicInstructions").style.display = "block";
    })
    .catch(error => console.error('Error:', error));
}

