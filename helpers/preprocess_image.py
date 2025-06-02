import cv2
import pytesseract
import re

def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def extract_speed_and_unit_from_frame(frame):
    roi = frame #potentially add auto cropping
    pre = preprocess_image(roi)
    text = pytesseract.image_to_string(pre, config='--psm 7')
    match = re.search(r'(\d+(?:\.\d+)?)(\s*[a-zA-Z]+)?', text)
    if match:
        speed = float(match.group(1))
        unit = match.group(2).strip() if match.group(2) else None
        return [speed], unit
    return [None], None