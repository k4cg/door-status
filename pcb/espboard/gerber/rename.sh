#!/bin/bash

N=$1
M=$2

cp ${N}-F.Cu.gbr ${M}.GTL
cp ${N}-B.Cu.gbr ${M}.GBL
cp ${N}-F.SilkS.gbr ${M}.GTO
cp ${N}-B.SilkS.gbr ${M}.GBO
cp ${N}-F.Mask.gbr ${M}.GTS
cp ${N}-B.Mask.gbr ${M}.GBS
cp ${N}-Edge.Cuts.gbr ${M}.GML
cp ${N}.drl ${M}.TXT

