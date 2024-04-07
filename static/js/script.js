
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
    console.log("Recording started.");

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
    document.getElementById("startButton").style.display = "none";
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

const surveyButton = document.getElementById('surveyButton');
const nextButton_alarm = document.getElementById('nextButton_alarm');

 // 添加跳转到调查页面的点击事件处理程序
function goToSurveyPage() {
    window.location.href = "/survey";
    surveyButton.style.display = "none";
}

function goToSurveyPage_alarm() {
    window.location.href = "/survey_alarm";

}

function goToSurveyPage_weather() {
    window.location.href = "/survey_weather";

}

function processAlarm() {
    // 执行 AJAX 请求来处理闹钟任务
    fetch('/process_alarm_task', {
        method: 'POST'
    })
    .then(response => response.text())
    .then(data => {
        // 在指定的 div 中显示响应
        document.getElementById("responseText").innerText = data;
        // 显示音乐指令文本
        document.getElementById("musicInstructions").style.display = "block";
    })
    .catch(error => console.error('Error:', error));
}


function processWeather() {
    // 执行 AJAX 请求来处理闹钟任务
    fetch('/process_weather_task', {
        method: 'POST'
    })
    .then(response => response.text())
    .then(data => {

        document.getElementById("responseText").innerText = data;
        document.getElementById("musicInstructions").style.display = "block";
    })
    .catch(error => console.error('Error:', error));
}

document.addEventListener("DOMContentLoaded", function() {
    // 在文档加载完成后执行以下代码

    // 获取按钮和提示文字的引用
    var startFeedbackButton = document.getElementById("startFeedbackButton");
    var feedbackMessage = document.getElementById("feedbackMessage");

    // 为按钮添加点击事件监听器
    startFeedbackButton.addEventListener("click", function() {
        // 显示提示文字
        feedbackMessage.style.display = "block";

        // 创建一个 FormData 对象，用于发送表单数据
        var formData = new FormData();
        formData.append('duration', "5"); // 默认录音时长为 5 秒

        // 发送 POST 请求到 Flask 服务器开始录音
        fetch('/feedback', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                console.log("Feedback recording started.");
                // 在这里可以添加一些界面交互，例如显示录音已开始的消息等
            } else {
                console.error("Failed to start feedback recording.");
            }
        })
        .catch(error => {
            console.error("Error starting feedback recording:", error);
        });
    });
});



const video = document.getElementById('video');
const canvas = document.getElementById('canvas');

Promise.all([
    faceapi.nets.ssdMobilenetv1.loadFromUri('/models'),
    faceapi.nets.faceExpressionNet.loadFromUri('/models')
])
    .then(startVideo)
    .catch(err => console.error(err));

async function startVideo() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
            video.play();
            processVideo();
        })
        .catch(err => console.error(err));
}

function processVideo() {
  const displaySize = { width: video.width, height: video.height };
  faceapi.matchDimensions(canvas, displaySize);

  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      const context = canvas.getContext('2d');

      const drawBox = (detection, expressions, context) => {
        const box = detection.detection.box;
        const drawSize = new faceapi.Size(video.width, video.height);
        const resizedBox = faceapi.resizeResults(box, drawSize);

        context.strokeStyle = 'blue';
        context.lineWidth = 2;
        context.rect(resizedBox.x, resizedBox.y, resizedBox.width, resizedBox.height);
        context.stroke();

        // Display expression labels
        const expressionsArray = Object.entries(expressions);
        const topExpression = expressionsArray.reduce((prev, curr) => curr[1] > prev[1] ? curr : prev);
        context.font = "24px Arial";
        context.fillStyle = "white";
        context.fillText(topExpression[0], resizedBox.x + 5, resizedBox.y + resizedBox.height + 15);

        // Perform actions based on expression (replace with your logic)
        const audioElement = document.getElementById(topExpression[0]);
        if (audioElement) {
          audioElement.play();
        } else {
          console.log(`No audio for expression: ${topExpression[0]}`);
        }
      };

      video.onplay = () => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        setInterval(async () => {
          try {
            const detections = await faceapi.detectAllFaces(video, new faceapi.SsdMobilenetv1Options())
              .withFaceExpressions();
            const resizedDetections = faceapi.resizeResults(detections, displaySize);
            canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);

            resizedDetections.forEach(detection => drawBox(detection, detection.expressions, context));
          } catch (err) {
            console.error('Error processing video:', err);
          }
        }, 100); // Process video every 100 milliseconds
      };
    })
    .catch(err => console.error('Error accessing video stream:', err));
}

function countdown() {
            // 启动倒计时
            var seconds = 30;
            var countdownDisplay = document.getElementById('countdown');

            var countdownInterval = setInterval(function() {
                seconds--;
                countdownDisplay.textContent = seconds;

                if (seconds <= 0) {
                    clearInterval(countdownInterval);
                    countdownDisplay.textContent = 'Time up!';
                    // 在这里可以调用发送录音请求的函数
                    // sendRecordingRequest();
                }
            }, 1000);
        }