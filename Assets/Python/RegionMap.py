from Core import *
from Events import handler

iNumReligionMapTypes = 5
(iNone, iMinority, iPeriphery, iHistorical, iCore) = range(iNumReligionMapTypes)

def getMapValue(x, y):
	return tRegionMap[iWorldY-1-y][x]
	
def getSpreadFactor(iReligion, (x, y)):
	iRegion = plot(x, y).getRegionID()
	if iRegion < 0: return -1
	
	for iFactor in tSpreadFactors[iReligion].keys():
		if iRegion in tSpreadFactors[iReligion][iFactor]:
			return iFactor
	
	return iNone
	
def updateRegionMap():
	for plot in plots.all():
		plot.setRegionID(getMapValue(plot.getX(), plot.getY()))
			
	map.recalculateAreas()
			
def updateReligionSpread(iReligion):
	for plot in plots.all():
		plot.setSpreadFactor(iReligion, getSpreadFactor(iReligion, location(plot)))

def init():
	updateRegionMap()
	for iReligion in range(iNumReligions):
		updateReligionSpread(iReligion)
				

tRegionMap = ( 
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	1,	1,	1,	-1,	1,	1,	-1,	-1,	1,	1,	-1,	1,	-1,	1,	1,	1,	1,	1,	-1,	-1,	-1,	-1,	-1,	-1,	35,	35,	35,	35,	35,	35,	35,	35,	35,	35,	35,	35,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	0,	0,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	1,	1,	-1,	1,	-1,	-1,	1,	-1,	-1,	1,	-1,	-1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	35,	35,	35,	35,	35,	35,	35,	35,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	35,	35,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	-1,	-1,	-1,	-1,	-1,	1,	1,	1,	1,	1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	1,	1,	1,	-1,	1,	-1,	1,	1,	1,	1,	1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	35,	35,	35,	35,	35,	35,	35,	35,	-1,	-1,	-1,	-1,	-1,	-1,	35,	35,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	-1,	-1,	-1,	-1,	-1,	-1,	1,	-1,	1,	1,	1,	-1,	-1,	-1,	-1,	-1,	-1,	1,	1,	-1,	1,	1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	35,	35,	35,	35,	35,	35,	-1,	-1,	-1,	-1,	-1,	-1,	35,	35,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	-1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	-1,	-1,	-1,	1,	-1,	-1,	-1,	1,	1,	1,	1,	1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	35,	-1,	35,	35,	35,	35,	35,	-1,	-1,	-1,	-1,	-1,	35,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	-1,	-1,	-1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	-1,	-1,	-1,	-1,	-1,	1,	1,	1,	-1,	-1,	-1,	-1,	-1,	-1,	4,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	35,	35,	35,	35,	35,	35,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	-1,	1,	1,	-1,	-1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	-1,	1,	1,	1,	1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	4,	4,	-1,	-1,	4,	4,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	35,	35,	35,	35,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	-1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	4,	4,	4,	4,	4,	-1,	-1,	4,	4,	4,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	35,	35,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	-1,	1,	1,	1,	1,	-1,	1,	1,	1,	1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	0,	0,	0,	0,	-1,	0,	-1,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	-1,	-1,	1,	1,	1,	1,	1,	1,	1,	1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	5,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	0,	0,	-1,	0,	-1,	-1,	-1,	-1,	0,	15,	15,	15,	15,	15,	15,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	4,	4,	-1,	4,	4,	4,	4,	4,	4,	4,	4,	5,	5,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	0,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	0,	15,	15,	15,	15,	15,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	3,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	5,	5,	5,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	0,	-1,	0,	-1,	-1,	0,	-1,	-1,	-1,	-1,	-1,	-1,	0,	15,	15,	15,	15,	15,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	-1,	2,	2,	2,	2,	2,	2,	3,	3,	3,	3,	3,	3,	3,	3,	-1,	-1,	-1,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	-1,	4,	5,	5,	-1,	5,	5,	5,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	0,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	15,	15,	15,	15,	15,	2,	2,	2,	2,	2,	2,	2,	2,	2,	-1,	2,	-1,	2,	2,	2,	2,	3,	3,	3,	3,	3,	3,	3,	3,	3,	-1,	-1,	-1,	-1,	4,	4,	4,	4,	4,	4,	4,	4,	4,	-1,	4,	4,	4,	5,	5,	5,	5,	5,	5,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	15,	15,	15,	15,	15,	2,	2,	2,	2,	2,	2,	2,	2,	2,	-1,	2,	-1,	2,	2,	3,	3,	3,	-1,	3,	3,	3,	3,	3,	3,	3,	3,	3,	-1,	-1,	4,	4,	4,	4,	4,	4,	-1,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	-1,	-1,	-1,	5,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	15,	-1,	15,	15,	15,	15,	15,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	-1,	4,	4,	4,	4,	4,	4,	-1,	4,	4,	4,	4,	4,	4,	4,	4,	4,	-1,	-1,	-1,	-1,	5,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	15,	15,	15,	15,	15,	15,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	-1,	3,	3,	3,	-1,	-1,	3,	3,	3,	3,	3,	3,	3,	3,	3,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	-1,	-1,	-1,	-1,	5,	-1,	-1,	5,	5,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	15,	-1,	15,	15,	15,	15,	15,	15,	12,	12,	12,	12,	12,	12,	12,	12,	12,	12,	10,	10,	3,	3,	3,	-1,	-1,	-1,	-1,	3,	3,	3,	3,	3,	3,	3,	4,	4,	4,	4,	4,	-1,	4,	4,	4,	4,	4,	-1,	-1,	-1,	4,	4,	-1,	-1,	-1,	5,	5,	5,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	15,	15,	15,	15,	15,	15,	15,	15,	12,	12,	12,	12,	12,	12,	12,	12,	12,	12,	10,	10,	10,	-1,	-1,	-1,	-1,	-1,	-1,	3,	3,	3,	3,	3,	3,	3,	3,	4,	4,	4,	4,	4,	4,	4,	4,	4,	-1,	-1,	4,	4,	4,	4,	4,	-1,	-1,	-1,	-1,	-1,	5,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	15,	15,	15,	15,	15,	15,	15,	12,	12,	12,	12,	12,	12,	12,	12,	12,	12,	12,	10,	10,	-1,	-1,	-1,	10,	10,	-1,	-1,	-1,	3,	-1,	-1,	3,	3,	3,	3,	3,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	6,	6,	5,	5,	5,	5,	-1,	5,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	15,	15,	15,	15,	15,	11,	13,	13,	13,	12,	12,	12,	12,	12,	12,	12,	12,	12,	12,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	-1,	-1,	-1,	-1,	-1,	3,	3,	3,	3,	3,	4,	4,	4,	4,	4,	4,	4,	4,	6,	6,	6,	5,	5,	-1,	5,	5,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	15,	15,	15,	15,	13,	13,	13,	13,	13,	13,	12,	12,	12,	12,	12,	12,	12,	12,	12,	10,	10,	10,	10,	10,	10,	10,	-1,	-1,	-1,	10,	-1,	-1,	3,	-1,	3,	3,	3,	-1,	3,	3,	4,	4,	4,	6,	6,	6,	6,	6,	6,	6,	5,	-1,	5,	5,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	15,	15,	15,	15,	12,	13,	13,	13,	13,	13,	13,	13,	12,	12,	12,	12,	12,	12,	12,	12,	10,	10,	-1,	10,	10,	10,	-1,	10,	-1,	10,	10,	-1,	-1,	3,	3,	3,	-1,	-1,	-1,	7,	7,	7,	-1,	7,	6,	6,	6,	6,	6,	-1,	-1,	-1,	-1,	5,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	14,	14,	14,	14,	13,	13,	13,	13,	13,	13,	13,	13,	13,	12,	12,	12,	12,	12,	12,	12,	10,	10,	-1,	-1,	10,	10,	10,	-1,	-1,	10,	10,	10,	-1,	3,	3,	3,	7,	7,	7,	7,	7,	7,	7,	7,	6,	6,	6,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	14,	14,	14,	14,	13,	13,	13,	13,	-1,	-1,	13,	13,	12,	12,	12,	12,	12,	12,	12,	12,	10,	10,	10,	-1,	10,	10,	10,	-1,	-1,	10,	10,	10,	3,	-1,	-1,	-1,	7,	7,	-1,	7,	7,	7,	7,	7,	6,	6,	6,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	14,	14,	14,	14,	13,	13,	13,	13,	13,	-1,	13,	13,	13,	13,	12,	12,	12,	12,	12,	12,	10,	10,	10,	-1,	10,	10,	10,	-1,	10,	10,	10,	-1,	-1,	-1,	10,	7,	7,	7,	7,	7,	7,	7,	7,	7,	6,	6,	6,	6,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	14,	14,	14,	14,	13,	-1,	13,	13,	13,	13,	13,	13,	13,	13,	12,	12,	12,	12,	12,	-1,	10,	10,	10,	-1,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	7,	7,	7,	7,	7,	7,	7,	7,	7,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	14,	14,	-1,	14,	13,	13,	13,	13,	13,	13,	13,	13,	13,	13,	12,	12,	12,	12,	12,	-1,	10,	10,	10,	-1,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	7,	7,	7,	7,	7,	7,	7,	7,	-1,	7,	7,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	14,	13,	13,	13,	13,	13,	13,	13,	13,	13,	13,	12,	12,	12,	12,	12,	12,	10,	10,	10,	-1,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	10,	7,	7,	7,	7,	7,	7,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	14,	-1,	14,	14,	13,	13,	13,	13,	13,	13,	13,	10,	10,	12,	12,	12,	12,	12,	12,	10,	-1,	-1,	10,	10,	10,	-1,	-1,	-1,	-1,	-1,	10,	10,	10,	7,	7,	7,	7,	7,	-1,	7,	7,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	14,	14,	14,	11,	11,	11,	11,	11,	11,	11,	10,	10,	12,	12,	12,	12,	12,	12,	10,	10,	10,	10,	-1,	-1,	-1,	10,	10,	10,	10,	10,	10,	7,	7,	7,	7,	7,	7,	-1,	-1,	7,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	14,	14,	14,	14,	11,	11,	11,	11,	11,	11,	10,	10,	12,	12,	12,	12,	12,	12,	10,	10,	10,	10,	-1,	10,	10,	10,	10,	10,	10,	10,	10,	7,	7,	7,	7,	7,	7,	7,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	14,	14,	14,	14,	14,	11,	11,	11,	11,	11,	11,	12,	12,	12,	12,	12,	12,	8,	8,	8,	8,	8,	-1,	8,	8,	8,	8,	8,	8,	8,	8,	8,	8,	8,	8,	8,	8,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	14,	14,	14,	11,	11,	11,	11,	11,	11,	11,	12,	12,	12,	12,	8,	8,	8,	8,	8,	8,	-1,	8,	8,	8,	8,	8,	8,	8,	8,	8,	8,	8,	8,	8,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	14,	14,	11,	11,	11,	11,	11,	11,	11,	11,	11,	11,	11,	8,	8,	8,	8,	8,	8,	-1,	8,	8,	8,	8,	8,	8,	8,	8,	8,	8,	8,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	16,	16,	11,	11,	11,	11,	11,	11,	11,	11,	11,	11,	11,	11,	8,	8,	8,	8,	8,	-1,	8,	8,	8,	8,	8,	8,	8,	8,	8,	8,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	16,	-1,	16,	16,	16,	11,	16,	16,	11,	11,	11,	11,	11,	11,	11,	9,	9,	9,	9,	9,	9,	9,	9,	8,	8,	8,	8,	8,	8,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	16,	-1,	-1,	16,	16,	16,	16,	16,	11,	11,	11,	11,	11,	11,	9,	9,	9,	9,	9,	9,	-1,	-1,	9,	9,	9,	9,	9,	9,	9,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	16,	-1,	-1,	16,	16,	16,	16,	16,	11,	16,	11,	11,	9,	9,	9,	-1,	-1,	9,	9,	9,	-1,	-1,	-1,	-1,	9,	-1,	9,	9,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	16,	-1,	16,	16,	16,	16,	16,	16,	16,	16,	11,	9,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	9,	9,	9,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	16,	16,	-1,	-1,	16,	16,	16,	16,	16,	16,	16,	9,	9,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	9,	-1,	9,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	16,	-1,	16,	16,	16,	16,	16,	16,	16,	16,	9,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	9,	9,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	16,	-1,	-1,	16,	16,	16,	16,	16,	16,	16,	16,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	9,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	16,	-1,	-1,	-1,	16,	16,	16,	16,	16,	16,	17,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	20,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	16,	-1,	-1,	16,	16,	16,	16,	16,	17,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	16,	16,	16,	16,	17,	-1,	-1,	-1,	-1,	-1,	18,	18,	18,	-1,	-1,	20,	20,	20,	20,	20,	20,	-1,	-1,	-1,	-1,	-1,	20,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	16,	17,	17,	17,	17,	17,	-1,	-1,	-1,	18,	18,	18,	18,	-1,	-1,	20,	-1,	-1,	-1,	20,	20,	20,	20,	20,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	17,	17,	17,	17,	17,	17,	-1,	-1,	-1,	18,	18,	18,	-1,	-1,	-1,	-1,	-1,	20,	-1,	-1,	-1,	20,	20,	20,	20,	-1,	20,	20,	20,	20,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	17,	17,	17,	17,	17,	17,	17,	18,	18,	18,	19,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	20,	20,	20,	20,	-1,	20,	20,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	17,	17,	17,	17,	17,	18,	18,	19,	19,	-1,	-1,	-1,	-1,	-1,	-1,	20,	-1,	-1,	20,	20,	-1,	-1,	20,	20,	20,	20,	-1,	-1,	-1,	-1,	-1,	-1,	20,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	17,	17,	17,	-1,	18,	19,	19,	19,	19,	19,	19,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	19,	19,	19,	19,	19,	19,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	20,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	21,	-1,	21,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	19,	19,	19,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	21,	21,	-1,	21,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	19,	-1,	19,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	23,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	20,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	21,	21,	21,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	19,	19,	19,	-1,	-1,	-1,	-1,	-1,	22,	22,	23,	-1,	23,	23,	23,	-1,	23,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	21,	21,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	19,	19,	19,	-1,	19,	-1,	22,	22,	22,	23,	-1,	23,	23,	23,	23,	23,	23,	23,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	19,	-1,	22,	22,	22,	22,	23,	23,	23,	23,	23,	23,	23,	-1,	23,	24,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	21,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	22,	22,	22,	22,	22,	23,	23,	23,	23,	23,	23,	23,	24,	24,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	21,	21,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	22,	22,	22,	22,	22,	22,	22,	23,	23,	23,	23,	23,	24,	24,	24,	24,	24,	24,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	21,	21,	21,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	22,	22,	22,	22,	22,	22,	22,	23,	23,	27,	27,	27,	24,	24,	24,	24,	24,	24,	27,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	21,	21,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	22,	22,	22,	22,	22,	22,	22,	22,	23,	23,	23,	27,	27,	24,	24,	24,	24,	24,	24,	27,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	25,	22,	22,	22,	22,	27,	27,	23,	23,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	25,	25,	25,	22,	22,	22,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	25,	25,	25,	25,	22,	22,	22,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	-1,	-1,	27,	27,	27,	27,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	-1,	25,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	25,	25,	25,	25,	25,	22,	27,	27,	27,	27,	27,	27,	27,	-1,	-1,	-1,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	28,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	25,	25,	25,	25,	25,	27,	27,	27,	-1,	-1,	-1,	-1,	-1,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	28,	28,	28,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	25,	25,	25,	25,	27,	27,	-1,	-1,	-1,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	28,	28,	28,	28,	28,	28,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	25,	25,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	28,	28,	28,	28,	28,	28,	28,	28,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	25,	25,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	28,	28,	28,	28,	28,	28,	28,	28,	28,	28,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	25,	25,	25,	25,	27,	27,	26,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	28,	28,	28,	28,	28,	28,	28,	28,	28,	28,	28,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	25,	25,	25,	25,	26,	26,	26,	27,	27,	27,	27,	27,	27,	27,	27,	27,	27,	28,	28,	28,	28,	28,	28,	28,	28,	28,	28,	28,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	25,	25,	25,	25,	26,	26,	26,	26,	27,	27,	27,	27,	27,	27,	27,	28,	28,	28,	28,	28,	28,	28,	28,	28,	28,	28,	28,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	25,	25,	26,	26,	26,	26,	26,	26,	26,	29,	29,	27,	27,	29,	28,	28,	28,	28,	28,	28,	28,	28,	28,	28,	28,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	-1,	-1,	26,	26,	26,	26,	26,	26,	29,	29,	29,	29,	29,	29,	28,	28,	28,	28,	28,	28,	28,	28,	28,	28,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	26,	26,	26,	26,	26,	26,	26,	26,	29,	29,	29,	29,	29,	29,	28,	28,	28,	28,	28,	28,	28,	28,	28,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	26,	26,	-1,	26,	26,	26,	26,	26,	26,	29,	29,	29,	29,	29,	29,	29,	28,	28,	28,	28,	28,	28,	28,	28,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	26,	26,	26,	26,	26,	31,	26,	29,	29,	29,	29,	29,	29,	29,	28,	28,	28,	28,	28,	28,	28,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	26,	26,	26,	26,	31,	31,	31,	29,	29,	29,	29,	29,	29,	29,	28,	28,	28,	28,	28,	28,	28,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	26,	33,	26,	33,	31,	31,	31,	29,	29,	29,	29,	29,	29,	29,	28,	28,	28,	28,	28,	28,	28,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	30,	33,	33,	33,	31,	31,	31,	31,	31,	29,	29,	29,	29,	28,	28,	28,	28,	28,	28,	28,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	33,	33,	33,	33,	33,	33,	31,	31,	31,	29,	29,	28,	28,	28,	28,	28,	28,	28,	-1,	28,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	33,	33,	33,	33,	33,	33,	33,	31,	31,	29,	29,	28,	28,	28,	28,	28,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	33,	33,	33,	33,	33,	33,	33,	31,	31,	33,	28,	28,	28,	28,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	33,	33,	33,	33,	33,	33,	33,	31,	31,	33,	28,	28,	28,	28,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	30,	33,	33,	33,	33,	33,	33,	33,	33,	33,	28,	28,	28,	28,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	33,	33,	33,	33,	33,	33,	33,	33,	33,	28,	28,	28,	28,	28,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	33,	33,	-1,	33,	33,	33,	33,	33,	28,	28,	28,	28,	28,	28,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	33,	33,	33,	33,	-1,	33,	33,	33,	32,	32,	28,	28,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	33,	33,	33,	33,	33,	33,	33,	33,	33,	32,	32,	32,	28,	-1,	28,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	33,	33,	33,	33,	33,	33,	33,	33,	33,	32,	32,	32,	-1,	28,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	33,	33,	33,	33,	34,	34,	33,	33,	32,	32,	32,	32,	32,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	34,	34,	34,	34,	34,	34,	33,	33,	-1,	-1,	32,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	34,	34,	34,	34,	34,	34,	34,	34,	33,	33,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	34,	34,	34,	34,	34,	34,	34,	34,	34,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	34,	34,	34,	34,	34,	34,	34,	34,	34,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	34,	34,	34,	34,	34,	34,	34,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	34,	34,	34,	34,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	-1,	30,	34,	34,	34,	34,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	34,	34,	34,	34,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	34,	34,	34,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	34,	34,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	34,	34,	34,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	34,	34,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	34,	-1,	-1,	-1,	-1,	-1,	-1,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	-1,	-1,	34,	-1,	-1,	-1,	-1,	-1,	-1,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	34,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	34,	34,	34,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
)

