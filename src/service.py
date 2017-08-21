#
#	k4cg space-status
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

class StatusService:
	def __init__(self):
		pass

	def __push(self, dataDict):
		url = "http://heimat:8000"
		headers = {"content-type": "application/json"}
		jsonData = json.dumps(dataDict)
		urequests.post(url,data=jsonData,headers=headers)

	def submit(self,temp,humidity,door):
		d = "open" if door else "closed"
		t = time.localtime()
		tstr = "%d-%02d-%02d %02d:%02d:%02d" % t[0:6]
		data = {"tempDoor":temp, "humidity":humidity,"door":d,"date":tstr}
		self.__push(data)
		return data

def run():
	try:
		s = StatusService()
		dht11 = sensors.DHT11Mgr()
		temp,humi = dht11.read_dht11()
		door = sensors.Door()
		stat = "open" if door.read() else "closed"
		data = s.submit(temp,humi,stat)
		print("done, submitted " + repr(data))


	except Exception as e:
		print("Exception: " + repr(e))

	print("waiting 60s ...")
	time.sleep(60)

	print("going to sleep ...")
	rtc = machine.RTC()
	rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
	rtc.alarm(rtc.ALARM0, 1000*60*5)
	machine.deepsleep()
		
