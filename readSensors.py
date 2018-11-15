import RPi.GPIO as GPIO
from mongoTest import Update
import urllib, http.client, time

GPIO.setmode(GPIO.BOARD)

ambientSensorIO = 7

update = Update()
ambientLightSensorData = update.ambientLightSensorData

def rc_time (ambientSensorIO):
    chargeCount = 0

    GPIO.setup(ambientSensorIO, GPIO.OUT)
    GPIO.output(ambientSensorIO, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(ambientSensorIO, GPIO.IN)

    while (GPIO.input(ambientSensorIO) == GPIO.LOW):
        chargeCount += 1

    return chargeCount

try:

    useCount = 1

    while True:
        charge = rc_time(ambientSensorIO)
        if charge > 10000:
            update.runUpdate(charge, ambientLightSensorData, useCount)
            print(charge, "green on")
            greenOff = urllib.request.urlopen("http://192.168.0.59/?cmd=TURN_ON_GREEN")
            useCount += 1
        else:
            update.runUpdate(charge, ambientLightSensorData, useCount)
            print(charge, "green off")
            greenOn = urllib.request.urlopen("http://192.168.0.59/?cmd=TURN_OFF_GREEN")
            useCount += 1

except KeyboardInterrupt:
    pass
#except httplib.BadStatusLine:
#    checker = rc_time(pin_to_circuit)
finally:
    GPIO.cleanup()
