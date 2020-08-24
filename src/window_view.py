from tkinter import Tk, Label
from src.controller import AppController
from src.model import DCMotor


class AppWindow(Tk):
    def __init__(self):
        super().__init__()

        self.controller = AppController(self)

        self.info_labels = [
            Label(self, text="Esc", borderwidth=2, relief="raised", width=10),  # Esc
            Label(self, text="", borderwidth=2, relief="solid", width=10),  # Up
            Label(self, text="", borderwidth=2, relief="solid", width=10),  # Left
            Label(self, text="", borderwidth=2, relief="solid", width=10),  # Down
            Label(self, text="", borderwidth=2, relief="solid", width=10),  # Right
            Label(self, text=str(DCMotor.duty_cycle) + "%", borderwidth=2, relief="raised", width=10),  # Speed
            Label(self, text=str(7.5), borderwidth=2, relief="raised", width=10)  # Rotation
        ]

        self.set_window_details()
        self.window_elements_settings()

    def set_window_details(self):
        self.resizable(False, False)
        self.title("SpeedCar")
        self.geometry("260x75")
        self.eval("tk::PlaceWindow . center")
        self.bind("<Key>", self.controller.action_pressed)
        self.bind("<KeyRelease>", self.controller.action_released)
        self.protocol("WM_DELETE_WINDOW", self.controller.program_exit)

    def window_elements_settings(self):
        # LABELS
        self.info_labels[0].grid(sticky="w", row=0, column=0)  # Esc
        self.info_labels[1].grid(sticky="w", row=0, column=1)  # Up
        self.info_labels[2].grid(sticky="w", row=1, column=0)  # Left
        self.info_labels[3].grid(sticky="w", row=2, column=1)  # Down
        self.info_labels[4].grid(sticky="w", row=1, column=2)  # Right
        self.info_labels[5].grid(sticky="w", row=2, column=2)  # Speed
        self.info_labels[6].grid(sticky="w", row=2, column=0)  # Rotation
