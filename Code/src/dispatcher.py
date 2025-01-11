from drivers.controlboard_driver import ControlBoard
from time import sleep


class Dispatcher:
    def __init__(self, control_board: ControlBoard):
        self.control_board = control_board

        self.dispatcher = {
            "print": self.print_task,
            "sleep": self.sleep_task,
            "goto": self.control_board.goto,
            "echo": self.control_board.echo,
            "gcode": self.control_board.send_message
        }

    def print_task(self, message: str):
        print(message)

    def sleep_task(self, seconds: int):
        print(f"Sleeping for {seconds} seconds")
        sleep(seconds)
