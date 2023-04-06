import sys
import time

from fhict_cb_01.CustomPymata4 import CustomPymata4

ORDER_PLACED = 0
PIZZA_IN_OVEN = 1
PIZZA_IS_DONE = 2
OVEN_IS_OFF = 3

LED_PINS = [4, 5, 6, 7]
BUTTON1PIN = 8


def setup():
    global board
    board = CustomPymata4(com_port="COM3")
    for pin in LED_PINS:
        board.set_pin_mode_digital_output(pin)
    board.set_pin_mode_digital_input_pullup(BUTTON1PIN)
    board.displayOn()


def start_timer():
    start_timer = time.time()
    while time.time() - start_timer < 10:
        remaining_time = int(10 - (time.time() - start_timer))
        board.displayShow(remaining_time)
        board.digital_pin_write(LED_PINS[3], 1)
        time.sleep(0.1)

        level, time_stamp = board.digital_read(BUTTON1PIN)
        if level == 0:
            board.digital_pin_write(LED_PINS[3], 0)
            return

    board.digital_pin_write(LED_PINS[3], 0)
    board.displayShow(0)


def cook_pizza():
    board.digital_pin_write(LED_PINS[1], 1)

    while True:
        level, time_stamp = board.digital_read(BUTTON1PIN)
        if level == 0:
            break
        time.sleep(0.1)

    board.digital_pin_write(LED_PINS[1], 0)

    start_timer()

setup()
while True:
    try:
        cook_pizza()
    except KeyboardInterrupt:
        print('shutdown')
        board.shutdown()
        sys.exit(0)
