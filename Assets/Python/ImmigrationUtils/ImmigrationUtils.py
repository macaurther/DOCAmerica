#
# Mercenaries Mod
# By: The Lopez
# ImmigrationUtils
# 

from CvPythonExtensions import *

import CvUtil

import CvEventManager
import sys
import PyHelpers
import CvMainInterface
#import CvConfigParser #Rhye
import math

import pickle

from RFCUtils import *
from Consts import *
from Core import *
from Civics import *
import PlayerUtil

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

#Rhye - start
lForbiddenUnits = ("UNIT_BEAR",
				"UNIT_PANTHER",
				"UNIT_WOLF",
				"UNIT_SPY")
#Rhye - end

iNumImmigrantCategories = 12
#				2				3				4				5				6				7				8				9				10
(iSettlersCat,	iWorkersCat,	iMissionariesCat,iTransportsCat,iGreatPeopleCat,iSlavesCat,		iColonistsCat,	iMigrantWorkerCat,iExplorersCat,iMilitiaCat,	
iMainlineCat,	iSpecialtyCat) = range(iNumImmigrantCategories)

lSettlers = [iSettler, iPioneer]
lWorkers = [iWorker, iPromyshlenniki, iLaborer, iMadeireiro]
lMissionaries = [iOrthodoxMiss, iCatholicMiss, iProtestantMiss]
lTransports = [iLongship, iCaravel, iCarrack, iIndiaman, iGalleon, iFluyt, iBrigantine, iSteamship]
lGreatPeople = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral]
lSlaves = [iAfricanSlave]
lColonists = [iColonist]
lMigrantWorkers = [iMigrantWorker]
lExplorers = [iExplorer, iBandeirante, iCoureurDesBois, iRanger]
lMilitia = [iMilitia2, iMilitia3, iMilitia4, iMilitia5]
lMainlineUnits = [iArquebusier, iMusketman, iMusketeer, iRifleman]
lSpecialtyUnits = [iTercio, iFusilier, iCompagnies, iLineInfantry, iRedcoat, iMarine, iCrossbowman, iLightCannon, iFieldGun, iGatlingGun, iSkirmisher, iGrenadier, iHussar, iDragoon, iPistolier, iCuirassier, iConquistador, iCarabineer, iCavalry, iBombard, iCannon, iArtillery, iHowitzer, iSloop, iFrigate, iIronclad, iPrivateer, iTorpedoBoat, iBarque, iShipOfTheLine, iManOfWar, iCruiser]

lPossibleColonists = [lSettlers, lWorkers, lMissionaries, lTransports, lGreatPeople, lSlaves, lColonists, lMigrantWorkers]

lPossibleExpeditionaries = [lExplorers, lMilitia, lMainlineUnits, lSpecialtyUnits]

lPossibleImmigrants = lPossibleColonists + lPossibleExpeditionaries

# Change this to increase or decrease the chance that a mercenary will get a promotion.
# The default value of 10 means that the mercenary has a 10% chance of getting one of
# their promotions.
# Default value is 10
g_iMercenaryPromotionChance = 6 #Rhye

# Change this to true to give mercenaries the prereq promotions when it is set to true 
# and the mercenary is given a promotion with unmet prereqs. Mercenaries that can have 
# combat 1 - 5 and were given combat 5 would automaticallly be given combat 1-4 if the 
# value is set to true. WARNING: Setting this value to true will cause hire and 
# maintenance costs to go up for mercenaries.
# Default value is true
g_bBackfillPrereqPromotions = true

# Change this to either increase or decrease mercenary hiring costs. For example if 
# mercenaries should cost 50% less then the value should be set to 0.5. If mercenaries
# should cost 50% more then the value should be set to 1.5.
# Default value is 0.8
g_dHireCostModifier = 0.20 #Rhye

g_dBaseHireCost = 15 #Rhye

# Change this to either increase or decrease mercenary maintenace costs. For example if 
# mercenary maintenace should cost 50% less then the value should be set to 0.5. If 
# mercenary maintenace should cost 50% more then the value should be set to 1.5.
# Default value is 1.0
g_dMaintenanceCostModifier = 0.15 #Rhye

g_dBaseMaintenanceCost = 2 #Rhye

# Change this to increase or decrease the minimum number of promotions each mercenary 
# should have when initially added to the global mercenary pool by the game.
# Default value is 1
g_iMinimumStartingMercenaryPromotionCount = 1

# Change this to true if mercenary moves should be consumed when they are hired and
# added to the game.
# Default value is true
g_bConsumeMercenaryMovesOnHire = true

# Change this to false to supress the mercenary messages.
# Default value is true
g_bDisplayMercenaryMessages = true

# Set to true to print out debug messages in the logs
g_bDebug = false


# Default value is 100
g_iAIHireCostPercent = 100 - (gc.getGame().getHandicapType())*25 #Rhye

# Default value is 100
g_iAIMaintenanceCostPercent = 100 - (gc.getGame().getHandicapType())*25 #Rhye


