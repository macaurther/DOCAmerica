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
	
	def getNumImmigrants(self, iPlayer, iHomeland):
		iNumImmigrants = 0
		iCiv = civ(iPlayer)
		for sUnit in data.civs[iCiv].dEarnedImmigrants[iHomeland].keys():
			iNumImmigrants += data.civs[iCiv].dEarnedImmigrants[iHomeland][sUnit].getCount()
		return iNumImmigrants

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

	# Performs the thinking for the computer players in regards to the mercenaries mod functionality.
	# It will:
	# 	- Load earned immigrants on waiting ships
	# It will not:
	#	- Hire additional military units (MacAurther TODO: Add this?)
	#	- Exchange immigrants for Settlers, Workers, etc. (MacAurther TODO: Add this?)
	def computerPlayerThink(self, iPlayer):
		# Get the player
		pPlayer = gc.getPlayer(iPlayer)
		iCiv = civ(iPlayer)
		
		# Return immediately if the player is a filthy human :p
		if(pPlayer.isHuman()):
			return

		# Return immediately if the player is a barbarian, independent, or native
		if(pPlayer.isBarbarian() or pPlayer.isIndependent() or pPlayer.isNative()):
			return
		
		for iHomeland in lHomelands:
			# Load waiting Immigrants with no prejudice (MacAurther TODO: Load most important units first?)
			for sImmigrant in data.civs[iCiv].dEarnedImmigrants[iHomeland].keys():
				iNumImmigrants = data.civs[iCiv].dEarnedImmigrants[iHomeland][sImmigrant].getCount()
				if iNumImmigrants > 0:
					for _ in range(iNumImmigrants):
						if data.civs[iCiv].dEarnedImmigrants[iHomeland][sImmigrant].getImmigrant().hasShipForPlacement(iPlayer, iHomeland):
							self.placeMercenary(int(sImmigrant), iPlayer, iHomeland)
						else:
							break