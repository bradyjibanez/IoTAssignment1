import RPi.GPIO as GPIO
from mongoUpdate import Update
import urllib, http.client, time, sys, Adafruit_DHT
GPIO.setmode(GPIO.BOARD)

ambientSensorIO = 15
temperatureSensorIO = 7
update = Update()
ambientLightSensorData = update.ambientLightSensorData

def getLightReading(ambientSensorIO):
    chargeCount = 0

    GPIO.setup(ambientSensorIO, GPIO.OUT)
    GPIO.output(ambientSensorIO, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(ambientSensorIO, GPIO.IN)

    while (GPIO.input(ambientSensorIO) == GPIO.LOW):
        chargeCount += 1

#    GPIO.cleanup()
    return chargeCount

def getTemperatureHumidity(temperatureSensorIO):
     humidity, temperature = Adafruit_DHT.read_retry(11, 4)
#     temp, hum = .format(temperature,humidity)
     return temperature, humidity
try:

#    GPIO.setup(temperatureSensor, GPIO.IN)
    useCount = 1

    while True:
        charge = getLightReading(ambientSensorIO)
        temperature, humidity = getTemperatureHumidity(temperatureSensorIO)
#        humidity = str(str(humidity)+"%") use these if we want % and C in the mongoDB
#        temperature = str(str(temperature)+"C")

        if charge > 10000:
            update.runUpdate(charge, ambientLightSensorData, useCount, temperature, humidity)
            print(charge, "green on")
            greenOff = urllib.request.urlopen("http://192.168.0.59/?cmd=TURN_ON_GREEN")
            useCount += 1
        else:
            update.runUpdate(charge, ambientLightSensorData, useCount, temperature, humidity)
            print(charge, "green off")
            greenOn = urllib.request.urlopen("http://192.168.0.59/?cmd=TURN_OFF_GREEN")
            useCount += 1
#        humidity, temperature = Adafruit_DHT.read_retry(11, 4)
#        print('Temp: {0:0.1f} C Humidity: {1:0.1f} %'.format(temperature,humidity))
#        print(temperature, humidity)
except KeyboardInterrupt:
    pass
#except httplib.BadStatusLine:
#    checker = rc_time(pin_to_circuit)
finally:
    GPIO.cleanup()
