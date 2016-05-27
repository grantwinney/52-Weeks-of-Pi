import RPi.GPIO as GPIO
import Gmail

CHECK_NOW_PIN = 12


def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Gmail.PIN, GPIO.OUT)
    GPIO.setup(CHECK_NOW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(CHECK_NOW_PIN, GPIO.RISING, callback=Gmail.refresh, bouncetime=1000)


#def check_all_mail_now(_):
#    Gmail.refresh()


def main():
    try:
        initialize_gpio()
        Gmail.start()
        raw_input("\nPress any key to exit.\n")
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
