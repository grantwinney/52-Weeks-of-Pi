# Send Morse Code Via Button Click
This is a Python script for accepting incoming signals (via a physical button that "closes" the circuit), and translating the input into morse code.

There are two files of interest:

* Transmitter.py contains the main code that interprets our dots and dashes, and outputs the translated letters.

* InternationalMorseCode.py has a dictionary with all the letters, numbers and punctuation for which there are "international" morse code symbols. Makes for easy lookup.

## Setup for Pi

You may want to make a few adjustments.

The length of time of one "beat" (i.e. a single "dot") can be adjusted via BASE_TIME_SECONDS, which represents seconds.

    BASE_TIME_SECONDS = 1.0
    
The tolerance can be adjusted via TOLERANCE. Exact timing is difficult. On the following line, I've stated a tolerance of 1/2 second. So instead of pressing the button for 1 sec for a dot or 3 sec for a dash, you're allowed 0.5 - 1.5 sec for a dot, and 2.5 - 3.5 sec for a dash.
    
    TOLERANCE = BASE_TIME_SECONDS / 2.0

Depending on how you have your board setup, you may want to adjust the pin numbers throughout the script.

## To Run

Run the Transmitter.py file.

I uploaded a [demo](https://www.youtube.com/watch?v=rpsq2FidA8U) if you're interested in seeing it work.
