from Resources import setupScenarioResources
from DynamicCivs import checkName
from Slots import findSlot, addPlayer
from GoalHandlers import event_handler_registry
from Periods import dScenarioPeriods, setPeriod

from Core import *
from RFCUtils import *
from Civilizations import *
from Parsers import *


START_HISTORY = -500

LEADER_DATES = {
	# Maya
	iPacal: 100,
	# Zapotec
	iCosijoeza: 300,
	# Teotihuacan
	iAtlatlCauac: -100,
	# Tiwanaku
	iMalkuHuyustus: 110,
	# Wari
	iWariCapac: 500,
	# Mississippi
	iRedHorn: 500,
	# Puebloan
	iItzukuma: 750,
	# Muisca
	iSaguamanchica: 750,
	# Norse
	iRagnar: 1000,
	iGustav: 1600,
	iGerhardsen: 1940,
	# Chimu
	iTacaynamo: 1000,
	# Inuit
	iAua: 1000,
	# Inca
	iHuaynaCapac: 1400,
	iPachacuti: 1500,
	# Purepecha
	iTariacuri: 1150,
	# Aztecs
	iMontezuma: 1440,
	# Iroquois
	iHiawatha: 1350,
	# Lakota
	iSittingBull: 1450,
	# Spain
	iIsabella: 1480,
	iPhilip: 1560,
	# Portugal
	iJoao: 1490,
	iMaria: 1830,
	# England
	iElizabeth: 1600,
	iVictoria: 1840,
	iChurchill: 1940,
	# France
	iLouis: 1600,
	iNapoleon: 1800,
	iDeGaulle: 1950,
	# Netherlands
	iWillemVanOranje: 1570,
	iWilliam: 1650,
	# Hawaii
	iKamehameha: 1650,
	# Russia
	iCatherine: 1700,
	iAlexanderI: 1890,
	iStalin: 1930,
	# America
	iWashington: 1790,
	iJackson: 1820,
	iLincoln: 1860,
	iRoosevelt: 1900,
	iFDR: 1940,
	iKennedy: 1960,
	iReagan: 1980,
	iObama: 2000,
	# Haiti
	iLOuverture: 1800,
	# Bolivia
	
	# Argentina
	iSanMartin: 1820,
	iPeron: 1950,
	# Mexico
	iJuarez: 1860,
	iSantaAnna: 1850,
	iCardenas: 1940,
	# Colombia
	iBolivar: 1820,
	# Chile
	
	# Peru
	iCastilla: 1820,
	# Venezuela
	iChavez: 1980,
	# Brazil
	iPedro: 1840,
	iVargas: 1930,
	# Canada
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

DEFAULT_CIV_DESCRIPTIONS = {}


@handler("fontsLoaded")
def loadCivDescriptions():
	global DEFAULT_CIV_DESCRIPTIONS
	DEFAULT_CIV_DESCRIPTIONS = dict((iCiv, infos.civ(iCiv).getDescriptionKeyPersistent()) for iCiv in infos.civs())

class Revealed(object):

	def __init__(self, *args, **kwargs):
		self.lLandRegions = kwargs.get("lLandRegions", [])
		self.lCoastRegions = kwargs.get("lCoastRegions", [])
		self.lSeaAreas = kwargs.get("lSeaAreas", [])
	
	def getArea(self):	
		landPlots = plots.regions(*self.lLandRegions).where(CyPlot.isOwned)
		coastPlots = plots.regions(*self.lCoastRegions).coastal().expand(1).water()
		seaPlots = plots.sum(plots.rectangle(*tArea) for tArea in self.lSeaAreas).water()
		
		return landPlots + coastPlots + seaPlots
			

class Scenario(object):

	def __init__(self, *args, **kwargs):
		self.iStartYear = kwargs.get("iStartYear")
		self.fileName = kwargs.get("fileName")
		
		self.lCivilizations = kwargs.get("lCivilizations", [])
		
		self.dCivilizationDescriptions = kwargs.get("dCivilizationDescriptions", {})
		
		self.dOwnedTiles = kwargs.get("dOwnedTiles", {})
		self.iCultureTurns = kwargs.get("iCultureTurns", 0)
		
		self.lTribalVillages = kwargs.get("lTribalVillages", [])
		
		self.dRevealed = kwargs.get("dRevealed", {})
		
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
		for iCiv, description in DEFAULT_CIV_DESCRIPTIONS.items():
			infos.civ(iCiv).setDescriptionKeyPersistent(description)
	
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
		
		self.updatePeriods()
		self.createStartingUnits()
		
		self.adjustTerritories()
		
		self.adjustReligions()
		self.adjustWonders()
		self.adjustGreatPeople()
		
		self.revealTiles()
		
		self.initDiplomacy()
		
		self.restoreCivs()
		self.restoreLeaders()
		
		self.updateNames()
	
	def adjustTerritories(self):
		for city in cities.all():
			for _ in range(turns(self.iCultureTurns)):
				city.doPlotCulture(False, city.getOwner(), city.getModifiedCultureRate(), True)
		
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

	def revealTiles(self):
		for iGroup, revealed in self.dRevealed.items():
			revealedPlots = revealed.getArea()
			revealedPlots = revealedPlots.expand(1).unique()
			
			for iPlayer in players.group(iGroup):
				iTeam = player(iPlayer).getTeam()
				for plot in revealedPlots + plots.birth(iPlayer) + plots.core(iPlayer):
					plot.setRevealed(iTeam, True, False, -1)
	
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
	
	def updatePeriods(self):
		for iYear, dPeriods in dScenarioPeriods.items():
			if self.iStartYear >= iYear:
				for iCiv, iPeriod in dPeriods.items():
					setPeriod(iCiv, iPeriod)
