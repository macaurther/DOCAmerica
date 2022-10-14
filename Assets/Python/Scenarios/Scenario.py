from Resources import setupScenarioResources
from DynamicCivs import checkName
from Slots import findSlot, addPlayer
from GoalHandlers import event_handler_registry

from Core import *
from RFCUtils import *
from Parsers import *


START_HISTORY = 250

LEADER_DATES = {
	iPacal: 250,
	iIsabella: 1480,
	iPhilip: 1560,
	iCharlemagne: 770,
	iLouis: 1650,
	iNapoleon: 1800,
	iDeGaulle: 1950,
	iAlfred: 880,
	iElizabeth: 1560,
	iVictoria: 1840,
	iChurchill: 1940,
	iAfonso: 1140,
	iJoao: 1490,
	iMaria: 1830,
	iHuaynaCapac: 1500,
	iMontezuma: 1440,
	iWillemVanOranje: 1570,
	iWilliam: 1650,
	iWashington: 1790,
	iLincoln: 1860,
	iRoosevelt: 1940,
	iSanMartin: 1820,
	iPeron: 1950,
	iJuarez: 1860,
	iSantaAnna: 1850,
	iCardenas: 1940,
	iBolivar: 1820,
	iPedro: 1840,
	iVargas: 1930,
	iMacDonald: 1870,
	iTrudeau: 1970,
}

RELIGION_FOUNDING_DATES = {
	iJudaism: -2000,
	iOrthodoxy: 40,
	iCatholicism: 500,
	iProtestantism: 1521,
	iIslam: 622,
	iHinduism: -1500,
	iBuddhism: 80,
	iConfucianism: -500,
	iTaoism: -400,
	iZoroastrianism: -600
}

WONDER_ORIGINAL_BUILDERS = {
	iTempleOfKukulkan : (iMaya, 800),
	iFloatingGardens : (iAztecs, 1350),
}

