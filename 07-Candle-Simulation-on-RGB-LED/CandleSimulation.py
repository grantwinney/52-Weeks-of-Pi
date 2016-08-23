import RPi.GPIO as GPIO
import threading
import time
import random

R = 37
G = 33

pwms = []


def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([R,G], GPIO.OUT, initial=GPIO.HIGH)


def red_light():
    p = GPIO.PWM(R, 300)
    p.start(100)
    pwms.append(p)

    while True:
        p.ChangeDutyCycle(random.randint(80,100))
        rand_flicker_time()


def green_light():
    p = GPIO.PWM(G, 300)
    p.start(0)
    pwms.append(p)

    while True:
        p.ChangeDutyCycle(random.randint(10,20))
        rand_flicker_time()


def rand_flicker_time():
    time.sleep(random.randint(3,15) / 100.0)


#def dying_down():
    


def light_a_fire():
    threads = []
    threads.append(threading.Thread(target=red_light))
    threads.append(threading.Thread(target=green_light))
    #threads.append(threading.Thread(target=dying_down))
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
