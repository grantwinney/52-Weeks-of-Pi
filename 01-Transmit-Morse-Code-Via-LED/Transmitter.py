import RPi.GPIO as GPIO
import time
import InternationalMorseCode as ICM

UNIT_TIME = .25
PIN = 21
VERBOSE = True


def initialize_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PIN, GPIO.OUT)


def transmit_sentence(sentence):
    for (index, word) in enumerate(sentence.split()):
        if index > 0:
            wait_between_words()
        transmit_word(word)


def transmit_word(word):
    for (index, letter) in enumerate(word):
        if index > 0:
            wait_between_letters()
        transmit_letter(letter)


def transmit_letter(letter):
    code = ICM.symbols.get(letter.upper(), '')

    if code != '':

        if VERBOSE:
            print('\nProcessing letter "{}" and code "{}"'.format(letter.upper(), code))

        for (index, signal) in enumerate(code):
            if index > 0:
                wait_between_signals()

            if signal == '.':
                transmit_dot()
            else:
                transmit_dash()

    else:
        if VERBOSE:
            print('\nInvalid input: {}'.format(letter))


def transmit_dot():
    GPIO.output(PIN, GPIO.HIGH)
    time.sleep(UNIT_TIME)


def transmit_dash():
    GPIO.output(PIN, GPIO.HIGH)
    time.sleep(UNIT_TIME * 3)


def wait_between_signals():
    GPIO.output(PIN, GPIO.LOW)
    time.sleep(UNIT_TIME)


def wait_between_letters():
    GPIO.output(PIN, GPIO.LOW)
    time.sleep(UNIT_TIME * 3)


def wait_between_words():
    GPIO.output(PIN, GPIO.LOW)
    time.sleep(UNIT_TIME * 7)


initialize_gpio()

message = '~'

while message != '':
    message = input('\nEnter a message to transmit, or leave blank to exit: ')

    if message != '':
        if VERBOSE:
            print('\nBegin Transmission')

        transmit_sentence(message)
        GPIO.output(PIN, GPIO.LOW)

        if VERBOSE:
            print('\nEnd Transmission')

print("\nGoodbye!")
