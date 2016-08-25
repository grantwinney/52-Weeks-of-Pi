import RPi.GPIO as GPIO
import threading
import time
import random
import math

R = 37
G = 33
BUTTON = 22

pwms = []
intensity = 1.0


def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([R,G], GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(BUTTON, GPIO.FALLING, fan_the_flame, 250)


def red_light():
    p = GPIO.PWM(R, 300)
    p.start(100)
    pwms.append(p)
    while True:
        p.ChangeDutyCycle(random.randint(75, 100) * (intensity + ((1 - intensity) / 10)))
        rand_flicker_sleep()


def green_light():
    global green_dc
    p = GPIO.PWM(G, 300)
    p.start(0)
    pwms.append(p)
    while True:
        p.ChangeDutyCycle(random.randint(9, 12) * math.pow(intensity, 1 / intensity) if intensity > 0 else 0)
        rand_flicker_sleep()


def rand_flicker_sleep():
    time.sleep(random.randint(3,10) / 100.0)


def burning_down():
    global intensity
    while True:
        intensity = max(intensity - .01, 0)
        time.sleep(.25)


def fan_the_flame(_):
    global intensity
    intensity = min(intensity + 0.25, 1.0)


def light_candle():
    threads = [
        threading.Thread(target=red_light),
        threading.Thread(target=green_light),
        threading.Thread(target=burning_down)
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
        light_candle()
    except KeyboardInterrupt:
        pass
    finally:
        for p in pwms:
            p.stop()
        GPIO.cleanup()


if __name__ == '__main__':
    main()
