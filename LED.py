# RJ Wakefield-Carl
# LED as Light Sensor
# Date: February 11, 2018
#
# Description:
#  Demonstration of how to use an LED as a light sensors. Shine
#  light on LED plugged into pin 20/21 to light up the output LED
#  plugged into pin 18. Note that you might have to change the
#  THRESHOLD parameter.
#
# Hardware Connections:
#  Pin | LED In 1 | LED 1
#  ----|----------|------
#   21 |     +    |
#   20 |     -    |
#   18 |          |   +
#
#  You will also need to connect the - sides of the output
#  LED through a 330 Ohm resistor to ground.

import RPi.GPIO as GPIO
import pigpio

pi = pigpio.pi()

# Any reading over this value will turn on the output LED
THRESHOLD = 30

# Stop counting after this value (we can assume it is total darkness)
MAX_T = 1000

# Pin definitions
P_JNCT_PIN = 21  # P junction of sensing LED
N_JNCT_PIN = 20  # N junction of sensing LED
OUT_LED_PIN = 18  # Output LED pin (P junction pin)


def setup():
    # Set up GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Set P juction pin to output low (GND)
    GPIO.setup(P_JNCT_PIN, GPIO.OUT)
    GPIO.output(P_JNCT_PIN, GPIO.LOW)

    # Set output LED pin to output
    GPIO.setup(OUT_LED_PIN, GPIO.OUT)

    return


def loop():
    # Read the amount of light falling on the LED
    readLED()

    # Print out the raw discharge time
    print(sen_time)

    # If the light is above a certain level (discharge time
    # is under the threshold), turn on the output LED
    if sen_time < THRESHOLD:
        GPIO.output(OUT_LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(OUT_LED_PIN, GPIO.LOW)
    return


def readLED():
    t = 0

    global sen_time  # Time it takes to discharge LED
    sen_time = 0  # Reset global LED discharge time

    # Apply reverse voltage to charge the sensing LED's capacitance
    GPIO.setup(N_JNCT_PIN, GPIO.OUT)
    GPIO.output(N_JNCT_PIN, GPIO.HIGH)

    # Isolate N junction and turn off pull-up resistor
    # GPIO.output(N_JNCT_PIN, GPIO.LOW)
    GPIO.setup(N_JNCT_PIN, GPIO.IN)

    # Count how long it takes for the LED to discharge
    for y in range(0, MAX_T):
        # if GPIO.input(N_JNCT_PIN) == 0:
        if pi.read(N_JNCT_PIN) == 0:
            x = 1
            break
        t += 1
        sen_time = t
        # print sen_time
    return


setup()
x = 1
while x > 0:
    loop()
