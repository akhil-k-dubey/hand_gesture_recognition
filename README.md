# Hand Gesture Recognition

A real-time hand gesture recognition system using computer vision. This project captures hand landmarks from your webcam, trains a machine learning classifier on your custom gestures, and performs live gesture predictions.

## Features

- 🎥 **Real-time Webcam Input**: Capture video frames directly from your webcam
- ✋ **Hand Landmark Detection**: Uses MediaPipe to detect 21 hand keypoints (fingertips, knuckles, wrist)
- 📊 **Custom Gesture Training**: Collect and train on your own gesture definitions
- 🤖 **Machine Learning Classifier**: Random Forest model for robust predictions
- 📈 **Model Evaluation**: Automatic accuracy, precision, recall, and F1-score metrics
- 🎯 **Confidence Scores**: See prediction confidence for each gesture

## Project Structure

```
hand_gesture_recognition/
├── collect_data.py         # Script to record gesture samples from webcam
├── train_model.py          # Script to train the Random Forest classifier
├── run_app.py              # Live gesture recognition from webcam
├── requirements.txt        # Project dependencies
├── .gitignore              # Git ignore file
├── data/                   # Collected gesture CSV data (auto-created)
│   ├── thumbs_up.csv
│   ├── peace.csv
│   ├── open_hand.csv
│   ├── fist.csv
│   └── pointing.csv
├── model.pkl               # Trained model file (auto-created)
├── label_encoder.pkl       # Label encoder (auto-created)
└── README.md               # This file
```

## Installation

### Prerequisites
- Python 3.7 or higher
- Webcam/Camera

### Step 1: Clone the Repository

```bash
git clone https://github.com/akhil-k-dubey/hand_gesture_recognition.git
cd hand_gesture_recognition
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Collect Training Data

Run the data collection script to record samples of your gestures:

```bash
python collect_data.py
```

**Instructions:**
1. Choose a gesture name (or create a custom one)
2. Position your hand in front of the camera
3. Press **SPACE** to capture each sample (collect 20-30 samples per gesture)
4. Press **ESC** to finish collecting that gesture
5. Repeat for multiple gestures

**Recommended Gestures to Start With:**
- `thumbs_up` - Thumbs pointing upward
- `peace` - Two fingers up (V sign)
- `open_hand` - Palm open, all fingers spread
- `fist` - Hand closed in a fist
- `pointing` - Index finger pointing

**Tips for Better Results:**
- Ensure good lighting
- Keep consistent distance from camera (arm's length)
- Vary hand position and rotation slightly for robustness
- Collect at least 20-30 samples per gesture
- Practice consistent hand positions for each gesture

### Step 2: Train the Model

Once you've collected data for your gestures, train the classifier:

```bash
python train_model.py
```

**What it does:**
1. Loads all CSV files from the `data/` directory
2. Combines them into a training dataset
3. Trains a Random Forest classifier
4. Evaluates the model on a test set
5. Displays accuracy, precision, recall, and F1-score
6. Saves the trained model to `model.pkl`

**Expected Output:**
```
Loading training data...
Found 5 gesture(s)
  • thumbs_up: 30 samples
  • peace: 28 samples
  • open_hand: 32 samples
  • fist: 30 samples
  • pointing: 29 samples

Total samples: 149
Feature dimensions: 63

TRAINING MODEL
Gestures: ['fist', 'open_hand', 'peace', 'pointing', 'thumbs_up']
Training set: 119 samples
Test set: 30 samples
Training Random Forest Classifier...

MODEL EVALUATION
Accuracy:  0.9667 (96.67%)
Precision: 0.9667
Recall:    0.9667
F1-Score:  0.9667
```

### Step 3: Run Live Gesture Recognition

Start the real-time gesture recognition application:

```bash
python run_app.py
```

**Controls:**
- **ESC** - Exit the application
- **SPACE** - Take a screenshot (saved as `gesture_screenshot_X.jpg`)

**On Screen:**
- Green landmarks = detected hand points
- Red lines = connections between landmarks
- Gesture name and confidence score displayed at top

## How It Works

### 1. Hand Landmark Detection
- MediaPipe detects 21 key points on your hand:
  - 5 points per finger (fingertip, middle, MCP, PIP, DIP)
  - 4 points on the palm (wrist, etc.)
- Each point has x, y, z coordinates
- Total: 21 landmarks × 3 coordinates = 63 features

### 2. Feature Extraction
The system uses raw normalized coordinates as features. Each gesture is represented as a vector of 63 values.

### 3. Model Training
A Random Forest Classifier learns to distinguish between different gestures based on the landmark patterns. Key parameters:
- **n_estimators**: 100 decision trees
- **max_depth**: 20 levels deep
- **Train/Test Split**: 80/20

### 4. Real-time Prediction
For each video frame:
1. Detect hand landmarks using MediaPipe
2. Extract the 63 features
3. Pass to trained Random Forest model
4. Return gesture label with confidence score

## Troubleshooting

### "No hand detected"
- Ensure your hand is clearly visible in the camera
- Make sure you have good lighting
- Try positioning your hand closer to the camera
- Check that your webcam is working

### Low accuracy
- **Collect more data**: Aim for 30+ samples per gesture
- **Vary hand positions**: Include different angles and distances
- **Improve consistency**: Practice the gesture in the same way each time
- **Check for overlap**: Some gestures might be too similar

### "Model files not found"
- Make sure you've run `train_model.py` before `run_app.py`
- Check that `model.pkl` and `label_encoder.pkl` exist in the current directory

### Webcam not working
- Verify your camera is connected and not being used by another application
- Try checking camera permissions in your OS settings
- Test with a different program to ensure hardware works

## Extension Ideas

- **Add More Gestures**: Collect and train on custom gestures
- **Neural Network Classifier**: Replace Random Forest with CNN
- **Gesture Sequences**: Recognize patterns of consecutive gestures
- **Hand-Tracking Games**: Create interactive games based on gestures
- **Multi-hand Detection**: Recognize gestures from both hands
- **Export Model**: Convert to TensorFlow Lite or ONNX for mobile deployment
- **Web Interface**: Build a Flask/Django web app for browser-based recognition
- **Real-time Feedback**: Add sound or visual effects for gesture recognition

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| opencv-python | 4.8.1.78 | Video capture and image processing |
| mediapipe | 0.10.8 | Hand landmark detection |
| scikit-learn | 1.3.2 | Random Forest classifier |
| numpy | 1.24.3 | Numerical computations |
| pandas | 2.0.3 | Data loading and manipulation |
| joblib | 1.3.2 | Model serialization |

## Performance Notes

- **Inference Speed**: ~30-60 FPS on modern hardware
- **Latency**: <50ms per frame
- **Memory**: ~200-300 MB RAM usage
- **Model Size**: ~1-2 MB

## License

This project is open source and available under the MIT License.

## Resources

- [MediaPipe Hands Documentation](https://github.com/google/mediapipe/blob/master/docs/solutions/hands.md)
- [OpenCV Documentation](https://docs.opencv.org/)
- [scikit-learn Random Forest](https://scikit-learn.org/stable/modules/ensemble.html#random-forests)
- [MediaPipe Solutions](https://solutions.mediapipe.dev/)

## Contributing

Feel free to fork this repository and submit pull requests with improvements!

## Author

**Akhil K Dubey**

---

**Happy Gesture Recognition! 🖐️**
