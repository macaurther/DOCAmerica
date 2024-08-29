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
# This class provides the structure needed to represent mercenaries in the game.

class Mercenary:
	# The name of the mercenary
	strMercenaryName = ""

	# The list of promotions
	promotionList = []
	
	# The cost to hire the mercenary
	iHireCost = -1
	
	# The reference to the mercenary group that the mercenary belongs to
	objMercenaryGroup = None
	
	# The boolean variable indicating if the mercenary is hired by a player or not
	bHired = false
	
	# The reference to the CyUnit object representing the mercenary in the game when hired
	# by a player
	objUnit = None
	
	# The Reference to the CvUnitInfo object representing the mercenary info 
	objUnitInfo = None
	
	# The ID for the CvUnitInfo
	iUnitInfo = -1
	
	# The ID for the player that hired the mercenary
	iOwner = -1

	# The ID for the player that originally built the unit
	iBuilder = -1
	
	# The current experience for the mercenary
	iExperienceLevel = -1
	
	# The amount of experience needed for the next level
	iNextExperienceLevel = -1
	
	# The current level for the mercenary
	iLevel = -1
	
	# The turn the unit was/should be placed in the game
	iPlacementTurn = -1
	
			
	def __init__(self, mercenaryName, objUnitInfo, promotionList, iExperienceLevel, iNextExperienceLevel):
		self.strMercenaryName = mercenaryName
		self.promotionList = promotionList
		
		self.objUnitInfo = objUnitInfo
		if(self.objUnitInfo != None):
			self.iUnitInfo = gc.getInfoTypeForString(self.objUnitInfo.getType())
			
		self.iLevel = len(promotionList)
		self.iExperienceLevel = iExperienceLevel
		self.iNextExperienceLevel = iNextExperienceLevel
		self.iHireCost = self.getHireCost(-1)


	# This method should be used for setting the instance of the Mercenary class
	# with the data from a CyUnit
	def loadUnitData(self, objUnit):

		# Return immediately if the objUnit is not valid
		if(objUnit == None):
			return
	
		self.objUnit = objUnit
	
		self.getCurrentPromotionList()	

		self.getExperienceLevel()

		self.getNextExperienceLevel()

		self.getLevel()

		self.getHireCost(-1)

		self.getOwner()

		self.getUnitInfo()
	
		if(self.iBuilder == -1):
			self.iBuilder = objUnit.getOwner()
		
		if(len(objUnit.getNameNoDesc())>0):
			self.strMercenaryName = objUnit.getNameNoDesc()
		
	
	# This method should be used for setting the instance of the Mercenary class 
	# with the data retrieved using the Sd-Toolkit
	def loadData(self, objDict):
		self.strMercenaryName = objDict["strMercenaryName"]
		
		self.promotionList = []
		
		# Retrieve all of the actual PromotionInfo objects
		
		promotionList = objDict["promotionList"]
		promotionList.sort()
		
		for i in range(len(promotionList)):
			self.promotionList.append(gc.getPromotionInfo(objDict["promotionList"][i]))
			
		self.iHireCost = objDict["iHireCost"]
		
		self.iOwner = objDict["iOwner"]

		# if the owner is set for the mercenary then set the hired flag and get the reference to the
		# unit that represents the mercenary in the game.
		if(self.iOwner != -1):
			self.bHired = true
			
		if(objDict["iUnitID"] != -1):
			self.objUnit = gc.getPlayer(self.iOwner).getUnit(objDict["iUnitID"])
		else:	
			self.objUnit = None

		self.objUnitInfo = gc.getUnitInfo(objDict["iUnitInfo"])

		self.iUnitInfo = objDict["iUnitInfo"]

		self.iExperienceLevel = objDict["iExperienceLevel"]

		self.iNextExperienceLevel = objDict["iNextExperienceLevel"]

		self.iLevel = objDict["iLevel"]
		
		self.iBuilder = objDict["iBuilder"]
	
		self.iPlacementTurn = objDict["iPlacementTurn"]	

		#TO DO: add mercenary group support

		
	# This method builds a dictionary that is used to represent the mercenary in the global mercenary pool.		
	def getDictionaryRepresentation(self):
	
		objDict = {}
		objDict["strMercenaryName"] = self.strMercenaryName

		tmpPromotionList = []
		
		# Add all of the promotions into the tmpPromotionList using their promotion type ID number
		for i in range (len(self.promotionList)):
			if(gc.getInfoTypeForString(self.promotionList[i].getType()) not in tmpPromotionList):
				tmpPromotionList.append(gc.getInfoTypeForString(self.promotionList[i].getType()))
	
		objDict["promotionList"] = tmpPromotionList
				
		objDict["iHireCost"] = self.iHireCost

		objDict["bHired"] = self.bHired

		objDict["iOwner"] = self.iOwner

		if(self.iOwner != -1 and self.objUnit != None):
			objDict["iUnitID"] = self.objUnit.getID()
		else:	
			objDict["iUnitID"] = -1

		objDict["iUnitInfo"] = gc.getInfoTypeForString(self.objUnitInfo.getType())
		
		objDict["iExperienceLevel"] = self.iExperienceLevel

		objDict["iNextExperienceLevel"] = self.iNextExperienceLevel
		
		objDict["iLevel"] = self.iLevel

		objDict["iBuilder"] = self.iBuilder

		objDict["iPlacementTurn"] = self.iPlacementTurn
		
		return objDict
					

	# Returns the instance of the mercenary in the game as a CyUnit
	def hire(self, iPlayer, pPlot):
		' CyUnit - the instance of the mercenary in the game '

		# get the player instance
		player = gc.getPlayer(iPlayer)
		iCiv = civ(iPlayer)
		civics = Civics.player(iPlayer)
		
		# return nothing if the iPlayer is an invalid value
		if(player == None):
			return
			
		# return nothing if the player is dead
		if(player.isAlive() == false):
			return

		# Set the player as the owner of the mercenary.	
		self.iOwner = iPlayer
		
		# Set the mercenary as hired
		self.bHired = true
		
		unitType = gc.getInfoTypeForString(self.objUnitInfo.getType())

		# Create the unit and place it in the game		
		self.objUnit = player.initUnit(unitType, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		# Use up all of the mercenaries moves
		self.objUnit.finishMoves()

		# Inform the player that the mercenary has arrived.
		strMessage = self.getName() + " has arrived"
		CyInterface().addMessage(self.iOwner, False, 20, strMessage, "", 0, self.objUnitInfo.getButton(), ColorTypes(0), pPlot.getX(), pPlot.getY(), True, True) 

		# Set the mercenaries experience
		self.setExperience()

		# Set the mercenaries unique name
		self.objUnit.setName(self.strMercenaryName)

		self.iPlacementTurn = -1
	
		# Subtract cost to hire from player current cash
		(iImmigrationCost, iGoldCost) = self.getHireCost(iPlayer)
		player.setImmigration(player.getImmigration() - iImmigrationCost)
		player.setGold(player.getGold() - iGoldCost)
		
		# Increase cost of future Immigrants from this category
		data.civs[iCiv].lUnitCategoriesHired[self.getUnitCategory()] += 1
		
		if iGoldCost > 0:
			self.promotionList.append(gc.getPromotionInfo(gc.getInfoTypeForString("PROMOTION_MERCENARY")))
		
		iExp = 0
		# Conquest and Zealotry Civic
		if self.getUnitInfoID() in lPossibleExpeditionariesLand:
			if iConquest1 in civics or iConquest2 in civics:
				iExp += 2
			if iZealotry2 in civics:
				iExp += 2
		
		# Admiralty Civic
		if iAdmiralty2 in civics and self.getUnitInfoID() in lTransports + lPossibleExpeditionariesSea:
			iExp += 4
		
		if iExp > 0:
			self.objUnit.changeExperience(iExp, -1, False, False, False)
		
		# Apply of the promotions to the mercenary in the game
		self.applyPromotions()
		
		# Publish event to track spent Immigration
		events.fireEvent("immigrationSpent", iPlayer, iImmigrationCost)

	# Returns the list of current promotions the mercenary has. If the objUnit is set to
	# a non-None value then the method will rebuild the promotion list and return the
	# promotion list.		
	def getCurrentPromotionList(self):
		' promotionList - the mercenarys current list of promotions '
		
		# If the self.objUnit is actually set then rebuild the self.promotionList from the
		# self.objUnit to get their current promotion list.
		if(self.objUnit != None):
		
			self.promotionList = []			
			
			# Go through each of the promotions defined in the game.
			for i in range(gc.getNumPromotionInfos()):				
				# If the unit has the promotion add it to the promotion list
				if(self.objUnit.isHasPromotion(i)):
					self.promotionList.append(gc.getPromotionInfo(i))

		return self.promotionList

	# Returns true if the available funds are enough to hire
	def canAfford(self, iPlayer):
		# get the player instance
		player = gc.getPlayer(iPlayer)
		
		(iImmigrationCost, iGoldCost) = self.getHireCost(iPlayer)
		
		if iGoldCost <= player.getGold():
			return True
		
		return False
	
	# Returns the cost to hire the mercenary. If objUnit is non-none then the 
	# iHireCost will be updated. Returns (iCostImmigration, iCostGold)
	def getHireCost(self, iPlayer):
		' iHireCost - the cost to hire the mercenary'
		
		if iPlayer == -1:
			iCurrentImmigration = 0
			bDecolonization = False
			bIntervention = False
			bProprietaries = False
			bIndenturedServitude = False
			bPenalColony = False
		else:
			# Get the actual current player object
			player = gc.getPlayer(iPlayer)
			civics = Civics.player(iPlayer)
			iCurrentImmigration = player.getImmigration()
			bDecolonization = iDecolonization3 in civics
			bIntervention = iIntervention2 in civics
			bProprietaries = iProprietaries2 in civics
			bIndenturedServitude = iIndenturedServitude2 in civics
			bPenalColony = iPenalColony2 in civics
			
		# if the self.objUnitInfo is actually set then get the latest cost to hire the mercenary.
		if(self.objUnitInfo != None):
			self.iHireCost = self.objUnitInfo.getProductionCost()
		
		iImmigrationCost = self.iHireCost / 2
		iGoldCost = 0
		
		# Settlers are expensive
		if self.getUnitInfoID() in lSettlers:
			iImmigrationCost = 50
		
		# Great people are very expensive
		if self.getUnitInfoID() in lGreatPeople:
			iImmigrationCost = 1000
		
		# Old World Boosts : Starts at 1 Immigration per 1 Commerce
		if self.getUnitInfoID() in lEndowmentsBase:
			iImmigrationCost = 500
		
		# Scale by game speed
		iImmigrationCost *= int(3 - gc.getGame().getGameSpeedType())
		
		# Increase Immigrant cost by 20% for each time this Civ has hired from category that before
		if iPlayer > -1:
			iImmigrationCost += iImmigrationCost * data.civs[civ(iPlayer)].lUnitCategoriesHired[self.getUnitCategory()] / 5
		
		iImmigrationCostModifier = 100
		
		if bDecolonization:
			iImmigrationCostModifier += 25
		elif bIntervention:
			iImmigrationCostModifier -= 25
		
		if bIndenturedServitude and self.getUnitInfoID() in lWorkers:
			iImmigrationCostModifier -= 50
		
		if bPenalColony and self.getUnitInfoID() == iColonist:
			iImmigrationCostModifier -= 50
		
		iImmigrationCost *= iImmigrationCostModifier
		iImmigrationCost /= 100
		
		if iImmigrationCost > iCurrentImmigration:
			iGoldCost = (iImmigrationCost - iCurrentImmigration) * 2
			iImmigrationCost = iCurrentImmigration
		
		if bProprietaries:
			iGoldCost /= 2
		
		return (iImmigrationCost, iGoldCost)
			
	
	def getHireCostString(self, iPlayer):
		(iImmigrationCost, iGoldCost) = self.getHireCost(iPlayer)
		strHCost = ""
		if iImmigrationCost > 0:
			strHCost += u"%d%c" %(iImmigrationCost, gc.getCommerceInfo(CommerceTypes.COMMERCE_IMMIGRATION).getChar())
		if iGoldCost > 0:
			strHCost += u"%d%c" %(iGoldCost, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
		return strHCost

	def canHireUnit(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		
		# Angle-America RP: Can hire Great People
		if civ(iPlayer) == iAmerica or civ(iPlayer) == iCanada:
			if self.getUnitInfoID() in lGreatPeople:
				return True
		
		# Can hire Colonists and other special units even though you can't train them
		if self.getUnitInfoID() in [iColonist] + lEndowmentsBase:
			return True
		
		if pPlayer.canTrain(self.getUnitInfoID(), false, false):
			return True
		
		return False

	# Returns true if the mercenary is already hired by a player, false otherwise.
	def isHired(self):
		' True - if the mercenary is hired by a player '

		# if the self.objUnit is actually set then set the hired flag and get the reference to the
		# unit that represents the mercenary in the game.		
		if(self.objUnit != None and self.objUnit.getOwner() != self.iBuilder):
			self.bHired = true
			self.iOwner = self.objUnit.getOwner()
		elif(self.iOwner != -1 and self.iOwner != self.iBuilder):
			self.bHired = true
		else:
			self.bHired = false
			self.iOwner = -1
			
		return self.bHired
		

	# Returns true if the mercenary is placed in the game, false otherwise
	def isPlaced(self):
		return (self.iPlacementTurn == -1)

	
	# Returns the number of turns until the mercenary is placed in the game or
	# it will return -1 if the mercenary is already placed in the game.	
	def getPlacementTurns(self):

		# Return -1 immediately if the mercenary is already in the game
		if(self.objUnit != None):
			return -1

		return (self.iPlacementTurn - gc.getGame().getGameTurn()) 


	# Returns the mercenary's current experience level. If objUnit is non-none then the 
	# iExperienceLevel will be updated		
	def getExperienceLevel(self):
		' iExperience - the current mercenary experience level'
		
		# if the self.objUnit is actually set then get the mercenary's current experience level		
		if(self.objUnit != None):
			self.iExperienceLevel = self.objUnit.getExperience()
			
		return self.iExperienceLevel
		

	# Returns the mercenary's next experience level. If objUnit is non-none then the 
	# iNextExperienceLevel will be updated		
	def getNextExperienceLevel(self):
		' iNextExperienceLevel - the next mercenary experience level'
		
		# if the self.objUnit is actually set then get the mercenary's experience required to 
		# get to the next level
		if(self.objUnit != None):
			self.iNextExperienceLevel = self.objUnit.experienceNeeded()
			
		return self.iNextExperienceLevel		
		
		
	# Returns the mercenary's current level. If objUnit is non-none then the 
	# iLevel will be updated		
	def getLevel(self):
		' iLevel - the current mercenarys level'
		
		# if the self.objUnit is actually set then get the mercenary's current level
		if(self.objUnit != None):
			self.iLevel = self.objUnit.getLevel()
			
		return self.iLevel
		
		
	# Returns the mercenary's current owner ID. If objUnit is non-none then the 
	# iOwner and bHired will be updated				
	def getOwner(self):
		' iOwner - the iPlayer value of the owner of the mercenary'

		# if the self.objUnit is actually set then set the hired flag and get the reference to the
		# unit that represents the mercenary in the game.		
		if(self.objUnit != None):
			self.bHired = true
			self.iOwner = self.objUnit.getOwner()
		elif(self.iPlacementTurn != -1):
			self.bHired = true
		else:
			self.bHired = false
			self.iOwner = -1
	
		return self.iOwner
	

	# Applies the promotions from the promotionList to the mercenary represent by objUnit 
	def applyPromotions(self):

		# Return immediately if the self.objUnit is not set.
		if(self.objUnit == None):
			return
					
		for i in range(len(self.promotionList)):
			self.objUnit.setHasPromotion(gc.getInfoTypeForString(self.promotionList[i].getType()),true)
	
	
	# This method will set the initial the mercenary experience and level
	def setExperience(self):

		# Return immediately if the self.objUnit is not set.
		if(self.objUnit == None):
			return

		#level = self.iLevel - 1
		
		#if(level < 0):
		#	level = 0
			
		#self.objUnit.setLevel(level)
		
		#experienceNeeded = self.objUnit.experienceNeeded()
		
		self.objUnit.setLevel(self.iLevel)
		
		# FIX: 03/07/06 - setExperience does not work as expected if you pass in the experience points
		# you want and the number of experience points for the next level. Instead we need to pass in
		# the experience points you want as the value for both parameters.
		#self.objUnit.setExperience(self.iExperienceLevel,self.iNextExperienceLevel)	
		self.objUnit.setExperience(self.iExperienceLevel,self.iExperienceLevel)	


	# Returns the mercenary's name		
	def getName(self):
		return self.strMercenaryName


	# Sets the name for the mercenary
	def setName(self, strMercenaryName):

		# Return immediately if the name passed in is not set	
		if(strMercenaryName == None):
			return

		# Return immediately if the name passed in has a length of 0
		if(len(strMercenaryName) == 0):
			return
			
		self.strMercenaryName = strMercenaryName

		
	# Returns the mercenary's UnitInfo object		
	def getUnitInfo(self):
		
		if(self.objUnitInfo == None and self.objUnit != None):
			self.iUnitInfo = self.objUnit.getUnitType()
			self.objUnitInfo = gc.getUnitInfo(self.iUnitInfo)
			
		# Set the self.iUnitInfo if it hasn't been set and the self.objUnit is set.
		elif(self.iUnitInfo == -1 and self.objUnit != None):
			self.iUnitInfo = self.objUnit.getUnitType()
			
		# Set the self.iUnitInfo if it hasn't been set and the self.objUnitInfo is set.
		elif(self.iUnitInfo == -1 and self.objUnitInfo != None):
			self.iUnitInfo = gc.getInfoTypeForString(self.objUnitInfo.getType())

		return self.objUnitInfo
	
	
	# Returns the UnitInfoID for the mercenary					
	def getUnitInfoID(self):
	
		# Set the self.iUnitInfo if it hasn't been set and the self.objUnit is set.
		if(self.iUnitInfo == -1 and self.objUnit != None):
			self.iUnitInfo = self.objUnit.getUnitType()

		# Set the self.iUnitInfo if it hasn't been set and the self.objUnitInfo is set.
		elif(self.iUnitInfo == -1 and self.objUnitInfo != None):
			self.iUnitInfo = gc.getInfoTypeForString(self.objUnitInfo.getType())
		#print ("self.iUnitInfo", self.iUnitInfo)
			
		return self.iUnitInfo

		
	# Returns the builder ID of the mercenary
	def getBuilder(self):
		return self.iBuilder
	
	def getMercenaryStartingLocation(self, iPlayer):
		pPlot = None
		if self.isShip():
			pPlot = self.getShipPlacementPlot(iPlayer)
		else:
			if self.hasValidSpawnTile(iPlayer):
				pPlot = self.getPlacementShip(iPlayer).plot()
		return pPlot
	
	# Check to see if the mercenary has a spot to go
	def hasValidSpawnTile(self, iPlayer):
		if self.isShip():
			return True
		elif self.objUnitInfo.getDomainType() == 2:		# DOMAIN_LAND = 2
			if self.hasShipForPlacement(iPlayer):
				return True
		return False
	
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
	def getShipPlacementPlot(self, iPlayer):
		iCiv = civ(iPlayer)
		# Some civs spawn in West
		if iCiv in [iPurepecha, iTiwanaku, iWari, iChimu, iMuisca, iRussia, iHawaii, iPeru]:
			return gc.getMap().plot(0, dCapitals[civ(iPlayer)][1])
		else:
			return gc.getMap().plot(iWorldX - 1, dCapitals[civ(iPlayer)][1])
	
	# Is Ship?
	def isShip(self):
		return self.objUnitInfo.getDomainType() == 0		# DOMAIN_SEA = 0
	
	def getUnitCategory(self):
		for iUnitCategory, lUnitCategory in enumerate(lPossibleImmigrants):
			if self.getUnitInfoID() in lUnitCategory:
				return iUnitCategory
		return -1
	
# TO DO: Remove before initial release, but retain in dev copy to finish implementation for mercenary groups feature	
class MercenaryGroup:
	
	# The name of the mercenary group
	strMercenaryGroupName = ""
	
	# The list of mercenaries belonging to the mercenary group
	listMercenaries = []