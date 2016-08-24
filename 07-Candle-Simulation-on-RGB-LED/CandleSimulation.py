import RPi.GPIO as GPIO
import threading
import time
import random

R = 37
G = 33
BUTTON = 22

pwms = []
aging = 1.0


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
        if aging > .1:
            p.ChangeDutyCycle(rand_flicker_level(75,100))
        else:
            p.ChangeDutyCycle(rand_flicker_level(75,100) / (aging * 4))
        rand_flicker_sleep()


def green_light():
    p = GPIO.PWM(G, 300)
    p.start(0)
    pwms.append(p)
    GPIO.output(G, GPIO.HIGH)
    while True:
        if aging > .1:
            p.ChangeDutyCycle(rand_flicker_level(15,20))
        else:
            p.ChangeDutyCycle(rand_flicker_level(1,3)/10)
        #p.ChangeDutyCycle(rand_flicker_level(15,20) if aging > .05 else 0)
        rand_flicker_sleep()


def rand_flicker_sleep():
    time.sleep(random.randint(3,15) / 100.0)


def rand_flicker_level(min_lvl, max_lvl):
    return random.randint(min_lvl, max_lvl) * aging


def dying_down():
    global aging
    while True:
        if aging > .05:
            aging -= .01
        elif aging > .01:
            aging -= .001
        else:
            aging = 0 
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
