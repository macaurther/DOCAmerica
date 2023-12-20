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
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	0,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	0,	-1,	-1,	0,	0,	-1,	-1,	0,	0,	0,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	4,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	0,	-1,	-1,	-1,	-1,	0,	0,	-1,	-1,	0,	0,	0,	-1,	0,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	4,	4,	4,	-1,	),
(	-1,	-1,	0,	-1,	-1,	-1,	-1,	0,	0,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	4,	4,	4,	4,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	-1,	0,	0,	0,	0,	0,	0,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	4,	4,	4,	4,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	4,	4,	4,	4,	4,	4,	-1,	),
(	0,	-1,	-1,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	2,	-1,	-1,	-1,	-1,	3,	3,	-1,	3,	-1,	4,	-1,	4,	4,	4,	-1,	-1,	),
(	-1,	-1,	0,	-1,	-1,	-1,	0,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	2,	2,	2,	2,	2,	-1,	-1,	3,	3,	3,	3,	3,	-1,	-1,	-1,	-1,	4,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	2,	2,	-1,	2,	-1,	2,	-1,	-1,	2,	2,	2,	2,	-1,	-1,	3,	3,	3,	3,	3,	3,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	-1,	-1,	-1,	-1,	-1,	-1,	2,	-1,	-1,	2,	-1,	-1,	-1,	-1,	2,	-1,	-1,	2,	2,	2,	-1,	-1,	3,	3,	3,	3,	3,	3,	3,	3,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	0,	0,	-1,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	-1,	-1,	-1,	2,	2,	2,	2,	-1,	-1,	2,	2,	-1,	2,	-1,	-1,	2,	2,	2,	-1,	-1,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	0,	-1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	-1,	1,	1,	-1,	-1,	-1,	2,	2,	2,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	-1,	2,	2,	2,	2,	-1,	2,	-1,	2,	-1,	-1,	2,	2,	2,	2,	-1,	-1,	-1,	-1,	-1,	3,	3,	3,	3,	3,	3,	3,	3,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	-1,	-1,	1,	1,	-1,	-1,	-1,	-1,	2,	-1,	-1,	-1,	2,	-1,	2,	2,	2,	2,	2,	2,	-1,	-1,	-1,	-1,	-1,	3,	3,	3,	3,	3,	3,	3,	3,	3,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	0,	-1,	5,	5,	1,	1,	1,	1,	1,	1,	1,	1,	-1,	-1,	1,	1,	1,	1,	2,	2,	-1,	-1,	-1,	2,	-1,	2,	-1,	-1,	2,	2,	2,	2,	2,	2,	2,	-1,	-1,	-1,	3,	3,	3,	3,	3,	3,	3,	3,	3,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	0,	5,	5,	5,	5,	5,	1,	1,	1,	1,	1,	1,	1,	-1,	1,	1,	1,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	-1,	2,	-1,	-1,	-1,	2,	2,	2,	2,	-1,	-1,	-1,	3,	3,	3,	3,	3,	3,	3,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	5,	-1,	5,	5,	5,	5,	5,	5,	5,	1,	1,	1,	1,	1,	1,	1,	1,	1,	2,	2,	2,	2,	2,	2,	-1,	2,	2,	2,	-1,	-1,	-1,	-1,	-1,	-1,	2,	2,	2,	2,	-1,	-1,	-1,	-1,	3,	3,	3,	3,	3,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	5,	5,	5,	5,	5,	5,	5,	5,	-1,	5,	5,	1,	-1,	-1,	1,	-1,	2,	2,	2,	2,	-1,	2,	2,	2,	2,	2,	-1,	-1,	2,	2,	-1,	2,	2,	2,	-1,	2,	2,	2,	2,	-1,	3,	3,	3,	3,	3,	3,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	5,	5,	5,	5,	5,	5,	5,	5,	5,	5,	5,	-1,	-1,	1,	1,	2,	2,	2,	2,	2,	2,	2,	2,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	2,	2,	-1,	2,	-1,	-1,	-1,	3,	3,	3,	3,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	5,	-1,	5,	5,	5,	5,	5,	5,	5,	5,	5,	5,	6,	6,	6,	-1,	2,	2,	2,	2,	2,	2,	2,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	2,	-1,	8,	8,	-1,	-1,	-1,	2,	-1,	-1,	-1,	-1,	-1,	3,	3,	3,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	5,	5,	5,	5,	5,	5,	5,	5,	5,	5,	6,	6,	6,	6,	6,	6,	6,	-1,	6,	6,	6,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	8,	8,	8,	8,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	3,	3,	3,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	10,	-1,	10,	10,	5,	5,	5,	5,	5,	5,	5,	6,	6,	6,	6,	6,	6,	-1,	6,	6,	6,	6,	6,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	8,	8,	-1,	8,	8,	-1,	-1,	8,	-1,	-1,	-1,	-1,	-1,	-1,	3,	3,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	10,	10,	10,	10,	10,	10,	10,	5,	5,	5,	5,	6,	6,	6,	6,	6,	-1,	6,	-1,	6,	6,	6,	7,	7,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	8,	8,	8,	8,	8,	8,	8,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	10,	-1,	10,	10,	10,	10,	10,	12,	12,	5,	5,	5,	6,	6,	6,	6,	6,	-1,	6,	-1,	6,	6,	7,	7,	7,	7,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	8,	8,	8,	8,	8,	8,	8,	9,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	10,	10,	-1,	-1,	10,	10,	10,	12,	12,	12,	12,	12,	6,	6,	6,	6,	6,	6,	6,	-1,	6,	6,	7,	7,	7,	7,	7,	7,	-1,	-1,	-1,	-1,	8,	8,	8,	8,	-1,	8,	8,	8,	9,	9,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	10,	10,	10,	10,	10,	10,	10,	12,	12,	12,	12,	12,	12,	12,	12,	15,	6,	6,	6,	6,	6,	6,	7,	7,	7,	7,	7,	7,	7,	7,	-1,	-1,	8,	8,	8,	8,	-1,	8,	8,	8,	-1,	8,	9,	9,	9,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	11,	11,	11,	10,	10,	10,	10,	10,	12,	12,	12,	12,	12,	12,	12,	12,	15,	15,	15,	15,	6,	6,	-1,	7,	7,	7,	-1,	7,	7,	7,	7,	-1,	-1,	8,	-1,	8,	8,	8,	8,	8,	8,	8,	8,	8,	9,	9,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	11,	11,	11,	11,	11,	12,	10,	10,	12,	12,	12,	12,	12,	12,	12,	12,	12,	15,	15,	15,	15,	16,	16,	16,	7,	7,	7,	7,	7,	7,	7,	7,	7,	-1,	8,	8,	8,	8,	8,	8,	8,	8,	8,	8,	8,	8,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	11,	11,	11,	11,	12,	12,	12,	12,	12,	12,	12,	12,	12,	12,	12,	12,	15,	15,	15,	15,	15,	16,	-1,	16,	16,	16,	7,	-1,	7,	7,	7,	7,	7,	8,	8,	8,	8,	8,	8,	8,	8,	8,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	11,	11,	12,	-1,	12,	12,	12,	12,	12,	12,	12,	12,	12,	12,	15,	15,	15,	15,	15,	16,	16,	16,	-1,	-1,	-1,	-1,	-1,	7,	7,	7,	7,	8,	8,	8,	8,	8,	8,	8,	8,	-1,	8,	8,	-1,	9,	-1,	9,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	11,	-1,	11,	11,	12,	12,	12,	12,	-1,	-1,	12,	12,	12,	12,	12,	12,	15,	-1,	15,	15,	15,	16,	16,	16,	16,	-1,	16,	-1,	-1,	7,	7,	7,	8,	8,	8,	8,	8,	8,	8,	8,	8,	8,	8,	-1,	-1,	-1,	-1,	9,	9,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	11,	11,	11,	11,	12,	12,	12,	12,	-1,	12,	12,	12,	12,	12,	12,	15,	15,	-1,	15,	15,	15,	16,	-1,	16,	16,	16,	16,	16,	16,	-1,	7,	7,	7,	8,	8,	8,	8,	8,	8,	8,	8,	9,	9,	9,	-1,	-1,	9,	9,	9,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	11,	11,	11,	11,	12,	12,	12,	12,	12,	12,	12,	12,	12,	12,	15,	15,	15,	15,	-1,	15,	15,	15,	15,	-1,	16,	16,	16,	-1,	-1,	-1,	-1,	7,	7,	7,	7,	8,	8,	8,	8,	17,	17,	9,	9,	9,	-1,	-1,	-1,	-1,	-1,	9,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	11,	11,	11,	11,	12,	13,	13,	13,	12,	12,	12,	12,	12,	12,	15,	15,	15,	15,	15,	-1,	15,	15,	15,	-1,	16,	16,	-1,	-1,	16,	-1,	-1,	7,	7,	7,	7,	8,	8,	8,	17,	17,	17,	9,	9,	-1,	-1,	9,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	11,	11,	11,	11,	13,	13,	13,	13,	12,	12,	12,	12,	12,	15,	15,	15,	15,	15,	-1,	15,	15,	15,	-1,	16,	16,	-1,	16,	16,	-1,	7,	7,	7,	-1,	18,	18,	-1,	17,	17,	17,	17,	-1,	-1,	9,	9,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	11,	-1,	11,	11,	13,	13,	13,	13,	13,	13,	12,	12,	15,	15,	15,	15,	15,	15,	-1,	15,	15,	15,	-1,	16,	16,	-1,	16,	16,	7,	7,	7,	-1,	-1,	18,	18,	18,	17,	17,	-1,	-1,	-1,	9,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	11,	11,	11,	13,	13,	13,	13,	13,	13,	13,	13,	13,	15,	15,	15,	15,	15,	15,	-1,	20,	20,	-1,	16,	16,	16,	16,	16,	16,	-1,	-1,	-1,	18,	18,	18,	18,	18,	17,	17,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	24,	24,	13,	13,	13,	13,	13,	13,	13,	13,	13,	13,	15,	15,	15,	15,	15,	15,	20,	-1,	-1,	16,	16,	16,	16,	16,	16,	16,	16,	16,	18,	18,	-1,	18,	18,	18,	17,	17,	17,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	24,	24,	25,	13,	13,	13,	13,	13,	13,	13,	13,	13,	14,	15,	15,	15,	15,	15,	20,	20,	20,	-1,	16,	16,	16,	16,	16,	16,	16,	18,	18,	18,	18,	18,	18,	18,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	24,	-1,	25,	25,	13,	13,	13,	13,	13,	13,	13,	13,	14,	14,	14,	15,	15,	15,	20,	20,	20,	-1,	16,	16,	16,	-1,	16,	16,	-1,	18,	18,	18,	18,	18,	18,	-1,	18,	18,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	24,	-1,	25,	25,	25,	13,	13,	14,	13,	13,	13,	13,	14,	14,	14,	14,	14,	15,	22,	22,	20,	20,	-1,	-1,	-1,	20,	-1,	-1,	20,	20,	18,	18,	18,	18,	18,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	24,	-1,	25,	25,	25,	25,	25,	14,	14,	14,	13,	14,	14,	14,	14,	14,	22,	22,	22,	22,	22,	-1,	20,	20,	20,	20,	20,	20,	20,	19,	19,	19,	19,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	24,	24,	-1,	25,	25,	25,	25,	25,	14,	14,	14,	14,	14,	14,	14,	14,	14,	22,	22,	22,	22,	-1,	20,	20,	20,	20,	20,	20,	20,	20,	19,	21,	19,	-1,	19,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	24,	24,	-1,	25,	25,	25,	25,	25,	14,	14,	14,	14,	14,	14,	14,	14,	14,	22,	22,	22,	-1,	22,	22,	22,	22,	22,	22,	22,	21,	21,	21,	21,	21,	-1,	19,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	24,	-1,	25,	25,	25,	25,	25,	14,	14,	14,	14,	14,	14,	14,	14,	14,	22,	22,	-1,	22,	22,	22,	22,	22,	22,	22,	21,	21,	21,	21,	21,	21,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	24,	-1,	25,	25,	25,	25,	25,	25,	25,	14,	14,	14,	14,	14,	14,	14,	22,	22,	-1,	22,	22,	22,	22,	22,	22,	21,	21,	21,	21,	21,	21,	21,	21,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	24,	-1,	25,	25,	25,	25,	25,	25,	25,	14,	14,	14,	14,	14,	14,	14,	22,	-1,	22,	22,	22,	22,	22,	22,	21,	21,	21,	21,	21,	21,	21,	21,	21,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	24,	-1,	25,	25,	25,	25,	25,	25,	25,	14,	14,	14,	14,	14,	-1,	14,	22,	22,	-1,	22,	22,	22,	22,	22,	21,	21,	21,	21,	-1,	21,	21,	21,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	24,	-1,	-1,	25,	25,	25,	-1,	25,	25,	14,	14,	14,	-1,	-1,	-1,	-1,	22,	22,	-1,	22,	22,	22,	22,	22,	21,	21,	21,	21,	21,	21,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	25,	25,	25,	25,	14,	14,	-1,	-1,	-1,	-1,	-1,	-1,	22,	22,	-1,	-1,	23,	23,	23,	21,	21,	21,	21,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	25,	25,	25,	25,	25,	14,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	23,	23,	21,	21,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	25,	25,	25,	25,	25,	25,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	23,	23,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	25,	25,	26,	26,	26,	26,	26,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	23,	23,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	26,	26,	26,	26,	26,	26,	26,	26,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	23,	23,	23,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	26,	26,	26,	26,	26,	26,	26,	26,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	23,	-1,	23,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	26,	26,	26,	26,	26,	26,	26,	27,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	23,	23,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	26,	26,	26,	26,	-1,	26,	27,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	23,	-1,	-1,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	28,	28,	26,	26,	26,	26,	27,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	28,	28,	28,	26,	27,	27,	27,	-1,	-1,	-1,	-1,	-1,	29,	29,	29,	-1,	-1,	31,	31,	31,	-1,	-1,	-1,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	28,	28,	28,	28,	27,	27,	27,	-1,	-1,	-1,	29,	29,	29,	29,	-1,	31,	-1,	-1,	31,	31,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	28,	28,	28,	28,	27,	27,	27,	29,	29,	29,	29,	29,	29,	-1,	-1,	-1,	-1,	-1,	-1,	31,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	28,	28,	28,	28,	27,	27,	29,	29,	29,	29,	29,	-1,	-1,	-1,	-1,	31,	-1,	-1,	-1,	31,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	28,	28,	27,	27,	30,	30,	29,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	31,	31,	-1,	-1,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	28,	30,	30,	30,	30,	30,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	31,	31,	31,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	30,	30,	30,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	32,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	30,	30,	30,	30,	-1,	-1,	-1,	-1,	-1,	-1,	31,	31,	-1,	-1,	31,	-1,	31,	31,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	32,	32,	-1,	32,	32,	-1,	-1,	32,	32,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	30,	30,	30,	30,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	31,	31,	31,	31,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	32,	32,	32,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	30,	30,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	31,	-1,	31,	31,	-1,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	32,	-1,	32,	32,	32,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	30,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	32,	32,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	-1,	30,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	32,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	32,	32,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	32,	32,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	30,	30,	-1,	-1,	-1,	-1,	33,	33,	33,	33,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	32,	32,	32,	32,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	30,	30,	-1,	30,	-1,	-1,	33,	33,	33,	34,	34,	-1,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	32,	32,	32,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	33,	33,	33,	33,	33,	33,	34,	-1,	34,	34,	34,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	32,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	33,	33,	33,	33,	33,	34,	34,	34,	34,	34,	34,	34,	34,	34,	-1,	-1,	31,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	33,	33,	33,	33,	33,	33,	33,	34,	34,	34,	34,	34,	34,	34,	34,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	33,	33,	33,	33,	33,	33,	33,	34,	34,	34,	34,	34,	34,	34,	34,	34,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	33,	33,	33,	33,	33,	33,	33,	33,	33,	34,	34,	34,	34,	34,	34,	-1,	34,	34,	34,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	33,	33,	33,	33,	33,	33,	33,	33,	33,	33,	33,	34,	34,	34,	34,	34,	34,	34,	34,	35,	35,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	33,	33,	33,	33,	33,	33,	33,	33,	33,	33,	33,	33,	34,	34,	34,	34,	34,	39,	34,	34,	34,	35,	35,	35,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	33,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	33,	33,	33,	33,	33,	33,	33,	33,	33,	33,	33,	38,	38,	34,	34,	34,	34,	39,	39,	39,	39,	39,	35,	35,	35,	35,	35,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	33,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	33,	33,	33,	33,	33,	33,	36,	33,	33,	33,	33,	38,	38,	38,	34,	34,	39,	39,	39,	39,	39,	35,	35,	35,	35,	-1,	35,	35,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	36,	36,	36,	33,	33,	36,	36,	36,	-1,	33,	33,	33,	38,	38,	38,	38,	38,	38,	38,	39,	39,	39,	39,	35,	35,	35,	35,	35,	35,	35,	35,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	36,	36,	36,	36,	36,	36,	36,	36,	36,	-1,	-1,	33,	33,	38,	38,	38,	38,	38,	38,	38,	39,	39,	39,	39,	39,	35,	35,	35,	35,	35,	39,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	36,	36,	36,	36,	36,	36,	36,	36,	36,	36,	36,	-1,	-1,	38,	38,	38,	38,	38,	38,	38,	-1,	39,	39,	39,	39,	39,	39,	39,	39,	39,	39,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	36,	36,	36,	36,	36,	36,	36,	36,	36,	36,	33,	38,	-1,	-1,	-1,	38,	38,	38,	38,	38,	39,	39,	39,	39,	39,	39,	39,	39,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	36,	36,	36,	36,	36,	36,	36,	38,	38,	38,	38,	38,	38,	38,	38,	-1,	-1,	-1,	38,	38,	39,	39,	-1,	-1,	-1,	-1,	-1,	-1,	39,	39,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	36,	36,	36,	36,	36,	36,	36,	38,	38,	38,	38,	38,	38,	38,	38,	38,	38,	38,	38,	-1,	-1,	-1,	-1,	39,	39,	39,	39,	39,	39,	39,	-1,	39,	39,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	36,	36,	36,	36,	36,	36,	38,	38,	38,	38,	38,	38,	38,	38,	38,	38,	38,	38,	38,	38,	38,	39,	39,	39,	39,	39,	39,	39,	39,	39,	39,	39,	39,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	36,	36,	36,	36,	36,	36,	36,	38,	38,	38,	38,	38,	38,	38,	38,	38,	38,	38,	38,	38,	39,	39,	39,	39,	39,	39,	39,	39,	39,	39,	39,	-1,	40,	40,	40,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	36,	36,	36,	36,	36,	36,	36,	36,	36,	38,	38,	38,	38,	38,	38,	38,	38,	38,	38,	38,	39,	39,	39,	39,	39,	39,	39,	39,	39,	39,	39,	40,	40,	40,	40,	40,	40,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	36,	36,	36,	36,	36,	36,	36,	37,	37,	37,	38,	38,	38,	38,	38,	38,	38,	38,	38,	39,	39,	39,	39,	39,	39,	39,	39,	39,	40,	40,	40,	40,	40,	40,	40,	40,	40,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	36,	36,	36,	36,	37,	37,	37,	37,	38,	38,	38,	38,	38,	42,	42,	38,	38,	39,	39,	39,	39,	39,	39,	39,	39,	40,	40,	40,	40,	40,	40,	40,	40,	40,	40,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	36,	36,	-1,	-1,	37,	37,	37,	37,	37,	38,	38,	38,	42,	42,	42,	42,	42,	42,	39,	39,	39,	39,	39,	39,	40,	40,	40,	40,	40,	40,	40,	40,	40,	40,	40,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	37,	37,	-1,	37,	37,	37,	37,	37,	37,	42,	42,	42,	42,	42,	42,	42,	42,	42,	42,	39,	-1,	41,	41,	40,	40,	40,	-1,	40,	40,	40,	40,	40,	40,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	44,	37,	37,	37,	37,	37,	37,	37,	37,	37,	42,	42,	42,	42,	42,	42,	42,	42,	42,	42,	42,	41,	41,	41,	41,	41,	-1,	40,	40,	40,	40,	40,	40,	40,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	44,	37,	37,	37,	37,	37,	37,	37,	37,	37,	42,	42,	42,	42,	42,	42,	42,	42,	42,	42,	41,	41,	41,	41,	41,	41,	41,	40,	40,	40,	40,	40,	40,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	44,	44,	37,	-1,	37,	37,	37,	37,	37,	37,	37,	42,	42,	42,	42,	42,	42,	42,	42,	42,	42,	42,	41,	41,	41,	41,	41,	41,	41,	41,	41,	41,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	44,	44,	48,	37,	-1,	37,	37,	37,	37,	45,	45,	37,	42,	42,	42,	42,	42,	42,	42,	42,	42,	42,	42,	41,	41,	41,	41,	41,	41,	41,	41,	41,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	44,	44,	44,	48,	48,	37,	37,	37,	37,	45,	45,	45,	42,	42,	42,	42,	42,	42,	42,	42,	42,	42,	42,	41,	41,	41,	41,	41,	41,	41,	41,	41,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	44,	44,	44,	48,	-1,	48,	48,	48,	48,	45,	45,	45,	42,	42,	42,	42,	42,	-1,	42,	42,	42,	42,	42,	42,	41,	41,	41,	41,	41,	41,	41,	41,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	44,	44,	44,	48,	48,	48,	48,	48,	48,	48,	48,	45,	45,	45,	42,	42,	42,	42,	-1,	41,	41,	41,	42,	42,	41,	41,	41,	41,	41,	41,	41,	41,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	44,	44,	44,	48,	48,	48,	48,	48,	48,	48,	47,	47,	45,	45,	45,	45,	43,	43,	43,	43,	41,	41,	41,	41,	41,	41,	41,	41,	41,	41,	41,	41,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	44,	44,	44,	48,	48,	48,	48,	-1,	48,	48,	47,	47,	47,	47,	45,	45,	45,	43,	43,	43,	43,	41,	41,	41,	41,	41,	41,	41,	41,	41,	41,	41,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	44,	44,	44,	48,	48,	48,	-1,	48,	48,	48,	47,	47,	47,	-1,	45,	45,	47,	43,	43,	43,	43,	43,	43,	41,	41,	41,	41,	41,	41,	41,	-1,	41,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	44,	44,	44,	48,	48,	48,	48,	48,	49,	-1,	-1,	47,	47,	47,	47,	47,	47,	43,	43,	43,	43,	43,	43,	43,	-1,	-1,	-1,	-1,	-1,	-1,	41,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	44,	44,	44,	44,	48,	48,	48,	49,	49,	49,	49,	49,	49,	47,	47,	47,	47,	47,	43,	43,	43,	43,	43,	43,	43,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	44,	44,	44,	44,	48,	48,	48,	48,	-1,	49,	49,	49,	49,	49,	47,	47,	43,	43,	43,	43,	43,	43,	43,	43,	43,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	44,	44,	-1,	50,	50,	48,	-1,	48,	49,	49,	49,	49,	49,	49,	49,	47,	46,	46,	43,	43,	43,	43,	43,	43,	43,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	44,	44,	-1,	44,	50,	50,	50,	48,	48,	48,	49,	49,	49,	49,	49,	49,	49,	46,	46,	46,	43,	43,	43,	-1,	-1,	43,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	44,	44,	50,	50,	50,	50,	50,	49,	49,	49,	49,	49,	49,	49,	49,	-1,	46,	46,	46,	46,	43,	-1,	43,	43,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	44,	44,	44,	44,	44,	50,	50,	-1,	50,	49,	49,	49,	49,	49,	49,	49,	49,	49,	49,	-1,	46,	46,	46,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	44,	-1,	44,	50,	50,	50,	50,	50,	49,	49,	49,	49,	-1,	49,	49,	49,	49,	49,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	-1,	44,	44,	44,	50,	50,	50,	-1,	50,	50,	49,	-1,	-1,	49,	-1,	-1,	-1,	-1,	49,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	-1,	44,	44,	44,	50,	-1,	50,	50,	50,	50,	50,	-1,	49,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	-1,	44,	44,	-1,	50,	50,	50,	50,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	44,	44,	50,	50,	50,	50,	50,	50,	50,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	),
(	-1,	44,	-1,	-1,	-1,	50,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	51,	51,	51,	51,	),
(	-1,	-1,	44,	50,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	51,	51,	51,	51,	),
(	-1,	-1,	44,	50,	50,	-1,	-1,	-1,	-1,	-1,	50,	-1,	50,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	51,	51,	51,	51,	),
(	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	-1,	51,	51,	51,	51,	),
)



