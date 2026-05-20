"""
Hand Gesture Recognition - Streamlit Web App
Deploy and share your gesture recognition model online!
"""

import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import joblib
import os
from PIL import Image
import tempfile

# Page configuration
st.set_page_config(
    page_title="Hand Gesture Recognition",
    page_icon="🖐️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #0066cc;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .gesture-result {
        background-color: #d4edda;
        border: 2px solid #28a745;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5
)

# Model paths
MODEL_FILE = "model.pkl"
LABEL_ENCODER_FILE = "label_encoder.pkl"

@st.cache_resource
def load_model():
    """Load trained model and label encoder"""
    try:
        model = joblib.load(MODEL_FILE)
        label_encoder = joblib.load(LABEL_ENCODER_FILE)
        return model, label_encoder
    except FileNotFoundError:
        return None, None

def extract_landmarks(image):
    """Extract hand landmarks from image"""
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)
    
    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0]
        landmarks_list = []
        for landmark in landmarks.landmark:
            landmarks_list.extend([landmark.x, landmark.y, landmark.z])
        return np.array(landmarks_list, dtype=np.float32).reshape(1, -1), landmarks
    
    return None, None

def predict_gesture(landmarks_array, model, label_encoder):
    """Predict gesture from landmarks"""
    if landmarks_array is None:
        return None, None
    
    prediction = model.predict(landmarks_array)[0]
    confidence = model.predict_proba(landmarks_array)[0]
    
    gesture_name = label_encoder.inverse_transform([prediction])[0]
    confidence_score = np.max(confidence)
    
    return gesture_name, confidence_score

