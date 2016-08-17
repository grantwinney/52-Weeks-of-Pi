import RPi.GPIO as GPIO
#import GPIOmock as GPIO
import threading
import time
import random

R = 37
G = 33
B = 31

PINS = [R,G,B]

ROTATION_IN_MS = 750


def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PINS, GPIO.OUT, initial=GPIO.LOW)


def color_test():
    while True:
        next_pin = PINS[random.randint(0, 2)]
        GPIO.output(next_pin, not GPIO.input(next_pin))
        time.sleep(ROTATION_IN_MS / 1000)


def color_test_thread():
    t = threading.Thread(target=color_test)
    t.daemon = True
    t.start()
    t.join()


def main():
    try:
        initialize_gpio()
        print("\nPress ^C (control-C) to exit the program.\n")
        color_test_thread()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
