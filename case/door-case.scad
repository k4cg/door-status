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

module shell(w,bh,x,y,z,winw,winh)
{
	difference()
	{
		union()
		{
			translate([0,0,-bh])
				cube([w+x, w+y, z+bh]); // outer volume
			cube([x+winw,y+winw,z+winh]);
		}
		translate([-eps,-eps,0])
			cube([x+eps,y+eps,z+eps+winh]); // inner volume
	}
}

module mount(w,r,h,off)
{
	union()
	{
		translate([0,0,-eps])
		linear_extrude(height=h+eps)
		polygon(points=[[off+eps,off+eps],[-w,off+eps],
			[-w,-w/2],[-w/2,-w],[off+eps,-w] ]);
		
		translate([-w/2,-w/2,-eps])
		cylinder(h=h+eps, r=w/2);
	}
}

module mountr(x,y,r,h)
{
	translate([x,y,-eps])
	cylinder(h=h+eps, r=r);
}

module case()
{
	difference()
	{
		union()
		{
			// outer case shell
			shell(wall, bottomHeight, boardX/2+boardGap, boardY/2+boardGap, boardZ+addZ,
				wallInsetW, wallInsetH);

			// pc mount feature
			translate([boardX/2, boardY/2, 0])
			{
				mount(mountW, mountR, mountHeight, boardGap, mountDrill);
			}
		}

		translate([boardX/2, boardY/2])
		translate([-mountR,-mountR,addZ-15])
		{
			// screw drill
			cylinder(h=(15+2*eps), r=mountDrill/2);
		}
	}
}

module cut(x,y,w,h)
{
	translate([x-w/2,y-h/2,-bottomHeight-eps])
	cube([w,h,bottomHeight+2*eps]);
}

module cutr(x,y,r,hadd=0)
{
    translate([x,y,-bottomHeight-eps])
    cylinder(h=bottomHeight+2*eps+hadd, r=r);
}

module cutWall(x,y,w,d,h)
{
	translate([x-w/2,y-d/2,0])
	cube([w,d,h]);
}

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

			mountr(21,21,3,3);

			mirror([0,-1,0])
			mountr(21,21,3,3);
			
			mirror([-1,0,0])
			mountr(21,21,3,3);

			mirror([0,-1,0])
			mirror([-1,0,0])
			mountr(21,21,3,3);

		}

		cutr(0,28,3.4/2);
		cutr(0,-28,3.4/2);
		
		cutr(21,21,2.5/2,hadd=10);
		mirror([0,-1,0])
		cutr(21,21,2.5/2,hadd=10);
		mirror([-1,0,0])
		cutr(21,21,2.5/2,hadd=10);
		mirror([0,-1,0])
		mirror([-1,0,0])
		cutr(21,21,2.5/2,hadd=10);
		
		cutWall(-15,-boardY/2,5,10,3);
		cutWall(boardX/2,0,10,5,3);
		
	}
}

//translate([0,0,boardZ+addZ]) import("test1-top.stl");

