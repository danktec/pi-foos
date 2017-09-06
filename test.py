import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)


for i in range(9999):
    print "on %s" % i
    GPIO.output(23, GPIO.HIGH)
    time.sleep(1)
    print "off"
    GPIO.output(23, GPIO.LOW)
    time.sleep(1)

GPIO.cleanup()
