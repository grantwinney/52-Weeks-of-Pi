HIGH = 1
LOW = 0

BCM = 'BroadCom Numbering'
BOARD = 'Board Numbering'

IN = '"In" direction'
OUT = '"Out" direction'


def output(pin, signal):
    print("Sent GPIO pin {} to {}".format(pin, _convert_signal_to_text(signal)))


def setmode(numbering_style):
    print("Numbering style set to {} style".format(numbering_style))


def setwarnings(set_warnings):
    print("Set warnings to {}".format(set_warnings))


def setup(pin, direction, initial):
    print("Set GPIO pin {} to {} and initialize to {}".format(pin, direction, initial))


def _convert_signal_to_text(signal):
    if signal == HIGH:
        return "HIGH"
    else:
        return "LOW"


def cleanup():
    print("Wash, rinse, repeat! GPIO all cleaned up.")
