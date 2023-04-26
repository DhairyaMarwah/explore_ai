import cv2
import numpy as np
from keras.models import load_model

# Load pre-trained facial expression recognition model
model = load_model('model.h5')

# Define emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Initialize camera capture
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces using Haar Cascade classifier
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # Loop over all detected faces
    for (x,y,w,h) in faces:
        # Extract face region of interest (ROI)
        roi_gray = gray[y:y+h, x:x+w]

        # Resize ROI to match input size of the model
        roi_gray = cv2.resize(roi_gray, (64, 64))

        # Normalize pixel values to be in range [0, 1]
        roi_gray = roi_gray / 255.0

        # Reshape ROI to match input shape of the model
        roi_gray = np.reshape(roi_gray, (1, 64, 64, 1)) 

        # Make prediction using the model
        predictions = model.predict(roi_gray)

        # Get the emotion label with highest predicted probability
        emotion_label = emotion_labels[np.argmax(predictions)]

        # Draw a rectangle around the detected face and label with predicted emotion
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, emotion_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera capture and close all windows
cap.release()
cv2.destroyAllWindows()
