import RPi.GPIO as GPIO
import spidev
import threading
import time
import os

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Define sensor channels
# (channels 3 to 7 unused)
swt_channel = 0  # switch
vrx_channel = 1  # x voltage
vry_channel = 2  # y voltage

# Define delay between readings (s)
delay = 0.01

# Define RGB channels
red = 36
green = 31
blue = 37

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup([red, green, blue], GPIO.OUT, initial=GPIO.LOW)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

# An array to hold instances of GPIO.PWM for later cleanup
pwms = []

# Function to adjust the red LED according to the joystick position
def red_light():
  p = GPIO.PWM(red, 300)
  p.start(100)
  pwms.append(p)
  while True:
    p.ChangeDutyCycle(100 if ReadChannel(vry_channel) <= 507 else 0)

# Function to adjust the green LED according to the joystick position
def green_light():
  p = GPIO.PWM(green, 300)
  p.start(100)
  pwms.append(p)
  while True:
    p.ChangeDutyCycle(100 if ReadChannel(vrx_channel) >= 512 and ReadChannel(vry_channel) >= 507 else 0)

# Function to adjust the blue LED according to the joystick position
def blue_light():
  p = GPIO.PWM(blue, 300)
  p.start(100)
  pwms.append(p)
  while True:
    p.ChangeDutyCycle(100 if ReadChannel(vrx_channel) <= 512 and ReadChannel(vry_channel) >= 507 else 0)

threads = [
  threading.Thread(target=red_light),
  threading.Thread(target=green_light),
  threading.Thread(target=blue_light)
]

for t in threads:
  t.daemon = True
  t.start()  

try:
  while True:
    # Read the joystick position data
    vrx_pos = ReadChannel(vrx_channel)
    vry_pos = ReadChannel(vry_channel)

    # Read switch state
    swt_val = ReadChannel(swt_channel)

    # Print out results
    # print("--------------------------------------------")
    # print("X : {}  Y : {}  Switch : {}".format(vrx_pos, vry_pos, swt_val))

    # Wait before repeating loop
    # time.sleep(delay)

except KeyboardInterrupt:
  pass

finally:
  for p in pwms:
    p.stop()
  GPIO.cleanup()
