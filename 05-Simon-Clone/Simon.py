import RPi.GPIO as GPIO
#import GPIOmock as GPIO
import threading
import time
import random
import sys
import os

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

# values you can change that affect game play
speed = 0.25

# flags used to signal game status
is_displaying_pattern = False
is_won_current_level = True
is_game_over = False

# game state
current_level = 1
current_step_of_level = 0
pattern = []


def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(LIGHTS, GPIO.OUT, initial=GPIO.LOW)
    for i in range(4):
        GPIO.add_event_detect(BUTTONS[i], GPIO.FALLING, callback=verify_player_selection, bouncetime=50)


def verify_player_selection(channel):
    global current_step_of_level, current_level, is_won_current_level, is_game_over
    if not is_displaying_pattern and not is_won_current_level and not is_game_over:
        light_led_for_button(channel)
        #if GPIO.input(channel) == GPIO.LOW:
        #print("Channel is: {}".format(channel))
        #print("Current step: {}".format(current_step_of_level))
        #print("Current pattern item is: {}".format(pattern[current_step_of_level]))
        if channel == BUTTONS[pattern[current_step_of_level]]:
            current_step_of_level += 1
            if current_step_of_level >= current_level:
                current_level += 1
                is_won_current_level = True
        else:
            is_game_over = True


def light_led_for_button(button_channel):
    led = LIGHTS[BUTTONS.index(button_channel)]
    #GPIO.output(led, GPIO.input(button_channel))
    GPIO.output(led, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(led, GPIO.LOW)


def add_new_color_to_pattern():
    global is_won_current_level, current_step_of_level
    is_won_current_level = False
    current_step_of_level = 0
    next_color = random.randint(0, 3)
    #print("Next color is: {}".format(next_color))
    pattern.append(next_color)


def display_pattern_to_player():
    global is_displaying_pattern
    is_displaying_pattern = True
    GPIO.output(LIGHTS, GPIO.LOW)
    for i in range(current_level):
        GPIO.output(LIGHTS[pattern[i]], GPIO.HIGH)
        time.sleep(speed)
        GPIO.output(LIGHTS[pattern[i]], GPIO.LOW)
        time.sleep(speed)
    is_displaying_pattern = False


def wait_for_player_to_repeat_pattern():
    while not is_won_current_level and not is_game_over:
        time.sleep(0.1)


def start_game():
    while True:
        add_new_color_to_pattern()
        display_pattern_to_player()
        wait_for_player_to_repeat_pattern()
        if is_game_over:
            print("\nGame Over! Your max score was {} colors!".format(current_level-1))
            break
        time.sleep(2)


def start_game_monitor():
    t = threading.Thread(target=start_game)
    t.daemon = True
    t.start()
    t.join()


def main():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Let the games begin!")
        initialize_gpio()
        start_game_monitor()
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
