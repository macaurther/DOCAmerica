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
		return int(self.calculateBaseImmigrationThreshold(iPlayer, iHomeland) * self.getHomelandImmigrationThresholdModifier(iPlayer, iHomeland))

	def getHomelandImmigrationThresholdModifier(self, iPlayer, iHomeland):
		iModifier = 0
		
		# Civics
		if iPlayer == -1:
			bPenalColony = False
		else:
			# Get the actual current player object
			civics = Civics.player(iPlayer)
			bPenalColony = iPenalColony in civics
		if bPenalColony: iModifier -= 50

		# England UP:
		if civ(iPlayer) == iEngland and iHomeland == iHomelandNorthEurope:
			iModifier -= 50
		
		return max(100 + iModifier, 20) / 100.0

	def calculateBaseImmigrationThreshold(self, iPlayer, iHomeland):
		iThreshold = 10
		iThreshold += data.civs[civ(iPlayer)].numImmigrations
		iThreshold += 2 * data.civs[civ(iPlayer)].lNumImmigrantsEared[iHomeland]
		return iThreshold

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
		iBestHomeland = 0
		while iBestHomeland != -1:
			iBestHomeland = -1
			for iHomeland in lHomelands:
				if not self.canEarnImmigrants(iPlayer, iHomeland):
					continue
				if pPlayer.getImmigration() < self.getImmigrationThreshold(iPlayer, iHomeland):
					continue
				if iBestHomeland == -1:
					iBestHomeland = iHomeland
				elif self.getImmigrationThreshold(iPlayer, iBestHomeland) > self.getImmigrationThreshold(iPlayer, iHomeland):
					iBestHomeland = iHomeland
					
			if iBestHomeland != -1:
				# Grant Immigrant
				self.changeImmigrants(iPlayer, iBestHomeland, iImmigrant, 1)
				# Subtract cost
				pPlayer.changeImmigration(-1*self.getImmigrationThreshold(iPlayer, iBestHomeland))
				# Increment num immigrant trackers
				data.civs[iCiv].numImmigrations += 1
				data.civs[iCiv].lNumImmigrantsEared[iBestHomeland] += 1
				# Notify player (if human)
				if pPlayer.isHuman():
					strHomeland = ""
					if iBestHomeland == iHomelandNorthEurope:
						strHomeland = "North Europe"
					elif iBestHomeland == iHomelandSouthEurope:
						strHomeland = "South Europe"
					elif iBestHomeland == iHomelandAfrica:
						strHomeland = "Africa"
					elif iBestHomeland == iHomelandSiberia:
						strHomeland = "Siberia"
					elif iBestHomeland == iHomelandAsia:
						strHomeland = "Asia"

					# Inform the player that the immigrant has arrived.
					strMessage = "A new Immigrant is waiting on the docks of " + strHomeland + "!"
					CyInterface().addMessage(iPlayer, False, 20, strMessage, "AS2D_IMMIGRANTEARNED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, "", gc.getInfoTypeForString("COLOR_YELLOW"), -1, -1, False, False) 

	def changeImmigrants(self, iPlayer, iHomeland, iUnit, iChange):
		iCiv = civ(iPlayer)
		if str(iUnit) in data.civs[iCiv].dEarnedUnits[iHomeland].keys():
			# If immigrant group already exists, do nothing
			pass
		elif iChange > 0:
			# If immigrant group doesn't exist and will be added to, create group and decrement change (because creating starts it at 1)
			data.civs[iCiv].dEarnedUnits[iHomeland][str(iUnit)] = self.getImmigrantGroup(iUnit)
			iChange -= 1
		else:
			# If the immigrant group doesn't exist and the change is negative, return
			return
		
		# If the change made the change count function return false, delete entry
		if not data.civs[iCiv].dEarnedUnits[iHomeland][str(iUnit)].changeCount(iChange):
			print("Deleting earned immigrant entry for: " + data.civs[iCiv].dEarnedUnits[iHomeland][str(iUnit)].getImmigrant().sUnitName)
			del data.civs[iCiv].dEarnedUnits[iHomeland][str(iUnit)]
	
	def getTotalNumImmigrants(self, iPlayer, iHomeland):
		iNumImmigrants = 0
		iCiv = civ(iPlayer)
		for sUnit in data.civs[iCiv].dEarnedUnits[iHomeland].keys():
			iNumImmigrants += data.civs[iCiv].dEarnedUnits[iHomeland][sUnit].getCount()
		return iNumImmigrants
	
	def getNumImmigrants(self, iPlayer, iHomeland, iUnit):
		if str(iUnit) in data.civs[civ(iPlayer)].dEarnedUnits[iHomeland].keys():
			return data.civs[civ(iPlayer)].dEarnedUnits[iHomeland][str(iUnit)].getCount()
		return 0

	def getAvailableUnit(self, iPlayer, iHomeland, dSchedule):
		dUnits = {}

		for iUnit in dSchedule.keys():
			if not iHomeland in dSchedule[iUnit][1]:
				continue
			if not turn() in range(year(dSchedule[iUnit][0][0]), year(dSchedule[iUnit][0][1]) + 1):
				continue
			if not self.canHire(iUnit, iPlayer, iHomeland):
				continue
			if unique_unit(iPlayer, iUnit) != iUnit and not iUnit in lUniqueOverride:
				continue
			dUnits[str(iUnit)] = self.getImmigrantGroup(iUnit)
			
		return dUnits
	
	# Extra check for special can hire cases
	def canHire(self, iUnit, iPlayer, iHomeland):
		civics = Civics.player(iPlayer)
		if iUnit == iChattleSlave and not (iBondage in civics or iSlavery in civics):
			return False
		return True

	# Returns a list of available immigrants given a homeland and date
	def getAvailableImmigrants(self, iPlayer, iHomeland):
		return self.getAvailableUnit(iPlayer, iHomeland, dImmigrantSchedule)
	
	# Returns a list of available mercenaries given a homeland and date
	def getAvailableMercenaries(self, iPlayer, iHomeland):
		return self.getAvailableUnit(iPlayer, iHomeland, dMercenarySchedule)

	def getEarnedImmigrants(self, iCiv, iHomeland):
		return data.civs[iCiv].dEarnedUnits[iHomeland]
	
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
	def hireMercenary(self, iUnit, iPlayer, iHomeland, bPay=True, bImmediate=False):
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
		if bPay and not immigrant.canAfford(iPlayer, iHomeland):
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
		
		# Place immediately if ship or force immediate with space, otherwise add to earned Immigrants
		if immigrant.isShip() or (bImmediate and immigrant.hasShipForPlacement(iPlayer, iHomeland)):
			self.placeMercenary(iUnit, iPlayer, iHomeland, bImmediate)
		else:
			# If not placed, add to earned immigrants list
			self.changeImmigrants(iPlayer, iHomeland, iUnit, 1)

		if g_bDebug:
			print(pPlayer.getName() + " | Current Gold: " + str(pPlayer.getGold()) + " | Current Immigrants: " + str(self.getNumImmigrants(iPlayer, iHomeland, iImmigrant)) + " | Hired " + immigrant.getName() + " for " + str(iImmigrationCost) + " immigration and " + str(iGoldCost) + " gold.")
		
		return True

	def placeMercenary(self, iUnit, iPlayer, iHomeland, bImmediate=False):
		# Get the player
		pPlayer = gc.getPlayer(iPlayer)
		
		# Return immediately if the player specified in iPlayer is not alive
		if(not pPlayer.isAlive()):
			return False
		
		immigrant = self.getImmigrant(iUnit)

		# Reduce earned units by 1 if not a ship and not immediate
		if not immigrant.isShip() and not bImmediate:
			self.changeImmigrants(iPlayer, iHomeland, iUnit, -1)
		
		# If unit is Mercenary and placed while AI owner is at war with another player, make it aggressive
		bAggressive = not pPlayer.isHuman() and team(iPlayer).getAtWarCount(True)

		immigrant.place(iPlayer, iHomeland, bAggressive)

	# Performs the thinking for the computer players in regards to the mercenaries mod functionality.
	# It will:
	# 	- Load earned units on waiting ships
	#   - Exchange Immigrants for Settlers, Workers, etc.
	# It will not:
	#	- Hire additional military units
	def computerPlayerThink(self, iPlayer):
		# Get the player
		pPlayer = gc.getPlayer(iPlayer)
		
		# Return immediately if the player is a filthy human :p
		if pPlayer.isHuman():
			return

		# Return immediately if the player is a barbarian, independent, or native
		if pPlayer.isBarbarian() or pPlayer.isIndependent() or pPlayer.isNative():
			return

		# Return immediately if the player cannot earn immigrants
		if not self.canEarnImmigrants(iPlayer):
			return
		
		# Convert earned Immigrants into other units
		for iHomeland in lHomelands:
			self.computerPlayerHireImmigrants(iPlayer, iHomeland)
			if iHomeland == iHomelandAfrica:
				self.computerPlayerHireSlaves(iPlayer)

		
		# Load waiting units
		for iHomeland in lHomelands:
			self.computerPlayerLoadHomeland(iPlayer, iHomeland)

		if g_bDebug:
			print(pPlayer.getName() + " has the following earned immigrants:")
			for iHomeland in lHomelands:
				if self.getTotalNumImmigrants(iPlayer, iHomeland) > 0:
					print("Homeland: " + str(iHomeland))
					for sUnit in data.civs[civ(iPlayer)].dEarnedUnits[iHomeland].keys():
						if self.getNumImmigrants(iPlayer, iHomeland, int(sUnit)) > 0:
							print(data.civs[civ(iPlayer)].dEarnedUnits[iHomeland][sUnit].getImmigrantTitle())

	def computerPlayerHireImmigrants(self, iPlayer, iHomeland):
		# Priority: Settlers, Workers, then Missionaries
		# Try to hire, if didn't work, just continue on
		if self.computerPlayerWantsSettlers(iPlayer):
			self.hireMercenary(unique_unit(iPlayer, iSettler), iPlayer, iHomeland, bPay=True)
		if self.computerPlayerWantsWorkers(iPlayer):
			self.hireMercenary(unique_unit(iPlayer, iWorker), iPlayer, iHomeland, bPay=True)
		if self.computerPlayerWantsMissionaries(iPlayer):
			self.hireMercenary(unique_unit(iPlayer, missionary(player(iPlayer).getStateReligion())), iPlayer, iHomeland, bPay=True)
	
	def computerPlayerHireSlaves(self, iPlayer):
		if self.computerPlayerWantsSlaves(iPlayer):
			self.hireMercenary(unique_unit(iPlayer, iChattleSlave), iPlayer, iHomelandAfrica, bPay=True)

	def computerPlayerLoadHomeland(self, iPlayer, iHomeland):
		for sUnit in data.civs[civ(iPlayer)].dEarnedUnits[iHomeland].keys():
			# Heuristic: Don't load any Immigrants unless you don't want any more settlers, workers, or missionaries
			if str(iImmigrant) == sUnit and not self.computerPlayerWantsImmigrants(iPlayer):
				continue
			iNumUnits = self.getNumImmigrants(iPlayer, iHomeland, int(sUnit))
			if iNumUnits > 0:
				for _ in range(iNumUnits):
					if data.civs[civ(iPlayer)].dEarnedUnits[iHomeland][sUnit].getImmigrant().hasShipForPlacement(iPlayer, iHomeland):
						self.placeMercenary(int(sUnit), iPlayer, iHomeland)
					else:
						return

	def computerPlayerWantsImmigrants(self, iPlayer):
		return (not self.computerPlayerWantsSettlers(iPlayer)) and \
			   (not self.computerPlayerWantsMissionaries(iPlayer)) and \
			   (not self.computerPlayerWantsWorkers(iPlayer))	# Evaluate workers last since it'll probably take the longest and there's a chance to escape earlier

	def computerPlayerWantsSettlers(self, iPlayer):
		# Wants no more than 1 settler
		for unit in units.owner(iPlayer):
			if unit.isFound():
				return False
		return True

	def computerPlayerWantsWorkers(self, iPlayer):
		# Wants no more than 1 worker per city
		iNumWorkers = 0
		for unit in units.owner(iPlayer):
			if base_unit(unit) in [iWorker, iLaborer]:
				iNumWorkers += 1
		return iNumWorkers < player(iPlayer).getNumCities()

	def computerPlayerWantsMissionaries(self, iPlayer):
		# Doesn't want if no State religion
		if player(iPlayer).getStateReligion() == -1:
			return False
		# Wants no more than 1 missionary
		for unit in units.owner(iPlayer):
			if gc.getUnitInfo(unit.getUnitType()).getReligionSpreads(player(iPlayer).getStateReligion()) > 0:
				return False
		return True
	
	def computerPlayerWantsSlaves(self, iPlayer):
		# Doesn't want if can't buy
		if not player(iPlayer).canBuySlaves():
			return False
		# Use baked in method
		if player(iPlayer).countRequiredSlaves() > 0:
			return True
		return False
	
	def computerGetNumImmigrantsToTransport(self, iPlayer, iHomeland):
		bWantsImmigrants = self.computerPlayerWantsImmigrants(iPlayer)
		iNumUnitsToTransport = 0
		for sUnit in data.civs[civ(iPlayer)].dEarnedUnits[iHomeland].keys():
			if bWantsImmigrants or (not "Immigrant" in sUnit):
				iNumUnitsToTransport += 1
		return iNumUnitsToTransport
