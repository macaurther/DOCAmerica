# Rhye's and Fall of Civilization - Historical Victory Goals

from CvPythonExtensions import *
from StoredData import data
from Consts import *
from RFCUtils import utils
import heapq
import Areas
import CityNameManager as cnm
import DynamicCivs as dc
import BugCore
AdvisorOpt = BugCore.game.Advisors
AlertsOpt = BugCore.game.MoreCiv4lerts

### GLOBALS ###

gc = CyGlobalContext()
localText = CyTranslator()

### CONSTANTS ###

# general constants
lWonders = [i for i in range(iBeginWonders, iNumBuildings)]
lGreatPeople = [iSpecialistGreatProphet, iSpecialistGreatArtist, iSpecialistGreatScientist, iSpecialistGreatMerchant, iSpecialistGreatEngineer, iSpecialistGreatStatesman, iSpecialistGreatGeneral, iSpecialistGreatSpy]


# third Virginian goal: settle 10 great generals or statesmen in Richmond by 1860 AD
tRichmond = ((129, 39),(128, 39),(128, 40))	# Three possible tiles for Richmond

# first Maryland goal: control 70% of the Chesapeake by 1700 AD
tChesapeakeBL = (130, 37)
tChesapeakeTR = (134, 48)
tChesapeakeExceptions = ((130,48), (134,48), (134,47), (134,46), (134,45), (134,44), (130,40), (130,39), (130,38), (130,37),)

# second Maryland goal: build the B&0 Railway by 1827 AD
tBaltimore = ((130, 47),(131, 47),(130, 46)) # Three possible tiles for Baltimore
lOhioWatershed = [(121, 49), (122, 49), (123, 49), (121, 48), (122, 48), (123, 48), (121, 47), (122, 47), (123, 47), 
(121, 46), (122, 46), (123, 46), (121, 45), (122, 45), (121, 44), (122, 44),]

### GOAL CONSTANTS ###

dTechGoals = {
	iMassachusetts: (1, [iIndependence]),
	iDelaware: (0, [iFederalism]),
}

dEraGoals = {}

dWonderGoals = {
	iFrance: (2, [iStatueOfLiberty], True),
	iMassachusetts: (2, [iHarvard], True),
	iNewYork: (2, [iStatueOfLiberty, iBrooklynBridge, iEmpireStateBuilding, iWorldTradeCenter]),
	iAmerica: (1, [iStatueOfLiberty, iBrooklynBridge, iEmpireStateBuilding, iGoldenGateBridge, iPentagon, iUnitedNations], True),
}

dReligionGoals = {}
		
### EVENT HANDLING ###

def setup():

	# ignore AI goals
	bIgnoreAI = (gc.getDefineINT("NO_AI_UHV_CHECKS") == 1)
	data.bIgnoreAI = bIgnoreAI
	
	if bIgnoreAI:
		for iPlayer in range(iNumPlayers):
			if utils.getHumanID() != iPlayer:
				loseAll(iPlayer)
				
def checkTurn(iGameTurn, iPlayer):

	if not gc.getGame().isVictoryValid(7): return
	
	if iPlayer >= iNumPlayers: return
	
	if iGameTurn == utils.getScenarioStartTurn(): return
	
	if not gc.getPlayer(iPlayer).isAlive(): return
	
	# Don't check AI civilizations to improve speed
	if utils.getHumanID() != iPlayer and data.bIgnoreAI: return
	
	pPlayer = gc.getPlayer(iPlayer)
	
	#MacAurther TODO: Add UHVs
	if iPlayer == iSpain:
		pass
				
	elif iPlayer == iFrance:
		pass
			
	elif iPlayer == iEngland:
		pass
		
	elif iPlayer == iVirginia:
		
		# first goal: control Virginia, West Virginia, and Kentucky in 1763 AD
		if iGameTurn == getTurnForYear(1763):
			bVirginia = getNumCitiesInArea(iVirginia, Areas.getNormalArea(iVirginia, False)) >= 5
			bWestVirginia = False
			bKentucky = False
			# MacAurther TODO: Uncomment when WV and KY are added
			#bWestVirginia = getNumCitiesInArea(iVirginia, Areas.getNormalArea(iWestVirginia, False)) >= 2
			#bKentucky = getNumCitiesInArea(iVirginia, Areas.getNormalArea(iKentucky, False)) >= 3
			if bVirginia and bWestVirginia and bKentucky:
				win(iVirginia, 0)
			else:
				lose(iVirginia, 0)
		
		# second goal: have the largest population in the USA in 1800 AD
		if iGameTurn == getTurnForYear(1800):
			if isBestPlayer(iVirginia, playerRealPopulation):
				win(iVirginia, 1)
			else:
				lose(iVirginia, 1)
		
		# third goal: settle a total of ten great generals and statesmen in Richmond
		if isPossible(iVirginia, 2):
			iGreatGenerals = 0
			iGreatStatesmen = 0
			for tPlot in tRichmond:
				iGreatGenerals = max(iGreatGenerals, countCitySpecialists(iVirginia, tPlot, iSpecialistGreatGeneral))
				iGreatStatesmen = max(iGreatStatesmen, countCitySpecialists(iVirginia, tPlot, iSpecialistGreatStatesman))
			
			if iGreatStatesmen + iGreatStatesmen >= 10:
				win(iVirginia, 2)
		
		if iGameTurn == getTurnForYear(1860):
			expire(iVirginia, 2)
	
	elif iPlayer == iMassachusetts:
		
		# first goal: control Massachusetts and Maine in 1660 AD
		if iGameTurn == getTurnForYear(1660):
			bMassachusetts = getNumCitiesInArea(iMassachusetts, Areas.getNormalArea(iMassachusetts, False)) >= 3
			bMaine = False
			# MacAurther TODO: Uncomment when ME is added
			#bMaine = getNumCitiesInArea(iMassachusetts, Areas.getNormalArea(iMaine, False)) >= 2
			if bMassachusetts and bMaine:
				win(iMassachusetts, 0)
			else:
				lose(iMassachusetts, 0)
			
		# second goal: defeat 10 British Units by 1780 AD
		if isPossible(iMassachusetts, 1):
			if data.iMassachusettsVsBritain >= 10:
				win(iEngland, 1)
		
		if iGameTurn == getTurnForYear(1780):
			expire(iEngland, 1)
		
		# third goal: build Harvard by 1675 AD
		if iGameTurn == getTurnForYear(1675):
			expire(iMassachusetts, 2)
		
		# third goal: be the most advanced state in 1800 AD
		if iGameTurn == getTurnForYear(1800):
			if isBestPlayer(iMassachusetts, playerTechs):
				win(iMassachusetts, 0)
			else:
				lose(iMassachusetts, 0)
	
	elif iPlayer == iNewHampshire:
		
		# first goal: control New Hampshire and Vermont in 1660 AD
		if iGameTurn == getTurnForYear(1691):
			bNewHampshire = getNumCitiesInArea(iNewHampshire, Areas.getNormalArea(iNewHampshire, False)) >= 3
			bVermont = False
			# MacAurther TODO: Uncomment when ME is added
			#bVermont = getNumCitiesInArea(iNewHampshire, Areas.getNormalArea(iVermont, False)) >= 2
			if bNewHampshire and bVermont:
				win(iNewHampshire, 0)
			else:
				lose(iNewHampshire, 0)
	
	elif iPlayer == iMaryland:
		
		# first goal: control 70% of the Chesapeake by 1700 AD
		if isPossible(iMaryland, 0):
			iChesapeake, iTotalChesapeake = countControlledTiles(iMaryland, tChesapeakeBL, tChesapeakeTR, False, tChesapeakeExceptions, True)
			fChesapeake = iChesapeake * 100.0 / iTotalChesapeake
			
			if fChesapeake >= 70.0:
				win(iMaryland, 0)
				
		if iGameTurn == getTurnForYear(1930):
			expire(iMaryland, 0)
		
		# second goal: connect the Chesapeake to the Ohio Watershed by Rail by 1827 AD
		# MacAurther TODO: This goal isn't working
		if isPossible(iMaryland, 1):
			for tPlot in tBaltimore:
				if isConnectedByRailroad(iMaryland, tPlot, lOhioWatershed):
					win(iMaryland, 1)
					
		if iGameTurn == getTurnForYear(1827):
			expire(iMaryland, 1)
	
	
	elif iPlayer == iConnecticut:
		
		# first goal: be the first to research 8 Industrial techs
		pass
	
	elif iPlayer == iRhodeIsland:
		pass
	
	elif iPlayer == iNorthCarolina:
		
		# first goal: control North Carolina and Tennessee in 1796 AD
		if iGameTurn == getTurnForYear(1796):
			bNorthCarolina = getNumCitiesInArea(iNorthCarolina, Areas.getNormalArea(iNorthCarolina, False)) >= 5
			bTennessee = False
			# MacAurther TODO: Uncomment when TN is added
			#bWestVirginia = getNumCitiesInArea(iNorthCarolina, Areas.getNormalArea(iTennessee, False)) >= 3
			if bNorthCarolina and bTennessee:
				win(iNorthCarolina, 0)
			else:
				lose(iNorthCarolina, 0)
	
	elif iPlayer == iSouthCarolina:
		pass
	
	elif iPlayer == iNewJersey:
		
		# first goal: have an average city size of 20 in 1950 AD
		if iGameTurn == getTurnForYear(1950):
			if isPossible(iNewJersey, 0):
				if getAverageCitySize(iNewJersey) >= 20.0:
					win(iNewJersey, 0)
				else:
					lose(iNewJersey, 0)
	
	elif iPlayer == iNewYork:
		
		# first goal: make New York the most populous and cultured city in the world in 1900 AD
		if iGameTurn == getTurnForYear(1900):
			if isBestCity(iNewYork, (137, 54), cityPopulation) and isBestCity(iNewYork, (137, 54), cityCulture):
				win(iNewYork, 0)
			else:
				lose(iNewYork, 0)
		
		# second goal: receive the most cumulative Immigrants in 1900 AD
		if iGameTurn == getTurnForYear(1900):
			# If there is a tie, rule in the favor of NY
			iNumImmigrants = data.lImmigrantCount[iNewYork]
			iMostImmigrantsCiv = iNewYork	
			for iCiv in range(iVirginia, iNumPlayers):	# Don't count Euros for now
				if data.lImmigrantCount[iCiv] > iNumImmigrants:
					iNumImmigrants = data.lImmigrantCount[iCiv]
					iMostImmigrantsCiv = iCiv
			
			if iMostImmigrantsCiv == iNewYork:
				win(iNewYork, 1)
			else:
				lose(iNewYork, 1)
	
	elif iPlayer == iPennsylvania:
		
		# first goal: receive 15 immigrants by 1800 AD
		if isPossible(iPennsylvania, 0):
			if data.lImmigrantCount[iPennsylvania] >= 15:
				win(iPennsylvania, 0)
					
		if iGameTurn == getTurnForYear(1800):
			expire(iPennsylvania, 0)
		
		# second goal: secure 8 iron or coal resources by 1910 AD
		if isPossible(iPennsylvania, 1):
			iNumIron = countResources(iPennsylvania, iIron)
			iNumCoal = countResources(iPennsylvania, iCoal)
			
			if iNumIron + iNumCoal >= 8:
				win(iPennsylvania, 1)
				
		if iGameTurn == getTurnForYear(1910):
			expire(iPennsylvania, 1)
	
	elif iPlayer == iDelaware:
		pass
	
	elif iPlayer == iGeorgia:
		
		# first goal: control Georgia, Alabama, and Mississippi in 1797 AD
		if iGameTurn == getTurnForYear(1797):
			bGeorgia = getNumCitiesInArea(iGeorgia, Areas.getNormalArea(iGeorgia, False)) >= 5
			bAlabama = False
			bMississippi = False
			# MacAurther TODO: Uncomment when AL and MS are added
			#bAlabama = getNumCitiesInArea(iGeorgia, Areas.getNormalArea(iAlabama, False)) >= 2
			#bMississippi = getNumCitiesInArea(iGeorgia, Areas.getNormalArea(iMississippi, False)) >= 2
			if bGeorgia and bAlabama and bMississippi:
				win(iGeorgia, 0)
			else:
				lose(iGeorgia, 0)
	
		# second goal: acquire 4000 gold by trade by 1860 AD
		if isPossible(iGeorgia, 1):
			iTradeGold = 0
			
			# gold from city trade routes
			iTradeCommerce = 0
			for city in utils.getCityList(iGeorgia):
				iTradeCommerce += city.getTradeYield(2)
			iTradeGold += iTradeCommerce * pGeorgia.getCommercePercent(0)
			
			# gold from per turn gold trade
			for iPlayer in range(iNumPlayers):
				iTradeGold += pGeorgia.getGoldPerTurnByPlayer(iPlayer) * 100
			
			data.iGeorgiaTradeGold += iTradeGold
			
			if data.iGeorgiaTradeGold / 100 >= utils.getTurns(4000):
				win(iGeorgia, 1)
				
		if iGameTurn == getTurnForYear(1860):
			expire(iGeorgia, 1)
	
	elif iPlayer == iAmerica:
	
		# first goal: allow no European colonies in North America, Central America and the Caribbean and control or vassalize Mexico in 1930 AD
		if iGameTurn == getTurnForYear(1900):
			pass
				
		# second goal: build the Statue of Liberty, the Brooklyn Bridge, the Empire State Building, the Golden Gate Bridge, the Pentagon and the United Nations by 1950 AD
		if iGameTurn == getTurnForYear(1950):
			expire(iAmerica, 1)
			
		# third goal: control 75% of the world's commerce output and military power between you, your vassals and allies by 1990 AD
		if isPossible(iAmerica, 2):
			if calculateAlliedCommercePercent(iAmerica) >= 75.0 and calculateAlliedPowerPercent(iAmerica) >= 75.0:
				win(iAmerica, 2)
				
		if iGameTurn == getTurnForYear(1990):
			expire(iAmerica, 2)
			
	elif iPlayer == iCanada:
	
		# first goal: connect your capital to an Atlantic and a Pacific port by 1920 AD
		if isPossible(iCanada, 0):
			capital = pCanada.getCapitalCity()
			tCapital = (capital.getX(), capital.getY())
			bAtlantic = isConnectedByRailroad(iCanada, tCapital, lAtlanticCoast)
			bPacific = isConnectedByRailroad(iCanada, tCapital, lPacificCoast)
			if bAtlantic and bPacific:
				win(iCanada, 0)
				
		if iGameTurn == getTurnForYear(1920):
			expire(iCanada, 0)
			
		# second goal: control all cities and 90% of the territory in Canada without ever conquering a city by 1950 AD
		if isPossible(iCanada, 1):
			iEast, iTotalEast = countControlledTiles(iCanada, tCanadaEastTL, tCanadaEastBR, False, tCanadaEastExceptions)
			iWest, iTotalWest = countControlledTiles(iCanada, tCanadaWestTL, tCanadaWestBR, False, tCanadaWestExceptions)
			
			fCanada = (iEast + iWest) * 100.0 / (iTotalEast + iTotalWest)
			
			bAllCitiesEast = controlsAllCities(iCanada, tCanadaEastTL, tCanadaEastBR, tCanadaEastExceptions)
			bAllCitiesWest = controlsAllCities(iCanada, tCanadaWestTL, tCanadaWestBR, tCanadaWestExceptions)
			
			if fCanada >= 90.0 and bAllCitiesEast and bAllCitiesWest:
				win(iCanada, 1)
				
		if iGameTurn == getTurnForYear(1950):
			expire(iCanada, 1)
			
		# third goal: end twelve wars through diplomacy by 2000 AD
		if iGameTurn == getTurnForYear(2000):
			expire(iCanada, 2)
			
			
	# check religious victory (human only)
	#MacAurther TODO: Religious Victories?
	'''if utils.getHumanID() == iPlayer:
		iVictoryType = utils.getReligiousVictoryType(iPlayer)
		
		if iVictoryType == iCatholicism:
			if gc.getGame().getSecretaryGeneral(1) == iPlayer:
				data.iPopeTurns += 1
				
		elif iVictoryType == iHinduism:
			if pPlayer.isGoldenAge():
				data.iHinduGoldenAgeTurns += 1
				
		elif iVictoryType == iBuddhism:
			if isAtPeace(iPlayer):
				data.iBuddhistPeaceTurns += 1
				
			if isHappiest(iPlayer):
				data.iBuddhistHappinessTurns += 1
				
		elif iVictoryType == iTaoism:
			if isHealthiest(iPlayer):
				data.iTaoistHealthTurns += 1
				
		elif iVictoryType == iVictoryPaganism:
			if 2 * countReligionCities(iPlayer) > pPlayer.getNumCities():
				data.bPolytheismNeverReligion = False
				
			if gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getPaganReligionName(0) == "Vedism":
				for city in utils.getCityList(iPlayer):
					if city.isWeLoveTheKingDay():
						data.iVedicHappiness += 1
				
		if checkReligiousGoals(iPlayer):
			gc.getGame().setWinner(iPlayer, 8)'''
			
