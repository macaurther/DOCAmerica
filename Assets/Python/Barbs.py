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
# MacAurther TODO: For now, iIndependent is Dutch, iIndependent2 is Swedish/other
# MacAurther: Using this to help AI settle some hard-to-reach cities as well
tMinorCities = (
	(1608, (137, 74), iFrance, 'Quebec City', 1, iMusketman, 1),				# Quebec City
	(1624, (134, 60), iIndependent, 'Fort Orange', 1, iMusketman, 1),			# Fort Orange (Albany)
	(1625, (137, 54), iIndependent, 'Nieuw Amsterdam', 1, iMusketman, 1),		# New Amsterdam (New York)
	(1630, (140, 57), iIndependent, 'Fort de Goede Hoop', 1, iMusketman, 1),	# Fort de Goede Hoop (Hartford)
	(1632, (142, 68), iMassachusetts, 'Portland', 1, iMusketman, 1),			# Portland, ME
	(1638, (134, 48), iIndependent2, 'Fort Kristina', 1, iMusketman, 1),		# Fort Kristina (Wilmington)
	(1653, (129, 34), iIndependent2, 'Raleigh', 1, iMusketman, 1),				# Albemarle Settlers
	(1718, (100, 14), iFrance, 'New Orleans', 1, iMusketman, 1),				# New Orleans
	(1732, (134, 43), iMaryland, 'Salisbury', 1, iMusketman, 1),				# Salisbury, MD (help AI maryland settle the Delaware peninsula)
)

