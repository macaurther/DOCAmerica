from RFCUtils import *
from Consts import *
from StoredData import data

from Events import handler
from Core import *
from Locations import *

# Spawning cities (Leoreth)
# Year, coordinates, owner, name, population, unit type, unit number, religions, forced spawn
tMinorCities = (
(-250, (19, 35), iNative, 'Danibaan', 2, iHolkan, 1),	# Monte Albán
(100, (18, 37), iBarbarian, 'Tolan', 2, iJaguar, 2),		# Teotihuacan
)

# do some research on dates here
tMinorStates = (
)

#handicap level modifier
iHandicapOld = (game.getHandicapType() - 1)


@handler("BeginGameTurn")
def helpMinorStates():
	if every(20):
		for iStartYear, iEndYear, tPlot, lUnits in tMinorStates:
			if year().between(iStartYear, iEndYear):
				plot = plot_(tPlot)
				iOwner = plot.getOwner()
				if plot.isCity() and is_minor(iOwner) and plot.getNumUnits() < 4:
					makeUnit(iOwner, random_entry(lUnits), plot)


@handler("BeginGameTurn")
def spawnBarbarians(iGameTurn):
	iHandicap = infos.handicap().getBarbarianSpawnModifier()

	if year().between(250, -850):
		if iHandicap >= 0:
			checkSpawn(iBarbarian, iWarrior, 1, (76, 46), (99, 53), spawnMinors, iGameTurn, 5, 0)
		
		checkSpawn(iBarbarian, iWolf, 1, (75, 54), (104, 64), spawnNatives, iGameTurn, 5, 2)
		checkSpawn(iBarbarian, iBear, 1, (75, 54), (104, 64), spawnNatives, iGameTurn, 5, 4)
		checkLimitedSpawn(iBarbarian, iLion, 1, 5, (60, 10), (72, 28), spawnNatives, iGameTurn, 5, 1)
		checkLimitedSpawn(iBarbarian, iPanther, 1, 5, (60, 10), (72, 28), spawnNatives, iGameTurn, 5, 3)
	
	# Holkans in classical Mesoamerica
	if year().between(-200, 100):
		checkSpawn(iBarbarian, iHolkan, 1, (17, 31), (25, 37), spawnUprising, iGameTurn, 7, 5)
	if year().between(100, 600):
		checkSpawn(iBarbarian, iHolkan, 1, (17, 31), (25, 37), spawnUprising, iGameTurn, 6, 4)	
	elif year().between(600, 1000):
		checkSpawn(iBarbarian, iHolkan, 1, (17, 31), (25, 37), spawnUprising, iGameTurn, 4, 2)
		
	#pirates in Mediterranean
	if year().between(-210, 50):
		checkSpawn(iBarbarian, iWarGalley, 1, (49, 37), (72, 44), spawnPirates, iGameTurn, 8, 0)

	#American natives
	if year().between(600, 1100):
		checkSpawn(iNative, iDogSoldier, 1 + iHandicap, (15, 38), (24, 47), spawnNatives, iGameTurn, 20, 0)
		if scenario() == i3000BC:  #late start condition
			checkSpawn(iNative, iJaguar, 3, (15, 38), (24, 47), spawnNatives, iGameTurn, 16 - 2*iHandicap, 10)
		else:  #late start condition
			checkSpawn(iNative, iJaguar, 2, (15, 38), (24, 47), spawnNatives, iGameTurn, 16 - 2*iHandicap, 10)
	if year().between(1300, 1600):
		checkSpawn(iNative, iDogSoldier, 2 + iHandicap, (15, 38), (24, 47), spawnNatives, iGameTurn, 8, 0)
	if year().between(1400, 1800):
		checkSpawn(iNative, iDogSoldier, 1 + iHandicap, (11, 44), (33, 51), spawnUprising, iGameTurn, 12, 0)
		checkSpawn(iNative, iDogSoldier, 1 + iHandicap, (11, 44), (33, 51), spawnUprising, iGameTurn, 12, 6)
	if year().between(1300, 1600):
		if iGameTurn % 18 == 0:
			if not plot_(27, 29).isUnit():
				makeUnits(iNative, iDogSoldier, (27, 29), 2 + iHandicap, UnitAITypes.UNITAI_ATTACK)
		elif iGameTurn % 18 == 9:
			if not plot_(30, 13).isUnit():
				makeUnits(iNative, iDogSoldier, (30, 13), 2 + iHandicap, UnitAITypes.UNITAI_ATTACK)
	
	if includesActiveHuman(iAmerica, iEngland, iFrance):
		if year().between(1700, 1900):
			checkSpawn(iNative, iMountedBrave, 1 + iHandicap, (15, 44), (24, 52), spawnNomads, iGameTurn, 12 - iHandicap, 2)
		
		if year().between(1500, 1850):
			checkSpawn(iNative, iMohawk, 1, (24, 46), (30, 51), spawnUprising, iGameTurn, 8, 4)
			
	if iGameTurn == year(-500):
		plot_(19, 35).setImprovementType(iHut)
		makeUnits(iNative, iHolkan, (19, 35), 2, UnitAITypes.UNITAI_ATTACK)
		
	#pirates in the Caribbean
	if year().between(1600, 1800):
		checkSpawn(iNative, iPrivateer, 1, (24, 32), (35, 46), spawnPirates, iGameTurn, 5, 0)

	if iGameTurn == year(dBirth[iInca]):
		if player(iInca).isHuman():
			makeUnit(iNative, iAucac, (24, 26))
			makeUnit(iNative, iAucac, (25, 23))
				
