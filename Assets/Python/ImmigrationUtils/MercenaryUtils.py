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
	
	# Returns True if unit was place, False if not
	def hire(self, iPlayer, pPlot):
		player = gc.getPlayer(iPlayer)
		iCiv = civ(iPlayer)
		
		# return nothing if the iPlayer is an invalid value
		if(player == None):
			return
			
		# return nothing if the player is dead
		if(player.isAlive() == False):
			return
		
		# Increase cost of future Immigrants from this category
		data.civs[iCiv].lUnitCategoriesHired[self.getUnitCategory()] += 1

		if pPlot is not None:	# Place unit if it can be placed (i.e. ships)
			self.place(iPlayer, pPlot)
			return True
		else:
			return False		
		

	def place(self, iPlayer, pPlot):
		player = gc.getPlayer(iPlayer)
		civics = Civics.player(iPlayer)

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
		if self.getUnitId() in lPossibleMercenariesLand:
			if iConquest1 in civics or iConquest2 in civics:
				iExp += 2
			if iZealotry2 in civics:
				iExp += 2
		
		# Admiralty Civic
		if iAdmiralty2 in civics and self.getUnitId() in lTransports + lPossibleMercenariesSea:
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
		
		# if iPlayer == -1:
		# 	iCurrentImmigration = 0
		# 	bDecolonization = False
		# 	bIntervention = False
		# 	bProprietaries = False
		# 	bIndenturedServitude = False
		# 	bPenalColony = False
		# 	bEuropeanRP = False
		# else:
		# 	# Get the actual current player object
		# 	player = gc.getPlayer(iPlayer)
		# 	civics = Civics.player(iPlayer)
		# 	iCurrentImmigration = player.getImmigration()
		# 	bDecolonization = iDecolonization3 in civics
		# 	bIntervention = iIntervention2 in civics
		# 	bProprietaries = iProprietaries2 in civics
		# 	bIndenturedServitude = iIndenturedServitude2 in civics
		# 	bPenalColony = iPenalColony2 in civics
		# 	bEuropeanRP = civ(iPlayer) in dCivGroups[iCivGroupEurope]
		
		iImmigrationCost = 0
		iGoldCost = 0
		
		# Set Immigration costs
		if self.iUnitID in [iSettler, iDogSled]:
			iImmigrationCost = 6
		elif self.iUnitID == iPioneer:
			iImmigrationCost = 10
		elif self.iUnitID in [iWorker, iPromyshlenniki]:
			iImmigrationCost = 3
		elif self.iUnitID == iLaborer:
			iImmigrationCost = 4
		elif self.iUnitID == iTrackman:
			iImmigrationCost = 2
		elif self.iUnitID in [iOrthodoxMiss, iCatholicMiss, iProtestantMiss]:
			iImmigrationCost = 1
			iGoldCost = 20 * int(3 - gc.getGame().getGameSpeedType())
		elif self.getUnitId() in lGreatPeople:
			iImmigrationCost = 1
			iGoldCost = 500 * int(3 - gc.getGame().getGameSpeedType())
		else:
			iGoldCost = self.getUnitInfo().getProductionCost() / 2
			# Double price if unique unit
			if gc.getUnitClassInfo(self.getUnitInfo().getUnitClassType()).getDefaultUnitIndex() != self.iUnitID:
				iGoldCost *= 2

		
		return (iImmigrationCost, iGoldCost)
			
	
	def getHireCostString(self, iPlayer):
		(iImmigrationCost, iGoldCost) = self.getHireCost(iPlayer)
		strHCost = ""
		if iImmigrationCost > 0:
			strHCost += u"%d%c" %(iImmigrationCost, CyTranslator().getText("[ICON_ANGRYPOP]", ()))	# MacAurther TODO: Better icon?
		if iGoldCost > 0:
			strHCost += u"%d%c" %(iGoldCost, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
		return strHCost

	def canHireUnit(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		
		# Anglo-America RP: Can hire Great People
		if civ(iPlayer) in [iAmerica, iCanada]:
			if self.getUnitId() in lGreatPeople:
				return True
		
		# Can hire Colonists and other special units even though you can't train them
		if self.getUnitId() in [iImmigrant]:
			return True
		
		if pPlayer.canTrain(self.getUnitId(), False, False):
			return True
		
		return False

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
		return pPlot
	
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
	
	# Get the tile where hire mercenary ships appear
	def getShipPlacementPlot(self, iPlayer, iHomeland):
		iCiv = civ(iPlayer)

		x = dHomelandArea[iHomeland][0][0][0]
		y = dHomelandArea[iHomeland][0][0][1]

		lHomelandYs = []
		for segment in dHomelandArea[iHomeland]:
			lHomelandYs += range(segment[0][1], segment[1][1])
		for hly in lHomelandYs:
			if abs(dCapitals[iCiv][1] - hly) < abs(dCapitals[iCiv][1] - y):
				y = hly

		return gc.getMap().plot(x, y)
	
	# Is Ship?
	def isShip(self):
		return self.getUnitInfo().getDomainType() == 0		# DOMAIN_SEA = 0
	
	def getUnitCategory(self):
		for iUnitCategory, lUnitCategory in enumerate(lPossibleImmigrants):
			if self.getUnitId() in lUnitCategory:
				return iUnitCategory
		return -1
	
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