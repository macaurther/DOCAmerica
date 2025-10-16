from Core import *
from Files import FileMap
from Events import handler

iNumReligionMapTypes = 5
(iNone, iMinority, iPeriphery, iHistorical, iCore) = range(iNumReligionMapTypes)

def getSpreadFactor(iReligion, plot):
	iRegion = plot.getRegionID()
	if iRegion < 0: 
		return -1
	
	return next((iFactor for iFactor, lRegions in tSpreadFactors[iReligion].items() if iRegion in lRegions), iNone)
	
def updateRegionMap():
	for (x, y), iRegion in FileMap.read("Regions.csv"):
		plot(x, y).setRegionID(iRegion)

	map.recalculateAreas()
			
def updateReligionSpread(iReligion):
	for plot in plots.all():
		plot.setSpreadFactor(iReligion, getSpreadFactor(iReligion, plot))

def init():
	updateRegionMap()
	for iReligion in range(iNumReligions):
		updateReligionSpread(iReligion)
				

# TODO: revisit
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
)