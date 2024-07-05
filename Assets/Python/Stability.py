from Core import *
from RFCUtils import *
from Civics import *
from Resurrection import *
from Secession import *
from Collapse import *

from Slots import findSlot
from Events import handler, events

from operator import itemgetter
from datetime import date

import Periods as periods
import Logging as log

import BugPath

import math


tEraAdministrationModifier = (
	100, # ancient
	200, # classical
	200, # exploration
	250, # colonial
	300, # revolutionary
	350, # industrial
	400, # modern
)

dCivilizationAdministrationModifier = CivDict({
}, 0)


@handler("BeginGameTurn")
def crisisCountdown():
	for iPlayer in players.major():
		if getCrisisCountdown(iPlayer) > 0:
			changeCrisisCountdown(iPlayer, -1)


@handler("BeginGameTurn")
def updateTrendScores():
	# calculate economic and happiness stability
	if every(3):
		for iPlayer in players.major():
			updateEconomyTrend(iPlayer)
			updateHappinessTrend(iPlayer)
			
		# calculate war stability
		for iPlayer, iEnemy in players.major().permutations():
			if team(iPlayer).isAtWar(iEnemy):
				updateWarTrend(iPlayer, iEnemy)
		
		for iPlayer, iEnemy in players.major().permutations():
				if team(iPlayer).isAtWar(iEnemy):
					data.players[iPlayer].lLastWarSuccess[iEnemy] = team(iPlayer).AI_getWarSuccess(iEnemy)
				else:
					data.players[iPlayer].lLastWarSuccess[iEnemy] = 0


@handler("BeginGameTurn")
def decayPenalties():
	# decay penalties from razing cities and losing to barbarians
	if every(5):
		if data.iHumanRazePenalty < 0:
			data.iHumanRazePenalty += 2
		for iPlayer in players.major():
			if data.players[iPlayer].iBarbarianLosses > 0:
				data.players[iPlayer].iBarbarianLosses -= 1 + data.players[iPlayer].iBarbarianLosses / 5


@handler("BeginGameTurn")
def checkLostCitiesCollapses():
	if every(12):
		for iPlayer in players.major():
			checkLostCitiesCollapse(iPlayer)
	

@handler("BeginGameTurn")
def updateHumanStability(iGameTurn):
	if iGameTurn >= year(dBirth[active()]):
		data.iHumanStability = calculateStability(active())[0]


@handler("EndPlayerTurn")
def checkSecedingCities(iGameTurn, iPlayer):
	secedingCities = data.getSecedingCities(iPlayer)
	
	if secedingCities:
		secedeCities(iPlayer, secedingCities.existing())
		data.setSecedingCities(iPlayer, cities.of([]))


def triggerCrisis(iPlayer):
	if getCrisisCountdown(iPlayer) > 0:
		return
	
	changeCrisisCountdown(iPlayer, turns(10))
	
	bFall = since(year(dFall[iPlayer])) >= 0
	
	# help AI to not immediately collapse
	if not player(iPlayer).isHuman() and not bFall:
		# with no overexpansion at all, just have a domestic crisis (once until back at shaky again)
		if not data.players[iPlayer].bDomesticCrisis and data.players[iPlayer].lStabilityCategoryValues[0] >= 0:
			domesticCrisis(iPlayer)
			return
		
		# collapse to core if controlling cities outside of core
		if cities.core(iPlayer).owner(iPlayer) < cities.owner(iPlayer) and civ(iPlayer) not in dCivGroups[iCivGroupEurope]: 	# MacAurther: European RP, doesn't have Core
			collapseToCore(iPlayer)
			return

	scheduleCollapse(iPlayer)

@handler("cityAcquired")
def onCityAcquired(iOwner, iPlayer, city, bConquest):
	if not bConquest:
		return
	
	checkStability(iOwner)
	checkLostCoreCollapse(iOwner)
	
	if player(iPlayer).isBarbarian():
		checkBarbarianCollapse(iOwner)

@handler("cityRazed")
def onCityRazed(city, iPlayer):
	iOwner = slot(Civ(city.getPreviousCiv()))
	if iOwner < 0:
		return 
	
	if player(iOwner).isBarbarian():
		return

	if player(iPlayer).isHuman():
		iRazePenalty = -10
		if city.getHighestPopulation() < 5 and not city.isCapital():
			iRazePenalty = -2 * city.getHighestPopulation()
			
		if is_minor(iOwner): iRazePenalty /= 2
			
		data.iHumanRazePenalty += iRazePenalty
		checkStability(iPlayer)

@handler("techAcquired")
def onTechAcquired(iTech, iTeam, iPlayer):
	if year() == scenarioStartTurn():
		return
	
	checkStability(iPlayer)

@handler("vassalState")
def onVassalState(iMaster, iVassal, bVassal, bCapitulated):
	if bVassal and bCapitulated:
		checkStability(iMaster, True)	
		balanceStability(iVassal, iStabilityShaky)

@handler("changeWar")
def onChangeWar(bWar, iTeam, iOtherTeam):
	if not is_minor(iTeam) and not is_minor(iOtherTeam):
		checkStability(iTeam, not bWar)
		checkStability(iOtherTeam, not bWar)
		
		if bWar:
			startWar(iTeam, iOtherTeam)
			startWar(iOtherTeam, iTeam)

@handler("revolution")
def onRevolution(iPlayer):
	checkStability(iPlayer)

@handler("playerChangeStateReligion")
def onPlayerChangeStateReligion(iPlayer):
	checkStability(iPlayer)

@handler("capitalMoved")
def onCapitalMoved(city):
	checkStability(city.getOwner())

@handler("wonderBuilt")
def onWonderBuilt(city, iWonder):
	checkStability(city.getOwner(), True)

@handler("goldenAge")	
def onGoldenAge(iPlayer):
	checkStability(iPlayer, True)

@handler("greatPersonBorn")
def onGreatPersonBorn(unit, iPlayer):
	checkStability(iPlayer, True)

@handler("combatResult")
def onCombatResult(winningUnit, losingUnit):
	if player(winningUnit).isBarbarian() and not is_minor(losingUnit):
		data.players[losingUnit.getOwner()].iBarbarianLosses += 1

def incrementStability(iPlayer):
	setStabilityLevel(iPlayer, min(iStabilitySolid, stability(iPlayer) + 1))
	
def decrementStability(iPlayer):
	setStabilityLevel(iPlayer, max(iStabilityCollapsing, stability(iPlayer) - 1))
	
def getCrisisCountdown(iPlayer):
	return data.players[iPlayer].iCrisisCountdown
	
def changeCrisisCountdown(iPlayer, iChange):
	data.players[iPlayer].iCrisisCountdown += iChange
	
def isImmune(iPlayer):
	pPlayer = player(iPlayer)
	
	# must not be dead
	if not pPlayer.isExisting():
		return True
		
	# only for major civs
	if is_minor(iPlayer):
		return True
		
	# immune right after scenario start
	if turn() < scenarioStartTurn() + turns(20):
		return True
		
	# immune if birth protected
	if pPlayer.isBirthProtected():
		return True
		
	# immune right after birth
	if turn() < pPlayer.getInitialBirthTurn() + turns(20):
		return True
		
	# immune right after resurrection
	if turn() < pPlayer.getLastBirthTurn() + turns(10):
		return True
		
	return False
	
def checkBarbarianCollapse(iPlayer):
	pPlayer = player(iPlayer)
		
	if isImmune(iPlayer): return
		
	iNumCities = pPlayer.getNumCities()
	iLostCities = cities.owner(iBarbarian).where(lambda city: city.isOriginalOwner(iPlayer)).count()
			
	# lost more than half of your cities to barbarians: collapse
	if iLostCities > iNumCities:
		debug('Collapse by barbarians: ' + pPlayer.getCivilizationShortDescription(0))
		message(iPlayer, 'TXT_KEY_STABILITY_MAJOR_BARBARIAN_LOSSES', color=iRed)
		completeCollapse(iPlayer)
		
	# lost at least two cities to barbarians: lose stability
	elif iLostCities >= 2:
		debug('Lost stability to barbarians: ' + pPlayer.getCivilizationShortDescription(0))
		message(iPlayer, 'TXT_KEY_STABILITY_MINOR_BARBARIAN_LOSSES', color=iRed)
		decrementStability(iPlayer)
		
def checkLostCitiesCollapse(iPlayer):
	pPlayer = player(iPlayer)
	
	if isImmune(iPlayer): return
		
	iNumCurrentCities = pPlayer.getNumCities()
	iNumPreviousCities = data.players[iPlayer].iNumPreviousCities
	
	# half or less cities than 12 turns ago: collapse (exceptions for civs with very little cities to begin with -> use lost core collapse)
	if iNumPreviousCities > 2 and 2 * iNumCurrentCities <= iNumPreviousCities:
	
		message(iPlayer, 'TXT_KEY_STABILITY_LOST_CITIES_COLLAPSE', color=iRed)
	
		if stability(iPlayer) == iStabilityCollapsing:
			debug('Collapse by lost cities: ' + pPlayer.getCivilizationShortDescription(0))
			scheduleCollapse(iPlayer)
		else:
			debug('Collapse to core by lost cities: ' + pPlayer.getCivilizationShortDescription(0))
			setStabilityLevel(iPlayer, iStabilityCollapsing)
			collapseToCore(iPlayer)
		
	data.players[iPlayer].iNumPreviousCities = iNumCurrentCities
	
