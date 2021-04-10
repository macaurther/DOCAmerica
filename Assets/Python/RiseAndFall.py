# Rhye's and Fall of Civilization - Main Scenario

from CvPythonExtensions import *
import CvUtil
from PyHelpers import PyPlayer
import Popup
from StoredData import data # edead
import CvTranslator
from RFCUtils import utils
from Consts import *
import CityNameManager as cnm
import Victory as vic
import DynamicCivs as dc
from operator import itemgetter
import Stability as sta
import Areas
import Civilizations
import Modifiers
import CvEspionageAdvisor
import BugCore
MainOpt = BugCore.game.MainInterface

################
### Globals ###
##############

gc = CyGlobalContext()
localText = CyTranslator()

iCheatersPeriod = 12
iBetrayalPeriod = 8
iBetrayalThreshold = 80
iRebellionDelay = 15
iEscapePeriod = 30

### Screen popups ###
# (Slowly migrate event handlers here when rewriting to use BUTTONPOPUP_PYTHON and more idiomatic code)

def startNewCivSwitchEvent(iPlayer):
	if MainOpt.isSwitchPopup():
		popup = CyPopupInfo()
		popup.setText(localText.getText("TXT_KEY_INTERFACE_NEW_CIV_SWITCH", (gc.getPlayer(iPlayer).getCivilizationAdjective(0),)))
		popup.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popup.setOnClickedPythonCallback("applyNewCivSwitchEvent")
		
		popup.setData1(iPlayer)
		popup.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_EVENT_BULLET")).getPath())
		popup.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), gc.getInterfaceArtInfo(gc.getInfoTypeForString("INTERFACE_EVENT_BULLET")).getPath())
		
		popup.addPopup(utils.getHumanID())
	
def applyNewCivSwitchEvent(argsList):
	iButton = argsList[0]
	iPlayer = argsList[1]
	
	if iButton == 1:
		handleNewCiv(iPlayer)
		
### Utility methods ###

def handleNewCiv(iPlayer):
	iPreviousPlayer = utils.getHumanID()
	iOldHandicap = gc.getActivePlayer().getHandicapType()
	
	pPlayer = gc.getPlayer(iPlayer)
	
	gc.getActivePlayer().setHandicapType(pPlayer.getHandicapType())
	gc.getGame().setActivePlayer(iPlayer, False)
	pPlayer.setHandicapType(iOldHandicap)
	
	for iMaster in range(iNumPlayers):
		if (gc.getTeam(pPlayer.getTeam()).isVassal(iMaster)):
			gc.getTeam(pPlayer.getTeam()).setVassal(iMaster, False, False)
	
	data.bAlreadySwitched = True
	gc.getPlayer(iPlayer).setPlayable(True)
	
	if gc.getGame().getWinner() == iPreviousPlayer:
		gc.getGame().setWinner(-1, -1)
	
	data.resetHumanStability()

	for city in utils.getCityList(iPlayer):
		city.setInfoDirty(True)
		city.setLayoutDirty(True)
					
	for i in range(3):
		data.players[iPlayer].lGoals[i] = -1
					
	if gc.getDefineINT("NO_AI_UHV_CHECKS") == 1:
		vic.loseAll(iPreviousPlayer)
		
	for iLoopPlayer in range(iNumPlayers):
		gc.getPlayer(iPlayer).setEspionageSpendingWeightAgainstTeam(iLoopPlayer, 0)

class RiseAndFall:

