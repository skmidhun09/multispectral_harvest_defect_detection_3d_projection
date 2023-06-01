from flask import Flask,Response
import cv2
import jsonpickle


app = Flask(__name__)

@app.route("/arm/<angle>/shift")
def shift_arm_pos(angle):
    return "Robotic arm position shifted" + angle

@app.route("/image/get")
def image_response():
    img = cv2.imread('input/6.jpg')
    _, frame = cv2.imencode('.jpg', img)
    response_pickled = jsonpickle.encode(frame)
    return Response(response=response_pickled, status=200, mimetype="application/json")


app.run()
