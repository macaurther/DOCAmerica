# Rhye's and Fall of Civilization - Dynamic resources

from CvPythonExtensions import *
import CvUtil
import PyHelpers
from Core import *
from RFCUtils import * # edead
from StoredData import data

from Events import handler


@handler("GameStart")
def setupOnGameStart():
	setup()
	
@handler("OnLoad")
def setupOnLoad():
	setup()

@handler("PythonReloaded")
def setupOnPythonReloaded():
	setup()

def setup():
	global dResources
	dResources = TileDict(dResourcesDict, year)
	
	global dSpawnResources
	dSpawnResources = TileDict(dSpawnResourcesDict)
	
	global dRemovedResources
	dRemovedResources = TileDict(dRemovedResourcesDict, year)
	
	global dPlotTypes
	dPlotTypes = TileDict(dPlotTypesDict, year)
	
	global dFeatures
	dFeatures = TileDict(dFeaturesDict, year)
	
	for tile in lNewfoundlandCapes:
		dFeatures[tile] = (700, iCape)
	
	global dRemovedFeatures
	dRemovedFeatures = TileDict(dRemovedFeaturesDict, year)
	
	global dConquerorPlotTypes
	dConquerorPlotTypes = TileDict(dConquerorPlotTypesDict)
	
	global dConquerorRemovedFeatures
	dConquerorRemovedFeatures = TileDict(dConquerorRemovedFeaturesDict)
	
	for tile in lNewfoundlandCapes:
		dRemovedFeatures[tile] = 1500
		
	global dRoutes
	dRoutes = appenddict(dict((year(iYear), tiles) for iYear, tiles in dRoutesDict.items()))


### Constants ###

# initialise bonuses variables

lSilkRoute = [(85,48), (86,49), (87,48), (88,47), (89,46), (90,47), (90,45), (91,47), (91,45), (92,48), (93,48), (93,46), (94,47), (95,47), (96,47), (97,47), (98,47), (99,46)]
lNewfoundlandCapes = [(34, 52), (34, 53), (34, 54), (35, 52), (36, 52), (35, 55), (35, 56), (35, 57), (36, 51), (36, 58), (36, 59)]

dResourcesDict = {
	(29, 52)  : (1600,  iCow),     # Montreal
	(18, 53)  : (1600,  iCow),     # Alberta
	(12, 52)  : (1600,  iCow),     # British Columbia
	(28, 46)  : (1600,  iCow),     # Washington area
	(30, 49)  : (1600,  iCow),     # New York area
	(23, 42)  : (1600,  iCow),     # Jacksonville area
	(18, 46)  : (1600,  iCow),     # Colorado
	(20, 45)  : (1600,  iCow),     # Texas
	(37, 14)  : (1600,  iCow),     # Argentina
	(33, 11)  : (1600,  iCow),     # Argentina
	(35, 10)  : (1600,  iCow),     # Pampas
	(24, 43)  : (1600,  iCotton),  # near Florida
	(23, 45)  : (1600,  iCotton),  # Louisiana
	(22, 44)  : (1600,  iCotton),  # Louisiana
	(13, 45)  : (1600,  iCotton),  # California
	(26, 49)  : (1600,  iPig),     # Lakes
	(19, 51)  : (1600,  iSheep),   # Canadian border
	(19, 48)  : (1600,  iWheat),   # Midwest
	(20, 53)  : (1600,  iWheat),   # Manitoba
	(22, 33)  : (1600,  iBanana),  # Guatemala
	(27, 31)  : (1600,  iBanana),  # Colombia
	(43, 23)  : (1600,  iBanana),  # Brazil
	(39, 26)  : (1600,  iBanana),  # Brazil
	(16, 54)  : (1700,  iHorse),   # Alberta
	(26, 45)  : (1700,  iHorse),   # Washington area
	(21, 48)  : (1700,  iHorse),   # Midwest
	(19, 45)  : (1700,  iHorse),   # Texas
	(17, 42)  : (1700,  iHorse),   # Mexico
	(40, 25)  : (1700,  iHorse),   # Brazil
	(33, 10)  : (1700,  iHorse),   # Buenos Aires area
	(32, 8)   : (1700,  iHorse),   # Pampas
	(30, 30)  : (1700,  iHorse),   # Venezuela
	(27, 36)  : (1700,  iSugar),   # Caribbean
	(39, 25)  : (1700,  iSugar),   # Brazil
	(37, 20)  : (1700,  iSugar),   # inner Brazil
	(29, 37)  : (1700,  iSugar),   # Hispaniola
	(38, 18)  : (1700,  iCoffee),  # Brazil
	(39, 20)  : (1700,  iCoffee),  # Brazil
	(38, 22)  : (1700,  iCoffee),  # Brazil
	(27, 30)  : (1700,  iCoffee),  # Colombia
	(29, 30)  : (1700,  iCoffee),  # Colombia
	(26, 27)  : (1700,  iCoffee),  # Colombia
	(39, 16)  : (1700,  iFish),    # Brazil
	(12, 45)  : (1850,  iWine),    # California
	(31, 10)  : (1850,  iWine),    # Andes
	(12, 49)  : (1850,  iRice),    # California
	(11, 45)  : (1850,  iFish),    # California
	(1, 38)   : (1850,  iSugar),   # Hawaii
	(5, 36)   : (1850,  iBanana),  # Hawaii
}

