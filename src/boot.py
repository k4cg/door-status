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

import util

def wlan_connect(ssid="k4cg-intern", password=None):
	import network
	import time
	wlan = network.WLAN(network.STA_IF)
	if password == None:
		password = open("wlan_pw.txt").read().strip()
	if not wlan.active():
		wlan.active(True)
		wlan.connect(ssid, password)
	print("connecting to:", ssid)
	cnt = 0
	while not wlan.isconnected() and cnt < 200:
		time.sleep(0.1)
		cnt += 1
	if wlan.isconnected():
		print("network config:", wlan.ifconfig())
	else:
		print("wlan connect failed")
		util.deepsleep(2)

	import webrepl
	webrepl.start()

def reboot():
	import machine
	machine.reset()

try:
	wlan_connect()
	import ntptime
	ntptime.settime()
	import service
	service.run()
except Exception as e:
	print("High Level Exception: " + repr(e))

util.deepsleep(2)

