from RFCUtils import *
from Consts import *
from StoredData import data

from Events import handler
from Core import *
from Locations import *

from SettlerMaps import dSettlerMaps

# Spawning cities (Leoreth)
# Year, coordinates, owner, name, population, unit type, unit number, religions, forced spawn
tMinorCities = (
#(250, (36, 60), iNative, 'Calakmul', 2, iHolkan, 3),				# Calakmul
(410, (22, 56), iNative, 'Copan', 2, iMilitia1, 2),					# Copan
(450, (22, 28), iNative, 'Nazca', 2, iMilitia1, 2),					# Nazca
(950, (16, 15), iNative, 'Mapuches', 2, iMilitia1, 2),				# Mapuche
(1836, (33, 70), iIndependent2, 'Houston', 3, iMilitia5, 4),		# Republic of Texas
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

# MacAurther: Tribes reproduce
@handler("EndGameTurn")
def reproduceTribes():
	# Commenting this out because it doesn't work very well
	'''if data.iTribeGenerationTurn + 5 == turn():
		pPlot = possibleTiles(tTribeRespawnArea[0], tTribeRespawnArea[1], bWater=False, bTerritory=False, bTribeSpawn=True).random()
		
		print("Generating new Tribe at x: " + str(pPlot.getX()) + " y: " + str(pPlot.getY()))
		pPlot.setImprovementType(iTribe)
		data.iTribeGenerationTurn = turn()'''

# MacAurther: Pillaging Tribes generates warriors
@handler("unitPillage")
def tribePillage(pUnit, iImprovement, iRoute, iOwner, iGold):
	# If pillage a tribe, get uprising
	if iImprovement == iTribe or iImprovement == iContactedTribe:
		team(pUnit.getOwner()).declareWar(player(iNative).getTeam(), False, WarPlanTypes.WARPLAN_LIMITED)
		iX = pUnit.getX()
		iY = pUnit.getY()
		spawnTribeDefenders(iX, iY)
	
		# If pillage a tribe with the Encomienda or Captives Civics, get Native Slaves
		iPlayer = pUnit.getOwner()
		iSlave = getNativeSlaveType(iPlayer)
		
		if iSlave > -1:
			makeUnit(iPlayer, iSlave, pUnit, UnitAITypes.UNITAI_WORKER)
			message(iPlayer, 'TXT_KEY_UP_ENSLAVE_WIN', sound='SND_REVOLTEND', event=1, button=infos.unit(iSlave).getButton(), color=8, location=pUnit)


@handler("BeginGameTurn")
def spawnBarbarians(iGameTurn):
	iHandicap = infos.handicap().getBarbarianSpawnModifier()

	#pirates in the Caribbean
	if year().between(1600, 1800):
		checkSpawn(iBarbarian, iPrivateer, 1, (41, 57), (58, 66), spawnPirates, iGameTurn, 5, 0)
	
	if iGameTurn < year(tMinorCities[len(tMinorCities)-1][0])+10:
		foundMinorCities(iGameTurn)


def foundMinorCities(iGameTurn):
	for i, (iYear, tPlot, iCiv, sName, iPopulation, iUnitType, iNumUnits) in enumerate(tMinorCities):
		if iGameTurn < year(iYear): return
		if iGameTurn > year(iYear)+10: continue

		if i >= len(data.lMinorCityFounded):
			print("ERROR: Number of independent city definitions exceeds iNumMinorCities. Did you forget to update consts.py?")
			data.lMinorCityFounded.append(False);
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
			
def possibleTiles(tTL, tBR, bWater=False, bTerritory=False, bBorder=False, bImpassable=False, bNearCity=False, bForceSpawn=False, bTribeSpawn=False):
	return plots.start(tTL).end(tBR).where(lambda p: possibleTile(p, bWater, bTerritory, bBorder, bImpassable, bNearCity, bForceSpawn, bTribeSpawn))
	
def possibleTile(plot, bWater, bTerritory, bBorder, bImpassable, bNearCity, bForceSpawn, bTribeSpawn):
	# never on peaks
	if plot.isPeak(): return False
	
	# only land or water
	if bWater != plot.isWater(): return False
	
	# only inside territory if specified
	if not bTerritory and plot.isOwned(): return False
	
	# never directly next to cities, (MacAurther) unless Force Spawn
	if not bForceSpawn and cities.surrounding(plot): return False
	
	# never on tiles with units
	if plot.isUnit(): return False
	
	# never in bog (impassable)
	if plot.getFeatureType() == iBog: return False
	
	# allow other impassable terrain (ocean, jungle)
	if not bImpassable:
		if plot.getTerrainType() == iOcean: return False
		if plot.getFeatureType() == iJungle: return False
	
	# restrict to borders if specified
	if bBorder and not plots.surrounding(plot).notowner(plot.getOwner()): return False
	
	# near a city if specified (next to cities excluded above)
	if bNearCity and not plots.surrounding(plot, radius=2).where(lambda p: not p.isCity()): return False
	
	# not on landmasses without cities, (MacAurther): except if Force Spawn
	if not bForceSpawn and not bWater and map.getArea(plot.getArea()).getNumCities() == 0: return False
	
	# MacAurther: Extra check for Tribe spawning
	# Commenting this out. It just doesn't work very well. 
	'''if bTribeSpawn:
		if (plot.isImpassable()) or (plot.getImprovementType() != ImprovementTypes.NO_IMPROVEMENT) or \
			(plot.getTerrainType() in [iSnow, iSaltflat, iLagoon, iAtoll]) or (plot.getBonusType(-1) != BonusTypes.NO_BONUS):
			return False
	
		# MacAurther: Don't spawn a Tribe next to another Tribe
		for iX in range(-1, 2):
			iCheckX = plot.getX() + iX
			if iCheckX < 0 or iCheckX >= iWorldX:
				continue
			for iY in range(-1, 2):
				iCheckY = plot.getY() + iY
				if iCheckY < 0 or iCheckY >= iWorldY:
					continue
				pCheckPlot = gc.getMap().plot(iCheckX, iCheckY)
				if pCheckPlot.getImprovementType() in [iTribe, iContactedTribe]:
					return False
		
		# Make sure to not cover up an AI's desired spot
		iX = plot.getX()
		iY = plot.getY()
		for iCiv in dSettlerMaps:
			if dSettlerMaps[iCiv][iY][iX] > 90:
				return False'''
	
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

def spawnDefenders(iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
	''' MacAurther: represents Native defenders against tribe pillagers. CAN be next to cities,
	in territory, and in areas with no cities present'''
	plot = possibleTiles(tTL, tBR, bTerritory=True, bForceSpawn=True).random()
	
	if plot:
		makeUnits(iPlayer, iUnitType, plot, iNumUnits, UnitAITypes.UNITAI_ATTACK).adjective(sAdj)

def includesActiveHuman(*civs):
	return civ() in civs and year(dBirth[active()]) <= year()

def spawnTribeDefenders(iX, iY):
	iHandicap = infos.handicap().getBarbarianSpawnModifier()
	
	iRange = 1
	if year() >= year(1650):
		iRange += 1
	if year() >= year(1800):
		iRange += 1
	tTL = (iX - iRange, iY - iRange)
	tBR = (iX + iRange, iY + iRange)
	
	spawnDefenders(iNative, iWarrior, 1 + iHandicap, tTL, tBR)
	spawnDefenders(iNative, iArcher, 1 + iHandicap, tTL, tBR)
	if year() <= year(1650):
		spawnDefenders(iNative, iAtlatlist, iHandicap, tTL, tBR)
		spawnDefenders(iNative, iSpearman, iHandicap, tTL, tBR)
	elif year() <= year(1800):
		spawnDefenders(iNative, iArmedBrave, 1 + iHandicap, tTL, tBR)
	else:
		spawnDefenders(iNative, iMountedBrave, 1 + iHandicap, tTL, tBR)
		