import datetime, threading, time
# import RPi.GPIO as GPIO
import GPIOmock as GPIO
import InternationalMorseCode as ICM

BASE_TIME_SECONDS = 1
TOLERANCE = BASE_TIME_SECONDS / 4.0


# Initialize GPIO settings
def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([11, 32, 36], GPIO.OUT)  # LEDs: Blue (metronome), Green (ok), Red (error)
    GPIO.setup(31, GPIO.IN)
    GPIO.add_event_detect(31, GPIO.BOTH, callback=intercept_morse_code)


# Blink a blue LED on/off repeatedly, to assist in sending morse code
def metronome():
    while True:
        GPIO.output(11, not GPIO.input(11))
        time.sleep(BASE_TIME_SECONDS)


last_edge = GPIO.LOW
press = datetime.datetime.now()
release = datetime.datetime.now()


# Intercept a rise or fall on pin 31 (button press/release)
def intercept_morse_code(channel):
    global last_edge, press, release

    # Button pressed - ????
    if GPIO.input(channel) == GPIO.HIGH and last_edge == GPIO.LOW:
        last_edge = GPIO.HIGH
        press = datetime.datetime.now()
        detect_end_of_letter()

    # Button released - determine what the input is
    elif GPIO.input(channel) == GPIO.LOW and last_edge == GPIO.HIGH:
        last_edge = GPIO.LOW
        release = datetime.datetime.now()
        interpret_input()


sequence = ""
letters = []
words = []


def detect_end_of_letter():
    global sequence
    base_time_in_ms = BASE_TIME_SECONDS * 1000000
    tolerance_in_ms = TOLERANCE * 1000000

    delta = calc_delta(release, press)

    if (delta > ((base_time_in_ms * 3) - tolerance_in_ms)) and (delta < ((base_time_in_ms * 3) + tolerance_in_ms)):
        code = ICM.symbols.get(sequence, '')
        if code != '':
            print('detected letter is ' + code)
            letters.append(code)
            sequence = ""
        else:
            print('invalid combo: ' + sequence)

    elif (delta > ((base_time_in_ms * 7) - tolerance_in_ms)) and (delta < ((base_time_in_ms * 7) + tolerance_in_ms)):
        code = ICM.symbols.get(sequence, '')
        if code != '':
            print('detected letter is ' + code)
            letters.append(code)
            word = ''.join(letters)
            if word == "AR":
                print('END OF TRANSMISSION! Thanks for playing!')
            words.append(word)
            letters[:] = []
            sequence = ""
        else:
            print('invalid combo: ' + sequence)


def interpret_input():
    global sequence
    base_time_in_ms = BASE_TIME_SECONDS * 1000000
    tolerance_in_ms = TOLERANCE * 1000000

    delta = calc_delta(press, release)

    print(base_time_in_ms)
    print(tolerance_in_ms)

    if (delta > (base_time_in_ms - tolerance_in_ms)) and (delta < (base_time_in_ms + tolerance_in_ms)):
        sequence += '.'
        print("Timespan " + str(delta) + " : " + sequence)
    elif (delta > ((base_time_in_ms * 3) - tolerance_in_ms)) and (delta < ((base_time_in_ms * 3) + tolerance_in_ms)):
        sequence += '-'
        print("Timespan " + str(delta) + " : " + sequence)
    else:
        print("Timespan " + str(delta) + " : unrecognized input")


def calc_delta(t1, t2):
    delta = t2 - t1
    return (delta.seconds * 1000000) + delta.microseconds


try:
    initialize_gpio()
    threading.Thread(target=metronome, daemon=True).start()
    message = raw_input('\nPress any key to exit.\n')


finally:
    GPIO.cleanup()

print("Goodbye!")