###############
### Popups ###
#############

	''' popupID has to be a registered ID in CvRhyesCatapultEventManager.__init__!! '''
	def showPopup(self, popupID, title, message, labels):
		popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setHeaderString(title)
		popup.setBodyString(message)
		for i in labels:
		    popup.addButton( i )
		popup.launch(False)

	def eventApply7614(self, popupReturn):
		iNewCiv = data.getNewCiv()
		if popupReturn.getButtonClicked() == 0: # 1st button
			self.handleNewCiv(iNewCiv)

	def scheduleFlipPopup(self, iNewCiv, lPlots):
		data.lTempEvents.append((iNewCiv, lPlots))
		self.checkFlipPopup()

	def checkFlipPopup(self):
		for tEvent in data.lTempEvents:
			iNewCiv, lPlots = tEvent
			self.flipPopup(iNewCiv, lPlots)

	def flipPopup(self, iNewCiv, lPlots):
		iHuman = utils.getHumanID()
		
		flipText = CyTranslator().getText("TXT_KEY_FLIPMESSAGE1", ())
		
		for city in self.getConvertedCities(iNewCiv, lPlots):
			flipText += city.getName() + "\n"
			
		flipText += CyTranslator().getText("TXT_KEY_FLIPMESSAGE2", ())
							
		self.showPopup(7615, CyTranslator().getText("TXT_KEY_NEWCIV_TITLE", ()), flipText, (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), CyTranslator().getText("TXT_KEY_POPUP_NO", ())))
		data.iNewCivFlip = iNewCiv
		data.iOldCivFlip = iHuman
		data.lTempPlots = lPlots

	def eventApply7615(self, popupReturn):
		iHuman = utils.getHumanID()
		lPlots = data.lTempPlots
		iNewCivFlip = data.iNewCivFlip
		
		iNumCities = gc.getPlayer(iNewCivFlip).getNumCities()

		lHumanCityList = [city for city in self.getConvertedCities(iNewCivFlip, lPlots) if city.getOwner() == iHuman]
		
		if popupReturn.getButtonClicked() == 0: # 1st button
			print ("Flip agreed")
			CyInterface().addMessage(iHuman, True, iDuration, CyTranslator().getText("TXT_KEY_FLIP_AGREED", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
						
			if lHumanCityList:
				for city in lHumanCityList:
					tCity = (city.getX(), city.getY())
					print ("flipping ", city.getName())
					utils.cultureManager(tCity, 100, iNewCivFlip, iHuman, False, False, False)
					utils.flipUnitsInCityBefore(tCity, iNewCivFlip, iHuman)
					utils.flipCity(tCity, 0, 0, iNewCivFlip, [iHuman])
					utils.flipUnitsInCityAfter(tCity, iNewCivFlip)
					
			if iNumCities == 0 and gc.getPlayer(iNewCivFlip).getNumCities() > 0:
				self.createStartingWorkers(iNewCivFlip, (gc.getPlayer(iNewCivFlip).getCapitalCity().getX(), gc.getPlayer(iNewCivFlip).getCapitalCity().getY()))

			#same code as Betrayal - done just once to make sure human player doesn't hold a stack just outside of the cities
			for (x, y) in lPlots:
				betrayalPlot = gc.getMap().plot(x,y)
				if betrayalPlot.isCore(betrayalPlot.getOwner()) and not betrayalPlot.isCore(iNewCivFlip): continue
				iNumUnitsInAPlot = betrayalPlot.getNumUnits()
				if iNumUnitsInAPlot > 0:
					for iUnit in reversed(range(iNumUnitsInAPlot)):
						unit = betrayalPlot.getUnit(iUnit)
						if unit.getOwner() == iHuman:
							rndNum = gc.getGame().getSorenRandNum(100, 'betrayal')
							if rndNum >= iBetrayalThreshold:
								if unit.getDomainType() == DomainTypes.DOMAIN_LAND:
									iUnitType = unit.getUnitType()
									unit.kill(False, iNewCivFlip)
									utils.makeUnit(iUnitType, iNewCivFlip, (x,y), 1)


			if data.lCheatersCheck[0] == 0:
				data.lCheatersCheck[0] = iCheatersPeriod
				data.lCheatersCheck[1] = data.iNewCivFlip
				
		elif popupReturn.getButtonClicked() == 1: # 2nd button
			print ("Flip disagreed")
			CyInterface().addMessage(iHuman, True, iDuration, CyTranslator().getText("TXT_KEY_FLIP_REFUSED", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
						

			if lHumanCityList:
				for city in lHumanCityList:
					pPlot = gc.getMap().plot(city.getX(), city.getY())
					oldCulture = pPlot.getCulture(iHuman)
					pPlot.setCulture(iNewCivFlip, oldCulture/2, True)
					pPlot.setCulture(iHuman, oldCulture/2, True)
					data.iSpawnWar += 1
					if data.iSpawnWar == 1:
						gc.getTeam(gc.getPlayer(iNewCivFlip).getTeam()).declareWar(iHuman, False, -1) ##True??
						data.iBetrayalTurns = iBetrayalPeriod
						self.initBetrayal()
						
		data.lTempEvents.remove((iNewCivFlip, lPlots))
		
		gc.getGame().autosave()
				
	def rebellionPopup(self, iRebelCiv):
		self.showPopup(7622, CyTranslator().getText("TXT_KEY_REBELLION_TITLE", ()), \
				CyTranslator().getText("TXT_KEY_REBELLION_TEXT", (gc.getPlayer(iRebelCiv).getCivilizationAdjectiveKey(),)), \
				(CyTranslator().getText("TXT_KEY_POPUP_YES", ()), \
				CyTranslator().getText("TXT_KEY_POPUP_NO", ())))

	def eventApply7622(self, popupReturn):
		iHuman = utils.getHumanID()
		iRebelCiv = data.iRebelCiv
		if popupReturn.getButtonClicked() == 0: # 1st button
			gc.getTeam(gc.getPlayer(iHuman).getTeam()).makePeace(iRebelCiv)
		elif popupReturn.getButtonClicked() == 1: # 2nd button
			gc.getTeam(gc.getPlayer(iHuman).getTeam()).declareWar(iRebelCiv, False, -1)

	def eventApply7625(self, popupReturn):
		iHuman = utils.getHumanID()
		iPlayer, targetList = data.lTempEventList
		if popupReturn.getButtonClicked() == 0:
			for tPlot in targetList:
				x, y = tPlot
				if gc.getMap().plot(x, y).getPlotCity().getOwner() == iHuman:
					utils.colonialAcquisition(iPlayer, tPlot)
					gc.getPlayer(iHuman).changeGold(200)
		elif popupReturn.getButtonClicked() == 1:
			for tPlot in targetList:
				x, y = tPlot
				if gc.getMap().plot(x, y).getPlotCity().getOwner() == iHuman:
					utils.colonialConquest(iPlayer, tPlot)
		
	def eventApply7629(self, netUserData, popupReturn):
		pass

#######################################
### Main methods (Event-Triggered) ###
#####################################  

	def setup(self):

		self.determineEnabledPlayers()
		
		self.initScenario()
		
		# MacAurther TODO: Why is this required?? Can delete??
		# Leoreth: make sure to select the Spanish settler
		if pSpain.isHuman():
			x, y = Areas.getCapital(iSpain)
			plotSpain = gc.getMap().plot(x, y)  
			for i in range(plotSpain.getNumUnits()):
				unit = plotSpain.getUnit(i)
				if unit.getUnitType() == iSettler:
					CyInterface().selectUnit(unit, True, False, False)
					break
					
	def initScenario(self):
		self.updateStartingPlots()
	
		self.adjustCityCulture()
			
		self.foundCapitals()
		self.flipStartingTerritory()
		
		self.adjustReligionFoundingDates()
		self.initStartingReligions()
		
		Civilizations.initScenarioTechs(utils.getScenario())
	
		if utils.getScenario() == i1600AD:
			self.create1600ADstartingUnits()
			
		for iPlayer in [iPlayer for iPlayer in range(iNumPlayers) if tBirth[iPlayer] < utils.getScenarioStartYear()]:
			data.players[iPlayer].bSpawned = True
		
		self.invalidateUHVs()
		
		gc.getGame().setVoteSourceReligion(1, iCatholicism, False)
		
		self.updateExtraOptions()
		
	def updateExtraOptions(self):
		# Human player can switch infinite times
		data.bUnlimitedSwitching = (gc.getDefineINT("UNLIMITED_SWITCHING") != 0)
		# No congresses
		data.bNoCongresses = (gc.getDefineINT("NO_CONGRESSES") != 0)
		# No plagues
		data.bNoPlagues = (gc.getDefineINT("NO_PLAGUES") != 0)
		
	def updateStartingPlots(self):
		for iPlayer in range(iNumPlayers):
			x, y = Areas.getCapital(iPlayer)
			gc.getPlayer(iPlayer).setStartingPlot(gc.getMap().plot(x, y), False)
		
	def adjustCityCulture(self):
		if utils.getTurns(10) == 10: return
	
		lCities = []
		for iPlayer in range(iNumTotalPlayersB):
			lCities.extend(utils.getCityList(iPlayer))
			
		for city in lCities:
			city.setCulture(city.getOwner(), utils.getTurns(city.getCulture(city.getOwner())), True)
			
	def adjust1700ADCulture(self):
		for (x, y) in utils.getWorldPlotsList():
			plot = gc.getMap().plot(x, y)
			if plot.getOwner() != -1:
				plot.changeCulture(plot.getOwner(), 100, True)
				utils.convertPlotCulture(plot, plot.getOwner(), 100, True)
			
	def prepareColonists(self):
		for iPlayer in [iSpain, iFrance, iEngland]:
			data.players[iPlayer].iExplorationTurn = getTurnForYear(1700)
			
		data.players[iSpain].iColonistsAlreadyGiven = 7
		data.players[iFrance].iColonistsAlreadyGiven = 3
		data.players[iEngland].iColonistsAlreadyGiven = 3
		
	def init1600ADDiplomacy(self):
		pass
	
	def changeAttitudeExtra(self, iPlayer1, iPlayer2, iValue):
		gc.getPlayer(iPlayer1).AI_changeAttitudeExtra(iPlayer2, iValue)
		gc.getPlayer(iPlayer2).AI_changeAttitudeExtra(iPlayer1, iValue)

	def invalidateUHVs(self):
		for iPlayer in range(iNumPlayers):
			if not gc.getPlayer(iPlayer).isPlayable():
				for i in range(3):
					data.players[iPlayer].lGoals[i] = 0
					
	def foundCapitals(self):
		pass

	def flipStartingTerritory(self):
		pass
			
			
	def startingFlip(self, iPlayer, lRegionList):
	
		for tuple in lRegionList:
			tTL = tuple[0]
			tBR = tuple[1]
			tExceptions = ()
			if len(tuple) > 2: tExceptions = tuple[2]
			self.convertSurroundingCities(iPlayer, utils.getPlotList(tTL, tBR, tExceptions))
			self.convertSurroundingPlotCulture(iPlayer, utils.getPlotList(tTL, tBR, tExceptions))
		
	def expireWonders(self, lWonders):
		for iWonder in lWonders:
			gc.getGame().incrementBuildingClassCreatedCount(gc.getBuildingInfo(iWonder).getBuildingClassType())
			
	def setupBirthTurnModifiers(self):
		for iCiv in range(iNumPlayers):
			if tBirth[iCiv] > -3000 and not gc.getPlayer(iCiv).isHuman():
				data.players[iCiv].iBirthTurnModifier = gc.getGame().getSorenRandNum(11, "BirthTurnModifier") - 5 # -5 to +5
		#now make sure that no civs spawn in the same turn and cause a double "new civ" popup
		for iCiv in range(utils.getHumanID()+1, iNumPlayers):
			for j in range(iNumPlayers-1-iCiv):
				iNextCiv = iCiv+j+1
				if getTurnForYear(tBirth[iCiv]) + data.players[iCiv].iBirthTurnModifier == getTurnForYear(tBirth[iNextCiv]) + data.players[iNextCiv].iBirthTurnModifier:
					data.players[iNextCiv].iBirthTurnModifier += 1
						
	def placeGoodyHuts(self):
			
		if utils.getScenario() == i1600AD:
			#East Coast Tribes
			self.placeHut((140, 69), (144, 73)) # Pennacook
			self.placeHut((135, 35), (139, 69)) # Mahican
			self.placeHut((136, 60), (139, 63)) # Wampanoag
			self.placeHut((128, 57), (132, 61)) # Mohawk
			self.placeHut((125, 55), (127, 59)) # Oneida
			self.placeHut((122, 55), (124, 58)) # Onondaga
			self.placeHut((120, 47), (125, 51)) # Susquehannock
			self.placeHut((132, 43), (134, 45)) # Lenni-Lenape
			self.placeHut((131, 32), (134, 34)) # Tuscarora
			self.placeHut((121, 33), (126, 37)) # Tutelo
			self.placeHut((111, 25), (116, 30)) # Cherokee
			self.placeHut((119, 26), (122, 30)) # Catawba
			self.placeHut((118, 21), (120, 24)) # Yamasee
			self.placeHut((108, 20), (111, 23)) # Creek
			self.placeHut((117, 15), (118, 17)) # Timucua
			self.placeHut((112, 16), (114, 19)) # Apalachee
			self.placeHut((122, 5), (124, 9)) # Calusa
		
		if utils.getScenario() <= i1770AD:
			#Mid-West Tribes
			self.placeHut((107, 54), (110, 58)) # Potawatomi
			self.placeHut((105, 47), (109, 50)) # Miami
			self.placeHut((113, 46), (116, 48)) # Erie
			self.placeHut((105, 34), (108, 37)) # Shawnee
			self.placeHut((100, 40), (104, 43)) # Illinois
			self.placeHut((99, 51), (101, 55)) # Winnebago
			self.placeHut((99, 23), (103, 26)) # Chickasaw
			self.placeHut((101, 17), (104, 20)) # Biloxi
			self.placeHut((96, 17), (99, 20)) # Natchez
			self.placeHut((92, 20), (95, 23)) # Caddo
			self.placeHut((91, 14), (93, 17)) # Atakapa
		
		#Western Tribes
		# MacAurther TODO

		
	def adjustReligionFoundingDates(self):
		lReligionFoundingYears = [-2000, 40, 500, 1521, 622, -1500, 80, -500, -400, -600]
	
		for iReligion in range(iNumReligions):
			if gc.getGame().isReligionFounded(iReligion):
				gc.getGame().setReligionGameTurnFounded(iReligion, getTurnForYear(lReligionFoundingYears[iReligion]))
		
	def initStartingReligions(self):
		if utils.getScenario() == i1600AD:
			utils.setStateReligionBeforeBirth(lCatholicStart, iCatholicism)
			utils.setStateReligionBeforeBirth(lEpiscopalianStart, iEpiscopalianism)
			
	def checkTurn(self, iGameTurn):
	
		# Leoreth: randomly place goody huts
		if iGameTurn == utils.getScenarioStartTurn()+3:
			self.placeGoodyHuts()
		
		#Trigger betrayal mode
		if data.iBetrayalTurns > 0:
			self.initBetrayal()

		if data.lCheatersCheck[0] > 0:
			teamPlayer = gc.getTeam(gc.getPlayer(utils.getHumanID()).getTeam())
			if (teamPlayer.isAtWar(data.lCheatersCheck[1])):
				print ("No cheaters!")
				self.initMinorBetrayal(data.lCheatersCheck[1])
				data.lCheatersCheck[0] = 0
				data.lCheatersCheck[1] = -1
			else:
				data.lCheatersCheck[0] -= 1

		if iGameTurn % utils.getTurns(20) == 0:
			if pIndependent.isAlive():
				utils.updateMinorTechs(iIndependent, iBarbarian)
			if pIndependent2.isAlive():
				utils.updateMinorTechs(iIndependent2, iBarbarian)
			
		'''if utils.isYearIn(1350, 1918):
			for iPlayer in [iSpain, iEngland, iFrance]:
				if iGameTurn == data.players[iPlayer].iExplorationTurn + 1 + data.players[iPlayer].iColonistsAlreadyGiven * 8:
					self.giveColonists(iPlayer)'''
		
		
		
		for iLoopCiv in [iPlayer for iPlayer in range(iNumMajorPlayers) if tBirth[iPlayer] > utils.getScenarioStartYear()]:
			if iGameTurn >= getTurnForYear(tBirth[iLoopCiv]) - 2 and iGameTurn <= getTurnForYear(tBirth[iLoopCiv]) + 6:
				self.initBirth(iGameTurn, tBirth[iLoopCiv], iLoopCiv)
		
		#kill the remaining barbs in the region: it's necessary to do this more than once to protect those civs
		'''for iPlayer in [iSpain, iFrance]:
			if iGameTurn >= getTurnForYear(tBirth[iPlayer])+2 and iGameTurn <= getTurnForYear(tBirth[iPlayer])+utils.getTurns(10):
				utils.killUnitsInArea(iBarbarian, Areas.getBirthArea(iPlayer))'''
				
		#fragment utility
		if iGameTurn >= getTurnForYear(50) and iGameTurn % utils.getTurns(15) == 6:
			self.fragmentIndependents()

		if iGameTurn % utils.getTurns(10) == 5:
			sta.checkResurrection(iGameTurn)
			
		# Leoreth: check for scripted rebirths
		for iCiv in range(iNumPlayers):
			if iCiv in dRebirth:
				if iGameTurn == getTurnForYear(dRebirth[iCiv]) and not gc.getPlayer(iCiv).isAlive():
					self.rebirthFirstTurn(iCiv)
				if iGameTurn == getTurnForYear(dRebirth[iCiv])+1 and gc.getPlayer(iCiv).isAlive() and utils.isReborn(iCiv):
					self.rebirthSecondTurn(iCiv)
					
	def endTurn(self, iPlayer):
		for tTimedConquest in data.lTimedConquests:
			iConqueror, tPlot = tTimedConquest
			utils.colonialConquest(iConqueror, tPlot)
			
		if utils.getHumanID() == iPlayer:
			self.checkFlipPopup()
			
		data.lTimedConquests = []

	def rebirthFirstTurn(self, iCiv):
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		if iCiv in dRebirthCiv:
			pCiv.setCivilizationType(dRebirthCiv[iCiv])
		Modifiers.updateModifiers(iCiv)
		x, y = Areas.dRebirthPlot[iCiv]
		plot = gc.getMap().plot(x,y)
		
		# reset contacts and make peace
		for iOtherCiv in range(iNumPlayers):
			if iCiv != iOtherCiv:
				teamCiv.makePeace(iOtherCiv)
				teamCiv.cutContact(iOtherCiv)
		
		# reset diplomacy
		pCiv.AI_reset()
		
		# reset player espionage weights
		gc.getPlayer(gc.getGame().getActivePlayer()).setEspionageSpendingWeightAgainstTeam(pCiv.getTeam(), 0)
		
		# reset great people
		pCiv.resetGreatPeopleCreated()
		
		# reset map visibility
		for (i, j) in utils.getWorldPlotsList():
			gc.getMap().plot(i, j).setRevealed(iCiv, False, True, -1)
		
		# assign new leader
		if iCiv in rebirthLeaders:
			if pCiv.getLeader() != rebirthLeaders[iCiv]:
				pCiv.setLeader(rebirthLeaders[iCiv])

		CyInterface().addMessage(gc.getGame().getActivePlayer(), True, iDuration, (CyTranslator().getText("TXT_KEY_INDEPENDENCE_TEXT", (pCiv.getCivilizationAdjectiveKey(),))), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
		utils.setReborn(iCiv, True)
		
		# Determine whether capital location is free
		bFree = True
		if not utils.isFree(iCiv, (x, y), True):
			bFree = False

		if plot.isUnit():
			bFree = False

		# if city present, flip it. If plot is free, found it. Else give settler.
		if plot.isCity():
			utils.completeCityFlip(x, y, iCiv, plot.getPlotCity().getOwner(), 100)
		else:
			utils.convertPlotCulture(plot, iCiv, 100, True)
			if bFree:
				pCiv.found(x,y)
			else:
				utils.makeUnit(iSettler, iCiv, (x, y), 1)
				
		# make sure there is a palace in the city
		if plot.isCity():
			capital = plot.getPlotCity()
			if not capital.hasBuilding(iPalace):
				capital.setHasRealBuilding(iPalace, True)
		
		self.createRespawnUnits(iCiv, (x, y))
		

		self.assignTechs(iCiv)
		if gc.getGame().getGameTurn() >= getTurnForYear(tBirth[gc.getGame().getActivePlayer()]):
			startNewCivSwitchEvent(iCiv)

		gc.getPlayer(iCiv).setLatestRebellionTurn(getTurnForYear(dRebirth[iCiv]))
		
		dc.onCivRespawn(iCiv, [])
		
	def rebirthSecondTurn(self, iCiv):
		lRebirthPlots = Areas.getRebirthArea(iCiv)
		
		# exclude American territory for Mexico
		lRemovedPlots = []
					
		for tPlot in lRemovedPlots:
			lRebirthPlots.remove(tPlot)
		
		lCities = []
		for tPlot in lRebirthPlots:
			x, y = tPlot
			plot = gc.getMap().plot(x, y)
					
			if plot.isCity():
				lCities.append(plot.getPlotCity())
			
		# remove garrisons
		for city in lCities:
			if city.getOwner() != utils.getHumanID():
				tPlot = (city.getX(), city.getY())
				utils.relocateGarrisons(tPlot, city.getOwner())
				utils.relocateSeaGarrisons(tPlot, city.getOwner())
				#utils.createGarrisons(tPlot, iCiv)
				
		# convert cities
		iConvertedCities, iHumanCities = self.convertSurroundingCities(iCiv, lRebirthPlots)
		
		# create garrisons
		for city in lCities:
			if city.getOwner() == utils.getHumanID():
				x = city.getX()
				y = city.getY()
				utils.createGarrisons((x, y), iCiv, 1)
				
		# convert plot culture
		self.convertSurroundingPlotCulture(iCiv, lRebirthPlots)
		
		# reset plague
		data.players[iCiv].iPlagueCountdown = -10
		utils.clearPlague(iCiv)
		
		# adjust starting stability
		data.players[iCiv].resetStability()
		data.players[iCiv].iStabilityLevel = iStabilityStable
		if utils.getHumanID() == iCiv: data.resetHumanStability()
		
		# ask human player for flips
		if iHumanCities > 0 and iCiv != utils.getHumanID():
			self.scheduleFlipPopup(iCiv, lRebirthPlots)

	def checkPlayerTurn(self, iGameTurn, iPlayer):
		return

	def fragmentIndependents(self):
		if pIndependent.getNumCities() > 8 or pIndependent2.getNumCities() > 8:
			iBigIndependent = -1
			iSmallIndependent = -1
			if pIndependent.getNumCities() > 2*pIndependent2.getNumCities():
				iBigIndependent = iIndependent
				iSmallIndependent = iIndependent2
			if pIndependent.getNumCities() < 2*pIndependent2.getNumCities():
				iBigIndependent = iIndependent2
				iSmallIndependent = iIndependent
			if iBigIndependent != -1:
				iDivideCounter = 0
				iCounter = 0
				for city in utils.getCityList(iBigIndependent):
					iDivideCounter += 1 #convert 3 random cities cycling just once
					if iDivideCounter % 2 == 1:
						tPlot = (city.getX(), city.getY())
						utils.cultureManager(tPlot, 50, iSmallIndependent, iBigIndependent, False, True, True)
						utils.flipUnitsInCityBefore(tPlot, iSmallIndependent, iBigIndependent)
						utils.flipCity(tPlot, 0, 0, iSmallIndependent, [iBigIndependent])   #by trade because by conquest may raze the city
						utils.flipUnitsInCityAfter(tPlot, iSmallIndependent)
						iCounter += 1
						if iCounter == 3:
							return



	def fragmentBarbarians(self, iGameTurn):
		iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
		for j in range(iRndnum, iRndnum + iNumPlayers):
			iDeadCiv = j % iNumPlayers
			if not gc.getPlayer(iDeadCiv).isAlive() and iGameTurn > getTurnForYear(tBirth[iDeadCiv]) + utils.getTurns(50):
				pDeadCiv = gc.getPlayer(iDeadCiv)
				teamDeadCiv = gc.getTeam(pDeadCiv.getTeam())
				iCityCounter = 0
				for (x, y) in Areas.getNormalArea(iDeadCiv):
					pPlot = gc.getMap().plot( x, y )
					if pPlot.isCity():
						if pPlot.getPlotCity().getOwner() == iBarbarian:
							iCityCounter += 1
				if iCityCounter > 3:
					iDivideCounter = 0
					for (x, y) in Areas.getNormalArea(iDeadCiv):
						pPlot = gc.getMap().plot( x, y )
						if pPlot.isCity():
							city = pPlot.getPlotCity()
							if city.getOwner() == iBarbarian:
								if iDivideCounter % 4 == 0:
									iNewCiv = iIndependent
								elif iDivideCounter % 4 == 1:
									iNewCiv = iIndependent2
								if iDivideCounter % 4 == 0 or iDivideCounter % 4 == 1:
									tPlot = (city.getX(), city.getY())
									utils.cultureManager(tPlot, 50, iNewCiv, iBarbarian, False, True, True)
									utils.flipUnitsInCityBefore(tPlot, iNewCiv, iBarbarian)
									utils.flipCity(tPlot, 0, 0, iNewCiv, [iBarbarian])   #by trade because by conquest may raze the city
									utils.flipUnitsInCityAfter(tPlot, iNewCiv)
									iDivideCounter += 1
					return


	def secession(self, iGameTurn):
		iRndnum = gc.getGame().getSorenRandNum(iNumPlayers, 'starting count')
		for j in range(iRndnum, iRndnum + iNumPlayers):
			iPlayer = j % iNumPlayers
			if gc.getPlayer(iPlayer).isAlive() and iGameTurn >= getTurnForYear(tBirth[iPlayer]) + utils.getTurns(30):
				
				if data.getStabilityLevel(iPlayer) == iStabilityCollapsing:

					cityList = []
					for city in utils.getCityList(iPlayer):
						x = city.getX()
						y = city.getY()
						pPlot = gc.getMap().plot(x, y)

						if not city.isWeLoveTheKingDay() and not city.isCapital() and (x, y) != Areas.getCapital(iPlayer):
							if gc.getPlayer(iPlayer).getNumCities() > 0: #this check is needed, otherwise game crashes
								capital = gc.getPlayer(iPlayer).getCapitalCity()
								iDistance = utils.calculateDistance(x, y, capital.getX(), capital.getY())
								if iDistance > 3:
							
									if city.angryPopulation(0) > 0 or \
										city.healthRate(False, 0) < 0 or \
										city.getReligionBadHappiness() > 0 or \
										city.getLargestCityHappiness() < 0 or \
										city.getHurryAngerModifier() > 0 or \
										city.getNoMilitaryPercentAnger() > 0 or \
										city.getWarWearinessPercentAnger() > 0:
										cityList.append(city)
										continue
									
									for iLoop in range(iNumTotalPlayers+1):
										if iLoop != iPlayer:
											if pPlot.getCulture(iLoop) > 0:
												cityList.append(city)
												break

					if cityList:
						iNewCiv = iIndependent
						iRndNum = gc.getGame().getSorenRandNum(2, 'random independent')
						if iRndNum == 1:
							iNewCiv = iIndependent2
						splittingCity = utils.getRandomEntry(cityList)
						tPlot = (splittingCity.getX(), splittingCity.getY())
						utils.cultureManager(tPlot, 50, iNewCiv, iPlayer, False, True, True)
						utils.flipUnitsInCityBefore(tPlot, iNewCiv, iPlayer)
						utils.flipCity(tPlot, 0, 0, iNewCiv, [iPlayer])   #by trade because by conquest may raze the city
						utils.flipUnitsInCityAfter(tPlot, iNewCiv)
						if iPlayer == utils.getHumanID():
							CyInterface().addMessage(iPlayer, True, iDuration, splittingCity.getName() + " " + \
												CyTranslator().getText("TXT_KEY_STABILITY_SECESSION", ()), "", 0, "", ColorTypes(iOrange), -1, -1, True, True)
						
					return



	def initBirth(self, iCurrentTurn, iBirthYear, iCiv): # iBirthYear is really year now, so no conversion prior to function call - edead
		print 'init birth in: '+str(iBirthYear)
		iHuman = utils.getHumanID()
		iBirthYear = getTurnForYear(iBirthYear) # converted to turns here - edead
		
		if iCiv in lSecondaryCivs:
			if iHuman != iCiv and not data.isPlayerEnabled(iCiv):
				return
		
		lConditionalCivs = [iCanada]
		
				
		tCapital = Areas.getCapital(iCiv)
				
		x, y = tCapital
		bCapitalSettled = False
		
		# MacAurther: Handle colonies that were settled by other Europeans
		if iCiv == iConnecticut or iCiv == iNewYork or iCiv == iDelaware:
			for (i, j) in utils.surroundingPlots(tCapital):
				if gc.getMap().plot(i, j).isCity():
					bCapitalSettled = True
					tCapital = (i, j)
					x, y = tCapital
					break

		if iCurrentTurn == iBirthYear-1 + data.players[iCiv].iSpawnDelay + data.players[iCiv].iFlipsDelay:
			if iCiv in lConditionalCivs or bCapitalSettled:
				utils.convertPlotCulture(gc.getMap().plot(x,y), iCiv, 100, True)

			reborn = utils.getReborn(iCiv)
			tTopLeft, tBottomRight = Areas.getBirthRectangle(iCiv)
			tBroaderTopLeft, tBroaderBottomRight = Areas.tBroaderArea[iCiv]
			
				
			iPreviousOwner = gc.getMap().plot(x, y).getOwner()
				

			if data.players[iCiv].iFlipsDelay == 0: #city hasn't already been founded)
			
				#this may fix the -1 bug
				if iCiv == iHuman: 
					killPlot = gc.getMap().plot(x, y)
					iNumUnitsInAPlot = killPlot.getNumUnits()
					if iNumUnitsInAPlot > 0:
						for i in range(iNumUnitsInAPlot):
							unit = killPlot.getUnit(0)
							if unit.getOwner() != iCiv:
								unit.kill(False, iBarbarian)
				
				bBirthInCapital = False
				
				if (iCiv in lConditionalCivs) or bCapitalSettled:
					bBirthInCapital = True
				
				if bBirthInCapital:
					utils.makeUnit(iMilitia, iCiv, (0, 0), 1)
			
				bDeleteEverything = False
				pCapital = gc.getMap().plot(x, y)
				if pCapital.isOwned():
					if iCiv == iHuman or not gc.getPlayer(iHuman).isAlive():
						if not (pCapital.isCity() and pCapital.getPlotCity().isHolyCity()):
							bDeleteEverything = True
							print ("bDeleteEverything 1")
					else:
						bDeleteEverything = True
						for (i, j) in utils.surroundingPlots(tCapital):
							pPlot=gc.getMap().plot(i, j)
							if (pPlot.isCity() and (pPlot.getPlotCity().getOwner() == iHuman or pPlot.getPlotCity().isHolyCity())):
								bDeleteEverything = False
								print ("bDeleteEverything 2")
								break
				print ("bDeleteEverything", bDeleteEverything)
				if not gc.getMap().plot(x, y).isOwned():
					if iCiv in [iGeorgia]: #dangerous starts
						data.lDeleteMode[0] = iCiv
					if bBirthInCapital:
						self.birthInCapital(iCiv, iPreviousOwner, tCapital, tTopLeft, tBottomRight)
					else:
						self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
				elif bDeleteEverything and not bBirthInCapital:
					for (i, j) in utils.surroundingPlots(tCapital):
						data.lDeleteMode[0] = iCiv
						pCurrent=gc.getMap().plot(i, j)
						for iLoopCiv in range(iNumTotalPlayers+1): #Barbarians as well
							if iCiv != iLoopCiv:
								utils.flipUnitsInArea(utils.getPlotList(tTopLeft, tBottomRight, utils.getOrElse(Areas.dBirthAreaExceptions, iCiv, [])), iCiv, iLoopCiv, True, False)
						if pCurrent.isCity():
							pCurrent.eraseAIDevelopment() #new function, similar to erase but won't delete rivers, resources and features()
						for iLoopCiv in range(iNumTotalPlayers+1): #Barbarians as well
							if iCiv != iLoopCiv:
								pCurrent.setCulture(iLoopCiv, 0, True)
						pCurrent.setOwner(-1)
					if bBirthInCapital:
						self.birthInCapital(iCiv, iPreviousOwner, tCapital, tTopLeft, tBottomRight)
					else:
						self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
				else:
					if bBirthInCapital:
						self.birthInCapital(iCiv, iPreviousOwner, tCapital, tTopLeft, tBottomRight)
					else:
						self.birthInForeignBorders(iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight)
						
				if bBirthInCapital:	
					utils.clearCatapult(iCiv)
						
			else:
				print ( "setBirthType again: flips" )
				self.birthInFreeRegion(iCiv, tCapital, tTopLeft, tBottomRight)
				
		# Leoreth: reveal all normal plots on spawn
		# MacAurther TODO: Do not do this, reveal new array of RevealArea plots
		for (x, y) in Areas.getNormalArea(iCiv):
			gc.getMap().plot(x, y).setRevealed(iCiv, True, True, 0)
				
		
		#MacAurther TODO: Set up British Colony Vassals
		#MacAurther TODO: Break vassalage automatically upon Revolution event
		#if iCiv in [iVirginia, iMassachusetts, iNewHampshire, iMaryland, iConnecticut, iRhodeIsland, iNorthCarolina, iSouthCarolina, 
		#	iNewJersey, iNewYork, iPennsylvania, iDelaware, iGeorgia]:
		#	print "Setting up British Colony Vassal - " + str(iCiv)
		#	gc.getTeam(iCiv).setVassal(iEngland, False, False) #gc.getPlayer(iCiv).getCivilizationType()
		
		if (iCurrentTurn == iBirthYear + data.players[iCiv].iSpawnDelay) and (gc.getPlayer(iCiv).isAlive()) and (not data.bAlreadySwitched or utils.getReborn(iCiv) == 1 or data.bUnlimitedSwitching) and ((iHuman not in lNeighbours[iCiv] and getTurnForYear(tBirth[iCiv]) - getTurnForYear(tBirth[iHuman]) > 0) or getTurnForYear(tBirth[iCiv]) - getTurnForYear(tBirth[iHuman]) >= utils.getTurns(25) ):
			startNewCivSwitchEvent(iCiv)
			
		data.players[iCiv].bSpawned = True

	def moveOutInvaders(self, tTL, tBR):
		#MacAurther TODO: Not doing anything, either delete or repurpose
		for (x, y) in utils.getPlotList(tTL, tBR):
			plot = gc.getMap().plot(x, y)
			for i in range(plot.getNumUnits()):
				unit = plot.getUnit(i)

	def deleteMode(self, iCurrentPlayer):
		iCiv = data.lDeleteMode[0]
		print ("deleteMode after", iCurrentPlayer)
		tCapital = Areas.getCapital(iCiv)
		x, y = tCapital
			
		
		if iCurrentPlayer == iCiv:
			for (i, j) in utils.surroundingPlots(tCapital, 2):
				pPlot=gc.getMap().plot(i, j)
				pPlot.setCulture(iCiv, 300, True)
			for (i, j) in utils.surroundingPlots(tCapital):
				pPlot=gc.getMap().plot(i, j)
				utils.convertPlotCulture(pPlot, iCiv, 100, True)
				if pPlot.getCulture(iCiv) < 3000:
					pPlot.setCulture(iCiv, 3000, True) #2000 in vanilla/warlords, cos here Portugal is choked by spanish culture
				pPlot.setOwner(iCiv)
			data.lDeleteMode[0] = -1
			return
		    
		#print ("iCurrentPlayer", iCurrentPlayer, "iCiv", iCiv)
		if iCurrentPlayer != iCiv-1:
			return
		
		bNotOwned = True
		for (i, j) in utils.surroundingPlots(tCapital):
			#print ("deleting again", i, j)
			pPlot=gc.getMap().plot(i, j)
			if pPlot.isOwned():
				bNotOwned = False
				for iLoopCiv in range(iNumTotalPlayersB): #Barbarians as well
					if iLoopCiv != iCiv:
						pPlot.setCulture(iLoopCiv, 0, True)
				pPlot.setOwner(iCiv)
		
		for (i, j) in utils.surroundingPlots(tCapital, 15): # must include the distance from Sogut to the Caspius
			if (i, j) != tCapital:
				pPlot=gc.getMap().plot(i, j)
				if pPlot.isUnit() and not pPlot.isWater():
					unit = pPlot.getUnit(0)
					if unit.getOwner() == iCiv:
						print ("moving starting units from", i, j, "to", tCapital)
						for i in range(pPlot.getNumUnits()):
							unit = pPlot.getUnit(0)
							unit.setXY(x, y, False, True, False)
		
	def birthInFreeRegion(self, iCiv, tCapital, tTopLeft, tBottomRight):
		x, y = tCapital
		startingPlot = gc.getMap().plot(x, y)
		if data.players[iCiv].iFlipsDelay == 0:
			iFlipsDelay = data.players[iCiv].iFlipsDelay + 2
			if iFlipsDelay > 0:
				print ("starting units in", x, y)
				self.createStartingUnits(iCiv, tCapital)
				
				
				lPlots = utils.surroundingPlots(tCapital, 3)
				utils.flipUnitsInArea(lPlots, iCiv, iBarbarian, True, True) #This is mostly for the AI. During Human player spawn, that area should be already cleaned			
				utils.flipUnitsInArea(lPlots, iCiv, iIndependent, True, False) #This is mostly for the AI. During Human player spawn, that area should be already cleaned			
				utils.flipUnitsInArea(lPlots, iCiv, iIndependent2, True, False) #This is mostly for the AI. During Human player spawn, that area should be already cleaned			
				self.assignTechs(iCiv)
				data.players[iCiv].iPlagueCountdown = -iImmunity
				utils.clearPlague(iCiv)
				data.players[iCiv].iFlipsDelay = iFlipsDelay #save
				

		else: #starting units have already been placed, now the second part
		
			iNumCities = gc.getPlayer(iCiv).getNumCities()
		
			lPlots = utils.getPlotList(tTopLeft, tBottomRight, Areas.getBirthExceptions(iCiv))
			iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, lPlots)
			self.convertSurroundingPlotCulture(iCiv, lPlots)
			utils.flipUnitsInArea(lPlots, iCiv, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ
			utils.flipUnitsInArea(lPlots, iCiv, iIndependent, False, False) #remaining independents in the region now belong to the new civ   
			utils.flipUnitsInArea(lPlots, iCiv, iIndependent2, False, False) #remaining independents in the region now belong to the new civ# starting workers
		
			# create starting workers
			if iNumCities == 0 and gc.getPlayer(iCiv).getNumCities() > 0:
				self.createStartingWorkers(iCiv, (gc.getPlayer(iCiv).getCapitalCity().getX(), gc.getPlayer(iCiv).getCapitalCity().getY()))
			
   
			print ("utils.flipUnitsInArea()") 
			#cover plots revealed by the lion
			utils.clearCatapult(iCiv)

			if iNumHumanCitiesToConvert > 0 and iCiv != utils.getHumanID(): # Leoreth: quick fix for the "flip your own cities" popup, still need to find out where it comes from
				print "Flip Popup: free region"
				self.scheduleFlipPopup(iCiv, lPlots)
				

			
	def birthInForeignBorders(self, iCiv, tTopLeft, tBottomRight, tBroaderTopLeft, tBroaderBottomRight):
		
				
		iNumCities = gc.getPlayer(iCiv).getNumCities()
		
		lPlots = utils.getPlotList(tTopLeft, tBottomRight, Areas.getBirthExceptions(iCiv))
		iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, lPlots)
		self.convertSurroundingPlotCulture(iCiv, lPlots)
		
		# create starting workers
		if iNumCities == 0 and gc.getPlayer(iCiv).getNumCities() > 0:
			self.createStartingWorkers(iCiv, (gc.getPlayer(iCiv).getCapitalCity().getX(), gc.getPlayer(iCiv).getCapitalCity().getY()))

		#now starting units must be placed
		if iNumAICitiesConverted > 0:
			plotList = utils.squareSearch(tTopLeft, tBottomRight, utils.ownedCityPlots, iCiv)
			if plotList:
				tPlot = utils.getRandomEntry(plotList)
				if tPlot:
					self.createStartingUnits(iCiv, tPlot)
					self.assignTechs(iCiv)
					data.players[iCiv].iPlagueCountdown = -iImmunity
					utils.clearPlague(iCiv)
			utils.flipUnitsInArea(lPlots, iCiv, iBarbarian, False, True) #remaining barbs in the region now belong to the new civ 
			utils.flipUnitsInArea(lPlots, iCiv, iIndependent, False, False) #remaining barbs in the region now belong to the new civ 
			utils.flipUnitsInArea(lPlots, iCiv, iIndependent2, False, False) #remaining barbs in the region now belong to the new civ

		else:   #search another place
			plotList = utils.squareSearch(tTopLeft, tBottomRight, utils.goodPlots, [])
			if plotList:
				tPlot = utils.getRandomEntry(plotList)
				if tPlot:
					self.createStartingUnits(iCiv, tPlot)
					self.assignTechs(iCiv)
					data.players[iCiv].iPlagueCountdown = -iImmunity
					utils.clearPlague(iCiv)
			else:
				plotList = utils.squareSearch(tBroaderTopLeft, tBroaderBottomRight, utils.goodPlots, [])
			if plotList:
				tPlot = utils.getRandomEntry(plotList)
				if tPlot:
					self.createStartingUnits(iCiv, tPlot)
					#self.createStartingWorkers(iCiv, tPlot)
					self.assignTechs(iCiv)
					data.players[iCiv].iPlagueCountdown = -iImmunity
					utils.clearPlague(iCiv)
			utils.flipUnitsInArea(lPlots, iCiv, iBarbarian, True, True) #remaining barbs in the region now belong to the new civ 
			utils.flipUnitsInArea(lPlots, iCiv, iIndependent, True, False) #remaining barbs in the region now belong to the new civ 
			utils.flipUnitsInArea(lPlots, iCiv, iIndependent2, True, False) #remaining barbs in the region now belong to the new civ 

		if iNumHumanCitiesToConvert > 0:
			print "Flip Popup: foreign borders"
			self.scheduleFlipPopup(iCiv, lPlots)
			

	#Leoreth - adapted from SoI's birthConditional method by embryodead
	def birthInCapital(self, iCiv, iPreviousOwner, tCapital, tTopLeft, tBottomRight):
		iOwner = iPreviousOwner
		x, y = tCapital

		if data.players[iCiv].iFlipsDelay == 0:

			iFlipsDelay = data.players[iCiv].iFlipsDelay + 2

			if iFlipsDelay > 0:

				# flip capital instead of spawning starting units
				utils.flipCity(tCapital, False, True, iCiv, ())
				gc.getMap().plot(x, y).getPlotCity().setHasRealBuilding(iPalace, True)
				utils.convertPlotCulture(gc.getMap().plot(x, y), iCiv, 100, True)
				self.convertSurroundingPlotCulture(iCiv, utils.surroundingPlots(tCapital))
				
				#cover plots revealed
				for (i, j) in utils.surroundingPlots((0, 0), 2):
					gc.getMap().plot(i, j).setRevealed(iCiv, False, True, -1)


				print ("birthConditional: starting units in", x, y)
				self.createStartingUnits(iCiv, tCapital)

				data.players[iCiv].iPlagueCountdown
				utils.clearPlague(iCiv)

				print ("flipping remaining units")
				lPlots = utils.getPlotList(tTopLeft, tBottomRight)
				utils.flipUnitsInArea(lPlots, iCiv, iBarbarian, True, True) #remaining barbs in the region now belong to the new civ 
				utils.flipUnitsInArea(lPlots, iCiv, iIndependent, True, False) #remaining barbs in the region now belong to the new civ 
				utils.flipUnitsInArea(lPlots, iCiv, iIndependent2, True, False) #remaining barbs in the region now belong to the new civ 
				
				self.assignTechs(iCiv)
				
				data.players[iCiv].iFlipsDelay = iFlipsDelay #save

				# kill the catapult and cover the plots
				utils.clearCatapult(iCiv)
				
				utils.convertPlotCulture(gc.getMap().plot(x, y), iCiv, 100, True)
				
				# notify dynamic names
				dc.onCityAcquired(iCiv, iOwner)
				
				self.createStartingWorkers(iCiv, tCapital)

		else: # starting units have already been placed, now to the second part
			lPlots = utils.getPlotList(tTopLeft, tBottomRight, Areas.getBirthExceptions(iCiv))
			iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(iCiv, lPlots)
			self.convertSurroundingPlotCulture(iCiv, lPlots)
				
			for i in range(iIndependent, iBarbarian+1):
				utils.flipUnitsInArea(lPlots, iCiv, i, False, True) #remaining barbs/indeps in the region now belong to the new civ   
			
			# kill the catapult and cover the plots
			utils.clearCatapult(iCiv)
				
			# convert human cities
			if iNumHumanCitiesToConvert > 0:
				print "Flip Popup: in capital"
				self.scheduleFlipPopup(iCiv, lPlots)
				
			utils.convertPlotCulture(gc.getMap().plot(x, y), iCiv, 100, True)
			
				
	def getConvertedCities(self, iPlayer, lPlots = []):
		lCities = []
		
		for city in utils.getAreaCities(lPlots):
			if city.plot().isCore(city.getOwner()) and not city.plot().isCore(iPlayer): continue
			
			if city.getOwner() != iPlayer:
				lCities.append(city)
			
					
		# Leoreth: Canada also flips English/American/French cities in the Canada region
		if iPlayer == iCanada:
			lCanadaCities = []
			lCanadaCities.extend(utils.getCityList(iFrance))
			lCanadaCities.extend(utils.getCityList(iEngland))
			lCanadaCities.extend(utils.getCityList(iAmerica))
			
			for city in lCanadaCities:
				if city.getRegionID() == rCanada and city.getX() < Areas.getCapital(iCanada)[0] and (city.getX(), city.getY()) not in [(c.getX(), c.getY()) for c in lCities]:
					lCities.append(city)
					
		# Leoreth: remove capital locations
		for city in lCities:
			if city.getOwner() < iNumPlayers:
				if (city.getX(), city.getY()) == Areas.getCapital(city.getOwner()) and city.isCapital():
					lCities.remove(city)

		return lCities
						
	def convertSurroundingCities(self, iPlayer, lPlots):
		iConvertedCitiesCount = 0
		iNumHumanCities = 0
		data.iSpawnWar = 0
					
		lEnemies = []
		lCities = self.getConvertedCities(iPlayer, lPlots)
		
		for city in lCities:
			x = city.getX()
			y = city.getY()
			iHuman = utils.getHumanID()
			iOwner = city.getOwner()
			iCultureChange = 0
			
			# Case 1: Minor civilization
			if iOwner in [iBarbarian, iIndependent, iIndependent2, iNative]:
				iCultureChange = 100
				
			# Case 2: Human city
			elif iOwner == iHuman:
				iNumHumanCities += 1
				
			# Case 3: Other
			else:
				iCultureChange = 100
				if iOwner not in lEnemies: lEnemies.append(iOwner)
			
			if iCultureChange > 0:
				utils.completeCityFlip(x, y, iPlayer, iOwner, iCultureChange, True, False, False, True)
				utils.ensureDefenders(iPlayer, (x, y), 2)
				iConvertedCitiesCount += 1
				
		self.warOnSpawn(iPlayer, lEnemies)
				
		if iConvertedCitiesCount > 0:
			if iHuman == iPlayer:
				CyInterface().addMessage(iPlayer, True, iDuration, CyTranslator().getText("TXT_KEY_FLIP_TO_US", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
				
		return iConvertedCitiesCount, iNumHumanCities
		
	def warOnSpawn(self, iPlayer, lEnemies):
		if iPlayer == iCanada: return
		
		if gc.getGame().getGameTurn() <= getTurnForYear(tBirth[iPlayer]) + 5:
			for iEnemy in lEnemies:
				tEnemy = gc.getTeam(iEnemy)
				
				if tEnemy.isAtWar(iPlayer): continue
			
				iRand = gc.getGame().getSorenRandNum(100, 'War on spawn')
				if iRand >= tAIStopBirthThreshold[iEnemy]:
					tEnemy.declareWar(iPlayer, True, WarPlanTypes.WARPLAN_ATTACKED_RECENT)
					self.spawnAdditionalUnits(iPlayer)
					
	def spawnAdditionalUnits(self, iPlayer):
		tPlot = Areas.getCapital(iPlayer)
		self.createAdditionalUnits(iPlayer, tPlot)

	def convertSurroundingPlotCulture(self, iCiv, lPlots):
		for (x, y) in lPlots:
			pPlot = gc.getMap().plot(x, y)
			if pPlot.isOwned() and pPlot.isCore(pPlot.getOwner()) and not pPlot.isCore(iCiv): continue
			pPlot.resetCultureConversion()
			if not pPlot.isCity():
				utils.convertPlotCulture(pPlot, iCiv, 100, False)

	def findSeaPlots( self, tCoords, iRange, iCiv):
		"""Searches a sea plot that isn't occupied by a unit and isn't a civ's territory surrounding the starting coordinates"""
		seaPlotList = []
		for (x, y) in utils.surroundingPlots(tCoords, iRange): 
			pPLot = gc.getMap().plot(x, y)
			if pPLot.isWater():
				if not pPLot.isUnit():
					if not (pPLot.isOwned() and pPLot.getOwner() != iCiv):
						seaPlotList.append((x, y))
						# this is a good plot, so paint it and continue search
		if seaPlotList:
			return utils.getRandomEntry(seaPlotList)
		return (None)


	def giveRaiders( self, iCiv, lPlots):
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		if pCiv.isAlive() and not pCiv.isHuman():

			cityList = []
			#collect all the coastal cities belonging to iCiv in the area
			for (x, y) in lPlots:
				pPLot = gc.getMap().plot(x, y)
				if pPLot.isCity():
					city = pPLot.getPlotCity()
					if city.getOwner() == iCiv:
						if city.isCoastalOld():
							cityList.append(city)

			if cityList:
				city = utils.getRandomEntry(cityList)
				if city:
					tCityPlot = (city.getX(), city.getY())
					tPlot = self.findSeaPlots(tCityPlot, 1, iCiv)
					if tPlot:
						x, y = tPlot
						gc.getPlayer(iCiv).initUnit(utils.getUniqueUnitType(iCiv, gc.getUnitInfo(iGalley).getUnitClassType()), x, y, UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
						if teamCiv.isHasTech(iSteel):
							gc.getPlayer(iCiv).initUnit(utils.getUniqueUnitType(iCiv, gc.getUnitInfo(iPikeman).getUnitClassType()), x, y, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
							gc.getPlayer(iCiv).initUnit(utils.getUniqueUnitType(iCiv, gc.getUnitInfo(iPikeman).getUnitClassType()), x, y, UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.DIRECTION_SOUTH)
						else:
							gc.getPlayer(iCiv).initUnit(iSwordsman, x, y, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
							gc.getPlayer(iCiv).initUnit(iSwordsman, x, y, UnitAITypes.UNITAI_ATTACK_CITY, DirectionTypes.DIRECTION_SOUTH)

	def giveEarlyColonists( self, iCiv):
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		if pCiv.isAlive() and not pCiv.isHuman():
			capital = gc.getPlayer(iCiv).getCapitalCity()
			tCapital = (capital.getX(), capital.getY())
						
			tSeaPlot = self.findSeaPlots(tCapital, 1, iCiv)
			
			if tSeaPlot:
				gc.getPlayer(iCiv).initUnit(iGalley, tSeaPlot[0], tSeaPlot[1], UnitAITypes.UNITAI_SETTLER_SEA, DirectionTypes.DIRECTION_SOUTH)
				utils.makeUnit(iSettler, iCiv, tSeaPlot, 1)
				utils.makeUnit(iArcher, iCiv, tSeaPlot, 1)

	def giveColonists(self, iCiv):
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		
		if pCiv.isAlive() and utils.getHumanID() != iCiv and iCiv in dMaxColonists:
			if teamCiv.isHasTech(iExploration) and data.players[iCiv].iColonistsAlreadyGiven < dMaxColonists[iCiv]:
				lCities = utils.getAreaCitiesCiv(iCiv, Areas.getCoreArea(iCiv))
				
						
				lCoastalCities = [city for city in lCities if city.isCoastal(20)]
						
				if lCoastalCities:
					city = utils.getRandomEntry(lCoastalCities)
					tPlot = (city.getX(), city.getY())
					tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
					if not tSeaPlot: tSeaPlot = tPlot
					
					utils.makeUnitAI(utils.getUniqueUnitType(iCiv, gc.getUnitInfo(iGalleon).getUnitClassType()), iCiv, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA, 1)
					utils.makeUnitAI(iSettler, iCiv, tSeaPlot, UnitAITypes.UNITAI_SETTLE, 1)
					utils.makeUnit(utils.getBestDefender(iCiv), iCiv, tSeaPlot, 1)
					utils.makeUnit(iWorker, iCiv, tSeaPlot, 1)
					
					data.players[iCiv].iColonistsAlreadyGiven += 1
					

	def onFirstContact(self, iTeamX, iHasMetTeamY):
		pass

	def lateTradingCompany(self, iCiv):
		pass

	def earlyTradingCompany(self, iCiv):
		pass
				
	def onRailroadDiscovered(self, iCiv):
		pass
		#MacAurther TODO
		'''if utils.getHumanID() != iCiv:
			if iCiv == iAmerica:
				iCount = 0
				lWestCoast = [(11, 50), (11, 49), (11, 48), (11, 47), (11, 46), (12, 45)]
				lEnemyCivs = []
				lFreePlots = []
				for tPlot in lWestCoast:
					x, y = tPlot
					pPlot = gc.getMap().plot(x, y)
					if pPlot.isCity():
						if pPlot.getPlotCity().getOwner() != iAmerica:
							iCount += 1
							lWestCoast.remove((x, y))
							lEnemyCivs.append(pPlot.getPlotCity().getOwner())
							for (i, j) in utils.surroundingPlots(tPlot):
								plot = gc.getMap().plot(i, j)
								if not (plot.isCity() or plot.isPeak() or plot.isWater()):
									lFreePlots.append((i, j))
									
				for iEnemy in lEnemyCivs:
					gc.getTeam(iCiv).declareWar(iEnemy, True, WarPlanTypes.WARPLAN_LIMITED)
									
				if iCount > 0:
					for i in range(iCount):
						tPlot = utils.getRandomEntry(lFreePlots)
						utils.makeUnitAI(iMinuteman, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 3)
						utils.makeUnitAI(iCannon, iCiv, tPlot, UnitAITypes.UNITAI_ATTACK_CITY, 2)
						
				if 2-iCount > 0:
					for i in range(2-iCount):
						tPlot = utils.getRandomEntry(lWestCoast)
						utils.makeUnit(iSettler, iCiv, tPlot, 1)
						utils.makeUnit(iMinuteman, iCiv, tPlot, 1)'''
						
					


	def handleColonialAcquisition(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		targetList = utils.getColonialTargets(iPlayer, True)
		targetCivList = []
		settlerList = []
		
		if not targetList:
			return

		iGold = len(targetList) * 200

		for tPlot in targetList:
			x, y = tPlot
			if gc.getMap().plot(x, y).isCity():
				iTargetCiv = gc.getMap().plot(x, y).getPlotCity().getOwner()
				if not iTargetCiv in targetCivList:
					targetCivList.append(iTargetCiv)
			else:
				settlerList.append(tPlot)

		for tPlot in settlerList:
			utils.colonialAcquisition(iPlayer, tPlot)
	
		for iTargetCiv in targetCivList:
			if iTargetCiv == utils.getHumanID():
				askCityList = []
				sAskCities = ""
				sPlayer = pPlayer.getCivilizationAdjectiveKey()
				for tPlot in targetList:
					x, y = tPlot
					if gc.getMap().plot(x, y).getPlotCity().getOwner() == iTargetCiv:
						askCityList.append(tPlot)
						#sAskCities += gc.getMap().plot(x, y).getPlotCity().getName() + " "
						
				if askCityList:
					x, y = askCityList[0]
					sAskCities = gc.getMap().plot(x, y).getPlotCity().getName()
					
				for tPlot in askCityList:
					x, y = tPlot
					if tPlot != askCityList[0]:
						if tPlot != askCityList[len(askCityList)-1]:
							sAskCities += ", " + gc.getMap().plot(x, y).getPlotCity().getName()
						else:
							sAskCities += CyTranslator().getText("TXT_KEY_AND", ()) + gc.getMap().plot(x, y).getPlotCity().getName()
						
				iAskGold = len(askCityList) * 200
						
				popup = Popup.PyPopup(7625, EventContextTypes.EVENTCONTEXT_ALL)
				popup.setHeaderString(CyTranslator().getText("TXT_KEY_ASKCOLONIALCITY_TITLE", (sPlayer,)))
				popup.setBodyString(CyTranslator().getText("TXT_KEY_ASKCOLONIALCITY_MESSAGE", (sPlayer, iAskGold, sAskCities)))
				popup.addButton(CyTranslator().getText("TXT_KEY_POPUP_YES", ()))
				popup.addButton(CyTranslator().getText("TXT_KEY_POPUP_NO", ()))
				argsList = (iPlayer, askCityList)
				data.lTempEventList = argsList
				popup.launch(False)
			else:
				iRand = gc.getGame().getSorenRandNum(100, 'City acquisition offer')
				if iTargetCiv < iNumPlayers:
					if iRand >= tPatienceThreshold[iTargetCiv] and not gc.getTeam(iPlayer).isAtWar(iTargetCiv):
						bAccepted = True
					else:
						bAccepted = False
				else:
					bAccepted = True
				
				iNumCities = 0
				for tPlot in targetList:
					x, y = tPlot
					if gc.getMap().plot(x, y).getPlotCity().getOwner() == iTargetCiv:
						iNumCities += 1
						
				if iNumCities >= gc.getPlayer(iTargetCiv).getNumCities():
					bAccepted = False

				for tPlot in targetList:
					x, y = tPlot
					if gc.getMap().plot(x, y).getPlotCity().getOwner() == iTargetCiv:
						if bAccepted:
							utils.colonialAcquisition(iPlayer, tPlot)
							gc.getPlayer(iTargetCiv).changeGold(200)
						else:
							data.timedConquest(iPlayer, tPlot)

		pPlayer.setGold(max(0, pPlayer.getGold()-iGold))

	def handleColonialConquest(self, iPlayer):
		targetList = utils.getColonialTargets(iPlayer)
		
		if not targetList:
			self.handleColonialAcquisition(iPlayer)
			return

		for tPlot in targetList:
			data.timedConquest(iPlayer, tPlot)

		tSeaPlot = -1
		for (i, j) in utils.surroundingPlots(targetList[0]):
			if gc.getMap().plot(i, j).isWater():
				tSeaPlot = (i, j)
				break

		if tSeaPlot != -1:
			utils.makeUnit(utils.getUniqueUnitType(iPlayer, gc.getUnitInfo(iGalleon).getUnitClassType()), iPlayer, tSeaPlot, 1)
	
	def startWarsOnSpawn(self, iCiv):
	
		pCiv = gc.getPlayer(iCiv)
		teamCiv = gc.getTeam(pCiv.getTeam())
		
		iMin = 10
		
		if gc.getGame().getSorenRandNum(100, 'Trigger spawn wars') >= iMin:
			for iLoopCiv in lEnemyCivsOnSpawn[iCiv]:
				if utils.isAVassal(iLoopCiv): continue
				if not gc.getPlayer(iLoopCiv).isAlive(): continue
				if teamCiv.isAtWar(iLoopCiv): continue
				if utils.getHumanID() == iCiv and iLoopCiv not in lTotalWarOnSpawn[iCiv]: continue
				
				iLoopMin = 50
				if iLoopCiv >= iNumMajorPlayers: iLoopMin = 30
				if utils.getHumanID() == iLoopCiv: iLoopMin += 10
				
				if gc.getGame().getSorenRandNum(100, 'Check spawn war') >= iLoopMin:
					iWarPlan = -1
					if iLoopCiv in lTotalWarOnSpawn[iCiv]:
						iWarPlan = WarPlanTypes.WARPLAN_TOTAL
					teamCiv.declareWar(iLoopCiv, False, iWarPlan)
					
					if utils.getHumanID() == iCiv: data.iBetrayalTurns = 0
					
					
	def immuneMode(self, argsList): 
		pWinningUnit,pLosingUnit = argsList
		iLosingPlayer = pLosingUnit.getOwner()
		iUnitType = pLosingUnit.getUnitType()
		if iLosingPlayer < iNumMajorPlayers:
			if gc.getGame().getGameTurn() >= getTurnForYear(tBirth[iLosingPlayer]) and gc.getGame().getGameTurn() <= getTurnForYear(tBirth[iLosingPlayer])+2:
				if (pLosingUnit.getX(), pLosingUnit.getY()) == Areas.getCapital(iLosingPlayer):
					print("new civs are immune for now")
					if gc.getGame().getSorenRandNum(100, 'immune roll') >= 50:
						utils.makeUnit(iUnitType, iLosingPlayer, (pLosingUnit.getX(), pLosingUnit.getY()), 1)

	def initMinorBetrayal( self, iCiv ):
		iHuman = utils.getHumanID()
		lPlots = Areas.getBirthArea(iCiv)
		plotList = utils.listSearch(lPlots, utils.outerInvasion, [])
		if plotList:
			tPlot = utils.getRandomEntry(plotList)
			if tPlot:
				self.createAdditionalUnits(iCiv, tPlot)
				self.unitsBetrayal(iCiv, iHuman, lPlots, tPlot)

	def initBetrayal( self ):
		iFlipPlayer = data.iNewCivFlip
		if not gc.getPlayer(iFlipPlayer).isAlive() or not gc.getTeam(iFlipPlayer).isAtWar(utils.getHumanID()):
			data.iBetrayalTurns = 0
			return
	
		iHuman = utils.getHumanID()
		turnsLeft = data.iBetrayalTurns
		
		lTempPlots = [(x, y) for (x, y) in data.lTempPlots if not gc.getMap().plot(x, y).isCore(data.iOldCivFlip)]
		plotList = utils.listSearch(lTempPlots, utils.outerInvasion, [] )
		if not plotList:
			plotList = utils.listSearch(lTempPlots, utils.innerSpawn, [data.iOldCivFlip, data.iNewCivFlip] )			
		if not plotList:
			plotList = utils.listSearch(lTempPlots, utils.innerInvasion, [data.iOldCivFlip, data.iNewCivFlip] )				
		if plotList:
			tPlot = utils.getRandomEntry(plotList)
			if tPlot:
				if turnsLeft == iBetrayalPeriod:
					self.createAdditionalUnits(data.iNewCivFlip, tPlot)
				self.unitsBetrayal(data.iNewCivFlip, data.iOldCivFlip, lTempPlots, tPlot)
		data.iBetrayalTurns = turnsLeft - 1



	def unitsBetrayal( self, iNewOwner, iOldOwner, lPlots, tPlot):
		if gc.getPlayer(data.iOldCivFlip).isHuman():
			CyInterface().addMessage(data.iOldCivFlip, False, iDuration, CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
		elif gc.getPlayer(data.iNewCivFlip).isHuman():
			CyInterface().addMessage(data.iNewCivFlip, False, iDuration, CyTranslator().getText("TXT_KEY_FLIP_BETRAYAL_NEW", ()), "", 0, "", ColorTypes(iGreen), -1, -1, True, True)
		for (x, y) in lPlots:
			killPlot = gc.getMap().plot(x,y)
			if killPlot.isCore(iOldOwner) and not killPlot.isCore(iNewOwner): continue
			iNumUnitsInAPlot = killPlot.getNumUnits()
			if iNumUnitsInAPlot > 0:
				for iUnit in reversed(range(iNumUnitsInAPlot)):
					unit = killPlot.getUnit(iUnit)
					if unit.getOwner() == iOldOwner:
						rndNum = gc.getGame().getSorenRandNum(100, 'betrayal')
						if rndNum >= iBetrayalThreshold:
							if unit.getDomainType() == DomainTypes.DOMAIN_LAND:
								iUnitType = unit.getUnitType()
								unit.kill(False, iNewOwner)
								utils.makeUnit(iUnitType, iNewOwner, tPlot, 1)

	def createAdditionalUnits(self, iCiv, tPlot):
		#MacAurther TODO
		if iCiv == iSpain:
			pass
		elif iCiv == iFrance:
			pass
		elif iCiv == iEngland:
			pass
		elif iCiv == iAmerica:
			pass
		elif iCiv == iCanada:
			pass


	def createStartingUnits(self, iCiv, tPlot):
		if iCiv == iSpain:
			pass
		elif iCiv == iFrance:
			pass
		elif iCiv == iEngland:
			pass
		elif iCiv == iVirginia:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iCrossbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(iPikeman, iCiv, tPlot, 1)
			utils.makeUnitAI(iExplorer, iCiv, tPlot, UnitAITypes.UNITAI_EXPLORE, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			utils.makeUnit(iCaravel, iCiv, tSeaPlot, 1)
			pVirginia.setLastStateReligion(iEpiscopalianism)
			utils.createMissionaries(iCiv, 1)
		elif iCiv == iMassachusetts:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iCrossbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(iPikeman, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			utils.makeUnit(iCaravel, iCiv, tSeaPlot, 1)
			pMassachusetts.setLastStateReligion(iPuritanism)
			utils.createMissionaries(iCiv, 1)
		elif iCiv == iNewHampshire:
			utils.createSettlers(iCiv, 1)
			utils.makeUnitAI(iCrossbowman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(iPikeman, iCiv, tPlot, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			utils.makeUnit(iCaravel, iCiv, tSeaPlot, 1)
			pNewHampshire.setLastStateReligion(iPuritanism)
			utils.createMissionaries(iCiv, 1)
		elif iCiv == iMaryland:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iMusketman, iCiv, tPlot, 1)
			utils.makeUnitAI(iMusketman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnitAI(iExplorer, iCiv, tPlot, UnitAITypes.UNITAI_EXPLORE, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			utils.makeUnit(iCaravel, iCiv, tSeaPlot, 1)
			utils.makeUnit(iWorkboat, iCiv, tSeaPlot, 1)
			pMaryland.setLastStateReligion(iCatholicism)
			utils.createMissionaries(iCiv, 1)
		elif iCiv == iConnecticut:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iMusketman, iCiv, tPlot, 1)
			utils.makeUnitAI(iMusketman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			pConnecticut.setLastStateReligion(iPuritanism)
			utils.createMissionaries(iCiv, 1)
		elif iCiv == iRhodeIsland:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iMusketman, iCiv, tPlot, 1)
			utils.makeUnitAI(iMusketman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			utils.makeUnit(iCaravel, iCiv, tSeaPlot, 1)
			pRhodeIsland.setLastStateReligion(iBaptism)
			utils.createMissionaries(iCiv, 1)
		elif iCiv == iNorthCarolina:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iMusketman, iCiv, tPlot, 2)
			utils.makeUnitAI(iMusketman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnitAI(iExplorer, iCiv, tPlot, UnitAITypes.UNITAI_EXPLORE, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			utils.makeUnit(iCaravel, iCiv, tSeaPlot, 1)
			pNorthCarolina.setLastStateReligion(iEpiscopalianism)
			utils.createMissionaries(iCiv, 2)
		elif iCiv == iSouthCarolina:
			utils.createSettlers(iCiv, 2)
			utils.makeUnit(iMusketman, iCiv, tPlot, 2)
			utils.makeUnitAI(iMusketman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnitAI(iExplorer, iCiv, tPlot, UnitAITypes.UNITAI_EXPLORE, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			utils.makeUnit(iCaravel, iCiv, tSeaPlot, 1)
			pSouthCarolina.setLastStateReligion(iEpiscopalianism)
			utils.createMissionaries(iCiv, 2)
		elif iCiv == iNewJersey:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iMusketman, iCiv, tPlot, 1)
			utils.makeUnitAI(iMusketman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			pNewJersey.setLastStateReligion(iEpiscopalianism)
			utils.createMissionaries(iCiv, 1)
		elif iCiv == iNewYork:
			utils.createSettlers(iCiv, 2)
			utils.makeUnit(iMusketman, iCiv, tPlot, 3)
			utils.makeUnitAI(iMusketman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnit(iExplorer, iCiv, tPlot, 1)
			utils.makeUnitAI(iExplorer, iCiv, tPlot, UnitAITypes.UNITAI_EXPLORE, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			utils.makeUnit(iCaravel, iCiv, tSeaPlot, 1)
			pNewYork.setLastStateReligion(iEpiscopalianism)
			utils.createMissionaries(iCiv, 2)
		elif iCiv == iPennsylvania:
			utils.createSettlers(iCiv, 3)
			utils.makeUnit(iMusketman, iCiv, tPlot, 3)
			utils.makeUnitAI(iMusketman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnitAI(iExplorer, iCiv, tPlot, UnitAITypes.UNITAI_EXPLORE, 1)
			pPennsylvania.setLastStateReligion(iPuritanism)
			utils.createMissionaries(iCiv, 3)
		elif iCiv == iDelaware:
			utils.createSettlers(iCiv, 1)
			utils.makeUnit(iMusketman, iCiv, tPlot, 1)
			utils.makeUnitAI(iMusketman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			utils.makeUnit(iCaravel, iCiv, tSeaPlot, 1)
			pDelaware.setLastStateReligion(iEpiscopalianism)
			utils.createMissionaries(iCiv, 1)
		elif iCiv == iGeorgia:
			utils.createSettlers(iCiv, 2)
			utils.makeUnit(iMusketman, iCiv, tPlot, 2)
			utils.makeUnitAI(iMusketman, iCiv, tPlot, UnitAITypes.UNITAI_CITY_DEFENSE, 1)
			utils.makeUnitAI(iExplorer, iCiv, tPlot, UnitAITypes.UNITAI_EXPLORE, 1)
			tSeaPlot = self.findSeaPlots(tPlot, 1, iCiv)
			utils.makeUnit(iCaravel, iCiv, tSeaPlot, 1)
			pGeorgia.setLastStateReligion(iMethodism)
			utils.createMissionaries(iCiv, 2)


		elif iCiv == iAmerica:
			pass
		elif iCiv == iCanada:
			pass
				
		# Leoreth: start wars on spawn when the spawn actually happens
		self.startWarsOnSpawn(iCiv)
		
		# MacAurther TODO: Find a better spot for this call:
		self.initialDiplomacy(iCiv)

	def initialDiplomacy(self, iCiv):
		tCiv = gc.getTeam(iCiv)
		
		print("Setting up colonial vassal relationships for: " + str(iCiv))
		# Set up Vassal colonial relationships
		if iCiv in range(iVirginia, iGeorgia + 1):
			if not tCiv.canContact(iEngland): tCiv.meet(iEngland, False)
			if not tCiv.isVassal(iEngland): tCiv.setVassal(iEngland, True, False)


	def createRespawnUnits(self, iCiv, tPlot):
		pass
	
	def findAreaReligion(self, iPlayer, lPlots):
		lReligions = [0 for i in range(iNumReligions)]
		
		for (x, y) in lPlots:
			plot = gc.getMap().plot(x, y)
			if plot.isCity():
				city = plot.getPlotCity()
				iOwner = city.getOwner()
				if iOwner != iPlayer:
					for iReligion in range(iNumReligions):
						if city.isHasReligion(iReligion):
							lReligions[iReligion] += 1
					iStateReligion = gc.getPlayer(iOwner).getStateReligion()
					if iStateReligion >= 0:
						lReligions[iStateReligion] += 1
						
		iMax = 0
		iHighestReligion = -1
		for i in range(iNumReligions):
			iLoopReligion = (iJudaism + i) % iNumReligions
			if lReligions[iLoopReligion] > iMax:
				iMax = lReligions[iLoopReligion]
				iHighestReligion = iLoopReligion
				
		return iHighestReligion

				
	def createStartingWorkers( self, iCiv, tPlot ):
		if iCiv == iVirginia:
			utils.makeUnit(iWorker, iCiv, tPlot, 1)
		elif iCiv == iMassachusetts:
			utils.makeUnit(iWorker, iCiv, tPlot, 1)
		elif iCiv == iNewHampshire:
			utils.makeUnit(iWorker, iCiv, tPlot, 1)
		elif iCiv == iMaryland:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iConnecticut:
			utils.makeUnit(iWorker, iCiv, tPlot, 1)
		elif iCiv == iRhodeIsland:
			utils.makeUnit(iWorker, iCiv, tPlot, 1)
		elif iCiv == iNorthCarolina:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iSouthCarolina:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iNewJersey:
			utils.makeUnit(iWorker, iCiv, tPlot, 2)
		elif iCiv == iNewYork:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iPennsylvania:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iDelaware:
			utils.makeUnit(iWorker, iCiv, tPlot, 1)
		elif iCiv == iGeorgia:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
		elif iCiv == iAmerica:
			utils.makeUnit(iWorker, iCiv, tPlot, 4)
		elif iCiv == iCanada:
			utils.makeUnit(iWorker, iCiv, tPlot, 3)
			
	def create1770ADstartingUnits(self):
		#MacAurther TODO
		for iPlayer in range(iNumPlayers):
			tCapital = Areas.getCapital(iPlayer)

			if tBirth[iPlayer] > utils.getScenarioStartYear() and gc.getPlayer(iPlayer).isHuman():
				utils.makeUnit(iSettler, iPlayer, tCapital, 1)
				utils.makeUnit(iMilitia, iPlayer, tCapital, 1)
		pass

	def create1850ADstartingUnits( self ):
		#MacAurther TODO
		for iPlayer in range(iNumPlayers):
			tCapital = Areas.getCapital(iPlayer)

			if tBirth[iPlayer] > utils.getScenarioStartYear() and gc.getPlayer(iPlayer).isHuman():
				utils.makeUnit(iSettler, iPlayer, tCapital, 1)
				utils.makeUnit(iMilitia, iPlayer, tCapital, 1)
		pass


	def create1600ADstartingUnits(self):
		for iPlayer in range(iNumPlayers):
			tCapital = Areas.getCapital(iPlayer)

			if tBirth[iPlayer] > utils.getScenarioStartYear() and gc.getPlayer(iPlayer).isHuman():
				utils.makeUnit(iSettler, iPlayer, tCapital, 1)
				utils.makeUnit(iMilitia, iPlayer, tCapital, 1)
		
	def assignTechs(self, iPlayer):
		Civilizations.initPlayerTechs(iPlayer)
				
		sta.onCivSpawn(iPlayer)
				
	def determineEnabledPlayers(self):
	
		iHuman = utils.getHumanID()
		
				
	def placeHut(self, tTL, tBR):
		plotList = []
		
		for (x, y) in utils.getPlotList(tTL, tBR):
			plot = gc.getMap().plot(x, y)
			if plot.isFlatlands() or plot.isHills():
				if plot.getFeatureType() != iMud:
					if plot.getOwner() < 0:
						plotList.append((x, y))
		
		if not plotList:
			#utils.debugTextPopup('List empty: ' + str(tTL) + ' ' + str(tBR))
			return
		
		tPlot = utils.getRandomEntry(plotList)
		i, j = tPlot
		
		gc.getMap().plot(i, j).setImprovementType(iHut)
		
		#MacAurther TODO: These extra archers are messing with the Native player's AI, and any 
		# uprising event has the units just wander away. Solutions: makes Native Player 1 and 
		# Native Player 2? Make unit spawn contingent upon good hut collection?
		#FOB - Added native player 2 and random chance to spawn guard
		#MacAurther: Also place a defending archer on the hut to make more difficult to get (i.e. need to send a conquering force)
		iGuardResult = gc.getGame().getSorenRandNum(100, 'Hut guard chance')
		if iGuardResult < iGoodyHutGuardChance:
			utils.makeUnitAI(iArcher, iNative2, tPlot, UnitAITypes.UNITAI_DEFENSE, 1)
		
	def setStateReligion(self, iCiv):
		lCities = utils.getAreaCities(Areas.getCoreArea(iCiv))
		lReligions = [0 for i in range(iNumReligions)]
		
		for city in lCities:
			if city.getReligionCount() == 0:
				iOwner = city.getOwner()
				if iOwner == iCiv:
					iOwner = city.getPreviousOwner()

				if iOwner != -1:
					iReligion = gc.getPlayer(iOwner).getStateReligion()
					if iReligion >= 0:
						lReligions[iReligion] += 1
						continue
		
			for iReligion in range(iNumReligions):
				if iReligion not in [iJudaism] and city.isHasReligion(iReligion): lReligions[iReligion] += 1
				
		iHighestEntry = utils.getHighestEntry(lReligions)
		
		if iHighestEntry > 0:
			gc.getPlayer(iCiv).setLastStateReligion(lReligions.index(iHighestEntry))
			
rnf = RiseAndFall()