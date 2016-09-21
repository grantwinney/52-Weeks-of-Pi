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

# Define RGB channels
red_led = 36
green_led = 31
blue_led = 37

# Center positions when joystick is at rest
center_x_pos = 530
center_y_pos = 504

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
    dx = x - center_x_pos
    dy = y - center_y_pos
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


def is_joystick_near_center(x, y):
    dx = math.fabs(x - center_x_pos)
    dy = math.fabs(y - center_y_pos)
    return dx < 20 and dy < 20


def main():
    pwm_r = GPIO.PWM(red_led, 300)
    pwm_g = GPIO.PWM(green_led, 300)
    pwm_b = GPIO.PWM(blue_led, 300)

    pwm_instances = [pwm_r, pwm_g, pwm_b]

    for p in pwm_instances:
        p.start(0)

    try:
        while True:
            # If joystick switch is pressed down, turn off LEDs
            switch = read_spi_data_channel(mcp3008_switch_channel)
            if (switch == 0):
                for p in pwm_instances:
                    p.ChangeDutyCycle(0)
                continue

            # Read the joystick position data
            x_pos = read_spi_data_channel(mcp3008_x_voltage_channel)
            y_pos = read_spi_data_channel(mcp3008_y_voltage_channel)

            # If joystick is at rest, turn on all LEDs (producing 'white')
            if is_joystick_near_center(x_pos, y_pos):
                for p in pwm_instances:
                    p.ChangeDutyCycle(100)
                continue

            # Adjust duty cycle of LEDs based on joystick position
            angle = convert_coordinates_to_angle(x_pos, y_pos)
            pwm_r.ChangeDutyCycle(interpret_angle_for_led(angle, 90))   # red
            pwm_g.ChangeDutyCycle(interpret_angle_for_led(angle, 330))  # green
            pwm_b.ChangeDutyCycle(interpret_angle_for_led(angle, 210))  # blue

            print("Coordinate : ({},{})  --  Angle : {}".format(x_pos, y_pos, angle))

    except KeyboardInterrupt:
        pass

    finally:
        for p in pwm_instances:
            p.stop()
        GPIO.cleanup()


if __name__ == '__main__':
    main()
