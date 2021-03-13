# Rhye's and Fall of Civilization - (a part of) Unique Powers

#Egypt in CvPlayer::canDoCivics() and in WBS
#India in CvPlayer::updateMaxAnarchyTurns()
#China (and England before the change) in CvPlayer::getProductionNeeded()
#Babylonia in CvPlayer.cpp::acquireCity()
# Babylonia now in CvPlayer::getCapitalYieldModifier(); +33% production and commerce in the capital after Code of Laws
#Greece CvCity:getGreatPeopleRate()
#Persia (USED TO BE in CvHandicapInfo::getDistanceMaintenancePercentByID(); THEN in RiseAndFall.py, collapseCapitals()), NOW in Stability.py, onCityAcquired()
#Rome in CvPlot::movementCost()
#Japan, Spain and England in CvUnit::init(). Turkey used to be there as well
# Japan now in CvUnit::experienceNeeded(); +50% promotion tempo
# England now in CvHandicapInfo::getDistanceMaintenancePercentByID()
#Ethiopia in Congresses.py (USED TO BE in CvUnit::init() and CvUnit::upgrade())
#Maya in CvHandicapInfo::getResearchPercentByID()
#Byzantium in Stability.checkImplosion()
#Khmer in CvUnit::canMoveInto()
#Germany (USED TO BE IN in CvUnit::init(), CvUnit::upgrade() and CvUnitAI::AI_pillageValue()); NOW IN CvUnit::upgradePrice()
#France in CvPlayerAI::AI_getAttitudeVal() and in Congresses.py
#Netherlands in CvUnit::canEnterTerritory()
#Mali in CvPlot::calculateYield() and Stability.py and CvInfos.cpp (CvHandicapInfo::getResearchPercentByID())
#Portugal in CvUnit::init()
#Inca in CvPlot::calculateNatureYield()
#Mongolia (USED TO BE IN in CvUnit::pillage()); now HERE and in CvRFCEventHandler.py (in OnCityRazed() and BeginPlayerTurn())
#Turkey HERE + in CvPlayer::canRazeCity()
#America HERE + in CvCity::getCulturePercentAnger()

#MacAurther: States:
#Virginia in CvCity:getGreatPeopleRate()
#Massachusetts in CvPlayer::canDoCivics() and in WBS
#Rhode Island  in CvPlot::calculateNatureYield()

from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
#import cPickle as pickle
from StoredData import data # edead
from Consts import *
from RFCUtils import utils
from operator import itemgetter
import Areas

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

### Constants ###

class UniquePowers:

#######################################
### Main methods (Event-Triggered) ###
#####################################  


	def checkTurn(self, iGameTurn):
		if iGameTurn >= getTurnForYear(tBirth[iMassachusetts])+utils.getTurns(5):
			self.checkImmigration()
					
	def onChangeWar(self, bWar, iTeam, iOtherTeam):
		pass
			
	def setup(self):
		pass
		
	def onBuildingBuilt(self, city, iOwner, iBuilding):
		pass
					

