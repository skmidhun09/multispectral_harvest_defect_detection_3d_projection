from flask import Flask

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


app.run()
