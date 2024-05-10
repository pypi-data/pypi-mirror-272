"""
Python interface for l298n h-bridge motor driver
This library provides an interface to a L298N.
"""

import l298n_driver.IO_Types as IO_Types

class L298N:

    
    def __init__(self, IOExpaner, pinMotorIN1, pinMotorIN2, pinMotorSpeed):
        """
        Constructor for the L298N motor driver class.
        
        :param IOExpaner: An instance of the IO expander class.
        :param pinMotorIN1: The pin number for motor input 1.
        :param pinMotorIN2: The pin number for motor input 2.
        :param pinMotorSpeed: The pin number for motor speed control.
        """
        
        self._IOExpander = IOExpaner
        self._pinMotorIN1 = pinMotorIN1
        self._pinMotorIN2 = pinMotorIN2
        self._pinMotorSpeed = pinMotorSpeed
        self._motorIsSpinning = False
        self._speed = 0

        self._IOExpander.pinMode(self._pinMotorIN1, IO_Types.PIN_TYPE_OUTPUT)
        self._IOExpander.pinMode(self._pinMotorIN2, IO_Types.PIN_TYPE_OUTPUT)
        self._IOExpander.pinMode(self._pinMotorSpeed, IO_Types.PIN_TYPE_ANALOG_OUTPUT)
        self._IOExpander.pinMode(15,IO_Types.PIN_TYPE_OUTPUT)
        self._IOExpander.digitalWrite(15,1)

    def getSpeed(self):
        """
        Returns the current set speed (8 bit value -> 0-255).
        """
        return self._speed

    def set_speed(self, speed):
        """
        Set the motor speed (8bit value -> 0-255).
        Note: This function only changes the variable's value, but does not automatically apply the new speed to the motor!
        Therefore, you have to call forward() or backward() to apply the new speed to the actual motor.
        
        :param speed: The desired speed (0-255).
        """
        # Scale the speed value to match the 12V limit (12/16.8 of the input speed)
        self._speed = int((12/16.8) * speed)

    def forward(self):
        """
        By calling this function, the motor will spin forward with the speed set by the setSpeed() function.
        """
        self._motorIsSpinning = True if self._speed > 0 else False

        self._IOExpander.digitalWrite(self._pinMotorIN1,0)    # set IN pins differently to set one of the 2 spinning directions. Since forward and backward directions do depend on the motors connection, I've defined HIGH, LOW as forward :)
        self._IOExpander.digitalWrite(self._pinMotorIN2,1) 
        self._IOExpander.analogWrite(self._pinMotorSpeed, self._speed)  # set the motors speed via the SX1509 PWM modulation    

    def backward(self):
        """
        By calling this function, the motor will spin backward with the speed set by the setSpeed() function.
        """
        self._motorIsSpinning = True if self._speed > 0 else False

        self._IOExpander.digitalWrite(self._pinMotorIN1,1)  # set IN pins differently to set one of the 2 spinning directions. Here I've set IN1 and IN2 to the exact opposite as in the forward() function to let the motor spin in the opposite direction :)
        self._IOExpander.digitalWrite(self._pinMotorIN2,0)
        self._IOExpander.analogWrite(self._pinMotorSpeed, self._speed)  # set the motors speed via the Arduinos PWM modulation

    def set_direction(self, direction):
        """
        Set the motor direction.
        
        :param direction: The desired direction ("FORWARD" or "BACKWARD").
        """
        if direction == "FORWARD":
            self.forward()
        elif direction == "BACKWARD":
            self.backward()

    def smartDrive(self, speed):
        """
        Set the motor speed and direction simultaneously.
        Just set the speed to a value between (-255-255) and the function will automatically call the set_speed() function and according to the given speed value also call the forward() or backward() function.
        
        :param speed: The desired speed (-255 to 255).
        """
        self.set_speed(abs(speed))  # set the objects speed variable (always positive)

        if speed >= 0:
            self.forward()
        else:
            self.backward()

    def stop(self):
        """
        Stop the motor by setting its speed to 0.
        """
        self._speed = 0
        self._motorIsSpinning = False
        self._IOExpander.digitalWrite(self._pinMotorIN1,0)
        self._IOExpander.digitalWrite(self._pinMotorIN2,0)
        self._IOExpander.analogWrite(self._pinMotorSpeed, 255)
        self._IOExpander.digitalWrite(15,0)

    def is_motor_spinning(self):
        """
        Returns the current state of the motor.
        """
        return self._motorIsSpinning

        