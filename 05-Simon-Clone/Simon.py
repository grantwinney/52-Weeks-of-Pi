import RPi.GPIO as GPIO
#import GPIOmock as GPIO
import threading
import time
import random

LED_GRN = 33
LED_RED = 37
LED_BLU = 35
LED_YLW = 31

BTN_GRN = 11
BTN_RED = 15
BTN_BLU = 13
BTN_YLW = 7

LIGHTS = [LED_GRN, LED_RED, LED_BLU, LED_YLW]
BUTTONS = [BTN_GRN, BTN_RED, BTN_BLU, BTN_YLW]

DISPLAYING_PATTERN = False

current_iteration = 0

passed_level = True

level = 1
pattern = []
random.seed()
speed = 0.25


def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(LIGHTS, GPIO.OUT, initial=GPIO.LOW)
    for i in range(4):
        GPIO.add_event_detect(BUTTONS[i], GPIO.BOTH, callback=process_button_click)


def process_button_click(channel):
    if not DISPLAYING_PATTERN:
        global current_iteration
        for i in range(level):
            if current_iteration >= level:
                move_to_next_level()
                break
            toggle_led(channel)
            if GPIO.input(channel) == GPIO.HIGH:
                print current_iteration
                print pattern[current_iteration-1]
                if channel == BUTTONS[pattern[current_iteration]]:
                    current_iteration += 1
                    print("Right!")
                else:
                    print("Wrong!")
                    break


def move_to_next_level():
    global level
    level += 1
    passed_level = True
    print("passed!")


def toggle_led(channel):
    GPIO.output(LIGHTS[BUTTONS.index(channel)], not GPIO.input(channel))


def reset_for_next_iteration():
    global passed_level
    passed_level = False
    global current_iteration
    current_iteration = 0


def add_color_to_pattern():
    pattern.append(random.randint(0, 3))
    #pattern.append(0)
    

def display_pattern_to_user():
    global DISPLAYING_PATTERN
    DISPLAYING_PATTERN = True
    GPIO.output(LIGHTS, GPIO.LOW)
    for i in range(level):
        GPIO.output(LIGHTS[pattern[i]], GPIO.HIGH)
        time.sleep(speed)
        GPIO.output(LIGHTS[pattern[i]], GPIO.LOW)
        time.sleep(speed)
    DISPLAYING_PATTERN = False


def wait_for_user_input():
    while not passed_level:
        time.sleep(0.1)
    time.sleep(speed)


def start_game():
    while True:
        reset_for_next_iteration()
        add_color_to_pattern()
        display_pattern_to_user()
        wait_for_user_input()


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
