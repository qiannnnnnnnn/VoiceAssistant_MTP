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

// script.js
// script.js

// script.js

function startRecording() {
    console.log("Recording started."); // 添加这行日志，用于检查函数是否被调用

    // 创建文本元素
    var textElement = document.createElement('p');
    textElement.innerHTML = "Hi! I'm Lumi, your voice assistant.<br>I'll be guiding you through a short experiment that should take about 10 minutes.<br><br>Here's how it will go:<br><br>1. I'll present you with a short text to read.<br>2. We'll then move on to three tasks. In each task, you'll give me instructions by voice, telling me what you want me to accomplish.<br>3. Throughout the experiment, I'll ask you to share how you're feeling.<br>4. Finally, you'll have the chance to record your overall experience.<br><br>Let's Begin!";
    textElement.style.textAlign = "center"; // 居中文本
    document.body.appendChild(textElement);


    // 向服务器发送录音请求
    fetch('/record_voice', {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            console.log("Recording started.");
        } else {
            console.error("Failed to start recording.");
        }
    })
    .catch(error => {
        console.error("Error starting recording:", error);
    });
}
