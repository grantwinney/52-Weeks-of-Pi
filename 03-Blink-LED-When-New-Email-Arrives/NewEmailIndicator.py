import RPi.GPIO as GPIO
import Gmail

YAHOO_PIN = 32
MSOFT_PIN = 36
CHECK_NOW_PIN = 12


def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([Gmail.PIN, YAHOO_PIN, MSOFT_PIN], GPIO.OUT)
    GPIO.setup(CHECK_NOW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(CHECK_NOW_PIN, GPIO.RISING, callback=check_all_mail_now, bouncetime=1000)


def check_all_mail_now(_):
    Gmail.refresh()


def main():
    try:
        initialize_gpio()

        Gmail.start()
        Outlook.start()
        #Yahoo.start()

        raw_input("\nPress any key to exit.\n")

    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
