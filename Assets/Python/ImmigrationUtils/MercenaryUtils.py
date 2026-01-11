#
# Mercenaries Mod
# By: The Lopez
# Modified by MacAurther
# Mercenary
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

##########################
# Mercenary Class		
# By: The Lopez
# Modified by MacAurther
# This class provides the structure needed to represent mercenaries in the game.

class Mercenary:
	def __init__(self, iUnitID, sUnitName="", lPromotionList=None, iExperienceLevel=0, iNextExperienceLevel=0):
		self.iUnitID = iUnitID

		if sUnitName != "":
			self.sUnitName = sUnitName
		else:
			self.sUnitName = str(self.getUnitInfo().getDescription())

		# Populate Promotion List
		if lPromotionList is None:
			self.lPromotionList = []
		else:
			# make a copy so callers can't share references
			self.lPromotionList = list(lPromotionList)
		
		# Add unit type's free promotions
		for iPromo in range(gc.getNumPromotionInfos()):
			if self.getUnitInfo().getFreePromotions(iPromo):
				self.lPromotionList.append(iPromo)

		# Add Mercenary promotion
		if self.isMercenaryType():
			self.lPromotionList.append(gc.getInfoTypeForString("PROMOTION_MERCENARY"))

		
		self.iLevel = len(self.lPromotionList)
		self.iExperienceLevel = iExperienceLevel
		self.iNextExperienceLevel = iNextExperienceLevel		

	def place(self, iPlayer, iHomeland):
		player = gc.getPlayer(iPlayer)
		civics = Civics.player(iPlayer)

		pPlot = self.getMercenaryStartingLocation(iPlayer, iHomeland)

		if pPlot is None:
			return

		# Create the unit and place it in the game		
		objUnit = player.initUnit(self.iUnitID, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		# Use up all of the mercenaries moves
		objUnit.finishMoves()

		# Inform the player that the mercenary has arrived.
		strMessage = self.getName() + " has arrived"
		CyInterface().addMessage(iPlayer, False, 20, strMessage, "", 0, self.getUnitInfo().getButton(), ColorTypes(0), pPlot.getX(), pPlot.getY(), True, True) 

		# Set the mercenaries experience
		self.setExperience(objUnit)

		# Set the mercenaries unique name
		objUnit.setName(self.sUnitName)

		iExp = 0
		# Conquest and Zealotry Civic
		if self.getUnitInfo().getDomainType() == DomainTypes.DOMAIN_LAND and not self.getUnitInfo().getUnitCombatType() in [UnitCombatTypes.NO_UNITCOMBAT, UnitCombatTypes.UNITCOMBAT_SPY]:
			if iConquest in civics or iImperialism in civics:
				iExp += 2
			if iPatronato in civics:
				iExp += 2
		
		# Admiralty Civic
		if iAdmiralty in civics and self.getUnitInfo().getDomainType() == DomainTypes.DOMAIN_SEA:
			iExp += 4
		
		if iExp > 0:
			objUnit.changeExperience(iExp, -1, False, False, False)
		
		# Apply of the promotions to the mercenary in the game
		self.applyPromotions(objUnit)
	
	def isMercenaryType(self):
		return self.iUnitID in dMercenarySchedule.keys()

	# Returns the list of current promotions the mercenary has.	
	def getCurrentPromotionList(self):
		return self.lPromotionList

	# Returns true if the available funds are enough to hire
	def canAfford(self, iPlayer, iHomeland):
		# get the player instance
		player = gc.getPlayer(iPlayer)
		
		(iImmigrationCost, iGoldCost) = self.getHireCost(iPlayer)

		bCanAffordImmigrants = iImmigrationCost == 0
		if str(iImmigrant) in data.civs[civ(iPlayer)].dEarnedImmigrants[iHomeland].keys():
			bCanAffordImmigrants = iImmigrationCost <= data.civs[civ(iPlayer)].dEarnedImmigrants[iHomeland][str(iImmigrant)].getCount()
		
		return iGoldCost <= player.getGold() and bCanAffordImmigrants
	
	def getUnitId(self):
		return self.iUnitID

	# Returns the cost to hire the mercenary. Returns (iCostImmigration, iCostGold)
	def getHireCost(self, iPlayer):
		' iHireCost - the cost to hire the mercenary'
		
		if iPlayer == -1:
			bProprietaries = False
			bAdmiralty = False
			bIndenturedServitude = False
		else:
			# Get the actual current player object
			civics = Civics.player(iPlayer)
			bProprietaries = iProprietors in civics
			bAdmiralty = iAdmiralty in civics
			bIndenturedServitude = iIndenturedServitude in civics
		
		iImmigrationCost = 0
		iGoldCost = 0
		
		# Set Immigration costs
		if self.iUnitID in [iSettler, iDogSled]:
			iImmigrationCost = 4
		elif self.iUnitID == iPioneer:
			iImmigrationCost = 6
		elif self.iUnitID in [iWorker, iPromyshlenniki]:
			iImmigrationCost = 2
		elif self.iUnitID == iLaborer:
			iImmigrationCost = 3
		elif self.iUnitID == iTrackman:
			iImmigrationCost = 1
		elif self.iUnitID in [iOrthodoxMiss, iCatholicMiss, iProtestantMiss]:
			iImmigrationCost = 1
			iGoldCost = scale(10)
		else:
			iGoldCost = self.getUnitInfo().getProductionCost() / 2

		# Apply effects
		if bIndenturedServitude and self.iUnitID in [iWorker, iPromyshlenniki, iLaborer]: iImmigrationCost -= 1
		if civ(iPlayer) == iNorse and self.iUnitID == iSettler: iImmigrationCost -= 1	# Norse UP
		if bProprietaries and self.getUnitInfo().getUnitCombatType() != UnitCombatTypes.NO_UNITCOMBAT and self.getUnitInfo().getDomainType() == DomainTypes.DOMAIN_LAND:
			iGoldCost /= 2
		if bAdmiralty and self.getUnitInfo().getDomainType() == DomainTypes.DOMAIN_SEA:
			iGoldCost /= 2
		
		return (iImmigrationCost, iGoldCost)
			
	
	def getHireCostString(self, iPlayer):
		(iImmigrationCost, iGoldCost) = self.getHireCost(iPlayer)
		strHCost = ""
		if iImmigrationCost > 0:
			strHCost += u"%d%c" %(iImmigrationCost, CyTranslator().getText("[ICON_IMMIGRANT]", ()))
		if iGoldCost > 0:
			strHCost += u"%d%c" %(iGoldCost, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
		return strHCost

	# Returns the mercenary's current experience level
	def getExperienceLevel(self):
		return self.iExperienceLevel
		

	# Returns the mercenary's next experience level.
	def getNextExperienceLevel(self):
		return self.iNextExperienceLevel		
		
		
	# Returns the mercenary's current level.
	def getLevel(self):
		return self.iLevel
	

	# Applies the promotions from the lPromotionList to the mercenary represent by objUnit 
	def applyPromotions(self, objUnit):

		# Return immediately if the self.objUnit is not set.
		if(objUnit == None):
			return
					
		for i in range(len(self.lPromotionList)):
			objUnit.setHasPromotion(self.lPromotionList[i], True)
	
	
	# This method will set the initial the mercenary experience and level
	def setExperience(self, objUnit):

		# Return immediately if the self.objUnit is not set.
		if(objUnit == None):
			return

		objUnit.setLevel(self.iLevel)

		objUnit.setExperience(self.iExperienceLevel,self.iExperienceLevel)	


	# Returns the mercenary's name		
	def getName(self):
		return self.sUnitName


	# Sets the name for the mercenary
	def setName(self, sUnitName):

		# Return immediately if the name passed in is not set	
		if(sUnitName == None):
			return

		# Return immediately if the name passed in has a length of 0
		if(len(sUnitName) == 0):
			return
			
		self.sUnitName = sUnitName
		
	# Returns the mercenary's UnitInfo object		
	def getUnitInfo(self):
		return gc.getUnitInfo(self.iUnitID)

	def getMercenaryStartingLocation(self, iPlayer, iHomeland):
		pPlot = None
		if self.isShip():
			pPlot = self.getShipPlacementPlot(iPlayer, iHomeland)
		else:
			if self.hasValidSpawnTile(iPlayer, iHomeland):
				pPlot = self.getPlacementShip(iPlayer, iHomeland).plot()
		return pPlot
	
	# In order to place hired unit, the player must have a ship on the edge of the map
	def hasShipForPlacement(self, iPlayer, iHomeland):
		if self.getPlacementShip(iPlayer, iHomeland) != None:
			return True
		return False
	
	# Check to see if the mercenary has a spot to go
	def hasValidSpawnTile(self, iPlayer, iHomeland):
		if self.isShip():
			return self.getShipPlacementPlot(iPlayer, iHomeland) is not None
		elif self.getUnitInfo().getDomainType() == DomainTypes.DOMAIN_LAND:
			if self.hasShipForPlacement(iPlayer, iHomeland):
				return True
		return False

	# Get the ship in which to place a hired land unit
	def getPlacementShip(self, iPlayer, iHomeland):
		lUnits = PlayerUtil.getPlayerUnits(iPlayer)
		for pUnit in lUnits:
			if pUnit.plot().getFeatureType() - iTradeWindsStart == iHomeland:
				if not pUnit.isFull():
					return pUnit
		return None
	
	# Get the tile where hire mercenary ships appear
	def getShipPlacementPlot(self, iPlayer, iHomeland):
		iCiv = civ(iPlayer)
		
		for x in range(iWorldX):
			pLoopPlot = plot(x, dCapitals[iCiv][1])
			if pLoopPlot.getFeatureType() - iTradeWindsStart == iHomeland:
				return pLoopPlot

		# If no plots were found that matched the given homeland at the latitude of the player's capital, return default
		return plot(dHomelandDefaultUnitSpawn[iHomeland])
	
	# Is Ship?
	def isShip(self):
		return self.getUnitInfo().getDomainType() == 0		# DOMAIN_SEA = 0
	
class ImmigrantGroup:
	def __init__(self, immigrant, iCount=1):
		self.immigrant = immigrant
		self.iCount = iCount
	
	def getImmigrant(self):
		return self.immigrant
	
	def getUnitId(self):
		return self.immigrant.getUnitId()
	
	def getCount(self):
		return self.iCount
	
	# Return False if the count changed to 0 or below
	def changeCount(self, iAmount = 1):
		self.iCount += iAmount
		if self.iCount <= 0:
			self.iCount = 0
			return False
		return True
	
	def getImmigrantTitle(self):
		if self.getCount() > 1:
			return self.immigrant.sUnitName + " (" + str(self.getCount()) + ")"
		else:
			return self.immigrant.sUnitName