tSpreadFactors = (
# Judaism
{
	iCore :			[rOldWorld],
	iHistorical :	[],
	iPeriphery :	[],
	iMinority :		[rOntario, rNewEngland, rMidAtlantic, rCalifornia, rBahia, rPampas],
},
# Orthodoxy
{
	iCore :			[rOldWorld],
	iHistorical : 	[rAlaska],
	iPeriphery : 	[rNorthPlains],
	iMinority :		[rMidAtlantic],
},
# Catholicism
{
	iCore :			[rBajio, rColombia, rPeru, rParaguay, rOldWorld],
	iHistorical :	[rQuebec, rFlorida, rTexas, rSierraMadres, rYucatan, rOaxaca, rVeracruz, rBajaCalifornia, rMesoamerica, rCaribbean, rVenezuela, rGuyana, rBolivia, rGuyana, rAmazonas, rBahia, rPara, rMinasGerais, rMatoGrosso, rParana, rChile, rUruguay, rChaco, rCuyo, rPampas, rPatagonia, rMaryland],
	iPeriphery :	[rOntario, rNewEngland, rMidAtlantic, rSouthwest, rCalifornia, rRockies, rSouthCascadia, rDeepSouth],
	iMinority :		[],
},
# Protestantism
{
	iCore :			[rOntario, rNewEngland, rMidAtlantic, rCoastalPlain, rTexas, rDeepSouth, rGreatLakes, rOldWorld],
	iHistorical :	[rAlaska, rNunavut, rNorthPlains, rNewFoundland, rSouthwest, rGreatPlains, rCalifornia, rRockies, rSouthCascadia, rNorthCascadia, rHawaii, rGuyana, rMaryland],
	iPeriphery :	[rQuebec, rMesoamerica, rPeru, rChile, rMinasGerais, rGreenland, rIceland],
	iMinority :		[],
},
# Islam
{
	iCore :			[rOldWorld],
	iHistorical :	[],
	iPeriphery :	[],
	iMinority : 	[rOntario, rMidAtlantic, rGuyana],
},
# Hinduism
{
	iCore :			[rOldWorld],
	iHistorical :	[],
	iPeriphery :	[rGuyana],
	iMinority :		[],
},
# Buddhism
{
	iCore :			[rOldWorld],
	iHistorical :	[],
	iPeriphery :	[],
	iMinority :		[rCalifornia],
},
# Confucianism
{
	iCore :			[rOldWorld],
	iHistorical :	[],
	iPeriphery :	[],
	iMinority :		[],
},
# Taoism
{
	iCore :			[rOldWorld],
	iHistorical :	[],
	iPeriphery :	[],
	iMinority :		[],
},
# Zoroastrianism
{
	iCore :			[rOldWorld],
	iHistorical :	[],
	iPeriphery :	[],
	iMinority :		[],
},
)