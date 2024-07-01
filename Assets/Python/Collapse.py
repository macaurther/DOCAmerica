from Core import *
from RFCUtils import *
from Secession import *

from Slots import getImpact, getNextBirth, allSlotsTaken
from Events import events, handler


@handler("BeginGameTurn")
def checkScheduledCollapse():
	for iPlayer in players.major():
		if data.players[iPlayer].iTurnsToCollapse == 0:
			if player(iPlayer).isExisting():
				completeCollapse(iPlayer)
			data.players[iPlayer].iTurnsToCollapse = -1
		elif data.players[iPlayer].iTurnsToCollapse > 0:
			data.players[iPlayer].iTurnsToCollapse -= 1

@handler("BeginGameTurn")
def checkAvailableSlots():
	if allSlotsTaken():
		iNextCiv = getNextBirth()
		if iNextCiv is not None:
			freeSlotFor(iNextCiv)
			

def freeSlotFor(iCiv):
	iCivImpact = getImpact(iCiv)
	availableSlots = players.major().alive().where(lambda p: getImpact(civ(p)) <= iCivImpact)
	metric = lambda iPlayer: (getImpact(civ(iPlayer)), until(year(dFall[iPlayer])))
	
	iSlot = availableSlots.where(lambda p: stability(p) == iStabilityCollapsing).minimum(metric)
	if iSlot is not None:
		completeCollapse(iSlot)
		return
	
	iSlot = availableSlots.where(lambda p: stability(p) == iStabilityUnstable and since(year(dFall[p])) >= 0).minimum(metric)
	if iSlot is not None:
		completeCollapse(iSlot)
		return
	
	iSlot = availableSlots.where(lambda p: stability(p) == iStabilityUnstable and getImpact(civ(p)) < iCivImpact).minimum(metric)
	if iSlot is not None:
		completeCollapse(iSlot)
	
def scheduleCollapse(iPlayer):
	data.players[iPlayer].iTurnsToCollapse = 1
	
def completeCollapse(iPlayer):
	# before cities are seceded, downgrade their cottages
	downgradeCottages(iPlayer)
	
	# secede all cities, destroy close and less important ones
	bRazeMinorCities = (player(iPlayer).getCurrentEra() <= iColonialEra)
	secedeCities(iPlayer, cities.owner(iPlayer), bRazeMinorCities)
		
	# take care of the remnants of the civ
	player(iPlayer).killUnits()
	
	# remove human vision so their slot can be safely reassigned
	resetRevealedOwner(iPlayer)
		
	message(active(), 'TXT_KEY_STABILITY_COMPLETE_COLLAPSE', adjective(iPlayer))
	
	events.fireEvent("collapse", iPlayer)
		
def downgradeCottages(iPlayer):
	for plot in plots.all().owner(iPlayer):
		iImprovement = plot.getImprovementType()
		
		if iImprovement == iTown: 
			plot.setImprovementType(iHamlet)
		elif iImprovement == iVillage: 
			plot.setImprovementType(iCottage)
		elif iImprovement == iHamlet: 
			plot.setImprovementType(iCottage)
		elif iImprovement == iCottage: 
			plot.setImprovementType(-1)
		
		# MacAurther: Also destroy forts
		if iImprovement == iFort: 
			plot.setImprovementType(-1)
		
		# Destroy all Mississippi improvements and routes
		if civ(iPlayer) == iMississippi and not player(iPlayer).isHuman():
			if iImprovement >= 0 and not iImprovement in [iTribe, iContactedTribe]:
				plot.setImprovementType(-1)
			iRoute = plot.getRouteType()
			if iRoute >= 0:
				plot.setRouteType(-1)
			
	message(iPlayer, 'TXT_KEY_STABILITY_DOWNGRADE_COTTAGES', color=iRed)
		
def collapseToCore(iPlayer):
	nonCoreCities = cities.owner(iPlayer).where(lambda city: not city.isPlayerCore(iPlayer))
	ahistoricalCities = nonCoreCities.where(lambda city: plot(city).getPlayerSettlerValue(iPlayer) < 90)
	
	# release all vassals
	for iVassal in players.vassals(iPlayer):
		team(iVassal).setVassal(player(iPlayer).getTeam(), False, False)
				
	# more than half ahistorical, only secede ahistorical cities
	if 2 * ahistoricalCities.count() > nonCoreCities.count():
	
		# notify owner
		message(iPlayer, 'TXT_KEY_STABILITY_FOREIGN_SECESSION', color=iRed)
				
		# secede all foreign cities
		secession(iPlayer, ahistoricalCities)
		
	# otherwise, secede all cities outside of core
	elif nonCoreCities:
	
		# notify owner
		message(iPlayer, 'TXT_KEY_STABILITY_COLLAPSE_TO_CORE', color=iRed)
			
		# secede all non-core cities
		secession(iPlayer, nonCoreCities)