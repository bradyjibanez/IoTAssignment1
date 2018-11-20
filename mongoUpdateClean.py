from pymongo import MongoClient
from urllib.request import urlopen
from bson import ObjectId
import socket, datetime, pytz, sys, json, urllib, requests, Adafruit_DHT

class Update:

	makeUpJunk = 0
	MONGO_DB = "IoTI"
	CONNECTION = MongoClient()

	db = CONNECTION.IoTI
	ambientLightSensorData = db.AmbientLightSensorData

	def runUpdate(self, sensorCount, ambientLightSensorData, count, temperature, humidity):

		yourName = socket.gethostname()
		yourIP = socket.gethostbyname(yourName)
		response = urlopen("http://ip-api.com/json")
		userData = response.read().decode("utf-8")
		userDataJSON = json.loads(userData)
		headers = {'content-type': 'application/json'}

		url = "https://demo.thingsboard.io/api/v1/3mmZ09cG3cyrzFZku4BF/telemetry"
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json; charset=utf-8')

        lightStatus = "off"

        userCurrentTime = datetime.datetime.now(pytz.timezone(userDataJSON['timezone']))
        userCTimeString = userCurrentTime.strftime('%d/%m/%Y|%I:%M:%S')

        print(" ")

        temperature = str(temperature)
        humidity = str(humidity)

        if sensorCount > 1000:

            lightStatus = "on"
            post = {
                "author": yourName,
                "author IP": yourIP,
                "light status": lightStatus,
                "times updated": count,
                "date": userCTimeString,
                "Temperature": temperature,
                "Humidity": humidity
            }
            ambientLightSensorData.insert(post)
            count += 1

        else:
            lightStatus = "off"
            post = {
                "author": yourName,
                "author IP": yourIP,
                "light status": lightStatus,
                "times updated": count,
                "date": userCTimeString,
                "Temperature": temperature,
                "Humidity": humidity
            }
            ambientLightSensorData.insert(post)
            latestData = ambientLightSensorData.find_one({"Humidity": humidity, "Temperature": temperature, "times updated": count})
            count += 1
            latestData = JSONEncoder().encode(latestData)
            print(JSONEncoder().encode(latestData))
            print(latestData)


        jsondata = json.dumps(post)
        jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
        req.add_header('Content-Length', len(jsondataasbytes))
        print(jsondataasbytes)
        response = urllib.request.urlopen(req, jsondataasbytes)