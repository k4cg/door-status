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

import dht
import machine
import time

class DHT11Mgr:
	def __init__(self):
		self.dht11 = dht.DHT11(machine.Pin(4))
		self.pwr = machine.Pin(15, machine.Pin.OUT)

	def __enable(self,turnOn=True):
		if turnOn:
			self.pwr.on()
		else:
			self.pwr.off()

	def __read_dht11_single(self):
		self.dht11.measure()
		humi = self.dht11.humidity()
		temp = self.dht11.temperature()
		return temp,humi

	def read_dht11(self):
		self.__enable()
		time.sleep(0.2)
		for i in range(0,4):
			self.__read_dht11_single()
		v = self.__read_dht11_single()
		self.__enable(False)
		return v

class Door:
	def __init__(self):
		self.pullup = machine.Pin(14, machine.Pin.OUT)
		self.sw = machine.Pin(12, machine.Pin.IN)
	
	def read(self):
		self.pullup.on()
		time.sleep(0.2)
		v = self.sw.value() == 1
		self.pullup.off()
		return v
