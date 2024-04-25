from flask import Flask, render_template, Response
import cv2
import os

app = Flask(__name__)

if not os.path.exists('templates'):
  os.makedirs('templates')

camera_indexes = [0]

camera = None
for index in camera_indexes:
  cap = cv2.VideoCapture(index)
  if cap.isOpened():
    camera = cap
    break
  cap.release()


def gen_frames():
  global camera
  while True:
    success, frame = camera.read()
    if not success:
      break
    else:
      ret, buffer = cv2.imencode('.jpg', frame)
      frame = buffer.tobytes()
      yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
  global camera
  if camera is not None:
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
  else:
    return "Camera is not available", 503


@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  app.run(debug=True)
