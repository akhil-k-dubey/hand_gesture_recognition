"""
Real-time Hand Gesture Recognition App
Uses trained model to predict gestures from webcam feed.
"""

import cv2
import mediapipe as mp
import numpy as np
import joblib
import os

# Initialize MediaPipe Hand Detector
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

MODEL_FILE = "model.pkl"
LABEL_ENCODER_FILE = "label_encoder.pkl"

def load_model():
    """Load trained model and label encoder"""
    if not os.path.exists(MODEL_FILE) or not os.path.exists(LABEL_ENCODER_FILE):
        raise FileNotFoundError(
            f"Model files not found!\n"
            f"Please run 'python train_model.py' first to train the model."
        )
    
    model = joblib.load(MODEL_FILE)
    label_encoder = joblib.load(LABEL_ENCODER_FILE)
    
    return model, label_encoder

def predict_gesture(hand_landmarks, model, label_encoder):
    """
    Predict gesture from hand landmarks
    
    Args:
        hand_landmarks: MediaPipe hand landmarks
        model: Trained classifier
        label_encoder: Label encoder for gesture names
    
    Returns:
        gesture_name: Predicted gesture
        confidence: Prediction confidence
    """
    # Extract and flatten landmarks
    landmarks_list = []
    for landmark in hand_landmarks.landmark:
        landmarks_list.extend([landmark.x, landmark.y, landmark.z])
    
    # Predict
    landmarks_array = np.array(landmarks_list, dtype=np.float32).reshape(1, -1)
    prediction = model.predict(landmarks_array)[0]
    confidence = model.predict_proba(landmarks_array)[0]
    
    gesture_name = label_encoder.inverse_transform([prediction])[0]
    confidence_score = np.max(confidence)
    
    return gesture_name, confidence_score

def draw_gesture_info(frame, gesture_name, confidence, position=(10, 30)):
    """Draw gesture info on frame"""
    text = f"Gesture: {gesture_name.upper()}"
    confidence_text = f"Confidence: {confidence*100:.1f}%"
    
    # Background box for better visibility
    cv2.rectangle(frame, (position[0]-5, position[1]-25), 
                  (position[0]+400, position[1]+35), (0, 0, 0), -1)
    
    cv2.putText(frame, text, position, 
               cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
    cv2.putText(frame, confidence_text, (position[0], position[1]+35), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

def draw_instructions(frame):
    """Draw instructions on frame"""
    instructions = [
        "ESC - Exit",
        "SPACE - Take screenshot",
    ]
    
    y = frame.shape[0] - 60
    for instruction in instructions:
        cv2.putText(frame, instruction, (10, y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        y += 25

def run_gesture_recognition():
    """Main gesture recognition loop"""
    try:
        print("Loading model...")
        model, label_encoder = load_model()
        print("✓ Model loaded successfully!")
        print(f"Trained gestures: {list(label_encoder.classes_)}")
        print("\nStarting gesture recognition...")
        print("Press ESC to exit | SPACE to take screenshot")
        print("="*50 + "\n")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    cap = cv2.VideoCapture(0)
    screenshot_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        
        # Flip for selfie view
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        # Process hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                )
                
                # Predict gesture
                gesture_name, confidence = predict_gesture(
                    hand_landmarks, model, label_encoder
                )
                
                # Only display if confidence is reasonable
                if confidence > 0.5:
                    draw_gesture_info(frame, gesture_name, confidence)
                else:
                    cv2.putText(frame, "Low confidence - more samples needed", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "No hand detected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Draw instructions
        draw_instructions(frame)
        
        # Display frame
        cv2.imshow("Hand Gesture Recognition", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        # ESC to exit
        if key == 27:
            break
        
        # SPACE to take screenshot
        elif key == 32:
            screenshot_count += 1
            filename = f"gesture_screenshot_{screenshot_count}.jpg"
            cv2.imwrite(filename, frame)
            print(f"✓ Screenshot saved: {filename}")
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n✓ Gesture recognition closed.")

if __name__ == "__main__":
    run_gesture_recognition()
