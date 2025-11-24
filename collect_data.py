import cv2
import numpy as np
import mediapipe as mp
import os

# Configuration
words = ["Hello", "Thank You", "Yes", "No", "I Love You", "Stop","iam hungry"]
num_sequences = 50
sequence_length = 50
DATA_DIR = "Dataset"

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
for w in words:
    os.makedirs(os.path.join(DATA_DIR, w), exist_ok=True)

cap = cv2.VideoCapture(0)

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    for idx, word in enumerate(words):
        print(f"Starting collection for: {word}")
        for seq in range(num_sequences):
            data = []
            print(f" Sequence {seq+1}/{num_sequences} - perform the gesture now")
            for frame_num in range(sequence_length):
                ret, frame = cap.read()
                if not ret:
                    continue
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(image)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                keypoints = []
                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    for lm in hand_landmarks.landmark:
                        keypoints.extend([lm.x, lm.y, lm.z])
                    mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                else:
                    keypoints = [0.0] * 63

                data.append(keypoints)

                cv2.putText(image, f"{word} Seq:{seq+1} Frame:{frame_num+1}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                cv2.imshow("Collect Data - Press q to abort", image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            np.save(os.path.join(DATA_DIR, word, f"{seq}.npy"), np.array(data))

cap.release()
cv2.destroyAllWindows()
print("Data collection finished.")