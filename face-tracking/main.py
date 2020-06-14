from face_detection import detect_first_face
from simple_pid import PID
from urllib import request
import cv2
import numpy as np
import socketio
import time

SERVER_ADDR = "192.168.0.18"

sio = socketio.Client()
sio.connect("http://%s:5000" % SERVER_ADDR)


def read_from_mjpg_stream():
    stream = request.urlopen("http://%s:8080/?action=stream" % SERVER_ADDR)
    bytes = b""
    while True:
        bytes += stream.read(1024)
        a = bytes.find(b"\xff\xd8")
        b = bytes.find(b"\xff\xd9")
        if a != -1 and b != -1:
            jpg = bytes[a : b + 2]
            bytes = bytes[b + 2 :]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

            yield frame

            cv2.imshow("rpi-robot - face tracking", frame)
            if cv2.waitKey(1) == 27:
                exit(0)


if __name__ == "__main__":
    pid = PID(0.5, 0.2, 0.0, setpoint=0)

    # Control loop
    for frame in read_from_mjpg_stream():
        face_center_ndc = detect_first_face(frame)

        in_ = face_center_ndc[0] if (face_center_ndc is not None) else 0.0
        out = pid(in_)
        print("in=%.2f  out=%.2f" % (in_, out))

        # Only rotate the robot without moving forward and backward (y is set to 0).
        sio.emit("set_axis", {"x": -out, "y": 0.0})
