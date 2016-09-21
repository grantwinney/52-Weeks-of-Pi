# Created by comments in spidev_module.c, in the py-spidev package
# available here -> https://github.com/doceme/py-spidev


def SpiDev():
    return SpiDevMock()


class SpiDevMock:
    def __init__(self):
        print("New instance of class created: {}".format(self))

    def open(self, bus, device):
        print("Connects the object to the specified SPI device. Will open /dev/spidev{}.{}".format(bus, device))

    def xfer2(self, values):
        print("Perform SPI transaction using [{}]. CS will be held active between blocks.".format(values))
        speed_hz = 0
        delay_usecs = 0
        bits_per_word = 0
        return speed_hz, delay_usecs, bits_per_word
