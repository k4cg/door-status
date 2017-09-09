#
#	k4cg door-status
#	Copyright (C) 2017  Christian Carlowitz <chca@cmesh.de>
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import urequests
import json
import time
import machine

import sensors
import util

class StatusService:
	def __init__(self, url):
		self.url = url

	def __push(self, dataDict):
		headers = {"content-type": "application/json"}
		jsonData = json.dumps(dataDict)
		urequests.post(self.url,data=jsonData,headers=headers)

	def submit(self,temp,humidity,door):
		d = "open" if door else "closed"
		t = time.localtime()
		tstr = "%d-%02d-%02dT%02d:%02d:%02d.000000" % t[0:6]
		data = {"tempDoor":temp, "humidity":humidity,"door":d,"date_GMT":tstr}
		self.__push(data)
		return data

def run(cfg):
	#dht11 = sensors.DHT11Mgr()
	#temp,humi = dht11.read_dht11()
	door = sensors.Door()
	stat = "open" if door.read() else "closed"

	if cfg["push-enabled"]:
		s = StatusService(cfg["push-url"])
		data = s.submit("","",stat)
		print("push: submitted " + repr(data))
		
	if cfg["mqtt-enabled"]:
		host = cfg["mqtt-server"]
		port = cfg["mqtt-port"]
		# TODO
