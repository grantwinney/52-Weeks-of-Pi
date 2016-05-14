HIGH = 1
LOW = 0

BCM = 'BroadCom Numbering'
BOARD = 'Board Numbering'

IN = '"In" Direction for Pin'
OUT = '"Out" Direction for Pin'


def output(pin, signal):
    print("Sent GPIO pin {} to {}".format(pin, _convert_signal_to_text(signal)))


def setmode(numbering_style):
    print("Numbering style set to {} style".format(numbering_style))


def setwarnings(set_warnings):
    print("Set warnings to {}".format(set_warnings))


def setup(pin, direction):
    print("Set {} {}".format(direction, pin))


def _convert_signal_to_text(signal):
    if signal == HIGH:
        return "HIGH"
    else:
        return "LOW"
