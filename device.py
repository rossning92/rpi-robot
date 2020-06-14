from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import DigitalOutputDevice, PWMOutputDevice
import time

Device.pin_factory = PiGPIOFactory()


class Motor:
    """
    The class takes three pin numbers as the input to control one of the motor connected to TB6612FNG module.
    """

    def __init__(self, in1, in2, pwm):
        self.in1 = DigitalOutputDevice(in1)
        self.in1.off()

        self.in2 = DigitalOutputDevice(in2)
        self.in2.on()

        self.pwm = PWMOutputDevice(pwm, frequency=1000)

    def set_throttle(self, val):
        """Control the orientation and the speed of the motor.
        Arguments:
            val: a number between -1.0 and 1.0. The motor rotates in forward direction if val > 1, otherwise in reverse direction.
            Setting val to None will set the motor to stop mode.
        """

        # Set the motor to stop mode.
        if val is None:
            self.in1.off()
            self.in2.off()
            self.pwm.value = 1.0

        else:
            # Determine the orientation of the motor.
            if val > 0.0:
                self.in1.off()
                self.in2.on()
            else:
                self.in1.on()
                self.in2.off()

            # Clamp the pwm signal (throttle) to [0, 1].
            pwm = max(0.0, min(abs(val), 1.0))

            # Note that setting PWM to low will brake the motor no matter what
            # in1 and in2 input is.
            self.pwm.value = pwm
