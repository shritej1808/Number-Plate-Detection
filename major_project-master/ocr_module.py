import easyocr
import cv2
import imutils

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def detect_plate(frame, draw=True):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

    plate_text = ""
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(c)
            plate_img = frame[y:y+h, x:x+w]
            if draw:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # OCR
            result = reader.readtext(plate_img)
            for (_, text, _) in result:
                plate_text = text
                if draw:
                    cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
            break

    return plate_text, frame
