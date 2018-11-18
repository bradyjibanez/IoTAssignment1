from pymongo import MongoClient
from urllib.request import urlopen
import socket, datetime, pytz, sys, json

class Update:

	makeUpJunk = 0
	MONGO_DB = "IoTI"
	CONNECTION = MongoClient()

	db = CONNECTION.IoTI
	ambientLightSensorData = db.AmbientLightSensorData
	db.AmbientLightSensorData.delete_many({})

#	yourName = socket.gethostname()
#	yourIP = socket.gethostbyname(yourName)
#	response = urlopen("http://ip-api.com/json")
#	userData = response.read().decode("utf-8")
#	userDataJSON = json.loads(userData)
#	count = 1

	def runUpdate(self, sensorCount, ambientLightSensorData, count):

#		MONGO_DB = "IoTI"
#		CONNECTION = MongoClient()

#		db = CONNECTION.IoTI
#		ambientLightSensorData = db.AmbientLightSensorData
#		db.AmbientLightSensorData.delete_many({})

		yourName = socket.gethostname()
		yourIP = socket.gethostbyname(yourName)
		response = urlopen("http://ip-api.com/json")
		userData = response.read().decode("utf-8")
		userDataJSON = json.loads(userData)

		myurl = "https://demo.thingsboard.io/api/v1/3mmZ09cG3cyrzFZku4BF/telemetry"
		req = urllib.request.Request(myurl)
		req.add_header('Content-Type', 'application/json; charset=utf-8')

		lightStatus = "off"

#		update = input('Update the db with whatever...or enter quit to quit: ')
#		print('Oh ya...count is ', count)
		userCurrentTime = datetime.datetime.now(pytz.timezone(userDataJSON['timezone']))
		userCTimeString = userCurrentTime.strftime('%d/%m/%Y|%I:%M:%S')
#		if update == "quit":
#			print(" ")
#			print("See ya")
#			print(" ")
#			sys.exit(0)
#		else:
		print(" ")
		if sensorCount > 10000:
			lightStatus = "on"
			post = {"author": yourName,
				"author IP": yourIP,
				"light status": lightStatus,
				"times updated": count,
				"date": userCTimeString}
			ambientLightSensorData.insert(post)
			count += 1

			jsondata = json.dumps(post)
			jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
			req.add_header('Content-Length', len(jsondataasbytes))
			# print (jsondataasbytes)
			response = urllib.request.urlopen(req, jsondataasbytes)

		else:
			lightStatus = "off"
			post = {"author": yourName,
				"author IP": yourIP,
				"light status": lightStatus,
				"times updated": count,
				"date": userCTimeString}
			ambientLightSensorData.insert(post)
			count += 1

			jsondata = json.dumps(post)
			jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
			req.add_header('Content-Length', len(jsondataasbytes))
			# print (jsondataasbytes)
			response = urllib.request.urlopen(req, jsondataasbytes)