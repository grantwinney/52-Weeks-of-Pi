import datetime, threading, time
import RPi.GPIO as GPIO
import InternationalMorseCode as ICM

BASE_TIME_SECONDS = 1
TOLERANCE = BASE_TIME_SECONDS / 4.0

INPUT_PIN = 31
METRONOME_PIN = 11


### METRONOME: Setup a blue LED to blink at the "base time" interval,
###  which will assist in timing the button clicks

is_metronome_on = False


def metronome_tick():
    global is_metronome_on

    while True:
        if is_metronome_on == False:
            GPIO.output(METRONOME_PIN, GPIO.HIGH)
            is_metronome_on = True
        else:
            GPIO.output(METRONOME_PIN, GPIO.LOW)
            is_metronome_on = False
        time.sleep(BASE_TIME_SECONDS)


def start_metronome():
    GPIO.setup(METRONOME_PIN, GPIO.OUT)
    timerThread = threading.Thread(target=metronome_tick)
    timerThread.daemon = True
    timerThread.start()


### TRANSMITTER: Setup pin 31 to read input when the button is clicked.
###  Interpret and store each dot/dash, letter and word.

sequence = ""
letters = []
words = []
last_edge = GPIO.LOW
press = datetime.datetime.now()
release = datetime.datetime.now()


def my_callback(channel):
    global last_edge, press, release

    if GPIO.input(INPUT_PIN) == GPIO.HIGH and last_edge == GPIO.LOW:
        last_edge = GPIO.HIGH
        press = datetime.datetime.now()
        detect_end_of_letter(press, release)
    elif GPIO.input(INPUT_PIN) == GPIO.LOW and last_edge == GPIO.HIGH:
        last_edge = GPIO.LOW
        release = datetime.datetime.now()
        interpret_input(press, release)


def detect_end_of_letter(press, release):
    global sequence
    base_time_in_ms = BASE_TIME_SECONDS * 1000000
    tolerance_in_ms = TOLERANCE * 1000000

    delta = calc_delta(release, press)

    if (delta > ((base_time_in_ms * 3) - tolerance_in_ms)) and (delta < ((base_time_in_ms * 3) + tolerance_in_ms)):
        code = ICM.symbols.get(sequence, '')
        if code != '':
            print 'detected letter is ' + code
            letters.append(code)
            sequence = ""
        else:
            print 'invalid combo: ' + sequence

    elif (delta > ((base_time_in_ms * 7) - tolerance_in_ms)) and (delta < ((base_time_in_ms * 7) + tolerance_in_ms)):
        code = ICM.symbols.get(sequence, '')
        if code != '':
            print 'detected letter is ' + code
            letters.append(code)
            word = ''.join(letters)
            if word == "AR":
                print 'END OF TRANSMISSION! Thanks for playing!'
            words.append(word)
            letters[:] = []
            sequence = ""
        else:
            print 'invalid combo: ' + sequence


def interpret_input(press, release):
    global sequence
    base_time_in_ms = BASE_TIME_SECONDS * 1000000
    tolerance_in_ms = TOLERANCE * 1000000

    delta = calc_delta(press, release)

    print base_time_in_ms
    print tolerance_in_ms

    if (delta > (base_time_in_ms - tolerance_in_ms)) and (delta < (base_time_in_ms + tolerance_in_ms)):
        sequence += '.'
        print "Timespan " + str(delta) + " : " + sequence
    elif (delta > ((base_time_in_ms * 3) - tolerance_in_ms)) and (delta < ((base_time_in_ms * 3) + tolerance_in_ms)):
        sequence += '-'
        print "Timespan " + str(delta) + " : " + sequence
    else:
        print "Timespan " + str(delta) + " : unrecognized input"


def calc_delta(t1, t2):
    delta = t2 - t1
    return (delta.seconds * 1000000) + delta.microseconds


def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(36, GPIO.OUT)             # Red LED
    GPIO.setup(32, GPIO.OUT)             # Green LED

    GPIO.setup(INPUT_PIN, GPIO.IN)
    GPIO.add_event_detect(INPUT_PIN, GPIO.BOTH, callback=my_callback)


try:
    initialize_gpio()
    start_metronome()
    message = raw_input('\nPress any key to exit.\n')


finally:
    GPIO.cleanup()

print("Goodbye!")
