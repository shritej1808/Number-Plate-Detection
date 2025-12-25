---

# 🚘 Number Plate Detection System (OCR-Driven Trip Trigger)

This repository contains a **real-time Number Plate Detection (OCR) system** built using **OpenCV and Python**, designed to work alongside a **GPS tracking backend** and an **Android application**.

The system detects vehicle number plates using a live camera feed and **automatically triggers trip creation** in the backend **only when the detected plate matches the vehicle logged into the Android app**.

---

## 🧠 System Purpose

✔ Detect vehicle number plates via camera
✔ Validate Indian number plate format
✔ Match OCR result with Android login state
✔ Trigger backend `/start_trip` automatically
✔ Prevent duplicate or unauthorized triggers

This ensures **secure, automated, and tamper-proof trip initiation**.

---

## 🏗️ How It Fits in the System

```
Camera Feed
   ↓
OCR Detection (OpenCV)
   ↓
Plate Validation
   ↓
Android Login Check
   ↓
Backend /start_trip API
```

The OCR system **never blindly starts trips** — it coordinates with backend session state and Android login to avoid misuse.

---

## 🚀 Features

### 👁️ Real-Time Plate Detection

* Uses OpenCV to read frames from live camera
* Frame resizing for improved OCR accuracy
* Continuous detection loop

### 🔍 Plate Validation

* Regex-based validation for Indian number plates
  Format:

  ```
  KA01AB1234
  ```

### 🔐 Secure Matching Logic

* OCR plate must match:

  * Android logged-in vehicle
  * Backend session state
* Duplicate detections are ignored

### 🔄 Backend Coordination

* Polls backend to:

  * Check Android login state
  * Check if trip is already active
* Calls `/start_trip` only when required

### 🗄️ Database Logging

* Stores detected plates via `db_module`
* Useful for audit and debugging

---

## 🧰 Tech Stack

| Layer                 | Technology              |
| --------------------- | ----------------------- |
| Language              | **Python**              |
| Computer Vision       | **OpenCV**              |
| OCR                   | Custom OCR module       |
| Backend Communication | **REST APIs (FastAPI)** |
| Image Utils           | imutils                 |
| Regex Validation      | re                      |
| Camera                | Webcam / USB Camera     |

---

## 📁 Project Structure

```
NUMBER-PLATE-DETECTION/
├── major_project-master/
│   ├── main.py              # OCR execution loop
│   ├── ocr_module.py        # Plate detection logic
│   ├── db_module.py         # Plate logging
│   ├── config.py            # Configuration
│   ├── requirements.txt
│   ├── venv/
│   └── __pycache__/
│
├── playground-1.mongodb.js  # MongoDB playground script
├── README.md
└── .gitignore
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd NUMBER-PLATE-DETECTION/major_project-master
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔧 Configuration

Inside `main.py`:

```python
API_BASE = "https://<your-backend-url>"
POLL_INTERVAL = 1.5
HTTP_TIMEOUT = 5.0
```

Ensure:

* Backend server is running
* Android app is logged in
* Camera is connected and accessible

---

## ▶️ Running the OCR System

```bash
python main.py
```

Output:

* Live camera feed window
* Console logs showing:

  * Detected plates
  * Login state
  * Backend responses

Press **`q`** to quit.

---

## 🧪 Detection Logic Summary

1. Read camera frame
2. Detect plate text via OCR
3. Normalize & validate plate
4. Check Android logged-in vehicle
5. Ignore duplicates
6. Call `/start_trip` if allowed
7. Log detection in DB

---

## 🔒 Safety & Validation

✔ Prevents duplicate trip triggers
✔ Rejects invalid plate formats
✔ Rejects mismatched vehicle detections
✔ Respects backend session state

This makes the system **robust against false positives**.

---

## 🔮 Future Enhancements

* Deep learning–based plate recognition (YOLO + CRNN)
* Multiple camera support
* Night-time detection improvements
* Confidence score thresholding
* Edge deployment (Jetson / Raspberry Pi)

---

## 🎯 Why This Module Matters

This OCR system transforms GPS tracking from **manual to automatic**.
It demonstrates:

* Computer vision
* API coordination
* Real-time system design
* Secure automation


---

Just say **“next”** 😄
