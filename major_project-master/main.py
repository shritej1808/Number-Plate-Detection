import cv2
import imutils
import requests
import re
import time
from ocr_module import detect_plate
from db_module import insert_plate

API_BASE = "https://unspruced-marlin-unlively.ngrok-free.dev"
POLL_INTERVAL = 1.5
HTTP_TIMEOUT = 5.0

last_detected_plate = None
last_login_vehicle = None
last_poll = 0


def is_valid_plate(plate: str) -> bool:
    pattern = r"^[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}$"
    return re.match(pattern, plate) is not None


def get_android_login():
    global last_login_vehicle
    try:
        r = requests.get(f"{API_BASE}/get_logged_in_vehicle", timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        vid = r.json().get("vehicle_id")
        print(f"📲 Android logged-in vehicle: {vid}")
        last_login_vehicle = vid
        return vid
    except Exception as e:
        print("⚠ Could not poll login state:", repr(e))
        return last_login_vehicle


def get_session_state():
    try:
        r = requests.get(f"{API_BASE}/session_state", timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        return r.json()
    except:
        return None


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Could not open camera")
    exit()

print("🎥 OCR plate detection started. Press 'q' to quit.\n")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Camera read error")
        break

    frame = imutils.resize(frame, width=900)

    if time.time() - last_poll > POLL_INTERVAL:
        get_android_login()
        last_poll = time.time()

        if last_login_vehicle is None:
            last_detected_plate = None
            print("🔄 Reset OCR — waiting for login.\n")

    if last_login_vehicle is None:
        cv2.imshow("Number Plate Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    plate_text, frame = detect_plate(frame)

    if plate_text:
        plate_text = plate_text.replace(" ", "").upper()
        print(f"🔍 Detected OCR Plate: {plate_text}")

        if not is_valid_plate(plate_text):
            print("❌ Invalid plate ignored\n")
            continue

        if plate_text == last_detected_plate:
            print(f"⏳ Duplicate ignored: {plate_text}\n")
            continue

        if plate_text != last_login_vehicle:
            print(f"🚫 OCR plate {plate_text} does NOT match logged-in vehicle {last_login_vehicle}. Skipped.\n")
            continue

        # MATCHED
        last_detected_plate = plate_text
        print(f"✅ PLATE MATCH! {plate_text}\n")

        session_state = get_session_state()
        if session_state and session_state.get("ocr_detected") and session_state.get("vehicle_id") == plate_text:
            print("ℹ Trip already active — skipping /start_trip.\n")
        else:
            print("🚀 Calling /start_trip ...")
            try:
                resp = requests.post(
                    f"{API_BASE}/start_trip",
                    json={"vehicle_id": plate_text},
                    timeout=HTTP_TIMEOUT
                )
                print("Backend returned:", resp.status_code, resp.text)
            except Exception as e:
                print("❌ Error calling /start_trip:", repr(e))

        try:
            insert_plate(plate_text)
        except Exception as e:
            print("⚠ DB error:", e)

    cv2.imshow("Number Plate Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
