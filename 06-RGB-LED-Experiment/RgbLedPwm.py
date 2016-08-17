import RPi.GPIO as GPIO
#import GPIOmock as GPIO
import threading
import time
import random

R = 12
G = 33
B = 32

PINS = [R,G,B]

ROTATION_IN_MS = 750


def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PINS, GPIO.OUT, initial=GPIO.LOW)


def color_test(channel, freq, speed):
    p = GPIO.PWM(channel, freq)
    p.start(0)
    while True:
        for dc in range(0, 101, 2):
            p.ChangeDutyCycle(dc)
            time.sleep(speed)
        for dc in range(100, -1, -2):
            p.ChangeDutyCycle(dc)
            time.sleep(speed)


def color_test_thread():
    threads = []
    threads.append(threading.Thread(target=color_test, args=(R, 50, 0.04)))
    threads.append(threading.Thread(target=color_test, args=(G, 50, 0.07)))
    threads.append(threading.Thread(target=color_test, args=(B, 50, 0.10)))
    for t in threads:
        t.daemon = True
        t.start()
    for t in threads:
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
