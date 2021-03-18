# Rhye's and Fall of Civilization - Barbarian units and cities

from CvPythonExtensions import *
import CvUtil
import PyHelpers	# LOQ
#import Popup
#import cPickle as pickle
from RFCUtils import utils
from Consts import *
from StoredData import data

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer	# LOQ

# Spawning cities (Leoreth)
# Year, coordinates, owner, name, population, unit type, unit number, religions, forced spawn
# MacAurther TODO: For now, iIndependent is Dutch, iIndependent2 is Swedish
tMinorCities = (
	(1624, (134, 60), iIndependent, 'Fort Orange', 1, iMusketman, 1),			# Fort Orange (Albany)
	(1625, (137, 54), iIndependent, 'Nieuw Amsterdam', 1, iMusketman, 1),		# New Amsterdam (New York)
	(1630, (140, 57), iIndependent, 'Fort de Goede Hoop', 1, iMusketman, 1),	# Fort de Goede Hoop (Hartford)
	(1638, (134, 48), iIndependent2, 'Fort Kristina', 1, iMusketman, 1),		# Fort Kristina (Wilmington)
	(1653, (129, 34), iIndependent2, 'Raleigh', 1, iMusketman, 1),				# Albemarle Settlers
)

# do some research on dates here
# MacAurther TODO: Add natives
tMinorStates = (
	(1600, 1700, (113, 48), [iArcher, iSwordsman]),	# Powhatan
)

# Native Spawn Areas
tEastVATL = (128, 37)
tEastVABR = (132, 41)

tEastMABR = (140, 59)
tEastMATL = (143, 62)
tEastNHBR = (139, 62)
tEastNHTL = (142, 66)
tCNBR = (137, 56)
tCNTL = (141, 60)

#handicap level modifier
iHandicapOld = (gc.getGame().getHandicapType() - 1)

