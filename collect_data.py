"""
Hand Gesture Data Collection Script
Captures hand landmarks from webcam and saves them to CSV for training.
"""

import cv2
import mediapipe as mp
import csv
import os
from datetime import datetime

# Initialize MediaPipe Hand Detector
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Create data directory if it doesn't exist
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_gesture_name():
    """Prompt user for gesture name"""
    print("\n" + "="*50)
    print("Available Gestures:")
    print("1. thumbs_up")
    print("2. peace")
    print("3. open_hand")
    print("4. fist")
    print("5. pointing")
    print("="*50)
    gesture = input("Enter gesture name (or custom): ").strip().lower()
    return gesture

def collect_gesture_data(gesture_name, num_samples=30):
    """
    Collect hand landmark data for a specific gesture
    
    Args:
        gesture_name: Name of the gesture to collect
        num_samples: Number of samples to collect (default: 30)
    """
    csv_file = os.path.join(DATA_DIR, f"{gesture_name}.csv")
    
    # Initialize CSV file with headers if it doesn't exist
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            # 21 landmarks × 3 coordinates (x, y, z) = 63 features
            headers = []
            for i in range(21):
                headers.extend([f'landmark_{i}_x', f'landmark_{i}_y', f'landmark_{i}_z'])
            writer.writerow(headers)
    
    cap = cv2.VideoCapture(0)
    collected = 0
    
    print(f"\nCollecting {num_samples} samples of '{gesture_name}' gesture")
    print("Press 'SPACE' to capture | 'ESC' to exit")
    print("="*50)
    
    while collected < num_samples:
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
        
        # Draw hand landmarks if detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                )
        
        # Display info
        cv2.putText(frame, f"Gesture: {gesture_name}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Collected: {collected}/{num_samples}", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, "SPACE to capture | ESC to exit", (10, 110), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
        
        cv2.imshow("Gesture Data Collection", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        # Space key to capture
        if key == 32:  # Space key
            if results.multi_hand_landmarks:
                # Extract landmarks and flatten them
                landmarks = results.multi_hand_landmarks[0]
                data_row = []
                
                for landmark in landmarks.landmark:
                    data_row.extend([landmark.x, landmark.y, landmark.z])
                
                # Append to CSV
                with open(csv_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(data_row)
                
                collected += 1
                print(f"✓ Captured sample {collected}/{num_samples}")
                
                # Visual feedback
                cv2.putText(frame, "Captured!", (w//2 - 100, h//2), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                cv2.imshow("Gesture Data Collection", frame)
                cv2.waitKey(500)
            else:
                print("✗ No hand detected. Please show your hand.")
        
        # ESC to exit
        elif key == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n✓ Successfully collected {collected} samples for '{gesture_name}'")
    print(f"Data saved to: {csv_file}")

def main():
    """Main function to run data collection"""
    print("\n" + "="*50)
    print("HAND GESTURE DATA COLLECTION")
    print("="*50)
    
    while True:
        gesture = get_gesture_name()
        if gesture:
            try:
                num_samples = int(input("Number of samples to collect (default 30): ") or "30")
                collect_gesture_data(gesture, num_samples)
            except ValueError:
                print("Invalid input. Using default 30 samples.")
                collect_gesture_data(gesture, 30)
        
        cont = input("\nCollect another gesture? (y/n): ").strip().lower()
        if cont != 'y':
            break
    
    print("\n✓ Data collection complete!")

if __name__ == "__main__":
    main()
