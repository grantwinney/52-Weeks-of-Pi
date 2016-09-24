# Using an Analog Joystick to Display Colors on an RGB LED

This project demonstrates using pulse width modulation (PWM) to change the color of an RGB LED, as well as integrating analog controls with the Pi via specialized (inexpensive) hardware.

I used an MCP3008 analog-to-digital converter to connect a joystick to the Pi, thanks to some extremely _very_ helpful tutorials on the Raspberry Pi Spy site.

Then I took it a step further by using the joystick to "select" the color from an RGB color wheel, which I display with an RGB LED.

[Read more about the setup here](https://grantwinney.com/connecting-an-analog-joystick-to-the-raspberry-pi-and-using-it-with-an-rgb-led-to-simulate-a-color-wheel/), and then [check out everything I'm doing with the Pi](https://grantwinney.com/tag/52-weeks-of-pi/).

## To Run

`python3 joystick_color_wheel.py`

## Notes

There's a test file too. This was my first foray into writing Python unit tests, a habit I'd suggest every developer learn more about.

To run the test file, you'll need to install the [DDT (Data-Driven Tests) package for Python unit testing](https://technomilk.wordpress.com/2012/02/12/multiplying-python-unit-test-cases-with-different-sets-of-data/) via pip.
