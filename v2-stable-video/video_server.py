from flask import Flask, request,jsonify
from flask_cors import CORS
import os
import subprocess
import mimetypes
import cv2
import numpy as np
from keras.models import load_model

model = load_model('./models/model.h5')
app = Flask(__name__)
CORS(app)
@app.route("/")
def hello():
	return "Hello Geeks!! from Google Colab"

@app.route('/upload', methods=['POST'])
def upload():
    video_file = request.files.get('video')
    if video_file:
        video_filename = video_file.filename
        video_save_path = os.path.join('uploads', video_filename)
        video_file.save(video_save_path) 
        audio_save_path = os.path.join('uploads', os.path.splitext(video_filename)[0] + '.mp3')
        subprocess.call(['ffmpeg', '-i', video_save_path, '-vn', '-acodec', 'libmp3lame', audio_save_path])
        emotion( video_file)
     
def emotion(video_file):
    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    face_cascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')
    
    # Create an empty list to store detected emotions
    detected_emotions = []

    # Open the video file
    cap = cv2.VideoCapture(video_file)

    while True:
        # Read frames from the video
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # For each face, detect the emotion and save it in the detected_emotions list
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (64, 64))
            roi_gray = roi_gray / 255.0
            roi_gray = np.reshape(roi_gray, (1, 64, 64, 1))
            predictions = model.predict(roi_gray)
            emotion_label = emotion_labels[np.argmax(predictions)]
            detected_emotions.append(emotion_label)

            # Draw a rectangle around the face and display the detected emotion label
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, emotion_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and destroy all windows
    cap.release()
    cv2.destroyAllWindows()

    # Find the emotion with the highest frequency
    if len(detected_emotions) > 0:
        most_frequent_emotion = max(set(detected_emotions), key=detected_emotions.count)
        print('The most frequent emotion detected in the video is:', most_frequent_emotion)
        return jsonify(most_frequent_emotion)
    else:
        print('No faces detected in the video.')
        return jsonify('No faces detected in the video.')
if __name__ == "__main__":
    app.run(debug=True)
