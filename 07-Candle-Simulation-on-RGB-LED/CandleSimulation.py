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


def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([R,G], GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(BUTTON, GPIO.FALLING, throw_on_a_log, 250)


def red_light():
    p = GPIO.PWM(R, 300)
    p.start(100)
    pwms.append(p)

    while True:
        p.ChangeDutyCycle(rand_flicker_level(80,100))
        rand_flicker_sleep()


def green_light():
    p = GPIO.PWM(G, 300)
    p.start(0)
    pwms.append(p)

    while True:
        p.ChangeDutyCycle(rand_flicker_level(10,20))
        rand_flicker_sleep()


def rand_flicker_sleep():
    time.sleep(random.randint(3,15) / 100.0)


def rand_flicker_level(min_lvl, max_lvl):
    math.floor(random.randint(min_lvl, max_lvl) * aging)


def dying_down():
    global aging
    aging -= 0.02
    if aging < 0:
        aging = 0
    time.sleep(1)


def throw_on_a_log(_):
    global aging
    aging += 0.25
    if aging > 100:
        aging = 100


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
