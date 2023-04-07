import json
import logging
import time
from enum import Enum
import requests

from fhict_cb_01.CustomPymata4 import CustomPymata4


class OrderState(Enum):
    SUBMITTED = "OrderState.SUBMITTED"
    IN_PROGRESS = "OrderState.IN_PROGRESS"
    COMPLETED = "OrderState.COMPLETED"


class OrderStateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, OrderState):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


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

    def check_order_exists(self, order_id):
        response = requests.get(f"{self.ORDERS_URL}/{order_id}")
        if response.status_code == 200:
            order_state = OrderState(response.json()['state'])
            if order_state == OrderState.SUBMITTED:
                return True
        logging.info("Order does not exist in the database.")
        return False

    # def update_order_state(self, order_id, state):
    #     response = requests.patch(f"{self.ORDERS_URL}/{order_id}", json={"state": state}, cls=OrderStateEncoder)
    #     if response.status_code == 200:
    #         logging.info(f"Order {order_id} state updated successfully to {state}.")
    #     logging.error(f"Failed to update the order state. {response.text}")

    def start_timer(self, order_id):
        for remaining_time in range(10, 0, -1):
            self.board.displayShow(remaining_time)
            self.board.digital_pin_write(self.LED_PINS[3], 1)

            oven_data = {
                "order_number": order_id,
                "time_left": remaining_time,
                "oven_status": "Busy"
            }
            requests.post(self.UPLOAD_URL, json=oven_data)

            level, time_stamp = self.board.digital_read(self.BUTTON_PIN)
            if level == 0:
                self.board.digital_pin_write(self.LED_PINS[3], 0)
                return False

            time.sleep(1)

        oven_data = {
            "order_number": order_id,
            "time_left": 0,
            "oven_status": "Done"
        }
        requests.post(self.UPLOAD_URL, json=oven_data)

        self.board.digital_pin_write(self.LED_PINS[3], 0)
        self.board.displayShow(0)

        # self.update_order_state(order_id, OrderState.COMPLETED)
        return True

    def cook_pizza(self):
        self.board.digital_pin_write(self.LED_PINS[1], 1)

        while True:
            level, time_stamp = self.board.digital_read(self.BUTTON_PIN)
            if level == 0:
                break
            time.sleep(0.1)

        self.board.digital_pin_write(self.LED_PINS[1], 0)

        order_id = input("Enter order id to proceed: ")
        while not self.check_order_exists(order_id):
            order_id = input("Try again. Enter order id to proceed: ")

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