def checkLostCoreCollapse(iPlayer):
	# MacAurther: European RP, doesn't have Core
	if civ(iPlayer) in dCivGroups[iCivGroupEurope]:
		return

	pPlayer = player(iPlayer)
	
	if isImmune(iPlayer): return
	
	lCities = cities.core(iPlayer).owner(iPlayer)
	
	# completely pushed out of core: collapse
	if len(lCities) == 0:
		if periods.evacuate(iPlayer):
			return
			
		message(iPlayer, 'TXT_KEY_STABILITY_LOST_CORE_COLLAPSE', color=iRed)
	
		debug('Collapse from lost core: ' + pPlayer.getCivilizationShortDescription(0))
		scheduleCollapse(iPlayer)

def determineStabilityThreshold(iPlayer, iCurrentLevel):
	iThreshold = 10 * iCurrentLevel - 10
	
	if isDecline(iPlayer): 
		iThreshold += 10
		
		# not that decline already reduces impact by 1
		if getImpact(iPlayer) == iImpactMarginal:
			iThreshold += 5
	
	return iThreshold
	
def determineStabilityLevel(iPlayer, iCurrentLevel, iStability):
	iThreshold = determineStabilityThreshold(iPlayer, iCurrentLevel)
	
	if iStability >= iThreshold: return min(iStabilitySolid, iCurrentLevel + 1)
	elif isDecline(iPlayer): return max(iStabilityCollapsing, iCurrentLevel - (iThreshold - iStability) / 10)
	elif iStability < iThreshold - 10: return max(iStabilityCollapsing, iCurrentLevel - 1)
	
	return iCurrentLevel

def checkStability(iPlayer, bPositive = False, iMaster = -1):
	pPlayer = player(iPlayer)
	
	bVassal = (iMaster != -1)
	
	# no check if already scheduled for collapse
	if data.players[iPlayer].iTurnsToCollapse >= 0: return
	
	# vassal checks are made for triggers of their master civ
	if team(iPlayer).isAVassal() and not bVassal: return
	
	if isImmune(iPlayer): return
		
	# immune to negative stability checks in golden ages
	if pPlayer.isGoldenAge(): bPositive = True
		
	# immune during anarchy
	if pPlayer.isAnarchy(): return
	
	# no repeated stability checks
	if data.players[iPlayer].iLastStabilityTurn == turn(): return
	
	data.players[iPlayer].iLastStabilityTurn = turn()
		
	iStability, lStabilityTypes, lParameters = calculateStability(iPlayer)
	iStabilityLevel = stability(iPlayer)
	bHuman = player(iPlayer).isHuman()
	bFall = isDecline(iPlayer)
	
	iNewStabilityLevel = determineStabilityLevel(iPlayer, iStabilityLevel, iStability)
	
	if iNewStabilityLevel > iStabilityLevel:
		setStabilityLevel(iPlayer, iNewStabilityLevel)
		
	elif not bPositive:
		if iNewStabilityLevel < iStabilityLevel:
			setStabilityLevel(iPlayer, iNewStabilityLevel)
	
		# if remain on collapsing and stability does not improve, collapse ensues
		elif iNewStabilityLevel == iStabilityCollapsing:
			if iStability <= data.players[iPlayer].iLastStability:
				triggerCrisis(iPlayer)
		
	# update stability information
	data.players[iPlayer].iLastStability = iStability
	for i in range(5):
		data.players[iPlayer].lStabilityCategoryValues[i] = lStabilityTypes[i]
	
	for i in range(iNumStabilityParameters):
		pPlayer.setStabilityParameter(i, lParameters[i])
	
	# check vassals
	for iLoopPlayer in players.major():
		if team(iLoopPlayer).isVassal(iPlayer):
			checkStability(iLoopPlayer, bPositive, iPlayer)
		
def domesticCrisis(iPlayer):
	data.players[iPlayer].bDomesticCrisis = True

	iStability = data.players[iPlayer].iLastStability
	iStabilityThreshold = determineStabilityThreshold(iPlayer, iStabilityCollapsing)
	
	iStabilityDifference = iStabilityThreshold - iStability
	if iStabilityDifference >= 0:
		iCrisisTurns = turns(1 + iStabilityDifference / 5)
		
		player(iPlayer).changeAnarchyTurns(iCrisisTurns)
		
		for city in cities.owner(iPlayer):
			city.changeOccupationTimer(iCrisisTurns)
			
		message(iPlayer, 'TXT_KEY_STABILITY_DOMESTIC_CRISIS', iCrisisTurns, color=iRed)

def calculateAdministration(city):
	iPlayer = city.getOwner()

	if not city.isPlayerCore(iPlayer):
		return 0
	
	iPopulation = city.getPopulation()
	iAdministrationModifier = getAdministrationModifier(iPlayer)

	iAdministration = iAdministrationModifier * iPopulation / 100
	
	if city.isCapital():
		iAdministration += iPopulation
	
	return iAdministration
	
def getSeparatismModifier(iPlayer, city):
	iModifier = 0
	
	iCiv = civ(iPlayer)
	
	plot = city.plot()
	civic = civics(iPlayer)
	
	bHistorical = plot.getPlayerSettlerValue(iPlayer) >= 90
	bFall = since(year(dFall[iPlayer])) >= 0
	
	iTotalCulture = civs.major().sum(lambda c: plot.isCore(c) and 2 * plot.getCivCulture(c) or plot.getCivCulture(c))
	iCulturePercent = iTotalCulture != 0 and 100 * plot.getCulture(iPlayer) / iTotalCulture or 0
	
	# ahistorical tiles
	if not bHistorical:
		iModifier += 2
		
	# not original owner
	if not city.isOriginalOwner(iPlayer) and since(city.getGameTurnAcquired()) < turns(25):
		iModifier += 1
	
	# not majority culture
	if iCulturePercent < 50: iModifier += 1
	if iCulturePercent < 20: iModifier += 1
	
	# Courthouse
	if city.hasBuilding(unique_building(iPlayer, iCourthouse)):
		# English Assembly UB
		if iCiv == iEngland:
			iModifier -= 2
		else:
			iModifier -= 1
	
	# Jail
	if city.hasBuilding(unique_building(iPlayer, iJail)):
		iModifier -= 1
	
	# cap
	if iModifier < -1: iModifier = -1
	
	return 100 + iModifier * 50

def calculateSeparatism(city):
	iPlayer = city.getOwner()
	civics = Civics.player(iPlayer)

	if city.isPlayerCore(iPlayer):
		return 0
	
	iModifier = getSeparatismModifier(iPlayer, city)
	iSeparatism = city.getPopulation()
	
	if city.isOccupation():
		iSeparatism -= city.getTotalPopulationLoss()
	
	iSeparatism *= iModifier / 100
	
	return iSeparatism

def calculateSlaveStability(city):
	iPlayer = city.getOwner()
	
	iSlaveryStability = 0
	for iSpecialistSlave in lSlaveSpecialists:
		iSlaveryStability -= city.getFreeSpecialistCount(iSpecialistSlave)
	
	iModifier = 100
	# Spanish UP
	if civ(iPlayer) == iSpain: iModifier -= 25
	# Stocks
	if city.hasBuilding(unique_building(iPlayer, iStocks)): iModifier -= 25
	# Estate
	if city.hasBuilding(unique_building(iPlayer, iEstate)): iModifier -= 25
	
	return int(iSlaveryStability * iModifier / 100)


