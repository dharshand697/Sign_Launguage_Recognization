// Path: /mnt/data/static/main.js

// ===============================
//  main.js (working version)
// ===============================

// DOM elements
const video = document.getElementById("webcam");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");

const predText = document.getElementById("prediction");
const confText = document.getElementById("confidence");
const fpsText = document.getElementById("fps");

// Unique ID per client
const client_id = Math.random().toString(36).substring(2);

// ------------------ Webcam Start ------------------
async function startWebcam() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: true
        });

        video.srcObject = stream;
        video.play();

        console.log("📷 Webcam started");
        startPredictionLoop();
    } catch (err) {
        console.error("❌ Webcam error:", err);
        alert("Unable to access webcam.");
    }
}

startBtn && (startBtn.onclick = startWebcam);

// ------------------ Capture Frame ------------------
function captureFrame() {
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    return canvas.toDataURL("image/jpeg", 0.6);
}

// ------------------ Send Frame to Backend ------------------
async function sendFrame() {
    const img_b64 = captureFrame();

    const body = {
        client_id: client_id,
        image: img_b64
    };

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            console.warn("⚠️ Predict returned error:", response.status);
            return;
        }

        const data = await response.json();

        // Update UI when model is ready
        if (data.ready && data.prediction) {
            predText && (predText.innerText = data.prediction);
            confText && (confText.innerText = (data.confidence * 100).toFixed(2) + "%");
        }

    } catch (err) {
        console.error("❌ Error sending frame:", err);
    }
}

// ------------------ FPS Counter ------------------
let lastFrameTime = performance.now();

function updateFPS() {
    const now = performance.now();
    const fps = Math.round(1000 / (now - lastFrameTime));
    lastFrameTime = now;

    fpsText && (fpsText.innerText = fps);
}

// ------------------ Prediction Loop ------------------
let predictionInterval = null;
function startPredictionLoop() {
    if (predictionInterval) return; // avoid duplicates
    predictionInterval = setInterval(() => {
        sendFrame();
        updateFPS();
    }, 200); // 5 FPS
}

function stopPredictionLoop() {
    if (predictionInterval) {
        clearInterval(predictionInterval);
        predictionInterval = null;
    }
}

stopBtn && (stopBtn.onclick = stopPredictionLoop);

// Safety: if DOM elements missing, log a helpful message
if (!video) console.warn("Missing video element with id=webcam");
if (!startBtn) console.warn("Missing button with id=startBtn");
if (!stopBtn) console.warn("Missing button with id=stopBtn");
if (!predText) console.warn("Missing element with id=prediction");
if (!confText) console.warn("Missing element with id=confidence");
if (!fpsText) console.warn("Missing element with id=fps");
