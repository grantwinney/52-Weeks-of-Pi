# 52 Weeks of Pi
I read about Shekhar Gulati's "52 technologies in 2016" idea, where he's learning something new and posting it to GitHub every week. You can see what he's up to [here](https://github.com/shekhargulati/52-technologies-in-2016).

Inspired by his goal, I've decided to set my own goal of 52 Pi projects over the next year, since I've been trying to get more familiar with it. That doesn't mean they'll be big or anything... I'm going for consistent learning more than anything else.

1. **Transmit Morse Code Via LED**: A Python script for translating input (via the keyboard) into morse code, and transmitting it via on-off LED blinks (or anything else you connect to a GPIO pin).

2. **Send Morse Code Via Button Click**: A Python script for accepting incoming signals (via a button on the bread board that "closes" the circuit), and translating the input into morse code.

3. **Blink LED When New Email Arrives**: Authenticates to your Gmail account, then polls your unread message account via their API every xx seconds. When unread mail arrives, an LED blinks. When you mark it read, the LED turns off.

4. **Sonic Pi Grandfather Clock**: Checks the time at some regular interval (default is 10 seconds), playing the [Westminster Quarters](https://en.wikipedia.org/wiki/Westminster_Quarters) at each quarter-hour.

5. **Simon Clone**: A clone of the Simon pattern-matching game from the 80's.

6. **RGB / LED Experiment**: Experimenting with an RGB LED, getting it to randomly cycle through different color combinations.

## Mocking RPi.GPIO

The "mock" GPIOmock.py script allows for development on a machine that is not the Raspberry Pi, and thus doesn't have the RPi.GPIO package installed. It just outputs a message to the console that indicates its usage. I created it by referencing the comments available in the source/py_gpio.c file in the [RPi.GPIO module](https://pypi.python.org/pypi/RPi.GPIO), also available on [GitHub](https://github.com/Tieske/rpi-gpio/blob/master/source/py_gpio.c).

Copy the file into the same directory as any of the above scripts, then comment out the `import RPi.GPIO` line:

    # import RPi.GPIO as GPIO

And add this line after it:

    import GPIOmock as GPIO

## Issues? Errors? Comments?

If you notice a typo or something that's blatantly wrong, I'd appreciate pull requests with fixes. I don't know much about the Pi yet, and the last thing I want to do is steer someone wrong...

Alternatively, feel free to post an issue if you want to bring something in here to my attention. Thanks!
