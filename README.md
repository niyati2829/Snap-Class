# SnapClass — AI-Powered Smart Attendance System

An automated classroom attendance system using computer vision (facial recognition) and speech processing (voice biometrics). Built with Streamlit, Supabase, dlib, and Resemblyzer.

---

## 🌟 Key Features

- **Dual-Portal Interface**: Seamless navigation for Teachers and Students with clean, modern branding.
- **AI Face Recognition**: High-precision 128-dimensional facial landmark extraction with dlib and SVC/nearest-centroid classification.
- **AI Voice Recognition**: Voice embedding extraction and speaker diarization via Resemblyzer and Librosa for audio-based roll calls.
- **Course & Section Management**: Teachers can create courses, generate QR codes, and share quick enrollment links.
- **Instant Enrollment**: Students can self-enroll via QR code scan or deep links (`/?join-code=<CODE>`).
- **Interactive Review & Audit**: Review attendance results before confirming and committing them to the database.
- **Analytics & History**: Track attendance percentage, total classes, and student attendance logs.

---

## 🛠️ Architecture & Tech Stack

- **Frontend & App Framework**: [Streamlit](https://streamlit.io/)
- **Database & Cloud Storage**: [Supabase](https://supabase.com/) (PostgreSQL)
- **Computer Vision**: [dlib](http://dlib.net/), [face_recognition_models](https://github.com/ageitgey/face_recognition_models), [Pillow](https://python-pillow.org/)
- **Audio & Speech Processing**: [Resemblyzer](https://github.com/resemble-ai/Resemblyzer), [Librosa](https://librosa.org/), [webrtcvad](https://github.com/wiseman/py-webrtcvad)
- **Machine Learning**: [scikit-learn](https://scikit-learn.org/) (Linear Support Vector Classifier)
- **Security**: [bcrypt](https://pypi.org/project/bcrypt/) (Salted password hashing)
- **Utilities**: [Segno](https://segno.readthedocs.io/) (QR Code Generation), [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 - 3.14
- macOS / Linux / Windows
- CMake (required for building dlib if not using prebuilt wheels)

### 2. Environment Setup
```bash
# Clone or navigate to the project directory
cd "Attendence project "

# Activate the virtual environment
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Supabase Credentials
Create `.streamlit/secrets.toml` in your project root with your Supabase credentials:
```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-or-service-key"
```

### 5. Run the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Testing

Run the automated test suite:
```bash
python3 tests/test_all.py
python3 tests/test_e2e_simulation.py
```

---

## 📁 Project Structure

```
├── app.py                      # Main application entry point & router
├── assets/                     # Custom illustrations and logos
│   ├── logo_url.png            # Application logo
│   ├── student_illustration.png# Student portal banner
│   └── teacher_illustration.png# Teacher portal banner
├── requirements.txt            # Python dependencies
├── src/
│   ├── database/
│   │   ├── config.py           # Supabase client configuration
│   │   └── db.py               # Database queries, auth, & operations
│   ├── pipelines/
│   │   ├── face_pipeline.py    # dlib facial recognition & classification
│   │   └── voice_pipeline.py   # Resemblyzer voice embedding & matching
│   ├── screens/
│   │   ├── home_screen.py      # Role selection landing screen
│   │   ├── teacher_screen.py   # Teacher login, registration & dashboard
│   │   ├── student_screen.py   # Student FaceID login & dashboard
│   │   ├── components/         # Modals, cards, headers, footers
│   │   └── ui/
│   │       └── base_layout.py  # UI design tokens and typography styling
└── tests/                      # Automated unit and integration tests
```
