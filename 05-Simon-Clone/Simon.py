import RPi.GPIO as GPIO
#import GPIOmock as GPIO
import threading
import time

LED_GRN = 33
LED_RED = 37
LED_BLU = 35
LED_YLW = 31

BTN_GRN = 11
BTN_RED = 15
BTN_BLU = 13
BTN_YLW = 7

COLORS = [LED_GRN, LED_RED, LED_BLU, LED_YLW]
BUTTONS = [BTN_GRN, BTN_RED, BTN_BLU, BTN_YLW]

DISPLAYING_PATTERN = False


def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([BTN_GRN, BTN_RED, BTN_BLU, BTN_YLW], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup([LED_GRN, LED_RED, LED_BLU, LED_YLW], GPIO.OUT)
    GPIO.output([LED_GRN, LED_RED, LED_BLU, LED_YLW], GPIO.LOW)
    GPIO.add_event_detect(BTN_GRN, GPIO.BOTH, callback=process_button_click)
    GPIO.add_event_detect(BTN_RED, GPIO.BOTH, callback=process_button_click)
    GPIO.add_event_detect(BTN_BLU, GPIO.BOTH, callback=process_button_click)
    GPIO.add_event_detect(BTN_YLW, GPIO.BOTH, callback=process_button_click)


def process_button_click(channel):
    if not DISPLAYING_PATTERN:
        if channel == BTN_GRN:
            GPIO.output(LED_GRN, GPIO.input(channel))
        elif channel == BTN_RED:
            GPIO.output(LED_RED, GPIO.input(channel))
        elif channel == BTN_BLU:
            GPIO.output(LED_BLU, GPIO.input(channel))
        else:
            GPIO.output(LED_YLW, GPIO.input(channel))

level = 1
pattern = []


def create_next_pattern():
    global pattern
    pattern = [COLORS[0]]


def display_pattern_to_user():
    global DISPLAYING_PATTERN
    DISPLAYING_PATTERN = True
    GPIO.output(pattern[0], GPIO.HIGH)
    time.sleep(500)
    GPIO.output(pattern[0], GPIO.LOW)
    DISPLAYING_PATTERN = False


def start_game():
    while True:
        create_next_pattern()
        display_pattern_to_user()
        time.sleep(500)


def start_game_monitor():
    t = threading.Thread(target=start_game)
    t.daemon = True
    t.start()


def main():
    try:
        initialize_gpio()
        start_game_monitor()
        raw_input("\nPress any key to exit.\n")
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
