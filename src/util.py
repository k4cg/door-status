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

def deepsleep(timeSecs):
	print("going to sleep ...")
	import machine
	rtc = machine.RTC()
	rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
	rtc.alarm(rtc.ALARM0, 1000*timeSecs)
	machine.deepsleep()

def reboot():
	import machine
	machine.reset()

def wlan_connect(ssid, secret):
	import network
	import time

	wlan = network.WLAN(network.STA_IF)
	if not wlan.active():
		wlan.active(True)
	wlan.connect(ssid, secret)
	print("connecting to:", ssid)

def wlan_wait(timeoutSecs=20, initrepl=False):
	import network
	import time
	
	wlan = network.WLAN(network.STA_IF)
	cnt = 0
	while not wlan.isconnected() and cnt < timeoutSecs*10:
		time.sleep(0.1)
		cnt += 1
	if wlan.isconnected():
		print("network config:", wlan.ifconfig())
		if initrepl:
			import webrepl
			webrepl.start()
	else:
		print("wlan connect failed")
	
