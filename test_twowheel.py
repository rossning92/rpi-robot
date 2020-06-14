from device import Motor
from time import sleep
from twowheel import TwoWheelController


def test_controller(controller):
    for _ in range(2):
        controller.set_axis(x=-0.3)
        sleep(0.25)

        controller.set_axis(x=0.3)
        sleep(0.25)

        controller.set_axis()


if __name__ == "__main__":
    controller = TwoWheelController()
    test_controller(controller)
