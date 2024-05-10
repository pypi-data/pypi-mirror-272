"""
Python interface for l298n h-bridge motor driver
Various useful variables used in the L298N functions
"""

#Pin types
PIN_TYPE_INPUT = 0x00
PIN_TYPE_OUTPUT = 0x01
PIN_TYPE_INPUT_PULLUP = 0x02
PIN_TYPE_ANALOG_OUTPUT = 0x03
PIN_TYPE_INPUT_PULLDOWN = 0x04
PIN_TYPE_INPUT_OPEN_DRAIN = 0x05

#Interrupt states
INTERRUPT_STATE_CHANGE = 0b11
INTERRUPT_STATE_FALLING = 0b10
INTERRUPT_STATE_RISING = 0b01
