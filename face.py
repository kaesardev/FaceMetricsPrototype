from datetime import datetime
import cv2

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def multi_face_detect(frame):
    # Detect the faces
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))

    result = []
    # Draw the rectangle around each face
    for (x0, y0, w, h) in faces:
        x1, y1 = x0 + w, y0 + h
        # Draw detection rectangle
        frame = cv2.rectangle(frame, (x0,y0), (x1, y1), (0,0,255), 2)
        # Analyze face figure
        crop_img = frame[y0:y1, x0:x1] # Crop from x, y, w, h
        result.append((crop_img, x0, y0, x1, y1))
    return result