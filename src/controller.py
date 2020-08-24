import RPi.GPIO as GPIO
import threading
from src.model import DCMotor, ServoMotor


class AppController:
    def __init__(self, app_window):
        self.app_window = app_window
        GPIO.setmode(GPIO.BCM)

        # DC motors
        self.motor1 = DCMotor(self.app_window, "Motor_1", 16, 20, 21)  # 21 - PWM-EN
        self.motor2 = DCMotor(self.app_window, "Motor_2", 13, 19, 26)  # 26 - PWM-EN

        # Servo motor
        self.servo1 = ServoMotor(self.app_window, "ServoMotor_1", 12)  # 12 - PWM

    def action_pressed(self, event):
        if event.keysym == "Up":
            if not DCMotor.is_back_flag:
                DCMotor.is_forward_flag = True
                self.app_window.info_labels[1]["text"] = "GO forward"
                self.motor1.go_forward()
                self.motor2.go_forward()
        elif event.keysym == "Down":
            if not DCMotor.is_forward_flag:
                DCMotor.is_back_flag = True
                self.app_window.info_labels[3]["text"] = "GO back"
                self.motor1.go_backward()
                self.motor2.go_backward()
        elif event.keysym == "XF86AudioPrev":
            ServoMotor.move_left_flag = True
            self.app_window.info_labels[2]["text"] = "Left"
            new_thread_left = threading.Thread(target=self.servo1.go_left)
            new_thread_left.start()
        elif event.keysym == "XF86AudioNext":
            ServoMotor.move_right_flag = True
            self.app_window.info_labels[4]["text"] = "Right"
            new_thread_right = threading.Thread(target=self.servo1.go_right)
            new_thread_right.start()
        elif event.keysym == "XF86AudioPlay":
            # if (ServoMotor.move_left_flag is False) and (ServoMotor.move_right_flag is False):
            self.servo1.go_center()
        elif event.keysym == "Left":
            if DCMotor.duty_cycle != 0:
                DCMotor.change_speed("Left")
                self.motor1.set_speed()
                self.motor2.set_speed()
                self.app_window.info_labels[5]["text"] = str(DCMotor.duty_cycle) + "%"
        elif event.keysym == "Right":
            if DCMotor.duty_cycle != 100:
                DCMotor.change_speed("Right")
                self.motor1.set_speed()
                self.motor2.set_speed()
                self.app_window.info_labels[5]["text"] = str(DCMotor.duty_cycle) + "%"
        elif event.keysym == "Escape":
            self.program_exit()

    def action_released(self, event):
        if event.keysym == "Up":
            DCMotor.is_forward_flag = False
            self.app_window.info_labels[1]["text"] = ""
            self.motor1.stop_moving()
            self.motor2.stop_moving()
        elif event.keysym == "Down":
            DCMotor.is_back_flag = False
            self.app_window.info_labels[3]["text"] = ""
            self.motor1.stop_moving()
            self.motor2.stop_moving()
        elif event.keysym == "XF86AudioPrev":
            ServoMotor.move_left_flag = False
            self.app_window.info_labels[2]["text"] = ""
        elif event.keysym == "XF86AudioNext":
            ServoMotor.move_right_flag = False
            self.app_window.info_labels[4]["text"] = ""

    def program_exit(self):
        self.motor1.pwm.stop()
        self.motor2.pwm.stop()
        self.servo1.pwm.stop()
        GPIO.cleanup()
        self.app_window.destroy()
        print("Speed car program finished!")
