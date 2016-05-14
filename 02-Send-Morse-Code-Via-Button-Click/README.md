# Send Morse Code Via Button Click
This is a Python3 script for accepting incoming signals (via a physical button that "closes" the circuit), and translating the input into morse code.

There are three files of interest:

* Transmitter.py contains the main code that writes out dots and dashes for each morse code in the input sentence.

* InternationalMorseCode.py has a dictionary with all the letters, numbers and punctuation for which there are "international" morse code symbols. Makes for easy lookup.

* GPIOmock.py contains some functions that are named as the same as those needed from the RPi.GPIO package. In this "mock" file, they simply output a string message.

The "mock" GPIO script allows for development on a machine that is not the Raspberry Pi, and thus doesn't have the RPi.GPIO package installed.

## When Running on a Raspberry Pi...

Uncomment this line:

    # import RPi.GPIO as GPIO

And comment out the one after it:

    import GPIOmock as GPIO

## Setup for Pi

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