dSpawnResourcesDict = {
	(17, 41) : (iMexico,    iHorse),
	(16, 42) : (iMexico,    iIron),
	(28, 31) : (iColombia,  iIron),
	(31, 10) : (iArgentina, iWine),
	(31, 6)  : (iArgentina, iSheep),
	(32, 11) : (iArgentina, iIron),
	(36, 18) : (iBrazil,    iCorn),
	(42, 18) : (iBrazil,    iFish),
}

dRemovedResourcesDict = {
}

dRoutesDict = {
}

dSpawnRoutes = {
}

# there must be stuff like this elsewhere, maybe barbs?
dPlotTypesDict = {
}

dFeaturesDict = {
	(35, 54) : (700,  iMud),         # Newfoundland obstacles
	(11, 46) : (1850, iFloodPlains), # California
	(11, 47) : (1850, iFloodPlains), # California
	(11, 48) : (1850, iFloodPlains), # California
}

dRemovedFeaturesDict = {
}

dConquerorPlotTypesDict = {
	(29, 23) : (iInca, PlotTypes.PLOT_HILLS),
	(31, 13) : (iInca, PlotTypes.PLOT_HILLS),
	(32, 19) : (iInca, PlotTypes.PLOT_HILLS),
	(27, 29) : (iInca, PlotTypes.PLOT_HILLS),
}

dConquerorRemovedFeaturesDict = {
	(27, 30) : iInca,
	(28, 31) : iInca,
}


@handler("BeginGameTurn")
def createResources():
	for (x, y), iResource in dResources[game.getGameTurn()]:
		createResource(x, y, iResource)


@handler("prepareBirth")
def createResourcesBeforeBirth(iCiv):
	for (x, y), iResource in dSpawnResources[iCiv]:
		createResource(x, y, iResource)


@handler("collapse")
def removeResourcesOnCollapse(iPlayer):
	iCiv = civ(iPlayer)
	for (x, y), iResource in dSpawnResources[iCiv]:
		removeResource(x, y)


@handler("birth")
def removeColombianJungle(iPlayer):
	if civ(iPlayer) == iColombia:
		plot(28, 31).setFeatureType(-1, 0)


@handler("BeginGameTurn")
def removeResources():
	for x, y in dRemovedResources[game.getGameTurn()]:
		removeResource(x, y)


@handler("BeginGameTurn")
def createRoutes():
	for tile in dRoutes[game.getGameTurn()]:
		plot(tile).setRouteType(iRouteRoad)


@handler("prepareBirth")
def createRoutesBeforeSpawn(iCiv):
	for tile in dSpawnRoutes.get(iCiv, []):
		plot(tile).setRouteType(iRouteRoad)


@handler("BeginGameTurn")
def changePlotType():
	for tile, type in dPlotTypes[game.getGameTurn()]:
		plot(tile).setPlotType(type, True, True)


@handler("BeginGameTurn")
def createFeatures():
	for tile, iFeature in dFeatures[game.getGameTurn()]:
		plot(tile).setFeatureType(iFeature, 0)


@handler("BeginGameTurn")
def removeFeatures(iGameTurn):
	for tile in dRemovedFeatures[game.getGameTurn()]:
		plot(tile).setFeatureType(-1, 0)


@handler("conquerors")
def changeConquerorPlotTypes(iConquerorPlayer, iTargetPlayer):
	iTargetCiv = civ(iTargetPlayer)
	for tile, type in dConquerorPlotTypes[iTargetCiv]:
		plot(tile).setPlotType(type, True, True)


