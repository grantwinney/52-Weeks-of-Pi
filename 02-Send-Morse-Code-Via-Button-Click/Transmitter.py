# coding=utf-8

import RPi.GPIO as GPIO
import datetime
import InternationalMorseCode as ICM

BASE_TIME = 1000000  # in microseconds, 1000000 ms = 1 sec
TOLERANCE = BASE_TIME / 4

INPUT_PIN = 31

segments = ""
letters = []
words = []
last_edge = GPIO.LOW
press = datetime.datetime.now()
release = datetime.datetime.now()


def my_callback(channel):
    #GPIO.output(21, GPIO.input(PIN))
    global last_edge, press, release

    if GPIO.input(INPUT_PIN) == GPIO.HIGH and last_edge == GPIO.LOW:
        #print('\n▼  at ' + str(datetime.datetime.now()))
        last_edge = GPIO.HIGH
        press = datetime.datetime.now()
        detect_end_of_letter(press, release)

    elif GPIO.input(INPUT_PIN) == GPIO.LOW and last_edge == GPIO.HIGH:
        #print('\n ▲ at ' + str(datetime.datetime.now()))
        last_edge = GPIO.LOW
        release = datetime.datetime.now()
        interpret_input(press, release)


def interpret_input(press, release):
    global segments

    delta = calc_delta(press, release)
    print('Button click timespan: ' + str(delta))

    if (delta > (BASE_TIME - TOLERANCE)) and (delta < (BASE_TIME + TOLERANCE)):
        print 'received dot'
        segments += '.'
        #print segments
    elif (delta > ((BASE_TIME * 3) - TOLERANCE)) and (delta < ((BASE_TIME * 3) + TOLERANCE)):
        print 'received dash'
        segments += '-'
        print segments


def detect_end_of_letter(press, release):
    global segments

    delta = calc_delta(release, press)
    if (delta > ((BASE_TIME * 3) - TOLERANCE)) and (delta < ((BASE_TIME * 3) + TOLERANCE)):
        #print 'edge of letter detected!'
        code = ICM.symbols.get(segments, '')
        if code != '':
            print 'detected letter is ' + code
            letters.append(code)
            segments = ""
        else:
            print 'invalid combo: ' + segments


def calc_delta(t1, t2):
    delta = t2 - t1
    return (delta.seconds * 1000000) + delta.microseconds


def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(36, GPIO.OUT)  # Red LED
    GPIO.setup(32, GPIO.OUT)  # Green LED

    GPIO.setup(INPUT_PIN, GPIO.IN)
    GPIO.add_event_detect(INPUT_PIN, GPIO.BOTH, callback=my_callback)


try:
    initialize_gpio()
    message = raw_input('\nPress any key to exit.\n')

finally:
    GPIO.cleanup()

print("Goodbye!")
