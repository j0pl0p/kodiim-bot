from flask import Flask, send_file, Response
import cv2 as cv

app = Flask(__name__)
cam = cv.VideoCapture(0)


def get_frame():
    _, frame = cam.read()
    scale_percent = 40  # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    frame = cv.resize(frame, dim, interpolation=cv.INTER_AREA)
    _, frame = cv.imencode('.JPEG', frame)
    return frame

def gen():
    while True:
        frame = get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame.tostring() + b'\r\n')


@app.route('/stream')
def stream():
    return Response(gen(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
@app.route("/image")
def image():
    frame = get_frame()
    content = frame.tostring()
    return Response(content, mimetype='image/jpg')


app.run(host="localhost", port=8080)