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
        print("reached",video_file) 
        return emotion(video_save_path)
     
def emotion(video_save_path):
    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    face_cascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml') 
    detected_emotions = [] 
    cap =cv2.VideoCapture(video_save_path) 
    while True: 
        ret, frame = cap.read()
        if not ret:
            break 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (64, 64))
            roi_gray = roi_gray / 255.0
            roi_gray = np.reshape(roi_gray, (1, 64, 64, 1))
            predictions = model.predict(roi_gray)
            emotion_label = emotion_labels[np.argmax(predictions)]
            detected_emotions.append(emotion_label) 
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, emotion_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2) 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 
    cap.release()
    cv2.destroyAllWindows() 
    if len(detected_emotions) > 0:
        most_frequent_emotion = max(set(detected_emotions), key=detected_emotions.count) 
        return jsonify({'emotions': most_frequent_emotion})
    else: 
        return jsonify({'emotions': "No faces detected in the video."})

if __name__ == "__main__":
    app.run(debug=True)