def foundMinorCities(iGameTurn):
	for i, (iYear, tPlot, iCiv, sName, iPopulation, iUnitType, iNumUnits) in enumerate(tMinorCities):
		if iGameTurn < year(iYear): return
		if iGameTurn > year(iYear)+10: continue
		
		if data.lMinorCityFounded[i]: continue
		
		if plot(tPlot).isCity(): continue
		
		# special cases
		if not canFoundCity(sName): continue
		
		lReligions = []
		bForceSpawn = False
		
		if not isFree(iCiv, tPlot, bNoCity=True, bNoCulture=not bForceSpawn): continue
		
		evacuate(slot(iCiv), tPlot)
	
		if foundCity(iCiv, tPlot, sName, iPopulation, iUnitType, iNumUnits, lReligions):
			data.lMinorCityFounded[i] = True
		
def canFoundCity(sName):
	
	return True
	
def foundCity(iCiv, (x, y), sName, iPopulation, iUnitType = -1, iNumUnits = -1, lReligions = []):
	iPlayer = slot(iCiv)
	pPlayer = player(iPlayer)
	plot(x, y).setOwner(iPlayer)
	pPlayer.found(x, y)
	
	founded = city(x, y)
	if founded:
		founded.setName(sName, False)
		founded.setPopulation(iPopulation)
		
		plot(founded).changeCulture(iPlayer, 10 * (game.getCurrentEra() + 1), True)
		founded.changeCulture(iPlayer, 10 * (game.getCurrentEra() + 1), True)
		
		if iNumUnits > 0 and iUnitType > 0:
			makeUnits(iPlayer, iUnitType, founded, iNumUnits)
			
		for iReligion in lReligions:
			if game.isReligionFounded(iReligion):
				founded.setHasReligion(iReligion, True, False, False)
				
		return True
	
	return False

def checkLimitedSpawn(iCiv, iUnitType, iNumUnits, iMaxUnits, tTL, tBR, spawnFunction, iTurn, iPeriod, iRest, lAdj=[]):
	iAreaUnits = plots.start(tTL).end(tBR).units().owner(iCiv).count()
	if iAreaUnits < iMaxUnits:
		checkSpawn(iCiv, iUnitType, iNumUnits, tTL, tBR, spawnFunction, iTurn, iPeriod, iRest, lAdj)
					
# Leoreth: new ways to spawn barbarians
def checkSpawn(iCiv, iUnitType, iNumUnits, tTL, tBR, spawnFunction, iTurn, iPeriod, iRest, lAdj=[]):	
	if periodic(iPeriod):
		spawnFunction(slot(iCiv), iUnitType, iNumUnits, tTL, tBR, random_entry(lAdj))
			
