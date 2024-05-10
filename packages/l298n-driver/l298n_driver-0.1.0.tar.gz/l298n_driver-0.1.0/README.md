# L298N Driver Python Package

This package provides a Python interface for controlling the L298N H-Bridge Motor Driver.

## Prerequisites

This library requires the `sx1509_gpio_expander` library. You can install it using pip:

```sh
pip install sx1509_gpio_expander
```

## Installation

Install the package using pip:

```sh
pip install l298n-driver
```

## Usage

```python
from sx1509_gpio_expander import SX1509
from l298n_driver import L298N
import board

# Configure I2C
i2c = board.I2C() 

# Create an instance of the SX1509 GPIO expander
IOExpander0 = SX1509.SX1509(i2c, 0x3E)

# Create an instance of the L298N motor driver
# The parameters are the IO expander, and the pin numbers for motor input 1, motor input 2, and motor speed control
motor = L298N.L298N(IOExpander0, 1, 2, 3)

# Use the motor driver
# The smartDrive function sets the motor speed and direction simultaneously
# Just set the speed to a value between (-255-255) and the function will automatically call the set_speed() function and according to the given speed value also call the forward() or backward() function
motor.smartDrive(255)
```

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the [LICENSE](LICENSE) file for details.
