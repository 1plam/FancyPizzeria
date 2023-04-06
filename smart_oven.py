import logging
import time

from fhict_cb_01.CustomPymata4 import CustomPymata4

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


class SmartOven:
    UPLOAD_URL = "http://127.0.0.1:8080/"
    DATA_SEND_INTERVAL = 10
    RESPONSE_DATA = []

    def __init__(self, com_port="COM3", button_pin=8):
        self.BUTTON_PIN = button_pin
        self.LED_PINS = [4, 5, 6, 7]
        self.board = CustomPymata4(com_port=com_port)
        self.board.set_pin_mode_digital_input_pullup(self.BUTTON_PIN)
        for pin in self.LED_PINS:
            self.board.set_pin_mode_digital_output(pin)

        self.board.displayOn()
        time.sleep(2)

    def __del__(self):
        self.board.shutdown()

    def start_timer(self):
        start_timer = time.time()
        while time.time() - start_timer < 10:
            remaining_time = int(10 - (time.time() - start_timer))
            self.board.displayShow(remaining_time)
            self.board.digital_pin_write(self.LED_PINS[3], 1)
            time.sleep(0.1)

            level, time_stamp = self.board.digital_read(self.BUTTON_PIN)
            if level == 0:
                self.board.digital_pin_write(self.LED_PINS[3], 0)
                return

        self.board.digital_pin_write(self.LED_PINS[3], 0)
        self.board.displayShow(0)

    def cook_pizza(self):
        self.board.digital_pin_write(self.LED_PINS[1], 1)

        while True:
            level, time_stamp = self.board.digital_read(self.BUTTON_PIN)
            if level == 0:
                break
            time.sleep(0.1)

        self.board.digital_pin_write(self.LED_PINS[1], 0)
        self.start_timer()

    def run(self):
        while True:
            try:
                self.cook_pizza()
            except Exception as e:
                board.__del__()
                logging.error(f"Failed to send data. {str(e)}")


if __name__ == '__main__':
    board = SmartOven()
    board.run()
