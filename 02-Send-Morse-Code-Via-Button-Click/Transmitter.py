# coding=utf-8

import RPi.GPIO as GPIO
import datetime
import InternationalMorseCode as ICM

UNIT_TIME = .25
ACCEPTABLE_DELTA = UNIT_TIME / 4

PIN = 6


def my_callback(channel):
    #GPIO.output(21, GPIO.input(PIN))

    if GPIO.input(PIN) == GPIO.HIGH:
        print('\n▼  at ' + str(datetime.datetime.now()))
    else:
        print('\n ▲ at ' + str(datetime.datetime.now()))


def initialize_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.IN)#, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(PIN, GPIO.BOTH, callback=my_callback)#, bouncetime=100)
    #GPIO.setup(21,GPIO.OUT)

try:
    initialize_gpio()
    message = raw_input('\nPress any key to exit.\n')

finally:
    GPIO.cleanup()

print("Goodbye!")
