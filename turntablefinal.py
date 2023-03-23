from gpiozero import LED
import time

class StepperMotor:

    def __init__(self, A1, A2, B1, B2):
        self.PIN_A1 = LED( A1 )
        self.PIN_A2 = LED( A2 )
        self.PIN_B1 = LED( B1 )
        self.PIN_B2 = LED( B2 )


    def forward(self, delay, steps):
        for i in range(steps):
            self.setStep(1, 0, 1, 0)
            time.sleep(delay)
            self.setStep(0, 1, 1, 0)
            time.sleep(delay)
            self.setStep(0, 1, 0, 1)
            time.sleep(delay)
            self.setStep(1, 0, 0, 1)
            time.sleep(delay)

    def backward(self, delay, steps):
        for i in range(steps):
            self.setStep(1, 0, 0, 1)
            time.sleep(delay)
            self.setStep(0, 1, 0, 1)
            time.sleep(delay)
            self.setStep(0, 1, 1, 0)
            time.sleep(delay)
            self.setStep(1, 0, 1, 0)
            time.sleep(delay)

    def setStep(self, w1, w2, w3, w4):
        self.PIN_A1.value = w1
        self.PIN_A2.value = w2
        self.PIN_B1.value = w3
        self.PIN_B2.value = w4

if __name__=='__main__':

    motor1 = StepperMotor(22, 27, 17, 18)

    while True:
        motor1.forward( 5.0/1000, 128 )
        time.sleep(2)