def calculateStability(iPlayer):
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iCiv = civ(iPlayer)

	iExpansionStability = 0
	iEconomyStability = 0
	iDomesticStability = 0
	iForeignStability = 0
	iMilitaryStability = 0
	
	lParameters = [0 for i in range(iNumStabilityParameters)]
	
	# Collect required data
	iStateReligion = pPlayer.getStateReligion()
	iCurrentEra = pPlayer.getCurrentEra()
	iTotalPopulation = pPlayer.getTotalPopulation()
	iPlayerScore = pPlayer.getScoreHistory(turn())
	
	civics = Civics.player(iPlayer)
	
	iTotalCoreCities = 0
	iOccupiedCoreCities = 0
	
	iRecentlyFounded = 0
	iRecentlyConquered = 0
	
	iStateReligionPopulation = 0
	iOnlyStateReligionPopulation = 0
	iDifferentReligionPopulation = 0
	iNoReligionPopulation = 0
	
	iAdministration = cities.owner(iPlayer).sum(calculateAdministration) + 10
	iSeparatism = cities.owner(iPlayer).sum(calculateSeparatism)
	
	for city in cities.owner(iPlayer):
		iPopulation = city.getPopulation()
		bHistorical = city.plot().getPlayerSettlerValue(iPlayer) > 0
		bConquest = city.plot().getPlayerWarValue(iPlayer) > 1
		
		# Recent conquests
		if since(city.getGameTurnAcquired()) <= turns(20):
			if city.getPreviousCiv() < 0:
				if bHistorical:
					iRecentlyFounded += 1
			else:
				if bHistorical or bConquest:
					iRecentlyConquered += 1
			
		# Religions
		if city.getReligionCount() == 0:
			iNoReligionPopulation += iPopulation
		else:
			bNonStateReligion = False
			for iReligion in range(iNumReligions):
				if iReligion != iStateReligion and city.isHasReligion(iReligion):
					if not isTolerated(iPlayer, iReligion) and not gc.getReligionInfo(iReligion).isLocal():
						bNonStateReligion = True
						break

			if iStateReligion >= 0 and city.isHasReligion(iStateReligion):
				iStateReligionPopulation += iPopulation
				if not bNonStateReligion: iOnlyStateReligionPopulation += iPopulation
					
			if bNonStateReligion: 
				if iStateReligion >= 0 and city.isHasReligion(iStateReligion): iDifferentReligionPopulation += iPopulation / 2
				else: iDifferentReligionPopulation += iPopulation
				
	iAdministrationImprovements = plots.core(iPlayer).owner(iPlayer).where(lambda plot: plot.getWorkingCity() and plot.getImprovementType() in [iVillage, iTown]).count()
	iAdministration += getAdministrationModifier(iPlayer) * iAdministrationImprovements / 100
	
	# MacAurther: Europeans RP: Increased Administration (i.e. their core cities are off of the map)
	if iCiv == iEngland:
		iAdministration += 100
	elif iCiv == iFrance:
		iAdministration += 110
	elif iCiv == iNetherlands:
		iAdministration += 25
	elif iCiv == iNorse:
		iAdministration += 5
	elif iCiv == iPortugal:
		iAdministration += 70
	elif iCiv == iRussia:
		iAdministration += 75
	elif iCiv == iSpain:
		iAdministration += 90
	
	iCurrentPower = pPlayer.getPower()
	iPreviousPower = pPlayer.getPowerHistory(since(turns(10)))
	
	# EXPANSION
	iExpansionStability = 0
	
	iCorePeripheryStability = 0
	iRecentExpansionStability = 0
	iRazeCityStability = 0
	
	# Core vs. Periphery Populations
	iSeparatismExcess = 100 * iSeparatism / iAdministration - 100
	
	if iSeparatismExcess > 200: iSeparatismExcess = 200
		
	if iSeparatismExcess > 0:
		iCorePeripheryStability -= int(25 * sigmoid(1.0 * iSeparatismExcess / 100))
		
	lParameters[iParameterCorePeriphery] = iCorePeripheryStability
	lParameters[iParameterAdministration] = iAdministration
	lParameters[iParameterSeparatism] = iSeparatism
		
	iExpansionStability += iCorePeripheryStability
	
	# recent expansion stability
	iConquestModifier = 1
	if iConquest1 in civics or iConquest2 in civics: iConquestModifier += 1
	
	iRecentExpansionStability += iRecentlyFounded
	iRecentExpansionStability += iConquestModifier * iRecentlyConquered
		
	lParameters[iParameterRecentExpansion] = iRecentExpansionStability
	
	iExpansionStability += iRecentExpansionStability
	
	# apply raze city penalty
	if pPlayer.isHuman():
		iRazeCityStability = data.iHumanRazePenalty
	
	lParameters[iParameterRazedCities] = iRazeCityStability
		
	iExpansionStability += iRazeCityStability
	
	# stability if not expanded beyond core with isolationism
	iIsolationismStability = 0
	
	if iIsolationism1 in civics and iSeparatism <= 10:
		iIsolationismStability = 10
		
	lParameters[iParameterIsolationism] = iIsolationismStability
	
	iExpansionStability += iIsolationismStability
	
	# MacAurther: European RP: Extra stability from Motherland
	iMotherlandStability = 0
	if iCiv == iEngland:
		iMotherlandStability = 10
	elif iCiv == iFrance:
		iMotherlandStability = 10
	elif iCiv == iNetherlands:
		iMotherlandStability = 10
	elif iCiv == iNorse:
		iMotherlandStability = 5
	elif iCiv == iPortugal:
		iMotherlandStability = 5
	elif iCiv == iRussia:
		iMotherlandStability = 10
	elif iCiv == iSpain:
		iMotherlandStability = 15
	
	# MacAurther: Make Mississippi AI collapse because they like to stick around too long
	if not pPlayer.isHuman() and iCiv == iMississippi and turn() > turn(dFall[iMississippi]):
		iMotherlandStability = -25
	
	lParameters[iParameterMotherland] = iMotherlandStability
	
	iExpansionStability += iMotherlandStability
	
	# ECONOMY
	iEconomyStability = 0
	
	# Economic Growth
	iEconomicGrowthModifier = 3
	if iFreeEnterprise3 in civics: iEconomicGrowthModifier = 4
	
	iEconomicGrowthStability = iEconomicGrowthModifier * calculateTrendScore(data.players[iPlayer].lEconomyTrend)
	if iEconomicGrowthStability < 0 and iPublicWelfare3 in civics: iEconomicGrowthStability /= 2
	
	lParameters[iParameterEconomicGrowth] = iEconomicGrowthStability
	iEconomyStability += iEconomicGrowthStability
	
	iTradeStability = 0
	
	lParameters[iParameterTrade] = iTradeStability
	iEconomyStability += iTradeStability
					
	# DOMESTIC
	iDomesticStability = 0
	
	# Happiness
	iHappinessStability = calculateTrendScore(data.players[iPlayer].lHappinessTrend)
	
	if iHappinessStability > 5: iHappinessStability = 5
	if iHappinessStability < -5: iHappinessStability = -5
	
	if not player(iPlayer).isHuman() and iHappinessStability < 0:
		iHappinessStability *= 2
		iHappinessStability /= 3
	
	lParameters[iParameterHappiness] = iHappinessStability
	
	# Slaves
	iSlaveryStability = cities.owner(iPlayer).sum(calculateSlaveStability)
	lParameters[iParameterSlaves] = iSlaveryStability
	
	iDomesticStability += iHappinessStability + iSlaveryStability
	
	# Civics (combinations)
	iCivicCombinationStability = getCivicStability(iPlayer)
		
	if not player(iPlayer).isHuman() and iCivicCombinationStability < 0: iCivicCombinationStability /= 2
	
	lParameters[iParameterCivicCombinations] = iCivicCombinationStability
	
	iCivicEraTechStability = 0
	
	# Civics (eras and techs and religions)
	# note: make sure to reflect this in CvPlayerAI::isUnstableCivic
	if iIsolationism1 in civics:
		if iCurrentEra >= iIndustrialEra: iCivicEraTechStability -= (iCurrentEra - iRevolutionaryEra) * 3
	
	if iSlavery1 in civics or iSlavery2 in civics or iSlavery3 in civics:
		if iCurrentEra >= iIndustrialEra: iCivicEraTechStability -= 5
	
	if iCasteSystem1 in civics:
		if iCurrentEra >= iIndustrialEra: iCivicEraTechStability -= 5
	
	if iAdmiralty2 in civics:
		if iCurrentEra >= iIndustrialEra: iCivicEraTechStability -= 3
	
	if iIndenturedServitude2 in civics:
		if iCurrentEra >= iIndustrialEra: iCivicEraTechStability -= 2
	
	if iMercantilism2 in civics:
		if iCurrentEra >= iIndustrialEra: iCivicEraTechStability -= 3
	
	if iAnimism1 in civics:
		if iCurrentEra >= iRevolutionaryEra: iCivicEraTechStability -= 4
	
	if iChiefdom1 in civics:
		if iCurrentEra >= iRevolutionaryEra: iCivicEraTechStability -= 5
	
	if iTraditionalism1 in civics:
		if iCurrentEra >= iRevolutionaryEra: iCivicEraTechStability -= 5
	
	if tPlayer.isHasTech(iCivilRights):
		if iSlavery1 in civics or iSlavery2 in civics or iSlavery3 in civics or iCasteSystem1 in civics: iCivicEraTechStability -= 5
	
	if tPlayer.isHasTech(iNationalism):
		if iConquest1 in civics or iConquest2 in civics or iTributaries1 in civics: iCivicEraTechStability -= 5
	
	if tPlayer.isHasTech(iEvangelism):
		if iAnimism1 in civics or iCouncil1 in civics: iCivicEraTechStability -= 5
		
	if not player(iPlayer).isHuman() and iCivicEraTechStability < 0: iCivicEraTechStability /= 2
	
	lParameters[iParameterCivicsEraTech] = iCivicEraTechStability
	
	iDomesticStability += iCivicCombinationStability + iCivicEraTechStability
	
	# Religion
	iReligionStability = 0
	
	if iTotalPopulation > 0:
		iHeathenRatio = 100 * iDifferentReligionPopulation / iTotalPopulation
		iHeathenThreshold = 30
		iBelieverThreshold = 75
		
		if iHeathenRatio > iHeathenThreshold:
			iReligionStability -= (iHeathenRatio - iHeathenThreshold) / 10
			
		if iStateReligion >= 0:
			iStateReligionRatio = 100 * iStateReligionPopulation / iTotalPopulation
			iNoReligionRatio = 100 * iNoReligionPopulation / iTotalPopulation
			
			iBelieverRatio = iStateReligionRatio - iBelieverThreshold
			if iBelieverRatio < 0: iBelieverRatio = min(0, iBelieverRatio + iNoReligionRatio)
			iBelieverStability = iBelieverRatio / 5
			
			# cap at -10 for threshold = 75
			iCap = 2 * (iBelieverThreshold - 100) / 5
			if iBelieverStability < iCap: iBelieverStability = iCap
			
			iReligionStability += iBelieverStability
			
	
	lParameters[iParameterReligion] = iReligionStability
		
	iDomesticStability += iReligionStability
	
	# FOREIGN
	iForeignStability = 0
	iVassalStability = 0
	iDefensivePactStability = 0
	iRelationStability = 0
	iNationhoodStability = 0
	
	iNumContacts = 0
	iFriendlyRelations = 0
	iFuriousRelations = 0
	
	lContacts = []
	
	for iLoopPlayer in players.major():
		pLoopPlayer = player(iLoopPlayer)
		tLoopPlayer = team(iLoopPlayer)
		iLoopScore = pLoopPlayer.getScoreHistory(turn())
		
		if iLoopPlayer == iPlayer: continue
		if not pLoopPlayer.isAlive(): continue
				
		# master stability
		if tPlayer.isVassal(iLoopPlayer):
			if stability(iPlayer) > stability(iLoopPlayer):
				iVassalStability += 4 * (stability(iPlayer) - stability(iLoopPlayer))
				
		# vassal stability
		if tLoopPlayer.isVassal(iPlayer):
			if stability(iLoopPlayer) == iStabilityCollapsing: iVassalStability -= 3
			elif stability(iLoopPlayer) == iStabilityUnstable: iVassalStability -= 1
			elif stability(iLoopPlayer) == iStabilitySolid: iVassalStability += 2
			
			if iTributaries1 in civics: iVassalStability += 2
			
		# relations
		if tPlayer.canContact(iLoopPlayer):
			lContacts.append(iLoopPlayer)
			
		# defensive pacts
		if tPlayer.isDefensivePact(iLoopPlayer):
			if iLoopScore > iPlayerScore: iDefensivePactStability += 3
		
		# worst enemies
		if pLoopPlayer.getWorstEnemy() == iPlayer:
			if iLoopScore > iPlayerScore: iRelationStability -= 3
			
		# wars
		if tPlayer.isAtWar(iLoopPlayer):
			if game.isNeighbors(iPlayer, iLoopPlayer):
				if iNationhood3 in civics: iNationhoodStability += 2
		
	# attitude stability
	lStrongerAttitudes, lEqualAttitudes, lWeakerAttitudes = calculateRankedAttitudes(iPlayer, lContacts)
	
	iAttitudeThresholdModifier = pPlayer.getCurrentEra() / 2
	
	iRelationStronger = 0
	iPositiveStronger = count(lStrongerAttitudes, lambda x: x >= 4 + iAttitudeThresholdModifier * 2)
	if iPositiveStronger > len(lStrongerAttitudes) / 2:
		iRelationStronger = 5 * iPositiveStronger / max(1, len(lStrongerAttitudes))
		iRelationStronger = min(iRelationStronger, len(lStrongerAttitudes))
	
	iRelationWeaker = 0
	iNegativeWeaker = max(0, count(lWeakerAttitudes, lambda x: x < -1) - count(lWeakerAttitudes, lambda x: x >= 3 + iAttitudeThresholdModifier))
	
	if iNegativeWeaker > 0:
		iRelationWeaker = -8 * min(iNegativeWeaker, len(lWeakerAttitudes) / 2) / max(1, len(lWeakerAttitudes) / 2)
		iRelationWeaker = max(iRelationWeaker, -len(lWeakerAttitudes))
		
	iRelationEqual = sum(sign(iAttitude) * min(25, abs(iAttitude) / 5) for iAttitude in lEqualAttitudes if abs(iAttitude) > 2)

	iRelationStability = iRelationStronger + iRelationEqual + iRelationWeaker
		
	if iIsolationism1 in civics:
		if iRelationStability < 0: iRelationStability = 0
		if iRelationStability > 0: iRelationStability /= 2
	
	if not player(iPlayer).isHuman():
		if iRelationStability < 0:
			iRelationStability /= 2
	
	lParameters[iParameterVassals] = iVassalStability
	lParameters[iParameterDefensivePacts] = iDefensivePactStability
	lParameters[iParameterRelations] = iRelationStability
	lParameters[iParameterNationhood] = iNationhoodStability
	lParameters[iParameterMultilateralism] = 0
			
	iForeignStability += iVassalStability + iDefensivePactStability + iRelationStability + iNationhoodStability + 0
	
	# MILITARY
	
	iMilitaryStability = 0
	
	iWarSuccessStability = 0
	iMilitaryStrengthStability = 0
	iBarbarianLossesStability = 0
	
	iWarSuccessStability = 0 # war success (conquering cities and defeating units)
	iWarWearinessStability = 0 # war weariness in comparison to war length
	iBarbarianLossesStability = 0 # like previously
	
	# iterate ongoing wars
	for iEnemy in players.major().existing():
		pEnemy = player(iEnemy)
		if tPlayer.isAtWar(iEnemy):
			iTempWarSuccessStability = calculateTrendScore(data.players[iPlayer].lWarTrend[iEnemy])
			
			iOurSuccess = tPlayer.AI_getWarSuccess(iEnemy)
			iTheirSuccess = team(iEnemy).AI_getWarSuccess(iPlayer)
			
			if iTempWarSuccessStability > 0 and iTheirSuccess > iOurSuccess: iTempWarSuccessStability /= 2
			elif iTempWarSuccessStability < 0 and iOurSuccess > iTheirSuccess: iTempWarSuccessStability /= 2
			
			if iTempWarSuccessStability > 0: iTempWarSuccessStability /= 2
			
			iWarSuccessStability += iTempWarSuccessStability
			
			iOurWarWeariness = tPlayer.getWarWeariness(iEnemy)
			iTheirWarWeariness = team(iEnemy).getWarWeariness(iPlayer)
			
			iWarTurns = turn() - data.players[iPlayer].lWarStartTurn[iEnemy]
			iDurationModifier = 0
			
			if iWarTurns > turns(20):
				iDurationModifier = min(9, (iWarTurns - turns(20)) / turns(10))
				
			iTempWarWearinessStability = (iTheirWarWeariness - iOurWarWeariness) / (4000 * (iDurationModifier + 1))
			if iTempWarWearinessStability > 0: iTempWarWearinessStability = 0
			
			iWarWearinessStability += iTempWarWearinessStability
			
			debug(pPlayer.getCivilizationAdjective(0) + ' war against ' + pEnemy.getCivilizationShortDescription(0) + '\nWar Success Stability: ' + str(iTempWarSuccessStability) + '\nWar Weariness: ' + str(iTempWarWearinessStability))
	
	lParameters[iParameterWarSuccess] = iWarSuccessStability
	lParameters[iParameterWarWeariness] = iWarWearinessStability
	
	iMilitaryStability = iWarSuccessStability + iWarWearinessStability
	
	# apply barbarian losses
	iBarbarianLossesStability = -min(10, data.players[iPlayer].iBarbarianLosses)
	
	lParameters[iParameterBarbarianLosses] = iBarbarianLossesStability
	
	iMilitaryStability += iBarbarianLossesStability
	
	iStability = iExpansionStability + iEconomyStability + iDomesticStability + iForeignStability + iMilitaryStability
	
	return iStability, [iExpansionStability, iEconomyStability, iDomesticStability, iForeignStability, iMilitaryStability], lParameters
	
