import cv2
import imutils
import requests
import re
from ocr_module import detect_plate
from db_module import insert_plate

# 🔵 Your backend URL
API_BASE = "https://nena-unhaggling-pierce.ngrok-free.dev"

# To avoid repeat triggers
last_detected_plate = None

# ==========================
# VALIDATION FOR REAL PLATES
# ==========================

def is_valid_plate(plate):
    """
    Validates Indian vehicle number plates.
    Example valid: UP70GT1215, KA03AB1234
    """
    pattern = r"^[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}$"
    return re.match(pattern, plate) is not None


# ==========================
# VIDEO CAPTURE LOOP
# ==========================

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=800)

    # Run your detection
    plate_text, frame = detect_plate(frame)

    if plate_text:
        print(f"Detected Number Plate (raw): {plate_text}")

        # Clean the text
        plate_text = plate_text.replace(" ", "").upper()

        # 1️⃣ CHECK VALID FORMAT BEFORE TRIGGER
        if not is_valid_plate(plate_text):
            print(f"❌ Ignored: Not a valid number plate → {plate_text}")
            cv2.imshow("Number Plate Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        print(f"✅ Valid Number Plate: {plate_text}")

        # 2️⃣ Avoid duplicate triggers
        if plate_text != last_detected_plate:
            last_detected_plate = plate_text

            # Save detected plate to DB
            try:
                inserted_id = insert_plate(plate_text)
                print(f"Inserted into DB: {inserted_id}")
            except Exception as e:
                print("DB Error:", e)

            # 3️⃣ TRIGGER FASTAPI
            print("\n🚀 Triggering FastAPI /start_trip...\n")

            try:
                response = requests.post(
                    f"{API_BASE}/start_trip",
                    json={"vehicle_id": plate_text}
                )
                print("Start Trip Response:", response.json())
            except Exception as e:
                print("Backend Error:", e)

    # Show video frame
    cv2.imshow("Number Plate Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