def checkHistoricalVictory(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	
	if not data.players[iPlayer].bHistoricalGoldenAge:
		if countAchievedGoals(iPlayer) >= 2:	
			data.players[iPlayer].bHistoricalGoldenAge = True
			
			iGoldenAgeTurns = gc.getPlayer(iPlayer).getGoldenAgeLength()
			if not gc.getPlayer(iPlayer).isAnarchy(): iGoldenAgeTurns += 1
			
			gc.getPlayer(iPlayer).changeGoldenAgeTurns(iGoldenAgeTurns)
			
			if pPlayer.isHuman():
				CyInterface().addMessage(iPlayer, False, iDuration, CyTranslator().getText("TXT_KEY_VICTORY_INTERMEDIATE", ()), "", 0, "", ColorTypes(iPurple), -1, -1, True, True)
				
				for iLoopPlayer in range(iNumPlayers):
					if iLoopPlayer != iPlayer:
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							pLoopPlayer.AI_changeAttitudeExtra(iPlayer, -2)
			
	if gc.getGame().getWinner() == -1:
		if countAchievedGoals(iPlayer) == 3:
			gc.getGame().setWinner(iPlayer, 7)
		
def onCityBuilt(iPlayer, city):

	if not gc.getGame().isVictoryValid(7): return
	
	if utils.getHumanID() != iPlayer and data.bIgnoreAI: return
	
	if iPlayer >= iNumPlayers: return
	
	iGameTurn = gc.getGame().getGameTurn()
	
				
def onCityAcquired(iPlayer, iOwner, city, bConquest):

	if not gc.getGame().isVictoryValid(7): return
	
	
	if utils.getHumanID() != iPlayer and data.bIgnoreAI: return
			
def onTechAcquired(iPlayer, iTech):
	if not gc.getGame().isVictoryValid(7): return
	
	if iPlayer >= iNumPlayers: return
	
	iGameTurn = gc.getGame().getGameTurn()
	iEra = gc.getTechInfo(iTech).getEra()
	
	# handle all "be the first to discover" goals
	if not isDiscovered(iTech):
		data.lFirstDiscovered[iTech] = iPlayer
		
		for iLoopPlayer in dTechGoals.keys():
			iGoal = dTechGoals[iLoopPlayer][0]
			lTechs = dTechGoals[iLoopPlayer][1]
			
			if not isPossible(iLoopPlayer, iGoal): continue
			
			if iTech in lTechs:
				if iPlayer != iLoopPlayer: lose(iLoopPlayer, iGoal)
				elif checkTechGoal(iLoopPlayer, lTechs): win(iLoopPlayer, iGoal)
				
		# third English goal: be the first to discover ten Renaissance and ten Industrial technologies
		if isPossible(iEngland, 2):
			if iEra in [iExpansionEra, iIndustrialEra]:
				if countFirstDiscovered(iPlayer, iExpansionEra) >= 8 and countFirstDiscovered(iPlayer, iIndustrialEra) >= 8:
					if iPlayer == iEngland: win(iEngland, 2)
					else: lose(iEngland, 2)
				if not isFirstDiscoveredPossible(iEngland, iExpansionEra, 8) or not isFirstDiscoveredPossible(iEngland, iIndustrialEra, 8):
					lose(iEngland, 2)
		
		# first Connecticut goal: be the first to discover eight Industrial technologies
		if isPossible(iConnecticut, 0):
			if iEra in [iIndustrialEra]:
				if countFirstDiscovered(iPlayer, iIndustrialEra) >= 8:
					if iPlayer == iConnecticut: win(iConnecticut, 0)
					else: lose(iEngland, 0)
				if not isFirstDiscoveredPossible(iConnecticut, iIndustrialEra, 8):
					lose(iConnecticut, 0)
				
			
	# handle all "be the first to enter" goals
	if not isEntered(iEra):
		data.lFirstEntered[iEra] = iPlayer
		
		for iLoopPlayer in dEraGoals.keys():
			iGoal = dEraGoals[iLoopPlayer][0]
			lEras = dEraGoals[iLoopPlayer][1]
			
			if not isPossible(iLoopPlayer, iGoal): continue
			
			if iEra in lEras:
				if iPlayer != iLoopPlayer: lose(iLoopPlayer, iGoal)
				elif checkEraGoal(iLoopPlayer, lEras): win(iLoopPlayer, iGoal)
				
def checkTechGoal(iPlayer, lTechs):
	for iTech in lTechs:
		if data.lFirstDiscovered[iTech] != iPlayer:
			return False
	return True
	
def checkEraGoal(iPlayer, lEras):
	for iEra in lEras:
		if data.lFirstEntered[iEra] != iPlayer:
			return False
	return True
	
def onBuildingBuilt(iPlayer, iBuilding):

	if not gc.getGame().isVictoryValid(7): return False
	
	# handle all "build wonders" goals
	if isWonder(iBuilding) and not isWonderBuilt(iBuilding):
		data.setWonderBuilder(iBuilding, iPlayer)
		
		for iLoopPlayer in dWonderGoals.keys():
			iGoal, lWonders, bCanWin = dWonderGoals[iLoopPlayer]
			
			if not isPossible(iLoopPlayer, iGoal): continue
			
			if iBuilding in lWonders:
				if iPlayer != iLoopPlayer: lose(iLoopPlayer, iGoal)
				elif bCanWin and checkWonderGoal(iLoopPlayer, lWonders): win(iLoopPlayer, iGoal)
				
	if utils.getHumanID() != iPlayer and data.bIgnoreAI: return
	
	if not gc.getPlayer(iPlayer).isAlive(): return
	
def checkWonderGoal(iPlayer, lWonders):
	for iWonder in lWonders:
		if data.getWonderBuilder(iWonder) != iPlayer:
			return False
	return True
				
def onReligionFounded(iPlayer, iReligion):

	if not gc.getGame().isVictoryValid(7): return
	
	# handle all "be the first to found" goals
	if not isFounded(iReligion):
		data.lReligionFounder[iReligion] = iPlayer
		
		for iLoopPlayer in dReligionGoals.keys():
			iGoal = dReligionGoals[iLoopPlayer][0]
			lReligions = dReligionGoals[iLoopPlayer][1]
			
			if not isPossible(iLoopPlayer, iGoal): continue
			
			if iReligion in lReligions:
				if iPlayer != iLoopPlayer: lose(iLoopPlayer, iGoal)
				elif checkReligionGoal(iLoopPlayer, lReligions): win(iLoopPlayer, iGoal)
				
def checkReligionGoal(iPlayer, lReligions):
	for iReligion in lReligions:
		if data.lReligionFounder[iReligion] != iPlayer:
			return False
	return True
				
def onCityRazed(iPlayer, city):
	if not gc.getGame().isVictoryValid(7): return
	
	if utils.getHumanID() != iPlayer and data.bIgnoreAI: return
				
def onProjectBuilt(iPlayer, iProject):

	if not gc.getGame().isVictoryValid(7): return
	
	
def onCombatResult(pWinningUnit, pLosingUnit):

	iWinningPlayer = pWinningUnit.getOwner()
	iLosingPlayer = pLosingUnit.getOwner()
	
	if utils.getHumanID() != iWinningPlayer and data.bIgnoreAI: return
	
	pLosingUnitInfo = gc.getUnitInfo(pLosingUnit.getUnitType())
	iDomainSea = DomainTypes.DOMAIN_SEA
	
	# second English goal: control a total of 25 frigates and ships of the line and sink 50 ships in 1800 AD
	if iWinningPlayer == iEngland:
		if isPossible(iEngland, 1):
			if pLosingUnitInfo.getDomainType() == iDomainSea:
				data.iEnglishSinks += 1
	
	# second Massachusetts goal:  defeat 10 British Units by 1780 AD
	if iWinningPlayer == iMassachusetts:
		if isPossible(iMassachusetts, 1):
			if pLosingUnit.getOwner() == iEngland:
				data.iMassachusettsVsBritain += 1
			
					
def onGreatPersonBorn(iPlayer, unit):
	iUnitType = utils.getBaseUnit(unit.getUnitType())
	pUnitInfo = gc.getUnitInfo(iUnitType)
	
	if not isGreatPersonTypeBorn(iUnitType):
		data.lFirstGreatPeople[lGreatPeopleUnits.index(iUnitType)] = iPlayer
					
def onUnitPillage(iPlayer, iGold, iUnit):
	if iGold >= 1000: return

def onCityCaptureGold(iPlayer, iGold):
	pass

def onPlayerGoldTrade(iPlayer, iGold):
	pass

def onPlayerSlaveTrade(iPlayer, iGold):
	pass

def onTradeMission(iPlayer, iX, iY, iGold):
	pass

def onPeaceBrokered(iBroker, iPlayer1, iPlayer2):

	# third Canadian goal: end twelve wars through diplomacy by 2000 AD
	if iBroker == iCanada:
		if isPossible(iCanada, 2):
			data.iCanadianPeaceDeals += 1
			if data.iCanadianPeaceDeals >= 12:
				win(iCanada, 2)
			
def onBlockade(iPlayer, iGold):
	pass
			
def onFirstContact(iPlayer, iHasMetPlayer):
	pass
					
def onPlayerChangeStateReligion(iPlayer, iStateReligion):
	pass
			
def checkReligiousGoals(iPlayer):
	for i in range(3):
		if checkReligiousGoal(iPlayer, i) != 1:
			return False
	return True
	
def checkReligiousGoal(iPlayer, iGoal):
	pPlayer = gc.getPlayer(iPlayer)
	iVictoryType = utils.getReligiousVictoryType(iPlayer)
	
	if iVictoryType == -1: return -1
	
	#MacAurther TODO: Religious Victories?
	
	'''elif iVictoryType == iJudaism:
	
		# first Jewish goal: have a total of 15 Great Prophets, Scientists and Statesmen in Jewish cities
		if iGoal == 0:
			iProphets = countSpecialists(iJudaism, iSpecialistGreatProphet)
			iScientists = countSpecialists(iJudaism, iSpecialistGreatScientist)
			iStatesmen = countSpecialists(iJudaism, iSpecialistGreatStatesman)
			if iProphets + iScientists + iStatesmen >= 15: return 1
		
		# second Jewish goal: have legendary culture in the Jewish holy city
		elif iGoal == 1:
			pHolyCity = gc.getGame().getHolyCity(iJudaism)
			if pHolyCity.getOwner() == iPlayer and pHolyCity.getCultureLevel() >= 6: return 1
			
		# third Jewish goal: have friendly relations with six civilizations with Jewish minorities
		elif iGoal == 2:
			iFriendlyRelations = countPlayersWithAttitudeAndReligion(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY, iJudaism)
			if iFriendlyRelations >= 6: return 1
			
	elif iVictoryType == iOrthodoxy:
	
		# first Orthodox goal: build four Orthodox cathedrals
		if iGoal == 0:
			if getNumBuildings(iPlayer, iOrthodoxCathedral) >= 4: return 1
			
		# second Orthodox goal: make sure the five most cultured cities in the world are Orthodox
		elif iGoal == 1:
			if countBestCitiesReligion(iOrthodoxy, cityCulture, 5) >= 5: return 1
			
		# third Orthodox goal: make sure there are no Catholic civilizations in the world
		elif iGoal == 2:
			if countReligionPlayers(iCatholicism)[0] == 0: return 1
			
	elif iVictoryType == iCatholicism:
	
		# first Catholic goal: be pope for 100 turns
		if iGoal == 0:
			if data.iPopeTurns >= utils.getTurns(100): return 1
			
		# second Catholic goal: control the Catholic shrine and make sure 12 great prophets are settled in Catholic civilizations
		elif iGoal == 1:
			bShrine = getNumBuildings(iPlayer, iCatholicShrine) > 0
			iSaints = countReligionSpecialists(iCatholicism, iSpecialistGreatProphet)
			
			if bShrine and iSaints >= 12: return 1
			
		# third Catholic goal: make sure 50% of world territory is controlled by Catholic civilizations
		elif iGoal == 2:
			if getReligiousLand(iCatholicism) >= 50.0: return 1
	
	elif iVictoryType == iProtestantism:
		
		# first Protestant goal: be first to discover Civil Liberties, Constitution and Economics
		if iGoal == 0:
			lProtestantTechs = [iCivilLiberties, iSocialContract, iLogistics]
			if checkTechGoal(iPlayer, lProtestantTechs): return 1
			elif data.lFirstDiscovered[iCivilLiberties] not in [iPlayer, -1] or data.lFirstDiscovered[iSocialContract] not in [iPlayer, -1] or data.lFirstDiscovered[iLogistics] not in [iPlayer, -1]: return 0
			
		# second Protestant goal: make sure five great merchants and great engineers are settled in Protestant civilizations
		elif iGoal == 1:
			iEngineers = countReligionSpecialists(iProtestantism, iSpecialistGreatEngineer)
			iMerchants = countReligionSpecialists(iProtestantism, iSpecialistGreatMerchant)
			if iEngineers >= 5 and iMerchants >= 5: return 1
			
		# third Protestant goal: make sure at least half of all civilizations are Protestant or Secular
		elif iGoal == 2:
			iProtestantCivs, iTotal = countReligionPlayers(iProtestantism)
			iSecularCivs, iTotal = countCivicPlayers(iCivicsReligion, iSecularism)
			
			if 2 * (iProtestantCivs + iSecularCivs) >= iTotal: return 1
			
	elif iVictoryType == iIslam:
	
		# first Muslim goal: spread Islam to 40%
		if iGoal == 0:
			fReligionPercent = gc.getGame().calculateReligionPercent(iIslam)
			if fReligionPercent >= 40.0: return 1
			
		# second Muslim goal: settle seven great people in the Muslim holy city
		elif iGoal == 1:
			iCount = 0
			pHolyCity = gc.getGame().getHolyCity(iIslam)
			for iGreatPerson in lGreatPeople:
				iCount += pHolyCity.getFreeSpecialistCount(iGreatPerson)
			if iCount >= 7: return 1
			
		# third Muslim goal: control five shrines
		elif iGoal == 2:
			iCount = 0
			for iReligion in range(iNumReligions):
				iCount += getNumBuildings(iPlayer, iShrine + 4*iReligion)
			if iCount >= 5: return 1
			
	elif iVictoryType == iHinduism:
	
		# first Hindu goal: settle five different great people in the Hindu holy city
		if iGoal == 0:
			iCount = 0
			pHolyCity = gc.getGame().getHolyCity(iHinduism)
			for iGreatPerson in lGreatPeople:
				if pHolyCity.getFreeSpecialistCount(iGreatPerson) > 0:
					iCount += 1
			if iCount >= 5: return 1
		
		# second Hindu goal: experience 24 turns of golden age
		elif iGoal == 1:
			if data.iHinduGoldenAgeTurns >= utils.getTurns(24): return 1
			
		# third Hindu goal: make sure the five largest cities in the world are Hindu
		elif iGoal == 2:
			if countBestCitiesReligion(iHinduism, cityPopulation, 5) >= 5: return 1
			
	elif iVictoryType == iBuddhism:
	
		# first Buddhist goal: be at peace for 100 turns
		if iGoal == 0:
			if data.iBuddhistPeaceTurns >= utils.getTurns(100): return 1
			
		# second Buddhist goal: have the highest approval rating for 100 turns
		elif iGoal == 1:
			if data.iBuddhistHappinessTurns >= utils.getTurns(100): return 1
			
		# third Buddhist goal: have cautious or better relations with all civilizations in the world
		elif iGoal == 2:
			if countGoodRelationPlayers(iPlayer, AttitudeTypes.ATTITUDE_CAUTIOUS) >= countLivingPlayers()-1: return 1
			
	elif iVictoryType == iConfucianism:
	
		# first Confucian goal: have friendly relations with five civilizations
		if iGoal == 0:
			if countGoodRelationPlayers(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY) >= 5: return 1
			
		# second Confucian goal: have five wonders in the Confucian holy city
		elif iGoal == 1:
			pHolyCity = gc.getGame().getHolyCity(iConfucianism)
			if countCityWonders(iPlayer, (pHolyCity.getX(), pHolyCity.getY()), True) >= 5: return 1
			
		# third Confucian goal: control an army of 200 non-obsolete melee or gunpowder units
		elif iGoal == 2:
			iUnitCombatMelee = gc.getInfoTypeForString("UNITCOMBAT_MELEE")
			iUnitCombatGunpowder = gc.getInfoTypeForString("UNITCOMBAT_GUN")
			if countUnitsOfType(iPlayer, [iUnitCombatMelee, iUnitCombatGunpowder]) >= 200: return 1
			
	elif iVictoryType == iTaoism:
	
		# first Taoist goal: have the highest life expectancy in the world for 100 turns
		if iGoal == 0:
			if data.iTaoistHealthTurns >= utils.getTurns(100): return 1
			
		# second Taoist goal: control the Confucian and Taoist shrine and combine their income to 40 gold
		elif iGoal == 1:
			iConfucianIncome = calculateShrineIncome(iPlayer, iConfucianism)
			iTaoistIncome = calculateShrineIncome(iPlayer, iTaoism)
			if getNumBuildings(iPlayer, iConfucianShrine) > 0 and getNumBuildings(iPlayer, iTaoistShrine) > 0 and iConfucianIncome + iTaoistIncome >= 40: return 1
			
		# third Taoist goal: have legendary culture in the Tao holy city
		elif iGoal == 2:
			pHolyCity = gc.getGame().getHolyCity(iTaoism)
			if pHolyCity.getOwner() == iPlayer and pHolyCity.getCultureLevel() >= 6: return 1
		
	elif iVictoryType == iZoroastrianism:

		# first Zoroastrian goal: acquire six incense resources
		if iGoal == 0:
			if pPlayer.getNumAvailableBonuses(iIncense) >= 6: return 1
			
		# second Zoroastrian goal: spread Zoroastrianism to 10%
		if iGoal == 1:
			fReligionPercent = gc.getGame().calculateReligionPercent(iZoroastrianism)
			if fReligionPercent >= 10.0: return 1
			
		# third Zoroastrian goal: have legendary culture in the Zoroastrian holy city
		elif iGoal == 2:
			pHolyCity = gc.getGame().getHolyCity(iZoroastrianism)
			if pHolyCity.getOwner() == iPlayer and pHolyCity.getCultureLevel() >= 6: return 1
			
	elif iVictoryType == iVictoryPaganism:
	
		# first Pagan goal: make sure there are 15 pagan temples in the world
		if iGoal == 0:
			if countWorldBuildings(iPaganTemple) >= 15: return 1
			
		# second Pagan goal: depends on Pagan religion
		elif iGoal == 1:
			paganReligion = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getPaganReligionName(0)
			
			# Anunnaki: have more wonders in your capital than any other city in the world
			if paganReligion == "Anunnaki":
				capital = pPlayer.getCapitalCity()
				
				if capital and isBestCity(iPlayer, (capital.getX(), capital.getY()), cityWonders):
					return 1
					
			# Asatru: have five units of level five
			elif paganReligion == "Asatru":
				if countUnitsOfLevel(iPlayer, 5) >= 5:
					return 1
					
			# Atua: acquire four pearl resources and 50 Ocean tiles
			elif paganReligion == "Atua":
				if pPlayer.getNumAvailableBonuses(iPearls) >= 4 and countControlledTerrain(iPlayer, iOcean) >= 50:
					return 1
			
			# Baalism: make your capital the city with the highest trade income in the world
			elif paganReligion == "Baalism":
				capital = pPlayer.getCapitalCity()
				
				if capital and isBestCity(iPlayer, (capital.getX(), capital.getY()), cityTradeIncome):
					return 1
					
			# Druidism: control 20 unimproved Forest or Marsh tiles
			elif paganReligion == "Druidism":
				if countControlledFeatures(iPlayer, iForest, -1) + countControlledFeatures(iPlayer, iMud, -1) >= 20:
					return 1
					
			# Inti: have more gold in your treasury than the rest of the world combined
			elif paganReligion == "Inti":
				if 2 * pPlayer.getGold() >= getGlobalTreasury():
					return 1
					
			# Mazdaism: acquire six incense resources
			elif paganReligion == "Mazdaism":
				if pPlayer.getNumAvailableBonuses(iIncense) >= 6:
					return 1
					
			# Olympianism: control ten wonders that require no state religion
			elif paganReligion == "Olympianism":
				if countReligionWonders(iPlayer, -1) >= 10:
					return 1
					
			# Pesedjet: be the first to create to three different types of great person
			elif paganReligion == "Pesedjet":
				if countFirstGreatPeople(iPlayer) >= 3:
					return 1
				
			# Rodnovery: acquire seven fur resources
			elif paganReligion == "Rodnovery":
				if pPlayer.getNumAvailableBonuses(iFur) >= 7:
					return 1
					
			# Shendao: control 25% of the world's population
			elif paganReligion == "Shendao":
				if getPopulationPercent(iPlayer) >= 25.0:
					return 1
					
			# Shinto: settle three great spies in your capital
			elif paganReligion == "Shinto":
				capital = pPlayer.getCapitalCity()
				
				if capital and countCitySpecialists(iPlayer, (capital.getX(), capital.getY()), iSpecialistGreatSpy) >= 3:
					return 1
			
			# Tengri: acquire eight horse resources
			elif paganReligion == "Tengri":
				if pPlayer.getNumAvailableBonuses(iHorse) >= 8:
					return 1
				
			# Teotl: sacrifice ten slaves
			elif paganReligion == "Teotl":
				if data.iTeotlSacrifices >= 10:
					return 1
					
			# Vedism: have 100 turns of cities celebrating "We Love the King" day
			elif paganReligion == "Vedism":
				if data.iVedicHappiness >= 100:
					return 1
					
			# Yoruba: acquire eight ivory resources and six gem resources
			elif paganReligion == "Yoruba":
				if pPlayer.getNumAvailableBonuses(iIvory) >= 8 and pPlayer.getNumAvailableBonuses(iGems) >= 6:
					return 1
			
		# third Pagan goal: don't allow more than half of your cities to have a religion
		elif iGoal == 2:
			if data.bPolytheismNeverReligion: return 1
			
	elif iVictoryType == iVictorySecularism:
	
		# first Secular goal: control the cathedrals of every religion
		if iGoal == 0:
			iCount = 0
			for iReligion in range(iNumReligions):
				if getNumBuildings(iPlayer, iCathedral + 4*iReligion) > 0:
					iCount += 1
			if iCount >= iNumReligions: return 1
			
		# second Secular goal: make sure there are 25 universities, 10 Great Scientists and 10 Great Statesmen in secular civilizations
		elif iGoal == 1:
			iUniversities = countCivicBuildings(iCivicsReligion, iSecularism, iUniversity)
			iScientists = countCivicSpecialists(iCivicsReligion, iSecularism, iSpecialistGreatScientist)
			iStatesmen = countCivicSpecialists(iCivicsReligion, iSecularism, iSpecialistGreatStatesman)
			if iUniversities >= 25 and iScientists >= 10 and iStatesmen >= 10: return 1
			
		# third Secular goal: make sure the five most advanced civilizations are secular
		elif iGoal == 2:
			iCount = 0
			lAdvancedPlayers = utils.getSortedList([iLoopPlayer for iLoopPlayer in range(iNumPlayers) if gc.getPlayer(iLoopPlayer).isAlive() and not utils.isAVassal(iLoopPlayer)], lambda iLoopPlayer: gc.getTeam(iLoopPlayer).getTotalTechValue(), True)
			for iLoopPlayer in lAdvancedPlayers[:5]:
				if gc.getPlayer(iLoopPlayer).getCivics(iCivicsReligion) == iSecularism:
					iCount += 1
			if iCount >= 5: return 1'''
			
	return -1

### UTILITY METHODS ###

def lose(iPlayer, iGoal):
	data.players[iPlayer].lGoals[iGoal] = 0
	if utils.getHumanID() == iPlayer and gc.getGame().getGameTurn() > utils.getScenarioStartTurn() and AlertsOpt.isShowUHVFailPopup():
		utils.show(localText.getText("TXT_KEY_VICTORY_GOAL_FAILED_ANNOUNCE", (iGoal+1,)))
	
def win(iPlayer, iGoal):
	data.players[iPlayer].lGoals[iGoal] = 1
	data.players[iPlayer].lGoalTurns[iGoal] = gc.getGame().getGameTurn()
	checkHistoricalVictory(iPlayer)
	
def expire(iPlayer, iGoal):
	if isPossible(iPlayer, iGoal): lose(iPlayer, iGoal)
	
def isWon(iPlayer, iGoal):
	return data.players[iPlayer].lGoals[iGoal] == 1
	
def isLost(iPlayer, iGoal):
	return data.players[iPlayer].lGoals[iGoal] == 0
	
def isPossible(iPlayer, iGoal):
	return data.players[iPlayer].lGoals[iGoal] == -1
	
def loseAll(iPlayer):
	for i in range(3): data.players[iPlayer].lGoals[i] = 0
	
def countAchievedGoals(iPlayer):
	iCount = 0
	for i in range(3):
		if isWon(iPlayer, i): iCount += 1
	return iCount
	
def isFounded(iReligion):
	return data.lReligionFounder[iReligion] != -1
	
def isWonderBuilt(iWonder):
	return data.getWonderBuilder(iWonder) != -1
	
def isDiscovered(iTech):
	return data.lFirstDiscovered[iTech] != -1
	
def isEntered(iEra):
	return data.lFirstEntered[iEra] != -1
	
def isGreatPersonTypeBorn(iGreatPerson):
	if iGreatPerson not in lGreatPeopleUnits: return True
	return getFirstBorn(iGreatPerson) != -1
	
def getFirstBorn(iGreatPerson):
	if iGreatPerson not in lGreatPeopleUnits: return -1
	return data.lFirstGreatPeople[lGreatPeopleUnits.index(iGreatPerson)]
	
	
def getBestCity(iPlayer, tPlot, function):
	x, y = tPlot
	#if not gc.getMap().plot(x, y).isCity(): return None
	
	bestCity = gc.getMap().plot(x, y).getPlotCity()
	iBestValue = function(bestCity)
	
	for city in utils.getAllCities():
		if function(city) > iBestValue:
			bestCity = city
			iBestValue = function(city)
	
	return bestCity
	
def isBestCity(iPlayer, tPlot, function):
	x, y = tPlot
	city = getBestCity(iPlayer, tPlot, function)
	if not city: return False
	
	return (city.getOwner() == iPlayer and city.getX() == x and city.getY() == y)
	
def cityPopulation(city):
	if not city: return 0
	return city.getPopulation()
	
def cityCulture(city):
	if not city: return 0
	return city.getCulture(city.getOwner())
	
def cityWonders(city):
	if not city: return 0
	return len([iWonder for iWonder in lWonders if city.isHasRealBuilding(iWonder)])

def cityTradeIncome(city):
	if not city: return 0
	return city.getTradeYield(YieldTypes.YIELD_COMMERCE)
	
def cityHappiness(city):
	if not city: return 0
	
	iHappiness = 0
	iHappiness += city.happyLevel()
	iHappiness -= city.unhappyLevel(0)
	iHappiness += city.getPopulation()
	
	return iHappiness
	
def getBestPlayer(iPlayer, function):
	iBestPlayer = iPlayer
	iBestValue = function(iPlayer)
	
	for iLoopPlayer in range(iNumPlayers):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			if function(iLoopPlayer) > iBestValue:
				iBestPlayer = iLoopPlayer
				iBestValue = function(iLoopPlayer)
				
	return iBestPlayer
	
def isBestPlayer(iPlayer, function):
	return getBestPlayer(iPlayer, function) == iPlayer
	
def playerTechs(iPlayer):
	iValue = 0
	for iTech in range(iNumTechs):
		if gc.getTeam(iPlayer).isHasTech(iTech):
			iValue += gc.getTechInfo(iTech).getResearchCost()
	return iValue
	
def playerRealPopulation(iPlayer):
	return gc.getPlayer(iPlayer).getRealPopulation()
	
def getNumBuildings(iPlayer, iBuilding):
	return gc.getPlayer(iPlayer).countNumBuildings(iBuilding)
	
def getPopulationPercent(iPlayer):
	iTotalPopulation = gc.getGame().getTotalPopulation()
	iOurPopulation = gc.getTeam(iPlayer).getTotalPopulation()
	
	if iTotalPopulation <= 0: return 0.0
	
	return iOurPopulation * 100.0 / iTotalPopulation
	
def getLandPercent(iPlayer):
	iTotalLand = gc.getMap().getLandPlots()
	iOurLand = gc.getPlayer(iPlayer).getTotalLand()
	
	if iTotalLand <= 0: return 0.0
	
	return iOurLand * 100.0 / iTotalLand
	
def getReligionLandPercent(iReligion):
	fPercent = 0.0
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive() and pPlayer.getStateReligion() == iReligion:
			fPercent += getLandPercent(iPlayer)
	return fPercent
	
def isBuildingInCity(tPlot, iBuilding):
	x, y = tPlot
	plot = gc.getMap().plot(x, y)
	
	if not plot.isCity(): return False
	
	return plot.getPlotCity().isHasRealBuilding(iBuilding)
	
def getNumCitiesInArea(iPlayer, lPlots):
	return len(utils.getAreaCitiesCiv(iPlayer, lPlots))
	
def getNumCitiesInRegions(iPlayer, lRegions):
	return len([city for city in utils.getCityList(iPlayer) if city.getRegionID() in lRegions])
	
def getNumFoundedCitiesInArea(iPlayer, lPlots):
	return len([city for city in utils.getAreaCitiesCiv(iPlayer, lPlots) if city.getOriginalOwner() == iPlayer])
	
def getNumConqueredCitiesInArea(iPlayer, lPlots):
	return len([city for city in utils.getAreaCitiesCiv(iPlayer, lPlots) if city.getOriginalOwner() != iPlayer])
	
def checkOwnedCiv(iPlayer, iOwnedPlayer):
	iPlayerCities = getNumCitiesInArea(iPlayer, Areas.getNormalArea(iOwnedPlayer, False))
	iOwnedCities = getNumCitiesInArea(iOwnedPlayer, Areas.getNormalArea(iOwnedPlayer, False))
	
	return (iPlayerCities >= 2 and iPlayerCities > iOwnedCities) or (iPlayerCities >= 1 and not gc.getPlayer(iOwnedPlayer).isAlive())
	
def isControlled(iPlayer, lPlots):
	lOwners = []
	for city in utils.getAreaCities(lPlots):
		iOwner = city.getOwner()
		if iOwner not in lOwners and iOwner < iNumPlayers:
			lOwners.append(iOwner)
	
	return iPlayer in lOwners and len(lOwners) == 1
	
def isControlledOrVassalized(iPlayer, lPlots):
	bControlled = False
	lOwners = []
	lValidOwners = [iPlayer]
	for city in utils.getAreaCities(lPlots):
		iOwner = city.getOwner()
		if iOwner not in lOwners and iOwner < iNumPlayers:
			lOwners.append(iOwner)
	for iLoopPlayer in range(iNumPlayers):
		if gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isVassal(iPlayer):
			lValidOwners.append(iLoopPlayer)
	for iLoopPlayer in lValidOwners:
		if iLoopPlayer in lOwners:
			bControlled = True
			lOwners.remove(iLoopPlayer)
	if lOwners:
		bControlled = False
	return bControlled
	
def isCoreControlled(iPlayer, lOtherPlayers):
	for iOtherPlayer in lOtherPlayers:
		if checkOwnedCiv(iPlayer, iOtherPlayer):
			return True
	return False
	
def countControlledTiles(iPlayer, tTopLeft, tBottomRight, bVassals=False, lExceptions=[], bCoastalOnly=False):
	lValidOwners = [iPlayer]
	iCount = 0
	iTotal = 0
	
	if bVassals:
		for iLoopPlayer in range(iNumPlayers):
			if gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isVassal(iPlayer):
				lValidOwners.append(iLoopPlayer)
				
	for (x, y) in utils.getPlotList(tTopLeft, tBottomRight, lExceptions):
		plot = gc.getMap().plot(x, y)
		if plot.isWater(): continue
		if bCoastalOnly and not plot.isCoastalLand(): continue
		iTotal += 1
		if plot.getOwner() in lValidOwners: iCount += 1
		
	return iCount, iTotal
	
def countWonders(iPlayer):
	iCount = 0
	for iWonder in range(iBeginWonders, iNumBuildings):
		iCount += getNumBuildings(iPlayer, iWonder)
	return iCount
	
def countShrines(iPlayer):
	iCount = 0
	for iReligion in range(iNumReligions):
		iCurrentShrine = iShrine + iReligion * 4
		iCount += getNumBuildings(iPlayer, iCurrentShrine)
	return iCount
	
def countOpenBorders(iPlayer, lContacts = [i for i in range(iNumPlayers)]):
	tPlayer = gc.getTeam(iPlayer)
	iCount = 0
	for iContact in lContacts:
		if tPlayer.isOpenBorders(iContact):
			iCount += 1
	return iCount
	
def getMostCulturedCity(iPlayer):
	return utils.getHighestEntry(utils.getCityList(iPlayer), lambda x: x.getCulture(iPlayer))

def isAreaFreeOfCivs(lPlots, lCivs):
	for city in utils.getAreaCities(lPlots):
		if city.getOwner() in lCivs: return False
	return True
	
def isAreaOnlyCivs(tTopLeft, tBottomRight, lCivs):
	for city in utils.getAreaCities(utils.getPlotList(tTopLeft, tBottomRight)):
		iOwner = city.getOwner()
		if iOwner < iNumPlayers and iOwner not in lCivs: return False
	return True
	
def countCitySpecialists(iPlayer, tPlot, iSpecialist):
	x, y = tPlot
	plot = gc.getMap().plot(x, y)
	if not plot.isCity(): return 0
	if plot.getPlotCity().getOwner() != iPlayer: return 0
	
	return plot.getPlotCity().getFreeSpecialistCount(iSpecialist)
	
def countSpecialists(iPlayer, iSpecialist):
	iCount = 0
	for city in utils.getCityList(iPlayer):
		iCount += countCitySpecialists(iPlayer, (city.getX(), city.getY()), iSpecialist)
	return iCount
	
def countReligionSpecialists(iReligion, iSpecialist):
	iCount = 0
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive() and pPlayer.getStateReligion() == iReligion:
			iCount += countSpecialists(iPlayer, iSpecialist)
	return iCount
	
def countCivicSpecialists(iCategory, iCivic, iSpecialist):
	iCount = 0
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive() and pPlayer.getCivics(iCategory) == iCivic:
			iCount += countSpecialists(iPlayer, iSpecialist)
	return iCount
	
def getAverageCitySize(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iNumCities = pPlayer.getNumCities()
	
	if iNumCities == 0: return 0.0
	
	return pPlayer.getTotalPopulation() * 1.0 / iNumCities
	
def getAverageCulture(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iNumCities = pPlayer.getNumCities()
	
	if iNumCities == 0: return 0
	
	return pPlayer.countTotalCulture() / iNumCities
	
def countHappinessResources(iPlayer):
	iCount = 0
	pPlayer = gc.getPlayer(iPlayer)
	for iBonus in range(iNumBonuses):
		if gc.getBonusInfo(iBonus).getHappiness() > 0:
			if pPlayer.getNumAvailableBonuses(iBonus) > 0:
				iCount += 1
	return iCount
	
def countResources(iPlayer, iBonus):
	iNumBonus = 0
	pPlayer = gc.getPlayer(iPlayer)
	
	iNumBonus += pPlayer.getNumAvailableBonuses(iBonus)
	iNumBonus -= pPlayer.getBonusImport(iBonus)
	
	for iLoopPlayer in range(iNumPlayers):
		if iLoopPlayer != iPlayer:
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if pLoopPlayer.isAlive() and gc.getTeam(pLoopPlayer.getTeam()).isVassal(iPlayer):
				iNumBonus += pLoopPlayer.getNumAvailableBonuses(iBonus)
				iNumBonus -= pLoopPlayer.getBonusImport(iBonus)
				
	return iNumBonus
	
def isStateReligionInArea(iReligion, tTopLeft, tBottomRight):
	lPlots = utils.getPlotList(tTopLeft, tBottomRight)
	
	for iPlayer in range(iNumPlayers):
		if gc.getPlayer(iPlayer).getStateReligion() == iReligion:
			for city in utils.getCityList(iPlayer):
				if (city.getX(), city.getY()) in utils.getPlotList(tTopLeft, tBottomRight):
					return True
					
	return False
	
def getCityCulture(iPlayer, tPlot):
	x, y = tPlot
	plot = gc.getMap().plot(x, y)
	if not plot.isCity(): return 0
	if plot.getPlotCity().getOwner() != iPlayer: return 0
	
	return plot.getPlotCity().getCulture(iPlayer)
	
def isConnected(tStart, lTargets, plotFunction):
	if not lTargets: return False
	if not plotFunction(tStart): return False
	
	if tStart in lTargets: return True
	if not [tTarget for tTarget in lTargets if plotFunction(tTarget)]: return False
	
	lNodes = [(utils.minimalDistance(tStart, lTargets, plotFunction), tStart)]
	heapq.heapify(lNodes)
	lVisitedNodes = []
	
	while lNodes:
		h, tNode = heapq.heappop(lNodes)
		lVisitedNodes.append((h, tNode))
		
		for tPlot in utils.surroundingPlots(tNode):
			if plotFunction(tPlot):
				if tPlot in lTargets: return True
				
				tTuple = (utils.minimalDistance(tPlot, lTargets, plotFunction), tPlot)
				if not tTuple in lVisitedNodes and not tTuple in lNodes:
					heapq.heappush(lNodes, tTuple)
							
	return False
	
def isConnectedByTradeRoute(iPlayer, lStarts, lTargets):
	for tStart in lStarts:
		startPlot = utils.plot(tStart)
		if not startPlot.isCity(): continue
		
		plotFunction = lambda tPlot: utils.plot(tPlot).getOwner() in [iPlayer, startPlot.getOwner()] and (utils.plot(tPlot).isCity() or utils.plot(tPlot).getRouteType() in [iRouteRoad, iRouteRailroad, iRouteRomanRoad, iRouteHighway])
	
		if isConnected(tStart, lTargets, plotFunction): return True
		
	return False
	
def isConnectedByRailroad(iPlayer, tStart, lTargets):
	if not gc.getTeam(iPlayer).isHasTech(iRailroad): return False
	
	startPlot = utils.plot(tStart)
	if not (startPlot.isCity() and startPlot.getOwner() == iPlayer): return False
	
	plotFunction = lambda tPlot: utils.plot(tPlot).getOwner() == iPlayer and (utils.plot(tPlot).isCity() or utils.plot(tPlot).getRouteType() == iRouteRailroad)
	
	return isConnected(tStart, lTargets, plotFunction)

def countPlayersWithAttitudeAndCriteria(iPlayer, eAttitude, function):
	return len([iOtherPlayer for iOtherPlayer in range(iNumPlayers) if gc.getPlayer(iPlayer).canContact(iOtherPlayer) and gc.getPlayer(iOtherPlayer).AI_getAttitude(iPlayer) >= eAttitude and function(iOtherPlayer)])
	
def countPlayersWithAttitudeAndReligion(iPlayer, eAttitude, iReligion):
	iCount = 0
	for iLoopPlayer in range(iNumPlayers):
		if iLoopPlayer == iPlayer: continue
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.AI_getAttitude(iPlayer) >= eAttitude:
			for city in utils.getCityList(iLoopPlayer):
				if city.isHasReligion(iReligion):
					iCount += 1
					break
	return iCount
	
def countPlayersWithAttitudeInGroup(iPlayer, eAttitude, lOtherPlayers):
	return countPlayersWithAttitudeAndCriteria(iPlayer, eAttitude, lambda x: not gc.getTeam(gc.getPlayer(x).getTeam()).isAVassal())
	
def getLargestCities(iPlayer, iNumCities):
	lCities = utils.getSortedList(utils.getCityList(iPlayer), lambda x: x.getPopulation(), True)
	return lCities[:iNumCities]
	
def countCitiesOfSize(iPlayer, iThreshold):
	iCount = 0
	for city in utils.getCityList(iPlayer):
		if city.getPopulation() >= iThreshold:
			iCount += 1
	return iCount
	
def countCitiesWithCultureLevel(iPlayer, iThreshold):
	iCount = 0
	for city in utils.getCityList(iPlayer):
		if city.getCultureLevel() >= iThreshold:
			iCount += 1
	return iCount
	
def countAcquiredResources(iPlayer, lResources):
	iCount = 0
	pPlayer = gc.getPlayer(iPlayer)
	for iBonus in lResources:
		iCount += pPlayer.getNumAvailableBonuses(iBonus)
	return iCount
	
def isRoad(iPlayer, lPlots):
	iRoad = gc.getInfoTypeForString("ROUTE_ROAD")
	
	for tPlot in lPlots:
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		if plot.getOwner() != iPlayer: return False
		if not plot.getRouteType() == iRoad and not plot.isCity(): return False
		
	return True
	
def countCityWonders(iPlayer, tPlot, bIncludeObsolete=False):
	iCount = 0
	x, y = tPlot
	plot = gc.getMap().plot(x, y)
	if not plot.isCity(): return 0
	if plot.getPlotCity().getOwner() != iPlayer: return 0
	
	for iWonder in lWonders:
		iObsoleteTech = gc.getBuildingInfo(iWonder).getObsoleteTech()
		if not bIncludeObsolete and iObsoleteTech != -1 and gc.getTeam(iPlayer).isHasTech(iObsoleteTech): continue
		if plot.getPlotCity().isHasRealBuilding(iWonder): iCount += 1
		
	return iCount
	
def isCultureControlled(iPlayer, lPlots):
	for tPlot in lPlots:
		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		if plot.getOwner() != -1 and plot.getOwner() != iPlayer:
			return False
	return True
	
def controlsCity(iPlayer, tPlot):
	for (x, y) in utils.surroundingPlots(tPlot):
		plot = gc.getMap().plot(x, y)
		if plot.isCity() and plot.getPlotCity().getOwner() == iPlayer:
			return True
	return False
	
def getTotalCulture(lPlayers):
	iTotalCulture = 0
	for iPlayer in lPlayers:
		iTotalCulture += gc.getPlayer(iPlayer).countTotalCulture()
	return iTotalCulture
	
def countImprovements(iPlayer, iImprovement):
	if iImprovement <= 0: return 0
	return gc.getPlayer(iPlayer).getImprovementCount(iImprovement)
	
def controlsAllCities(iPlayer, tTopLeft, tBottomRight, tExceptions=()):
	for city in utils.getAreaCities(utils.getPlotList(tTopLeft, tBottomRight, tExceptions)):
		if city.getOwner() != iPlayer: return False
	return True
	
def isAtPeace(iPlayer):
	for iLoopPlayer in range(iNumPlayers):
		if gc.getPlayer(iLoopPlayer).isAlive() and gc.getTeam(iPlayer).isAtWar(iLoopPlayer):
			return False
	return True
	
def getHappiest():
	lApprovalList = [utils.getApprovalRating(i) for i in range(iNumPlayers)]
	return utils.getHighestIndex(lApprovalList)
	
def isHappiest(iPlayer):
	return getHappiest() == iPlayer
	
def getHealthiest():
	lLifeExpectancyList = [utils.getLifeExpectancyRating(i) for i in range(iNumPlayers)]
	return utils.getHighestIndex(lLifeExpectancyList)
	
def isHealthiest(iPlayer):
	return getHealthiest() == iPlayer
	
def countReligionCities(iPlayer):
	iCount = 0
	for city in utils.getCityList(iPlayer):
		if city.getReligionCount() > 0:
			iCount += 1
	return iCount
	
def isCompleteTechTree(iPlayer):
	if gc.getPlayer(iPlayer).getCurrentEra() < iInformationEra: return False
	
	tPlayer = gc.getTeam(iPlayer)
	for iTech in range(iNumTechs):
		if not (tPlayer.isHasTech(iTech) or tPlayer.getTechCount(iTech) > 0): return False
		
	return True
	
def countFirstDiscovered(iPlayer, iEra):
	iCount = 0
	for iTech in range(iNumTechs):
		if gc.getTechInfo(iTech).getEra() == iEra and data.lFirstDiscovered[iTech] == iPlayer:
			iCount += 1
	return iCount
	
def isFirstDiscoveredPossible(iPlayer, iEra, iRequired):
	iCount = countFirstDiscovered(iPlayer, iEra)
	iNotYetDiscovered = countFirstDiscovered(-1, iEra)
	return iCount + iNotYetDiscovered >= iRequired
	
def isWonder(iBuilding):
	return iBeginWonders <= iBuilding < iNumBuildings
	
def countReligionPlayers(iReligion):
	iReligionPlayers = 0
	iTotalPlayers = 0
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			iTotalPlayers += 1
			if pPlayer.getStateReligion() == iReligion:
				iReligionPlayers += 1
	return iReligionPlayers, iTotalPlayers
	
def countCivicPlayers(iCivicType, iCivic):
	iCivicPlayers = 0
	iTotalPlayers = 0
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			iTotalPlayers += 1
			if pPlayer.getCivics(iCivicType) == iCivic:
				iCivicPlayers += 1
	return iCivicPlayers, iTotalPlayers
	
def getBestCities(function):
	lCities = []
	for iLoopPlayer in range(iNumPlayers):
		lCities.extend(utils.getCityList(iLoopPlayer))
	
	return utils.getSortedList(lCities, function, True)
	
def countBestCitiesReligion(iReligion, function, iNumCities):
	lCities = getBestCities(function)
	
	iCount = 0
	for city in lCities[:iNumCities]:
		if city.isHasReligion(iReligion) and gc.getPlayer(city.getOwner()).getStateReligion() == iReligion:
			iCount += 1
			
	return iCount
	
def getReligiousLand(iReligion):
	fLandPercent = 0.0
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive() and pPlayer.getStateReligion() == iReligion:
			fLandPercent += getLandPercent(iPlayer)
	return fLandPercent
	
def countLivingPlayers():
	iCount = 0
	for iPlayer in range(iNumPlayers):
		if gc.getPlayer(iPlayer).isAlive():
			iCount += 1
	return iCount
	
def countGoodRelationPlayers(iPlayer, iAttitudeThreshold):
	iCount = 0
	tPlayer = gc.getTeam(iPlayer)
	for iLoopPlayer in range(iNumPlayers):
		if iPlayer != iLoopPlayer and tPlayer.isHasMet(iLoopPlayer):
			if gc.getPlayer(iLoopPlayer).AI_getAttitude(iPlayer) >= iAttitudeThreshold:
				iCount += 1
	return iCount
	
def countUnitsOfType(iPlayer, lTypes, bIncludeObsolete=False):
	iCount = 0
	pPlayer = gc.getPlayer(iPlayer)
	for iUnit in range(iNumUnits):
		if bIncludeObsolete or pPlayer.canTrain(iUnit, False, False):
			if gc.getUnitInfo(iUnit).getUnitCombatType() in lTypes:
				iUnitClass = gc.getUnitInfo(iUnit).getUnitClassType()
				iCount += pPlayer.getUnitClassCount(iUnitClass)
	return iCount
	
def calculateShrineIncome(iPlayer, iReligion):
	if getNumBuildings(iPlayer, iShrine  + 4*iReligion) == 0: return 0
	
	iThreshold = 20
	if getNumBuildings(iPlayer, iDomeOfTheRock) > 0 and not gc.getTeam(iPlayer).isHasTech(iLiberalism): iThreshold = 40
	
	return min(iThreshold, gc.getGame().countReligionLevels(iReligion))
	
def countWorldBuildings(iBuilding):
	iCount = 0
	for iPlayer in range(iNumPlayers):
		if gc.getPlayer(iPlayer).isAlive():
			iCount += getNumBuildings(iPlayer, utils.getUniqueBuilding(iPlayer, iBuilding))
	return iCount
	
def countReligionWonders(iPlayer, iReligion):
	iCount = 0
	for iWonder in lWonders:
		if gc.getBuildingInfo(iWonder).getPrereqReligion() == iReligion and getNumBuildings(iPlayer, iWonder) > 0:
			iCount += 1
	return iCount
	
def countCivicBuildings(iCivicType, iCivic, iBuilding):
	iCount = 0
	for iPlayer in range(iNumPlayers):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive() and pPlayer.getCivics(iCivicType) == iCivic:
			iCount += getNumBuildings(iPlayer, utils.getUniqueBuilding(iPlayer, iBuilding))
	return iCount
	
def getApostolicVotePercent(iPlayer):
	iTotal = 0
	for iLoopPlayer in range(iNumPlayers):
		iTotal += gc.getPlayer(iLoopPlayer).getVotes(16, 1)
		
	if iTotal == 0: return 0.0
	
	return gc.getPlayer(iPlayer).getVotes(16, 1) * 100.0 / iTotal
	
def countNativeCulture(iPlayer, iPercent):
	iPlayerCulture = 0
	
	for city in utils.getCityList(iPlayer):
		iCulture = city.getCulture(iPlayer)
		iTotal = 0
		
		for iLoopPlayer in range(iNumTotalPlayersB): iTotal += city.getCulture(iLoopPlayer)
		
		if iTotal > 0 and iCulture * 100 / iTotal >= iPercent:
			iPlayerCulture += iCulture
			
	return iPlayerCulture
	
def isTradeConnected(iPlayer):
	for iOtherPlayer in range(iNumPlayers):
		if iPlayer != iOtherPlayer and gc.getPlayer(iPlayer).canContact(iOtherPlayer) and gc.getPlayer(iPlayer).canTradeNetworkWith(iOtherPlayer):
			return True
			
	return False
	
def countUnitsOfLevel(iPlayer, iLevel):
	pPlayer = gc.getPlayer(iPlayer)
	iCount = 0
	
	for iUnit in range(pPlayer.getNumUnits()):
		unit = pPlayer.getUnit(iUnit)
		if unit.getLevel() >= iLevel:
			iCount += 1
			
	return iCount
	
def countControlledTerrain(iPlayer, iTerrain):
	iCount = 0
	
	for (x, y) in utils.getWorldPlotsList():
		plot = gc.getMap().plot(x, y)
		if plot.getOwner() == iPlayer and plot.getTerrainType() == iTerrain:
			iCount += 1
			
	return iCount
	
def countControlledFeatures(iPlayer, iFeature, iImprovement):
	iCount = 0
	
	for (x, y) in utils.getWorldPlotsList():
		plot = gc.getMap().plot(x, y)
		if plot.getOwner() == iPlayer and plot.getFeatureType() == iFeature and plot.getImprovementType() == iImprovement:
			iCount += 1
			
	return iCount
	
def getGlobalTreasury():
	iTreasury = 0

	for iPlayer in range(iNumPlayers):
		iTreasury += gc.getPlayer(iPlayer).getGold()
		
	return iTreasury
	
def countFirstGreatPeople(iPlayer):
	return len([iGreatPerson for iGreatPerson in lGreatPeopleUnits if getFirstBorn(iGreatPerson) == iPlayer])
	
def countReligionSpecialistCities(iPlayer, iReligion, iSpecialist):
	iCount = 0
	for city in utils.getCityList(iPlayer):
		if city.isHasReligion(iReligion) and city.getFreeSpecialistCount(iSpecialist) > 0:
			iCount += 1
	return iCount
	
def calculateAlliedPercent(iPlayer, function):
	pTeam = gc.getTeam(gc.getPlayer(iPlayer).getTeam())

	iAlliedValue = 0
	iTotalValue = 0
	
	for iLoopPlayer in range(iNumPlayers):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		pLoopTeam = gc.getTeam(pLoopPlayer.getTeam())
		
		if not pLoopPlayer.isAlive(): continue
		
		iValue = function(iLoopPlayer)
		
		iTotalValue += iValue
		
		if iLoopPlayer == iPlayer or pLoopTeam.isVassal(gc.getPlayer(iPlayer).getTeam()) or pTeam.isDefensivePact(pLoopPlayer.getTeam()):
			iAlliedValue += iValue
			
	if iTotalValue == 0: return 0
	
	return 100.0 * iAlliedValue / iTotalValue
	
def calculateAlliedCommercePercent(iPlayer):
	return calculateAlliedPercent(iPlayer, lambda x: gc.getPlayer(x).calculateTotalCommerce())
	
def calculateAlliedPowerPercent(iPlayer):
	return calculateAlliedPercent(iPlayer, lambda x: gc.getPlayer(x).getPower())
	
def countRegionReligion(iReligion, lRegions):
	lCities = [gc.getMap().plot(x, y).getPlotCity() for (x, y) in utils.getRegionPlots(lRegions) if gc.getMap().plot(x, y).isCity()]
	return len([city for city in lCities if city.isHasReligion(iReligion)])
	
def findBestCityWith(iPlayer, filter, sort):
	lCities = [city for city in utils.getCityList(iPlayer) if filter(city)]
	return utils.getHighestEntry(lCities, sort)
	
def countVassals(iPlayer, lPlayers=None, iReligion=-1):
	lVassals = [iVassal for iVassal in range(iNumPlayers) if gc.getTeam(iVassal).isVassal(iPlayer) and (not lPlayers or iVassal in lPlayers) and (iReligion < 0 or gc.getPlayer(iVassal).getStateReligion() == iReligion)]
	return len(lVassals)
	
### UHV HELP SCREEN ###

def getIcon(bVal):
	if bVal:
		return u"%c" %(CyGame().getSymbolID(FontSymbols.SUCCESS_CHAR))
	else:
		return u"%c" %(CyGame().getSymbolID(FontSymbols.FAILURE_CHAR))

def getURVHelp(iPlayer, iGoal):
	pPlayer = gc.getPlayer(iPlayer)
	iVictoryType = utils.getReligiousVictoryType(iPlayer)
	aHelp = []

	if checkReligiousGoal(iPlayer, iGoal) == 1:
		aHelp.append(getIcon(True) + localText.getText("TXT_KEY_VICTORY_GOAL_ACCOMPLISHED", ()))
		return aHelp
	elif checkReligiousGoal(iPlayer, iGoal) == 0:
		aHelp.append(getIcon(False) + localText.getText("TXT_KEY_VICTORY_GOAL_FAILED", ()))
		return aHelp
	
	# MacAurther TODO: Religious Victories?
	
	'''if iVictoryType == iJudaism:
		if iGoal == 0:
			iProphets = countSpecialists(iPlayer, iSpecialistGreatProphet)
			iScientists = countSpecialists(iPlayer, iSpecialistGreatScientist)
			iStatesmen = countSpecialists(iPlayer, iSpecialistGreatStatesman)
			aHelp.append(getIcon(iProphets + iScientists + iStatesmen) + localText.getText("TXT_KEY_VICTORY_JEWISH_SPECIALISTS", (iProphets + iScientists + iStatesmen, 15)))
		elif iGoal == 1:
			holyCity = gc.getGame().getHolyCity(iJudaism)
			aHelp.append(getIcon(holyCity.getOwner() == iPlayer) + localText.getText("TXT_KEY_VICTORY_CONTROL_HOLY_CITY", (holyCity.getName(),)) + ' ' + getIcon(holyCity.getCultureLevel() >= 6) + localText.getText("TXT_KEY_VICTORY_LEGENDARY_CULTURE_CITY", (holyCity.getName(),)))
		elif iGoal == 2:
			iFriendlyRelations = countPlayersWithAttitudeAndReligion(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY, iJudaism)
			aHelp.append(getIcon(iFriendlyRelations >= 6) + localText.getText("TXT_KEY_VICTORY_FRIENDLY_RELIGION", (gc.getReligionInfo(iJudaism).getAdjectiveKey(), iFriendlyRelations, 6)))

	elif iVictoryType == iOrthodoxy:
		if iGoal == 0:
			iOrthodoxCathedrals = getNumBuildings(iPlayer, iOrthodoxCathedral)
			aHelp.append(getIcon(iOrthodoxCathedrals >= 4) + localText.getText("TXT_KEY_VICTORY_ORTHODOX_CATHEDRALS", (iOrthodoxCathedrals, 4)))
		elif iGoal == 1:
			lCultureCities = getBestCities(cityCulture)[:5]
			iCultureCities = countBestCitiesReligion(iOrthodoxy, cityCulture, 5)
			for city in lCultureCities:
				aHelp.append(getIcon(city.isHasReligion(iOrthodoxy) and gc.getPlayer(city.getOwner()).getStateReligion() == iOrthodoxy) + city.getName())
		elif iGoal == 2:
			bNoCatholics = countReligionPlayers(iCatholicism)[0] == 0
			aHelp.append(getIcon(bNoCatholics) + localText.getText("TXT_KEY_VICTORY_NO_CATHOLICS", ()))

	elif iVictoryType == iCatholicism:
		if iGoal == 0:
			iPopeTurns = data.iPopeTurns
			aHelp.append(getIcon(iPopeTurns >= utils.getTurns(100)) + localText.getText("TXT_KEY_VICTORY_POPE_TURNS", (iPopeTurns, utils.getTurns(100))))
		elif iGoal == 1:
			bShrine = pPlayer.countNumBuildings(iCatholicShrine) > 0
			iSaints = countReligionSpecialists(iCatholicism, iSpecialistGreatProphet)
			aHelp.append(getIcon(bShrine) + localText.getText("TXT_KEY_BUILDING_CATHOLIC_SHRINE", ()) + ' ' + getIcon(iSaints >= 12) + localText.getText("TXT_KEY_VICTORY_CATHOLIC_SAINTS", (iSaints, 12)))
		elif iGoal == 2:
			fLandPercent = getReligiousLand(iCatholicism)
			aHelp.append(getIcon(fLandPercent >= 50.0) + localText.getText("TXT_KEY_VICTORY_CATHOLIC_WORLD_TERRITORY", (str(u"%.2f%%" % fLandPercent), str(50))))

	elif iVictoryType == iProtestantism:
		if iGoal == 0:
			bCivilLiberties = data.lFirstDiscovered[iCivilLiberties] == iPlayer
			bConstitution = data.lFirstDiscovered[iSocialContract] == iPlayer
			bEconomics = data.lFirstDiscovered[iEconomics] == iPlayer
			aHelp.append(getIcon(bCivilLiberties) + localText.getText("TXT_KEY_TECH_CIVIL_LIBERTIES", ()) + ' ' + getIcon(bConstitution) + localText.getText("TXT_KEY_TECH_CONSTITUTION", ()) + ' ' + getIcon(bEconomics) + localText.getText("TXT_KEY_TECH_ECONOMICS", ()))
		elif iGoal == 1:
			iMerchants = countReligionSpecialists(iProtestantism, iSpecialistGreatMerchant)
			iEngineers = countReligionSpecialists(iProtestantism, iSpecialistGreatEngineer)
			aHelp.append(getIcon(iMerchants >= 5) + localText.getText("TXT_KEY_VICTORY_PROTESTANT_MERCHANTS", (iMerchants, 5)) + ' ' + getIcon(iEngineers >= 5) + localText.getText("TXT_KEY_VICTORY_PROTESTANT_ENGINEERS", (iEngineers, 5)))
		elif iGoal == 2:
			iProtestantCivs, iTotal = countReligionPlayers(iProtestantism)
			iSecularCivs, iTotal = countCivicPlayers(iCivicsReligion, iSecularism)
			iNumProtestantCivs = iProtestantCivs + iSecularCivs
			aHelp.append(getIcon(2 * iNumProtestantCivs >= iTotal) + localText.getText("TXT_KEY_VICTORY_PROTESTANT_CIVS", (iNumProtestantCivs, iTotal)))

	elif iVictoryType == iIslam:
		if iGoal == 0:
			fReligionPercent = gc.getGame().calculateReligionPercent(iIslam)
			aHelp.append(getIcon(fReligionPercent >= 40.0) + localText.getText("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", (gc.getReligionInfo(iIslam).getTextKey(), str(u"%.2f%%" % fReligionPercent), str(40))))
		elif iGoal == 1:
			iCount = 0
			pHolyCity = gc.getGame().getHolyCity(iIslam)
			for iGreatPerson in lGreatPeople:
				iCount += pHolyCity.getFreeSpecialistCount(iGreatPerson)
			aHelp.append(getIcon(iCount >= 7) + localText.getText("TXT_KEY_VICTORY_CITY_GREAT_PEOPLE", (gc.getGame().getHolyCity(iIslam).getName(), iCount, 7)))
		elif iGoal == 2:
			iCount = 0
			for iReligion in range(iNumReligions):
				iCount += getNumBuildings(iPlayer, iShrine + 4*iReligion)
			aHelp.append(getIcon(iCount >= 5) + localText.getText("TXT_KEY_VICTORY_NUM_SHRINES", (iCount, 5)))

	elif iVictoryType == iHinduism:
		if iGoal == 0:
			iCount = 0
			pHolyCity = gc.getGame().getHolyCity(iHinduism)
			for iGreatPerson in lGreatPeople:
				if pHolyCity.getFreeSpecialistCount(iGreatPerson) > 0:
					iCount += 1
			aHelp.append(getIcon(iCount >= 5) + localText.getText("TXT_KEY_VICTORY_CITY_DIFFERENT_GREAT_PEOPLE", (gc.getGame().getHolyCity(iHinduism).getName(), iCount, 5)))
		elif iGoal == 1:
			iGoldenAgeTurns = data.iHinduGoldenAgeTurns
			aHelp.append(getIcon(iGoldenAgeTurns >= utils.getTurns(24)) + localText.getText("TXT_KEY_VICTORY_GOLDEN_AGE_TURNS", (iGoldenAgeTurns, utils.getTurns(24))))
		elif iGoal == 2:
			iLargestCities = countBestCitiesReligion(iHinduism, cityPopulation, 5)
			aHelp.append(getIcon(iLargestCities >= 5) + localText.getText("TXT_KEY_VICTORY_HINDU_LARGEST_CITIES", (iLargestCities, 5)))

	elif iVictoryType == iBuddhism:
		if iGoal == 0:
			iPeaceTurns = data.iBuddhistPeaceTurns
			aHelp.append(getIcon(iPeaceTurns >= utils.getTurns(100)) + localText.getText("TXT_KEY_VICTORY_PEACE_TURNS", (iPeaceTurns, utils.getTurns(100))))
		elif iGoal == 1:
			iHappinessTurns = data.iBuddhistHappinessTurns
			aHelp.append(getIcon(iHappinessTurns >= utils.getTurns(100)) + localText.getText("TXT_KEY_VICTORY_HAPPINESS_TURNS", (iHappinessTurns, utils.getTurns(100))))
		elif iGoal == 2:
			iGoodRelations = countGoodRelationPlayers(iPlayer, AttitudeTypes.ATTITUDE_CAUTIOUS)
			iTotalPlayers = countLivingPlayers()-1
			aHelp.append(getIcon(iGoodRelations >= iTotalPlayers) + localText.getText("TXT_KEY_VICTORY_CAUTIOUS_OR_BETTER_RELATIONS", (iGoodRelations, iTotalPlayers)))

	elif iVictoryType == iConfucianism:
		if iGoal == 0:
			iFriendlyCivs = countGoodRelationPlayers(iPlayer, AttitudeTypes.ATTITUDE_FRIENDLY)
			aHelp.append(getIcon(iFriendlyCivs >= 5) + localText.getText("TXT_KEY_VICTORY_FRIENDLY_CIVS", (iFriendlyCivs, 5)))
		elif iGoal == 1:
			holyCity = gc.getGame().getHolyCity(iConfucianism)
			iCount = countCityWonders(iPlayer, (holyCity.getX(), holyCity.getY()), True)
			aHelp.append(getIcon(holyCity.getOwner() == iPlayer) + localText.getText("TXT_KEY_VICTORY_CONTROL_HOLY_CITY", (holyCity.getName(),)) + ' ' + getIcon(iCount >= 5) + localText.getText("TXT_KEY_VICTORY_HOLY_CITY_WONDERS", (holyCity.getName(), iCount, 5)))
		elif iGoal == 2:
			iUnitCombatMelee = gc.getInfoTypeForString("UNITCOMBAT_MELEE")
			iUnitCombatGunpowder = gc.getInfoTypeForString("UNITCOMBAT_GUN")
			iCount = countUnitsOfType(iPlayer, [iUnitCombatMelee, iUnitCombatGunpowder])
			aHelp.append(getIcon(iCount >= 200) + localText.getText("TXT_KEY_VICTORY_CONTROL_NUM_UNITS", (iCount, 200)))

	elif iVictoryType == iTaoism:
		if iGoal == 0:
			iHealthTurns = data.iTaoistHealthTurns
			aHelp.append(getIcon(iHealthTurns >= utils.getTurns(100)) + localText.getText("TXT_KEY_VICTORY_HEALTH_TURNS", (iHealthTurns, utils.getTurns(100))))
		elif iGoal == 1:
			bConfucianShrine = getNumBuildings(iPlayer, iConfucianShrine) > 0
			bTaoistShrine = getNumBuildings(iPlayer, iTaoistShrine) > 0

			iConfucianIncome = calculateShrineIncome(iPlayer, iConfucianism)
			iTaoistIncome = calculateShrineIncome(iPlayer, iTaoism)
			
			aHelp.append(getIcon(bConfucianShrine) + localText.getText("TXT_KEY_BUILDING_CONFUCIAN_SHRINE", ()) + ' ' + getIcon(bTaoistShrine) + localText.getText("TXT_KEY_BUILDING_TAOIST_SHRINE", ()) + ' ' + getIcon(iConfucianIncome + iTaoistIncome >= 40) + localText.getText("TXT_KEY_VICTORY_CHINESE_SHRINE_INCOME", (iConfucianIncome + iTaoistIncome, 40)))
		elif iGoal == 2:
			holyCity = gc.getGame().getHolyCity(iTaoism)
			aHelp.append(getIcon(holyCity.getOwner() == iPlayer) + localText.getText("TXT_KEY_VICTORY_CONTROL_HOLY_CITY", (holyCity.getName(),)) + ' ' + getIcon(holyCity.getCultureLevel() >= 6) + localText.getText("TXT_KEY_VICTORY_LEGENDARY_CULTURE_CITY", (holyCity.getName(),)))

	elif iVictoryType == iZoroastrianism:
		if iGoal == 0:
			iNumIncense = pPlayer.getNumAvailableBonuses(iIncense)
			aHelp.append(getIcon(iNumIncense >= 6) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_INCENSE_RESOURCES", (iNumIncense, 6)))
		elif iGoal == 1:
			fReligionPercent = gc.getGame().calculateReligionPercent(iZoroastrianism)
			aHelp.append(getIcon(fReligionPercent >= 10.0) + localText.getText("TXT_KEY_VICTORY_SPREAD_RELIGION_PERCENT", (gc.getReligionInfo(iZoroastrianism).getTextKey(), str(u"%.2f%%" % fReligionPercent), str(10))))
		elif iGoal == 2:
			holyCity = gc.getGame().getHolyCity(iZoroastrianism)
			aHelp.append(getIcon(holyCity.getOwner() == iPlayer) + localText.getText("TXT_KEY_VICTORY_CONTROL_HOLY_CITY", (holyCity.getName(),)) + ' ' + getIcon(holyCity.getCultureLevel() >= 6) + localText.getText("TXT_KEY_VICTORY_LEGENDARY_CULTURE_CITY", (holyCity.getName(),)))

	elif iVictoryType == iVictoryPaganism:
		if iGoal == 0:
			iCount = countWorldBuildings(iPaganTemple)
			aHelp.append(getIcon(iCount >= 15) + localText.getText("TXT_KEY_VICTORY_NUM_PAGAN_TEMPLES_WORLD", (iCount, 15)))
		elif iGoal == 1:
			aHelp.append(getPaganGoalHelp(iPlayer))
		elif iGoal == 2:
			bPolytheismNeverReligion = data.bPolytheismNeverReligion
			aHelp.append(getIcon(bPolytheismNeverReligion) + localText.getText("TXT_KEY_VICTORY_POLYTHEISM_NEVER_RELIGION", ()))

	elif iVictoryType == iVictorySecularism:
		if iGoal == 0:
			iCount = 0
			for iReligion in range(iNumReligions):
				if getNumBuildings(iPlayer, iCathedral + 4 * iReligion) > 0:
					iCount += 1
			aHelp.append(getIcon(iCount >= iNumReligions) + localText.getText("TXT_KEY_VICTORY_DIFFERENT_CATHEDRALS", (iCount, iNumReligions)))
		elif iGoal == 1:
			iUniversities = countCivicBuildings(iCivicsReligion, iSecularism, iUniversity)
			iScientists = countCivicSpecialists(iCivicsReligion, iSecularism, iSpecialistGreatScientist)
			iStatesmen = countCivicSpecialists(iCivicsReligion, iSecularism, iSpecialistGreatStatesman)
			aHelp.append(getIcon(iUniversities >= 25) + localText.getText("TXT_KEY_VICTORY_SECULAR_UNIVERSITIES", (iUniversities, 25)))
			aHelp.append(getIcon(iScientists >= 10) + localText.getText("TXT_KEY_VICTORY_SECULAR_SCIENTISTS", (iScientists, 10)) + ' ' + getIcon(iStatesmen >= 10) + localText.getText("TXT_KEY_VICTORY_SECULAR_STATESMEN", (iStatesmen, 10)))
		elif iGoal == 2:
			sString = ""
			lAdvancedPlayers = utils.getSortedList([iLoopPlayer for iLoopPlayer in range(iNumPlayers) if gc.getPlayer(iLoopPlayer).isAlive() and not utils.isAVassal(iLoopPlayer)], lambda iLoopPlayer: gc.getTeam(iLoopPlayer).getTotalTechValue(), True)
			for iLoopPlayer in lAdvancedPlayers[:5]:
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				sString += getIcon(pLoopPlayer.getCivics(iCivicsReligion) == iSecularism) + pLoopPlayer.getCivilizationShortDescription(0) + ' '
			aHelp.append(sString)'''
				
	return aHelp
	
def getPaganGoalHelp(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	paganReligion = gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getPaganReligionName(0)

	if paganReligion == "Anunnaki":
		x, y = 0, 0
		capital = pPlayer.getCapitalCity()
		
		if capital:
			x, y = capital.getX(), capital.getY()
		pBestCity = getBestCity(iPlayer, (x, y), cityWonders)
		bBestCity = isBestCity(iPlayer, (x, y), cityWonders)
		sBestCity = "(none)"
		if pBestCity:
			sBestCity = pBestCity.getName()
		return getIcon(bBestCity) + localText.getText("TXT_KEY_VICTORY_CITY_WITH_MOST_WONDERS", (sBestCity,))
		
	elif paganReligion == "Asatru":
		iCount = countUnitsOfLevel(iPlayer, 5)
		return getIcon(iCount >= 5) + localText.getText("TXT_KEY_VICTORY_UNITS_OF_LEVEL", (5, iCount, 5))
		
	elif paganReligion == "Atua":
		iNumPearls = pPlayer.getNumAvailableBonuses(iPearls)
		iOceanTiles = countControlledTerrain(iPlayer, iOcean)
		return getIcon(iNumPearls >= 4) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", (gc.getBonusInfo(iPearls).getText().lower(), iNumPearls, 4)) + ' ' + getIcon(iOceanTiles >= 50) + localText.getText("TXT_KEY_VICTORY_CONTROLLED_OCEAN_TILES", (iOceanTiles, 50))
		
	elif paganReligion == "Baalism":
		x, y = 0, 0
		capital = pPlayer.getCapitalCity()
		
		if capital:
			x, y = capital.getX(), capital.getY()
		pBestCity = getBestCity(iPlayer, (x, y), cityTradeIncome)
		bBestCity = isBestCity(iPlayer, (x, y), cityTradeIncome)
		return getIcon(bBestCity) + localText.getText("TXT_KEY_VICTORY_HIGHEST_TRADE_CITY", (pBestCity.getName(),))
		
	elif paganReligion == "Druidism":
		iCount = countControlledFeatures(iPlayer, iForest, -1) + countControlledFeatures(iPlayer, iMud, -1)
		return getIcon(iCount >= 20) + localText.getText("TXT_KEY_VICTORY_CONTROLLED_FOREST_AND_MARSH_TILES", (iCount, 20))
	
	elif paganReligion == "Inti":
		iOurTreasury = pPlayer.getGold()
		iWorldTreasury = getGlobalTreasury()
		return getIcon(2 * iOurTreasury >= iWorldTreasury) + localText.getText("TXT_KEY_VICTORY_TOTAL_GOLD", (iOurTreasury, iWorldTreasury - iOurTreasury))
	
	elif paganReligion == "Mazdaism":
		iCount = pPlayer.getNumAvailableBonuses(iIncense)
		return getIcon(iCount >= 6) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", (gc.getBonusInfo(iIncense).getText().lower(), iCount, 6))
	
	elif paganReligion == "Olympianism":
		iCount = countReligionWonders(iPlayer, -1)
		return getIcon(iCount >= 10) + localText.getText("TXT_KEY_VICTORY_NUM_NONRELIGIOUS_WONDERS", (iCount, 10))
		
	elif paganReligion == "Pesedjet":
		iCount = countFirstGreatPeople(iPlayer)
		return getIcon(iCount >= 3) + localText.getText("TXT_KEY_VICTORY_FIRST_GREAT_PEOPLE", (iCount, 3))
	
	elif paganReligion == "Rodnovery":
		iCount = pPlayer.getNumAvailableBonuses(iFur)
		return getIcon(iCount >= 7) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", (gc.getBonusInfo(iFur).getText().lower(), iCount, 7))
	
	elif paganReligion == "Shendao":
		fPopulationPercent = getPopulationPercent(iPlayer)
		return getIcon(fPopulationPercent >= 25.0) + localText.getText("TXT_KEY_VICTORY_PERCENTAGE_WORLD_POPULATION", (str(u"%.2f%%" % fPopulationPercent), str(25)))
	
	elif paganReligion == "Shinto":
		capital = pPlayer.getCapitalCity()
		iCount = 0
		if capital: iCount = countCitySpecialists(iPlayer, (capital.getX(), capital.getY()), iSpecialistGreatSpy)
		return getIcon(iCount >= 3) + localText.getText("TXT_KEY_VICTORY_CAPITAL_GREAT_SPIES", (iCount, 3))
	
	elif paganReligion == "Tengri":
		iCount = pPlayer.getNumAvailableBonuses(iHorse)
		return getIcon(iCount >= 8) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", (gc.getBonusInfo(iHorse).getText().lower(), iCount, 8))
	
	elif paganReligion == "Teotl":
		iCount = data.iTeotlSacrifices
		return getIcon(iCount >= 10) + localText.getText("TXT_KEY_VICTORY_SACRIFICED_SLAVES", (iCount, 10))
	
	elif paganReligion == "Vedism":
		iCount = data.iVedicHappiness
		return getIcon(iCount >= 100) + localText.getText("TXT_KEY_VICTORY_WE_LOVE_RULER_TURNS", (iCount, 100))
	
	elif paganReligion == "Yoruba":
		iNumIvory = pPlayer.getNumAvailableBonuses(iIvory)
		iNumGems = pPlayer.getNumAvailableBonuses(iGems)
		return getIcon(iNumIvory >= 8) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", (gc.getBonusInfo(iIvory).getText().lower(), iNumIvory, 8)) + ' ' + getIcon(iNumGems >= 6) + localText.getText("TXT_KEY_VICTORY_AVAILABLE_RESOURCES", (gc.getBonusInfo(iGems).getText().lower(), iNumGems, 6))

def getUHVHelp(iPlayer, iGoal):
	"Returns an array of help strings used by the Victory Screen table"

	aHelp = []

	# the info is outdated or irrelevant once the goal has been accomplished or failed
	if data.players[iPlayer].lGoals[iGoal] == 1:
		iWinTurn = data.players[iPlayer].lGoalTurns[iGoal]
		iTurnYear = gc.getGame().getTurnYear(iWinTurn)
		if iTurnYear < 0:
			sWinDate = localText.getText("TXT_KEY_TIME_BC", (-iTurnYear,))
		else:
			sWinDate = localText.getText("TXT_KEY_TIME_AD", (iTurnYear,))
		if AdvisorOpt.isUHVFinishDateNone():
			aHelp.append(getIcon(True) + localText.getText("TXT_KEY_VICTORY_GOAL_ACCOMPLISHED", ()))
		elif AdvisorOpt.isUHVFinishDateDate():
			aHelp.append(getIcon(True) + localText.getText("TXT_KEY_VICTORY_GOAL_ACCOMPLISHED_DATE", (sWinDate,)))
		else:
			aHelp.append(getIcon(True) + localText.getText("TXT_KEY_VICTORY_GOAL_ACCOMPLISHED_DATE_TURN", (sWinDate, iWinTurn - utils.getScenarioStartTurn())))
		if not AdvisorOpt.UHVProgressAfterFinish():
			return aHelp
	elif data.players[iPlayer].lGoals[iGoal] == 0:
		aHelp.append(getIcon(False) + localText.getText("TXT_KEY_VICTORY_GOAL_FAILED", ()))
		if not AdvisorOpt.UHVProgressAfterFinish():
			return aHelp

	if iPlayer == iSpain:
		if iGoal == 0:
			aHelp.append("TODO ;)")
		elif iGoal == 1:
			aHelp.append("TODO ;)")
		elif iGoal == 2:
			aHelp.append("TODO ;)")

	elif iPlayer == iFrance:
		if iGoal == 0:
			aHelp.append("TODO ;)")
		elif iGoal == 1:
			aHelp.append("TODO ;)")
		elif iGoal == 2:
			aHelp.append("TODO ;)")
			
	elif iPlayer == iEngland:
		if iGoal == 0:
			aHelp.append("TODO ;)")
		elif iGoal == 1:
			aHelp.append("TODO ;)")
		elif iGoal == 2:
			aHelp.append("TODO ;)")

	elif iPlayer == iVirginia:
		if iGoal == 0:
			iCitiesVirginia = getNumCitiesInArea(iVirginia, Areas.getNormalArea(iVirginia, False))
			iCitiesWestVirginia = 0
			iCitiesKentucky = 0
			# MacAurther TODO: Uncomment when WV and KY are added
			#iCitiesWestVirginia = getNumCitiesInArea(iVirginia, Areas.getNormalArea(iWestVirginia, False))
			#iCitiesKentucky = getNumCitiesInArea(iVirginia, Areas.getNormalArea(iKentucky, False))
			aHelp.append(getIcon(iCitiesVirginia >= 5) + localText.getText("TXT_KEY_VICTORY_VIRGINIA_CONTROL_VIRGINIA", (iCitiesVirginia, 5)) + ' ' + getIcon(iCitiesWestVirginia >= 2) + localText.getText("TXT_KEY_VICTORY_VIRGINIA_CONTROL_WEST_VIRGINIA", (iCitiesWestVirginia, 2)) + ' ' + getIcon(iCitiesKentucky >= 3) + localText.getText("TXT_KEY_VICTORY_VIRGINIA_CONTROL_KENTUCKY", (iCitiesKentucky, 3)))
		elif iGoal == 1:
			iHighestState = getBestPlayer(iVirginia, playerRealPopulation)
			bHighest = (iHighestState == iVirginia)
			aHelp.append(getIcon(bHighest) + localText.getText("TXT_KEY_VICTORY_HIGHEST_POPULATION_STATE", (gc.getPlayer(iHighestState).getCivilizationShortDescription(0),)))
		elif iGoal == 2:
			iGreatGenerals = 0
			iGreatStatesmen = 0
			for tPlot in tRichmond:
				iGreatGenerals = max(iGreatGenerals, countCitySpecialists(iVirginia, tPlot, iSpecialistGreatGeneral))
				iGreatStatesmen = max(iGreatStatesmen, countCitySpecialists(iVirginia, tPlot, iSpecialistGreatStatesman))
			aHelp.append(getIcon(iGreatGenerals + iGreatStatesmen >= 10) + localText.getText("TXT_KEY_VICTORY_GREAT_GENERALS_AND_STATESMEN_SETTLED", ('Richmond', iGreatGenerals + iGreatStatesmen, 10)))

	elif iPlayer == iMassachusetts:
		if iGoal == 0:
			iCitiesMassachusetts = getNumCitiesInArea(iMassachusetts, Areas.getNormalArea(iMassachusetts, False))
			iCitiesMaine = 0
			# MacAurther TODO: Uncomment when ME is added
			#iCitiesMaine = getNumCitiesInArea(iMassachusetts, Areas.getNormalArea(iMaine, False))
			aHelp.append(getIcon(iCitiesMassachusetts >= 3) + localText.getText("TXT_KEY_VICTORY_MASSACHUSETTS_CONTROL_MASSACHUSETTS", (iCitiesMassachusetts, 3)) + ' ' + getIcon(iCitiesMaine >= 2) + localText.getText("TXT_KEY_VICTORY_MASSACHUSETTS_CONTROL_MAINE", (iCitiesMaine, 2)))
		elif iGoal == 1:
			bIndependence = data.lFirstDiscovered[iIndependence] == iMassachusetts
			aHelp.append(getIcon(bIndependence) + localText.getText("TXT_KEY_TECH_INDEPENDENCE", ()))
			iBritsDefeated = data.iMassachusettsVsBritain
			aHelp.append(getIcon(iBritsDefeated >= 10) + localText.getText("TXT_KEY_VICTORY_BRITISH_UNITS", (iBritsDefeated, 10)))
		elif iGoal == 2:
			bHarvard = data.getWonderBuilder(iHarvard) == iMassachusetts
			aHelp.append(getIcon(bHarvard) + localText.getText("TXT_KEY_BUILDING_HARVARD", ()))
			iMostAdvancedCiv = getBestPlayer(iMassachusetts, playerTechs)
			aHelp.append(getIcon(iMostAdvancedCiv == iMassachusetts) + localText.getText("TXT_KEY_VICTORY_MOST_ADVANCED_STATE", (str(gc.getPlayer(iMostAdvancedCiv).getCivilizationShortDescriptionKey()),)))
		

	elif iPlayer == iNewHampshire:
		if iGoal == 0:
			iCitiesNewHampshire = getNumCitiesInArea(iNewHampshire, Areas.getNormalArea(iNewHampshire, False))
			iCitiesVermont = 0
			# MacAurther TODO: Uncomment when VT is added
			#iCitiesVermont = getNumCitiesInArea(iNewHampshire, Areas.getNormalArea(iCitiesVermont, False))
			aHelp.append(getIcon(iCitiesNewHampshire >= 3) + localText.getText("TXT_KEY_VICTORY_NEW_HAMPSHIRE_CONTROL_NEW_HAMPSHIRE", (iCitiesNewHampshire, 3)) + ' ' + getIcon(iCitiesVermont >= 2) + localText.getText("TXT_KEY_VICTORY_NEW_HAMPSHIRE_CONTROL_VERMONT", (iCitiesVermont, 2)))
		elif iGoal == 1:
			aHelp.append("TODO ;)")
		elif iGoal == 2:
			aHelp.append("TODO ;)")

	elif iPlayer == iMaryland:
		if iGoal == 0:
			iChesapeake, iTotalChesapeake = countControlledTiles(iMaryland, tChesapeakeBL, tChesapeakeTR, False, tChesapeakeExceptions, True)
			fChesapeake = iChesapeake * 100.0 / iTotalChesapeake
			aHelp.append(getIcon(fChesapeake >= 70.0) + localText.getText("TXT_KEY_VICTORY_CHESAPEAKE_TERRITORY", (str(u"%.2f%%" % fChesapeake), str(70))))
		elif iGoal == 1:
			# MacAurther TODO: This goal isn't working
			bBORailway = False
			for tPlot in tBaltimore:
				if isConnectedByRailroad(iMaryland, tPlot, lOhioWatershed):
					bBORailway = True
			aHelp.append(getIcon(bBORailway) + localText.getText("TXT_KEY_VICTORY_BO_RAILWAY", ()))
		elif iGoal == 2:
			aHelp.append("TODO ;)")

	elif iPlayer == iConnecticut:
		if iGoal == 0:
			iIndustrialTechs = countFirstDiscovered(iConnecticut, iIndustrialEra)
			aHelp.append(getIcon(iIndustrialTechs >= 8) + localText.getText("TXT_KEY_VICTORY_TECHS_FIRST_DISCOVERED", (gc.getEraInfo(iIndustrialEra).getText(), iIndustrialTechs, 8)))
		elif iGoal == 1:
			aHelp.append("TODO ;)")
		elif iGoal == 2:
			aHelp.append("TODO ;)")

	elif iPlayer == iRhodeIsland:
		if iGoal == 0:
			aHelp.append("TODO ;)")
		elif iGoal == 1:
			aHelp.append("TODO ;)")
		elif iGoal == 2:
			aHelp.append("TODO ;)")

	elif iPlayer == iNorthCarolina:
		if iGoal == 0:
			iCitiesNorthCarolina = getNumCitiesInArea(iNorthCarolina, Areas.getNormalArea(iNorthCarolina, False))
			iCitiesTennessee = 0
			# MacAurther TODO: Uncomment when TN is added
			#iCitiesTennessee = getNumCitiesInArea(iNorthCarolina, Areas.getNormalArea(iTennessee, False))
			aHelp.append(getIcon(iCitiesNorthCarolina >= 5) + localText.getText("TXT_KEY_VICTORY_NORTH_CAROLINA_CONTROL_NORTH_CAROLINA", (iCitiesNorthCarolina, 5)) + ' ' + getIcon(iCitiesTennessee >= 3) + localText.getText("TXT_KEY_VICTORY_NORTH_CAROLINA_CONTROL_TENNESSEE", (iCitiesTennessee, 3)))
		elif iGoal == 1:
			aHelp.append("TODO ;)")
		elif iGoal == 2:
			aHelp.append("TODO ;)")

	elif iPlayer == iSouthCarolina:
		if iGoal == 0:
			aHelp.append("TODO ;)")
		elif iGoal == 1:
			aHelp.append("TODO ;)")
		elif iGoal == 2:
			aHelp.append("TODO ;)")

	elif iPlayer == iNewJersey:
		if iGoal == 0:
			aHelp.append("TODO ;)")
		elif iGoal == 1:
			aHelp.append("TODO ;)")
		elif iGoal == 2:
			fPopPerCity = getAverageCitySize(iNewJersey)
			aHelp.append(getIcon(fPopPerCity >= 20.0) + localText.getText("TXT_KEY_VICTORY_AVERAGE_CITY_POPULATION", (str(u"%.2f" % fPopPerCity), str(20))))

	elif iPlayer == iNewYork:
		if iGoal == 0:
			pBestCity = getBestCity(iNewYork, (137, 54), cityPopulation)
			bBestCityPop = isBestCity(iNewYork, (137, 54), cityPopulation)
			aHelp.append(getIcon(bBestCityPop) + localText.getText("TXT_KEY_VICTORY_MOST_POPULOUS_CITY", (pBestCity.getName(),)))
			bBestCityCul = isBestCity(iNewYork, (137, 54), cityCulture)
			aHelp.append(getIcon(bBestCityCul) + localText.getText("TXT_KEY_VICTORY_MOST_CULTURED_CITY", (pBestCity.getName(),)))
		elif iGoal == 1:
			# If there is a tie, rule in the favor of NY
			iNumImmigrants = data.lImmigrantCount[iNewYork]
			iMostImmigrantsCiv = iNewYork	
			for iCiv in range(iVirginia, iNumPlayers):	# Don't count Euros for now
				if data.lImmigrantCount[iCiv] > iNumImmigrants:
					iNumImmigrants = data.lImmigrantCount[iCiv]
					iMostImmigrantsCiv = iCiv
			bNewYorkMost = iMostImmigrantsCiv == iNewYork
			aHelp.append(getIcon(bNewYorkMost) + localText.getText("TXT_KEY_VICTORY_MOST_IMMIGRANTS", (gc.getPlayer(iMostImmigrantsCiv).getCivilizationShortDescriptionKey(),
				iNumImmigrants,gc.getPlayer(iNewYork).getCivilizationShortDescriptionKey(),data.lImmigrantCount[iNewYork])))
		elif iGoal == 2:
			bBrooklynBridge = data.getWonderBuilder(iBrooklynBridge) == iNewYork
			bStatueOfLiberty = data.getWonderBuilder(iStatueOfLiberty) == iNewYork
			bEmpireState = data.getWonderBuilder(iEmpireStateBuilding) == iNewYork
			bWorldTradeCenter = data.getWonderBuilder(iWorldTradeCenter) == iNewYork
			aHelp.append(getIcon(bStatueOfLiberty) + localText.getText("TXT_KEY_BUILDING_STATUE_OF_LIBERTY", ()) + ' ' + getIcon(bBrooklynBridge) + localText.getText("TXT_KEY_BUILDING_BROOKLYN_BRIDGE", ()) + ' ')
			aHelp.append(getIcon(bEmpireState) + localText.getText("TXT_KEY_BUILDING_EMPIRE_STATE_BUILDING", ()) + ' ' + getIcon(bWorldTradeCenter) + localText.getText("TXT_KEY_BUILDING_WORLD_TRADE_CENTER", ()))
		

	elif iPlayer == iPennsylvania:
		if iGoal == 0:
			bNumImmigrants = data.lImmigrantCount[iPennsylvania] >= 15
			aHelp.append(getIcon(bNumImmigrants) + localText.getText("TXT_KEY_VICTORY_IMMIGRANT_COUNT", (data.lImmigrantCount[iPennsylvania],)))
		elif iGoal == 1:
			iNumIron = countResources(iPennsylvania, iIron)
			iNumCoal = countResources(iPennsylvania, iCoal)
			aHelp.append(getIcon(iNumIron + iNumCoal >= 8) + localText.getText("TXT_KEY_VICTORY_IRON_COAL_RESOURCES", (iNumIron + iNumCoal, 8)))
		elif iGoal == 2:
			aHelp.append("TODO ;)")

	elif iPlayer == iDelaware:
		if iGoal == 0:
			bFederalism = data.lFirstDiscovered[iFederalism] == iDelaware
			aHelp.append(getIcon(bFederalism) + localText.getText("TXT_KEY_TECH_FEDERALISM", ()))
		elif iGoal == 1:
			aHelp.append("TODO ;)")
		elif iGoal == 2:
			aHelp.append("TODO ;)")

	elif iPlayer == iGeorgia:
		if iGoal == 0:
			iCitiesGeorgia = getNumCitiesInArea(iGeorgia, Areas.getNormalArea(iGeorgia, False))
			iCitiesAlabama = 0
			iCitiesMississippi = 0
			# MacAurther TODO: Uncomment when AL and MS are added
			#iCitiesAlabama = getNumCitiesInArea(iGeorgia, Areas.getNormalArea(iAlabama, False))
			#iCitiesMississippi = getNumCitiesInArea(iGeorgia, Areas.getNormalArea(iMississippi, False))
			aHelp.append(getIcon(iCitiesGeorgia >= 5) + localText.getText("TXT_KEY_VICTORY_GEORGIA_CONTROL_GEORGIA", (iCitiesGeorgia, 5)) + ' ' + getIcon(iCitiesAlabama >= 2) + localText.getText("TXT_KEY_VICTORY_GEORGIA_CONTROL_ALABAMA", (iCitiesAlabama, 2)) + ' ' + getIcon(iCitiesMississippi >= 2) + localText.getText("TXT_KEY_VICTORY_GEORGIA_CONTROL_MISSISSIPPI", (iCitiesMississippi, 2)))
		elif iGoal == 1:
			iTradeGold = data.iGeorgiaTradeGold / 100
			aHelp.append(getIcon(iTradeGold >= utils.getTurns(4000)) + localText.getText("TXT_KEY_VICTORY_TRADE_GOLD", (iTradeGold, utils.getTurns(4000))))
		elif iGoal == 2:
			aHelp.append("TODO ;)")

	elif iPlayer == iAmerica:
		if iGoal == 0:
			pass
		elif iGoal == 1:
			bUnitedNations = data.getWonderBuilder(iUnitedNations) == iAmerica
			bBrooklynBridge = data.getWonderBuilder(iBrooklynBridge) == iAmerica
			bStatueOfLiberty = data.getWonderBuilder(iStatueOfLiberty) == iAmerica
			bGoldenGateBridge = data.getWonderBuilder(iGoldenGateBridge) == iAmerica
			bPentagon = data.getWonderBuilder(iPentagon) == iAmerica
			bEmpireState = data.getWonderBuilder(iEmpireStateBuilding) == iAmerica
			aHelp.append(getIcon(bStatueOfLiberty) + localText.getText("TXT_KEY_BUILDING_STATUE_OF_LIBERTY", ()) + ' ' + getIcon(bBrooklynBridge) + localText.getText("TXT_KEY_BUILDING_BROOKLYN_BRIDGE", ()) + ' ' + getIcon(bEmpireState) + localText.getText("TXT_KEY_BUILDING_EMPIRE_STATE_BUILDING", ()))
			aHelp.append(getIcon(bGoldenGateBridge) + localText.getText("TXT_KEY_BUILDING_GOLDEN_GATE_BRIDGE", ()) + ' ' + getIcon(bPentagon) + localText.getText("TXT_KEY_BUILDING_PENTAGON", ()) + ' ' + getIcon(bUnitedNations) + localText.getText("TXT_KEY_BUILDING_UNITED_NATIONS", ()))
		elif iGoal == 2:
			fAlliedCommercePercent = calculateAlliedCommercePercent(iAmerica)
			fAlliedPowerPercent = calculateAlliedPowerPercent(iAmerica)
			aHelp.append(getIcon(fAlliedCommercePercent >= 75.0) + localText.getText("TXT_KEY_VICTORY_ALLIED_COMMERCE_PERCENT", (str(u"%.2f%%" % fAlliedCommercePercent), str(75))))
			aHelp.append(getIcon(fAlliedPowerPercent >= 75.0) + localText.getText("TXT_KEY_VICTORY_ALLIED_POWER_PERCENT", (str(u"%.2f%%" % fAlliedPowerPercent), str(75))))

	elif iPlayer == iCanada:
		if iGoal == 0:
			capital = pCanada.getCapitalCity()
			bAtlantic = capital and isConnectedByRailroad(iCanada, (capital.getX(), capital.getY()), lAtlanticCoast)
			bPacific = capital and isConnectedByRailroad(iCanada, (capital.getX(), capital.getY()), lPacificCoast)
			aHelp.append(getIcon(bAtlantic) + localText.getText("TXT_KEY_VICTORY_ATLANTIC_RAILROAD", ()) + ' ' + getIcon(bPacific) + localText.getText("TXT_KEY_VICTORY_PACIFIC_RAILROAD", ()))
		elif iGoal == 1:
			iCanadaWest, iTotalCanadaWest = countControlledTiles(iCanada, tCanadaWestTL, tCanadaWestBR, False, tCanadaWestExceptions)
			iCanadaEast, iTotalCanadaEast = countControlledTiles(iCanada, tCanadaEastTL, tCanadaEastBR, False, tCanadaEastExceptions)
			fCanada = (iCanadaWest + iCanadaEast) * 100.0 / (iTotalCanadaWest + iTotalCanadaEast)
			bAllCities = controlsAllCities(iCanada, tCanadaWestTL, tCanadaWestBR, tCanadaWestExceptions) and controlsAllCities(iCanada, tCanadaEastTL, tCanadaEastBR, tCanadaEastExceptions)
			aHelp.append(getIcon(fCanada >= 90.0) + localText.getText("TXT_KEY_VICTORY_CONTROL_CANADA", (str(u"%.2f%%" % fCanada), str(90))) + ' ' + getIcon(bAllCities) + localText.getText("TXT_KEY_VICTORY_CONTROL_CANADA_CITIES", ()))
		elif iGoal == 2:
			iPeaceDeals = data.iCanadianPeaceDeals
			aHelp.append(getIcon(iPeaceDeals >= 12) + localText.getText("TXT_KEY_VICTORY_CANADIAN_PEACE_DEALS", (iPeaceDeals, 12)))
			
	return aHelp