def getCivicStability(iPlayer, civics=None):
	if civics is None:
		civics = Civics.player(iPlayer)
    
    # Confederacy doesn't care about synergies or antisynergies
	if iConfederacy3 in civics:
		return 0
	
	iCurrentEra = player(iPlayer).getCurrentEra()
	iStability = 0
	
	# Native
	#	Executive
	if iChiefdom1 in civics:
		if iCustomaryLaw1 in civics: iStability += 2
		if iBureaucracy1 in civics: iStability -= 2
		if iSubsistance1 in civics: iStability += 2
		if iMita1 in civics: iStability -= 2
		if iCommune1 in civics: iStability += 2
		if iPlunder1 in civics: iStability -= 2
		if iHarmony1 in civics: iStability += 2
		if iCosmopolis1 in civics: iStability -= 2
		if iNomads1 in civics: iStability += 2
		if iTributaries1 in civics: iStability -= 2
	
	if iDespotism1 in civics:
		if iCustomaryLaw1 in civics: iStability -= 2
		if iConfederacy1 in civics: iStability -= 2
		if iMita1 in civics: iStability += 2
		if iSlavery1 in civics: iStability += 2
		if iCommune1 in civics: iStability -= 2
		if iRedistribution1 in civics: iStability += 2
		if iAcculturation1 in civics: iStability -= 2
		if iSovereignty1 in civics: iStability += 2
		if iConquest1 in civics: iStability += 2
		if iCooperation1 in civics: iStability -= 2
	
	if iMonarchy1 in civics:
		if iCityStates1 in civics: iStability -= 2
		if iFirstNation1 in civics: iStability += 2
		if iCraftsmen1 in civics: iStability += 2
		if iCasteSystem1 in civics: iStability += 2
		if iRedistribution1 in civics: iStability += 2
		if iDependency1 in civics: iStability += 2
		if iIsolationism1 in civics: iStability += 2
		if iAcculturation1 in civics: iStability += 2
		if iDiffusion1 in civics: iStability += 2
		if iConquest1 in civics: iStability -= 2
	
	if iCouncil1 in civics:
		if iConfederacy1 in civics: iStability += 2
		if iVassalage1 in civics: iStability -= 2
		if iCaptives1 in civics: iStability -= 2
		if iCraftsmen1 in civics: iStability += 2
		if iMerchants1 in civics: iStability += 2
		if iTourism1 in civics: iStability += 2
		if iHarmony1 in civics: iStability += 2
		if iOrganizedReligion1 in civics: iStability -= 2
		if iDiffusion1 in civics: iStability -= 2
		if iAncestralLands1 in civics: iStability += 2
	
	if iAristocracy1 in civics:
		if iCityStates1 in civics: iStability += 2
		if iBureaucracy1 in civics: iStability += 2
		if iSubsistance1 in civics: iStability -= 2
		if iCasteSystem1 in civics: iStability += 2
		if iMerchants1 in civics: iStability += 2
		if iDependency1 in civics: iStability -= 2
		if iCosmopolis1 in civics: iStability += 2
		if iIsolationism1 in civics: iStability -= 2
		if iNomads1 in civics: iStability -= 2
		if iCooperation1 in civics: iStability += 2
	
	if iGodKing1 in civics:
		if iVassalage1 in civics: iStability += 2
		if iFirstNation1 in civics: iStability -= 2
		if iCaptives1 in civics: iStability += 2
		if iSlavery1 in civics: iStability += 2
		if iPlunder1 in civics: iStability += 2
		if iTourism1 in civics: iStability -= 2
		if iOrganizedReligion1 in civics: iStability += 2
		if iSovereignty1 in civics: iStability += 2
		if iTributaries1 in civics: iStability += 2
		if iAncestralLands1 in civics: iStability -= 2
	
	#	Administration
	if iCustomaryLaw1 in civics:
		if iCraftsmen1 in civics: iStability += 2
		if iSlavery1 in civics: iStability -= 2
		if iCommune1 in civics: iStability += 2
		if iPlunder1 in civics: iStability -= 2
		if iAcculturation1 in civics: iStability += 2
		if iSovereignty1 in civics: iStability -= 2
		if iNomads1 in civics: iStability += 2
		if iTributaries1 in civics: iStability -= 2
	
	if iCityStates1 in civics:
		if iSubsistance1 in civics: iStability -= 2
		if iCaptives1 in civics: iStability += 2
		if iRedistribution1 in civics: iStability += 2
		if iTourism1 in civics: iStability -= 2
		if iHarmony1 in civics: iStability -= 2
		if iCosmopolis1 in civics: iStability += 2
		if iNomads1 in civics: iStability -= 2
		if iDiffusion1 in civics: iStability += 2
	
	if iConfederacy1 in civics:
		if iSubsistance1 in civics: iStability += 2
		if iCasteSystem1 in civics: iStability -= 2
		if iMerchants1 in civics: iStability -= 2
		if iDependency1 in civics: iStability += 2
		if iHarmony1 in civics: iStability += 2
		if iIsolationism1 in civics: iStability -= 2
		if iConquest1 in civics: iStability -= 2
		if iCooperation1 in civics: iStability += 2
	
	if iBureaucracy1 in civics:
		if iCaptives1 in civics: iStability -= 2
		if iMita1 in civics: iStability += 2
		if iMerchants1 in civics: iStability += 2
		if iDependency1 in civics: iStability -= 2
		if iCosmopolis1 in civics: iStability -= 2
		if iIsolationism1 in civics: iStability += 2
		if iTributaries1 in civics: iStability += 2
		if iAncestralLands1 in civics: iStability -= 2
	
	if iVassalage1 in civics:
		if iCraftsmen1 in civics: iStability -= 2
		if iSlavery1 in civics: iStability += 2
		if iCommune1 in civics: iStability -= 2
		if iPlunder1 in civics: iStability += 2
		if iOrganizedReligion1 in civics: iStability += 2
		if iAcculturation1 in civics: iStability -= 2
		if iConquest1 in civics: iStability += 2
		if iCooperation1 in civics: iStability -= 2
	
	if iFirstNation1 in civics:
		if iMita1 in civics: iStability -= 2
		if iCasteSystem1 in civics: iStability += 2
		if iRedistribution1 in civics: iStability -= 2
		if iTourism1 in civics: iStability += 2
		if iOrganizedReligion1 in civics: iStability -= 2
		if iSovereignty1 in civics: iStability += 2
		if iDiffusion1 in civics: iStability -= 2
		if iAncestralLands1 in civics: iStability += 2
	
	#	Labor
	if iSubsistance1 in civics:
		if iCommune1 in civics: iStability += 2
		if iRedistribution1 in civics: iStability -= 2
		if iHarmony1 in civics: iStability += 2
		if iCosmopolis1 in civics: iStability -= 2
		if iNomads1 in civics: iStability += 2
		if iTributaries1 in civics: iStability -= 2
	
	if iCaptives1 in civics:
		if iMerchants1 in civics: iStability -= 2
		if iPlunder1 in civics: iStability += 2
		if iOrganizedReligion1 in civics: iStability += 2
		if iIsolationism1 in civics: iStability += 2
		if iDiffusion1 in civics: iStability += 2
		if iAncestralLands1 in civics: iStability -= 2
	
	if iMita1 in civics:
		if iRedistribution1 in civics: iStability += 2
		if iTourism1 in civics: iStability -= 2
		if iHarmony1 in civics: iStability -= 2
		if iAcculturation1 in civics: iStability -= 2
		if iNomads1 in civics: iStability -= 2
		if iConquest1 in civics: iStability += 2
	
	if iCraftsmen1 in civics:
		if iMerchants1 in civics: iStability += 2
		if iPlunder1 in civics: iStability -= 2
		if iCosmopolis1 in civics: iStability += 2
		if iSovereignty1 in civics: iStability += 2
		if iConquest1 in civics: iStability -= 2
		if iCooperation1 in civics: iStability += 2
	
	if iCasteSystem1 in civics:
		if iCommune1 in civics: iStability -= 2
		if iDependency1 in civics: iStability -= 2
		if iOrganizedReligion1 in civics: iStability += 2
		if iAcculturation1 in civics: iStability -= 2
		if iDiffusion1 in civics: iStability -= 2
		if iTributaries1 in civics: iStability += 2
	
	if iSlavery1 in civics:
		if iDependency1 in civics: iStability -= 2
		if iTourism1 in civics: iStability -= 2
		if iIsolationism1 in civics: iStability -= 2
		if iSovereignty1 in civics: iStability -= 2
		if iCooperation1 in civics: iStability -= 2
		if iAncestralLands1 in civics: iStability += 2
	
	#	Economy
	if iCommune1 in civics:
		if iHarmony1 in civics: iStability += 2
		if iAcculturation1 in civics: iStability -= 2
		if iDiffusion1 in civics: iStability += 2
		if iTributaries1 in civics: iStability -= 2
		
	if iRedistribution1 in civics:
		if iOrganizedReligion1 in civics: iStability += 2
		if iSovereignty1 in civics: iStability -= 2
		if iTributaries1 in civics: iStability += 2
		if iAncestralLands1 in civics: iStability -= 2
		
	if iMerchants1 in civics:
		if iCosmopolis1 in civics: iStability += 2
		if iIsolationism1 in civics: iStability -= 2
		if iNomads1 in civics: iStability += 2
		if iCooperation1 in civics: iStability -= 2
		
	if iPlunder1 in civics:
		if iHarmony1 in civics: iStability -= 2
		if iCosmopolis1 in civics: iStability -= 2
		if iDiffusion1 in civics: iStability -= 2
		if iConquest1 in civics: iStability += 2
		
	if iDependency1 in civics:
		if iIsolationism1 in civics: iStability -= 2
		if iAcculturation1 in civics: iStability += 2
		if iConquest1 in civics: iStability -= 2
		if iCooperation1 in civics: iStability += 2
		
	if iTourism1 in civics:
		if iOrganizedReligion1 in civics: iStability -= 2
		if iSovereignty1 in civics: iStability += 2
		if iNomads1 in civics: iStability -= 2
		if iAncestralLands1 in civics: iStability += 2
	
	#	Society
	if iHarmony1 in civics:
		if iNomads1 in civics: iStability += 2
		if iTributaries1 in civics: iStability -= 2
		
	if iOrganizedReligion1 in civics:
		if iCooperation1 in civics: iStability -= 2
		if iTributaries1 in civics: iStability += 2
		
	if iCosmopolis1 in civics:
		if iNomads1 in civics: iStability -= 2
		if iDiffusion1 in civics: iStability += 2
		
	if iIsolationism1 in civics:
		if iConquest1 in civics: iStability -= 2
		if iAncestralLands1 in civics: iStability += 2
		
	if iAcculturation1 in civics:
		if iCooperation1 in civics: iStability += 2
		if iAncestralLands1 in civics: iStability -= 2
		
	if iSovereignty1 in civics:
		if iDiffusion1 in civics: iStability -= 2
		if iConquest1 in civics: iStability += 2
	
	
	# Colony
	#	Executive
	if iViceroyality2 in civics:
		if iCharterColony2 in civics: iStability -= 2
		if iCommonLaw2 in civics: iStability -= 2
		if iEncomienda2 in civics: iStability += 2
		if iSlavery2 in civics: iStability += 2
		if iPlunder2 in civics: iStability += 2
		if iConsumerism2 in civics: iStability -= 2
		if iJesuits2 in civics: iStability += 2
		if iEmancipation2 in civics: iStability -= 2
		if iConquest2 in civics: iStability += 2
		if iCommonwealth2 in civics: iStability -= 2
	
	if iProprietaries2 in civics:
		if iAdmiralty2 in civics: iStability += 2
		if iProvinces2 in civics: iStability -= 2
		if iPenalColony2 in civics: iStability += 2
		if iImmigrantLabor2 in civics: iStability -= 2
		if iPlunder2 in civics: iStability += 2
		if iConsumerism2 in civics: iStability -= 2
		if iHaven2 in civics: iStability -= 2
		if iProfiteering2 in civics: iStability += 2
		if iOutposts2 in civics: iStability += 2
		if iHomesteads2 in civics: iStability -= 2
	
	if iTrustees2 in civics:
		if iAdmiralty2 in civics: iStability -= 2
		if iTradingCompany2 in civics: iStability += 2
		if iEncomienda2 in civics: iStability -= 2
		if iSlavery2 in civics: iStability -= 2
		if iFactory2 in civics: iStability += 2
		if iPublicWelfare2 in civics: iStability -= 2
		if iZealotry2 in civics: iStability -= 2
		if iHaven2 in civics: iStability += 2
		if iProvidence2 in civics: iStability += 2
		if iOutposts2 in civics: iStability -= 2
	
	if iGovernors2 in civics:
		if iTradingCompany2 in civics: iStability -= 2
		if iRoyalColony2 in civics: iStability += 2
		if iIndenturedServitude2 in civics: iStability += 2
		if iIndustrialism2 in civics: iStability -= 2
		if iMercantilism2 in civics: iStability += 2
		if iCustomsUnion2 in civics: iStability -= 2
		if iProfiteering2 in civics: iStability -= 2
		if iOpportunity2 in civics: iStability -= 2
		if iProvidence2 in civics: iStability -= 2
		if iHomesteads2 in civics: iStability += 2
	
	if iColonialAssembly2 in civics:
		if iCharterColony2 in civics: iStability += 2
		if iCommonLaw2 in civics: iStability += 2
		if iIndenturedServitude2 in civics: iStability -= 2
		if iIndustrialism2 in civics: iStability += 2
		if iFactory2 in civics: iStability -= 2
		if iCustomsUnion2 in civics: iStability += 2
		if iZealotry2 in civics: iStability += 2
		if iOpportunity2 in civics: iStability += 2
		if iConquest2 in civics: iStability -= 2
		if iIntervention2 in civics: iStability += 2
	
	if iHomeRule2 in civics:
		if iRoyalColony2 in civics: iStability -= 2
		if iProvinces2 in civics: iStability += 2
		if iPenalColony2 in civics: iStability -= 2
		if iImmigrantLabor2 in civics: iStability += 2
		if iMercantilism2 in civics: iStability -= 2
		if iPublicWelfare2 in civics: iStability += 2
		if iJesuits2 in civics: iStability -= 2
		if iEmancipation2 in civics: iStability += 2
		if iIntervention2 in civics: iStability -= 2
		if iCommonwealth2 in civics: iStability += 2
	
	#	Administration
	if iAdmiralty2 in civics:
		if iEncomienda2 in civics: iStability += 2
		if iIndustrialism2 in civics: iStability -= 2
		if iPlunder2 in civics: iStability += 2
		if iCustomsUnion2 in civics: iStability -= 2
		if iJesuits2 in civics: iStability += 2
		if iEmancipation2 in civics: iStability -= 2
		if iConquest2 in civics: iStability += 2
		if iCommonwealth2 in civics: iStability -= 2
	
	if iCharterColony2 in civics:
		if iIndenturedServitude2 in civics: iStability += 2
		if iImmigrantLabor2 in civics: iStability += 2
		if iMercantilism2 in civics: iStability += 2
		if iConsumerism2 in civics: iStability -= 2
		if iHaven2 in civics: iStability += 2
		if iProfiteering2 in civics: iStability -= 2
		if iProvidence2 in civics: iStability += 2
		if iIntervention2 in civics: iStability -= 2
	
	if iTradingCompany2 in civics:
		if iSlavery2 in civics: iStability += 2
		if iPenalColony2 in civics: iStability -= 2
		if iFactory2 in civics: iStability += 2
		if iMercantilism2 in civics: iStability -= 2
		if iProfiteering2 in civics: iStability += 2
		if iOpportunity2 in civics: iStability -= 2
		if iOutposts2 in civics: iStability += 2
		if iHomesteads2 in civics: iStability -= 2
	
	if iRoyalColony2 in civics:
		if iIndenturedServitude2 in civics: iStability += 2
		if iPenalColony2 in civics: iStability += 2
		if iCustomsUnion2 in civics: iStability += 2
		if iPublicWelfare2 in civics: iStability -= 2
		if iZealotry2 in civics: iStability += 2
		if iHaven2 in civics: iStability -= 2
		if iOutposts2 in civics: iStability -= 2
		if iIntervention2 in civics: iStability += 2
	
	if iCommonLaw2 in civics:
		if iEncomienda2 in civics: iStability -= 2
		if iImmigrantLabor2 in civics: iStability += 2
		if iPlunder2 in civics: iStability -= 2
		if iConsumerism2 in civics: iStability += 2
		if iJesuits2 in civics: iStability -= 2
		if iOpportunity2 in civics: iStability += 2
		if iConquest2 in civics: iStability -= 2
		if iHomesteads2 in civics: iStability += 2
	
	if iProvinces2 in civics:
		if iSlavery2 in civics: iStability -= 2
		if iIndustrialism2 in civics: iStability += 2
		if iFactory2 in civics: iStability -= 2
		if iPublicWelfare2 in civics: iStability += 2
		if iZealotry2 in civics: iStability -= 2
		if iEmancipation2 in civics: iStability += 2
		if iProvidence2 in civics: iStability -= 2
		if iCommonwealth2 in civics: iStability += 2
	
	#	Labor
	if iEncomienda2 in civics:
		if iPlunder2 in civics: iStability += 2
		if iMercantilism2 in civics: iStability -= 2
		if iJesuits2 in civics: iStability += 2
		if iConquest2 in civics: iStability += 2
		if iOutposts2 in civics: iStability -= 2
	
	if iIndenturedServitude2 in civics:
		if iFactory2 in civics: iStability += 2
		if iConsumerism2 in civics: iStability -= 2
		if iZealotry2 in civics: iStability -= 2
		if iHaven2 in civics: iStability += 2
		if iConquest2 in civics: iStability -= 2
		if iProvidence2 in civics: iStability += 2
	
	if iSlavery2 in civics:
		if iCustomsUnion2 in civics: iStability += 2
		if iPublicWelfare2 in civics: iStability -= 2
		if iProfiteering2 in civics: iStability += 2
		if iEmancipation2 in civics: iStability -= 2
		if iHomesteads2 in civics: iStability += 2
		if iCommonwealth2 in civics: iStability -= 2
	
	if iPenalColony2 in civics:
		if iMercantilism2 in civics: iStability += 2
		if iCustomsUnion2 in civics: iStability -= 2
		if iHaven2 in civics: iStability += 2
		if iOpportunity2 in civics: iStability -= 2
		if iHomesteads2 in civics: iStability -= 2
		if iIntervention2 in civics: iStability += 2
	
	if iIndustrialism2 in civics:
		if iFactory2 in civics: iStability -= 2
		if iConsumerism2 in civics: iStability += 2
		if iJesuits2 in civics: iStability -= 2
		if iOpportunity2 in civics: iStability += 2
		if iOutposts2 in civics: iStability -= 2
		if iCommonwealth2 in civics: iStability += 2
	
	if iImmigrantLabor2 in civics:
		if iPlunder2 in civics: iStability -= 2
		if iPublicWelfare2 in civics: iStability += 2
		if iZealotry2 in civics: iStability -= 2
		if iEmancipation2 in civics: iStability += 2
		if iProvidence2 in civics: iStability -= 2
		if iIntervention2 in civics: iStability += 2
	
	#	Economy
	if iPlunder2 in civics:
		if iZealotry2 in civics: iStability += 2
		if iOpportunity2 in civics: iStability -= 2
		if iConquest2 in civics: iStability += 2
		if iHomesteads2 in civics: iStability -= 2
	
	if iFactory2 in civics:
		if iJesuits2 in civics: iStability += 2
		if iHaven2 in civics: iStability -= 2
		if iOutposts2 in civics: iStability += 2
		if iIntervention2 in civics: iStability -= 2
	
	if iMercantilism2 in civics:
		if iProfiteering2 in civics: iStability += 2
		if iEmancipation2 in civics: iStability -= 2
		if iIntervention2 in civics: iStability += 2
		if iCommonwealth2 in civics: iStability -= 2
	
	if iCustomsUnion2 in civics:
		if iHaven2 in civics: iStability += 2
		if iProfiteering2 in civics: iStability -= 2
		if iOutposts2 in civics: iStability -= 2
		if iHomesteads2 in civics: iStability += 2
	
	if iConsumerism2 in civics:
		if iJesuits2 in civics: iStability -= 2
		if iOpportunity2 in civics: iStability += 2
		if iProvidence2 in civics: iStability -= 2
		if iCommonwealth2 in civics: iStability += 2
	
	if iPublicWelfare2 in civics:
		if iZealotry2 in civics: iStability -= 2
		if iEmancipation2 in civics: iStability += 2
		if iConquest2 in civics: iStability -= 2
		if iProvidence2 in civics: iStability += 2
	
	#	Society
	if iZealotry2 in civics:
		if iConquest2 in civics: iStability += 2
		if iOutposts2 in civics: iStability -= 2
	
	if iJesuits2 in civics:
		if iProvidence2 in civics: iStability += 2
		if iHomesteads2 in civics: iStability -= 2
	
	if iHaven2 in civics:
		if iHomesteads2 in civics: iStability += 2
		if iIntervention2 in civics: iStability -= 2
	
	if iProfiteering2 in civics:
		if iOutposts2 in civics: iStability += 2
		if iCommonwealth2 in civics: iStability -= 2
	
	if iOpportunity2 in civics:
		if iProvidence2 in civics: iStability -= 2
		if iCommonwealth2 in civics: iStability += 2
	
	if iEmancipation2 in civics:
		if iConquest2 in civics: iStability -= 2
		if iIntervention2 in civics: iStability += 2
	
	
	# Nation
	#	Executive
	if iJunta3 in civics:
		if iCommonLaw3 in civics: iStability -= 2
		if iSlavery3 in civics: iStability += 2
		if iIndustrialism3 in civics: iStability -= 2
		if iAgrarianism3 in civics: iStability += 2
		if iConsumerism3 in civics: iStability -= 2
		if iOpportunity3 in civics: iStability -= 2
		if iAssimilation3 in civics: iStability -= 2
	
	if iMonarchy3 in civics:
		if iCommonLaw3 in civics: iStability += 2
		if iMandate3 in civics: iStability -= 2
		if iApprenticeship3 in civics: iStability += 2
		if iExtraction3 in civics: iStability += 2
		if iProfiteering3 in civics: iStability += 2
		if iDecolonization3 in civics: iStability -= 2
	
	if iPlutocracy3 in civics:
		if iKleptocracy3 in civics: iStability += 2
		if iPoliceState3 in civics: iStability -= 2
		if iIndustrialism3 in civics: iStability += 2
		if iLaborUnions3 in civics: iStability -= 2
		if iProtectionism3 in civics: iStability += 2
		if iLibertarianism3 in civics: iStability += 2
		if iEmancipation3 in civics: iStability -= 2
		if iManifestDestiny3 in civics: iStability += 2
	
	if iDemocracy3 in civics:
		if iFederalism3 in civics: iStability += 2
		if iKleptocracy3 in civics: iStability -= 2
		if iSlavery3 in civics: iStability -= 2
		if iImmigrantLabor3 in civics: iStability += 2
		if iFreeEnterprise3 in civics: iStability += 2
		if iProtectionism3 in civics: iStability -= 2
		if iOpportunity3 in civics: iStability += 2
		if iNativism3 in civics: iStability -= 2
		if iDecolonization3 in civics: iStability += 2
		if iNationhood3 in civics: iStability -= 2
	
	if iDictatorship3 in civics:
		if iFederalism3 in civics: iStability -= 2
		if iPoliceState3 in civics: iStability += 2
		if iSubsistance3 in civics: iStability += 2
		if iImmigrantLabor3 in civics: iStability -= 2
		if iExtraction3 in civics: iStability += 2
		if iPublicWelfare3 in civics: iStability -= 2
		if iNativism3 in civics: iStability += 2
		if iEgalitarianism3 in civics: iStability -= 2
		if iNationhood3 in civics: iStability += 2
	
	if iStateParty3 in civics:
		if iMandate3 in civics: iStability += 2
		if iSubsistance3 in civics: iStability -= 2
		if iLaborUnions3 in civics: iStability += 2
		if iAgrarianism3 in civics: iStability -= 2
		if iPublicWelfare3 in civics: iStability += 2
		if iLibertarianism3 in civics: iStability -= 2
		if iHegemony3 in civics: iStability += 2
	
	#	Administration
	if iCommonLaw3 in civics:
		if iApprenticeship3 in civics: iStability += 2
		if iAgrarianism3 in civics: iStability += 2
		if iProtectionism3 in civics: iStability -= 2
		if iLibertarianism3 in civics: iStability += 2
		if iProfiteering3 in civics: iStability -= 2
		if iAssimilation3 in civics: iStability += 2
		if iManifestDestiny3 in civics: iStability -= 2
	
	if iFederalism3 in civics:
		if iSlavery3 in civics: iStability -= 2
		if iExtraction3 in civics: iStability -= 2
		if iProtectionism3 in civics: iStability += 2
		if iOpportunity3 in civics: iStability += 2
		if iNativism3 in civics: iStability -= 2
		if iEgalitarianism3 in civics: iStability += 2
		if iNationhood3 in civics: iStability -= 2
		if iHegemony3 in civics: iStability += 2
	
	if iMandate3 in civics:
		if iIndustrialism3 in civics: iStability += 2
		if iConsumerism3 in civics: iStability += 2
		if iEmancipation3 in civics: iStability += 2
		if iDecolonization3 in civics: iStability += 2
		if iHegemony3 in civics: iStability -= 2
	
	if iKleptocracy3 in civics:
		if iImmigrantLabor3 in civics: iStability += 2
		if iLaborUnions3 in civics: iStability -= 2
		if iExtraction3 in civics: iStability += 2
		if iProfiteering3 in civics: iStability += 2
		if iEgalitarianism3 in civics: iStability -= 2
		if iHomesteads3 in civics: iStability -= 2
		if iManifestDestiny3 in civics: iStability += 2
	
	if iPoliceState3 in civics:
		if iSlavery3 in civics: iStability += 2
		if iPublicWelfare3 in civics: iStability -= 2
		if iEmancipation3 in civics: iStability -= 2
		if iNativism3 in civics: iStability += 2
		if iAssimilation3 in civics: iStability -= 2
		if iNationhood3 in civics: iStability += 2
	
	#	Labor
	if iSubsistance3 in civics:
		if iAgrarianism3 in civics: iStability += 2
		if iExtraction3 in civics: iStability -= 2
		if iLibertarianism3 in civics: iStability += 2
		if iOpportunity3 in civics: iStability -= 2
		if iHomesteads3 in civics: iStability += 2
		if iHegemony3 in civics: iStability -= 2
	
	if iApprenticeship3 in civics:
		if iFreeEnterprise3 in civics: iStability += 2
		if iProtectionism3 in civics: iStability -= 2
		if iOpportunity3 in civics: iStability += 2
	
	if iSlavery3 in civics:
		if iExtraction3 in civics: iStability += 2
		if iPublicWelfare3 in civics: iStability -= 2
		if iProfiteering3 in civics: iStability += 2
		if iEmancipation3 in civics: iStability -= 2
		if iAssimilation3 in civics: iStability -= 2
		if iManifestDestiny3 in civics: iStability += 2
	
	if iIndustrialism3 in civics:
		if iAgrarianism3 in civics: iStability -= 2
		if iProtectionism3 in civics: iStability += 2
		if iEgalitarianism3 in civics: iStability -= 2
		if iHomesteads3 in civics: iStability -= 2
		if iNationhood3 in civics: iStability += 2
	
	if iImmigrantLabor3 in civics:
		if iProtectionism3 in civics: iStability -= 2
		if iConsumerism3 in civics: iStability += 2
		if iEmancipation3 in civics: iStability += 2
		if iNativism3 in civics: iStability -= 2
		if iNationhood3 in civics: iStability -= 2
		if iHegemony3 in civics: iStability += 2
	
	if iLaborUnions3 in civics:
		if iFreeEnterprise3 in civics: iStability -= 2
		if iPublicWelfare3 in civics: iStability += 2
		if iProfiteering3 in civics: iStability -= 2
		if iEgalitarianism3 in civics: iStability += 2
		if iManifestDestiny3 in civics: iStability -= 2
	
	#	Economy
	if iAgrarianism3 in civics:
		if iLibertarianism3 in civics: iStability += 2
		if iOpportunity3 in civics: iStability -= 2
		if iHomesteads3 in civics: iStability += 2
		if iHegemony3 in civics: iStability -= 2
	
	if iExtraction3 in civics:
		if iProfiteering3 in civics: iStability += 2
		if iEgalitarianism3 in civics: iStability -= 2
		if iAssimilation3 in civics: iStability -= 2
		if iManifestDestiny3 in civics: iStability += 2
	
	if iFreeEnterprise3 in civics:
		if iOpportunity3 in civics: iStability += 2
		if iEmancipation3 in civics: iStability -= 2
		if iAssimilation3 in civics: iStability += 2
		if iDecolonization3 in civics: iStability -= 2
	
	if iProtectionism3 in civics:
		if iLibertarianism3 in civics: iStability -= 2
		if iNativism3 in civics: iStability += 2
		if iDecolonization3 in civics: iStability += 2
	
	if iConsumerism3 in civics:
		if iEmancipation3 in civics: iStability += 2
		if iNativism3 in civics: iStability -= 2
		if iHomesteads3 in civics: iStability -= 2
		if iHegemony3 in civics: iStability += 2
	
	if iPublicWelfare3 in civics:
		if iProfiteering3 in civics: iStability -= 2
		if iEgalitarianism3 in civics: iStability += 2
		if iManifestDestiny3 in civics: iStability -= 2
		if iNationhood3 in civics: iStability += 2
	
	#	Society
	if iLibertarianism3 in civics:
		if iHomesteads3 in civics: iStability += 2
		if iHegemony3 in civics: iStability -= 2
	
	if iProfiteering3 in civics:
		if iManifestDestiny3 in civics: iStability += 2
	
	if iOpportunity3 in civics:
		if iHomesteads3 in civics: iStability += 2
		if iAssimilation3 in civics: iStability += 2
	
	if iEmancipation3 in civics:
		if iManifestDestiny3 in civics: iStability -= 2
		if iDecolonization3 in civics: iStability += 2
	
	if iNativism3 in civics:
		if iAssimilation3 in civics: iStability -= 2
		if iNationhood3 in civics: iStability += 2
	
	if iEgalitarianism3 in civics:
		if iManifestDestiny3 in civics: iStability -= 2
		if iHegemony3 in civics: iStability += 2
	
	
	return iStability

