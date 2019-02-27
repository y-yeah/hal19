from flask import Flask, render_template, Response, request, jsonify
import cv2
import numpy as np
# import webbrowser
# import time
# import pandas
# from datetime import datetime
app = Flask(__name__)
faceList = []

class VideoCamera(object):
    def __init__(self):
        # self.cap = cv2.VideoCapture("./video-1551173995.mp4")
        # self.cap = cv2.VideoCapture("./video-1551173751.mp4")
        self.cap = cv2.VideoCapture(0)
        self.is_record = False
        self.out = None
        self.recordingThread = None

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        global faceList
        ref, fra = self.cap.read()

        # setup initial location of window
        # r,h,c,w = 240,80,540,80
        # r,h,c,w = 400,80,400,80
        # original_window = (c,r,w,h)
        # # set up the ROI for tracking
        # roi = fra[r:r+h, c:c+w]
        # hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        # mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        # roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
        # cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
        # # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        # term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

        while ref:
            # face and eye recognition
            gray = cv2.cvtColor(fra, cv2.COLOR_BGR2GRAY)
            # bodies = body_cascade.detectMultiScale(gray, 1.3, 5)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            # faces = smile_cascade.detectMultiScale(gray, 1.3, 5)
            ret, jpeg = cv2.imencode(".jpg", fra)
            # for(x, y, w, h) in bodies:
            for(x, y, w, h) in faces:

                r,c = y,x 
                original_window = (c,r,w,h)
                # set up the ROI for tracking
                roi = fra[r:r+h, c:c+w]
                hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
                roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
                cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
                # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
                term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

                # motion detection
                hsv = cv2.cvtColor(fra, cv2.COLOR_BGR2HSV)
                dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
                # apply meanshift to get the new location
                ret, original_window = cv2.CamShift(dst, original_window, term_crit)
                # draw it on image
                # pts = cv2.boxPoints(ret)
                # pts = np.int0(pts)
                # cv2.polylines(fra, [pts], True, 255, 2)
                # x, y, w, h = original_window
                cv2.rectangle(fra, (x, y), (x+w, y+h), (255, 255, 255), 2)
                cv2.putText(fra, "Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), thickness=5)
                ret, jpeg = cv2.imencode(".jpg", fra)
                retFace, catchFace = cv2.imencode(".jpg", fra[y:y+h, x:x+w])
                faceList.append(catchFace.tobytes())
                # cv2.rectangle(fra, (x, y), (x+w, y+h), (255, 255, 255), 2)
                # cv2.line(fra, (int(x+w/2), y), (int(x+w/2), y+h), (255, 0, 0), thickness = 10)
                # print("Someone is in front of this PC!!")
                # print(catchFace)
                # preparation for eyes
                # roi_gray = gray[y:y+h, x:x+w]
                # roi_color = fra[y:y+h, x:x+w]
                # eyes = eye_cascade.detectMultiScale(roi_gray)
                # for(ex, ey, ew, eh) in eyes:
                #     cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                #     print("EYES")
                #     ret, jpeg = cv2.imencode(".jpg", fra)
            # # motion detection
            # hsv = cv2.cvtColor(fra, cv2.COLOR_BGR2HSV)
            # dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
            # # apply meanshift to get the new location
            # ret, original_window = cv2.CamShift(dst, original_window, term_crit)
            # # draw it on image
            # pts = cv2.boxPoints(ret)
            # pts = np.int0(pts)
            # cv2.polylines(fra, [pts], True, 255, 2)
            # # x, y, w, h = original_window
            # # cv2.rectangle(fra, (x, y), (x+w, y+h), 255, 2)
            # ret, jpeg = cv2.imencode(".jpg", fra)
            return jpeg.tobytes()
        else:
            return None


video_camera = None
global_frame = None
face_cascade = cv2.CascadeClassifier(
    "/usr/local/Cellar/opencv/4.0.1/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
smile_cascade = cv2.CascadeClassifier(
    "/usr/local/Cellar/opencv/4.0.1/share/opencv4/haarcascades/haarcascade_smile.xml")
body_cascade = cv2.CascadeClassifier(
    "/usr/local/Cellar/opencv/4.0.1/share/opencv4/haarcascades/haarcascade_fullbody.xml")
eye_cascade = cv2.CascadeClassifier(
    "/usr/local/Cellar/opencv/4.0.1/share/opencv4/haarcascades/haarcascade_eye.xml")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/photo")
def photo():
    return jsonify(tuple(map(tuple, faceList)))

# @app.route("/record", methods=["POST"])
# def record_status():
#     global video_camera
#     if video_camera == None:
#         video_camera = VideoCamera()

#     json = request.get_json()

#     status = json['status']

#     if status == "true":
#         video_camera.start_record()
#         return jsonify(result="started")
#     else:
#         video_camera.stop_record()
#         return jsonify(result="stopped")


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


@app.route('/video')
def video():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='127.0.0.1', threaded=True)


# first_frame = None
# status_list = [None, None]
# times = []
# df = pandas.DataFrame(columns=["Start", "End"])

    video = cv2.VideoCapture("./video-1551168945.mp4")
    while True:
        check, frame = video.read()
        # status = 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        # bodies = body_cascade.detectMultiScale(gray, 1.3, 5)
        for(x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
            # roi_gray = gray[y:y+h, x:x+w]
            # roi_color = frame[y:y+h, x:x+w]
            print("Someone is in front of this PC!!")
            # eyes = eye_cascade.detectMultiScale(roi_gray)
            # for(ex, ey, ew, eh) in eyes:
            #     cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
        # for(bx, by, bw, bh) in bodies:
        #     cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), (255, 0, 0), 2)

        # gray = cv2.GaussianBlur(gray, (21, 21), 0)
        # if first_frame is None:
            # first_frame = gray
        #     continue
        # delta_frame = cv2.absdiff(first_frame, gray)
        # retval, thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)
        # thresh_delta = cv2.dilate(thresh_delta, None, iterations=0)
        # (_, cnts, _) = cv2.findContours(
        #     thresh_delta.copy(),
        #     cv2.RETR_EXTERNAL,
        #     cv2.CHAIN_APPROX_SIMPLE,
        # )
        # for contour in cnts:
        #     if cv2.contourArea(contour) < 1000:
        #         continue
        #     status = 1
        #     (x, y, w, h) = cv2.boundingRect(contour)
        #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        # status_list.append(status)
        # status_list = status_list[-2:]
        # if status_list[-1] == 1 and status_list[-2] == 0:
        #     times.append(datetime.now())
        # if status_list[-1] == 0 and status_list[-2] == 1:
        #     times.append(datetime.now())
        # print(status_list)
        # print(times)
        # for i in range(0, len(times), 2):
        #     df = df.append(
        #         {"Start": times[i], "End": times[i+1]}, ignore_index=True)
        # df.to_csv("Times.csv")
        cv2.imshow("frame", frame)
        # cv2.imshow("Capture", gray)
        # cv2.imshow("delta", delta_frame)
        # cv2.imshow("thresh", thresh_delta)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    video.release()
    cv2.destroyAllWindows()
