#
# Mercenaries Mod
# By: The Lopez
# Modified by MacAurther
# ImmigrationUtils
# 

from CvPythonExtensions import *

import CvUtil

import CvEventManager
import sys
import PyHelpers
import CvMainInterface
import math

import pickle

from RFCUtils import *
from Consts import *
from StoredData import data
from Core import *
from Civics import *
import PlayerUtil
from MercenaryUtils import *

################# SD-UTILITY-PACK ###################
import SdToolKit
sdEcho         = SdToolKit.sdEcho
sdModInit      = SdToolKit.sdModInit
sdModLoad      = SdToolKit.sdModLoad
sdModSave      = SdToolKit.sdModSave
sdEntityInit   = SdToolKit.sdEntityInit
sdEntityExists = SdToolKit.sdEntityExists
sdGetVal       = SdToolKit.sdGetVal
sdSetVal       = SdToolKit.sdSetVal


# globals
###################################################
gc = CyGlobalContext()	

PyPlayer = PyHelpers.PyPlayer
PyGame = PyHelpers.PyGame()
PyInfo = PyHelpers.PyInfo

AVAILABLE_COLONISTS = "AvailableColonists"
AVAILABLE_EXPEDITIONARIES = "AvailableExpeditionaries"

# Set to true to print out debug messages in the logs
g_bDebug = false

