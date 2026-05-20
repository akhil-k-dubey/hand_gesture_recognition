"""
Hand Gesture Model Training Script
Trains a Random Forest classifier on collected gesture data.
"""

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import warnings

warnings.filterwarnings('ignore')

DATA_DIR = "data"
MODEL_FILE = "model.pkl"
LABEL_ENCODER_FILE = "label_encoder.pkl"

def load_training_data():
    """
    Load and combine all gesture data from CSV files
    
    Returns:
        X: Features (landmarks)
        y: Labels (gesture names)
    """
    X = []
    y = []
    
    # Find all CSV files in data directory
    csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in '{DATA_DIR}' directory. Please collect data first using collect_data.py")
    
    print("Loading training data...")
    print(f"Found {len(csv_files)} gesture(s)")
    
    for csv_file in csv_files:
        gesture_name = csv_file.replace('.csv', '')
        file_path = os.path.join(DATA_DIR, csv_file)
        
        try:
            df = pd.read_csv(file_path)
            print(f"  • {gesture_name}: {len(df)} samples")
            
            # Extract features (all columns except label)
            features = df.values
            
            # Add to training data
            X.extend(features)
            y.extend([gesture_name] * len(features))
        
        except Exception as e:
            print(f"  ✗ Error loading {csv_file}: {e}")
    
    if not X:
        raise ValueError("No training data could be loaded.")
    
    X = np.array(X, dtype=np.float32)
    y = np.array(y)
    
    print(f"\nTotal samples: {len(X)}")
    print(f"Feature dimensions: {X.shape[1]}")
    
    return X, y

def train_model(X, y):
    """
    Train Random Forest classifier
    
    Args:
        X: Features
        y: Labels
    
    Returns:
        model: Trained RandomForestClassifier
        label_encoder: Trained LabelEncoder
    """
    print("\n" + "="*50)
    print("TRAINING MODEL")
    print("="*50)
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    print(f"Gestures: {list(label_encoder.classes_)}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    print(f"Training set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Train Random Forest
    print("\nTraining Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    print("\n" + "="*50)
    print("MODEL EVALUATION")
    print("="*50)
    
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\nConfusion Matrix:")
    print(cm)
    
    return model, label_encoder

def save_model(model, label_encoder):
    """Save trained model and label encoder"""
    joblib.dump(model, MODEL_FILE)
    joblib.dump(label_encoder, LABEL_ENCODER_FILE)
    
    print("\n" + "="*50)
    print("✓ Model saved successfully!")
    print(f"  Model file: {MODEL_FILE}")
    print(f"  Label encoder: {LABEL_ENCODER_FILE}")
    print("="*50)

def main():
    """Main training function"""
    try:
        # Load data
        X, y = load_training_data()
        
        # Train model
        model, label_encoder = train_model(X, y)
        
        # Save model
        save_model(model, label_encoder)
        
        print("\nYou can now run 'python run_app.py' to use the trained model!")
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure you have collected training data first!")

if __name__ == "__main__":
    main()
