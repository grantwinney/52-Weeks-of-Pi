import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

PIN_A = 24
PIN_B = 25

def main():
    try:
        GPIO.setup(PIN_A, GPIO.OUT, initial=1)
        GPIO.setup(PIN_B, GPIO.OUT, initial=0)
        
        while True:
            GPIO.output(PIN_A, not GPIO.input(PIN_A))
            GPIO.output(PIN_B, not GPIO.input(PIN_B))
            time.sleep(.01)
            
    except KeyboardInterrupt:
        pass

    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