class Barbs:
		
	def checkTurn(self, iGameTurn):
		
		#handicap level modifier
		iHandicap = gc.getHandicapInfo(gc.getGame().getHandicapType()).getBarbarianSpawnModifier()
		
		# Leoreth: buff certain cities if independent / barbarian (imported from SoI)
		if iGameTurn % 20 == 10:
			for tMinorState in tMinorStates:
				iStartYear, iEndYear, tPlot, lUnitList = tMinorState
				if utils.isYearIn(iStartYear, iEndYear):
					x, y = tPlot
					plot = gc.getMap().plot(x, y)
					iOwner = plot.getOwner()
					if plot.isCity() and plot.getNumUnits() < 4 and iOwner >= iNumPlayers:
						iUnit = utils.getRandomEntry(lUnitList)
						utils.makeUnit(iUnit, iOwner, tPlot, 1)

		#American natives
		# MacAurther TODO: This is not fun, find something better:
		'''if iGameTurn == getTurnForYear(1610): #Powhatan War I
			self.checkSpawn(iNative, iWarrior, 2 + iHandicap, tEastVABR, tEastVATL, self.spawnUprising, iGameTurn, 1, 0)
		if iGameTurn == getTurnForYear(1622): #Powhatan War II
			self.checkSpawn(iNative, iWarrior, 1 + iHandicap, tEastVABR, tEastVATL, self.spawnUprising, iGameTurn, 1, 0)
			self.checkSpawn(iNative, iArcher, 0 + iHandicap, tEastVABR, tEastVATL, self.spawnUprising, iGameTurn, 1, 0)
		if iGameTurn == getTurnForYear(1636): #Pequot War
			self.checkSpawn(iNative, iWarrior, 1 + iHandicap, tEastMABR, tEastMATL, self.spawnUprising, iGameTurn, 1, 0)
			self.checkSpawn(iNative, iArcher, 1 + iHandicap, tEastMABR, tEastMATL, self.spawnUprising, iGameTurn, 1, 0)
			self.checkSpawn(iNative, iWarrior, 1 + iHandicap, tCNBR, tCNTL, self.spawnUprising, iGameTurn, 1, 0)
			self.checkSpawn(iNative, iArcher, 1 + iHandicap, tCNBR, tCNTL, self.spawnUprising, iGameTurn, 1, 0)
		if iGameTurn == getTurnForYear(1644): #Powhatan War III
			self.checkSpawn(iNative, iWarrior, 2 + iHandicap, tEastVABR, tEastVATL, self.spawnUprising, iGameTurn, 1, 0)
			self.checkSpawn(iNative, iArcher, 0 + iHandicap, tEastVABR, tEastVATL, self.spawnUprising, iGameTurn, 1, 0)
		if iGameTurn == getTurnForYear(1675): #King Phillip's War
			self.checkSpawn(iNative, iWarrior, 2 + iHandicap, tEastMABR, tEastMATL, self.spawnUprising, iGameTurn, 1, 0)
			self.checkSpawn(iNative, iArcher, 2 + iHandicap, tEastMABR, tEastMATL, self.spawnUprising, iGameTurn, 1, 0)
			self.checkSpawn(iNative, iWarrior, 1 + iHandicap, tCNBR, tCNTL, self.spawnUprising, iGameTurn, 1, 0)
			self.checkSpawn(iNative, iArcher, 1 + iHandicap, tCNBR, tCNTL, self.spawnUprising, iGameTurn, 1, 0)
			self.checkSpawn(iNative, iWarrior, 1 + iHandicap, tEastNHBR, tEastNHTL, self.spawnUprising, iGameTurn, 1, 0)
			self.checkSpawn(iNative, iArcher, 0 + iHandicap, tEastNHBR, tEastNHTL, self.spawnUprising, iGameTurn, 1, 0)'''
		
		
		
		
		
		#MacAurther: Old Natives
		'''if utils.isYearIn(600, 1100):
			self.checkSpawn(iNative, iDogSoldier, 1 + iHandicap, (15, 38), (24, 47), self.spawnNatives, iGameTurn, 20, 0)
		if utils.isYearIn(1300, 1600):
			self.checkSpawn(iNative, iDogSoldier, 2 + iHandicap, (15, 38), (24, 47), self.spawnNatives, iGameTurn, 8, 0)
		if utils.isYearIn(1400, 1800):
			self.checkSpawn(iNative, iDogSoldier, 1 + iHandicap, (11, 44), (33, 51), self.spawnUprising, iGameTurn, 12, 0)
			self.checkSpawn(iNative, iDogSoldier, 1 + iHandicap, (11, 44), (33, 51), self.spawnUprising, iGameTurn, 12, 6)
		if utils.isYearIn(1300, 1600):
			if iGameTurn % 18 == 0:
				if not gc.getMap().plot(27, 29).isUnit():
					utils.makeUnitAI(iDogSoldier, iNative, (27, 29), UnitAITypes.UNITAI_ATTACK, 2 + iHandicap)
			elif iGameTurn % 18 == 9:
				if not gc.getMap().plot(30, 13).isUnit():
					utils.makeUnitAI(iDogSoldier, iNative, (30, 13), UnitAITypes.UNITAI_ATTACK, 2 + iHandicap)
		
		if self.includesActiveHuman([iAmerica, iEngland, iFrance]):
			if utils.isYearIn(1700, 1900):
				self.checkSpawn(iNative, iMountedBrave, 1 + iHandicap, (15, 44), (24, 52), self.spawnNomads, iGameTurn, 12 - iHandicap, 2)
			
			if utils.isYearIn(1500, 1850):
				self.checkSpawn(iNative, iMohawk, 1, (24, 46), (30, 51), self.spawnUprising, iGameTurn, 8, 4)'''
				

		#pirates in the Caribbean
		# MacAurther TODO: Make this not impossible to defend against
		#if utils.isYearIn(1700, 1800):
		#	self.checkSpawn(iNative, iPrivateer, 1, (122, 0), (126, 2), self.spawnPirates, iGameTurn, 5, 0)

		if iGameTurn < getTurnForYear(tMinorCities[len(tMinorCities)-1][0])+10:
			self.foundMinorCities(iGameTurn)
				
	def foundMinorCities(self, iGameTurn):
		for i in range(len(tMinorCities)):
			iYear, tPlot, iPlayer, sName, iPopulation, iUnitType, iNumUnits = tMinorCities[i]
			if iGameTurn < getTurnForYear(iYear): return
			if iGameTurn > getTurnForYear(iYear)+10: continue
			
			if data.lMinorCityFounded[i]: continue
			
			x, y = tPlot
			plot = gc.getMap().plot(x, y)
			if plot.isCity(): continue
			
			# special cases
			if not self.canFoundCity(sName): continue
			
			lReligions = []
			bForceSpawn = False
			
			
			if not self.isFreePlot(tPlot, bForceSpawn): continue
			
			utils.evacuate(iPlayer, tPlot)
		
			if self.foundCity(iPlayer, tPlot, sName, iPopulation, iUnitType, iNumUnits, lReligions):
				data.lMinorCityFounded[i] = True
		
	def canFoundCity(self, sName):
		
		return True
	
	def foundCity(self, iPlayer, tPlot, sName, iPopulation, iUnitType = -1, iNumUnits = -1, lReligions = []):
		pPlayer = gc.getPlayer(iPlayer)
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		plot.setOwner(iPlayer)
		pPlayer.found(x, y)
		
		if plot.isCity():
			city = gc.getMap().plot(x, y).getPlotCity()
			
			city.setName(sName, False)
			city.setPopulation(iPopulation)
			
			# MacAurther: Don't give indies free culture
			#plot.changeCulture(iPlayer, 10 * (gc.getGame().getCurrentEra() + 1), True)
			#city.changeCulture(iPlayer, 10 * (gc.getGame().getCurrentEra() + 1), True)
			
			if iNumUnits > 0 and iUnitType > 0:
				utils.makeUnit(iUnitType, iPlayer, tPlot, iNumUnits)
				
			for iReligion in lReligions:
				if gc.getGame().isReligionFounded(iReligion):
					city.setHasReligion(iReligion, True, False, False)
					
			return True
		
		return False
					
	def clearUnits(self, iPlayer, tPlot): # Unused
		lHumanUnits = []
		lOtherUnits = []
	
		for (x, y) in utils.surroundingPlots(tPlot):
			plot = gc.getMap().plot(x, y)
			
			for iUnit in range(plot.getNumUnits()):
				unit = plot.getUnit(iUnit)
				
				if unit.getOwner() == utils.getHumanID():
					lHumanUnits.append(unit)
				else:
					lOtherUnits.append(unit)
						
		capital = gc.getPlayer(utils.getHumanID()).getCapitalCity()
		for unit in lHumanUnits:
			print "SETXY barbs 1"
			unit.setXY(capital.getX(), capital.getY(), False, True, False)
			
		for unit in lOtherUnits:
			utils.makeUnit(unit.getUnitType(), iPlayer, tPlot, 1)
			unit.kill(False, iBarbarian)
				
	def isFreePlot(self, tPlot, bIgnoreCulture = False):
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		
		# no cultural control over the tile
		if plot.isOwned() and plot.getOwner() < iNumPlayers and not bIgnoreCulture:
			return False
				
		# no city in adjacent tiles
		for (i, j) in utils.surroundingPlots(tPlot):
			currentPlot = gc.getMap().plot(i, j)
			if currentPlot.isCity(): return False
						
		return True
			
	def checkRegion(self, tCity): # Unusued
		cityPlot = gc.getMap().plot(tCity[0], tCity[1])
		iNumUnitsInAPlot = cityPlot.getNumUnits()