class Scenario(object):

	def __init__(self, *args, **kwargs):
		self.iStartYear = kwargs.get("iStartYear")
		self.fileName = kwargs.get("fileName")
		
		self.lCivilizations = kwargs.get("lCivilizations", [])
		
		self.dCivilizationDescriptions = kwargs.get("dCivilizationDescriptions", {})
		
		self.dOwnedTiles = kwargs.get("dOwnedTiles", {})
		self.iOwnerBaseCulture = kwargs.get("iOwnerBaseCulture", 0)
		
		self.dGreatPeopleCreated = kwargs.get("dGreatPeopleCreated", {})
		self.dGreatGeneralsCreated = kwargs.get("dGreatGeneralsCreated", {})
		
		self.dColonistsAlreadyGiven = kwargs.get("dColonistsAlreadyGiven", {})
		
		self.lInitialWars = kwargs.get("lInitialWars", [])
		
		self.lAllGoalsFailed = kwargs.get("lAllGoalsFailed", [])
		self.lGoalsSucceeded = kwargs.get("lGoalsSucceeded", [])
		self.setupGoals = kwargs.get("setupGoals", lambda *args: None)
		
		self.createStartingUnits = kwargs.get("createStartingUnits", lambda: None)
	
	def adjustTurns(self, bFinal=True):
		iStartTurn = getGameTurnForYear(self.iStartYear, START_HISTORY, game.getCalendar(), game.getGameSpeedType())
		
		game.setStartYear(START_HISTORY)
		game.setStartTurn(iStartTurn)
		game.setGameTurn(iStartTurn)
		
		if bFinal:
			game.setMaxTurns(game.getEstimateEndTurn() - iStartTurn)
		
	def setupCivilizations(self):
		for iCiv, description in self.dCivilizationDescriptions.items():
			infos.civ(iCiv).setDescriptionKeyPersistent(description)
	
		for i, iCiv in enumerate(lBirthOrder):
			infos.civ(iCiv).setDescription("%02d" % i)
			
		for iCiv in range(iNumCivs):
			iCivStartYear = infos.civ(iCiv).getStartingYear()
			infos.civ(iCiv).setPlayable(iCivStartYear != 0 and iCivStartYear >= self.iStartYear)
		
		for civ in self.lCivilizations:
			civ.info.setPlayable(civ.isPlayable())
	
	def setupLeaders(self):
		self.adjustTurns(False)
	
		for iCiv in range(iNumCivs):
			leaders = infos.leaders().where(lambda iLeader: infos.civ(iCiv).isOriginalLeader(iLeader) and iLeader in LEADER_DATES).sort(lambda iLeader: LEADER_DATES.get(iLeader, 2020))
			if not leaders:
				continue
			
			before, after = leaders.split(lambda iLeader: LEADER_DATES.get(iLeader, 2020) < self.iStartYear)
			if not after or (before and since(year(LEADER_DATES.get(before.last(), 2020))) < until(year(LEADER_DATES.get(after.first(), 2020)))):
				after = after.including(before.last())
				
			for iLeader in range(iNumLeaders):
				infos.civ(iCiv).setLeader(iLeader, infos.civ(iCiv).isOriginalLeader(iLeader) and iLeader in after)
	
	def init(self):
		event_handler_registry.reset()
		
		for civ in self.lCivilizations:
			iCiv = civ.iCiv
			
			if game.getActiveCivilizationType() == iCiv:
				continue
			
			iPlayer = findSlot(iCiv)
			addPlayer(iPlayer, iCiv, bAlive=True, bMinor=not civ.isPlayable())
	
		events.fireEvent("playerCivAssigned", game.getActivePlayer(), game.getActiveCivilizationType())
		events.fireEvent("playerCivAssigned", gc.getBARBARIAN_PLAYER(), iBarbarian)

		data.dSlots[game.getActiveCivilizationType()] = game.getActivePlayer()
		data.dSlots[iBarbarian] = gc.getBARBARIAN_PLAYER()
	
	def initGoals(self, iPlayer, goals):
		iCiv = civ(iPlayer)
		
		if iCiv in self.lAllGoalsFailed:
			for goal in goals:
				goal.fail()
				
		for iGoalCiv, iGoalIndex in self.lGoalsSucceeded:
			if iCiv == iGoalCiv:
				goals[iGoalIndex].succeed()
		
		self.setupGoals(iCiv, goals)
		
	def apply(self):
		self.adjustTurns()
	
		for civilization in self.lCivilizations:
			civilization.apply()
		
		setupScenarioResources()
		
		self.createStartingUnits()
		
		self.adjustTerritories()
		
		self.adjustReligions()
		self.adjustWonders()
		self.adjustGreatPeople()
		self.adjustColonists()
		
		self.initDiplomacy()
		
		self.restoreCivs()
		self.restoreLeaders()
		
		self.updateNames()
	
	def adjustTerritories(self):
		for plot in plots.all():
			if plot.isOwned():
				plot.changeCulture(plot.getOwner(), self.iOwnerBaseCulture, False)
				convertPlotCulture(plot, plot.getOwner(), 100, False)
		
		for iCiv, lTiles in self.dOwnedTiles.items():
			for plot in plots.of(lTiles):
				convertPlotCulture(plot, slot(iCiv), 100, True)
	
	def adjustReligions(self):
		for iReligion, iFoundingYear in RELIGION_FOUNDING_DATES.items():
			if game.isReligionFounded(iReligion):
				game.setReligionGameTurnFounded(iReligion, year(iFoundingYear))
		
		game.setVoteSourceReligion(1, iCatholicism, False)
	
	def adjustWonders(self):
		for iWonder, (iCiv, iYear) in WONDER_ORIGINAL_BUILDERS.items():
			city = getBuildingCity(iWonder, False)
			iEarliestYear = game.getTurnYear(year(min(iYear, self.iStartYear)))
			if city:
				city.setBuildingOriginalOwner(iWonder, iCiv)
				city.setBuildingOriginalTime(iWonder, iEarliestYear)
			elif iYear < self.iStartYear:
				game.incrementBuildingClassCreatedCount(infos.building(iWonder).getBuildingClassType())
	
	def adjustGreatPeople(self):
		for iCiv, iGreatPeople in self.dGreatPeopleCreated.items():
			player(iCiv).changeGreatPeopleCreated(iGreatPeople)
		
		for iCiv, iGreatGenerals in self.dGreatGeneralsCreated.items():
			player(iCiv).changeGreatPeopleCreated(iGreatGenerals)
	
	def adjustColonists(self):
		iStartTurn = scenarioStartTurn()
		
		for iCiv, iColonists in self.dColonistsAlreadyGiven.items():
			data.players[iCiv].iExplorationTurn = iStartTurn
			data.players[iCiv].iColonistsAlreadyGiven = iColonists
	
	def initDiplomacy(self):
		for iAttacker, iDefender, iWarPlan in self.lInitialWars:
			team(iAttacker).declareWar(player(iDefender).getTeam(), False, iWarPlan)
	
	def restoreCivs(self):
		for iCiv in range(iNumCivs):
			infos.civ(iCiv).setPlayable(infos.civ(iCiv).getStartingYear() != 0)
	
	def restoreLeaders(self):
		for iCiv in range(iNumCivs):
			for iLeader in range(iNumLeaders):
				infos.civ(iCiv).setLeader(iLeader, infos.civ(iCiv).isOriginalLeader(iLeader))
	
	def updateNames(self):
		for iPlayer in players.major():
			checkName(iPlayer)
