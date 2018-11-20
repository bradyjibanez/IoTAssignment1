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
	ambientLightSensorData = db.AmbientLightSensorData

	def runUpdate(self, sensorCount, ambientLightSensorData, count, temperature, humidity):

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
			latestData = ambientLightSensorData.find_one({"Humidity": humidity, "Temperature": temperature, "times updated": count})
			latestData = JSONEncoder().encode(post)


			count += 1

			req = requests.post(url, verify=False, json=latestData)
			#req.add_header('Accept', 'application/json; charset=utf-8')
			#jsondata = json.dumps(post)
			#jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
			#req.add_header('Content-Length', len(jsondataasbytes))
#			print (jsondataasbytes)
#			response = urllib.request.urlopen(req, jsondataasbytes)
#			requests.post(url, data=json.dumps(latestData), headers=headers)

		elif sensorCount < 1000:
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
			latestData = JSONEncoder().encode(post)

			count += 1

			req = requests.post(url, verify=False, json=latestData)
#			print(latestData)
#			requests.post(url, data=json.dumps(latestData), headers=headers)
