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
	
	global dRemovedFeatures
	dRemovedFeatures = TileDict(dRemovedFeaturesDict, year)
	
	global dConquerorPlotTypes
	dConquerorPlotTypes = TileDict(dConquerorPlotTypesDict)
	
	global dConquerorRemovedFeatures
	dConquerorRemovedFeatures = TileDict(dConquerorRemovedFeaturesDict)
		
	global dRoutes
	dRoutes = appenddict(dict((year(iYear), tiles) for iYear, tiles in dRoutesDict.items()))


### Constants ###

# initialise bonuses variables
dResourcesDict = {
	(13, 63)  : (1550,  iHorse),  	# Mexico
	(15, 89)  : (1550,  iHorse),  	# Utah
	(22, 79)  : (1550,  iHorse),  	# Texas
	(24, 88)  : (1550,  iHorse),  	# Nebraska
	(28, 63)  : (1550,  iHorse),  	# Cuba
	(31, 79)  : (1550,  iHorse),  	# Kentucky
	(37, 75)  : (1550,  iHorse),  	# North Carolina
	(45, 91)  : (1550,  iHorse),  	# Quebec
	(20, 11)  : (1550,  iHorse),  	# Argentina
	(24, 28)  : (1550,  iHorse),  	# Peru
	(26, 13)  : (1550,  iHorse),  	# Argentina
	(27, 16)  : (1550,  iHorse),  	# Argentina
	(30, 46)  : (1550,  iHorse),  	# Colombia
	(37, 45)  : (1550,  iHorse),  	# Venezuela
	(56, 27)  : (1550,  iHorse),  	# Brazil
	(32, 72)  : (1600,  iCotton),  	# Georgia
	(35, 73)  : (1600,  iCotton),  	# South Carolina
	(35, 75)  : (1600,  iCotton),  	# North Carolina
	(29, 73)  : (1600,  iCotton), 	# Alabama
	(28, 77)  : (1600,  iCotton),  	# Mississippi
	(22, 76)  : (1600,  iCotton),  	# Texas
	(17, 73)  : (1600,  iCotton),  	# Texas
	(49, 87)  : (1600,  iPotato),  	# New Brunswick
	(33, 87)  : (1600,  iPotato),  	# Michigan
	(24, 96)  : (1600,  iPotato),  	# North Dakota
	(16, 93)  : (1600,  iPotato),  	# Idaho
	(11, 96)  : (1600,  iPotato),  	# Oregon
	(37, 77)  : (1600,  iTobacco), 	# Virginia
	(37, 74)  : (1600,  iTobacco), 	# South Carolina
	(29, 75)  : (1600,  iTobacco), 	# Alabama
	(33, 80)  : (1600,  iTobacco), 	# Kentucky
}

dSpawnResourcesDict = {
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
	(8, 92) : (1850, iFloodPlains), # California
	(9, 92) : (1850, iFloodPlains), # California
	(8, 91) : (1850, iFloodPlains), # California
    (9, 90) : (1850, iFloodPlains), # California
	(9, 89) : (1850, iFloodPlains), # California
}

dRemovedFeaturesDict = {
	(10, 85)  : 1300,  # Southwest Flood Plains
	(11, 84)  : 1300,  # Southwest Flood Plains
	(13, 84)  : 1300,  # Southwest Flood Plains
	(13, 79)  : 1300,  # North Mexico Flood Plains
	(15, 78)  : 1300,  # North Mexico Flood Plains
}

dConquerorPlotTypesDict = {
}

dConquerorRemovedFeaturesDict = {
	(28, 44) : iInca,
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