# What is charlieplexing? (a demo on the Raspberry Pi)

These scripts help demonstrate a concept called "charlieplexing", which is arranging LEDs in such a way as to minimize the number of GPIO pins required to make them light up.

It's easy to demonstrate with only 2 pins, but you only start seeing benefits when you use 3 or more - the exact number of LEDs supported by `x` number of GPIO pins is `x² - x`.

[Read more about the setup]() or just [watch the demo](https://www.youtube.com/watch?v=GXnijBPWMEc), then [check out other stuff I'm doing with the Pi](https://grantwinney.com/tag/52-weeks-of-pi/).

## To Run

    python3 charlieplexing-2-on-2.py   # demo using 2 LEDs on 2 GPIO pins
    
    python3 charlieplexing-6-on-3.py   # demo using 6 LEDs on 3 GPIO pins
