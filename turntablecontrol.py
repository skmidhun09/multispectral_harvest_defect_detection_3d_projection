import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

#define GPIO pins
GPIO_pins = (14, 15, 18) # Microstep Resolution MS1-MS3 -> GPIO Pin
direction= 20       # Direction -> GPIO Pin
step = 21      # Step -> GPIO Pin

# Declare an named instance of class pass GPIO pins numbers
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")

def test():
    steps = 0 # total steps =200 that is 360 degrees
    while steps < 200:
        mymotortest.motor_go(True, "Full", steps, .05, False, .05)
        print("Rotating Clockwise")
        steps = steps + 90
        # click picture
