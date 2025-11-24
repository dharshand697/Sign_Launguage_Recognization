# Sign Language Word Detection (Demo Project)

**Target environment:** Windows, Python 3.9.x
**Includes:** demo Keras model placeholder, detection script with voice output, data collection and training scripts.

## Setup
1. Create a virtual environment (recommended):
   ```ps1
   python -m venv venv
   venv\Scripts\activate
   ```
2. Install dependencies:
   ```ps1
   pip install -r requirements.txt
   ```

## Files
- `collect_data.py` — Record landmark sequences using MediaPipe (to build your own dataset)
- `train.py` — Train an LSTM model on collected data (optional)
- `detect.py` — Real-time detection + male voice output (uses the included `gesture_model.h5` placeholder)
- `gesture_model.h5` — Placeholder file. To obtain a real model, run `train.py` after collecting data.
- `requirements.txt` — Python dependencies
- `README.md` — This file

## Usage (quick test)
- To run detection immediately (uses included placeholder model):
  ```ps1
  python detect.py
  ```
  Press `q` to quit.

## Notes
- The included `gesture_model.h5` is a placeholder to let you run the demo without training. 
  Predictions will be random. To get real recognition, collect data with `collect_data.py` and train with `train.py`.