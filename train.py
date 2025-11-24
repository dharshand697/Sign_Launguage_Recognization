import numpy as np
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Conv1D, MaxPooling1D, Dropout, BatchNormalization, Bidirectional, Flatten
from sklearn.model_selection import train_test_split

# ====================================
# Config
# ====================================
DATA_DIR = r"C:\Users\Keerthi\Downloads\sign_lang_project\Dataset"
words = ["Hello", "Thank You", "Yes", "No", "I Love You", "Stop"]
sequence_length = 50

# ====================================
# Load Dataset
# ====================================
X, y = [], []

for idx, word in enumerate(words):
    folder = os.path.join(DATA_DIR, word)
    for file in os.listdir(folder):
        if file.endswith(".npy"):
            arr = np.load(os.path.join(folder, file))

            if arr.shape != (sequence_length, 63):
                continue

            # normalize
            arr = (arr - np.mean(arr)) / (np.std(arr) + 1e-6)

            X.append(arr)
            y.append(idx)

X = np.array(X)
y = np.array(y)

print("Loaded:", X.shape, y.shape)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ====================================
# HIGH ACCURACY MODEL
# ====================================
model = Sequential([
    Conv1D(128, 3, activation='relu', input_shape=(sequence_length, 63)),
    BatchNormalization(),
    MaxPooling1D(2),

    Conv1D(256, 3, activation='relu'),
    BatchNormalization(),
    MaxPooling1D(2),

    Bidirectional(LSTM(128, return_sequences=True)),
    Dropout(0.3),

    Bidirectional(LSTM(128)),
    Dropout(0.3),

    Dense(128, activation='relu'),
    Dropout(0.2),

    Dense(len(words), activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ====================================
# Train
# ====================================
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=8,
    validation_split=0.1
)

loss, acc = model.evaluate(X_test, y_test)
print(f"TEST ACCURACY: {acc}")

model.save("gesture_model1.h5")
