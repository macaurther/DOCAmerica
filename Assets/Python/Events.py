from BugEventManager import g_eventManager as events
import inspect

from Core import *

from GoalHandlers import event_handler_registry

victory_handlers = appenddict()

def handler(event):
	def handler_decorator(func):
		arg_names = inspect.getargspec(func)[0]
		
		def handler_func(args):
			return func(*args[:len(arg_names)])
			
		handler_func.__name__ = func.__name__
		handler_func.__module__ = func.__module__
		handler_func.func_name = func.func_name
				
		events.addEventHandler(event, handler_func)
		return handler_func
		
	return handler_decorator
	
	
def noop(*args, **kwargs):
	pass


def popup_handler(event_id):
	def handler_decorator(func):
		events.addCustomEvent(event_id, func.__name__, func, noop)
		return func
		
	return handler_decorator


def register_victory_handler(event, handler):
	victory_handlers[event].append(handler)
	events.addEventHandler(event, handler)
	

def reset_victory_handlers():
	global victory_handlers
	for event, handlers in victory_handlers.items():
		for handler in handlers:
			if events.hasEventHandler(event, handler):
				events.removeEventHandler(event, handler)
	
	victory_handlers = appenddict()


events.addEvent("firstCity")
events.addEvent("capitalMoved")
events.addEvent("wonderBuilt")
events.addEvent("collapse")
events.addEvent("periodChange")
events.addEvent("playerPeriodChange")
events.addEvent("birth")
events.addEvent("resurrection")
events.addEvent("switch")
events.addEvent("enslave")
events.addEvent("combatGold")
events.addEvent("combatFood")
events.addEvent("sacrificeHappiness")
events.addEvent("prepareBirth")
events.addEvent("flip")
events.addEvent("conquerors")
events.addEvent("improvementBuilt")
events.addEvent("improvementDestroyed")
events.addEvent("EndGameTurn")
events.addEvent("freedSlaves")
events.addEvent("combatResult")


@handler("buildingBuilt")
def capitalMovedOnPalaceBuilt(city, iBuilding):
	if iBuilding == iPalace:
		events.fireEvent("capitalMoved", city)
	
	if iBuilding == iMission:
		makeUnits(city.getOwner(), iCatholicMiss, city.plot(), 1, UnitAITypes.UNITAI_MISSIONARY).adjective("")


@handler("firstCity")
def capitalMovedOnFirstCity(city):
	events.fireEvent("capitalMoved", city)


@handler("cityAcquired")
def capitalMovedOnCityAcquired(iOwner, iNewOwner, city):
	capital_city = capital(iOwner)
	if capital_city and not at(capital_city, city):
		events.fireEvent("capitalMoved", capital_city)


@handler("cityAcquiredAndKept")
def firstCityOnCityAcquiredAndKept(iPlayer, city):
	if data.civs[civ(iPlayer)].bFirstCity:
		events.fireEvent("firstCity", city)
		data.civs[civ(iPlayer)].bFirstCity = False


@handler("cityAcquiredAndKept")
def nativeCityConquered(iPlayer, pCity):
	# Check if city was taken from a Native
	if pCity.getPreviousCiv() in dCivGroups[iCivGroupNativeAmerica] + [iNative]:
		# If a non-native captured it, give a Native Tech and some Immigration
		if not civ(iPlayer) in dCivGroups[iCivGroupNativeAmerica]:
			lPossibleTechs = []
			for iTech in lNativeTechs:
				if not team(iPlayer).isHasTech(iTech):
					lPossibleTechs.append(iTech)
			
			if len(lPossibleTechs) > 0:
				team(iPlayer).setHasTech(random.choice(lPossibleTechs), true, iPlayer, False, True)
			
		# If the conquerer has the Plunder Civic, give some Immigration for conquerer
		if player(iPlayer).hasCivic(iPlunder2):
			iConquerImmigration = 20 + pCity.getPopulation() * 5
			iConquerImmigration *= (3 - gc.getGame().getGameSpeedType())	# Scale based on Game Speed
			gc.getPlayer(iPlayer).changeImmigration(iConquerImmigration)
			message(iPlayer, "TXT_KEY_CONQUER_IMMIGRATION", iConquerImmigration)
		
		# If the conquerer has the Captives or Encomienda Civic, give Native Slave based on the population
		if player(iPlayer).hasCivic(iCaptives1):
			iNumSlaves = max(1, int(pCity.getPopulation() / 2))
			makeUnits(iPlayer, iNativeSlave1, pCity, iNumSlaves, UnitAITypes.UNITAI_WORKER)
			message(iPlayer, 'TXT_KEY_UP_ENSLAVE_WIN', sound='SND_REVOLTEND', event=1, button=infos.unit(iNativeSlave1).getButton(), color=8, location=pCity)
		elif player(iPlayer).hasCivic(iEncomienda2):
			iNumSlaves = max(1, int(pCity.getPopulation() / 2))
			makeUnits(iPlayer, iNativeSlave2, pCity, iNumSlaves, UnitAITypes.UNITAI_WORKER)
			message(iPlayer, 'TXT_KEY_UP_ENSLAVE_WIN', sound='SND_REVOLTEND', event=1, button=infos.unit(iNativeSlave2).getButton(), color=8, location=pCity)