def draw_landmarks_on_image(image, landmarks):
    """Draw hand landmarks on image"""
    if landmarks is None:
        return image
    
    h, w, c = image.shape
    annotated_image = image.copy()
    
    # Draw landmarks and connections
    for i, landmark in enumerate(landmarks.landmark):
        x = int(landmark.x * w)
        y = int(landmark.y * h)
        cv2.circle(annotated_image, (x, y), 4, (0, 255, 0), -1)
    
    # Draw connections
    connections = [
        (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
        (0, 5), (5, 6), (6, 7), (7, 8),  # Index
        (0, 9), (9, 10), (10, 11), (11, 12),  # Middle
        (0, 13), (13, 14), (14, 15), (15, 16),  # Ring
        (0, 17), (17, 18), (18, 19), (19, 20)   # Pinky
    ]
    
    for start, end in connections:
        if start < len(landmarks.landmark) and end < len(landmarks.landmark):
            start_pos = (
                int(landmarks.landmark[start].x * w),
                int(landmarks.landmark[start].y * h)
            )
            end_pos = (
                int(landmarks.landmark[end].x * w),
                int(landmarks.landmark[end].y * h)
            )
            cv2.line(annotated_image, start_pos, end_pos, (255, 0, 0), 2)
    
    return annotated_image

def main():
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🖐️ Hand Gesture Recognition")
    with col2:
        st.markdown("### v1.0")
    
    st.markdown("---")
    st.write("**Recognize hand gestures in real-time using AI!** Upload an image or use your webcam.")
    
    # Check if model exists
    model, label_encoder = load_model()
    
    if model is None or label_encoder is None:
        st.error("""
        ❌ **Model Not Found!**
        
        The trained model files are missing. 
        
        **To use this app locally:**
        1. Run `python collect_data.py` to collect gesture samples
        2. Run `python train_model.py` to train the model
        3. Then run `streamlit run app.py`
        
        **Available Gestures:** thumbs_up, peace, open_hand, fist, pointing
        """)
        return
    
    st.success(f"✅ Model Loaded! Gestures: {', '.join(label_encoder.classes_)}")
    st.markdown("---")
    
    # Sidebar Navigation
    with st.sidebar:
        st.header("📋 Navigation")
        page = st.radio("Choose an option:", [
            "📸 Image Upload",
            "🎥 Webcam",
            "📊 Model Info",
            "ℹ️ About"
        ])
    
    # PAGE 1: Image Upload
    if page == "📸 Image Upload":
        st.header("📸 Upload Image for Gesture Recognition")
        
        uploaded_file = st.file_uploader(
            "Choose an image with a hand gesture",
            type=["jpg", "jpeg", "png"]
        )
        
        if uploaded_file is not None:
            # Read image
            image = Image.open(uploaded_file)
            image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Create columns for layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Original Image")
                st.image(image, use_column_width=True)
            
            # Extract landmarks
            landmarks_array, landmarks = extract_landmarks(image_np)
            
            if landmarks is not None:
                # Draw landmarks
                annotated_image = draw_landmarks_on_image(image_np, landmarks)
                annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                
                with col2:
                    st.subheader("Hand Landmarks Detected")
                    st.image(annotated_image_rgb, use_column_width=True)
                
                # Predict gesture
                gesture_name, confidence = predict_gesture(landmarks_array, model, label_encoder)
                
                st.markdown("---")
                st.subheader("🎯 Prediction Result")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        "Detected Gesture",
                        gesture_name.upper(),
                        help="The predicted gesture"
                    )
                
                with col2:
                    st.metric(
                        "Confidence",
                        f"{confidence*100:.1f}%",
                        help="How confident the model is"
                    )
                
                # Confidence bar
                st.progress(confidence)
                
                if confidence < 0.5:
                    st.warning(
                        "⚠️ Low confidence! The model is uncertain. "
                        "Try uploading a clearer image or a different angle."
                    )
            else:
                st.error("❌ No hand detected in the image. Please try another image.")
        
        else:
            st.info("👆 Upload an image to get started!")
    
    # PAGE 2: Webcam
    elif page == "🎥 Webcam":
        st.header("🎥 Real-time Webcam Recognition")
        
        st.info("""
        **Note:** Webcam requires camera permissions. 
        If it doesn't work, try uploading images instead.
        """)
        
        # Create a placeholder for video
        picture = st.camera_input("Take a picture")
        
        if picture is not None:
            # Convert to OpenCV format
            img = Image.open(picture)
            img_np = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            landmarks_array, landmarks = extract_landmarks(img_np)
            
            if landmarks is not None:
                # Draw landmarks
                annotated_image = draw_landmarks_on_image(img_np, landmarks)
                annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Captured Image")
                    st.image(img, use_column_width=True)
                
                with col2:
                    st.subheader("With Landmarks")
                    st.image(annotated_image_rgb, use_column_width=True)
                
                # Predict
                gesture_name, confidence = predict_gesture(landmarks_array, model, label_encoder)
                
                st.markdown("---")
                st.subheader("🎯 Prediction")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Gesture", gesture_name.upper())
                with col2:
                    st.metric("Confidence", f"{confidence*100:.1f}%")
                
                st.progress(confidence)
            else:
                st.error("❌ No hand detected. Please ensure your hand is clearly visible.")
    
    # PAGE 3: Model Info
    elif page == "📊 Model Info":
        st.header("📊 Model Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Gestures", len(label_encoder.classes_))
        with col2:
            st.metric("Features", model.n_features_in_)
        with col3:
            st.metric("Trees", model.n_estimators)
        
        st.markdown("---")
        
        st.subheader("Available Gestures")
        for i, gesture in enumerate(label_encoder.classes_, 1):
            st.write(f"{i}. **{gesture.upper()}**")
        
        st.markdown("---")
        
        st.subheader("Model Architecture")
        st.write("""
        - **Algorithm:** Random Forest Classifier
        - **Number of Trees:** 100
        - **Max Depth:** 20
        - **Training Method:** Scikit-learn
        - **Framework:** MediaPipe Hands (Google)
        
        **Hand Landmarks:**
        - 21 key points per hand
        - 3 coordinates per point (x, y, z)
        - Total features: 63
        """)
        
        st.markdown("---")
        
        st.subheader("How It Works")
        st.write("""
        1. **Detection:** MediaPipe detects hand landmarks (21 points)
        2. **Extraction:** Extracts x, y, z coordinates for each point
        3. **Classification:** Random Forest model predicts gesture
        4. **Output:** Shows gesture name with confidence score
        """)
    
    # PAGE 4: About
    elif page == "ℹ️ About":
        st.header("ℹ️ About This Project")
        
        st.markdown("""
        ## 🖐️ Hand Gesture Recognition System
        
        This is an AI-powered application that recognizes hand gestures in real-time using:
        - **MediaPipe Hands** for hand landmark detection
        - **Machine Learning (Random Forest)** for gesture classification
        - **Streamlit** for the web interface
        
        ### Features
        - 📸 Image upload for gesture recognition
        - 🎥 Real-time webcam capture
        - 🎯 High accuracy predictions with confidence scores
        - 📊 Model information and statistics
        
        ### Technologies Used
        - **Python 3.7+**
        - **OpenCV** - Computer Vision
        - **MediaPipe** - Hand Detection
        - **Scikit-learn** - Machine Learning
        - **Streamlit** - Web Framework
        - **NumPy & Pandas** - Data Processing
        
        ### Project Structure
        ```
        hand_gesture_recognition/
        ├── app.py                 # This Streamlit app
        ├── collect_data.py        # Data collection script
        ├── train_model.py         # Model training script
        ├── run_app.py             # Desktop app
        ├── model.pkl              # Trained model
        ├── label_encoder.pkl      # Label encoder
        ├── requirements.txt       # Dependencies
        └── data/                  # Training data
        ```
        
        ### GitHub Repository
        [Hand Gesture Recognition on GitHub](https://github.com/akhil-k-dubey/hand_gesture_recognition)
        
        ### Author
        **Akhil K Dubey**
        
        ### License
        MIT License - Feel free to use and modify!
        
        ---
        
        **Made with ❤️ using Streamlit**
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>🖐️ Hand Gesture Recognition | Powered by Streamlit & MediaPipe</p>
        <p style='color: gray; font-size: 0.8rem;'>
            © 2024 Akhil K Dubey | 
            <a href='https://github.com/akhil-k-dubey/hand_gesture_recognition' target='_blank'>GitHub</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
