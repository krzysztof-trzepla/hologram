#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, Response
from video_camera import VideoCamera

app = Flask(__name__)
video_camera = VideoCamera(400)


@app.route('/')
def index():
    return render_template('index.html')


def stream():
    while True:
        frame = video_camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: video/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
