from flask import Flask,Response
import cv2
import jsonpickle


app = Flask(__name__)


@app.route("/base/rotate")
def rotate_turn_table():
    return "rotated 90"


@app.route("/capture/tir")
def tir_image_capture():
    return "TIR image captured"


@app.route("/capture/rgb")
def rgb_image_capture():
    return "RGB image captured"


@app.route("/arm/shift")
def shift_arm_pos():
    return "Robotic arm position shifted"

@app.route("/image/get")
def image_response():
    img = cv2.imread('input/6.jpg')
    _, frame = cv2.imencode('.jpg', img)
    response_pickled = jsonpickle.encode(frame)
    return Response(response=response_pickled, status=200, mimetype="application/json")


app.run()
