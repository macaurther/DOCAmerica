from CvPythonExtensions import *
import CvUtil
import PyHelpers 
import Popup as PyPopup 

from StoredData import data # edead
import RiseAndFall
import Barbs
import Natives
from Religions import rel
import Resources
import CityNameManager as cnm
import UniquePowers     
import AIWars
import Congresses as cong
from Consts import *
from RFCUtils import utils
import CvScreenEnums #Rhye
import Victory as vic
import Stability as sta
import Plague
import Communications
import Companies
import DynamicCivs as dc
import Modifiers
import SettlerMaps
import WarMaps
import RegionMap
import Areas
import Civilizations
import AIParameters
import GreatPeople as gp
import Immigration
import Revolution
import Sentiments

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
localText = CyTranslator()

class CvRFCEventHandler:

	def __init__(self, eventManager):

		self.EventKeyDown=6
		self.bStabilityOverlay = False

		# initialize base class
		eventManager.addEventHandler("GameStart", self.onGameStart) #Stability
		eventManager.addEventHandler("BeginGameTurn", self.onBeginGameTurn) #Stability
		eventManager.addEventHandler("cityAcquired", self.onCityAcquired) #Stability
		eventManager.addEventHandler("cityRazed", self.onCityRazed) #Stability
		eventManager.addEventHandler("cityBuilt", self.onCityBuilt) #Stability
		eventManager.addEventHandler("combatResult", self.onCombatResult) #Stability
		eventManager.addEventHandler("changeWar", self.onChangeWar)
		eventManager.addEventHandler("religionFounded",self.onReligionFounded) #Victory
		eventManager.addEventHandler("buildingBuilt",self.onBuildingBuilt) #Victory
		eventManager.addEventHandler("projectBuilt",self.onProjectBuilt) #Victory
		eventManager.addEventHandler("BeginPlayerTurn", self.onBeginPlayerTurn)
		eventManager.addEventHandler("kbdEvent",self.onKbdEvent)
		eventManager.addEventHandler("OnLoad",self.onLoadGame) #edead: StoredData
		eventManager.addEventHandler("techAcquired",self.onTechAcquired) #Stability
		eventManager.addEventHandler("religionSpread",self.onReligionSpread) #Stability
		eventManager.addEventHandler("firstContact",self.onFirstContact)
		eventManager.addEventHandler("OnPreSave",self.onPreSave) #edead: StoredData
		eventManager.addEventHandler("vassalState", self.onVassalState)
		eventManager.addEventHandler("revolution", self.onRevolution)
		eventManager.addEventHandler("cityGrowth", self.onCityGrowth)
		eventManager.addEventHandler("unitPillage", self.onUnitPillage)
		eventManager.addEventHandler("cityCaptureGold", self.onCityCaptureGold)
		eventManager.addEventHandler("playerGoldTrade", self.onPlayerGoldTrade)
		eventManager.addEventHandler("tradeMission", self.onTradeMission)
		eventManager.addEventHandler("playerSlaveTrade", self.onPlayerSlaveTrade)
		eventManager.addEventHandler("playerChangeStateReligion", self.onPlayerChangeStateReligion)
				
		#Leoreth
		eventManager.addEventHandler("greatPersonBorn", self.onGreatPersonBorn)
		eventManager.addEventHandler("unitCreated", self.onUnitCreated)
		eventManager.addEventHandler("unitBuilt", self.onUnitBuilt)
		eventManager.addEventHandler("plotFeatureRemoved", self.onPlotFeatureRemoved)
		eventManager.addEventHandler("goldenAge", self.onGoldenAge)
		eventManager.addEventHandler("releasedPlayer", self.onReleasedPlayer)
		eventManager.addEventHandler("cityAcquiredAndKept", self.onCityAcquiredAndKept)
		eventManager.addEventHandler("blockade", self.onBlockade)
		eventManager.addEventHandler("peaceBrokered", self.onPeaceBrokered)
		eventManager.addEventHandler("EndPlayerTurn", self.onEndPlayerTurn)
		eventManager.addEventHandler("improvementDestroyed", self.onImprovementDestroyed)
		eventManager.addEventHandler("improvementBuilt", self.onImprovementBuilt)
		eventManager.addEventHandler("improvementOwnerChange", self.onImprovementOwnerChange)
		eventManager.addEventHandler("nativeIndoctrination", self.onNativeIndoctrination)
		
		# MacAurther
		eventManager.addEventHandler("unitBuildImprovement", self.onUnitBuildImprovement)
		eventManager.addEventHandler("EndGameTurn", self.onEndGameTurn)
	       
		self.eventManager = eventManager

		self.rnf = RiseAndFall.RiseAndFall()
		self.barb = Barbs.Barbs()
		self.native = Natives.Natives()
		self.res = Resources.Resources()
		self.up = UniquePowers.UniquePowers()
		self.aiw = AIWars.AIWars()
		self.pla = Plague.Plague()
		self.com = Communications.Communications()
		self.corp = Companies.Companies()
		self.imm = Immigration.Immigration()
		self.rev = Revolution.Revolution()
		self.sen = Sentiments.Sentiments()

		self.improvementTileChanges = [] #FoB - kludge to ensure native units don't move

	def onGameStart(self, argsList):
		'Called at the start of the game'
		
		data.setup()

		self.rnf.setup()
		self.pla.setup()
		dc.setup()
		self.aiw.setup()
		self.up.setup()
		
		vic.setup()
		cong.setup()
		self.imm.setup()
		self.rev.setup()
		self.sen.setup()
		
		# Leoreth: set DLL core values
		Modifiers.init()
		Areas.init()
		SettlerMaps.init()
		WarMaps.init()
		RegionMap.init()
		Civilizations.init()
		AIParameters.init()
		
		return 0


	def onCityAcquired(self, argsList):
		iOwner, iPlayer, city, bConquest, bTrade = argsList
		tCity = (city.getX(), city.getY())
		
		cnm.onCityAcquired(city, iPlayer)
		
		if bConquest:
			sta.onCityAcquired(city, iOwner, iPlayer)
		
		# relocate capitals
		if utils.getHumanID() != iPlayer:
			pass
				
		# remove slaves if unable to practice slavery
		if not gc.getPlayer(iPlayer).canUseSlaves():
			utils.removeSlaves(city)
		else:
			utils.freeSlaves(city, iPlayer)
			
		if city.isCapital():
			if city.isHasRealBuilding(iAdministrativeCenter): 
				city.setHasRealBuilding(iAdministrativeCenter, False)	
				
		# Leoreth: relocate capital for AI if reacquired:
		if utils.getHumanID() != iPlayer and iPlayer < iNumPlayers:
			if data.players[iPlayer].iResurrections == 0:
				if Areas.getCapital(iPlayer) == tCity:
					utils.relocateCapital(iPlayer, city)
			else:
				if Areas.getRespawnCapital(iPlayer) == tCity:
					utils.relocateCapital(iPlayer, city)

		# MacAurther: Hartford should spawn with a Palisade and Barracks
		if iPlayer == iConnecticut and tCity == Areas.getCapital(iConnecticut):
			city.setHasRealBuilding(iBarracks, True)
			city.setHasRealBuilding(iStockade, True)
			
			city.setName("Hartford", False)

		# MacAurther: New York should spawn with some infrastructure
		if iPlayer == iNewYork and tCity == Areas.getCapital(iNewYork):
			if city.getPopulation() < 5:
				city.setPopulation(5)
				
			city.setHasRealBuilding(iBarracks, True)
			city.setHasRealBuilding(iStockade, True)
			city.setHasRealBuilding(iMarket, True)
			city.setHasRealBuilding(iGranary, True)
			city.setHasRealBuilding(iHarbor, True)
			
			city.setName("New York", False)
		
		if bConquest:
			# Colombian UP: no resistance in conquered cities in Latin America -> MacAurther: Manifest Destiny Civic
			# MacAurther TODO: Implement Civic check
			#if iPlayer == iMaya and utils.isReborn(iMaya):
			#	if utils.isPlotInArea(tCity, tSouthCentralAmericaTL, tSouthCentralAmericaBR):
			#		city.setOccupationTimer(0)
			pass
					
		if bTrade:
			for iNationalWonder in range(iNumBuildings):
				if iNationalWonder != iPalace and isNationalWonderClass(gc.getBuildingInfo(iNationalWonder).getBuildingClassType()) and city.hasBuilding(iNationalWonder):
					city.setHasRealBuilding(iNationalWonder, False)
					
		self.pla.onCityAcquired(iOwner, iPlayer, city) # Plague
		self.com.onCityAcquired(city) # Communications
		self.corp.onCityAcquired(argsList) # Companies
		dc.onCityAcquired(iOwner, iPlayer) # DynamicCivs
		
		vic.onCityAcquired(iPlayer, iOwner, city, bConquest)
		
		lTradingCompanyList = [iSpain, iFrance, iEngland]
		
		#MacAurther TODO
		#if bTrade and iPlayer in lTradingCompanyList and (city.getX(), city.getY()) in tTradingCompanyPlotLists[lTradingCompanyList.index(iPlayer)]:
		#	self.up.tradingCompanyCulture(city, iPlayer, iOwner)
		
		return 0
		
	def onCityAcquiredAndKept(self, argsList):
		iPlayer, city = argsList
		iOwner = city.getPreviousOwner()
		
		if city.isCapital():
			self.rnf.createStartingWorkers(iPlayer, (city.getX(), city.getY()))
		
		utils.cityConquestCulture(city, iPlayer, iOwner)

	def onCityRazed(self, argsList):
		city, iPlayer = argsList
		
		# MacAurther: Need to check if previous owner exists because somehow the AI is razing their own cities ¯\_(ツ)_/¯
		#  My hypothesis is that when cities flip to Independents upon a partial collapse, the m_ePreviousOwner member
		#  variable isn't being set in CvCity.cpp, so when the AI re-conquers their original city, that variable is still
		#  unset, leaving it at -1. However, it looks like that should be handled correctly in the right methods, so
		#  I'm not sure. Anyways, this should be a band-aid.
		iPrevOwner = city.getPreviousOwner()
		if iPrevOwner >= 0:
			dc.onCityRazed(iPrevOwner)
		self.pla.onCityRazed(city, iPlayer) #Plague
			
		vic.onCityRazed(iPlayer, city)	
		sta.onCityRazed(iPlayer, city)

	def onCityBuilt(self, argsList):
		city = argsList[0]
		iOwner = city.getOwner()
		tCity = (city.getX(), city.getY())
		x, y = tCity
		
		if iOwner < iNumActivePlayers: 
			cnm.onCityBuilt(city)
			
		# starting workers
		if city.isCapital():
			self.rnf.createStartingWorkers(iOwner, tCity)

		#Rhye - delete culture of barbs and minor civs to prevent weird unhappiness
		pPlot = gc.getMap().plot(x, y)
		for i in range(iNumTotalPlayers - iNumActivePlayers):
			iMinorCiv = i + iNumActivePlayers
			pPlot.setCulture(iMinorCiv, 0, True)
		pPlot.setCulture(iBarbarian, 0, True)

		if iOwner < iNumMajorPlayers:
			utils.spreadMajorCulture(iOwner, tCity)
			if gc.getPlayer(iOwner).getNumCities() < 2:
				gc.getPlayer(iOwner).AI_updateFoundValues(False); # fix for settler maps not updating after 1st city is founded

		vic.onCityBuilt(iOwner, city)
			
		if iOwner < iNumPlayers:
			dc.onCityBuilt(iOwner)
		
		# MacAurther: Religion Founding:
		if iOwner == iVirginia:
			rel.foundEpiscopalianism()
		elif iOwner == iMassachusetts:
			rel.foundPuritanism()
		elif iOwner == iRhodeIsland:
			rel.foundBaptism()
		elif iOwner == iGeorgia:
			rel.foundMethodism()

		# Leoreth: free defender and worker for AI colonies
		#if iOwner in lCivGroups[0]:
		#	if city.getRegionID() not in mercRegions[iArea_Europe]:
		#		if utils.getHumanID() != iOwner:
		#			utils.createGarrisons(tCity, iOwner, 1)
		#			utils.makeUnit(iWorker, iOwner, tCity, 1)
		
		# MacAurther TODO: Somewhere in the code (haven't found where yet), new
		# city populations are set to the era number. However, I want new cities in
		# the PreColumbian-Colonization eras to be 1, and then increase by one each
		# era afterward. This is a hack to quickly reset the population to the desired
		# level 
		city.setPopulation(max(gc.getPlayer(iOwner).getCurrentEra() - iRevolutionaryEra, 1))
		
		# Leoreth: free defender and worker for cities founded by American Pioneer in North America
		#MacAurther TODO: tie to the Pioneer unit somehow?
		if iOwner == iAmerica:
			if city.getRegionID() in [rUnitedStates, rCanada, rAlaska]:
				utils.createGarrisons(tCity, iOwner, 1)
				utils.makeUnit(utils.getBestWorker(iOwner), iOwner, tCity, 1)

	def onPlayerChangeStateReligion(self, argsList):
		'Player changes his state religion'
		iPlayer, iNewReligion, iOldReligion = argsList
		
		if iPlayer < iNumPlayers:
			dc.onPlayerChangeStateReligion(iPlayer, iNewReligion)
			
		sta.onPlayerChangeStateReligion(iPlayer)
		vic.onPlayerChangeStateReligion(iPlayer, iNewReligion)

	def onCombatResult(self, argsList):
		self.rnf.immuneMode(argsList)
		
		pWinningUnit, pLosingUnit = argsList
		iWinningPlayer = pWinningUnit.getOwner()
		iLosingPlayer = pLosingUnit.getOwner()
		
		vic.onCombatResult(pWinningUnit, pLosingUnit)
		
		iUnitPower = 0
		pLosingUnitInfo = gc.getUnitInfo(pLosingUnit.getUnitType())
		
		if pLosingUnitInfo.getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_SIEGE"):
			iUnitPower = pLosingUnitInfo.getPowerValue()
		
		sta.onCombatResult(iWinningPlayer, iLosingPlayer, iUnitPower)
		
		# MacAurther TODO: Might use later
		#if iLosingPlayer == iNative:
		#	if iWinningPlayer not in lCivBioNewWorld or True in data.lFirstContactConquerors:
		#		if gc.getPlayer(iWinningPlayer).isSlavery() or gc.getPlayer(iWinningPlayer).isColonialSlavery():
		#			if pWinningUnit.getUnitType() == iBandeirante:
		#				utils.captureUnit(pLosingUnit, pWinningUnit, iSlave, 100)
		#			else:
		#				utils.captureUnit(pLosingUnit, pWinningUnit, iSlave, 35)
		
		# Brandenburg Gate effect -> MacAurther: West Point Effect
		if gc.getPlayer(iLosingPlayer).isHasBuildingEffect(iWestPoint):
			for iPromotion in range(gc.getNumPromotionInfos()):
				if gc.getPromotionInfo(iPromotion).isLeader() and pLosingUnit.isHasPromotion(iPromotion):
					gc.getPlayer(iLosingPlayer).restoreGeneralThreshold()
					
		
	def onReligionFounded(self, argsList):
		'Religion Founded'
		iReligion, iFounder = argsList
		
		if gc.getGame().getGameTurn() == utils.getScenarioStartTurn():
			return
	
		vic.onReligionFounded(iFounder, iReligion)
		rel.onReligionFounded(iReligion, iFounder)
		dc.onReligionFounded(iFounder)

	def onVassalState(self, argsList):
		'Vassal State'
		iMaster, iVassal, bVassal, bCapitulated = argsList
		
		if bCapitulated:
			sta.onVassalState(iMaster, iVassal)
		
		
		dc.onVassalState(iMaster, iVassal)

	def onRevolution(self, argsList):
		'Called at the start of a revolution'
		iPlayer = argsList[0]
		
		sta.onRevolution(iPlayer)
		
		if iPlayer < iNumPlayers:
			dc.onRevolution(iPlayer)
			
		utils.checkSlaves(iPlayer)
			
		if iPlayer in [iVirginia]:	#MacAurther TODO: Find out what to do with this
			cnm.onRevolution(iPlayer)
			
	def onCityGrowth(self, argsList):
		'City Population Growth'
		pCity, iPlayer = argsList
		
		# Leoreth/Voyhkah: Empire State Building effect
		if pCity.isHasBuildingEffect(iEmpireStateBuilding):
			iPop = pCity.getPopulation()
			pCity.setBuildingCommerceChange(gc.getBuildingInfo(iEmpireStateBuilding).getBuildingClassType(), 0, iPop)
			
	def onUnitPillage(self, argsList):
		unit, iImprovement, iRoute, iPlayer, iGold = argsList
		
		iUnit = unit.getUnitType()
		if iImprovement >= 0:
			vic.onUnitPillage(iPlayer, iGold, iUnit)
		if iImprovement == iNativeVillage:
			self.native.handleNativeVillageDestroyed(unit.getOwner(), unit.getX(), unit.getY(), True)
			
	def onCityCaptureGold(self, argsList):
		city, iPlayer, iGold = argsList
			
	def onPlayerGoldTrade(self, argsList):
		iFromPlayer, iToPlayer, iGold = argsList
			
	def onTradeMission(self, argsList):
		iUnitType, iPlayer, iX, iY, iGold = argsList
		
		
	def onPlayerSlaveTrade(self, argsList):
		iPlayer, iGold = argsList
		
		#if iPlayer == iCongo:
		#	vic.onPlayerSlaveTrade(iPlayer, iGold)
			
	def onUnitGifted(self, argsList):
		pUnit, iOwner, pPlot = argsList
			
	def onUnitCreated(self, argsList):
		utils.debugTextPopup("Unit created")
		pUnit = argsList
			
	def onUnitBuilt(self, argsList):
		city, unit = argsList
		
			
		# Leoreth: help AI by moving new slaves to the new world
		if unit.getUnitType() == iSlave and city.getRegionID() in [rIberia, rBritain, rEurope, rScandinavia, rRussia, rItaly, rBalkans, rMaghreb, rAnatolia] and utils.getHumanID() != city.getOwner():
			utils.moveSlaveToNewWorld(city.getOwner(), unit)
			
		# Space Elevator effect: +1 commerce per satellite built
		if unit.getUnitType() == iSatellite:
			city = utils.getBuildingEffectCity(iSpaceElevator)
			if city:
				city.changeBuildingYieldChange(gc.getBuildingInfo(iSpaceElevator).getBuildingClassType(), YieldTypes.YIELD_COMMERCE, 1)
	
		
	def onBuildingBuilt(self, argsList):
		city, iBuildingType = argsList
		iOwner = city.getOwner()
		tCity = (city.getX(), city.getY())
		
		vic.onBuildingBuilt(iOwner, iBuildingType)
		rel.onBuildingBuilt(city, iOwner, iBuildingType)
		self.rev.onBuildingBuilt(city, iOwner, iBuildingType)
		self.up.onBuildingBuilt(city, iOwner, iBuildingType)
		
		if iOwner < iNumPlayers:
			self.com.onBuildingBuilt(iOwner, iBuildingType, city)
		
		if isWorldWonderClass(gc.getBuildingInfo(iBuildingType).getBuildingClassType()):
			sta.onWonderBuilt(iOwner, iBuildingType)
			
		if iBuildingType == iPalace:
			sta.onPalaceMoved(iOwner)
			dc.onPalaceMoved(iOwner)
			
			if city.isHasRealBuilding(iAdministrativeCenter): city.setHasRealBuilding(iAdministrativeCenter, False)
			
		# Leoreth: update trade routes when Porcelain Tower is built to start its effect -> MacAurther: Capitol
		if iBuildingType == iCapitol:
			gc.getPlayer(iOwner).updateTradeRoutes()

		# Leoreth/Voyhkah: Empire State Building
		if iBuildingType == iEmpireStateBuilding:
			iPop = city.getPopulation()
			city.setBuildingCommerceChange(gc.getBuildingInfo(iEmpireStateBuilding).getBuildingClassType(), 0, iPop)
			
					
	def onPlotFeatureRemoved(self, argsList):
		plot, city, iFeature = argsList
		
	def onProjectBuilt(self, argsList):
		city, iProjectType = argsList
		vic.onProjectBuilt(city.getOwner(), iProjectType)
		
		# Space Elevator effect: +5 commerce per space projectBuilt
		if gc.getProjectInfo(iProjectType).isSpaceship():
			city = utils.getBuildingEffectCity(iSpaceElevator)
			if city:
				city.changeBuildingYieldChange(gc.getBuildingInfo(iSpaceElevator).getBuildingClassType(), YieldTypes.YIELD_COMMERCE, 5)
	
	def onUnitBuildImprovement(self, argsList):
		'Unit begins enacting a Build (building an Improvement or Route)'
		pUnit, iBuild, bFinished = argsList
		
		iBuildFortID = CvUtil.findInfoTypeNum(gc.getBuildInfo,gc.getNumBuildInfos(),'BUILD_FORT')
		
		# Fort WAS built
		if (iBuild == iBuildFortID):
			pUnit.setScriptData("BuildingFort")
	
	def onImprovementBuilt(self, argsList):
		iOldImprovement, iImprovement, iX, iY = argsList
		if iOldImprovement == iNativeVillage:
			print("FOB native village destroyed by improvement")
			iTileOwner = gc.getMap().plot(iX, iY).getOwner()
			if iTileOwner == -1:
				self.native.handleNativeVillageDestroyed(iTileOwner, iX, iY, True)
			else:
				self.native.handleNativeVillageDestroyed(iTileOwner, iX, iY, False)
		
		# MacAurther: Forts control territory
		if iImprovement == iFort:
			pPlot = CyMap().plot(iX, iY)
			# Look for Worker on this plot
			bFoundWorker = False
			for iUnitLoop in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(iUnitLoop)
				
				if (pUnit.getScriptData() == "BuildingFort"):
					iFortOwner = pUnit.getOwner()
					self.rnf.obtainFortCulture(iX, iY, iFortOwner)
					bFoundWorker = True
			
			# If no worker built the fort, assume it belongs to a unit in that tile (i.e. forts placed in the map file)
			if not bFoundWorker and pPlot.getNumUnits() > 0:
				self.rnf.obtainFortCulture(iX, iY, pPlot.getUnit(0).getOwner())

	def onImprovementOwnerChange(self, argsList):
		iImprovement, iOwner, iX, iY = argsList
		if iImprovement == iNativeVillage and iOwner > 0:
			print("FOB native village enveloped by cultural borders")
			self.improvementTileChanges.append((iX,iY,iOwner))
			gc.getMap().plot(iX, iY).setImprovementType(-1)
			# TODO - change to add chance of assimilation
			#self.barb.changeNativeAttitudeForPlayer(iOwner, -iNativeVillageAssimilateCost)
			#gc.getMap().plot(iX, iY).setImprovementType(-1)
		
		# MacAurther: Forts control territory
		# MacAurther TODO: Should there be anything done here?
		#if iImprovement == iFort:
		#	self.rnf.loseFortCulture(iX, iY)
		#	self.rnf.obtainFortCulture(iX, iY, iOwner)

	def onImprovementDestroyed(self, argsList):
		iImprovement, iOwner, iX, iY = argsList
		#FoB - do nothing, should be handled in other events now
		#if iImprovement == iNativeVillage:
		#self.native.handleNativeVillageDestroyed(iOwner, iX, iY, False)
		
		# MacAurther: Forts control territory
		if iImprovement == iFort:
			self.rnf.loseFortCulture(iX, iY)

	def onNativeIndoctrination(self, argsList):
		iPlayer = argsList[0]
		data.players[iPlayer].iNativeAttitudeBase = 5
		
	def onBeginGameTurn(self, argsList):
		iGameTurn = argsList[0]
		
		self.rnf.checkTurn(iGameTurn)
		self.barb.checkTurn(iGameTurn)
		rel.checkTurn(iGameTurn)
		self.res.checkTurn(iGameTurn)
		self.up.checkTurn(iGameTurn)
		self.aiw.checkTurn(iGameTurn)
		self.pla.checkTurn(iGameTurn)
		self.com.checkTurn(iGameTurn)
		self.corp.checkTurn(iGameTurn)
		
		sta.checkTurn(iGameTurn)
		cong.checkTurn(iGameTurn)
		
		# MacAurther
		self.imm.checkTurn(iGameTurn)
		self.rev.checkTurn(iGameTurn)
		
		if iGameTurn % 10 == 0:
			dc.checkTurn(iGameTurn)
		
		if utils.getScenario() == i1600AD and iGameTurn == getTurnForYear(1800):		#MacAurther TODO: Balance
			for iPlayer in range(iGeorgia):
				Modifiers.adjustInflationModifier(iPlayer)
			
		return 0

	def onBeginPlayerTurn(self, argsList):
		iGameTurn, iPlayer = argsList
		
		#if utils.getHumanID() == iPlayer:
		#	utils.debugTextPopup('Can contact: ' + str([gc.getPlayer(i).getCivilizationShortDescription(0) for i in range(iNumPlayers) if gc.getTeam(iPlayer).canContact(i)]))
		if (data.lDeleteMode[0] != -1):
			self.rnf.deleteMode(iPlayer)
			
		self.pla.checkPlayerTurn(iGameTurn, iPlayer)
		self.native.adjustNativeAttitudeForGameTurn(iGameTurn, iPlayer)

		#FoB kludge to ensure units don't move
		if iPlayer == iNative:
			self.onNativeTurn()
		
		if gc.getPlayer(iPlayer).isAlive():
			vic.checkTurn(iGameTurn, iPlayer)
			
			if iPlayer < iNumPlayers and not gc.getPlayer(iPlayer).isHuman():
				self.rnf.checkPlayerTurn(iGameTurn, iPlayer) #for leaders switch

	def onNativeTurn(self):
		for tTileChange in self.improvementTileChanges:
			print("FOB Preventing Unit Movement")
			iX, iY, iOwner = tTileChange
			self.native.handleNativeVillageDestroyed(iOwner, iX, iY, False)
		self.improvementTileChanges = []  # FoB clear list

	def onEndGameTurn(self, argsList):
		'Called at the end of the end of each turn'
		iGameTurn = argsList[0]
		
		self.rnf.updateAllFortCulture()

	def onGreatPersonBorn(self, argsList):
		'Great Person Born'
		pUnit, iPlayer, pCity = argsList
		
		gp.onGreatPersonBorn(pUnit, iPlayer, pCity)
		vic.onGreatPersonBorn(iPlayer, pUnit)
		sta.onGreatPersonBorn(iPlayer)
		
		# Leoreth: Silver Tree Fountain effect -> MacAurther: Mount Vernon Effect
		if gc.getUnitInfo(pUnit.getUnitType()).getLeaderExperience() > 0 and gc.getPlayer(iPlayer).isHasBuildingEffect(iMountVernon):
			city = utils.getHighestEntry(utils.getCityList(iPlayer), lambda city: city.getGreatPeopleProgress())
			if city and city.getGreatPeopleProgress() > 0:
				iGreatPerson = utils.getHighestEntry(range(iNumUnits), lambda iUnit: city.getGreatPeopleUnitProgress(iUnit))
				if iGreatPerson >= 0:
					gc.getPlayer(iPlayer).createGreatPeople(iGreatPerson, False, False, city.getX(), city.getY())

	def onReligionSpread(self, argsList):
		iReligion, iOwner, pSpreadCity = argsList
		
		cnm.onReligionSpread(iReligion, iOwner, pSpreadCity)

	def onFirstContact(self, argsList):
		iTeamX,iHasMetTeamY = argsList
		if iTeamX < iNumPlayers:
			self.rnf.onFirstContact(iTeamX, iHasMetTeamY)
		self.pla.onFirstContact(iTeamX, iHasMetTeamY)
		
		vic.onFirstContact(iTeamX, iHasMetTeamY)

	#Rhye - start
	def onTechAcquired(self, argsList):
		iTech, iTeam, iPlayer, bAnnounce = argsList

		iHuman = utils.getHumanID()
		
		iEra = gc.getTechInfo(iTech).getEra()
		iGameTurn = gc.getGame().getGameTurn()

		if iGameTurn == utils.getScenarioStartTurn():
			return
		
		sta.onTechAcquired(iPlayer, iTech)
		AIParameters.onTechAcquired(iPlayer, iTech)

		if iGameTurn > getTurnForYear(tBirth[iPlayer]):
			vic.onTechAcquired(iPlayer, iTech)
			cnm.onTechAcquired(iPlayer)
			dc.onTechAcquired(iPlayer, iTech)

		if gc.getPlayer(iPlayer).isAlive() and iGameTurn >= getTurnForYear(tBirth[iPlayer]) and iPlayer < iNumPlayers:
			rel.onTechAcquired(iTech, iPlayer)
			self.rev.onTechAcquired(iTech, iPlayer)
			if iGameTurn > getTurnForYear(1700):
				self.aiw.forgetMemory(iTech, iPlayer)

		if iTech == iExploration:
			if iPlayer in [iSpain, iFrance, iEngland]:
				data.players[iPlayer].iExplorationTurn = iGameTurn

		elif iTech == iMicrobiology:
			self.pla.onTechAcquired(iTech, iPlayer)

		elif iTech == iRailroad:
			self.rnf.onRailroadDiscovered(iPlayer)
			
		if iTech in [iExploration, iFirearms]:
			teamPlayer = gc.getTeam(iPlayer)
			if teamPlayer.isHasTech(iExploration) and teamPlayer.isHasTech(iFirearms):
				self.rnf.earlyTradingCompany(iPlayer)
			
		if iTech in [iEconomics, iReplaceableParts]:
			teamPlayer = gc.getTeam(iPlayer)
			if teamPlayer.isHasTech(iEconomics) and teamPlayer.isHasTech(iReplaceableParts):
				self.rnf.lateTradingCompany(iPlayer)
		
		#MacAurther TODO: AI Capital changes (get correct coordinates)
		'''if utils.getHumanID() != iPlayer:
			if iPlayer == iVirginia and iEra == iIndustrial:
				utils.moveCapital(iPlayer, (116, 47)) # Richmond
			elif iPlayer == iMaryland and iEra == iIndustrial:
				utils.moveCapital(iPlayer, (60, 44)) # Annapolis
			elif iPlayer == iNewYork and iEra == iRenaissance:
				utils.moveCapital(iPlayer, (63, 59)) # Albany
			elif iPlayer == iNewJersey and iEra == iRenaissance:
				utils.moveCapital(iPlayer, (63, 59)) # Trenton
			elif iPlayer == iPennsylvania and iEra == iRenaissance:
				utils.moveCapital(iPlayer, (62, 49)) # Harrisburg
			elif iPlayer == iGeorgia and iEra == iRenaissance:
				utils.moveCapital(iPlayer, (62, 49)) # Atlanta'''

	def onPreSave(self, argsList):
		'called before a game is actually saved'
		pass

	def onLoadGame(self, argsList):
		pass
		
	def onChangeWar(self, argsList):
		bWar, iTeam, iOtherTeam = argsList
		
		sta.onChangeWar(bWar, iTeam, iOtherTeam)
		self.up.onChangeWar(bWar, iTeam, iOtherTeam)
		
		if iTeam < iNumPlayers and iOtherTeam < iNumPlayers:
			cong.onChangeWar(bWar, iTeam, iOtherTeam)
		
		# don't start AIWars if they get involved in natural wars
		if bWar and iTeam < iNumPlayers and iOtherTeam < iNumPlayers:
			data.players[iTeam].iAggressionLevel = 0
			data.players[iOtherTeam].iAggressionLevel = 0
			
	def onGoldenAge(self, argsList):
		iPlayer = argsList[0]
		
		sta.onGoldenAge(iPlayer)
		
	def onReleasedPlayer(self, argsList):
		iPlayer, iReleasedPlayer = argsList
		
		lCities = []
		for city in utils.getCityList(iPlayer):
			if city.plot().isCore(iReleasedPlayer) and not city.plot().isCore(iPlayer) and not city.isCapital():
				lCities.append(city)
				
		sta.doResurrection(iReleasedPlayer, lCities, False)
		
		gc.getPlayer(iReleasedPlayer).AI_changeAttitudeExtra(iPlayer, 2)
		
	def onBlockade(self, argsList):
		iPlayer, iGold = argsList
		
		vic.onBlockade(iPlayer, iGold)
		
	def onPeaceBrokered(self, argsList):
		iBroker, iPlayer1, iPlayer2 = argsList
		
		vic.onPeaceBrokered(iBroker, iPlayer1, iPlayer2)
		
	def onEndPlayerTurn(self, argsList):
		iGameTurn, iPlayer = argsList
		
		self.rnf.endTurn(iPlayer)
		sta.endTurn(iPlayer)
		
	def onKbdEvent(self, argsList):
		'keypress handler - return 1 if the event was consumed'
		eventType,key,mx,my,px,py = argsList
			
		theKey=int(key)
		
		if ( eventType == self.EventKeyDown and theKey == int(InputTypes.KB_Q) and self.eventManager.bAlt and self.eventManager.bShift):
			print("SHIFT-ALT-Q") #enables squatting
			self.rnf.setCheatMode(True);
			CyInterface().addMessage(utils.getHumanID(), True, iDuration, "EXPLOITER!!! ;)", "", 0, "", ColorTypes(iRed), -1, -1, True, True)

		#Stability Cheat
		if data.bCheatMode and theKey == int(InputTypes.KB_S) and self.eventManager.bAlt and self.eventManager.bShift:
			print("SHIFT-ALT-S") #increases stability by one level
			utils.setStabilityLevel(utils.getHumanID(), min(5, utils.getStabilityLevel(utils.getHumanID()) + 1))
			
			
		if eventType == self.EventKeyDown and theKey == int(InputTypes.KB_V) and self.eventManager.bCtrl and self.eventManager.bShift:
			for iPlayer in range(iNumTotalPlayersB):
				pPlayer = gc.getPlayer(iPlayer)
				
				#pPlayer.initCity(71, 34)
				#city = gc.getMap().plot(71, 34).getPlotCity()
				
				lEras = [iPreColumbianEra, iExplorationEra, iRevolutionaryEra]
				for iEra in lEras:
					pPlayer.setCurrentEra(iEra)
					for iUnit in range(iNumUnits):
						print (str(gc.getCivilizationInfo(pPlayer.getCivilizationType()).getShortDescription(0)))
						print (str(gc.getEraInfo(iEra).getDescription()))
						print (str(gc.getUnitInfo(iUnit).getDescription()))
						utils.makeUnit(iUnit, iPlayer, (68, 33), 1)
						gc.getMap().plot(68, 33).getUnit(0).kill(False, iBarbarian)
						#print ("Button")
						#city.pushOrder(OrderTypes.ORDER_TRAIN, iUnit , -1, False, True, False, True)
				#city.getPlotCity().kill()