class ImmigrationUtils:

	# The constructor for the ImmigrationUtils class. First we check to see if the 
	# data has been setup using pickle. Then we try to read in the configuration 
	# information from the INI config file.
	def __init__(self):
		self.firsttime = true
		
		# Setup the mercenary data structure if it hasn't been setup yet.
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()
			
	# This method will setup the appropriate datastructures using the SD-Toolkit to maintain
	# the mercenary data.
	def setupMercenaryData(self):
	
		# The dictionary of available mercenaries. The keys will be the name of the mercenary
		# the value will be dictionary representations of Mercenary objects.
		availableMercenaries = {}
		
		# The dictionary of hired mercenaries. The keys will be the player ID and the values
		# will be the dictionaries containing the mercenaries.
		hiredMercenaries = {}
		
		playerList = PyGame.getCivPlayerList()
		
		for player in playerList:
			hiredMercenaries[player.getID()] = {}
		
		# Lets enable the barbarian
		hiredMercenaries[gc.getBARBARIAN_PLAYER()] = {}
		
		# The dictionary of unplaced mercenaries. The keys will be the name of the mercenary
		# the value will be dictionary representations of Mercenary Objects
		unplacedMercenaries = {}
					
		# The dictionary of mercenary groups. The keys will be the name of the mercenary group
		# the value will be MercenaryGroup objects.
		mercenaryGroups = {}
		
		# The dictionary of used mercenary names.
		mercenaryNames = {}
		
		mercenaryData = {
							AVAILABLE_COLONISTS : availableMercenaries,
							AVAILABLE_EXPEDITIONARIES : hiredMercenaries}
							
		sdEntityInit("Mercenaries Mod", "MercenaryData", mercenaryData)
			
	# Returns a dict of the most technologically advanced unit of a each category available for hire.
	def getAvailableImmigrants(self, iPlayer, lUnitCategories):
		' mercenariesDict - the dictionary containing the mercenaries that are available for hire by players '

		mercenariesDict = {}

		for lUnitCategory in lUnitCategories:
			mercenariesDict.update(self.getAvailableMercenaryDict(iPlayer, lUnitCategory))
			
		return mercenariesDict
	
	# Returns dictionary of best unit in category
	def getAvailableMercenaryDict(self, iPlayer, lUnitCategory):
		mercenariesDict = {}
		iUnit = self.getAvailableImmigrantFromCategory(iPlayer, lUnitCategory)
		if iUnit != -1:
			mercenariesDict = self.addAvailableUnitToDict(iUnit, mercenariesDict)
		return mercenariesDict
	
	# Returns best unit in category
	def getAvailableImmigrantFromCategory(self, iPlayer, lUnitCategory):
		pPlayer = gc.getPlayer(iPlayer)
		
		for iUnit in reversed(lUnitCategory):
			if self.isImmigrantValid(iPlayer, iUnit) and (pPlayer.canTrain(iUnit, false, false) or iUnit in lNoTrainingNeeded):
				return iUnit
		return -1
	
	def isImmigrantValid(self, iPlayer, iUnit):
		iCiv = civ(iPlayer)
		pPlayer = gc.getPlayer(iPlayer)
		
		# Special Cases
		# Get Missionary Type available
		if iUnit in [iOrthodoxMiss, iCatholicMiss, iProtestantMiss]:
			if iUnit == iOrthodoxMiss and pPlayer.getStateReligion() == iOrthodoxy and not gc.getGame().isUnitClassMaxedOut(gc.getUnitInfo(iOrthodoxMiss).getUnitClassType(), 0):
				return True
			elif iUnit == iCatholicMiss and pPlayer.getStateReligion() == iCatholicism and not gc.getGame().isUnitClassMaxedOut(gc.getUnitInfo(iCatholicMiss).getUnitClassType(), 0):
				return True
			elif iUnit == iProtestantMiss and pPlayer.getStateReligion() == iProtestantism and not gc.getGame().isUnitClassMaxedOut(gc.getUnitInfo(iProtestantMiss).getUnitClassType(), 0):
				return True
			return False
		
		# Colonist and base endowments are always available
		if iUnit in [iColonist] + lEndowmentsBase:
			return True
		
		# Get Great Person available (Anglo-America RP)
		if iUnit in lGreatPeople:
			if iCiv in [iAmerica, iCanada]:
				return True
			return False
		
		civics = Civics.player(iPlayer)
		
		# Slaves
		if iUnit in lAfricanSlaves:
			# Get Slave available
			if iSlavery2 in civics:
				return True
			elif iSlavery3 in civics:
				return True
			return False
		if iUnit in lNativeSlaves:
			return False
			
		# Get Migrant Worker available
		if iUnit in lMigrantWorkers:
			if iImmigrantLabor2 in civics or iImmigrantLabor3 in civics:
				return True
			return False
		
		# Default
		iUnitClass = gc.getUnitInfo(iUnit).getUnitClassType();
		if gc.getCivilizationInfo(iCiv).getCivilizationUnits(iUnitClass) == iUnit:
			return True
		
		return False
	
	def addAvailableUnitToDict(self, iUnit, unitDict):
		
		newImmigrant = self.getImmigrant(iUnit)
		
		# Add the immigrant into the unitDict
		unitDict[newImmigrant.getName()] = newImmigrant
		
		return unitDict

	
	# Gets a new Mercenary Object based off of the given ID
	def getImmigrant(self, iMercenary):
		' objMercenary - the instance of the Mercenary class that represents the mercenary '
		
		# return if that unit name can't be found
		if iMercenary == -1:
			return None
		
		pMercenary = gc.getUnitInfo(iMercenary)
		objMercenary = Mercenary(pMercenary.getDescription(), pMercenary, [], 0, 1)

		return objMercenary
		

	# Creates and returns a blank instance of the Mercenary class
	def createBlankMercenary(self):
		return Mercenary("",None,[],-1,-1)
	
	# This method acts as a proxy to the hire method in the Mercenary class. It will
	# get the mercenary object in the global mercenary pool
	def hireMercenary(self, iMercenary, iPlayer):
		' returns true if the objMercenary was successfully hired'
		
		# Get the player
		pPlayer = gc.getPlayer(iPlayer)
		
		# Return immediately if the player specified in iPlayer is not alive
		if(not pPlayer.isAlive()):
			return False
			
		# Get the immigrant from the global immigrant pool
		immigrant = self.getImmigrant(iMercenary)
		
		# Return immediately if the immigrant was not retrieved from the global
		# immigrant pool
		if(immigrant == None):
			return False
		
		# Return immediately if player can't afford immigrant
		(iImmigrationCost, iGoldCost) = immigrant.getHireCost(iPlayer)
		if iGoldCost > pPlayer.getGold():	# Only need to check gold because Immigration maxes out on available immigration
			return False
		
		# Return immediately if there's nowhere to spawn immigrant
		if not immigrant.hasValidSpawnTile(iPlayer):
			if g_bDebug:
				CvUtil.pyPrint("No place to spawn Immigrant")
			return False
	
		# Get the starting location for the immigrant
		pPlot = self.getMercenaryStartingLocation(iPlayer, immigrant)
		
		# Return immediately if no suitable plot to spawn
		if pPlot == None:
			return False
                
		immigrant.hire(iPlayer, pPlot)

		print(pPlayer.getName() + " | Current Gold: " + str(pPlayer.getGold()) + " | Current Immigration: " + str(pPlayer.getImmigration()) + " | Hired " + immigrant.getName() + " for " + str(iImmigrationCost) + " immigration and " + str(iGoldCost) + " gold.")
		
		return True

	
	# Returns the starting city for a player's mercenary
	def getMercenaryStartingLocation(self, iPlayer, mercenary):
		' CyPlot - the starting plot for hired mercenaries'
		player = gc.getPlayer(iPlayer)
		
		pPlot = mercenary.getMercenaryStartingLocation(iPlayer)
		
		return pPlot
	
	# Returns the most desired mercenary that is less expensive than the iGold/iImmigration values passed in.		
	def getBestAvailableImmigrant(self, iImmigration, iGold, iPlayer, lCategoryDesire):
		
		hireCost = 0
		
		pBestImmigrant = None
		iHighestDesire = 0
		iHighestDesireCategory = -1
		
		for iImmigrantCategory in range(iNumImmigrantCategories):
			iDesire = lCategoryDesire[iImmigrantCategory]
			if iDesire > iHighestDesire:
				iImmigrant = self.getAvailableImmigrantFromCategory(iPlayer, lPossibleImmigrants[iImmigrantCategory])
				
				# Check to see if there are no available immigrants in that category (i.e. doesn't have the tech or such)
				if iImmigrant == -1:
					continue
				
				# Check to see if immigrant can be hired
				pImmigrant = self.getImmigrant(iImmigrant)
				
				if (not pImmigrant.canHireUnit(iPlayer)):
					continue
				
				# Calculate how much gold the player will have after hiring the immigrant.
				(immigrationCost, goldCost) = pImmigrant.getHireCost(iPlayer)
				tmpImmigration = iImmigration - immigrationCost
				tmpGold = iGold - goldCost
				
				# Continue immediately if the player can't buy the immigrant
				if(tmpImmigration < 0 or tmpGold <= 0):
					continue
				
				if g_bDebug:
					CvUtil.pyPrint("Player: " + str(iPlayer) + " desires " + str(iDesire) + " " + pImmigrant.getName())
				
				if iDesire > iHighestDesire:
					iHighestDesire = iDesire 
					pBestImmigrant = pImmigrant
					iHighestDesireCategory = iImmigrantCategory
					if g_bDebug:
						CvUtil.pyPrint("Potential immigrant for " + gc.getPlayer(iPlayer).getName() + " is " + immigrant.getName())
		
		if(g_bDebug and pBestImmigrant != None):
			CvUtil.pyPrint("Best immigrant for " + gc.getPlayer(iPlayer).getName() + " is " + pBestImmigrant.getName())
		
		if pBestImmigrant:
			# Decrement recommended category so we can just reuse the modified lCategoryDesire list instead of having to recalculate
			lCategoryDesire[iHighestDesireCategory] -= 1
		
		return pBestImmigrant, lCategoryDesire
		
	
	# Performs the thinking for the computer players in regards to the mercenaries mod functionality.
	# It will:
	#   - Hire mercenaries	
	# MacAurther: TODO: It needs to be more complex but for right now it works
	def computerPlayerThink(self, iPlayer):
            
		# Get the player
		pPlayer = gc.getPlayer(iPlayer)
		
		# Return immediately if the player is a filthy human :p
		if(pPlayer.isHuman()):
			return

		# Return immediately if the player is a barbarian, independent, or native
		if(pPlayer.isBarbarian() or pPlayer.isIndependent() or pPlayer.isNative()):
			return
		
		# Don't do anything if you don't have a lot of immigration
		if pPlayer.getImmigration() <= 50:
			return

		immigrant = None
		
		# Get the player's current number of units
		lNumUnitsInCategories = self.getNumUnitsInCategories(iPlayer)
		
		# Check to see if AI needs mainline ship (they have none)
		if lNumUnitsInCategories[iMainlineShipCat] == 0:
			iMainlineShip = self.getAvailableImmigrantFromCategory(iPlayer, lMainlineShips)
			
			if iMainlineShip != UnitTypes.NO_UNIT:
				print(pPlayer.getName() + " has no mainline ships! Attempting to hire eUnitType " + str(iMainlineShip))
				# Try to hire that merc (might fail)
				self.hireMercenary(iMainlineShip, iPlayer)
			
		# Check to see if AI needs transport ship (they have none)
		if lNumUnitsInCategories[iTransportsCat] == 0:
			iTransportShip = self.getAvailableImmigrantFromCategory(iPlayer, lTransports)
			
			if iTransportShip != UnitTypes.NO_UNIT:
				print(pPlayer.getName() + " has no transport ships! Attempting to hire eUnitType " + str(iTransportShip))
				# Try to hire that merc (might fail)
				self.hireMercenary(iTransportShip, iPlayer)
		
		# Check to see if there's anywhere to spawn land Immigrants. If not, just pass for now so we don't spend a ton of time thinking about not buying anything. Eventually, either an Immigrant ship will come by, or we'll have no transport ships so the above code will force buy one
		# This also has the side effect of buying ships in batches, strengthening the fleet and creating "waves" of immigrants. Cool
		if not self.hasShipForPlacement(iPlayer):
			return
		
		# Pre-calculate the AI's desire for each Immigrant. Do this ONCE per computer player think call
		lCategoryDesire = self.getAIDesiredCategory(iPlayer, lNumUnitsInCategories)
		
		# Keep track of number of failed hires
		iNumFailedHires = 0
		
		# Hire Immigrants until we get below 50 Immigration, but don't go below -5 GPT, and don't go below 50 Gold
		while pPlayer.getImmigration() > 50 and pPlayer.getGoldPerTurn() > -5 and pPlayer.getGold() > 50:

			# Get the best available immigrant
			immigrant, lCategoryDesire = self.getBestAvailableImmigrant(pPlayer.getImmigration(), pPlayer.getGold(), iPlayer, lCategoryDesire)

			# Return immediately if a immigrant wasn't returned
			if immigrant == None:
				return
			
			if g_bDebug:
				CvUtil.pyPrint("Player: " + str(iPlayer) + " thinking about iImmigrant: " + str(immigrant.objUnitInfo.getType()))

			# Have the computer hire the immigrant			
			if not self.hireMercenary(immigrant.getUnitInfoID(), iPlayer):
				iNumFailedHires += 1	# increment the failure count if immigrant wasn't hired
			
			# Return if there's no space for land units and no ships will be hired
			if not self.hasShipForPlacement(iPlayer) and (lCategoryDesire[iTransportsCat] + lCategoryDesire[iMainlineShipCat] + lCategoryDesire[iSkirmishShipCat] + lCategoryDesire[iCapitalShipCat] < 1):
				return
			
			# Return if several hires have failed (saves looping through remaining desired units that can't be hired)
			if iNumFailedHires > 5:
				return
	
	def getNumUnitsInCategories(self, iPlayer):
		lNumUnitsInCategories = [0] * iNumImmigrantCategories
		
		lUnits = PlayerUtil.getPlayerUnits(iPlayer)
		for pUnit in lUnits:
			iUnitCategory = self.getUnitCategory(pUnit.getUnitType())
			if iUnitCategory > -1:
				lNumUnitsInCategories[iUnitCategory] += 1
		
		return lNumUnitsInCategories
	
	def getAIDesiredCategory(self, iPlayer, lNumUnitsInCategories):
		'''Returns the immigrant unit category that the AI wants most'''
		pPlayer = gc.getPlayer(iPlayer)
		iCiv = civ(iPlayer)
		civics = Civics.player(iPlayer)
		
		# Setup list
		lCategoryDesire = [0] * iNumImmigrantCategories
		
		lCities = PlayerUtil.getPlayerCities(iPlayer)
		iNumCities = len(lCities)
		
		# Settlers Category
		# TODO: Find a more robust way to do this?
		lCategoryDesire[iSettlersCat] = min(dNumCitiesGoal[iCiv] - iNumCities, 2) - lNumUnitsInCategories[iSettlersCat]	# Get specific AI's desire to build cities, but don't go crazy on Settlers, max at 3 at a time
		
		# Workers Category
		lCategoryDesire[iWorkersCat] = min(iNumCities, 5) - lNumUnitsInCategories[iWorkersCat]	# Ballpark want 1 worker per city, max 5
		
		# Missionaries Category
		if pPlayer.getStateReligion() > -1:
			iNumConvertedCities = 0
			for pCity in cities.owner(iPlayer):
				if pCity.isHasReligion(pPlayer.getStateReligion()):
					iNumConvertedCities += 1
			lCategoryDesire[iMissionariesCat] = min(iNumCities - iNumConvertedCities, 3) - lNumUnitsInCategories[iMissionariesCat]	# Max 3
		
		# Transports Category
		lCategoryDesire[iTransportsCat] = min(iNumCities / 2, 5) - lNumUnitsInCategories[iTransportsCat]	# Want 1 Transport per 2 cities, max 5
		
		# Choose randomly between Great People and Migrant Workers
		# TODO: Find better heuristic
		# Great People Category
		if iCiv in [iAmerica, iCanada]:
			lCategoryDesire[iGreatPeopleCat] = gc.getGame().getSorenRandNum(100, 'random') / 100.0
		
		# Slave Category
		if iSlavery1 in civics or iSlavery2 in civics or iSlavery3 in civics:
			# Get excess happiness in cities that can have slaves
			iExcessHappiness = 0
			for pCity in lCities:
				if pCity.canSlaveJoin(iSpecialistSlavePlanter):	# only really want to spend immigration on slaves to be planeters
					iExcessHappiness += max(pCity.happyLevel() - pCity.unhappyLevel(0), 0)	# Truncate to be non-negative per city
		
			lCategoryDesire[iSlavesCat] = min(iExcessHappiness, 3) - lNumUnitsInCategories[iSlavesCat]	# Max at 3 at any given time
		
		# Colonist Category
		# Get excess happiness in cities that have extra food
		iExcessHappiness = 0
		if lCategoryDesire[iSettlersCat] < 1:	# only think about getting colonists when you have all the settlers you want
			for pCity in lCities:
				if pCity.foodDifference(True) > 2:
					iExcessHappiness += max(pCity.happyLevel() - pCity.unhappyLevel(0), 0)	# Truncate to be non-negative per city
			
		lCategoryDesire[iColonistsCat] = min(iExcessHappiness, 2) - lNumUnitsInCategories[iColonistsCat]	# Max at 2 at any given time
		
		# Migrant Worker Category
		# TODO: Find better heuristic
		if iImmigrantLabor2 in civics or iImmigrantLabor3 in civics:
			lCategoryDesire[iMigrantWorkerCat] = min(gc.getGame().getSorenRandNum(100, 'random') / 100.0, 3 - lNumUnitsInCategories[iMigrantWorkerCat])	# Max at 3 at any given time
		
		# Explorers Category
		if iCiv in [iSpain, iPortugal, iEngland, iFrance, iNetherlands, iRussia]:
			lCategoryDesire[iExplorersCat] = 2 - lNumUnitsInCategories[iExplorersCat]	# Want 2 explorers max

		# Miltia Category
		lCategoryDesire[iMilitiaCat] = min(iNumCities, 10) - lNumUnitsInCategories[iMilitiaCat]	# Want 1 Militia per city, up to 10
		
		# Mainline Category
		lCategoryDesire[iMainlineCat] = min(iNumCities, 10) - lNumUnitsInCategories[iMainlineCat]	# Want 1 Mainline infantry per city, up to 10
		
		# Elite Category
		lCategoryDesire[iEliteCat] = min(iNumCities / 3, 3) - lNumUnitsInCategories[iEliteCat]	# Want 1/3 unit per city, up to 3
		
		# Collateral Category
		lCategoryDesire[iCollateralCat] = min(iNumCities / 3, 3) - lNumUnitsInCategories[iCollateralCat]	# Want 1/3 unit per city, up to 3
		
		# Skirmish Category
		lCategoryDesire[iSkirmishCat] = min(iNumCities / 3, 3) - lNumUnitsInCategories[iSkirmishCat]	# Want 1/3 unit per city, up to 3
		
		# Cav Category
		lCategoryDesire[iCavCat] = min(iNumCities / 3, 5) - lNumUnitsInCategories[iCavCat]	# Want 1/3 unit per city, up to 5
		
		# Siege Category
		lCategoryDesire[iSiegeCat] = min(iNumCities / 3, 5) - lNumUnitsInCategories[iSiegeCat]	# Want 1/3 unit per city, up to 5
		
		# Mainline Ship Category
		lCategoryDesire[iMainlineShipCat] = min(iNumCities / 3, 5) - lNumUnitsInCategories[iMainlineShipCat]	# Want 1/3 unit per city, up to 5
		
		# Capital Ship Category
		lCategoryDesire[iCapitalShipCat] = min(iNumCities / 3, 3) - lNumUnitsInCategories[iCapitalShipCat]	# Want 1/3 unit per city, up to 3
		
		# Skirmish Ship Category - On second thought, don't let the AI hire endless privateers...
		#if lCategoryDesire[iMainlineShipCat] < 1:
		#	lCategoryDesire[iSkirmishShipCat] = 2 - lNumUnitsInCategories[iSkirmishShipCat]	# Want up to 2 if own fleet is already built out (don't privateer spam!)
		
		return lCategoryDesire
	
	def getUnitCategory(self, iUnit):
		for iUnitCategory, lUnitCategory in enumerate(lPossibleImmigrants):
			if iUnit in lUnitCategory:
				return iUnitCategory
		return -1
	
	# In order to place hired unit, the player must have a ship on the edge of the map
	def hasShipForPlacement(self, iPlayer):
		if self.getPlacementShip(iPlayer) != None:
			return True
		return False
	
	# Get the ship in which to place a hired land unit
	def getPlacementShip(self, iPlayer):
		lUnits = PlayerUtil.getPlayerUnits(iPlayer)
		for pUnit in lUnits:
			iX = pUnit.getX();
			if iX == 0 or iX == iWorldX - 1:
				if not pUnit.isFull():
					return pUnit
		return None