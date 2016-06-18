from datetime import datetime
from subprocess import call
import threading
import time
# import RPi.GPIO as GPIO
import GPIOmock as GPIO


PAUSE_BETWEEN_NOTES = 0.75
CHECK_TIME_INTERVAL = 10

# LEDs to blink with each 15 min
_15_MIN_PIN = 40
_30_MIN_PIN = 12
_45_MIN_PIN = 16
_60_MIN_PIN = 22


# Sets of notes for Westminster Quarters
# https://en.wikipedia.org/wiki/Westminster_Quarters
NOTE_SET_1 = ["Gs4", "Fs4", "E4", "B3"]
NOTE_SET_2 = ["E4", "Gs4", "Fs4", "B3"]
NOTE_SET_3 = ["E4", "Fs4", "Gs4", "E4"]
NOTE_SET_4 = ["Gs4", "E4", "Fs4", "B3"]
NOTE_SET_5 = ["B3", "Fs4", "Gs4", "E4"]

NOTE_PERM_1 = [NOTE_SET_1]
NOTE_PERM_2 = [NOTE_SET_2, NOTE_SET_3]
NOTE_PERM_3 = [NOTE_SET_4, NOTE_SET_5, NOTE_SET_1]
NOTE_PERM_4 = [NOTE_SET_2, NOTE_SET_3, NOTE_SET_4, NOTE_SET_5]


def play_note(note):
    call(["sonic_pi", "play :" + note])


def play_perm(note_perm):
    for note_set in note_perm:
        for num in range(4):
            play_note(note_set[num])
            time.sleep(PAUSE_BETWEEN_NOTES)
        time.sleep(PAUSE_BETWEEN_NOTES)


def play_hour_chimes(hour):
    for num in range(hour if 0 < hour < 13 else abs(hour - 12)):
        call(["sonic_pi", "play :E3"])
        time.sleep(PAUSE_BETWEEN_NOTES * 2)


def sleep_to_next_minute():
    time.sleep(60)


def monitor():
    while True:
        curr_time = datetime.now().time()
        curr_minute = curr_time.minute
        if curr_minute == 15:
            play_perm(NOTE_PERM_1)
            sleep_to_next_minute()
        elif curr_minute == 30:
            play_perm(NOTE_PERM_2)
            sleep_to_next_minute()
        elif curr_minute == 45:
            play_perm(NOTE_PERM_3)
            sleep_to_next_minute()
        elif curr_minute == 00:
            play_perm(NOTE_PERM_4)
            play_hour_chimes(curr_time.hour)
            sleep_to_next_minute()
        else:
            time.sleep(CHECK_TIME_INTERVAL)


def start_monitor():
    t = threading.Thread(target=monitor)
    t.daemon = True
    t.start()


def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(-1, GPIO.OUT)


def main():
    try:
        initialize_gpio()
        start_monitor()
        raw_input("\nPress any key to exit.\n")
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
