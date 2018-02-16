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
#
# Note: must have pigpio installed
# http://abyz.me.uk/rpi/pigpio/index.html

import RPi.GPIO as GPIO
import time
# import pigpio

# pi = pigpio.pi()

# Any reading under this value will turn on the output LED
THRESHOLD = 5000

# Stop counting after this value (we can assume it is total darkness)
MAX_T = 6000

# Pin definitions
P_JNCT_PIN = 21  # P junction of sensing LED
N_JNCT_PIN = 20  # N junction of sensing LED
OUT_LED_PIN = 18  # Output LED pin (P junction pin)

# List
list = []


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

    # Return the raw discharge time
    return(sen_time)

    # If the light is above a certain level (discharge time
    # is under the threshold), turn on the output LED
    # if sen_time < THRESHOLD:
    #     GPIO.output(OUT_LED_PIN, GPIO.HIGH)
    # else:
    #     GPIO.output(OUT_LED_PIN, GPIO.LOW)
    # return


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
    for x in range(0, MAX_T):
        if GPIO.input(N_JNCT_PIN) == 0:
            # if pi.read(N_JNCT_PIN) == 0:
            break
        t += 1
        sen_time = t
        # print sen_time
    return


def receivebinary():
    timestep = .5
    x = 1
    while loop() > THRESHOLD:
        pass
    while x < 30:
        print(loop())
        if loop() < THRESHOLD:
            list.append(1)
        else:
            list.append(0)
        x += 1
        time.sleep(timestep)
    print(list[:])


def receivemorse():
    DOT = "."
    DASH = "-"

    key_down_time = 0
    key_down_length = 0
    key_up_time = 0

    end_time = 1.5
    dot_length = 0.5
    space_length = .25

    # Wait for input
    while loop() > THRESHOLD:
        pass

    x = True
    while x:
        init_time = time.time()
        y = True
        while loop() > THRESHOLD:
            if time.time() - init_time > space_length and y:
                list.append(" ")
                y = False
        # record the time when the key went down
        key_down_time = time.time()
        while loop() < THRESHOLD:
            wait_time = time.time()
            if (wait_time - key_down_time) > end_time:
                x = False
                break
        # record the time when the key was released
        key_up_time = time.time()
        # get the length of time it was held down for
        key_down_length = key_up_time - key_down_time
        print(key_down_length)
        if key_down_length > dot_length and key_down_length < end_time:
            list.append(DASH)
        elif key_down_length < dot_length:
            list.append(DOT)


encoding = {
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    # Seen in use on the uncyclopedia:
    "'": '.----.'}
decoding = {}
for key, val in encoding.items():
    decoding[val] = key


def encode(text):
    # should really pre-process {'.': 'stop', ',': 'comma', '-': 'dash', ...}
    return ' '.join(map(lambda x, g=encoding.get: g(x, ' '), text.upper()))


def decode(message):
    ans = ''.join(map(lambda x, g=decoding.get: g(x, ' '), message.split(' ')))
    return ' '.join(ans.split())  # tidy up spacing


def decipher(message):
    # like decode, but when there are no spaces.
    row = [('', message)]
    while filter(lambda x: x[1], row):
        old = row
        row = []
        for it in old:
            txt, code = it
            if code:
                for (t, c) in encoding.items():
                    if code[:len(c)] == c:
                        row.append((txt + t, code[len(c):]))
                # NB we discard it if no initial segment of code matches an encoding.
            else:
                row.append(it)

    return map(lambda it: it[0], row)


def returnmsg(message):
    for x in message:
        if x == ".":
            GPIO.output(OUT_LED_PIN, GPIO.HIGH)
            time.sleep(.1)
            GPIO.output(OUT_LED_PIN, GPIO.LOW)
        elif x == "-":
            GPIO.output(OUT_LED_PIN, GPIO.HIGH)
            time.sleep(.3)
            GPIO.output(OUT_LED_PIN, GPIO.LOW)
        elif x == " ":
            time.sleep(.8)
        time.sleep(.3)

setup()
receivemorse()
print(list[:])
message = ""
for x in list:
    message = message + x
print(decode(message))
returnmsg(message)