def possibleTiles(tTL, tBR, bWater=False, bTerritory=False, bBorder=False, bImpassable=False, bNearCity=False):
	return plots.start(tTL).end(tBR).where(lambda p: possibleTile(p, bWater, bTerritory, bBorder, bImpassable, bNearCity))
	
def possibleTile(plot, bWater, bTerritory, bBorder, bImpassable, bNearCity):
	# never on peaks
	if plot.isPeak(): return False
	
	# only land or water
	if bWater != plot.isWater(): return False
	
	# only inside territory if specified
	if not bTerritory and plot.isOwned(): return False
	
	# never directly next to cities
	if cities.surrounding(plot): return False
	
	# never on tiles with units
	if plot.isUnit(): return False
	
	# never in marsh (impassable)
	if plot.getFeatureType() == iMarsh: return False
	
	# allow other impassable terrain (ocean, jungle)
	if not bImpassable:
		if plot.getTerrainType() == iOcean: return False
		if plot.getFeatureType() == iJungle: return False
	
	# restrict to borders if specified
	if bBorder and not plots.surrounding(plot).notowner(plot.getOwner()): return False
	
	# near a city if specified (next to cities excluded above)
	if bNearCity and not plots.surrounding(plot, radius=2).where(lambda p: not p.isCity()): return False
	
	# not on landmasses without cities
	if not bWater and map.getArea(plot.getArea()).getNumCities() == 0: return False
	
	return True

def spawnPirates(iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
	'''Leoreth: spawns all ships at the same coastal spot, out to pillage and disrupt trade, can spawn inside borders'''
	plot = possibleTiles(tTL, tBR, bWater=True, bTerritory=False).random()
	
	if plot:
		makeUnits(iPlayer, iUnitType, plot, iNumUnits, UnitAITypes.UNITAI_PIRATE_SEA).adjective(sAdj)
	
def spawnNatives(iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
	'''Leoreth: outside of territory, in jungles, all dispersed on several plots, out to pillage'''
	for plot in possibleTiles(tTL, tBR, bTerritory=False, bImpassable=True).sample(iNumUnits):
		makeUnits(iPlayer, iUnitType, plot, 1, UnitAITypes.UNITAI_ATTACK).adjective(sAdj)
		
def spawnMinors(iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
	'''Leoreth: represents minor states without ingame cities
			outside of territory, not in jungles, in groups, passive'''
	plot = possibleTiles(tTL, tBR, bTerritory=False).random()
	
	if plot:
		makeUnits(iPlayer, iUnitType, plot, iNumUnits, UnitAITypes.UNITAI_ATTACK).adjective(sAdj)
	
def spawnNomads(iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
	'''Leoreth: represents aggressive steppe nomads etc.
			outside of territory, not in jungles, in small groups, target cities'''
	plot = possibleTiles(tTL, tBR, bTerritory=False).random()
	
	if plot:
		makeUnits(iPlayer, iUnitType, plot, iNumUnits, UnitAITypes.UNITAI_ATTACK).adjective(sAdj)
		
def spawnInvaders(iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
	'''Leoreth: represents large invasion forces and migration movements
			inside of territory, not in jungles, in groups, target cities'''
	plot = possibleTiles(tTL, tBR, bTerritory=True, bBorder=True).random()
	
	if plot:
		makeUnits(iPlayer, iUnitType, plot, iNumUnits, UnitAITypes.UNITAI_ATTACK).adjective(sAdj)
		
def spawnUprising(iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
	''' Leoreth: represents uprisings of Natives against colonial settlements, especially North America
			 spawns units in a free plot in the second ring of a random target city in the area
			 (also used for units from warring city states in classical Mesoamerica)'''
	plot = possibleTiles(tTL, tBR, bTerritory=True, bNearCity=True).random()
	
	if plot:
		makeUnits(iPlayer, iUnitType, plot, iNumUnits, UnitAITypes.UNITAI_ATTACK).adjective(sAdj)
		
def includesActiveHuman(*civs):
	return civ() in civs and year(dBirth[active()]) <= year()