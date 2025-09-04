from RFCUtils import *
from Locations import *
from Core import *

from Events import handler, popup_handler


# initialise coordinates

dCatholicPreference = CivDict({
iSpain		: 95,
iFrance		: 75,
iEngland	: 30,
iNetherlands: 10,
iPortugal	: 95,
iAmerica	: 20,
}, 50)

def getCatholicPreference(iPlayer):
	return dCatholicPreference[iPlayer]
	

@handler("BeginGameTurn")
def foundReligions():
	if turn() == year(30):
		foundReligion(tHolyCity, iCatholicism)
	if turn() == year(33):
		foundReligion(tHolyCity, iOrthodoxy)
	if turn() == year(610):
		foundReligion(tHolyCity, iIslam)
	if turn() == year(1521):
		foundReligion(tHolyCity, iProtestantism)


@handler("BeginGameTurn")
def spreadJudaism():
	spreadReligionToRegion(iJudaism, [rOntario, rNewEngland, rMidAtlantic], 1850, 10)

@handler("religionSpread")
def replacePaganTemple(iReligion, iPlayer, city):
	iUniquePaganTemple = unique_building(iPlayer, iPaganTemple)
	if city.isHasRealBuilding(iUniquePaganTemple):
		city.setHasRealBuilding(iUniquePaganTemple, False)
		
		iStateReligion = player(iPlayer).getStateReligion()
		iTemple = temple(iReligion)
		if iStateReligion == iReligion and city.canConstruct(iTemple, False, False, False):
			city.setHasRealBuilding(iTemple, True)
			message(iPlayer, "TXT_KEY_PAGAN_TEMPLE_REPLACED", infos.religion(iReligion).getText(), city.getName(), infos.building(iUniquePaganTemple).getText(), infos.building(iTemple).getText(), event=InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, button=infos.building(iTemple).getButton(), sound=infos.building(iTemple).getConstructSound(), location=city)
		else:
			message(iPlayer, "TXT_KEY_PAGAN_TEMPLE_REMOVED", infos.religion(iReligion).getText(), city.getName(), infos.building(iUniquePaganTemple).getText(), event=InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, location=city)

## IMPLEMENTATION


def foundReligion(location, iReligion):
	if not location:
		return False

	city = city_(location)
	if city:
		game.setHolyCity(iReligion, city, True)
		return True
		
	return False


def selectHolyCity(area, tPreferredCity = None, bAIOnly = True):
	preferredCity = city(tPreferredCity)
	if preferredCity and not (bAIOnly and preferredCity.isHuman()):
		return preferredCity
				
	holyCity = area.cities().where(lambda city: not bAIOnly or not city.isHuman()).random()
	if holyCity:
		return location(holyCity)
		
	return None

	
def spreadReligionToRegion(iReligion, lRegions, iStartDate, iInterval):
	if not game.isReligionFounded(iReligion): return
	if turn() < year(iStartDate): return
	
	if not periodic(iInterval): return
	
	regionCities = cities.regions(*lRegions)
	religionCities = regionCities.religion(iReligion)
	
	if 2 * len(religionCities) < len(regionCities):
		spreadCity = regionCities.where(lambda city: not city.isHasReligion(iReligion) and player(city.getOwner()).getSpreadType(plot(city), iReligion) > ReligionSpreadTypes.RELIGION_SPREAD_NONE).random()
		if spreadCity:
			spreadCity.spreadReligion(iReligion)


def checkLateReligionFounding(iReligion, iTech):
	if infos.religion(iReligion).getTechPrereq() != iTech:
		return
		
	if game.isReligionFounded(iReligion):
		return
		
	allPlayers = players.major().existing()
	techPlayers = allPlayers.tech(iTech)
				
	if 2 * techPlayers.count() >= allPlayers.count():
		foundReligionInCore(iReligion)


def foundReligionInCore(iReligion):
	city = cities.all().where(lambda c: c.plot().getSpreadFactor(iReligion) == RegionSpreadTypes.REGION_SPREAD_CORE).random()
	if city:
		foundReligion(location(city), iReligion)


### popup handlers - transition to using Popups module ###