##		print iNumUnitsInAPlot
		
		#checks if the plot already belongs to someone
		if cityPlot.isOwned():
			if cityPlot.getOwner() != iBarbarian:
				return (False, -1)
		
##		#checks if there's a unit on the plot
		if iNumUnitsInAPlot > 0:
			for i in range(iNumUnitsInAPlot):
				unit = cityPlot.getUnit(i)
				iOwner = unit.getOwner()
				if iOwner == iBarbarian:
					return (False, tCity[3]+1)

		#checks the surroundings and allows only AI units
		for (x, y) in utils.surroundingPlots(tCity[0], tCity[1]):
			currentPlot=gc.getMap().plot(x,y)
			if currentPlot.isCity():
				return (False, -1)
			iNumUnitsInAPlot = currentPlot.getNumUnits()
			if iNumUnitsInAPlot > 0:
				for i in range(iNumUnitsInAPlot):
					unit = currentPlot.getUnit(i)
					iOwner = unit.getOwner()
					pOwner = gc.getPlayer(iOwner)
					if pOwner.isHuman():
						return (False, tCity[3]+1)
		return (True, tCity[3])

	def killNeighbours(self, tCoords): # Unused
		'Kills all units in the neigbbouring tiles of plot (as well as plot itself) so late starters have some space.'
		for (x, y) in utils.surroundingPlots(tCoords):
			killPlot = CyMap().getPlot(x, y)
			for i in range(killPlot.getNumUnits()):
				unit = killPlot.getUnit(0)	# 0 instead of i because killing units changes the indices
				unit.kill(False, iBarbarian)
				
	# Leoreth: check region for number of units first
	def checkLimitedSpawn(self, iPlayer, iUnitType, iNumUnits, iMaxUnits, tTL, tBR, spawnFunction, iTurn, iPeriod, iRest, lAdj=[]):
		if iTurn % utils.getTurns(iPeriod) == iRest:
			lAreaUnits = utils.getAreaUnits(iPlayer, tTL, tBR)
			if len(lAreaUnits) < iMaxUnits:
				self.checkSpawn(iPlayer, iUnitType, iNumUnits, tTL, tBR, spawnFunction, iTurn, iPeriod, iRest, lAdj)
						
	# Leoreth: new ways to spawn barbarians
	def checkSpawn(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, spawnFunction, iTurn, iPeriod, iRest, lAdj=[]):
		if len(lAdj) == 0:
			sAdj = ""
		else:
			sAdj = utils.getRandomEntry(lAdj)
	
		if iTurn % utils.getTurns(iPeriod) == iRest:
			spawnFunction(iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj)
			
	def possibleTiles(self, tTL, tBR, bWater=False, bTerritory=False, bBorder=False, bImpassable=False, bNearCity=False):
		return [tPlot for tPlot in utils.getPlotList(tTL, tBR) if self.possibleTile(tPlot, bWater, bTerritory, bBorder, bImpassable, bNearCity)]
		
	def possibleTile(self, tPlot, bWater, bTerritory, bBorder, bImpassable, bNearCity):
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		lSurrounding = utils.surroundingPlots(tPlot)
		
		# never on peaks
		if plot.isPeak(): return False
		
		# only land or water
		if bWater != plot.isWater(): return False
		
		# only inside territory if specified
		if not bTerritory and plot.getOwner() >= 0: return False
		
		# never directly next to cities
		if [(i, j) for (i, j) in lSurrounding if gc.getMap().plot(i, j).isCity()]: return False
		
		# never on tiles with units
		if plot.isUnit(): return False
		
		# never in marsh (impassable)
		if plot.getFeatureType() == iMarsh: return False
		
		# allow other impassable terrain (ocean, jungle)
		if not bImpassable:
			if plot.getTerrainType() == iOcean: return False
			if plot.getFeatureType() == iJungle: return False
		
		# restrict to borders if specified
		if bBorder and not [(i, j) for (i, j) in lSurrounding if gc.getMap().plot(i, j).getOwner() != plot.getOwner()]: return False
		
		# near a city if specified (next to cities excluded above)
		if bNearCity and not [(i, j) for (i, j) in utils.surroundingPlots(tPlot, 2, lambda (a, b): not gc.getMap().plot(a, b).isCity())]: return False
		
		# not on landmasses without cities
		if not bWater and gc.getMap().getArea(plot.getArea()).getNumCities() == 0: return False
		
		return True

	def spawnPirates(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: spawns all ships at the same coastal spot, out to pillage and disrupt trade, can spawn inside borders'''
		
		lPlots = self.possibleTiles(tTL, tBR, bWater=True, bTerritory=False)
		tPlot = utils.getRandomEntry(lPlots)
		
		if tPlot:
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_PIRATE_SEA, iNumUnits, sAdj)
		
	def spawnNatives(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: outside of territory, in jungles, all dispersed on several plots, out to pillage'''
		
		lPlots = self.possibleTiles(tTL, tBR, bTerritory=False, bImpassable=True)
		
		for i in range(iNumUnits):
			tPlot = utils.getRandomEntry(lPlots)
			if not tPlot: break
			
			lPlots.remove(tPlot)
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, 1, sAdj)
			
	def spawnMinors(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: represents minor states without ingame cities
			    outside of territory, not in jungles, in groups, passive'''
			    
		lPlots = self.possibleTiles(tTL, tBR, bTerritory=False)
		tPlot = utils.getRandomEntry(lPlots)
		
		if tPlot:
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, iNumUnits, sAdj)
		
	def spawnNomads(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: represents aggressive steppe nomads etc.
			    outside of territory, not in jungles, in small groups, target cities'''
		
		lPlots = self.possibleTiles(tTL, tBR, bTerritory=False)
		tPlot = utils.getRandomEntry(lPlots)
		
		if tPlot:
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, iNumUnits, sAdj)
			
	def spawnInvaders(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''Leoreth: represents large invasion forces and migration movements
			    inside of territory, not in jungles, in groups, target cities'''
			    
		lPlots = self.possibleTiles(tTL, tBR, bTerritory=True, bBorder=True)
		tPlot = utils.getRandomEntry(lPlots)
		
		if tPlot:
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, iNumUnits, sAdj)
			
	def spawnUprising(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		''' Leoreth: represents uprisings of Natives against colonial settlements, especially North America
			     spawns units in a free plot in the second ring of a random target city in the area
			     (also used for units from warring city states in classical Mesoamerica)'''
		
		lPlots = self.possibleTiles(tTL, tBR, bTerritory=True, bNearCity=True)
		tPlot = utils.getRandomEntry(lPlots)
		
		if tPlot:
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK, iNumUnits, sAdj)
		
			
	def includesActiveHuman(self, lPlayers):
		return utils.getHumanID() in lPlayers and tBirth[utils.getHumanID()] <= gc.getGame().getGameTurnYear()

	
	def spawnNativesTerritory(self, iPlayer, iUnitType, iNumUnits, tTL, tBR, sAdj=""):
		'''MacAurther: regardless of territory, all dispersed on several plots, out to pillage'''
		
		lPlots = self.possibleTiles(tTL, tBR, bTerritory=True, bImpassable=False)
		
		for i in range(iNumUnits):
			tPlot = utils.getRandomEntry(lPlots)
			if not tPlot: break
			
			lPlots.remove(tPlot)
			utils.makeUnitAI(iUnitType, iPlayer, tPlot, UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, 1, sAdj)

	def spawnPowhatanWarriorsI(self, iNumUnits):
		iHandicap = gc.getHandicapInfo(gc.getGame().getHandicapType()).getBarbarianSpawnModifier()
		#self.spawnNativesTerritory(iNative, iWarrior, iNumUnits + iHandicap, tEastVATL, tEastVABR)
		utils.makeUnitAI(iWarrior, iNative, (131,40), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, iNumUnits + iHandicap)