/*	
	k4cg door-status
	Copyright (C) 2017  Christian Carlowitz <chca@cmesh.de>

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

eps = 0.1;
$fn=32;

boardGap = 1;
boardX = 55+eps; // PCB width
boardY = 55+eps; // PCB depth
boardZ = 0; // PCB height
addZ = 23; // additional Y height until top part begins
wall = 1.4; // casing wall thickness
wallInsetW = 0;
wallInsetH = 0;
wallInsetOff = 0.2;

bottomHeight = 1.4;

mountR = 3;
mountW = 7;
mountHeight = boardZ+addZ;
mountDrill = 2.5;

screwSinkH = 2.5;
screwSinkD = 6.5;

// top plate
topHeight = 3.5;

