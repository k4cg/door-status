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

// *** all dimensions in mm ***

include <door-case-params.scad>

module shell(w,x,y,z,winw,winh,woff)
{
	union()
	{
		difference()
		{
			cube([x+w, y+w, z]); // outer volume
	
			//translate([-eps,-eps,-eps])
			//cube([x+winw+woff+eps,y+winw+woff+eps,winh*2+2*eps]); // notch
		}
		
		//cube([x-woff*3,y-woff*3,z-eps]);
	}
}

module case()
{
	difference()
	{
		union()
		{
			// outer case shell
			shell(wall, boardX/2+boardGap, boardY/2+boardGap, topHeight,
				wallInsetW, wallInsetH, wallInsetOff);
		}

		translate([boardX/2-mountR, boardY/2-mountR, -eps])
		{
			// screw drill
			cylinder(h=(topHeight+2*eps), r=mountHole/2);
			
			// screw sink
			translate([0,0,topHeight-screwSinkH+eps])
			cylinder(h=(screwSinkH+eps), r=screwSinkD/2);
		}
	}
}

module cut(x,y,w,h)
{
	translate([x-w/2,y-h/2,-eps])
	cube([w,h,topHeight+2*eps]);
}

module body()
{

	union()
	{
		difference()
		{
			union()
			{
				translate([-eps,-eps,0])
				case();

				mirror([-1,0,0])
				translate([-eps,-eps,0])
				case();

				mirror([0,-1,0])
				translate([-eps,-eps,0])
				case();

				mirror([0,-1,0])
				mirror([-1,0,0])
				translate([-eps,-eps,0])
				case();
			}

			cut(22,10,1.5,20);
			cut(18,10,1.5,20);
			cut(14,10,1.5,20);
			cut(10,10,1.5,20);

		}
	}
}

module fillet(r,l) // along y axis
{
	translate([0,-l/2-eps,0])
	difference()
	{
		cube([r*2,l+2*eps,r*2]);
		translate([0,-eps,0])
		rotate([-90,0,0])
		cylinder(h=l+4*eps,r=r);
	}
}

filletR = 2;
caseY = boardY+2*boardGap+2*wall-2*eps; // -2*eps: remove offset for union of mirrored parts
caseX = boardX+2*boardGap+2*wall-2*eps;

difference()
{
	body();

	translate([caseX/2-filletR,0,topHeight-filletR])
	fillet(filletR,caseY);

	rotate([0,0,180])
	translate([caseX/2-filletR,0,topHeight-filletR])
	fillet(filletR,caseY);
	
	translate([0,caseY/2-filletR,topHeight-filletR])
	rotate([0,0,90])
	fillet(filletR,caseX);

	rotate([0,0,180])
	translate([0,caseY/2-filletR,topHeight-filletR])
	rotate([0,0,90])
	fillet(filletR,caseX);
}
