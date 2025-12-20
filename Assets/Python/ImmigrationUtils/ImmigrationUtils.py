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
g_bDebug = False

class ImmigrationUtils:

	# The constructor for the ImmigrationUtils class. First we check to see if the 
	# data has been setup using pickle. Then we try to read in the configuration 
	# information from the INI config file.
	def __init__(self):
		self.firsttime = True
		
	
	def getImmigrationThreshold(self, iPlayer, iHomeland):
		iCiv = civ(iPlayer)
		return int(self.calculateBaseImmigrationThreshold(iPlayer) * self.getHomelandImmigrationThresholdModifier(iPlayer, iHomeland))

	def getHomelandImmigrationThresholdModifier(self, iPlayer, iHomeland):
		iModifier = 0
		
		# Civics
		if iPlayer == -1:
			bPenalColony = False
			bDecolonization = False
		else:
			# Get the actual current player object
			civics = Civics.player(iPlayer)
			bPenalColony = iPenalColony in civics
			bDecolonization = iDecolonization in civics
		if bPenalColony: iModifier -= 50
		if bDecolonization: iModifier += 25

		# England UP:
		if civ(iPlayer) == iEngland and iHomeland == iHomelandNorthEurope:
			iModifier -= 50

		# Saturation
		iModifier += data.civs[civ(iPlayer)].lNumImmigrantsEared[iHomeland] ** 1.1

		return max(100 + iModifier, 20) / 100

	def calculateBaseImmigrationThreshold(self, iPlayer):
		return 10 + (data.civs[civ(iPlayer)].numImmigrations ** 1.1)

	def canEarnImmigrants(self, iPlayer, iHomeland=-1):
		pPlayer = player(iPlayer)
		if iHomeland == -1:
			return any(gc.getTeam(pPlayer.getTeam()).isHasTech(iTech) for iTech in lImmigraitonTechs)
		return gc.getTeam(pPlayer.getTeam()).isHasTech(lImmigraitonTechs[iHomeland])
	
	def getFirstOpenHomeland(self, iPlayer):
		for iHomeland in lHomelands:
			if self.canEarnImmigrants(iPlayer, iHomeland):
				return iHomeland

	def processImmigration(self, iPlayer):
		iCiv = civ(iPlayer)
		pPlayer = player(iPlayer)
		bImmigrantGranted = True
		while bImmigrantGranted:
			bImmigrantGranted = False
			for iHomeland in lHomelands:
				if not self.canEarnImmigrants(iPlayer, iHomeland):
					continue
				if pPlayer.getImmigration() < self.getImmigrationThreshold(iCiv, iHomeland):
					continue
				# Grant Immigrant
				self.changeImmigrants(iPlayer, iHomeland, iImmigrant, 1)
				bImmigrantGranted = True
				# Subtract cost
				pPlayer.changeImmigration(-1*self.getImmigrationThreshold(iCiv, iHomeland))
				# Increment num immigrant trackers
				data.civs[iCiv].numImmigrations += 1
				data.civs[iCiv].lNumImmigrantsEared[iHomeland] += 1
				# Notify player (if human)
				if pPlayer.isHuman():
					# MacAurther TODO: This is very messy. Maybe improve if you feel like it
					strHomeland = ""
					if iHomeland == iHomelandNorthEurope:
						strHomeland = "North Europe"
					elif iHomeland == iHomelandSouthEurope:
						strHomeland = "South Europe"
					elif iHomeland == iHomelandAfrica:
						strHomeland = "Africa"
					elif iHomeland == iHomelandSiberia:
						strHomeland = "Siberia"
					elif iHomeland == iHomelandAsia:
						strHomeland = "Asia"

					# Inform the player that the immigrant has arrived.
					strMessage = "A new Immigrant is waiting on the docks of " + strHomeland + "!"
					CyInterface().addMessage(iPlayer, False, 20, strMessage, "AS2D_IMMIGRANTEARNED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, "", gc.getInfoTypeForString("COLOR_YELLOW"), -1, -1, False, False) 

	def changeImmigrants(self, iPlayer, iHomeland, iUnit, iChange):
		iCiv = civ(iPlayer)
		if str(iUnit) in data.civs[iCiv].dEarnedImmigrants[iHomeland].keys():
			# If immigrant group already exists, do nothing
			pass
		elif iChange > 0:
			# If immigrant group doesn't exist and will be added to, create group and decrement change (because creating starts it at 1)
			data.civs[iCiv].dEarnedImmigrants[iHomeland][str(iUnit)] = self.getImmigrantGroup(iUnit)
			iChange -= 1
		else:
			# If the immigrant group doesn't exist and the change is negative, return
			return
		
		# If the change made the change count function return false, delete entry
		if not data.civs[iCiv].dEarnedImmigrants[iHomeland][str(iUnit)].changeCount(iChange):
			print("Deleting earned immigrant entry for: " + data.civs[iCiv].dEarnedImmigrants[iHomeland][str(iUnit)].getImmigrant().sUnitName)
			del data.civs[iCiv].dEarnedImmigrants[iHomeland][str(iUnit)]
	
	def getNumImmigrants(self, iCiv, iHomeland, iUnit=iImmigrant):
		data.civs[iCiv].dEarnedImmigrants[iHomeland][str(iUnit)].getCount()

	def getAvailableUnit(self, iHomeland, dSchedule):
		dUnits = {}

		for iUnit in dSchedule.keys():
			if not iHomeland in dSchedule[iUnit][1]:
				continue
			if not turn() in range(year(dSchedule[iUnit][0][0]), year(dSchedule[iUnit][0][1]) + 1):
				continue
			dUnits[str(iUnit)] = self.getImmigrantGroup(iUnit)
			
		return dUnits
			
	# Returns a list of available immigrants given a homeland and date
	def getAvailableImmigrants(self, iHomeland):
		return self.getAvailableUnit(iHomeland, dImmigrantSchedule)
	
	# Returns a list of available mercenaries given a homeland and date
	def getAvailableMercenaries(self, iHomeland):
		return self.getAvailableUnit(iHomeland, dMercenarySchedule)

	def getEarnedImmigrants(self, iCiv, iHomeland):
		return data.civs[iCiv].dEarnedImmigrants[iHomeland]
	
	def getHasEarnedImmigrant(self, iCiv, iHomeland, iUnit):
		if not str(iUnit) in self.getEarnedImmigrants(iCiv, iHomeland).keys():
			return False
		return self.getEarnedImmigrants(iCiv, iHomeland)[str(iUnit)].getCount() > 0

	def getImmigrantGroup(self, iUnit, iCount=1):
		# return if that unit name can't be found
		if iUnit == -1 or iCount < 1:
			return None
		
		immigrantGroup = ImmigrantGroup(self.getImmigrant(iUnit), iCount)

		return immigrantGroup

	def getImmigrant(self, iUnit):
		# return if that unit name can't be found
		if iUnit == -1:
			return None
		
		objMercenary = Mercenary(iUnit)

		return objMercenary
	
	# This method acts as a proxy to the hire method in the Mercenary class. It will
	# get the mercenary object in the global mercenary pool
	def hireMercenary(self, iUnit, iPlayer, iHomeland, bPay=True):
		' returns true if the objMercenary was successfully hired'
		
		# Get the player
		pPlayer = gc.getPlayer(iPlayer)
		
		# Return immediately if the player specified in iPlayer is not alive
		if(not pPlayer.isAlive()):
			return False
			
		immigrant = self.getImmigrant(iUnit)
		
		# Return immediately if the immigrant was not retrieved from the global
		# immigrant pool
		if(immigrant == None):
			return False
		
		# Return immediately if player can't afford immigrant
		(iImmigrationCost, iGoldCost) = immigrant.getHireCost(iPlayer)
		if iGoldCost > pPlayer.getGold() and iImmigrationCost > pPlayer.getImmigration():
			return False
	
		# Get the starting location for the immigrant
		pPlot = None
		if immigrant.isShip():
			pPlot = immigrant.getMercenaryStartingLocation(iPlayer, iHomeland)
		
			# Return immediately if no suitable plot to spawn
			if pPlot == None:
				return False
        
		# Subtract cost to hire from player current cash
		if bPay:
			(iImmigrantCost, iGoldCost) = immigrant.getHireCost(iPlayer)
			self.changeImmigrants(iPlayer, iHomeland, iImmigrant, -iImmigrantCost)
			pPlayer.setGold(pPlayer.getGold() - iGoldCost)
		
		# Place immediately if ship, otherwise add to earned Immigrants
		if immigrant.isShip():
			self.placeMercenary(iUnit, iPlayer, iHomeland)
		else:
			# If not placed, add to earned immigrants list
			self.changeImmigrants(iPlayer, iHomeland, iUnit, 1)


		print(pPlayer.getName() + " | Current Gold: " + str(pPlayer.getGold()) + " | Current Immigration: " + str(pPlayer.getImmigration()) + " | Hired " + immigrant.getName() + " for " + str(iImmigrationCost) + " immigration and " + str(iGoldCost) + " gold.")
		
		return True

	def placeMercenary(self, iUnit, iPlayer, iHomeland):
		# Get the player
		pPlayer = gc.getPlayer(iPlayer)
		
		# Return immediately if the player specified in iPlayer is not alive
		if(not pPlayer.isAlive()):
			return False
		
		immigrant = self.getImmigrant(iUnit)

		# Reduce earned immigrants by 1 if not a ship
		if not immigrant.isShip():
			self.changeImmigrants(iPlayer, iHomeland, iUnit, -1)

		immigrant.place(iPlayer, iHomeland)

	
	# Returns the most desired mercenary that is less expensive than the iGold/iImmigration values passed in.		
	def getBestAvailableImmigrant(self, iImmigration, iGold, iPlayer, lCategoryDesire):
		
		pBestImmigrant = None
		iHighestDesire = 0
		iHighestDesireCategory = -1
		
		for iImmigrantCategory in range(iNumImmigrantCategories):
			iDesire = lCategoryDesire[iImmigrantCategory]
			if iDesire > iHighestDesire:
				iUnit = self.getAvailableImmigrantFromCategory(iPlayer, lPossibleImmigrants[iImmigrantCategory])
				
				# Check to see if there are no available immigrants in that category (i.e. doesn't have the tech or such)
				if iUnit == -1:
					continue
				
				# Check to see if immigrant can be hired
				pImmigrant = self.getImmigrant(iUnit)
				
				if (not pImmigrant.canHireUnit(iPlayer)):
					continue
				
				# Calculate how much gold the AI will have after hiring the immigrant.
				(iImmigrationCost, iGoldCost) = pImmigrant.getHireCost(iPlayer)
				tmpImmigration = iImmigration - iImmigrationCost
				tmpGold = iGold - iGoldCost
				
				# Continue immediately if the AI can't buy the immigrant
				if(tmpImmigration < 0 or tmpGold <= 0):
					continue
				
				# MacAurther TODO: Evaluate this rule
				# Continue immediately if the AI will have to spend gold to buy this immigrant
				if iGoldCost > 0:
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
	# MacAurther TODO: It needs to be more complex but for right now it works
	def computerPlayerThink(self, iPlayer):
		return
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
			
			if g_bDebug:
				CvUtil.pyPrint(pPlayer.getName() + " has the following desires: " + str(lCategoryDesire))
			
			# Get the best available immigrant
			immigrant, lCategoryDesire = self.getBestAvailableImmigrant(pPlayer.getImmigration(), pPlayer.getGold(), iPlayer, lCategoryDesire)

			# Return immediately if a immigrant wasn't returned
			if immigrant == None:
				return
			
			if g_bDebug:
				CvUtil.pyPrint(pPlayer.getName() + " thinking about iUnit: " + str(immigrant.getUnitInfo().getType()))

			# Have the computer hire the immigrant			
			if not self.hireMercenary(immigrant.getUnitId(), iPlayer):
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
		
		# Slave Category
		if iGuilds in civics or iSlavery in civics or iBondage in civics:
			# Get excess happiness in cities that can have slaves
			iExcessHappiness = 0
			for pCity in lCities:
				if pCity.canSlaveJoin():
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
		if iApprenticeship in civics or iImmigrantLabor in civics:
			lCategoryDesire[iTrackmanCat] = 3 - lNumUnitsInCategories[iTrackmanCat]	# Max at 3 at any given time
		
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
		
		# Skirmish Ship Category - On second thought, don't let the AI hire endless privateers...
		#if lCategoryDesire[iMainlineShipCat] < 1:
		#	lCategoryDesire[iSkirmishShipCat] = 2 - lNumUnitsInCategories[iSkirmishShipCat]	# Want up to 2 if own fleet is already built out (don't privateer spam!)
		
		# Capital Ship Category
		lCategoryDesire[iCapitalShipCat] = min(iNumCities / 3, 3) - lNumUnitsInCategories[iCapitalShipCat]	# Want 1/3 unit per city, up to 3
		
		# Don't consider GPs until you're near your city goal
		if dNumCitiesGoal[iCiv] - iNumCities <= 1:
			# Great People Category
			if iCiv in [iAmerica, iCanada]:
				if turn() < year(1800): lCategoryDesire[iGPCatProphet] = 3
				lCategoryDesire[iGPCatArtist] = 5 - (player(iPlayer).getCommerceRate(CommerceTypes.COMMERCE_CULTURE) / 40)
				lCategoryDesire[iGPCatScientist] = 5 - (player(iPlayer).getCommerceRate(CommerceTypes.COMMERCE_RESEARCH) / 20)
				lCategoryDesire[iGPCatMerchant] = 5 - (player(iPlayer).getCommerceRate(CommerceTypes.COMMERCE_GOLD) / 20)
				if turn() >= year(1800): lCategoryDesire[iGPCatEngineer] = 3
				lCategoryDesire[iGPCatStatesman] = -stability(iPlayer)
				lCategoryDesire[iGPCatGeneral] = team(iPlayer).getAtWarCount(True)
		
		return lCategoryDesire
	
	def getUnitCategory(self, iUnit):
		for iUnitCategory, lUnitCategory in enumerate(lPossibleImmigrants):
			if iUnit in lUnitCategory:
				return iUnitCategory
		return -1