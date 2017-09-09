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

import json
import ntptime
import time
import machine

import util
import service

def wlan_init(cfg):
	util.wlan_connect(cfg["wlan-ssid"], cfg["wlan-secret"])
	util.wlan_wait(initrepl=True)
	ntptime.settime()

# init
cfg = json.loads(open("config.json").read())

if cfg["auto"]:
	# setup "watchdog timer"
	tim = machine.Timer(-1)
	tim.init(period=60000, mode=machine.Timer.ONE_SHOT, callback=lambda t: util.deepsleep(cfg["auto-sleep"]))
	# main routines
	wlan_init(cfg)
	service.run(cfg)
	# disarm watchdog
	tim.deinit()
	# wait to allow webrepl connections
	print("waiting 30s ...")
	time.sleep(cfg["auto-wake"])
	# go to sleep
	util.deepsleep(cfg["auto-sleep"])
