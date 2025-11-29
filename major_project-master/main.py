import cv2
import imutils
import requests
from ocr_module import detect_plate
from db_module import insert_plate

API_BASE = "http://YOUR_IP:8000"   # Your FastAPI backend IP
VEHICLE_ID = "UP70GT1215"                 # Or map based on plate

last_detected_plate = None

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=800)

    plate_text, frame = detect_plate(frame)

    if plate_text:
        print(f"Detected Number Plate: {plate_text}")

        if plate_text != last_detected_plate:
            last_detected_plate = plate_text

            # ➤ INSERT INTO MONGODB
            try:
                inserted_id = insert_plate(plate_text)
                print(f"Inserted into DB: {inserted_id}")
            except Exception as e:
                print("DB Error:", e)

            # ➤ START TRIP (NO RESET HERE!)
            print("\n🚀 Triggering GPS distance tracking...\n")

            try:
                r = requests.post(f"{API_BASE}/start_trip", json={
                    "vehicle_id": VEHICLE_ID
                })
                print("Start Trip Response:", r.json())
            except Exception as e:
                print("Error contacting backend:", e)

    cv2.imshow("Number Plate Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
