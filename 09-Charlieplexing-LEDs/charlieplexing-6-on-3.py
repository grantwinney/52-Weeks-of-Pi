import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

PINS = [23, 24, 25]

H = 1
L = 0
O = -1

LEDS = [[L, O, H],
        [H, O, L],
        [O, L, H],
        [L, H, O],
        [O, H, L],
        [H, L, O]]

def main():
    try:
        while True:
            for led in LEDS:
                for idx, pin in enumerate(led):
                    if pin == O:
                        GPIO.setup(PINS[idx], GPIO.IN)
                    else:
                        GPIO.setup(PINS[idx], GPIO.OUT)
                        GPIO.output(PINS[idx], pin)
                time.sleep(.1)
            
    except KeyboardInterrupt:
        pass

    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
