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

def deepsleep(timeMin):
	print("going to sleep ...")
	import machine
	rtc = machine.RTC()
	rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
	rtc.alarm(rtc.ALARM0, 1000*60*timeMin)
	machine.deepsleep()