@handler("BeginGameTurn")
def giveAINativeTechs(iGameTurn):
	# If European AI hasn't gotten Native Techs by 1700, help them out
	if iGameTurn == year(1700):
		for iPlayer in dCivGroups[iCivGroupEurope]:
			for iTech in lNativeTechs:
				if not team(iPlayer).isHasTech(iTech):
					team(iPlayer).setHasTech(iTech, true, iPlayer, False, True)


@handler("cityAcquiredAndKept")
def convertOnCityAcquired(iPlayer, pCity):
	if player(iPlayer).hasCivic(iZealotry2):
		if player(iPlayer).getStateReligion() != -1:
			pCity.spreadReligion(player(iPlayer).getStateReligion())


@handler("cityBuilt")
def firstCityOnCityBuilt(city):
	iPlayer = city.getOwner()
	if data.civs[civ(iPlayer)].bFirstCity:
		events.fireEvent("firstCity", city)
		data.civs[civ(iPlayer)].bFirstCity = False

@handler("goodyReceived")
# Give a popup to show what Tribe gave gift
def goodyPopup(iPlayer, pPlot, pUnit, iGoodyType):
	if pPlot.getImprovementType() == iAlliedTribe:
		strMessage = "A Tribe's Chieftan has given us a gift in honor of our new alliance!"
		CyInterface().addMessage(iPlayer, False, 20, strMessage, "", 0, gc.getImprovementInfo(iTribe).getButton(), ColorTypes(0), pPlot.getX(), pPlot.getY(), True, True)
	elif pPlot.getImprovementType() == iContactedTribe:
		strMessage = "A Tribe's Chieftan has given us a gift in honor of our meeting!"
		CyInterface().addMessage(iPlayer, False, 20, strMessage, "", 0, gc.getImprovementInfo(iTribe).getButton(), ColorTypes(0), pPlot.getX(), pPlot.getY(), True, True) 


@handler("buildingBuilt")
def wonderBuiltOnBuildingBuilt(city, iBuilding):
	if isWorldWonderClass(infos.building(iBuilding).getBuildingClassType()):
		events.fireEvent("wonderBuilt", city, iBuilding)


@handler("PythonReloaded")
def resetHandlersOnPythonReloaded():
	event_handler_registry.reset()


@handler("OnLoad")
def resetHandlersOnLoad():
	event_handler_registry.reset()


@handler("combatResult")
def onCombatResult(pWinner, pLoser):
	iWinner = pWinner.getOwner()
	
	if pWinner.getUnitType() == iWaaKaulua:
		if pLoser.getUnitType() in (iCaravel, iCarrack, iIndiaman, iWestIndianman, iBrigantine, iSloop, iFrigate, iBarque, iShipOfTheLine, iManOfWar):
			if not pWinner.isFull():
				pCannon = makeUnit(iWinner, unique_unit(iWinner, iCannon), (pWinner.getX(), pWinner.getY()), UnitAITypes.UNITAI_ATTACK)
				pCannon.setTransportUnit(pWinner)
