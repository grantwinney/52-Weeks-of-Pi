# Transmit Morse Code Via LED
This is a Python3 app for transmitting morse code via LED on-off blinks (or anything else you choose to connect to the GPIO pin).

There are three files of interest:

* Transmitter.py contains the main code that writes out dots and dashes for each morse code in the input sentence.

* InternationalMorseCode.py has a dictionary with all the letters, numbers and punctuation for which there are "international" morse code symbols. Makes for easy lookup.

* GPIOmock.py contains some functions that are named as the same as those needed from the RPi.GPIO package. In this "mock" file, they simply output a string message.

The "mock" GPIO script allows for development on a machine that is not the Raspberry Pi, and thus doesn't have the RPi.GPIO package installed.

## Using the RPi GPIO Library

When running this on the Pi, uncomment this line:

    # import RPi.GPIO as GPIO

And comment out the one after it:

    import GPIOmock as GPIO

## Other Settings

Before running on the app, you may want to make a few adjustments.

The speed of transmission can be adjusted via UNIT_TIME, which represents seconds (so .25 is a quarter-second).

    UNIT_TIME = .25

Depending on how you have your board setup, and where you're LED is, you may need to make adjustments to the pin (where your LED is located on the board), as well as the pin numbering system you prefer to use.

    PIN = 21

    GPIO.setmode(GPIO.BCM)

Set the following flag to False to cut down on some of the messages to the console. Personally, I found it helpful to know which letter was currently being transmitted.

    VERBOSE = True

## To Run

Run the Transmitter.py file. The following loop continues asking for input, and will end the app only when no input is specified (the message is left empty).

    while message != '':
        message = input('\nEnter a message to transmit, or leave blank to exit: ')
        transmit_sentence(message)

[Here's a video of me running the program and "sending" a few messages](https://www.youtube.com/watch?v=9kpA4cv_-uM).

## BreadBoard Setup

Here's how I setup the breadboard.

* Insert the anode side of an LED in pin 21 (broadcom numbering, or pin 40 if using board numbering).
* Insert the cathode side in an empty row next to it.
* Insert a resistor, connecting the empty row with the cathode side of the LED back to ground.

I used a cobbler. If you don't have one, then you'll have to wire up pin 21 bcm (pin 40 board) on the Pi to the anode side of the LED, and wire up ground back to a ground pin on the Pi.

![](https://github.com/grantwinney/MorseCode/blob/master/TransmitViaLed/breadboard-single-led-circuit.jpg)