def sigmoid(x):
	return math.tanh(5 * x / 2)
	
def count(iterable, function = lambda x: True):
	return len([element for element in iterable if function(element)])
	
def calculateTrendScore(lTrend):
	iPositive = 0
	iNeutral = 0
	iNegative = 0
	
	for iEntry in lTrend:
		if iEntry > 0: iPositive += 1
		elif iEntry < 0: iNegative += 1
		else: iNeutral += 1
		
	if iPositive > iNegative: return max(0, iPositive - iNegative - iNeutral / 2)
	
	if iNegative > iPositive: return min(0, iPositive - iNegative + iNeutral / 2)
	
	return 0
	
def calculateSumScore(lScores, iThreshold = 1):
	lThresholdScores = [sign(iScore) for iScore in lScores if abs(iScore) >= iThreshold]
	iSum = sum(lThresholdScores)
	iCap = len(lScores) / 2
	
	if abs(iSum) > iCap: iSum = sign(iSum) * iCap
	
	return iSum
	
def updateEconomyTrend(iPlayer):
	pPlayer = player(iPlayer)
	
	if not pPlayer.isExisting(): return
	
	iPreviousCommerce = data.players[iPlayer].iPreviousCommerce
	iCurrentCommerce = pPlayer.calculateTotalCommerce()
	
	if iPreviousCommerce == 0: 
		data.players[iPlayer].iPreviousCommerce = iCurrentCommerce
		return
	
	iCivicEconomy = pPlayer.getCivics(3)
		
	iPositiveThreshold = 5
	iNegativeThreshold = 0
	
	if isDecline(iPlayer):
		iNegativeThreshold = 2
	
	iPercentChange = 100 * iCurrentCommerce / iPreviousCommerce - 100
	
	if iPercentChange > iPositiveThreshold: data.players[iPlayer].pushEconomyTrend(1)
	elif iPercentChange < iNegativeThreshold: data.players[iPlayer].pushEconomyTrend(-1)
	else: data.players[iPlayer].pushEconomyTrend(0)
	
	data.players[iPlayer].iPreviousCommerce = iCurrentCommerce
	
