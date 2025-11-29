# 🚗 Number Plate Detection & MongoDB Automation

This project uses **EasyOCR** and **OpenCV** to automatically detect vehicle number plates from a live camera feed and store the detected text directly into **MongoDB Atlas**.  
It’s designed for real-time automation scenarios like smart parking systems, toll management, and vehicle entry logging.

---

## 🧠 Features

- 📸 Real-time number plate detection using webcam  
- 🔍 Text extraction using **EasyOCR**  
- 💾 Automatic insertion of detected text into **MongoDB Atlas**  
- 🧱 Clean, modular, and maintainable Python project structure  
- ⚡ Easy to extend for smart automation or cloud-based systems  

---

## 📁 Project Structure

```
numberplate_detection/
│
├── main.py                # Entry point: runs camera and performs OCR
├── ocr_module.py          # Contains plate detection & text extraction logic
├── db_module.py           # Handles MongoDB connection and data insertion
├── config.py              # Stores MongoDB credentials and configuration
├── utils.py               # (Optional) Utility functions like text cleaning
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## 🧩 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/numberplate_detection.git
cd numberplate_detection
```

### 2️⃣ Create and Activate Virtual Environment (Recommended)
```bash
python -m venv venv
# Activate it
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure MongoDB Connection
Create a free cluster on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).

Then edit `config.py`:
```python
MONGO_URI = "your_mongodb_atlas_connection_uri_here"
DB_NAME = "numberplates_db"
COLLECTION_NAME = "plates"
```

---

## ⚙️ How It Works

1. **main.py** starts the webcam feed.  
2. Each frame is passed to **ocr_module.py**, where:
   - Number plate region is detected using contours.
   - EasyOCR extracts text from the detected region.
3. Extracted text is inserted into MongoDB using **db_module.py**.  
4. The console logs show both detected plate numbers and inserted document IDs.

---

## ▶️ Running the Project

Run the following command:
```bash
python main.py
```

- Press **‘q’** to exit the video window.  
- Detected number plates will be printed in the console and stored in MongoDB.

---

## 🗃️ Sample MongoDB Document

Example document inserted into your collection:
```json
{
  "_id": "6719ef81aabc1234f1d23f45",
  "plate": "KA01AB1234"
}
```

---

## 💡 Optional Enhancements

- 🚫 **Avoid duplicate entries** for same number plate within a session.  
- 🕒 **Add timestamp & location** fields to MongoDB documents.  
- ☁️ **Integrate with Flask API** to fetch all stored plate records.  
- 🧠 **Train YOLO / OpenCV Haar Cascade** for better plate localization.  
- 📬 **Send detected plate data** to an external dashboard or REST API.

---

## 🧰 Dependencies

| Library | Description |
|----------|-------------|
| `opencv-python` | For webcam access and image processing |
| `imutils` | Simplifies OpenCV contour operations |
| `easyocr` | Extracts text from images |
| `pymongo` | Connects and inserts data into MongoDB Atlas |

Install all via:
```bash
pip install -r requirements.txt
```

---

## 🧑‍💻 Author

**Suhas Sabambargi**  
💼 Role: Developer & Designer  
📧 Email: *[your email here]*  
🌐 GitHub: [your-username](https://github.com/your-username)

---

## 📜 License

This project is licensed under the MIT License — you can freely use, modify, and distribute it.
