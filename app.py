from flask import Flask, render_template, request, jsonify
import base64, cv2, numpy as np
import mediapipe as mp
from collections import deque
import tensorflow as tf
import pyttsx3

app = Flask(__name__, static_folder="static", template_folder="templates")

# Load model
model = tf.keras.models.load_model("gesture_model1.h5")

LABELS = ["Hello", "Thank You", "Yes", "No", "I Love You", "Stop","iam hungry"]

# TTSl
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# Mediapipe
mp_hands = mp.solutions.hands
mp_proc = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# 50-frame storage per client
sequences = {}
last_prediction = {}
smooth_buffer = {}


def decode_b64_image(data_url):
    try:
        header, encoded = data_url.split(',', 1)
        img_data = base64.b64decode(encoded)
        arr = np.frombuffer(img_data, np.uint8)
        return cv2.imdecode(arr, cv2.IMREAD_COLOR)
    except:
        return None


def extract_keypoints(img_bgr):
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    res = mp_proc.process(img_rgb)

    if not res.multi_hand_landmarks:
        return None

    hand = res.multi_hand_landmarks[0]
    keypoints = []

    for lm in hand.landmark:
        keypoints.extend([lm.x, lm.y, lm.z])

    kps = np.array(keypoints, dtype=np.float32)

    # normalize
    kps = (kps - np.mean(kps)) / (np.std(kps) + 1e-6)

    return kps.tolist()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    client_id = data.get("client_id")
    img_b64 = data.get("image")

    if not client_id or not img_b64:
        return jsonify({"error": "missing parameters"}), 400

    if client_id not in sequences:
        sequences[client_id] = deque(maxlen=50)
        smooth_buffer[client_id] = deque(maxlen=5)

    img = decode_b64_image(img_b64)
    if img is None:
        return jsonify({"prediction": None, "ready": False})

    kps = extract_keypoints(img)
    if kps is None:
        sequences[client_id].append([0.0] * 63)
        return jsonify({"prediction": None, "ready": False})

    sequences[client_id].append(kps)

    if len(sequences[client_id]) == 50:
        X = np.array([list(sequences[client_id])], dtype=np.float32)
        pred = model.predict(X)[0]

        idx = int(np.argmax(pred))
        label = LABELS[idx]
        conf = float(pred[idx])

        # smoothing
        smooth_buffer[client_id].append(idx)
        most_common = max(set(smooth_buffer[client_id]), key=smooth_buffer[client_id].count)
        label = LABELS[most_common]

        try:
            engine.say(label)
            engine.runAndWait()
        except:
            pass

        return jsonify({
            "prediction": label,
            "confidence": conf,
            "ready": True
        })

    return jsonify({"prediction": None, "ready": False})


if __name__ == "__main__":
    print("🚀 Running at http://127.0.0.1:5000/")
    app.run(host="0.0.0.0", port=5000, debug=True)
