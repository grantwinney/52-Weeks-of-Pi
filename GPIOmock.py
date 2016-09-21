# Created by the comments in source/py_gpio.c, in the RPi.GPIO package
# available here -> https://pypi.python.org/pypi/RPi.GPIO
# or here -> https://github.com/Tieske/rpi-gpio/blob/master/source/py_gpio.c

HIGH = 1
LOW = 0

BCM = 'BroadCom Numbering'
BOARD = 'Board Numbering'

IN = '"In" Direction for Pin'
OUT = '"Out" Direction for Pin'

PUD_OFF = "Pull Up/Down Resitor Disabled"
PUD_UP = "Pull Up Resistor"
PUD_DOWN = "Pull Down Resistor"

RISING = "Rising Edge"
FALLING = "Falling Edge"
BOTH = "Rising and Falling Edges"


# Clean up by resetting all GPIO channels that have been used by this program to INPUT
#   with no pullup/pulldown and no event detection
# [channel] - individual channel or list/tuple of channels to clean up.
# Default - clean every channel that has been used."},
def cleanup(channel=None):
    print("Reset all GPIO channels (or channel {}) to INPUT with no pullup/pulldown and no event detection."
          .format(channel))


# Set up a GPIO channel or list of channels with a direction and (optional) pull/up down control
# channel        - either board pin number or BCM number depending on which mode is set.
# direction      - IN or OUT
# [pull_up_down] - PUD_OFF (default), PUD_UP or PUD_DOWN
# [initial]      - Initial value for an output channel
def setup(channels, direction, pull_up_down=PUD_OFF, initial=None):
    print("Setup channel(s) {} for direction {}, with pull_up_down {} and set to initial value {}"
          .format(channels, direction, pull_up_down, initial))


# Output to a GPIO channel or list of channels
# channel - either board pin number or BCM number depending on which mode is set.
# value   - 0/1 or False/True or LOW/HIGH
def output(channels, value):
    print("Output a {} value to channel(s) {}".format(value, channels))


# Input from a GPIO channel. Returns HIGH=1=True or LOW=0=False
# channel - either board pin number or BCM number depending on which mode is set.
def input(channel):
    print("Returns the current input value (HIGH or LOW) of channel {}".format(channel))


# Set up numbering mode to use for channels.
# BOARD - Use Raspberry Pi board numbers
# BCM   - Use Broadcom GPIO 00..nn numbers
def setmode(mode):
    print("Numbering style set to {} style".format(mode))


# Get numbering mode used for channel numbers.
# Returns BOARD, BCM or None
def getmode():
    print("Returns the numbering mode of BOARD, BCM or None")


# Add a callback for an event already defined using add_event_detect()
# channel      - either board pin number or BCM number depending on which mode is set.
# callback     - a callback function
def add_event_callback(gpio, callback):
    print("Also call {} when edge detected on channel {}".format(callback, gpio))


# Enable edge detection events for a particular GPIO channel.
# channel      - either board pin number or BCM number depending on which mode is set.
# edge         - RISING, FALLING or BOTH
# [callback]   - A callback function for the event (optional)
# [bouncetime] - Switch bounce timeout in ms for callback
def add_event_detect(gpio, edge, callback=None, bouncetime=None):
    print("Added event detection to PIN {} on edge {}. Call {} with minimal bounce time of {}."
          .format(gpio, edge, callback, bouncetime))


# Remove edge detection for a particular GPIO channel
# channel - either board pin number or BCM number depending on which mode is set.
def remove_event_detect(gpio):
    print("Edge detection removed for GPIO channel {}".format(gpio))


# Returns True if an edge has occurred on a given GPIO.
# You need to enable edge detection using add_event_detect() first.
# channel - either board pin number or BCM number depending on which mode is set.
def event_detected(channel):
    print("An event was detected on channel {}".format(channel))


# Wait for an edge.  Returns the channel number or None on timeout.
# channel      - either board pin number or BCM number depending on which mode is set.
# edge         - RISING, FALLING or BOTH
# [bouncetime] - time allowed between calls to allow for switch-bounce
# [timeout]    - timeout in ms
def wait_for_edge(channel, edge, bouncetime=None, timeout=None):
    print("Waiting for edge {} on channel {}, with a minimal time between calls of {} and a timeout of {}."
          .format(channel, edge, bouncetime, timeout))


# Return the current GPIO function (IN, OUT, PWM, SERIAL, I2C, SPI)
# channel - either board pin number or BCM number depending on which mode is set.
def gpio_function(channel):
    print("Returns the current GPIO function for channel {}".format(channel))


# Enable or disable warning messages
def setwarnings(state):
    print("Set warnings to {}".format(state))


def PWM(channel, frequency):
    return PwmMock(channel, frequency)


# Prints information about your Raspberry Pi
RPI_INFO = "{'P1_REVISION': -1, 'RAM': '-1M', 'REVISION': '-1', 'TYPE': 'Pi Model', 'PROCESSOR': 'Some Processor', 'MANUFACTURER': 'Some Mfr'}"

# Prints the version of RPi.GPIO
VERSION = "0.0.0"


class PwmMock:
    p_channel = 0

    def __init__(self, channel, frequency):
        global p_channel
        p_channel = channel
        print("New instance of class created: {}. Enables pulse-width modulation on channel {} at frequency {}".format(self, channel, frequency))

    def start(self, frequency):
        print("Start pulse-width modulation at {} for channel {}".format(frequency, p_channel))

    def ChangeDutyCycle(self, frequency):
        print("Set pulse-width modulation to {} for channel {}".format(frequency, p_channel))

    def stop(self):
        print("Stop pulse-width modulation on channel {}".format(p_channel))
