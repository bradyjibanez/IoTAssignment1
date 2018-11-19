Be sure to run with Python3 on Raspberrypi 3 running Raspbian

Install pymongo:
	~/$ pip3 install pymongo==2.7.2

Install urllib:
	~/$ pip3 install urllib

Install socket, datetime, pytz, http.client:
	~/$ pip3 install socket
	"    " datetime
	"    " pytz
	"    " http.client

Configure mongoDB:

	Begin by installing dirmngr on Pi:
		~/$ sudo apt-get install dirmngr

	Install mongoDB as indicated here:
		https://andyfelong.com/2018/03/mongodb-3-2-64-bit-running-on-raspberry-pi-3-with-caveats/

	Once installed, run the following commands:
		~/$ mongo
		> use IoTI
		> db.createCollection("AmbientLightSensorData")
		> db.addUser(
		... {
		... user: "thepi",
		... pwd: "thepi",
		... roles: [{role: "readWrite", db: "IoTI"})
		... }
		... )

Should be good to go.
		

# IoTI
