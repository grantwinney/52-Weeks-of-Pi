import RPi.GPIO as GPIO
#import GPIOmock as GPIO
import threading
import time
import random
import sys
import os
from subprocess import call

# green, red, blue, yellow
LIGHTS = [33, 37, 35, 31]
BUTTONS = [11, 15, 13, 7]
NOTES = ["E3", "A4", "E4", "Cs4"]

# values you can change that affect game play
speed = 0.25
use_sounds = True

# flags used to signal game status
is_displaying_pattern = False
is_won_current_level = False
is_game_over = False

# game state
current_level = 1
current_step_of_level = 0
pattern = []


def play_note(note):
    if use_sounds:
        call(["sonic_pi", "play :" + note])


def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LIGHTS, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    for i in range(4):
        GPIO.add_event_detect(BUTTONS[i], GPIO.FALLING, callback=verify_player_selection, bouncetime=400 if use_sounds else 250)


def verify_player_selection(channel):
    global current_step_of_level, current_level, is_won_current_level, is_game_over
    if not is_displaying_pattern and not is_won_current_level and not is_game_over:
        play_note(NOTES[BUTTONS.index(channel)])
        flash_led_for_button(channel)
        if channel == BUTTONS[pattern[current_step_of_level]]:
            current_step_of_level += 1
            if current_step_of_level >= current_level:
                current_level += 1
                is_won_current_level = True
        else:
            is_game_over = True


def flash_led_for_button(button_channel):
    led = LIGHTS[BUTTONS.index(button_channel)]
    GPIO.output(led, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(led, GPIO.LOW)


def add_new_color_to_pattern():
    global is_won_current_level, current_step_of_level
    is_won_current_level = False
    current_step_of_level = 0
    next_color = random.randint(0, 3)
    pattern.append(next_color)


def display_pattern_to_player():
    global is_displaying_pattern
    is_displaying_pattern = True
    GPIO.output(LIGHTS, GPIO.LOW)
    for i in range(current_level):
        play_note(NOTES[pattern[i]])
        GPIO.output(LIGHTS[pattern[i]], GPIO.HIGH)
        time.sleep(speed)
        GPIO.output(LIGHTS[pattern[i]], GPIO.LOW)
        time.sleep(speed)
    is_displaying_pattern = False


def wait_for_player_to_repeat_pattern():
    while not is_won_current_level and not is_game_over:
        time.sleep(0.1)


def reset_board_for_new_game():
    global is_displaying_pattern, is_won_current_level, is_game_over
    global current_level, current_step_of_level, pattern
    is_displaying_pattern = False
    is_won_current_level = False
    is_game_over = False
    current_level = 1
    current_step_of_level = 0
    pattern = []
    GPIO.output(LIGHTS, GPIO.LOW)


def start_game():
    while True:
        add_new_color_to_pattern()
        display_pattern_to_player()
        wait_for_player_to_repeat_pattern()
        if is_game_over:
            print("Game Over! Your max score was {} colors!\n".format(current_level-1))
            play_again = input("Enter 'Y' to play again, or just press [ENTER] to exit.\n")
            if play_again == "Y" or play_again == "y":
                reset_board_for_new_game()
                print("Begin new round!\n")
            else:
                print("Thanks for playing!\n")
                break
        time.sleep(2)


def start_game_monitor():
    t = threading.Thread(target=start_game)
    t.daemon = True
    t.start()
    t.join()


def main():
    try:
        call(["sonic_pi", "set_sched_ahead_time! 0"])
        call(["sonic_pi", "use_debug false"])
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Begin new round!\n")
        initialize_gpio()
        start_game_monitor()
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