#FoB - Spawn Native American Villages
tNativeVillages = (
	#East Coast Tribes
	(1600, (130, 40), iNative),
	(1600, (134, 40), iNative),
	(1600, (128, 38), iNative),
	(1600, (128, 41), iNative),
	(1600, (134, 37), iNative),
	(1600, (142, 69), iNative), # Pennacook
	(1600, (135, 35), iNative), # Mahican
	(1600, (136, 60), iNative), # Wampanoag
	(1600, (127, 58), iNative), # Mohawk
	(1600, (125, 57), iNative), # Oneida
	(1600, (122, 55), iNative), # Onondaga
	(1600, (120, 47), iNative), # Susquehannock
	(1600, (134, 44), iNative), # Lenni-Lenape
	(1600, (131, 32), iNative), # Tuscarora
	(1600, (121, 33), iNative), # Tutelo
	(1600, (114, 26), iNative), # Cherokee
	(1600, (119, 26), iNative), # Catawba
	(1600, (118, 21), iNative), # Yamasee
	(1600, (108, 20), iNative), # Creek
	(1600, (117, 15), iNative), # Timucua
	(1600, (112, 16), iNative), # Apalachee
	(1600, (124, 6), iNative), # Calusa
	#Mid-West Tribes
	(1600, (107, 54), iNative), # Potawatomi
	(1600, (105, 47), iNative), # Miami
	(1600, (114, 48), iNative), # Erie
	(1600, (105, 34), iNative), # Shawnee
	(1600, (100, 40), iNative), # Illinois
	(1600, (99, 51), iNative), # Winnebago
	(1600, (99, 23), iNative), # Chickasaw
	(1600, (101, 17), iNative), # Biloxi
	(1600, (98, 17), iNative), # Natchez
	(1600, (92, 20), iNative), # Caddo
	(1600, (91, 14), iNative), # Atakapa
	#Western Tribes
	#TODO
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

		# FOB - add blocking units
		if iGameTurn == getTurnForYear(1600):
			self.trySpawnNativeBlocker(iWarrior, 2, 98, 26)
			self.trySpawnNativeBlocker(iWarrior, 2, 99, 31)
			self.trySpawnNativeBlocker(iWarrior, 2, 98, 39)
			self.trySpawnNativeBlocker(iWarrior, 2, 98, 16)
			self.trySpawnNativeBlocker(iWarrior, 2, 100, 15)

		# American natives
		if utils.isYearIn(1600, 1700):
			print "trying to spawn nomad natives"
			self.checkSpawn(iNative2, iArcher, 1 + iHandicap, (85, 14), (121, 49), self.spawnNomads, iGameTurn, 5, 0)
			self.checkSpawn(iNative2, iWarrior, 1 + iHandicap, (85, 14), (121, 49), self.spawnNomads, iGameTurn, 5, 2)

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

		self.foundNativeVillages(iGameTurn)
		if iGameTurn < getTurnForYear(tMinorCities[len(tMinorCities)-1][0])+10:
			self.foundMinorCities(iGameTurn)

	def changeNativeAttitudeForPlayer(self, iPlayer, iValue):
		data.players[iPlayer].iNativeAttitude = max(iValue+data.players[iPlayer].iNativeAttitude,
													self.getMinNativeAttitudeForPlayer(iPlayer))

	def getNumNativeSpawnsFromAttitude(self, iPlayer):
		iValue = data.getTotalNativeAttitude(iPlayer)
		if iValue > 0:
			return 0
		elif iValue > -3:
			return 1
		elif iValue > -7:
			return 2
		return 3

	def adjustNativeAttitudeForGameTurn(self, iGameTurn, iPlayer):
		if iGameTurn % 10 == 5:
			iMaxValue = self.getMaxNativeAttitudeForPlayer(iPlayer)
			# FoB - don't adjust attitude if over limit from events
			if data.players[iPlayer].iNativeAttitude >= iMaxValue:
				return;
			data.players[iPlayer].iNativeAttitude = min(data.players[iPlayer].iNativeAttitude+1, iMaxValue)
			print("FOB Native attutide adjusted to: " + str(data.players[iPlayer].iNativeAttitude))

	def getMinNativeAttitudeForPlayer(self, iPlayer):
		return -10;

	def getMaxNativeAttitudeForPlayer(self, iPlayer):
		if gc.getTeam(iPlayer).isHasTech(iManifestDestiny):
			return 5;
		return 0;

	# FoB - Villages not guarenteed to spawn, but should be good enough
	def foundNativeVillages(self, iGameTurn):
		for i in range(len(tNativeVillages)):
			iYear, tPlot, iPlayer = tNativeVillages[i]
			if iGameTurn == getTurnForYear(iYear):
				x, y = tPlot
				plot = gc.getMap().plot(x, y)
				if plot.isCity(): continue
				if not self.isFreePlot(tPlot, False): continue
				gc.getMap().plot(x,y).setImprovementType(iNativeVillage)


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
			
	def possibleTiles(self, tTL, tBR, bWater=False, bTerritory=False, bBorder=False, bImpassable=False, bNearCity=False, bNextToCity=False):
		return [tPlot for tPlot in utils.getPlotList(tTL, tBR) if self.possibleTile(tPlot, bWater, bTerritory, bBorder, bImpassable, bNearCity, bNextToCity)]
		
	def possibleTile(self, tPlot, bWater, bTerritory, bBorder, bImpassable, bNearCity, bNextToCity=False):
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		lSurrounding = utils.surroundingPlots(tPlot)
		
		# never on peaks
		if plot.isPeak(): return False
		
		# only land or water
		if bWater != plot.isWater(): return False
		
		# only inside territory if specified
		if not bTerritory and plot.getOwner() >= 0: return False
		
		# directly next to cities
		if not bNextToCity and [(i, j) for (i, j) in lSurrounding if gc.getMap().plot(i, j).isCity()]: return False
		
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

	#TODO - redo to provide greater unit variation based on era and location
	def trySpawnNativePartisans(self, iX, iY, iPlayer=None):
		plot = (iX,iY)
		if not self.possibleTile(plot, bWater=False, bTerritory=True, bBorder=True, bImpassable=False, bNearCity=True, bNextToCity=True):
			lPlots = self.possibleTiles((iX-1,iY-1), (iX+1,iY+1), bWater=False, bTerritory=True, bBorder=True, bImpassable=False, bNearCity=True, bNextToCity=True)
			plot = utils.getRandomEntry(lPlots)
		if plot == None: return
		iNumUnits = iNativePillagePartisans
		if iPlayer:
			iNumUnits = self.getNumNativeSpawnsFromAttitude(iPlayer)
		utils.makeUnitAI(iWarrior, iNative, plot, UnitAITypes.UNITAI_ATTACK, iNumUnits, "Hostile")
		utils.setUnitsHaveMoved(iNative, (plot[0], plot[1]))

	def trySpawnNativeBlocker(self, iUnitType, iNumUnits, iX, iY):
		plot = gc.getMap().plot(iX, iY)
		if not plot.isOwned():
			utils.makeUnitAI(iUnitType, iNative2, (iX,iY), UnitAITypes.UNITAI_DEFENSE, iNumUnits)

	def spawnPowhatanWarriorsI(self, iNumUnits):
		iHandicap = gc.getHandicapInfo(gc.getGame().getHandicapType()).getBarbarianSpawnModifier()
		#self.spawnNativesTerritory(iNative, iWarrior, iNumUnits + iHandicap, tEastVATL, tEastVABR)
		utils.makeUnitAI(iWarrior, iNative, (131,40), UnitAITypes.UNITAI_ATTACK, iNumUnits + iHandicap, "Powhatan")