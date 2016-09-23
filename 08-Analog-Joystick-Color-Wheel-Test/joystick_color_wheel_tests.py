import unittest
import joystick_color_wheel as jcw
from ddt import ddt, data, unpack


@ddt
class JoystickColorWheelTests(unittest.TestCase):

    @data((530, 504, 530, 0, 90),         # center x-axis, top y-axis
          (530, 504, 530, 1023, 270),     # center x-axis, bottom y-axis
          (530, 504, 0, 504, 180),        # left x-axis, center y-axis
          (530, 504, 1023, 504, 0),       # right x-axis, center y-axis
          (530, 504, 0, 0, 135),          # left x-axis, top y-axis
          (530, 504, 0, 1023, 225),       # left x-axis, bottom y-axis
          (530, 504, 1023, 1023, 315),    # right x-axis, bottom y-axis

          (530, 504, 590, 564, 315),      # making sure the angle is the same
          (530, 504, 650, 624, 315),      # even if the joystick position is
          (530, 504, 1030, 1004, 315),    # not on one of the extreme edges

          (530, 504, 530, 504, 0))        # dead-center position
    @unpack
    def test_convert_coordinates_to_angle(self, center_x_pos, center_y_pos, x, y, expected_angle):
        self.assertAlmostEqual(expected_angle, jcw.convert_coordinates_to_angle(x, y, center_x_pos, center_y_pos), delta=2)

    @data((210, 'R', 120),    # Adjust angle for red while joystick position is on blue
          (330, 'R', 240),    # Adjust angle for red while joystick position is on green
          (90, 'G', 120),     # Adjust angle for green while joystick position is on red
          (210, 'G', 240),    # Adjust angle for green while joystick position is on blue
          (90, 'B', 240),     # Adjust angle for blue while joystick position is on red
          (330, 'B', 120),    # Adjust angle for blue while joystick position is on green

          (90, 'R', 0),       # Adjust angle for red while joystick position is on red
          (210, 'B', 0),      # Adjust angle for blue while joystick position is on blue
          (330, 'G', 0))      # Adjust angle for green while joystick position is on green
    @unpack
    def test_adjust_angle_for_perspective_of_current_led(self, angle, led_peak_angle, expected_adj_angle):
        self.assertEqual(expected_adj_angle, jcw.adjust_angle_for_perspective_of_current_led(angle, led_peak_angle))

    @data((210, 'R', 0),      # Duty cycle for red, joystick position on blue
          (330, 'R', 0),      # Duty cycle for red, joystick position on green
          (90, 'B', 0),       # Duty cycle for blue, joystick position on red
          (330, 'B', 0),      # Duty cycle for blue, joystick position on green
          (210, 'G', 0),      # Duty cycle for green, joystick position on blue
          (90, 'G', 0),       # Duty cycle for green, joystick position on red

          (90, 'R', 100),     # Duty cycle for red, joystick position directly on red
          (210, 'B', 100),    # Duty cycle for blue, joystick position directly on blue
          (330, 'G', 100)     # Duty cycle for green, joystick position directly on green
          )
    @unpack
    def test_calculate_next_pwm_duty_cycle_for_led(self, angle, led_peak_angle, expected_pwm_duty_cycle):
        self.assertEqual(expected_pwm_duty_cycle, jcw.calculate_next_pwm_duty_cycle_for_led(angle, led_peak_angle))

    @data((530, 504, 510, 484, False),       # Position just outside of range
          (530, 504, 510.1, 484.1, True),    # Position just inside of range
          (530, 504, 0, 0, False),           # Position way outside of range in upper-left
          (530, 504, 1024, 1024, False),     # Position way outside of range in lower-right
          (530, 504, 530, 504, True))        # Position exactly in center
    @unpack
    def test_is_joystick_near_center(self, center_x_pos, center_y_pos, x, y, expected_result):
        self.assertEqual(jcw.is_joystick_near_center(x, y, center_x_pos, center_y_pos), expected_result)
