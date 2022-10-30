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
# MacAurther TODO: Put these capes on the map
lNewfoundlandCapes = [(68, 82), (69, 93), (68, 93), (67, 93), (71, 91), (71, 90), (38, 91)]

dResourcesDict = {
	(37, 60)  : (1600,  iBanana),  # Yucatan
	(39, 56)  : (1600,  iBanana),  # Guatemala
	(41, 52)  : (1600,  iBanana),  # Costa Rica
	(48, 52)  : (1600,  iBanana),  # Colombia
	(45, 44)  : (1600,  iBanana),  # Ecuador
	(59, 49)  : (1600,  iBanana),  # Guyana
	(63, 48)  : (1600,  iBanana),  # French Guyana
	(68, 42)  : (1600,  iBanana),  # Brazil
	(67, 29)  : (1600,  iBanana),  # Brazil
	(63, 25)  : (1600,  iBanana),  # Brazil
	(61, 21)  : (1600,  iBanana),  # Brazil
	(46, 68)  : (1600,  iCitrus),  # Florida
	(42, 69)  : (1600,  iCitrus),  # Florida
	(43, 60)  : (1600,  iCitrus),  # Cuba
	(53, 59)  : (1600,  iCitrus),  # Haiti
	(16, 79)  : (1600,  iCitrus),  # California
	(18, 71)  : (1600,  iCitrus),  # Mexico
	(31, 67)  : (1600,  iCitrus),  # Texas
	(29, 63)  : (1600,  iCitrus),  # Mexico
	(37, 62)  : (1600,  iCitrus),  # Yucatan
	(52, 52)  : (1600,  iCitrus),  # Venezuela
	(61, 49)  : (1600,  iCitrus),  # Suriname
	(47, 42)  : (1600,  iCitrus),  # Peru
	(53, 37)  : (1600,  iCitrus),  # Peru
	(74, 37)  : (1600,  iCitrus),  # Brazil
	(61, 18)  : (1600,  iCitrus),  # Uruguay
	(64, 26)  : (1600,  iCoffee),  # Brazil
	(69, 28)  : (1600,  iCoffee),  # Brazil
	(73, 33)  : (1600,  iCoffee),  # Brazil
	(75, 38)  : (1600,  iCoffee),  # Brazil
	(50, 49)  : (1600,  iCoffee),  # Colombia
	(47, 52)  : (1600,  iCoffee),  # Colombia
	(44, 46)  : (1600,  iCoffee),  # Ecuador
	(40, 54)  : (1600,  iCoffee),  # Honduras
	(45, 72)  : (1600,  iCotton),  # Georgia
	(48, 74)  : (1600,  iCotton),  # South Carolina
	(50, 75)  : (1600,  iCotton),  # North Carolina
	(41, 71)  : (1600,  iCotton),  # Alabama
	(39, 74)  : (1600,  iCotton),  # Mississippi
	(33, 72)  : (1600,  iCotton),  # Texas
	(31, 69)  : (1600,  iCotton),  # Texas
	(56, 87)  : (1600,  iCow),     # Quebec
	(48, 84)  : (1600,  iCow),     # Ontario
	(31, 91)  : (1600,  iCow),     # Manitoba
	(26, 92)  : (1600,  iCow),     # Saskatchewan
	(23, 94)  : (1600,  iCow),     # Alberta
	(16, 93)  : (1600,  iCow),     # British Columbia
	(55, 82)  : (1600,  iCow),     # New York
	(50, 84)  : (1600,  iCow),     # New York
	(52, 80)  : (1600,  iCow),     # Maryland
	(43, 73)  : (1600,  iCow),     # World famous Butts County Dairy
	(32, 69)  : (1600,  iCow),     # Texas
	(30, 71)  : (1600,  iCow),     # Texas
	(26, 75)  : (1600,  iCow),     # New Mexico
	(31, 67)  : (1600,  iCow),     # Oklahoma
	(27, 79)  : (1600,  iCow),     # Colorado
	(33, 84)  : (1600,  iCow),     # Iowa
	(39, 83)  : (1600,  iCow),     # Wisconsin
	(36, 85)  : (1600,  iCow),     # Wisconsin
	(42, 84)  : (1600,  iCow),     # Michigan
	(28, 82)  : (1600,  iCow),     # Wyoming
	(30, 88)  : (1600,  iCow),     # South Dakota
	(25, 87)  : (1600,  iCow),     # Montana
	(27, 79)  : (1600,  iCow),     # Colorado
	(16, 78)  : (1600,  iCow),     # California
	(31, 85)  : (1600,  iCow),     # Idaho
	(47, 60)  : (1600,  iCow),     # Cuba
	(24, 70)  : (1600,  iCow),     # Mexico
	(24, 66)  : (1600,  iCow),     # Mexico
	(33, 59)  : (1600,  iCow),     # Mexico
	(40, 52)  : (1600,  iCow),     # Costa Rica
	(49, 52)  : (1600,  iCow),     # Venezuela
	(56, 33)  : (1600,  iCow),     # Brazil
	(58, 30)  : (1600,  iCow),     # Brazil
	(70, 38)  : (1600,  iCow),     # Brazil
	(65, 36)  : (1600,  iCow),     # Brazil
	(67, 32)  : (1600,  iCow),     # Brazil
	(75, 40)  : (1600,  iCow),     # Brazil
	(65, 28)  : (1600,  iCow),     # Brazil
	(59, 18)  : (1600,  iCow),     # Uruguay
	(60, 25)  : (1600,  iCow),     # Paraguay
	(58, 22)  : (1600,  iCow),     # Argentina
	(56, 18)  : (1600,  iCow),     # Argentina
	(55, 16)  : (1600,  iCow),     # Argentina
	(57, 17)  : (1600,  iCow),     # Argentina
	(54, 12)  : (1600,  iCow),     # Argentina
	(47, 13)  : (1600,  iCow),     # Chile
	(26, 94)  : (1700,  iHorse),   # Alberta
	(55, 89)  : (1700,  iHorse),   # Quebec
	(49, 75)  : (1700,  iHorse),   # North Carolina
	(41, 67)  : (1700,  iHorse),   # Kentucky
	(45, 81)  : (1700,  iHorse),   # Ohio
	(32, 73)  : (1700,  iHorse),   # Texas
	(29, 86)  : (1700,  iHorse),   # South Dakota
	(23, 84)  : (1700,  iHorse),   # Utah
	(30, 58)  : (1700,  iHorse),   # Mexico
	(42, 62)  : (1700,  iHorse),   # Cuba
	(47, 51)  : (1700,  iHorse),   # Colombia
	(64, 23)  : (1700,  iHorse),   # Brazil
	(57, 19)  : (1700,  iHorse),   # Argentina
	(57, 24)  : (1700,  iHorse),   # Argentina
	(59, 88)  : (1600,  iPig),     # Quebec
	(50, 86)  : (1600,  iPig),     # Ontario
	(29, 92)  : (1600,  iPig),     # Manitoba
	(24, 91)  : (1600,  iPig),     # Alberta
	(54, 81)  : (1600,  iPig),     # Pennsylvania
	(48, 82)  : (1600,  iPig),     # Pennsylvania
	(51, 75)  : (1600,  iPig),     # North Carolina
	(42, 80)  : (1600,  iPig),     # Indiana
	(37, 81)  : (1600,  iPig),     # Illinois
	(32, 85)  : (1600,  iPig),     # Nebraska
	(30, 80)  : (1600,  iPig),     # Kansas
	(49, 61)  : (1600,  iPig),     # Cuba
	(30, 62)  : (1600,  iPig),     # Mexico
	(62, 22)  : (1600,  iPig),     # Brazil
	(46, 50)  : (1600,  iPig),     # Colombia
	(64, 87)  : (1600,  iPotato),  # New Brunswick
	(42, 84)  : (1600,  iPotato),  # Michigan
	(37, 85)  : (1600,  iPotato),  # Wisconsin
	(27, 88)  : (1600,  iPotato),  # North Dakota
	(31, 89)  : (1600,  iPotato),  # North Dakota
	(32, 92)  : (1600,  iPotato),  # Manitoba
	(30, 85)  : (1600,  iPotato),  # Idaho
	(18, 87)  : (1600,  iPotato),  # Oregon
	(23, 83)  : (1600,  iPotato),  # Utah
	(37, 70)  : (1600,  iRice),    # Louisiana
	(34, 74)  : (1600,  iRice),    # Arkansas
	(39, 73)  : (1600,  iRice),    # Mississippi
	(36, 77)  : (1600,  iRice),    # Missouri
	(14, 80)  : (1600,  iRice),    # California
	(35, 58)  : (1600,  iRice),    # Mexico
	(63, 47)  : (1600,  iRice),    # French Guyana
	(61, 20)  : (1600,  iRice),    # Brazil
	(54, 58)  : (1600,  iRice),    # Hispaniola
	(23, 81)  : (1600,  iSheep),   # Utah
	(28, 63)  : (1600,  iSheep),   # Mexico
	(54, 30)  : (1600,  iSheep),   # Bolivia
	(56, 28)  : (1600,  iSheep),   # Bolivia
	(73, 38)  : (1600,  iSheep),   # Brazil
	(61, 18)  : (1600,  iSheep),   # Uruguay
	(48, 5)  : (1600,  iSheep),    # Argentina
	(49, 8)  : (1600,  iSheep),    # Argentina
	(50, 10)  : (1600,  iSheep),   # Argentina
	(50, 60)  : (1600,  iSugar),   # Cuba
	(51, 58)  : (1600,  iSugar),   # Haiti
	(52, 60)  : (1600,  iSugar),   # Haiti
	(45, 69)  : (1600,  iSugar),   # Florida
	(40, 75)  : (1600,  iSugar),   # Mississippi
	(62, 56)  : (1600,  iSugar),   # Caribbean
	(70, 29)  : (1600,  iSugar),   # Brazil
	(30, 32)  : (1600,  iSugar),   # Brazil
	(63, 38)  : (1600,  iSugar),   # Brazil
	(5, 54)   : (1600,  iSugar),   # Hawaii
	(13, 47)  : (1600,  iSugar),   # Hawaii
	(49, 77)  : (1600,  iTobacco), # Virginia
	(47, 74)  : (1600,  iTobacco), # South Carolina
	(21, 41)  : (1600,  iTobacco), # Alabama
	(44, 77)  : (1600,  iTobacco), # Kentucky
	(43, 81)  : (1600,  iWheat),   # Indiana
	(31, 92)  : (1600,  iWheat),   # Manitoba
	(27, 93)  : (1600,  iWheat),   # Saskatchewan
	(29, 90)  : (1600,  iWheat),   # North Dakota
	(32, 82)  : (1600,  iWheat),   # Iowa
	(34, 79)  : (1600,  iWheat),   # Missouri
	(28, 80)  : (1600,  iWheat),   # Colorado
	(30, 75)  : (1600,  iWheat),   # Oklahoma
	(20, 89)  : (1600,  iWheat),   # Washington
	(55, 13)  : (1600,  iWheat),   # Argentina
	(54, 19)  : (1600,  iWheat),   # Argentina
	(44, 80)  : (1600,  iWine),    # Ohio
	(16, 82)  : (1600,  iWine),    # California
	(25, 68)  : (1600,  iWine),    # Mexico
	(57, 15)  : (1600,  iWine),    # Argentina
	(52, 15)  : (1600,  iWine),    # Argentina
	(53, 12)  : (1600,  iWine),    # Argentina
	(48, 14)  : (1600,  iWine),    # Chile
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
	(16, 78) : (1850, iFloodPlains), # California
	(16, 81) : (1850, iFloodPlains), # California
	(15, 82) : (1850, iFloodPlains), # California
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