@handler("conquerors")
def removeConquerorFeatures(iConquerorPlayer, iTargetPlayer):
	iTargetCiv = civ(iTargetPlayer)
	for tile in dConquerorRemovedFeatures[iTargetCiv]:
		plot(tile).setFeatureType(-1, 0)


def setupScenarioResources():
	setup()
	iStartTurn = scenarioStartTurn()
	
	for iTurn, lResources in dResources:
		if iTurn <= iStartTurn:
			for (x, y), iResource in lResources:
				createResource(x, y, iResource)
	
	for iCiv, lResources in dSpawnResources:
		if year(dBirth[iCiv]) <= iStartTurn and any(iEnd >= iStartTurn for iStart, iEnd in dResurrections[iCiv]):
			for (x, y), iResource in lResources:
				createResource(x, y, iResource)
	
	for iTurn, lResources in dRemovedResources:
		if iTurn <= iStartTurn:
			for x, y in lResources:
				removeResource(x, y)
	
	for iTurn, lRoutes in dRoutes.items():
		if iTurn <= iStartTurn:
			for x, y in lRoutes:
				plot(x, y).setRouteType(iRouteRoad)
	
	for iTurn, lPlots in dPlotTypes:
		if iTurn <= iStartTurn:
			for (x, y), iPlotType in lPlots:
				plot(x, y).setPlotType(iPlotType, True, True)
	
	for iTurn, lFeatures in dFeatures:
		if iTurn <= iStartTurn:
			for (x, y), iFeature in lFeatures:
				plot(x, y).setFeatureType(iFeature, 0)
	
	for iTurn, lFeatures in dRemovedFeatures:
		if iTurn <= iStartTurn:
			for x, y in lFeatures:
				plot(x, y).setFeatureType(-1, 0)
	
	if year(700) <= iStartTurn:
		plot(41, 58).setFeatureType(-1, 0)
				
	for iCiv, lPlots in dConquerorPlotTypes:
		if year(dFall[iCiv]) <= iStartTurn:
			for (x, y), iPlotType in lPlots:
				plot(x, y).setPlotType(iPlotType, True, True)
	
	for iCiv, lFeatures in dConquerorRemovedFeatures:
		if year(dFall[iCiv]) <= iStartTurn:
			for x, y in lFeatures:
				plot(x, y).setFeatureType(-1, 0)
		

# Leoreth: bonus removal alerts by edead
def createResource(iX, iY, iBonus, createTextKey="TXT_KEY_MISC_DISCOVERED_NEW_RESOURCE", removeTextKey="TXT_KEY_MISC_EVENT_RESOURCE_EXHAUSTED"):
	"""Creates a bonus resource and alerts the plot owner"""
	plot = plot_(iX, iY)
	
	iRemovedBonus = plot.getBonusType(-1) # for alert
	
	if iRemovedBonus == iBonus:
		return
	
	plot.setBonusType(iBonus)
			
	if iBonus == -1:
		iImprovement = plot.getImprovementType()
		if iImprovement >= 0:
			if infos.improvement(iImprovement).isImprovementBonusTrade(iRemovedBonus):
				plot.setImprovementType(-1)
		
	iOwner = plot.getOwner()
	if iOwner >= 0: # only show alert to the tile owner
		bWater = plot.isWater()
		closest = closestCity(plot, iOwner, same_continent=not bWater, coastal_only=bWater)
		
		if iRemovedBonus >= 0:
			notifyResource(iOwner, closest, iX, iY, iRemovedBonus, removeTextKey)
		
		if iBonus >= 0:
			notifyResource(iOwner, closest, iX, iY, iBonus, createTextKey)


def notifyResource(iPlayer, city, iX, iY, iBonus, textKey):
	if not city: return
	if scenarioStart(): return
	
	if infos.bonus(iBonus).getTechReveal() == -1 or team(iPlayer).isHasTech(infos.bonus(iBonus).getTechReveal()):
		message(iPlayer, textKey, infos.bonus(iBonus).getText(), city.getName(), event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.bonus(iBonus).getButton(), location=(iX, iY))


def removeResource(iX, iY):
	"""Removes a bonus resource and alerts the plot owner"""
	if plot(iX, iY).getBonusType(-1) == -1: return
	createResource(iX, iY, -1)