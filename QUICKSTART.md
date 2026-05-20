# 🚀 Quick Start Guide - Local Testing

Get your Hand Gesture Recognition app running locally in 5 minutes!

## ⚡ Quick Setup (Windows)

### Step 1: Open Command Prompt
```bash
cd C:\Users\YourName\Downloads\hand_gesture_recognition
```

### Step 2: Create & Activate Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` at the start of your terminal line.

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

Wait for installation to complete (1-2 minutes).

### Step 4: Collect Gesture Data
```bash
python collect_data.py
```

**What to do:**
1. Type gesture name: `thumbs_up`
2. Position hand in front of camera
3. Press **SPACE** to capture (repeat 20+ times)
4. Press **ESC** when done
5. Repeat for more gestures (peace, fist, open_hand, pointing)

### Step 5: Train the Model
```bash
python train_model.py
```

Wait for training to complete. You should see ~90%+ accuracy!

### Step 6: Launch Streamlit App
```bash
streamlit run app.py
```

Your app will open at **http://localhost:8501** ✨

---

## ⚡ Quick Setup (macOS/Linux)

### Step 1: Open Terminal
```bash
cd ~/hand_gesture_recognition
```

### Step 2: Create & Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4-6: Same as Windows above
```bash
python collect_data.py
python train_model.py
streamlit run app.py
```

---

## 📱 Using the Web App

Once Streamlit is running:

### 📸 Image Upload
1. Click **"📸 Image Upload"** in sidebar
2. Upload or take a photo with your gesture
3. See predictions with confidence score

### 🎥 Webcam
1. Click **"🎥 Webcam"** in sidebar
2. Click "Take picture" button
3. Show your hand gesture
4. Get instant prediction

### 📊 Model Info
View details about your trained model and gestures

### ℹ️ About
Learn more about the project

---

## ✅ Verify Everything Works

**Test Checklist:**

- [ ] Virtual environment activated (see `(venv)` prefix)
- [ ] Dependencies installed without errors
- [ ] Can open camera in `collect_data.py`
- [ ] Can see hand landmarks detected
- [ ] Training completed successfully
- [ ] Streamlit app opens in browser
- [ ] Can upload images and get predictions
- [ ] Webcam works in app

---

## 🔧 If Something Goes Wrong

### "ModuleNotFoundError: No module named 'cv2'"
```bash
pip install opencv-python
```

### "No module named 'mediapipe'"
```bash
pip install mediapipe
```

### "Webcam not working"
- Close other camera apps (Zoom, Teams, etc.)
- Check camera permissions in Windows Settings
- Try a different USB port for external camera

### "Low accuracy"
- Collect more samples (30-50 per gesture)
- Ensure good lighting
- Keep consistent hand position

### "Streamlit won't open"
```bash
# Try specifying the port
streamlit run app.py --server.port 8501
```

---

## 📁 File Structure After Setup

```
hand_gesture_recognition/
├── app.py                          ← Streamlit web app
├── collect_data.py                 ← Data collection
├── train_model.py                  ← Model training
├── run_app.py                      ← Desktop app (alternative)
├── requirements.txt
├── README.md
├── DEPLOYMENT.md
├── .gitignore
├── venv/                           ← Virtual environment
├── data/                           ← Gesture training data
│   ├── thumbs_up.csv
│   ├── peace.csv
│   └── ...
├── model.pkl                       ← Trained model
├── label_encoder.pkl               ← Label encoder
└── .streamlit/
    └── config.toml
```

---

## 🎯 Next Steps

### 1. Test Locally
- Collect diverse gesture samples
- Train model until satisfied
- Test app with different images

### 2. Improve Model
- Collect 50+ samples per gesture
- Try different angles and distances
- Add more gesture types

### 3. Deploy Online
Follow [DEPLOYMENT.md](DEPLOYMENT.md) to:
- Deploy to Streamlit Cloud (FREE)
- Get a shareable URL
- Share with others!

---

## 💡 Tips for Best Results

✅ **Good lighting** - Use natural light or lamp  
✅ **Clear hand** - Avoid shadows and clutter  
✅ **Consistent position** - Keep hand at similar distance  
✅ **Distinct gestures** - Make each gesture visually different  
✅ **More data** - 30-50 samples = better accuracy  
✅ **Test thoroughly** - Try different angles before deploying  

---

## 🚀 Commands Cheat Sheet

```bash
# Activate virtual environment
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux

# Install packages
pip install -r requirements.txt

# Collect gesture data
python collect_data.py

# Train model
python train_model.py

# Run Streamlit app
streamlit run app.py

# Run desktop app (alternative)
python run_app.py

# Deactivate virtual environment
deactivate
```

---

## ❓ Common Questions

**Q: How many gestures can I add?**
A: As many as you want! Each gesture needs a separate CSV file.

**Q: Can I train on GPU?**
A: Scikit-learn doesn't use GPU by default, but the model is fast anyway.

**Q: How much data do I need?**
A: 20-30 samples minimum, 50+ for best accuracy.

**Q: Can I use pre-trained models?**
A: Yes! You could use neural networks, but Random Forest is simpler.

**Q: What if accuracy is low?**
A: Collect more diverse data with different hand positions and lighting.

---

## 📞 Need Help?

1. Check error messages carefully
2. Google the error message
3. Check [DEPLOYMENT.md](DEPLOYMENT.md) for more info
4. Review [README.md](README.md) for full documentation

---

**You're all set! Happy gesture recognizing! 🖐️**

Next up: Deploy to Streamlit Cloud for a shareable link! 🚀