def updateHappinessTrend(iPlayer):
	pPlayer = player(iPlayer)
	
	if not pPlayer.isExisting(): return
	
	iNumCities = pPlayer.getNumCities()
	
	if iNumCities == 0: return
	
	iHappyCities = 0
	iUnhappyCities = 0
	
	iAveragePopulation = pPlayer.getAveragePopulation()
	
	for city in cities.owner(iPlayer):
		iPopulation = city.getPopulation()
		iHappiness = city.happyLevel()
		iUnhappiness = city.unhappyLevel(0)
		iOvercrowding = city.getOvercrowdingPercentAnger(0) * city.getPopulation() / 1000
		iCorporationUnhappinessOffset = min(city.getCorporationBadHappiness(), 3 * city.getCorporationCount())
		
		if city.isWeLoveTheKingDay() or (iPopulation >= iAveragePopulation and iHappiness - iUnhappiness >= iAveragePopulation / 4):
			iHappyCities += 1
		elif iUnhappiness - iOvercrowding - iCorporationUnhappinessOffset > iPopulation / 5 or iUnhappiness - iHappiness > 0:
			iUnhappyCities += 1
			
	iCurrentTrend = 0
			
	if iHappyCities - iUnhappyCities > math.ceil(iNumCities / 5.0): iCurrentTrend = 1
	elif iUnhappyCities - iHappyCities > math.ceil(iNumCities / 5.0): iCurrentTrend = -1
	
	data.players[iPlayer].pushHappinessTrend(iCurrentTrend)
	
