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
import umqtt.simple as mqtt

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
		t = time.localtime()
		tstr = "%d-%02d-%02dT%02d:%02d:%02d.000000" % t[0:6]
		data = {"tempDoor":temp, "humidity":humidity,"door":door,"date_GMT":tstr}
		self.__push(data)
		return data

def run(cfg, i2c):
	
	t = time.localtime()
	tstr = "%d-%02d-%02dT%02d:%02d:%02d.000000" % t[0:6]
	
	# query sensor based on config
	data = {}
	cnt = 0	
	while True:
		k = "%d"%cnt
		if not (k in cfg["sensors"]):
			break
		s = cfg["sensors"][k]
		cls = s["class"]
		node = s["node"]

		obj = getattr(sensors,cls)
		if obj == None:
			continue
		
		if not ("bus" in s):
			obj_inst = obj()
		else:
			bus = s["bus"]
			if bus == "i2c":
				addr = s["addr"]
				obj_inst = obj(i2c,addr)
			else:
				print("unknown bus:", bus)
				continue

		dataTmp = obj_inst.json()
		for key in dataTmp.keys():
			data[node+"/"+key] = dataTmp[key]
			
		cnt += 1
		
	print("data:", str(data))
	
	# publish with HTTP push
	if cfg["push-enabled"]:
		try:
			door = sensors.Door()
			stat = "open" if door.read() else "closed"
			temp = "" if not "default/bme280/temperature" in data else data["default/bme280/temperature"]
			humi = "" if not "default/bme280/humidity" in data else data["default/bme280/humidity"]
			s = StatusService(cfg["push-url"])
			dataPush = s.submit(str(temp),str(humi),stat)
			print("push: submitted " + repr(dataPush))
		except:
			pass
	
	# publish with MQTT
	cnt = 0
	while True:
		k = "%d"%cnt
		if not (k in cfg["mqtt"]):
			break
		m = cfg["mqtt"][k]
		host = m["server"]
		port = m["port"]
		topic = m["topic"]
		clid = "k4cg-door"
		user = None
		pw = None
		if ("user" in m) and ("pass" in m):
			user = m["user"]
			pw = m["pass"]
			clid = user
	
		print("server " + k + ": " + host)
		cli = mqtt.MQTTClient(clid, host, port, user, pw)
		cli.connect(clean_session=True)
		
		if m["json"]:
			s = tstr + " " + json.dumps(data)
			cli.publish(topic.encode(), s.encode(), retain=True)
		else:
			for key in data:
				subtopic = topic + "/" + key
				s = tstr + " " + str(data[key])
				tdiff = 946684800 # (date(2000, 1, 1) - date(1970, 1, 1)).days * 24*60*60
				tstamp = time.time() +  tdiff
				jdata = {"_timestamp":tstamp, "_datestr":tstr, "value":data[key]}
				cli.publish(subtopic.encode(), json.dumps(jdata).encode(), retain=True)
		
		cli.disconnect()
		
		cnt += 1