#------------------AMERICAN U.P.-------------------

	def checkImmigration(self):
	
		if data.iImmigrationTimer == 0:
			self.doImmigration()
			iRandom = gc.getGame().getSorenRandNum(6, 'random')
			data.iImmigrationTimer = 5 + iRandom # 5-10 turns
		else:
			data.iImmigrationTimer -= 1
			
	def doImmigration(self):
	
		# get available migration and immigration cities
		lSourceCities = []
		lTargetCities = []
		
		for iPlayer in range(iNumPlayers):
			#if iPlayer in lCivBioNewWorld and not utils.isReborn(iPlayer): continue # no immigration to natives
			pPlayer = gc.getPlayer(iPlayer)
			lCities = []
			#bNewWorld = pPlayer.getCapitalCity().getRegionID() in lNewWorld
			for city in utils.getCityList(iPlayer):
				iFoodDifference = city.foodDifference(False)
				iHappinessDifference = city.happyLevel() - city.unhappyLevel(0)
				#if city.getRegionID() in lNewWorld and bNewWorld:
				if iFoodDifference <= 0 or iHappinessDifference <= 0: continue
				iBonus = 0
				#if city.getRegionID() in [rNewYork, rMassachusetts, rVirginia]: iBonus += 3
				iCivicImmigration = pPlayer.getCivics(4)
				if iCivicImmigration == iHaven: iBonus += 2
				if iCivicImmigration == iPenalColony: iBonus += 5
				if iCivicImmigration == iIsolationism: iBonus -= 2
				if iCivicImmigration == iMeltingPot: iBonus += 4
				
				lCities.append((city, iHappinessDifference + iFoodDifference / 2 + city.getPopulation() / 2 + iBonus))
				
				# MacAurther TODO: No source cities until Western Migration update
				'''elif city.getRegionID() not in lNewWorld and not bNewWorld:
					iValue = 0
					if iFoodDifference < 0:
						iValue -= iFoodDifference / 2
					if iHappinessDifference < 0:
						iValue -= iHappinessDifference
					if iValue > 0:
						lCities.append((city, iValue))'''
			
			if lCities:
				lCities.sort(key=itemgetter(1), reverse=True)
			
				#if bNewWorld:
				lTargetCities.append(lCities[0])
				# MacAurther TODO: No source cities until Western Migration update
				'''else:
					lSourceCities.append(lCities[0])'''
				
		# sort highest to lowest for happiness/unhappiness
		#lSourceCities.sort(key=itemgetter(1), reverse=True)
		lTargetCities.sort(key=itemgetter(1), reverse=True)
		
		#utils.debugTextPopup(str([(x.getName(), y) for (x,y) in lTargetCities]))
		#utils.debugTextPopup("Target city: "+targetCity.getName())
		#utils.debugTextPopup("Source city: "+sourceCity.getName())
		
		#iNumMigrations = min(len(lSourceCities) / 4, len(lTargetCities))
		iNumMigrations = len(lTargetCities) / 4
		
		for iMigration in range(iNumMigrations):
			#sourceCity = lSourceCities[iMigration][0]
			targetCity = lTargetCities[iMigration][0]
			targetCityX = targetCity.getX()
			targetCityY = targetCity.getY()
			iTargetPlayer = targetCity.getOwner()
			
			pPlayer = gc.getPlayer(iTargetPlayer)
			iCivicLabor = pPlayer.getCivics(2)
			iCivicDevelopment = pPlayer.getCivics(5)
			
			workerChance = 0
			settlerChance = 0
			if iCivicLabor == iIndenturedServitude:
				workerChance = 40
			if iCivicDevelopment == iHeadright:
				settlerChance = 20
			
			iRandom = gc.getGame().getSorenRandNum(100, 'random')
			
			if iRandom < workerChance:
				#worker outcome
				utils.makeUnit(utils.getUniqueUnit(iTargetPlayer, iWorker), iTargetPlayer, (targetCityX, targetCityY), 1)
			elif iRandom < workerChance + settlerChance:
				#settler outcome
				utils.makeUnit(utils.getUniqueUnit(iTargetPlayer, iSettler), iTargetPlayer, (targetCityX, targetCityY), 1)
			else:
				#population and cottage outcome
				#sourceCity.changePopulation(-1)
				targetCity.changePopulation(1)
				
				#if sourceCity.getPopulation() >= 9:
				#	sourceCity.changePopulation(-1)
				#	targetCity.changePopulation(1)
					
				# extra cottage growth for target city's vicinity
				for (i, j) in utils.surroundingPlots((targetCityX, targetCityY), 2):
					pCurrent = gc.getMap().plot(i, j)
					if pCurrent.getWorkingCity() == targetCity:
						pCurrent.changeUpgradeProgress(utils.getTurns(10))
			
			
			
			# MacAurther TODO: No source cities until Western Migration update
			'''# migration brings culture
			targetPlot = gc.getMap().plot(x, y)
			iSourcePlayer = sourceCity.getOwner()
			iCultureChange = targetPlot.getCulture(iTargetPlayer) / targetCity.getPopulation()
			targetPlot.changeCulture(iSourcePlayer, iCultureChange, False)'''
			
			# MacAurther TODO: No source cities until Western Migration update
			'''# chance to spread state religion if in source city
			if gc.getPlayer(iSourcePlayer).isStateReligion():
				iReligion = gc.getPlayer(iSourcePlayer).getStateReligion()
				if sourceCity.isHasReligion(iReligion) and not targetCity.isHasReligion(iReligion):
					iRandom = gc.getGame().getSorenRandNum(3, 'random religion spread')
					if iRandom == 0:
						targetCity.setHasReligion(iReligion, True, True, True)'''
						
			# notify affected players
			'''if utils.getHumanID() == iSourcePlayer:
				CyInterface().addMessage(iSourcePlayer, False, iDuration, CyTranslator().getText("TXT_KEY_UP_EMIGRATION", (sourceCity.getName(),)), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getUnitInfo(iSettler).getButton(), ColorTypes(iYellow), sourceCity.getX(), sourceCity.getY(), True, True)'''
			if utils.getHumanID() == iTargetPlayer:
				CyInterface().addMessage(iTargetPlayer, False, iDuration, CyTranslator().getText("TXT_KEY_UP_IMMIGRATION", (targetCity.getName(),)), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getUnitInfo(iSettler).getButton(), ColorTypes(iYellow), targetCityX, targetCityY, True, True)
	
			if iTargetPlayer == iCanada:
				self.canadianUP(targetCity)
		
		
	def canadianUP(self, city):
		iPopulation = 5 * city.getPopulation() / 2
		
		lProgress = []
		bAllZero = True
		for iSpecialist in [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman]:
			iProgress = city.getGreatPeopleUnitProgress(utils.getUniqueUnit(city.getOwner(), iSpecialist))
			if iProgress > 0: bAllZero = False
			lProgress.append(iProgress)
			
		if bAllZero:
			iGreatPerson = utils.getRandomEntry([iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman])
		else:
			iGreatPerson = utils.getHighestIndex(lProgress) + iGreatProphet
			
		iGreatPerson = utils.getUniqueUnit(city.getOwner(), iGreatPerson)
		
		city.changeGreatPeopleProgress(iPopulation)
		city.changeGreatPeopleUnitProgress(iGreatPerson, iPopulation)
		
		if utils.getHumanID() == city.getOwner():
			CyInterface().addMessage(city.getOwner(), False, iDuration, CyTranslator().getText("TXT_KEY_UP_MULTICULTURALISM", (city.getName(), gc.getUnitInfo(iGreatPerson).getText(), iPopulation)), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getUnitInfo(iGreatPerson).getButton(), ColorTypes(iGreen), city.getX(), city.getY(), True, True)
					
	def selectRandomCitySourceCiv(self, iCiv): # Unused
		if gc.getPlayer(iCiv).isAlive():
			cityList = [city for city in utils.getCityList(iCiv) if city.getPopulation() > 1]
			if cityList:
				return utils.getRandomEntry(cityList)
		return False


	def selectRandomCityTargetCiv(self, iCiv): # Unused
		if gc.getPlayer(iCiv).isAlive():
			lCities = []
			for city in utils.getCityList(iCiv):
				if not city.isDisorder() and city.foodDifference(False) > 0:
					lCities.append(city)
			if lCities:
				return utils.getRandomEntry(lCities)
		return False
		
	def getNewWorldCities(self): # Unused
		lCityList = []
		
		for iPlayer in range(iNumPlayers):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.getCapitalCity().getRegionID() in lNewWorld:
				for city in utils.getCityList(iPlayer):
					if city.getRegionID() in lNewWorld:
						lCityList.append(city)
						
		return lCityList
	
	def tradingCompanyCulture(self, city, iCiv, iPreviousOwner):
		tCity = (city.getX(), city.getY())
		x, y = tCity
		for (i, j) in utils.surroundingPlots(tCity):
			pPlot = gc.getMap().plot(i, j)
			if (i, j) == tCity:
				utils.convertPlotCulture(pPlot, iCiv, 51, False)
			elif pPlot.isCity():
				pass
			elif utils.calculateDistance(i, j, x ,y) == 1:
				utils.convertPlotCulture(pPlot, iCiv, 65, True)
			else:
				if pPlot.getOwner() == iPreviousOwner:
					utils.convertPlotCulture(pPlot, iCiv, 15, False)
			