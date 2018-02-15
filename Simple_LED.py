import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)

# num = input('Enter how many times to turn LED on: ')
num = 15
# print "LED on"
for x in range(0, int(num)):
    GPIO.output(18, GPIO.HIGH)
    time.sleep(.5)
    GPIO.output(18, GPIO.LOW)
    time.sleep(.5)
print("done")
