import logging
import time

import requests
from fhict_cb_01.CustomPymata4 import CustomPymata4

from oven.models import OrderState


class SmartOven:
    UPLOAD_URL = "http://127.0.0.1:8080/kitchen"
    ORDERS_URL = "http://127.0.0.1:8080/orders"

    def __init__(self, com_port="COM4", button_pin=8):
        self.BUTTON_PIN = button_pin
        self.LED_PINS = [4, 5, 6, 7]
        self.board = CustomPymata4(com_port=com_port)
        self.board.set_pin_mode_digital_input_pullup(self.BUTTON_PIN)
        for pin in self.LED_PINS:
            self.board.set_pin_mode_digital_output(pin)

        self.board.displayOn()

    def get_valid_order_id(self):
        while True:
            order_id = input("Enter order id to proceed: ")
            if self.check_order_exists(order_id):
                return order_id
            print("Order does not exist or is not in SUBMITTED state.")

    def check_order_exists(self, order_id):
        response = requests.get(f"{self.ORDERS_URL}/{order_id}")
        if response.status_code == 200:
            order_state = response.json().get('state')
            logging.info(f'Order with id {order_id} has state {order_state}.')
            return order_state == 'OrderState.SUBMITTED'

        logging.info(f"Order with id {order_id} does not exist in the database.")
        return False

    def update_order_state(self, order_id, new_state):
        payload = {'state': new_state}
        response = requests.patch(f"{self.ORDERS_URL}/{order_id}", json=payload)
        if response.status_code == 200:
            logging.info(f"Order with id {order_id} has been updated to {new_state} state.")
            return True

        logging.info(f"Failed to update order with id {order_id}.")
        return False

    def start_timer(self, order_id):
        global oven_data
        self.update_order_state(order_id, OrderState.PENDING)

        for remaining_time in reversed(range(0, 10)):
            self.board.displayShow(remaining_time)
            self.board.digital_pin_write(self.LED_PINS[3], 1)

            oven_data = {
                "order_number": order_id,
                "time_left": remaining_time,
                "oven_status": "Busy"
            }
            requests.post(self.UPLOAD_URL, json=oven_data)

            level, _ = self.board.digital_read(self.BUTTON_PIN)
            if level == 0:
                self.board.digital_pin_write(self.LED_PINS[3], 0)
                return False

            time.sleep(1)

        oven_data["oven_status"] = "Done"
        requests.post(self.UPLOAD_URL, json=oven_data)

        self.board.digital_pin_write(self.LED_PINS[3], 0)
        self.board.displayShow(0)

        self.update_order_state(order_id, OrderState.COMPLETED)
        return True

    def cook_pizza(self):
        self.board.digital_pin_write(self.LED_PINS[1], 1)

        while True:
            level, _ = self.board.digital_read(self.BUTTON_PIN)
            if level == 0:
                break
            time.sleep(0.1)

        self.board.digital_pin_write(self.LED_PINS[1], 0)

        order_id = self.get_valid_order_id()
        if order_id:
            if not self.start_timer(order_id):
                logging.info("Timer cancelled.")

    def run(self):
        while True:
            try:
                self.cook_pizza()
            except Exception as e:
                logging.error(f"Failed to send data. {str(e)}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    board = SmartOven()
    board.run()
