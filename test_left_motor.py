from device import Motor
from time import sleep

if __name__ == "__main__":
    motor = Motor(22, 23, 19)
    for val in [-1, -0.5, 0, 0.5, 1]:
        motor.set_throttle(val)
        sleep(1)

    # Set motor to stop mode.
    motor.set_throttle(None)
