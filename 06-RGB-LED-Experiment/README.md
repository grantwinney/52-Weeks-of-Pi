# RGB LED Experiment

I've been meaning to devote some time to learning how these RGB LEDs work, so this week is just a little experimenting with it, and getting it to randomly cycle through the different color combinations.

[Read more about the setup here](https://grantwinney.com/how-to-use-an-rgb-multicolor-led-with-pulse-width-modulation-pwm-on-the-raspberry-pi/), and then [check out everything I'm doing with the Pi](https://grantwinney.com/tag/52-weeks-of-pi/).

## To Run

The RgbLed.py file cycles through colors. Run it using: `python3 RgbLed.py`

The RgbLedPwm.py file cycles through colors too, but uses PWM (pulse-width modulation) to do so very smoothly.

## Notes

The pins for each color are listed at the top of each script. Change as necessary.
