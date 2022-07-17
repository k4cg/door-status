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

import dht
import machine
import time

def power(pwr3v3=False, pwr5v0=False):
	pin3v3 = machine.Pin(0, machine.Pin.OUT)
	pin5v0 = machine.Pin(2, machine.Pin.OUT)
	
	if pwr3v3:
		pin3v3.value(0)
	else:
		pin3v3.value(1)
		
	if pwr5v0:
		pin5v0.value(1)
	else:
		pin5v0.value(0)

class Door:
	def __init__(self):
		pass
	
	def read(self):
		sw = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
		time.sleep(0.2)
		v = sw.value() == 1
		sw = machine.Pin(12, machine.Pin.IN, None)
		return v
		
	def json(self):
		v = self.read()
		stat = "open" if v else "closed"
		return {"status": stat, "statusBool": v}

class BME280:
	def __init__(self, i2c, addr):
		from sensors_bme280 import BME280 as BME280_dev
		self.bme = BME280_dev(address = addr, i2c = i2c)
	
	def read(self):
		self.temp, self.press, self.humi = self.bme.fvalues
		return (self.temp, self.press, self.humi)
		
	def json(self):
		self.read()
		self.read()
		return { 
			"bme280/temperature" : float("%.2f" % self.temp),
			"bme280/pressure" : float("%.2f" % self.press),
			"bme280/humidity" : float("%.2f" % self.humi),
		}

