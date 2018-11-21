from pymongo import MongoClient
from urllib.request import urlopen
import urllib.error, contextlib
from bson import ObjectId
import socket, datetime, pytz, sys, json, urllib, requests, Adafruit_DHT

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

class Update:

	makeUpJunk = 0
	MONGO_DB = "IoTI"
	CONNECTION = MongoClient()

	db = CONNECTION.IoTI
	SensorInput = db.SensorInput

	def runUpdate(self, sensorCount, SensorInput, count, temperature, humidity):

		yourName = socket.gethostname()
		yourIP = socket.gethostbyname(yourName)

		with contextlib.closing(urllib.request.urlopen("http://ip-api.com/json")) as response:
			userData = response.read().decode("utf-8")
			userDataJSON = json.loads(userData)

		headers = {'content-type': 'application/json'}
		url = "https://demo.thingsboard.io/api/v1/pctO13ntOzj0uqYw1bHc/telemetry"

		userCurrentTime = datetime.datetime.now(pytz.timezone(userDataJSON['timezone']))
		userCTimeString = userCurrentTime.strftime('%d/%m/%Y|%I:%M:%S')

		print(" ")

		temperature = str(temperature)
		humidity = str(humidity)

		if sensorCount > 8000:

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
			SensorInput.insert(post)
			latestData = SensorInput.find_one({"Humidity": humidity, "Temperature": temperature, "times updated": count})
			latestData = JSONEncoder().encode(post)

			count += 1

			req = requests.post(url, latestData)
			print(req)

		elif sensorCount < 8000:
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
			SensorInput.insert(post)
			latestData = SensorInput.find_one({"Humidity": humidity, "Temperature": temperature, "times updated": count})
			latestData = JSONEncoder().encode(post)

			count += 1

			req = requests.post(url, latestData)
			print(req)