def updateWarTrend(iPlayer, iEnemy):
	iOurCurrentSuccess = team(iPlayer).AI_getWarSuccess(iEnemy)
	iTheirCurrentSuccess = team(iEnemy).AI_getWarSuccess(iPlayer)
	
	iOurLastSuccess = data.players[iPlayer].lLastWarSuccess[iEnemy]
	iTheirLastSuccess = data.players[iEnemy].lLastWarSuccess[iPlayer]
	
	iOurGain = max(0, iOurCurrentSuccess - iOurLastSuccess)
	iTheirGain = max(0, iTheirCurrentSuccess - iTheirLastSuccess)
	
	if iOurGain - iTheirGain > 0:
		iCurrentTrend = 1
	elif iOurGain - iTheirGain < 0:
		iCurrentTrend = -1
	elif abs(iOurCurrentSuccess - iTheirCurrentSuccess) >= max(iOurCurrentSuccess, iTheirCurrentSuccess) / 5:
		iCurrentTrend = sign(iOurCurrentSuccess - iTheirCurrentSuccess)
	else:
		iCurrentTrend = 0
	
	data.players[iPlayer].pushWarTrend(iEnemy, iCurrentTrend)
	
def startWar(iPlayer, iEnemy):
	data.players[iPlayer].lWarTrend[iEnemy] = []
	data.players[iEnemy].lWarTrend[iPlayer] = []
	
	data.players[iPlayer].lWarStartTurn[iEnemy] = turn()
	data.players[iEnemy].lWarStartTurn[iPlayer] = turn()
	
