import RPi.GPIO as GPIO
import time


class Motor:
    def __init__(self, app_window, motor_name, pwm_channel):
        self.app_window = app_window
        self.motor_name = motor_name
        self.pwm_channel = pwm_channel


class DCMotor(Motor):
    duty_cycle = 50  # Скорость моторов. Одна для всех.

    # Flags
    is_forward_flag = False
    is_back_flag = False

    def __init__(self, app_window, motor_name, gpio_in_first, gpio_in_second, pwm_channel):
        super().__init__(app_window, motor_name, pwm_channel)
        self.gpio_in_first = gpio_in_first
        self.gpio_in_second = gpio_in_second
        GPIO.setup(self.gpio_in_first, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.gpio_in_second, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pwm_channel, GPIO.OUT, initial=GPIO.LOW)
        self.pwm = GPIO.PWM(self.pwm_channel, 1000)
        self.pwm.start(DCMotor.duty_cycle)

    def go_forward(self):
        GPIO.output(self.gpio_in_first, GPIO.HIGH)
        GPIO.output(self.gpio_in_second, GPIO.LOW)

    def go_backward(self):
        GPIO.output(self.gpio_in_first, GPIO.LOW)
        GPIO.output(self.gpio_in_second, GPIO.HIGH)

    def stop_moving(self):
        GPIO.output(self.gpio_in_first, GPIO.LOW)
        GPIO.output(self.gpio_in_second, GPIO.LOW)

    def set_speed(self):
        self.pwm.ChangeDutyCycle(DCMotor.duty_cycle)

    @staticmethod
    def change_speed(speed):
        if speed == "Left":
            DCMotor.duty_cycle -= 25
        else:
            DCMotor.duty_cycle += 25


class ServoMotor(Motor):
    stabilization_time = 0.09  # Время стабилизации серво моторов. Одно для всех.

    # Flags
    move_left_flag = False
    move_right_flag = False

    def __init__(self, app_window, motor_name, pwm_channel):
        super().__init__(app_window, motor_name, pwm_channel)
        self.duty_cycle = 7.5
        GPIO.setup(self.pwm_channel, GPIO.OUT, initial=GPIO.LOW)
        self.pwm = GPIO.PWM(self.pwm_channel, 50)
        self.pwm.start(self.duty_cycle)
        time.sleep(self.stabilization_time)
        self.pwm.ChangeDutyCycle(0)

    def go_left(self):
        print("thread___1 alive!")
        while ServoMotor.move_left_flag:
            if self.duty_cycle != 5.0:
                self.duty_cycle -= 0.5
                self.pwm.ChangeDutyCycle(self.duty_cycle)
                time.sleep(self.stabilization_time)
                self.pwm.ChangeDutyCycle(0)
                self.app_window.info_labels[6]["text"] = str(self.duty_cycle)
        print("thread___1 finished.")

    def go_right(self):
        print("thread_2 alive!")
        while ServoMotor.move_right_flag:
            if self.duty_cycle != 10:
                self.duty_cycle += 0.5
                self.pwm.ChangeDutyCycle(self.duty_cycle)
                time.sleep(self.stabilization_time)
                self.pwm.ChangeDutyCycle(0)
                self.app_window.info_labels[6]["text"] = str(self.duty_cycle)
        print("thread___2 finished.")

    def go_center(self):
        self.duty_cycle = 7.5
        self.pwm.ChangeDutyCycle(self.duty_cycle)
        time.sleep(self.stabilization_time)
        self.pwm.ChangeDutyCycle(0)
        self.app_window.info_labels[6]["text"] = str(self.duty_cycle)
