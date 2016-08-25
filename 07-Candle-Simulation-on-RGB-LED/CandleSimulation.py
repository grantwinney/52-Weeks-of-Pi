import RPi.GPIO as GPIO
import threading
import time
import random
import math

R = 37
G = 33
BUTTON = 22

pwms = []
aging = 1.0
green_dc = 100


def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([R,G], GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(BUTTON, GPIO.FALLING, throw_on_a_log, 250)


def red_light():
    p = GPIO.PWM(R, 300)
    p.start(100)
    pwms.append(p)
    GPIO.output(R, GPIO.HIGH)
    while True:
        p.ChangeDutyCycle(random.randint(75, 100) * (aging + ((1 - aging) / 5)) if green_dc > 0 else 0)
        rand_flicker_sleep()


def green_light():
    global green_dc
    p = GPIO.PWM(G, 300)
    p.start(0)
    pwms.append(p)
    GPIO.output(G, GPIO.HIGH)
    while True:
        green_dc = random.randint(9, 12) * math.pow(aging, 0.5 / aging) if aging > 0.01 else 0
        p.ChangeDutyCycle(green_dc)
        rand_flicker_sleep()


def rand_flicker_sleep():
    time.sleep(random.randint(3,15) / 100.0)


def dying_down():
    global aging
    while True:
        aging = max(aging - .01, 0)
        time.sleep(.25)


def throw_on_a_log(_):
    global aging
    aging = min(aging + 0.25, 1.0)


def light_a_fire():
    threads = [
        threading.Thread(target=red_light),
        threading.Thread(target=green_light),
        threading.Thread(target=dying_down)
    ]
    for t in threads:
        t.daemon = True
        t.start()
    for t in threads:
        t.join()


def main():
    try:
        initialize_gpio()
        print("\nPress ^C (control-C) to exit the program.\n")
        light_a_fire()
    except KeyboardInterrupt:
        pass
    finally:
        for p in pwms:
            p.stop()
        GPIO.cleanup()


if __name__ == '__main__':
    main()
