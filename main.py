from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
from datetime import datetime

app = Flask(__name__)
faceList = []
nowList = []
video_camera = None
global_frame = None
# install opencv locally and set the right path
face_cascade = cv2.CascadeClassifier(
    "/usr/local/Cellar/opencv/4.0.1/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")

if __name__ == '__main__':
    app.run(host='127.0.0.1', threaded=True)

def video_stream():
    global video_camera
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()

    while True:
        frame = video_camera.get_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')


class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        global faceList
        ref, fra = self.cap.read()
        while ref:
            gray = cv2.cvtColor(fra, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            _, jpeg = cv2.imencode(".jpg", fra)
            for(x, y, w, h) in faces:
                # roi = fra[y: y+h, x: x+w]
                # hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                # mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
                # roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0,180])
                # cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
                now = datetime.now()
                cv2.rectangle(fra, (x, y), (x+w, y+h), (255, 255, 255), 2)
                cv2.putText(fra, "Face", (x, y-10), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), thickness=2)
                _, jpeg = cv2.imencode(".jpg", fra)
                _, catchFace = cv2.imencode(".jpg", fra[y:y+h, x:x+w])
                faceList.append(catchFace.tobytes())
                nowList.append(now.strftime("%Y-%m-%d %H:%M:%S"))
            return jpeg.tobytes()
        else:
            return None

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route('/video')
def video():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/photo")
def photo():
    return jsonify(tuple(map(tuple, faceList)))

@app.route("/photo/date")
def date():
    return jsonify(tuple(map(tuple, nowList)))