tSpreadFactors = (
# Judaism
{
	iMinority :	[rOntario, rNewEngland, rMidAtlantic, rCalifornia, rBrazilianHighlands, rPampas],
},
# Orthodoxy
{
	iHistorical : 	[rAlaska],
	iPeriphery : 	[rNorthPlains],
	iMinority :	[rMidAtlantic],
},
# Catholicism
{
	iCore :		[rBajio, rColombia, rPeru, rParaguay],
	iHistorical :	[rQuebec, rGulfCoast, rSierraMadre, rYucatan, rMesoamerica, rCaribbean, rVenezuela, rGuyana, rBolivia, rGuyana, rAmazon, rBrazilianHighlands, rPantanal, rChile, rUruguay, rPampas, rPatagonia],
	iPeriphery :	[rOntario, rNewEngland, rMidAtlantic, rSouthwest, rCalifornia, rRockies, rCascadia],
},
# Protestantism
{
	iCore :		[rOntario, rNewEngland, rMidAtlantic, rDeepSouth, rMidwest],
	iHistorical :	[rAlaska, rNunavut, rNorthPlains, rNewFoundland, rSouthwest, rGreatPlains, rCalifornia, rRockies, rCascadia, rHawaii, rGuyana],
	iPeriphery :	[rQuebec, rMesoamerica, rPeru, rChile, rBrazilianHighlands, rGreenland],
},
# Islam
{
	iMinority : 	[rOntario, rMidAtlantic, rGuyana],
},
# Hinduism
{
	iPeriphery :	[rGuyana],
},
# Buddhism
{
	iMinority :	[rCalifornia],
},
# Confucianism
{
},
# Taoism
{
},
# Zoroastrianism
{
},
)