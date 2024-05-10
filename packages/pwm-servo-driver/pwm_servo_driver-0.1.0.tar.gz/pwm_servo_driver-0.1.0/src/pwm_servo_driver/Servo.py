"""
Python interface for PWM servo driver
This library provides an interface to control a servo using Pulse Width Modulation (PWM).
"""

import pwm_servo_driver.IO_Types as IO_Types

class Servo:

    
    def __init__(self, IOExpaner, servoPin):
        """
        Constructor for the Servo class.
        
        :param IOExpaner: An instance of the IO expander class.
        :param servoPin: The pin number for the servo.
        """
        
        self._IOExpander = IOExpaner
        self._servoPin = servoPin

        self._IOExpander.pinMode(self._servoPin, IO_Types.PIN_TYPE_ANALOG_OUTPUT)
        self._IOExpander.SetLEDClkDivider(7)

    def setPosition(self, angle): 
        """
        Set the position of the servo.
        
        :param angle: The desired angle (0-180).
        """
        if angle < 0 or 180 < angle:
            raise ValueError("Angle must be between 0 and 180")

        # Convert angle from range 0-180 to 20-80
        converted_angle = int((angle / 180) * 60) + 20

        self._IOExpander.analogWrite(self._servoPin, converted_angle)

    def reset(self, hardware = 0):
        """
        Turn off the Servo.
        Important at the end of each script.
        
        :param hardware: The hardware reset pin (default is 0).
        """
        self._IOExpander.reset(hardware)

    
        