class ImmigrationUtils:

	# The constructor for the ImmigrationUtils class. First we check to see if the 
	# data has been setup using pickle. Then we try to read in the configuration 
	# information from the INI config file.
	def __init__(self):
		self.firsttime = true
		
		# Setup the mercenary data structure if it hasn't been setup yet.
		if(sdEntityExists("Mercenaries Mod","MercenaryData") == False):
			self.setupMercenaryData()

		global g_iStartingEra
		global g_iMercenaryPromotionChance
		global g_bBackfillPrereqPromotions
		global g_dHireCostModifier
		global g_dMaintenanceCostModifier
		global g_iMinimumStartingMercenaryPromotionCount
		global g_bConsumeMercenaryMovesOnHire
		global g_bDisplayMercenaryMessages
		
	# This method will set the initial the mercenary experience and levels by using the 
	# number of promotions retrieved from calling getMercenaryPromotions(...) method
	def setInitialMercenaryExperience(self, objMercenary, promotionList):
	
		# Return immediately if the objMercenary is not set
		if(objMercenary == None):
			return
			
		# Return immediately if the promotionList os not set
		if(promotionList == None):
			return
												
		# Get the number of promotions in the promotion list
		iPromotionCount = len(promotionList)
		
		# Set the level of the mercenary to promotion count - 1
		objMercenary.setLevel(iPromotionCount-1)
		
		# Get the experience level of the mercenary
		iMercenaryExperience = objMercenary.experienceNeeded()

		# Reset the mercenary level to their real level
		objMercenary.setLevel(iPromotionCount)
	
		iRandomBonusExperience = 0
	
		# Get a random experience amount 	
		if(iMercenaryExperience < objMercenary.experienceNeeded()):
			iRandomBonusExperience = gc.getGame().getMapRand().get(objMercenary.experienceNeeded()-iMercenaryExperience, "Random Bonus XP")

		# Set the experience level for the mercenary
		objMercenary.setExperience(iMercenaryExperience+iRandomBonusExperience,objMercenary.experienceNeeded())
		
		
	# This method will return the max era from the techList
	def getMaxTechEra(self, techList):
		' iEra - the youngest era in the techList'
		
		# Return ERA_ANCIENT immediately if the techList is not set
		if(techList == None):
                        #Rhye - start
			#return EraTypes.ERA_ANCIENT
                        return 0
                        #Rhye - end
			
		# Return ERA_ANCIENT immediately if the techList is empty
		if(len(techList) == 0):
			return 0
			
		# If the techList contains only one TechInfo then return its era information
		if(len(techList) == 1):
			return gc.getTechInfo(techList[0]).getEra()
									
		eraList = []
		
		# Go through each TechInfo in the techList and get its era information and
		# append it to the end of the eraList
		for i in range(len(techList)):
			eraList.append(gc.getTechInfo(techList[i]).getEra())
		
		# Sort the eraList and reverse its order. This is done to get the max era value
		# as the first item of the list.
		eraList.sort()
		eraList.reverse()
		
		return eraList[0]
	
	
	# This was developed to fetch the prereq techs for a unit in one call instead of having
	# to call the PyHelpers.py file UnitInfo getTechPrereqID and getPrereqOrTechIDList methods
	# which is quite silly since if there are two prereq techs for a UnitInfo you have to
	# call getTechPrereqID to get the first one and getPrereqOrTechIDList to get the second
	# one instead of just being able to call getPrereqOrTechIDList.
	def getUnitPrereqTechs(self, objUnitInfo):
		' list - the list of prereq techs'

		unitTechPrereqList = []

		# Return immediately if an invalid objUnitInfo was passed in
		if(objUnitInfo == None):
			return []

		# Return immediately if the unit doesn't have a tech prereq 
		if(objUnitInfo.getTechPrereqID() == -1):
			return unitTechPrereqList

		# Append the objUnitInfos first tech prereq
		unitTechPrereqList.append(objUnitInfo.getTechPrereqID())

		i = 0
		
		# Get the rest of objUnitInfos tech prereqs
		result = objUnitInfo.info.getPrereqAndTechs(i)
	
		# Return if there aren't any more prereq techs.
		if(result == -1):
			return unitTechPrereqList
	
		# Go through the tech prereqs and append them to the unitTechPrereqList
		while(result > -1):
			unitTechPrereqList.append(result)
			i = i + 1
			# get the next prereq tech
			result = objUnitInfo.info.getPrereqAndTechs(i)

		return unitTechPrereqList


	# Returns the list of possible promotions that the objUnit can have
	def getUnitPromotionList(self, objUnit):
		' objList - the list of possible promotions the mercenary can have'

		# Return immediately if objUnit was not set
		if(objUnit == None):
			return

		objUnitInfo = gc.getUnitInfo(objUnit.getUnitType())
							
		promotionList = []
		
		# Go through the list of the promotions defined in the game and check to see if the
		# CyUnit passed in as objUnit can have them
		for i in range(gc.getNumPromotionInfos()):

			# Get the promotion information
			promotionInfo = gc.getPromotionInfo(i)

			# Get the PromotionType integer value
			iPromotionInfoType = gc.getInfoTypeForString(gc.getPromotionInfo(i).getType())

			# If the CyUnit can have the promotion then append it to the end of promotionList
			if (isPromotionValid(iPromotionInfoType, objUnit.getUnitType(), False)):
				promotionList.append(promotionInfo)
		
		# Debug code - start		
		if g_bDebug:
			promotions = objUnit.getName() + " : "
			for i in range(len(promotionList)):
				promotions = promotions + promotionList[i].getType() + ", "		

			# Debug print statement
			CvUtil.pyPrint(promotions)
		# Debug code - end
		
		return promotionList
		
		
	# Returns the list of possible promotions that the objUnit can have up to the given
	# era through iEra
	def getEraAppropriateUnitPromotionList(self, objUnit, iEra):
		' objList - the list of possible promotions the mercenary can have'

		# Return immediately if objUnit was not set
		if(objUnit == None):
			return
		
		# return immediately if the iEra doesn't contain a valid value for an era
		if(gc.getEraInfo(iEra) == None):
			return

		promotionList = []
		
		objUnitInfo = gc.getUnitInfo(objUnit.getUnitType())

		for i in range(gc.getNumPromotionInfos()):
			# Get the promotion information
			promotionInfo = gc.getPromotionInfo(i)

			# Get the PromotionType integer value
			iPromotionInfoType = gc.getInfoTypeForString(gc.getPromotionInfo(i).getType())

			# Get the prereq tech for the promotion
			iTechInfo = promotionInfo.getTechPrereq()
			bEraMatch = false
			
			# Set bEraMatch to true if there is a tech prereq. for the promotion and the
			# tech prereq. era matches the era passed through iEra or if there is no
			# tech prereq.
			if(iTechInfo >= 0 and gc.getTechInfo(iTechInfo).getEra() <= iEra):
				bEraMatch = true
			else:
				bEraMatch = true

			#Rhye - start (less super-units)
			#vanilla array
			#lPromotionOdds = [100, 80, 60, 40, 20, 80, 80, 80, 60, 60, 60, 60, 20, 40, 20, 80, 60, 100, 80, 100, 80, 100, 80, 60, 100, 80, 60, 100, 80, 60, 40, 100, 80, 60, 60, 100, 80, 20, 60, 80, 60, 100, 100, 100, 100]
			#                                                                                       #guerilla                                                                     #flanking                #self pres.    #mercenary
			#warlords array
			#lPromotionOdds = [100, 80, 60, 40, 20, 80, 80, 80, 60, 60, 60, 60, 20, 40, 20, 80, 60, 100, 80, 60, 100, 80, 100, 80, 60, 100, 80, 60, 100, 80, 60, 40, 100, 80, 60, 60, 100, 80, 20, 60, 80, 60, 0, 0, 0, 0, 0, 0, 100, 100, 100, 100]
			#                                                                                      #guerilla                                                                         #flanking                 #leader           #self pres.    #mercenary
			#bts array
			lPromotionOdds = [100, 80, 60, 40, 20, 80, 80, 80, 60, 60, 60, 60, 20, 40, 20, 80, 60, 100, 80, 60, 100, 80, 60, 100, 80, 60, 100, 80, 60, 100, 80, 60, 40, 100, 80, 60, 60, 100, 80, 20, 60, 80, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100]#, 100, 100, 100]
                                                                                                              #guerilla              #woodsman3                                                     #flanking                 #leader           #range1        #mercenary #buggy self pres. commented
			iRndNum = gc.getGame().getSorenRandNum(100, 'random')
			#print (gc.getNumPromotionInfos(), len(lPromotionOdds))
			if (iRndNum > lPromotionOdds[i]):
				bEraMatch = false #skip this promotion
			#Rhye - end

			#Rhye - start (no anti-... before correct era)
			if ((i == 7 or i == 24 or i == 34) and gc.getActivePlayer().getCurrentEra() < iRevolutionaryEra):
				bEraMatch = false
			if (i == 10 and gc.getActivePlayer().getCurrentEra() < iIndustrialEra):
				bEraMatch = false
			if (i == 9 and gc.getActivePlayer().getCurrentEra() < iClassicalEra):
				bEraMatch = false
			#Rhye - end	
				
			# If the CyUnit can have the promotion and the era matched then append it to the end 
			# of promotionList
			if(isPromotionValid(iPromotionInfoType, objUnit.getUnitType(), False) and bEraMatch):
				promotionList.append(promotionInfo)
				
		return promotionList		
	
	
	# Returns a reduced set of promotions that the mercenary will have when it is actually
	# placed in the game.
	def getMercenaryPromotions(self, rawPromotionList):
		' objList - list of promotions that the mercenary will have.'
		
		# Return immediately if the rawPromotionList passed in is invalid
		if(rawPromotionList == None):
			return []

		# Return immediately if an empty rawPromotionList was passed in
		if(rawPromotionList == 0):
			return []		
			
		mercenaryPromotionList = []

                iMercenaryPromotionChance = g_iMercenaryPromotionChance + gc.getActivePlayer().getCurrentEra() #Rhye (stronger mercenaries later in the game)
		#print (iMercenaryPromotionChance) #Rhye
		
		# Go through the raw promotion list
		for i in range(len(rawPromotionList)):
			randVal = gc.getGame().getMapRand().get(100, "Unit Count")
			
			# If we beat the odds then append the promotion to the list containing the promotions
			# that mercenary will have
			#if(randVal < g_iMercenaryPromotionChance): #Rhye
			if(randVal < iMercenaryPromotionChance): #Rhye
				mercenaryPromotionList.append(rawPromotionList[i])
	
		# Backfill the prereq promotions if the variable is set and return the resulting list
		# of promotions
		if(g_bBackfillPrereqPromotions):
			return self.getBackfillPrereqPromotions(mercenaryPromotionList)

		return mercenaryPromotionList


	# Returns a list containing all of the promotions including the prereq promotions
	# for the promotion list passed in.
	def getBackfillPrereqPromotions(self, promotionList):
		' promoDict - the dictionary containing the full set of promotions '

		# Return immediately if the promotionList passed in is invalid
		if(promotionList == None):
			return []
			
		# Get the length of the promotionList passed in.
		listLength = len(promotionList)
		
		# Return immediately if an empty promotionList was passed in
		if(listLength == 0):
			return []		

		promoDict = {}

		# Go through the promotion list and populate the current set of promotions
		# in the promotion dictionary
		for i in range(listLength):
			promoDict[gc.getInfoTypeForString(promotionList[i].getType())] = promotionList[i]

		i = 0

		# Go through the promotionList until we get all of the prereq promotions
		while(i < listLength):
			promotionInfo = promotionList[i]

			# If the first promotion prereq is set and it hasn't been added to the promotion dictionary then process it
			if(promotionInfo.getPrereqOrPromotion1() != -1 and not promoDict.has_key(promotionInfo.getPrereqOrPromotion1())):

				# Append the first promotion prereq to the promotion list
				promotionList.append(gc.getPromotionInfo(promotionInfo.getPrereqOrPromotion1()))

				# Set the first promotion prereq to the promotion dictionary
				promoDict[promotionInfo.getPrereqOrPromotion1()] = gc.getPromotionInfo(promotionInfo.getPrereqOrPromotion1())
				
			# If the second promotion prereq is set and it hasn't been added to the promotion dictionary then process it
			if(promotionInfo.getPrereqOrPromotion2() != -1 and not promoDict.has_key(promotionInfo.getPrereqOrPromotion2())):

				# Append the second promotion prereq to the promotion list
				promotionList.append(gc.getPromotionInfo(promotionInfo.getPrereqOrPromotion2()))

				# Set the second promotion prereq to the promotion dictionary
				promoDict[promotionInfo.getPrereqOrPromotion2()] = gc.getPromotionInfo(promotionInfo.getPrereqOrPromotion2())
				
			i = i + 1
			
			# Get the new length of the promotion list since it might have changed
			listLength = len(promotionList)


		# Debug code - start
		if g_bDebug:
			promotionList = promoDict.values()
			promotions = ""
			for i in range(len(promotionList)):
				promotions = promotions + promotionList[i].getType() + ", "		

			CvUtil.pyPrint(promotions)
		# Debug code - end
	
		# Return the new list of promotions 	
		return promoDict.values()
		
		
	# Returns the colonists available for hire.
	def getAvailableColonists(self, iPlayer):
		' colonistsDict - the dictionary containing the colonists that are available for hire by players '

		colonistsDict = {}
		
		pPlayer = gc.getPlayer(iPlayer)
		
		# Get Settler type available
		if pPlayer.canTrain(iPioneer, false, false):
			colonistsDict = self.addAvailableUnit(iPioneer, colonistsDict)
		elif pPlayer.canTrain(iSettler, false, false):
			colonistsDict = self.addAvailableUnit(iSettler, colonistsDict)
		
		# Get Worker type available
		if pPlayer.canTrain(iMadeireiro, false, false):
			colonistsDict = self.addAvailableUnit(iMadeireiro, colonistsDict)
		elif pPlayer.canTrain(iLaborer, false, false):
			colonistsDict = self.addAvailableUnit(iLaborer, colonistsDict)
		elif pPlayer.canTrain(iPromyshlenniki, false, false):
			colonistsDict = self.addAvailableUnit(iPromyshlenniki, colonistsDict)
		elif pPlayer.canTrain(iWorker, false, false):
			colonistsDict = self.addAvailableUnit(iWorker, colonistsDict)
		
		# Get Missionary type available
		if pPlayer.getStateReligion() == iOrthodoxy and not gc.getGame().isUnitClassMaxedOut(gc.getUnitInfo(iOrthodoxMiss).getUnitClassType(), 0):
			colonistsDict = self.addAvailableUnit(iOrthodoxMiss, colonistsDict)
		elif pPlayer.getStateReligion() == iCatholicism and not gc.getGame().isUnitClassMaxedOut(gc.getUnitInfo(iCatholicMiss).getUnitClassType(), 0):
			colonistsDict = self.addAvailableUnit(iCatholicMiss, colonistsDict)
		elif pPlayer.getStateReligion() == iProtestantism and not gc.getGame().isUnitClassMaxedOut(gc.getUnitInfo(iProtestantMiss).getUnitClassType(), 0):
			colonistsDict = self.addAvailableUnit(iProtestantMiss, colonistsDict)
		
		# Get Transport Ship type available
		if pPlayer.canTrain(iSteamship, false, false):
			colonistsDict = self.addAvailableUnit(iSteamship, colonistsDict)
		elif pPlayer.canTrain(iBrigantine, false, false):
			colonistsDict = self.addAvailableUnit(iBrigantine, colonistsDict)
		elif pPlayer.canTrain(iFluyt, false, false):
			colonistsDict = self.addAvailableUnit(iFluyt, colonistsDict)
		elif pPlayer.canTrain(iGalleon, false, false):
			colonistsDict = self.addAvailableUnit(iGalleon, colonistsDict)
		elif pPlayer.canTrain(iIndiaman, false, false):
			colonistsDict = self.addAvailableUnit(iIndiaman, colonistsDict)
		elif pPlayer.canTrain(iCarrack, false, false):
			colonistsDict = self.addAvailableUnit(iCarrack, colonistsDict)
		elif pPlayer.canTrain(iCaravel, false, false):
			colonistsDict = self.addAvailableUnit(iCaravel, colonistsDict)
		elif pPlayer.canTrain(iLongship, false, false):
			colonistsDict = self.addAvailableUnit(iLongship, colonistsDict)
		
		# Colonist is always available
		colonistsDict = self.addAvailableUnit(iColonist, colonistsDict)
		
		# Get Great Person available (Anglo-America RP)
		if civ(iPlayer) == iAmerica or civ(iPlayer) == iCanada:
			colonistsDict = self.addAvailableUnit(iGreatProphet, colonistsDict)
			colonistsDict = self.addAvailableUnit(iGreatArtist, colonistsDict)
			colonistsDict = self.addAvailableUnit(iGreatScientist, colonistsDict)
			colonistsDict = self.addAvailableUnit(iGreatMerchant, colonistsDict)
			colonistsDict = self.addAvailableUnit(iGreatEngineer, colonistsDict)
			colonistsDict = self.addAvailableUnit(iGreatStatesman, colonistsDict)
			colonistsDict = self.addAvailableUnit(iGreatGeneral, colonistsDict)
		
		player = gc.getPlayer(iPlayer)
		civics = Civics.player(iPlayer)
		
		# Get Slave available
		if iSlavery in civics:
			colonistsDict = self.addAvailableUnit(iAfricanSlave, colonistsDict)
		
		# Get Migrant Worker available
		if iImmigrantLabor in civics:
			colonistsDict = self.addAvailableUnit(iMigrantWorker, colonistsDict)
		
		return colonistsDict
	
	# Returns the expeditionaries available for hire.
	def getAvailableExpeditionaries(self, iPlayer):
		' expeditionariesDict - the dictionary containing the expeditionaries that are available for hire by players '

		expeditionariesDict = {}
		
		pPlayer = gc.getPlayer(iPlayer)
		
		# Get Recon type available
		if pPlayer.canTrain(iRanger, false, false):
			expeditionariesDict = self.addAvailableUnit(iRanger, expeditionariesDict)
		elif pPlayer.canTrain(iCoureurDesBois, false, false):
			expeditionariesDict = self.addAvailableUnit(iCoureurDesBois, expeditionariesDict)
		elif pPlayer.canTrain(iBandeirante, false, false):
			expeditionariesDict = self.addAvailableUnit(iBandeirante, expeditionariesDict)
		elif pPlayer.canTrain(iExplorer, false, false):
			expeditionariesDict = self.addAvailableUnit(iExplorer, expeditionariesDict)
		
		# Get Militia type available
		if pPlayer.canTrain(iMilitia5, false, false):
			expeditionariesDict = self.addAvailableUnit(iMilitia5, expeditionariesDict)
		elif pPlayer.canTrain(iMilitia4, false, false):
			expeditionariesDict = self.addAvailableUnit(iMilitia4, expeditionariesDict)
		elif pPlayer.canTrain(iMilitia3, false, false):
			expeditionariesDict = self.addAvailableUnit(iMilitia3, expeditionariesDict)
		elif pPlayer.canTrain(iMilitia2, false, false):
			expeditionariesDict = self.addAvailableUnit(iMilitia2, expeditionariesDict)
		
		# Get Infantry type available
		if pPlayer.canTrain(iRifleman, false, false):
			expeditionariesDict = self.addAvailableUnit(iRifleman, expeditionariesDict)
		elif pPlayer.canTrain(iMusketeer, false, false):
			expeditionariesDict = self.addAvailableUnit(iMusketeer, expeditionariesDict)
		elif pPlayer.canTrain(iMusketman, false, false):
			expeditionariesDict = self.addAvailableUnit(iMusketman, expeditionariesDict)
		elif pPlayer.canTrain(iArquebusier, false, false):
			expeditionariesDict = self.addAvailableUnit(iArquebusier, expeditionariesDict)
		
		# Get Elite type available
		if pPlayer.canTrain(iMarine, false, false):
			expeditionariesDict = self.addAvailableUnit(iMarine, expeditionariesDict)
		elif pPlayer.canTrain(iRedcoat, false, false):
			expeditionariesDict = self.addAvailableUnit(iRedcoat, expeditionariesDict)
		elif pPlayer.canTrain(iLineInfantry, false, false):
			expeditionariesDict = self.addAvailableUnit(iLineInfantry, expeditionariesDict)
		elif pPlayer.canTrain(iCompagnies, false, false):
			expeditionariesDict = self.addAvailableUnit(iCompagnies, expeditionariesDict)
		elif pPlayer.canTrain(iFusilier, false, false):
			expeditionariesDict = self.addAvailableUnit(iFusilier, expeditionariesDict)
		elif pPlayer.canTrain(iTercio, false, false):
			expeditionariesDict = self.addAvailableUnit(iTercio, expeditionariesDict)
		
		# Get Collateral type available
		if pPlayer.canTrain(iGatlingGun, false, false):
			expeditionariesDict = self.addAvailableUnit(iGatlingGun, expeditionariesDict)
		elif pPlayer.canTrain(iFieldGun, false, false):
			expeditionariesDict = self.addAvailableUnit(iFieldGun, expeditionariesDict)
		elif pPlayer.canTrain(iLightCannon, false, false):
			expeditionariesDict = self.addAvailableUnit(iLightCannon, expeditionariesDict)
		elif pPlayer.canTrain(iCrossbowman, false, false):
			expeditionariesDict = self.addAvailableUnit(iCrossbowman, expeditionariesDict)
		
		# Get Withdrawl type available
		if pPlayer.canTrain(iGrenadier, false, false):
			expeditionariesDict = self.addAvailableUnit(iGrenadier, expeditionariesDict)
		elif pPlayer.canTrain(iSkirmisher, false, false):
			expeditionariesDict = self.addAvailableUnit(iSkirmisher, expeditionariesDict)
		
		# Get Light Cav type available
		if pPlayer.canTrain(iPistolier, false, false):
			expeditionariesDict = self.addAvailableUnit(iPistolier, expeditionariesDict)
		elif pPlayer.canTrain(iDragoon, false, false):
			expeditionariesDict = self.addAvailableUnit(iDragoon, expeditionariesDict)
		elif pPlayer.canTrain(iHussar, false, false):
			expeditionariesDict = self.addAvailableUnit(iHussar, expeditionariesDict)
		
		# Get Heavy Cav type available
		if pPlayer.canTrain(iCavalry, false, false):
			expeditionariesDict = self.addAvailableUnit(iCavalry, expeditionariesDict)
		elif pPlayer.canTrain(iCarabineer, false, false):
			expeditionariesDict = self.addAvailableUnit(iCarabineer, expeditionariesDict)
		elif pPlayer.canTrain(iConquistador, false, false):
			expeditionariesDict = self.addAvailableUnit(iConquistador, expeditionariesDict)
		elif pPlayer.canTrain(iCuirassier, false, false):
			expeditionariesDict = self.addAvailableUnit(iCuirassier, expeditionariesDict)
		
		# Get Seige type available
		if pPlayer.canTrain(iHowitzer, false, false):
			expeditionariesDict = self.addAvailableUnit(iHowitzer, expeditionariesDict)
		elif pPlayer.canTrain(iArtillery, false, false):
			expeditionariesDict = self.addAvailableUnit(iArtillery, expeditionariesDict)
		elif pPlayer.canTrain(iCannon, false, false):
			expeditionariesDict = self.addAvailableUnit(iCannon, expeditionariesDict)
		elif pPlayer.canTrain(iBombard, false, false):
			expeditionariesDict = self.addAvailableUnit(iBombard, expeditionariesDict)
		
		# Get Mainline Ship type available
		if pPlayer.canTrain(iIronclad, false, false):
			expeditionariesDict = self.addAvailableUnit(iIronclad, expeditionariesDict)
		elif pPlayer.canTrain(iFrigate, false, false):
			expeditionariesDict = self.addAvailableUnit(iFrigate, expeditionariesDict)
		elif pPlayer.canTrain(iSloop, false, false):
			expeditionariesDict = self.addAvailableUnit(iSloop, expeditionariesDict)
		
		# Get Withdrawl Ship type available
		if pPlayer.canTrain(iTorpedoBoat, false, false):
			expeditionariesDict = self.addAvailableUnit(iTorpedoBoat, expeditionariesDict)
		elif pPlayer.canTrain(iPrivateer, false, false):
			expeditionariesDict = self.addAvailableUnit(iPrivateer, expeditionariesDict)
		
		# Get Capital Ship type available
		if pPlayer.canTrain(iCruiser, false, false):
			expeditionariesDict = self.addAvailableUnit(iCruiser, expeditionariesDict)
		elif pPlayer.canTrain(iManOfWar, false, false):
			expeditionariesDict = self.addAvailableUnit(iManOfWar, expeditionariesDict)
		elif pPlayer.canTrain(iShipOfTheLine, false, false):
			expeditionariesDict = self.addAvailableUnit(iShipOfTheLine, expeditionariesDict)
		elif pPlayer.canTrain(iBarque, false, false):
			expeditionariesDict = self.addAvailableUnit(iBarque, expeditionariesDict)
			
		return expeditionariesDict
	
	def addAvailableUnit(self, iUnit, unitDict):
		# Get Unit Info
		pUnitInfo = gc.getUnitInfo(iUnit)
		
		# Create a new mercenary
		newMercenary = Mercenary(pUnitInfo.getDescription(), pUnitInfo, [], 0, 1)
		
		# Add the mercenary into the unitDict
		unitDict[newMercenary.getName()] = newMercenary
		
		return unitDict

	
	# Gets a new Mercenary Object based off of the given ID
	def getMercenary(self, iMercenary):
		' objMercenary - the instance of the Mercenary class that represents the mercenary '
		
		# return if that unit name can't be found
		if iMercenary == -1:
			return None
		
		pMercenary = gc.getUnitInfo(iMercenary)
		objMercenary = Mercenary(pMercenary.getDescription(), pMercenary, [], 0, 1)

		return objMercenary
		
		
	# Prints out the mercenary information into the debug log. Wooot!!!
	def printMercenaryDataToLog(self, objMercenary):
		CvUtil.pyPrint("__________________ Mercenary Data Dump Start __________________")
		CvUtil.pyPrint("          Name: " + objMercenary.strMercenaryName)

		CvUtil.pyPrint("     Unit Type: " + objMercenary.getUnitInfo().getDescription())
		CvUtil.pyPrint("     Hire Cost: " + str(objMercenary.getHireCost()))
		CvUtil.pyPrint("         Level: " + str(objMercenary.iLevel))
		CvUtil.pyPrint("            XP: " + str(objMercenary.iExperienceLevel))
		CvUtil.pyPrint("Promotion List: ")

		# Loop through the mercenary's promotion list and print them out to the log.
		for i in range(len(objMercenary.promotionList)):
			CvUtil.pyPrint("               " + objMercenary.promotionList[i].getDescription())
			
		CvUtil.pyPrint("")		
		CvUtil.pyPrint("      Is Hired: " + str(objMercenary.bHired))

		# If the mercenary is hired show the information.
		if(objMercenary.bHired):
			CvUtil.pyPrint("      Hired by: " + gc.getPlayer(objMercenary.iOwner).getName())
		else:
			CvUtil.pyPrint("      Hired by: None")
		
		if(objMercenary.iBuilder != -1):
			CvUtil.pyPrint("      Built by: " + gc.getPlayer(objMercenary.iBuilder).getName())
		else:
			CvUtil.pyPrint("      Built by: None")

		if(objMercenary.iPlacementTurn != -1):
			CvUtil.pyPrint("To be Placed on: " + str(objMercenary.iPlacementTurn))  
		else:
			CvUtil.pyPrint("To be Placed on: already placed")  
		
		CvUtil.pyPrint("__________________ Mercenary Data Dump End   __________________")
		CvUtil.pyPrint("")
		

	# Creates and returns a blank instance of the Mercenary class
	def createBlankMercenary(self):
		return Mercenary("",None,[],-1,-1)
		
	
	
	# This method acts as a proxy to the hire method in the Mercenary class. It will
	# get the mercenary object in the global mercenary pool
	def hireMercenary(self, iMercenary, iPlayer):
		' bSaved - returns true if the objMercenary was successfully hired'
		
		# Return immediately if the player specified in iPlayer is not alive
		if(not gc.getPlayer(iPlayer).isAlive()):
			return false
			
		# Get the mercenary from the global mercenary pool
		mercenary = self.getMercenary(iMercenary)
		
		# Return immediately if the mercenary was not retrieved from the global
		# mercenary pool
		if(mercenary == None):
			return false	
	
		# Get the starting location for the mercenary
		pPlot = self.getMercenaryStartingLocation(iPlayer, mercenary)
		
		# Return immediately if no suitable plot to spawn
		if pPlot == None:
			return false
                
		mercenary.hire(iPlayer, pPlot)

		print(mercenary.getName() + " hired by: " + gc.getPlayer(mercenary.iOwner).getName()) #Rhye
	
		if g_bDebug:
			self.printMercenaryDataToLog(mercenary)	

	# Gets the max era from the players in the game.
	def getMaxGameEra(self):
		iEra = 0
		
		# Get the active players in the game
		playerList = PyGame.getCivPlayerList()
		
		# Go through the active players in the game
		for pPlayer in playerList:
		
			# If the current player's era is bigger than the current value of iEra
			# set it as the value of iEra
			if(pPlayer.CyGet().getCurrentEra() > iEra):
				iEra = pPlayer.CyGet().getCurrentEra()
		
		return iEra

		
	# Returns the total number of military units in the game
	def getMilitaryUnitCount(self):

		totalMilitaryUnits = 0
		
		# Get the active players in the game
		playerList = PyGame.getCivPlayerList()

		# Go through the active players in the game
		for pPlayer in playerList:
		
			# Add the player's total number of military units to the total
			totalMilitaryUnits = totalMilitaryUnits + pPlayer.CyGet().getNumMilitaryUnits()
			
		return totalMilitaryUnits
	
	# Returns the starting city for a player's mercenary
	def getMercenaryStartingLocation(self, iPlayer, mercenary):
		' CyPlot - the starting plot for hired mercenaries'
		player = gc.getPlayer(iPlayer)
		
		pPlot = mercenary.getMercenaryStartingLocation(iPlayer)
		
		return pPlot
		
	
	# Returns the list of civilizations the player passed in is at war with.
	def getAtWarCivilizations(self, iPlayer):
		
		# Get the player reference
		player = gc.getPlayer(iPlayer)
		
		# Return immediately an empty list if the player reference is set
		# to None
		if(gc.getPlayer(iPlayer) == None):
			return []

		# Get the player's team
		iPlayerTeam = player.getTeam()
		playerTeam = gc.getTeam(iPlayerTeam)
		
		enemyPlayersList = []
		
		# Get the list of players in the game
		playerList = PyGame.getCivPlayerList()
		
		# Go through the list of players in the game
		for pyPlayer in playerList:
			cyPlayer = pyPlayer.CyGet()
	
			# If the player passed in is at war with the current player
			# being processed then add them to the enemyPlayersList		
			if(playerTeam.isAtWar(cyPlayer.getTeam())):
				#Rhye - start
				#enemyPlayersList.append(cyPlayer)
				if ((cyPlayer.getID() < iNumPlayers and gc.getTeam(gc.getPlayer(iPlayer).getTeam()).canContact(cyPlayer.getID()))):
					enemyPlayersList.append(cyPlayer)
				#Rhye - end
				

		return enemyPlayersList
		
	
	# Returns the number of players more powerful than the one passed in			
	def getMorePowerfulPlayerCount(self, iPlayer):
		
		playerCount = 0

		# Get the player reference
		player = gc.getPlayer(iPlayer)
		
		# Return immediately an empty list if the player reference is set
		# to None
		if(gc.getPlayer(iPlayer) == None):
			return 0
		
		# Get the list of players in the game
		playerList = PyGame.getCivPlayerList()
		
		# Go through the list of players in the game
		for pyPlayer in playerList:
			cyPlayer = pyPlayer.CyGet()
	
			# If the other player is more powerful increment playerCount
			if(cyPlayer.getPower() > player.getPower()):
				playerCount = playerCount + 1

		return playerCount
		
						
	# Currently returns the most expensive mercenary that is less expensive than the iGold value passed in.
	# This method needs to be rewritten to get the best mercenary with better definitions		
	def getBestAvailableImmigrant(self, iImmigration, iGold, iPlayer, lCategoryDesire):
		
		hireCost = 0
		
		immigrant = None
		bestImmigrant = None
		
		# Get the available mercenaries from the global immigrant pool
		immigrantDict = self.getAvailableColonists(iPlayer)
		immigrantDict.update(self.getAvailableExpeditionaries(iPlayer))
		
		iHighestDesire = 0
		iHighestDesireCategory = -1
		for immigrantName in immigrantDict:
		
			immigrant = immigrantDict[immigrantName]
			
			# Calculate how much gold the player will have after hiring the immigrant.
			(immigrationCost, goldCost) = immigrant.getHireCost(iPlayer)
			tmpImmigration = iImmigration - immigrationCost
			tmpGold = iGold - goldCost
			
			# Continue immediately if the player can't support the immigrant
			if(tmpImmigration < 0 or tmpGold <= 0):
				continue

			if (not immigrant.canHireUnit(iPlayer)):
				continue
			
			iImmigrantCategory = self.getUnitCategory(immigrant.getUnitInfoID())
			if iImmigrantCategory > -1:
				iDesire = lCategoryDesire[iImmigrantCategory]
			else:
				CvUtil.pyPrint("ERROR: Possible Immigrant " + immigrantName + " does not have a category!")

			if g_bDebug:
				CvUtil.pyPrint("Player: " + str(iPlayer) + " desires " + str(iDesire) + " " + immigrantName)
			
			if iDesire > iHighestDesire:
				iHighestDesire = iDesire 
				bestImmigrant = immigrant
				iHighestDesireCategory = iImmigrantCategory
				if g_bDebug:
					CvUtil.pyPrint("Potential immigrant for " + gc.getPlayer(iPlayer).getName() + " is " + immigrant.getName())
				
		if(g_bDebug and bestImmigrant != None):
			CvUtil.pyPrint("Best immigrant for " + gc.getPlayer(iPlayer).getName() + " is " + bestImmigrant.getName())
		
		# Decrement recommended category so we can just reuse the modified lCategoryDesire list instead of having to recalculate
		if bestImmigrant:
			lCategoryDesire[iHighestDesireCategory] -= 1
		
		return bestImmigrant, lCategoryDesire
	
	def getUnitCategory(self, iUnit):
		for iUnitCategory, lUnitCategory in enumerate(lPossibleImmigrants):
			if iUnit in lUnitCategory:
				return iUnitCategory
		return -1
		
	# Performs the thinking for the computer players in regards to the mercenaries mod functionality.
	# It will:
	#   - Hire mercenaries	
	# It needs to be more complex but for right now it works
	def computerPlayerThink(self, iPlayer):
            
		# Get the player
		pPlayer = gc.getPlayer(iPlayer)
		
		# Return immediately if the player is a filthy human :p
		if(pPlayer.isHuman()):
			return

		# Return immediately if the player is a barbarian
		if(pPlayer.isBarbarian()):
			return
		
		# Get the current immigration for the player	
		currentImmigration = pPlayer.getImmigration()
		
		# Don't do anything if you don't have a lot of immigration
		if currentImmigration <= 50:
			return

		# Get the current gold for the player			
		currentGold = pPlayer.getGold()

		immigrant = None
		
		# Pre-calculate the AI's desire for each Immigrant. Do this ONCE per computer player think call
		lCategoryDesire = self.getAIDesiredCategory(iPlayer)
		
		# Hire Immigrants until we get below 50 Immigration, but don't go below -5 GPT, and don't go below 50 Gold
		while currentImmigration > 50 and pPlayer.getGoldPerTurn() > -5 and currentGold > 50:

			# Get the best available immigrant
			immigrant, lCategoryDesire = self.getBestAvailableImmigrant(currentImmigration, currentGold, iPlayer, lCategoryDesire)

			# Return immediately if a immigrant wasn't returned
			if immigrant == None:
				return
			
			if g_bDebug:
				CvUtil.pyPrint("Player: " + str(iPlayer) + " thinking about iImmigrant: " + str(immigrant.objUnitInfo.getType()))
			
			# Return immediately if there's nowhere to spawn immigrant
			if not immigrant.hasValidSpawnTile(iPlayer):
				if g_bDebug:
					CvUtil.pyPrint("No place to spawn Immigrant")
				return

			# Have the computer hire the immigrant			
			self.hireMercenary(immigrant.getUnitInfoID(), iPlayer)

			# Debug code - start
			if g_bDebug:
				CvUtil.pyPrint(pPlayer.getName() + " current gold: " + str(currentGold) + " Hired " + immigrant.getName())
			# Debug code - end
			
			# deduct the hire cost from the computer players gold
			(immigrationCost, goldCost) = immigrant.getHireCost(iPlayer)
			currentImmigration -= immigrationCost
			currentGold -= goldCost

			# Set the new modified gold amount
			pPlayer.setImmigration(currentImmigration)
			pPlayer.setGold(currentGold)
		

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
		
	def getAIDesiredCategory(self, iPlayer):
		'''Returns the immigrant unit category that the AI wants most'''
		pPlayer = gc.getPlayer(iPlayer)
		iCiv = civ(iPlayer)
		civics = Civics.player(iPlayer)
		
		# Setup lists
		lNumUnitsInCategories = [0] * iNumImmigrantCategories
		lCategoryDesire = [0] * iNumImmigrantCategories
		
		lUnits = PlayerUtil.getPlayerUnits(iPlayer)
		for pUnit in lUnits:
			iUnitCategory = self.getUnitCategory(pUnit.getUnitType())
			if iUnitCategory > -1:
				lNumUnitsInCategories[iUnitCategory] += 1
		
		iNumCities = pPlayer.getNumCities()
		
		# Settlers Category
		# TODO: Find a more elegant way to do this?
		lCategoryDesire[iSettlersCat] = min(dNumCitiesGoal[iCiv] - iNumCities - lNumUnitsInCategories[iSettlersCat], 2 - lNumUnitsInCategories[iSettlersCat])	# Get specific AI's desire to build cities, but don't go crazy on Settlers, max at 2 at a time
		
		# Workers Category
		lCategoryDesire[iWorkersCat] = iNumCities - lNumUnitsInCategories[iWorkersCat]	# Ballpark want 1 worker per city
		
		# Missionaries Category
		if pPlayer.getStateReligion() > -1:
			iNumConvertedCities = 0
			lCities = PlayerUtil.getPlayerCities(iPlayer)
			for pCity in lCities:
				if pCity.isHasReligion(pPlayer.getStateReligion()):
					iNumConvertedCities += 1
			lCategoryDesire[iMissionariesCat] = iNumCities - iNumConvertedCities - lNumUnitsInCategories[iMissionariesCat]
		
		# Transports Category
		lCategoryDesire[iTransportsCat] = iNumCities - lNumUnitsInCategories[iTransportsCat]	# Want 1 Transport per city?
		
		# Choose randomly between Great People, Slaves, Colonists, and Migrant Workers
		# TODO: Find better heuristic
		# Great People Category
		if iCiv in [iAmerica, iCanada]:
			lCategoryDesire[iGreatPeopleCat] = gc.getGame().getSorenRandNum(100, 'random') / 100.0
		
		# Slave Category
		if iSlavery in civics:
			lCategoryDesire[iSlavesCat] = gc.getGame().getSorenRandNum(100, 'random') / 100.0
		
		# Colonist Category
		lCategoryDesire[iColonistsCat] = gc.getGame().getSorenRandNum(100, 'random') / 100.0
		
		# Migrant Worker Category
		if iImmigrantLabor in civics:
			lCategoryDesire[iMigrantWorkerCat] = gc.getGame().getSorenRandNum(100, 'random') / 100.0
		
		# Explorers Category
		if iCiv in [iSpain, iPortugal, iEngland, iFrance, iNetherlands, iRussia]:
			lCategoryDesire[iExplorersCat] = 3 - lNumUnitsInCategories[iExplorersCat]	# Want 3 explorers?

		# Miltia Category
		lCategoryDesire[iMilitiaCat] = iNumCities - lNumUnitsInCategories[iMilitiaCat]	# Want 1 Militia per city?
		
		# Mainline Category
		lCategoryDesire[iMainlineCat] = iNumCities - lNumUnitsInCategories[iMainlineCat]	# Want 1 Mainline infantry per city?
		
		# Specialty Category
		lCategoryDesire[iMainlineCat] = iNumCities / 3 - lNumUnitsInCategories[iMainlineCat]	# Want 1/3 specialty unit per city?
		
		return lCategoryDesire
	
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

		# If g_bConsumeMercenaryMovesOnHire is set to true then use up all of the 
		# mercenaries moves, otherwise just select the mercenary.
		if(g_bConsumeMercenaryMovesOnHire):
			self.objUnit.finishMoves()
		elif(CyGame().isNetworkMultiPlayer()):
			self.objUnit.finishMoves()
		else:
			CyInterface().selectUnit(self.objUnit, true, false, false)

		if(g_bDisplayMercenaryMessages):
			strMessage = self.getName() + " has arrived"
			# Inform the player that the mercenary has arrived.
			CyInterface().addMessage(self.iOwner, False, 20, strMessage, "", 0, self.objUnitInfo.getButton(), ColorTypes(0), pPlot.getX(), pPlot.getY(), True, True) 

		# Set the mercenaries experience
		self.setExperience()		

		# Set the mercenaries unique name
		self.objUnit.setName(self.strMercenaryName)

		self.iPlacementTurn = -1

		if(g_bDisplayMercenaryMessages and self.iBuilder != -1):
			strMessage = self.getName() + " has been hired by " + gc.getPlayer(self.iOwner).getName()
			# Inform the player that the mercenary has been hired.
			CyInterface().addMessage(self.iBuilder, True, 20, strMessage, "", 0, "", ColorTypes(0), -1, -1, True, True) 
	
		# Subtract cost to hire from player current cash
		(iImmigrationCost, iGoldCost) = self.getHireCost(iPlayer)
		player.setImmigration(player.getImmigration() - iImmigrationCost)
		player.setGold(player.getGold() - iGoldCost)
		
		if iGoldCost > 0:
			self.promotionList.append(gc.getPromotionInfo(gc.getInfoTypeForString("PROMOTION_MERCENARY")))
		
		# Apply of the promotions to the mercenary in the game
		self.applyPromotions()

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
		
		modifier = 0
		
		if iPlayer == -1:
			iCurrentImmigration = 0
			bDecolonization = False
			bIntervention = False
			bProprietaries = False
			bIndenturedServitude = False
		else:
			# Get the actual current player object
			player = gc.getPlayer(iPlayer)
			civics = Civics.player(iPlayer)
			iCurrentImmigration = player.getImmigration()
			bDecolonization = iDecolonization in civics
			bIntervention = iIntervention in civics
			bProprietaries = iProprietaries in civics
			bIndenturedServitude = iIndenturedServitude in civics
			
		# if the self.objUnitInfo is actually set then get the latest cost to hire the mercenary.
		if(self.objUnitInfo != None):
			self.iHireCost = (self.objUnitInfo.getProductionCost() * (self.getLevel()+1)) + ((self.getLevel()+1) * int(math.fabs(self.getExperienceLevel() - self.getNextExperienceLevel())))
	
		iImmigrationCost = int(self.iHireCost*g_dHireCostModifier) + g_dBaseHireCost #Rhye
		iGoldCost = 0
		
		# Settlers are expensive
		if self.getUnitInfoID() in lSettlers:
			iImmigrationCost *= 3
		
		# Great people are very expensive
		if self.getUnitInfoID() in lGreatPeople:
			iImmigrationCost *= 30
		
		iImmigrationCostModifier = 100
		
		if bDecolonization:
			iImmigrationCostModifier += 50
		elif bIntervention:
			iImmigrationCostModifier -= 50
		
		if bIndenturedServitude and self.getUnitInfoID() in lWorkers:
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
		
		# Can hire Colonists even though you can't train them
		if self.getUnitInfoID() in [iColonist]:
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
	
	# MacAurther: Check to see if the mercenary has a spot to go
	def hasValidSpawnTile(self, iPlayer):
		if self.isShip():
			return True
		elif self.objUnitInfo.getDomainType() == 2:		# DOMAIN_LAND = 2
			if self.hasShipForPlacement(iPlayer):
				return True
		return False
	
	# MacAurther: In order to place hired unit, the player must have a ship on the edge of the map
	def hasShipForPlacement(self, iPlayer):
		if self.getPlacementShip(iPlayer) != None:
			return True
		return False
	
	# MacAurther: get the ship in which to place a hired land unit
	def getPlacementShip(self, iPlayer):
		lUnits = PlayerUtil.getPlayerUnits(iPlayer)
		for pUnit in lUnits:
			iX = pUnit.getX();
			if iX == 0 or iX == iWorldX - 1:
				if not pUnit.isFull():
					return pUnit
		return None
	
	# MacAurther: Get the tile where hire mercenary ships appear
	def getShipPlacementPlot(self, iPlayer):
		iCiv = civ(iPlayer)
		# Some civs spawn in West
		if iCiv in [iPurepecha, iTiwanaku, iWari, iChimu, iMuisca, iRussia, iHawaii, iPeru]:
			return gc.getMap().plot(0, dCapitals[civ(iPlayer)][1])
		else:
			return gc.getMap().plot(iWorldX - 1, dCapitals[civ(iPlayer)][1])
	
	# MacAurther: Is Ship?
	def isShip(self):
		return self.objUnitInfo.getDomainType() == 0		# DOMAIN_SEA = 0
	
# TO DO: Remove before initial release, but retain in dev copy to finish implementation for mercenary groups feature	
class MercenaryGroup:
	
	# The name of the mercenary group
	strMercenaryGroupName = ""
	
	# The list of mercenaries belonging to the mercenary group
	listMercenaries = []


