
$fn=32;

wall=1;
inner=8;
H=6;
eps=0.1;
offs=0.4;
Hi=13.3-H-2*wall;

color("blue",0.5)
difference()
{
	union()
	{
		cylinder(h=H+wall,d=inner+2*wall);
		cylinder(h=wall,d=12);
	}
	translate([0,0,-eps])
	cylinder(h=H+eps,d=inner);
	
	cylinder(h=20,d=inner-2*wall);
}

*color("red",0.5)
translate([0,0,H-wall])
difference()
{
	union()
	{
		cylinder(h=Hi+wall,d=inner-2*wall-offs);
		cylinder(h=wall,d=inner-offs);
	}
	translate([0,0,-eps])
	cylinder(h=Hi+eps,d=inner-4*wall+offs);
}

