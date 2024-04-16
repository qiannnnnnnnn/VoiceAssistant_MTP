document.addEventListener("DOMContentLoaded", function() {
    const listenButton = document.getElementById('listenButton');
    const startButton = document.getElementById("startButton");
    const surveyButton = document.getElementById('surveyButton');
    const surveyButton_alarm = document.getElementById('surveyButton_alarm');
    const surveyButton_devices = document.getElementById('surveyButton_devices');
    const surveyButton_weather = document.getElementById('surveyButton_weather');
    const processAlarmButton = document.getElementById('processAlarmButton');
    const processDevicesButton = document.getElementById('processDevicesButton');
    const processWeatherButton = document.getElementById('processWeatherButton');
    const startFeedbackButton = document.getElementById("startFeedbackButton");
    const video = document.getElementById('video');
    const countdownDisplay = document.getElementById('countdown');

    // 定义一个全局变量，用来保存所有页面的表情数据
    let allFacialData = [];

    if (listenButton) {
        listenButton.addEventListener('click', async () => {
            const response = await fetch('/api/listen');
            const text = await response.text();
            document.getElementById('response').textContent = text;
        });
    }

    if (startButton) {
        startButton.addEventListener("click", function() {
            startRecording();
        });
    }

    if (surveyButton) {
        surveyButton.addEventListener("click", goToSurveyPage);
    }

    if (surveyButton_alarm) {
        surveyButton_alarm.addEventListener("click", goToSurveyPage_alarm);
    }

    if (surveyButton_devices) {
        surveyButton_devices.addEventListener("click", goToSurveyPage_devices);
    }

    if (surveyButton_weather) {
        surveyButton_weather.addEventListener("click", goToSurveyPage_weather);
    }
    if (processAlarmButton){
        processAlarmButton.addEventListener('click',processAlarm)
    }

    if (processDevicesButton){
        processDevicesButton.addEventListener('click',processDevices)
    }

    if (processWeatherButton){
        processWeatherButton.addEventListener('click',processWeather)
    }


    if (startFeedbackButton) {
    startFeedbackButton.addEventListener("click", function() {
        const feedbackMessage = document.getElementById("feedbackMessage");
        feedbackMessage.style.display = "block";

        var formData = new FormData();
        formData.append('duration', "5");

        fetch('/feedback', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                console.log("Feedback recording started.");
                // 启动倒计时
                countdown();
            } else {
                console.error("Failed to start feedback recording.");
            }
        })
        .catch(error => {
            console.error("Error starting feedback recording:", error);
        });
    });
    }


    if (video) {
        startVideo();
    }
    Promise.all([
      faceapi.nets.tinyFaceDetector.loadFromUri('/static/js/models'),
      faceapi.nets.faceLandmark68Net.loadFromUri('/static/js/models'),
      faceapi.nets.faceRecognitionNet.loadFromUri('/static/js/models'),
      faceapi.nets.faceExpressionNet.loadFromUri('/static/js/models')
    ]).then(startVideo);


      function startVideo() {
      navigator.getUserMedia(
        { video: {} },
        stream => video.srcObject = stream,
        err => console.error(err)
      )
    }

    video.addEventListener('play', () => {
      const canvas = faceapi.createCanvasFromMedia(video)
      document.body.append(canvas)
      const displaySize = { width: video.width, height: video.height }
      faceapi.matchDimensions(canvas, displaySize)
      setInterval(async () => {
        const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions()
        const resizedDetections = faceapi.resizeResults(detections, displaySize)
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
        //faceapi.draw.drawDetections(canvas, resizedDetections)
        //faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)
        faceapi.draw.drawFaceExpressions(canvas, resizedDetections)
        // 将识别到的表情数据添加到全局数组中
          const timestamp = Date.now();
          const facialData = { timestamp, expressions: resizedDetections.map(det => det.expressions) };
          allFacialData.push(facialData);
      }, 1000) //修改表情识别间隔
    });



    if (countdownDisplay) {
        countdown();
    }

    function countdown() {
        var seconds = 30;

        var countdownInterval = setInterval(function() {
            seconds--;
            countdownDisplay.textContent = seconds;

            if (seconds <= 0) {
                clearInterval(countdownInterval);
                countdownDisplay.textContent = 'Time up!';
            }
        }, 1000);
    }

    function startRecording() {
    console.log("Recording started.");

    var textElement = document.createElement('p');
    textElement.innerHTML = "Hi! I'm Lumi, your voice assistant.<br>I'd like to guide you through a quick experiment that shouldn't take longer than 15 minutes. <br><br>Here's what to expect:<br><br>Firsty, imagine yourself relaxing at your own home, using your voice to get things done.<br>Secondly,There will be three tasks in total, Lumi is here to assist you.<br>After every task, you'll be asked to fill out a short survey, please use mouse to click the survey button when needed<br>Finally, you'll have the chance to record your overall experience about the experiment.<br><br>Let's Begin!";
    textElement.style.textAlign = "justify";
    textElement.style.fontSize = "30px";
    textElement.style.fontFamily = "San Francisco, system-ui";
    textElement.style.maxWidth = "600px";
    textElement.style.margin = "0 auto";
    textElement.style.color = "#666";
    document.body.appendChild(textElement);

    //save as a document

    document.getElementById("recognizingButton").style.display = "inline";

    fetch('/record_voice', {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            console.log("Recording started.");
            processVoice();
            document.body.removeChild(textElement);
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


    function goToSurveyPage() {
        window.location.href = "/survey";
        surveyButton.style.display = "none";
    }

    function goToSurveyPage_alarm() {
        window.location.href = "/survey_alarm";
    }

    function goToSurveyPage_devices() {
        window.location.href = "/survey_devices";
    }

    function goToSurveyPage_weather() {
        window.location.href = "/survey_weather";
    }

   function processAlarm() {
    fetch('/process_alarm_task', {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            console.log("Alarm task processed.");
            // Optionally, handle any UI updates after processing the task
        } else {
            console.error("Failed to process alarm task.");
        }
    })
    .catch(error => {
        console.error("Error processing alarm task:", error);
    });
    }

    function processDevices() {
    fetch('/process_devices_task', {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            console.log("Devices task processed.");
            // Optionally, handle any UI updates after processing the task
        } else {
            console.error("Failed to process Devices task.");
        }
    })
    .catch(error => {
        console.error("Error processing Devices task:", error);
    });
    }


    function processWeather() {
    fetch('/process_weather_task', {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            console.log("Weather task processed.");
            // Optionally, handle any UI updates after processing the task
        } else {
            console.error("Failed to process Weather task.");
        }
    })
    .catch(error => {
        console.error("Error processing Weather task:", error);
    });
    }


    // 设置保存文件的时间，分*秒*毫秒
    setInterval(saveDataToFile, 10 * 60 * 1000);

    // 在需要保存数据时调用此函数
    function saveDataToFile() {
        // 将全局数据数组转换为 JSON 字符串
        const jsonData = JSON.stringify(allFacialData);

        // 创建一个 Blob 对象，用于保存 JSON 数据
        const blob = new Blob([jsonData], { type: 'application/json' });

        // 创建一个下载链接，并设置相关属性
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'facial_data.json';

        // 模拟点击下载链接
        a.click();

        // 释放 URL 对象
        URL.revokeObjectURL(url);
    }


});

