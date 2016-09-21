import math
import RPi.GPIO as GPIO
import spidev
import threading
import time

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)

# Define sensor channels (3 to 7 are unused)
mcp3008_switch_channel = 0
mcp3008_x_voltage_channel = 1
mcp3008_y_voltage_channel = 2

# Define delay between readings (s)
delay = 0.01

# Define RGB channels
red_led = 36
green_led = 31
blue_led = 37

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup([red_led, green_led, blue_led], GPIO.OUT, initial=GPIO.LOW)


# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def read_spi_data_channel(channel):
    """
    :param channel: integer
    :return:
    """
    adc = spi.xfer2([1, (8+channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


def convert_coordinates_to_angle(x, y):
    dx = x - 512
    dy = y - 512
    rads = math.atan2(-dy, dx)
    rads %= 2 * math.pi
    return math.degrees(rads)


def adjust_angle_for_perspective_of_current_led(angle, led_peak_angle):
    return ((angle - led_peak_angle) + 360) % 360


def interpret_angle_for_led(angle, led_peak_angle):
    angle = adjust_angle_for_perspective_of_current_led(angle, led_peak_angle)
    if 120 < angle < 240:
        return 0
    elif angle <= 120:
        return 100 - (angle * (100/120))
    else:
        return 100 - ((360 - angle) * (100/120))


def main():
    pwm_r = GPIO.PWM(red_led, 300)
    pwm_g = GPIO.PWM(green_led, 300)
    pwm_b = GPIO.PWM(blue_led, 300)

    for p in [pwm_r, pwm_g, pwm_b]:
        p.start(100)

    try:
        while True:
            # Read the joystick position data
            vrx_pos = read_spi_data_channel(mcp3008_x_voltage_channel)
            vry_pos = read_spi_data_channel(mcp3008_y_voltage_channel)
            angle = convert_coordinates_to_angle(vrx_pos, vry_pos)

            pwm_r.ChangeDutyCycle(interpret_angle_for_led(angle, 90))
            pwm_g.ChangeDutyCycle(interpret_angle_for_led(angle, 330))
            pwm_b.ChangeDutyCycle(interpret_angle_for_led(angle, 210))

            # Read switch state
            swt_val = read_spi_data_channel(mcp3008_switch_channel)

            # Print out results
            # print("--------------------------------------------")
            # print("X : {}  Y : {}  Switch : {}".format(vrx_pos, vry_pos, swt_val))

            # Wait before repeating loop
            # time.sleep(delay)

    except KeyboardInterrupt:
        pass

    finally:
        for p in [pwm_r, pwm_g, pwm_b]:
            p.stop()
        GPIO.cleanup()


if __name__ == '__main__':
    main()