def calculateCommerceRank(iPlayer, iTurn):
	return players.major().rank(iPlayer, lambda p: player(p).getEconomyHistory(iTurn))
	
def calculatePowerRank(iPlayer, iTurn):
	return players.major().rank(iPlayer, lambda p: player(p).getPowerHistory(iTurn))
	
def calculateRankedAttitudes(iPlayer, lContacts):
	contacts = players.of(*lContacts).including(iPlayer).sort(game.getPlayerScore, True)
	iPlayerIndex = contacts.index(iPlayer)
	
	iRangeSize = 4
	if iPlayerIndex <= len(contacts) / 5:
		iRangeSize = 3
	
	iRange = len(contacts) / iRangeSize
	iLeft = max(0, iPlayerIndex - iRange/2)
	iRight = min(iLeft + iRange, len(contacts)-1)
	
	lStronger = [calculateAttitude(iLoopPlayer, iPlayer) for iLoopPlayer in contacts[:iLeft] if iLoopPlayer != iPlayer]
	lEqual = [calculateAttitude(iLoopPlayer, iPlayer) for iLoopPlayer in contacts[iLeft:iRight] if iLoopPlayer != iPlayer]
	lWeaker = [calculateAttitude(iLoopPlayer, iPlayer) for iLoopPlayer in contacts[iRight:] if iLoopPlayer != iPlayer]
	
	return lStronger, lEqual, lWeaker
	
def calculateAttitude(iFromPlayer, iToPlayer):
	pPlayer = player(iFromPlayer)

	iAttitude = pPlayer.AI_getAttitudeVal(iToPlayer)
	iAttitude -= pPlayer.AI_getSameReligionAttitude(iToPlayer)
	iAttitude -= pPlayer.AI_getDifferentReligionAttitude(iToPlayer)
	iAttitude -= pPlayer.AI_getFirstImpressionAttitude(iToPlayer)
	
	if team(iFromPlayer).isVassal(team(iToPlayer).getID()) and not team(iFromPlayer).isCapitulated():
		iAttitude -= 100
	
	return iAttitude
	
def isTolerated(iPlayer, iReligion):
	pPlayer = player(iPlayer)
	iStateReligion = pPlayer.getStateReligion()
	
	# should not be asked, but still check
	if iStateReligion == iReligion: return True
	
	# civics
	if pPlayer.getCivics(4) in [iOpportunity2, iOpportunity3, iEgalitarianism3]: return True
	
	# Exceptions
	if iStateReligion == iConfucianism and iReligion == iTaoism: return True
	if iStateReligion == iTaoism and iReligion == iConfucianism: return True
	if iStateReligion == iHinduism and iReligion == iBuddhism: return True
	if iStateReligion == iBuddhism and iReligion == iHinduism: return True
	
	
	return False
	
def getAdministrationModifier(iPlayer):
	iEra = player(iPlayer).getCurrentEra()
	iModifier = tEraAdministrationModifier[iEra] + dCivilizationAdministrationModifier[iPlayer]

	return max(100, iModifier)
	
def isDecline(iPlayer):
	return not player(iPlayer).isHuman() and year() >= year(dFall[iPlayer])

		