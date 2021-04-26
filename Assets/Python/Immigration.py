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

import random

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

### Constants ###

### Immigration Schedule (by international civ) ###
# Used for Immigration from areas not represented on the map

tImmDates        =       (1600,1630,1670,1700,1770,1820,1870,1890,1930,1960)

tMigSchedule     =       (   1,   1,   1,   2,   3,   5,   8,   10,  20,  30)

tImmSchedule     =       {
iSpain           :       [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
iFrance          :       [   0,   1,   2,   1,   0,   0,   0,   0,   0,   0],
iEngland         :       [   1,   4,   5,   6,   5,   3,   2,   0,   0,   0],
#iNetherlands     :       [   0,   1,   1,   1,   0,   0,   0,   0,   0,   0],
#iSweden          :       [   0,   1,   1,   1,   1,   0,   0,   0,   1,   1],
#iIreland         :       [   0,   1,   1,   2,   1,   5,   1,   1,   0,   0],
#iGermany         :       [   0,   0,   1,   2,   2,   2,   3,   2,   0,   0],
#iAfrica          :       [   0,   1,   2,   3,   4,   2,   0,   0,   0,   0],
#iItaly           :       [   0,   0,   0,   0,   0,   0,   1,   5,   1,   0],
#iRussia          :       [   0,   0,   0,   0,   0,   0,   1,   4,   2,   0],
#iHungary         :       [   0,   0,   0,   0,   0,   0,   1,   2,   0,   0],
#iChina           :       [   0,   0,   0,   0,   0,   0,   1,   1,   1,   3],
#iJapan           :       [   0,   0,   0,   0,   0,   0,   0,   0,   2,   2],
#iIndia           :       [   0,   0,   0,   0,   0,   0,   0,   0,   0,   2],
}

# MacAurther TODO: Immigration regions
#tImmRegions      =       {
#iSpain           :       [rFlorida, rTexas, rNewMexico, rArizona, rColorado, rUtah, rCalifornia],
#iFrance          :       [rLouisiana], #rQuebec
#iEngland         :       [lColonial],
#iNetherlands     :       [rNewYork, rNewJersey],
#iSweden          :       [rDelaware, rPennslyvania, rMinnesota],
#iIreland         :       [rMassachusetts, rNewHampshire, rPennslyvania, rMaryland, rVirginia, rNorthCarolina, rSouthCarolina, rGeorgia, rConnecticut, rRhodeIsland, rTennessee],
#iGermany         :       [],
#iAfrica          :       [],
#iItaly           :       [],
#iRussia          :       [],
#iHungary         :       [],
#iChina           :       [],
#iJapan           :       [],
#iIndia           :       [],
#}

class Immigration:

#######################################
### Main methods (Event-Triggered) ###
#####################################  

	def checkTurn(self, iGameTurn):
		if iGameTurn >= getTurnForYear(tBirth[iMassachusetts])+utils.getTurns(5):
		#if iGameTurn >= getTurnForYear(tBirth[iVirginia])+utils.getTurns(5):
			self.checkImmigration(iGameTurn)
					
	def setup(self):
		pass

#------------------Immigration-------------------

	def checkImmigration(self, iGameTurn):
	
		if data.iImmigrationTimer == 0:
			print("Doing Immigration")
			self.doImmigration(iGameTurn)
			self.doMigration(iGameTurn)
			iRandom = gc.getGame().getSorenRandNum(6, 'random')
			data.iImmigrationTimer = 5 + iRandom # 5-10 turns
		else:
			data.iImmigrationTimer -= 1
	
	def doImmigration(self, iGameTurn):
		# get available international immigration cities
		lTargetCities = []
		
		# keep track of which players will be recieving Penal Colony immigrants
		lPenalCities = []
		
		# MacAurther TODO: Extend this immigration to more than just the 50 States
		for iPlayer in range(iVirginia, iNumPlayers):
			#MacAurther TODO: When Native Civs are added, implement this:
			#if iPlayer in lCivBioNewWorld and not utils.isReborn(iPlayer): continue # no immigration to natives
			pPlayer = gc.getPlayer(iPlayer)
			
			iCivicGovernment = pPlayer.getCivics(0)
			iCivicImmigration = pPlayer.getCivics(4)
			iPlayerBonus = 0
			if iCivicImmigration == iHaven: iPlayerBonus += 2
			if iCivicImmigration == iIsolationism: iPlayerBonus -= 2
			if iCivicImmigration == iMeltingPot: iPlayerBonus += 4
				
			lCities = []
			for city in utils.getCityList(iPlayer):
				iFoodDifference = city.foodDifference(False)
				iHappinessDifference = city.happyLevel() - city.unhappyLevel(0)
				if iFoodDifference <= 0 or iHappinessDifference <= 0: continue
				
				#if city.getRegionID() in [rNewYork, rMassachusetts, rVirginia]: iBonus += 3
				
				lCities.append((city, iHappinessDifference + iFoodDifference / 2 + city.getPopulation() / 2 + iPlayerBonus))
			
			if lCities:
				lCities.sort(key=itemgetter(1), reverse=True)
				lTargetCities.append(lCities[0])
				# MacAurther TODO: Add check to see if British Vassal once Play as Vassal is fully implemented
				if iCivicImmigration == iPenalColony and iCivicGovernment == iRoyalColony:
					lPenalCities.append(lCities[0])
				
		# sort highest to lowest for happiness/unhappiness
		lTargetCities.sort(key=itemgetter(1), reverse=True)
		
		# determine schedule column
		iCurrentCol = 0
		for iCol,iDate in enumerate(tImmDates):
			if getTurnForYear(iDate) >= iGameTurn:
				break
			iCurrentCol = iCol
		
		# debug:
		#print("iGameTurn: " + str(iGameTurn))
		#print("getTurnForYear(iDate): " + str(getTurnForYear(iDate)))
		#print("tImmDates: " + str(tImmDates))
		#print("iCurrentCol: " + str(iCurrentCol))
		
		# determine sources
		lSources = []
		for iSourceCiv in tImmSchedule:
			lSources += [iSourceCiv]*tImmSchedule[iSourceCiv][iCurrentCol]
		random.shuffle(lSources)
		
		iNumMigrations = min(len(lSources), len(lTargetCities))
		
		# debug:
		print("Immigration: lTargetCities:")
		print(str([(x.getName(), y) for (x,y) in lTargetCities]))
		print("iNumMigrations: " + str(iNumMigrations))
		
		for iMigration in range(iNumMigrations):
			targetCity = lTargetCities[iMigration][0]
			targetCityX = targetCity.getX()
			targetCityY = targetCity.getY()
			iTargetPlayer = targetCity.getOwner()
			
			pPlayer = gc.getPlayer(iTargetPlayer)
			iCivicLabor = pPlayer.getCivics(2)
			iCivicImmigration = pPlayer.getCivics(4)
			iCivicDevelopment = pPlayer.getCivics(5)
			
			bWorker = 0
			bSettler = 0
			data.lImmigrantCount[iTargetPlayer] += 1
			if iCivicLabor == iIndenturedServitude:
				bWorker = data.lImmigrantCount[iTargetPlayer] % 3 == 0
			if iCivicDevelopment == iHeadright:
				bSettler = data.lImmigrantCount[iTargetPlayer] % 5 == 0
			
			if bWorker:
				# worker outcome
				utils.makeUnit(utils.getUniqueUnit(iTargetPlayer, iWorker), iTargetPlayer, (targetCityX, targetCityY), 1)
			if bSettler:
				# settler outcome
				utils.makeUnit(utils.getUniqueUnit(iTargetPlayer, iSettler), iTargetPlayer, (targetCityX, targetCityY), 1)
			if not (bWorker or bSettler):
				# population and cottage outcome
				targetCity.changePopulation(1)
				
				# extra cottage growth for target city's vicinity
				for (i, j) in utils.surroundingPlots((targetCityX, targetCityY), 2):
					pCurrent = gc.getMap().plot(i, j)
					if pCurrent.getWorkingCity() == targetCity:
						pCurrent.changeUpgradeProgress(utils.getTurns(10))
			
			# migration brings culture. If immigrants are from Britian, skip this
			# MacAurther TODO: This isn't working. getCulture() in cvPlot.cpp is returning -1
			iSourcePlayer = lSources[iMigration]
			if iSourcePlayer != iEngland:
				targetPlot = gc.getMap().plot(targetCityX, targetCityX)
				iCultureChange = targetPlot.getCulture(iTargetPlayer) / targetCity.getPopulation()
				targetPlot.changeCulture(iSourcePlayer, iCultureChange, False)
			
				# debug
				#print("targetPlot.getCulture(iTargetPlayer): " + str(targetPlot.getCulture(iTargetPlayer)))
				#print("targetCity.getPopulation(): " + str(targetCity.getPopulation()))
				#print("iCultureChange: " + str(iCultureChange))
				#print("iSourcePlayer: " + str(iSourcePlayer))
			
			# chance to spread state religion if in source city
			if gc.getPlayer(iSourcePlayer).isStateReligion():
				iReligion = gc.getPlayer(iSourcePlayer).getStateReligion()
				if iReligion >= 0:
					if not targetCity.isHasReligion(iReligion):
						iRandom = gc.getGame().getSorenRandNum(3, 'random religion spread')
						if iRandom == 0:
							targetCity.setHasReligion(iReligion, True, True, True)
			
			if utils.getHumanID() == iTargetPlayer:
				pSourcePlayer = gc.getPlayer(iSourcePlayer)
				CyInterface().addMessage(iTargetPlayer, False, iDuration, CyTranslator().getText("TXT_KEY_UP_IMMIGRATION", (targetCity.getName(),pSourcePlayer.getCivilizationDescription(0))), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getUnitInfo(iSettler).getButton(), ColorTypes(iYellow), targetCityX, targetCityY, True, True)
			
			if iCivicImmigration == iMulticulturism:
				self.immigrantsGPP(targetCity)
		
		# Penal Colony immigrants
		for iMigration in range(len(lPenalCities)):
			targetCity = lTargetCities[iMigration][0]
			iTargetPlayer = targetCity.getOwner()
			
			targetCity.changePopulation(1)
			
			if utils.getHumanID() == iTargetPlayer:
				pSourcePlayer = gc.getPlayer(iSourcePlayer)
				CyInterface().addMessage(iTargetPlayer, False, iDuration, CyTranslator().getText("TXT_KEY_UP_IMMIGRATION_PRISONERS", (targetCity.getName(),)), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getUnitInfo(iSettler).getButton(), ColorTypes(iYellow), targetCityX, targetCityY, True, True)
	
	def doMigration(self, iGameTurn):
		
		#MacAurther TODO: Migrations increase in frequency as the game goes on
		#iMigrationFactor = 0
		#MacAurther TODO: Consider linking iMigrationFactor to techs
		
		# get available migration and immigration cities
		lSourceCities = []
		lTargetCities = []
		
		# MacAurther TODO: Extend this migration to more than just the 50 States
		for iPlayer in range(iVirginia, iNumPlayers):
			#MacAurther TODO: When Native Civs are added, implement this:
			#if iPlayer in lCivBioNewWorld and not utils.isReborn(iPlayer): continue # no immigration to natives
			pPlayer = gc.getPlayer(iPlayer)
			lSourceCitiesPlayer = []
			lTargetCitiesPlayer = []

			for city in utils.getCityList(iPlayer):
				iFoodDifference = city.foodDifference(False)
				iHappinessDifference = city.happyLevel() - city.unhappyLevel(0)
				
				if iFoodDifference <= 0 or iHappinessDifference <= 0:		#Population will only Emmigrate if unhappy or starving
					iValue = 0
					if iFoodDifference < 0:
						iValue -= iFoodDifference / 2
					if iHappinessDifference < 0:
						iValue -= iHappinessDifference
					if iValue > 0:
						lSourceCitiesPlayer.append((city, iValue))
				else:
					lTargetCitiesPlayer.append((city, iHappinessDifference + iFoodDifference / 2 + city.getPopulation() / 2))

			
			if lTargetCitiesPlayer:
				lTargetCitiesPlayer.sort(key=itemgetter(1), reverse=True)
				lTargetCities.append(lTargetCitiesPlayer[0])				#Only one target per player (#MacAurther TODO: Consider revising this, is that balanced?)
			
			if lSourceCitiesPlayer:
				lSourceCitiesPlayer.sort(key=itemgetter(1), reverse=True)
				lSourceCities.append(lSourceCitiesPlayer[0])				#Only one source per player (#MacAurther TODO: Consider revising this, is that balanced?)

				
		# sort highest to lowest for happiness/unhappiness
		lSourceCities.sort(key=itemgetter(1), reverse=True)
		lTargetCities.sort(key=itemgetter(1), reverse=True)
		
		# determine schedule column
		iCurrentCol = 0
		for iCol,iDate in enumerate(tImmDates):
			if getTurnForYear(iDate) >= iGameTurn:
				break
			iCurrentCol = iCol
		
		# determine max migrations
		# MacAurther TODO: Consider tying this to Technology as opposed to a schedule
		iMaxMigrations = tMigSchedule[iCol]
		
		iNumMigrations = min(min(len(lSourceCities), len(lTargetCities)), iMaxMigrations)
		
		#debug:
		print("Migration: lSourceCities:")
		print(str([(x.getName(), y) for (x,y) in lSourceCities]))
		print("Migration: lTargetCities:")
		print(str([(x.getName(), y) for (x,y) in lTargetCities]))
		print("iNumMigrations: " + str(iNumMigrations))
		
		for iMigration in range(iNumMigrations):
			sourceCity = lSourceCities[iMigration][0]
			targetCity = lTargetCities[iMigration][0]
			targetCityX = targetCity.getX()
			targetCityY = targetCity.getY()
			iTargetPlayer = targetCity.getOwner()
			
			pPlayer = gc.getPlayer(iTargetPlayer)
			iCivicLabor = pPlayer.getCivics(2)
			iCivicImmigration = pPlayer.getCivics(4)
			iCivicDevelopment = pPlayer.getCivics(5)
			
			sourceCity.changePopulation(-1)
			targetCity.changePopulation(1)
			
			# migration brings culture
			targetPlot = gc.getMap().plot(targetCityX, targetCityY)
			iSourcePlayer = sourceCity.getOwner()
			iCultureChange = targetPlot.getCulture(iTargetPlayer) / targetCity.getPopulation()
			targetPlot.changeCulture(iSourcePlayer, iCultureChange, False)
			
			if gc.getPlayer(iSourcePlayer).isStateReligion():
				iReligion = gc.getPlayer(iSourcePlayer).getStateReligion()
				if sourceCity.isHasReligion(iReligion) and not targetCity.isHasReligion(iReligion):
					iRandom = gc.getGame().getSorenRandNum(3, 'random religion spread')
					if iRandom == 0:
						targetCity.setHasReligion(iReligion, True, True, True)
						
			# notify affected players
			if utils.getHumanID() == iSourcePlayer:
				CyInterface().addMessage(iSourcePlayer, False, iDuration, CyTranslator().getText("TXT_KEY_UP_EMIGRATION", (sourceCity.getName(),targetCity.getName(),pPlayer.getName())), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getUnitInfo(iSettler).getButton(), ColorTypes(iYellow), sourceCity.getX(), sourceCity.getY(), True, True)
			if utils.getHumanID() == iTargetPlayer:
				pSourcePlayer = gc.getPlayer(iSourcePlayer)
				CyInterface().addMessage(iTargetPlayer, False, iDuration, CyTranslator().getText("TXT_KEY_UP_MIGRATION", (targetCity.getName(),sourceCity.getName(),pSourcePlayer.getCivilizationDescription(0))), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getUnitInfo(iSettler).getButton(), ColorTypes(iYellow), targetCityX, targetCityY, True, True)
			
	
	#MacAurther name change: canadianUP -> immigrantsGPP
	def immigrantsGPP(self, city):
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