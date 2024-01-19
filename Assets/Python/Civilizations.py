from RFCUtils import *
from Core import *

from Events import events, handler

import GreatPeople as GP

### Unit spawn functions ###

def getStartingUnits(iPlayer):
	lStartingUnits = [(iRole, iAmount) for iRole, iAmount in dStartingUnits[iPlayer].items() if iRole != iWork]
	
	if not player(iPlayer).isHuman():
		lStartingUnits += dExtraAIUnits[iPlayer].items()
	
	return lStartingUnits
	
def getAdditionalUnits(iPlayer):
	return dAdditionalUnits[iPlayer].items()

def getSpecificAdditionalUnits(iPlayer):
	return dSpecificAdditionalUnits[iPlayer].items()

### Tech preference functions ###

def getTechPreferences(iPlayer):
	dPreferences = defaultdict({}, 0)
	iCivilization = civ(iPlayer)
	
	if iCivilization not in dTechPreferences:
		return dPreferences
		
	for iTech, iValue in dTechPreferences[iCivilization].items():
		dPreferences[iTech] = iValue
		
	for iTech, iValue in dTechPreferences[iCivilization].items():
		for i in range(4):
			iOrPrereq = infos.tech(iTech).getPrereqOrTechs(i)
			iAndPrereq = infos.tech(iTech).getPrereqAndTechs(i)
			
			if iOrPrereq < 0 and iAndPrereq < 0: break
			
			updatePrereqPreference(dPreferences, iOrPrereq, iValue)
			updatePrereqPreference(dPreferences, iAndPrereq, iValue)
	
	return dPreferences
	
def updatePrereqPreference(dPreferences, iPrereqTech, iValue):
	if iPrereqTech < 0: return
	
	iPrereqValue = dPreferences[iPrereqTech]
	
	if iValue > 0 and iPrereqValue >= 0:
		iPrereqValue = min(max(iPrereqValue, iValue), iPrereqValue + iValue / 2)
		
	elif iValue < 0 and iPrereqValue <= 0:
		iPrereqValue = max(min(iPrereqValue, iValue), iPrereqValue + iValue / 2)
		
	dPreferences[iPrereqTech] = iPrereqValue
	
def initPlayerTechPreferences(iPlayer):
	initTechPreferences(iPlayer, getTechPreferences(iPlayer))
	
def initTechPreferences(iPlayer, dPreferences):
	player(iPlayer).resetTechPreferences()

	for iTech, iValue in dPreferences.items():
		player(iPlayer).setTechPreference(iTech, iValue)

### Wonder preference methods ###

def initBuildingPreferences(iPlayer):
	pPlayer = player(iPlayer)
	iCiv = civ(iPlayer)
	
	pPlayer.resetBuildingClassPreferences()
	
	if iCiv in dBuildingPreferences:
		for iBuilding, iValue in dBuildingPreferences[iCiv].iteritems():
			pPlayer.setBuildingClassPreference(infos.building(iBuilding).getBuildingClassType(), iValue)
			
	if iCiv in dDefaultWonderPreferences:
		iDefaultPreference = dDefaultWonderPreferences[iCiv]
		for iWonder in range(iFirstWonder, iNumBuildings):
			if iCiv not in dBuildingPreferences or iWonder not in dBuildingPreferences[iCiv]:
				pPlayer.setBuildingClassPreference(infos.building(iWonder).getBuildingClassType(), iDefaultPreference)


### General functions ###
		
@handler("playerCivAssigned")
def onPlayerCivAssigned(iPlayer):
	initPlayerTechPreferences(iPlayer)
	initBuildingPreferences(iPlayer)
	

### Civilization starting attributes ###

class Civilization(object):

	def __init__(self, iCiv, **kwargs):
		self.iCiv = iCiv
	
		self.iLeader = kwargs.get("iLeader")
		self.iGold = kwargs.get("iGold")
		self.iStateReligion = kwargs.get("iStateReligion")
		self.iAdvancedStartPoints = kwargs.get("iAdvancedStartPoints")
		
		self.lCivics = kwargs.get("lCivics", [])
		self.lEnemies = kwargs.get("lEnemies", []) + [iNative, iBarbarian]
		
		self.dAttitudes = kwargs.get("dAttitudes", {})
		
		self.sLeaderName = kwargs.get("sLeaderName")
		
		self.techs = kwargs.get("techs", techs.none())
	
	@property
	def player(self):
		return player(self.iCiv)
	
	@property
	def team(self):
		return team(self.player.getTeam())
	
	@property
	def info(self):
		return infos.civ(self.iCiv)
	
	def isPlayable(self):
		return self.info.getStartingYear() != 0
	
	def apply(self):
		if not self.player.isHuman():
			if self.iLeader is not None:
				self.player.setLeader(self.iLeader)
		
			if self.sLeaderName is not None:
				self.player.setLeaderName(text(self.sLeaderName))
		
		if self.iGold is not None:
			self.player.changeGold(scale(self.iGold))
		
		if self.iStateReligion is not None:
			iOldStateReligion = self.player.getStateReligion()
			iNewStateReligion = self.iStateReligion
			
			if iNewStateReligion == iProtestantism and not game.isReligionFounded(iProtestantism):
				iNewStateReligion = iCatholicism
			
			if iNewStateReligion == iCatholicism and not game.isReligionFounded(iCatholicism):
				iNewStateReligion = iOrthodoxy
			
			if game.isReligionFounded(iNewStateReligion):
				self.player.setLastStateReligion(iNewStateReligion)
				events.fireEvent("playerChangeStateReligion", self.player.getID(), iNewStateReligion, iOldStateReligion)
		
		if self.techs:
			for iTech in self.techs:
				self.team.setHasTech(iTech, True, self.player.getID(), False, False)
			
			self.player.setStartingEra(self.player.getCurrentEra())
		
		for iCivic in self.lCivics:
			self.player.setCivics(infos.civic(iCivic).getCivicOptionType(), iCivic)
			
		for iEnemy in self.lEnemies:
			iEnemyPlayer = slot(iEnemy)
			if iEnemyPlayer >= 0 and self.iCiv != iEnemy:
				team(iEnemyPlayer).declareWar(self.player.getTeam(), False, WarPlanTypes.NO_WARPLAN)
		
		for iCiv, iAttitude in self.dAttitudes.items():
			self.player.AI_changeAttitudeExtra(slot(iCiv), iAttitude)
	
	def advancedStart(self):
		if self.iAdvancedStartPoints is not None:
			self.player.setAdvancedStartPoints(scale(self.iAdvancedStartPoints))
			
			if not self.player.isHuman():
				self.player.AI_doAdvancedStart()

lCivilizations = [
	Civilization(
		iMaya,
		iGold=50,
		techs=techs.column(2).including(iPottery, iAgriculture, iMythology).without(iTrapping, iPathfinding, iLinguistics, iLocalization, iShallowFishing, iFishing)
	),
	Civilization(
		iTeotihuacan,
		iGold=50,
		techs=techs.column(2).including(iTanning, iPottery, iAgriculture).without(iPathfinding, iLinguistics, iLocalization, iShallowFishing, iFishing)
	),
	Civilization(
		iZapotec,
		iGold=100,
		techs=techs.column(2).including(iPottery, iAgriculture, iMythology).without(iTrapping, iPathfinding, iLinguistics, iLocalization, iShallowFishing, iFishing)
	),
	Civilization(
		iTiwanaku,
		iGold=50,
		techs=techs.column(2).including(iAgriculture, iPastoralism, iMining, iMythology, iArithmetics).without(iHunting, iTrapping, iLinguistics, iLocalization, iShallowFishing, iFishing)
	),
	Civilization(
		iWari,
		iGold=100,
		techs=techs.column(3).without(iTrapping, iLinguistics, iLocalization, iShallowFishing, iFishing)
	),
	Civilization(
		iMississippi,
		iGold=25,
		techs=techs.column(2).including(iPottery, iAgriculture, iMythology, iSailing, iTanning).without(iLandmarks, iPathfinding, iLinguistics, iLocalization)
	),
	Civilization(
		iPuebloan,
		iGold=50,
		techs=techs.column(3).including(iMasonry).without(iTrapping, iLinguistics, iLocalization, iHerbalism, iShallowFishing, iFishing)
	),
	Civilization(
		iMuisca,
		iGold=200,
		lCivics=[iMerchantTrade],
		techs=techs.column(3).including(iMasonry, iSmelting).without(iTrapping, iIrrigation, iEarthworks, iLinguistics, iLocalization, iShallowFishing, iFishing)
	),
	Civilization(
		iNorse,
		iGold=50,
		lCivics=[iExpedition, iSerfdom, iMerchantTrade],
		techs=techs.column(8).including(iFishing).without(*lNativeTechs)
	),
	Civilization(
		iChimu,
		iGold=300,
		lCivics=[iDespotism, iCraftsmen, iMerchantTrade],
		techs=techs.column(4).including(iConstruction, iTrade).without(iHunting, iTrapping)
	),
	Civilization(
		iInuit,
		iGold=25,
		lCivics=[iCouncil],
		techs=techs.column(2).including(iTanning, iMythology, iSailing).without(iLandmarks, iPathfinding, iIrrigation, iEarthworks, iLinguistics, iLocalization, iCultivation, iCompanionPlanting, iHerbalism)
	),
	Civilization(
		iInca,
		iGold=700,
		lCivics=[iAristocracy, iSlavery, iMerchantTrade, iCasteSystem, iConquest],
		lEnemies=[iWari, iTiwanaku],
		techs=techs.column(4).including(iConstruction, iMathematics, iWriting, iTrade).without(iHunting, iTrapping, iShallowFishing, iFishing)
	),
	Civilization(
		iPurepecha,
		iGold=500,
		lCivics=[iDespotism, iCaptives, iTributaries],
		techs=techs.column(4).including(iAlloys, iConstruction, iMathematics, iWriting).without(iTrapping)
	),
	Civilization(
		iAztecs,
		iGold=600,
		lCivics=[iDespotism, iCaptives, iTributaries],
		lEnemies=[iTeotihuacan, iPurepecha],
		techs=techs.column(4).including(iWriting, iCalendar, iTrade, iPriesthood).without(iTrapping, iShallowFishing, iFishing)
	),
	Civilization(
		iIroquois,
		iGold=200,
		lCivics=[iHarmony],
		techs=techs.column(3).including(iProperty, iCeremony).without(iLandmarks, iPathfinding, iIrrigation, iEarthworks)
	),
	Civilization(
		iSpain,
		iGold=200,
		iStateReligion=iCatholicism,
		lCivics=[iExpedition, iMaritimeLaw, iEncomienda, iMerchantTrade, iGloriaInDeo, iConquest],
		techs=techs.column(9).without(*lNativeTechs)
	),
	Civilization(
		iPortugal,
		iGold=200,
		iStateReligion=iCatholicism,
		lCivics=[iExpedition, iProprietaries, iEncomienda, iMerchantTrade, iDivineRight, iTributaries],
		techs=techs.column(9).including(iDiplomacy, iLogistics, iExploration, iOptics, iOfficials).without(*lNativeTechs)
	),
	Civilization(
		iEngland,
		iGold=200,
		iStateReligion=iProtestantism,
		lCivics=[iCharterColony, iCommonLaw, iSerfdom, iMercantilism, iHaven],
		techs=techs.column(10).including(iShipbuilding, iCharter, iCommunity).without(*lNativeTechs)
	),
	Civilization(
		iFrance,
		iGold=150,
		iStateReligion=iCatholicism,
		lCivics=[iExpedition, iMaritimeLaw, iSerfdom, iMerchantTrade, iDivineRight],
		techs=techs.column(10).including(iShipbuilding, iFortification).without(*lNativeTechs)
	),
	Civilization(
		iNetherlands,
		iGold=600,
		iStateReligion=iProtestantism,
		lCivics=[iTradeCompany, iMaritimeLaw, iSerfdom, iMerchantTrade, iDivineRight],
		techs=techs.column(10).including(iEconomics, iShipbuilding).without(*lNativeTechs)
	),
	Civilization(
		iHawaii,
		iGold=200,
		lCivics=[iCaptives],
		techs=techs.column(2).including(iNavigation).without(iTanning)
	),
	Civilization(
		iRussia,
		iGold=200,
		iStateReligion=iOrthodoxy,
		lCivics=[iExpedition, iMaritimeLaw, iIndenturedServitude, iAgrarianism, iProfiteering],
		techs=techs.column(12).without(iLandmarks, iLinguistics, iPathfinding, iCultivation, iHerbalism)
	),
	Civilization(
		iAmerica,
		iGold=1500,
		iStateReligion=iProtestantism,
		lCivics=[iDemocracy, iConfederacy, iSlavery, iAgrarianism, iProfiteering, iHomesteads],
		lEnemies=[iEngland],
		techs=techs.column(14).including(iRepresentation, iIndependence, iSurveying)
	),
	Civilization(
		iHaiti,
		iGold=100,
		lCivics=[iMonarchy, iCommonLaw, iCraftsmen, iAgrarianism, iIsolationism],
		lEnemies=[iFrance],
		techs=techs.column(15)
	),
	Civilization(
		iArgentina,
		iGold=1200,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iConfederacy, iSlavery, iAgrarianism, iProfiteering, iHomesteads],
		lEnemies=[iSpain],
		techs=techs.column(15).including(iGeology)
	),
	Civilization(
		iMexico,
		iGold=500,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iCommonLaw, iSlavery, iAgrarianism, iProfiteering, iHomesteads],
		lEnemies=[iSpain],
		techs=techs.column(15)
	),
	Civilization(
		iColombia,
		iGold=750,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iFederalism, iSlavery, iAgrarianism, iProfiteering, iHomesteads],
		lEnemies=[iSpain],
		techs=techs.column(15).including(iRightsOfMan)
	),
	Civilization(
		iPeru,
		iGold=1200,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iFederalism, iSlavery, iAgrarianism, iProfiteering, iHomesteads],
		lEnemies=[iSpain],
		techs=techs.column(15).including(iGeology)
	),
	Civilization(
		iBrazil,
		iGold=1600,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iFederalism, iSlavery, iAgrarianism, iProfiteering, iHomesteads],
		techs=techs.column(15).including(iMetallurgy, iProtectionism, iHydrology)
	),
	Civilization(
		iVenezuela,
		iGold=1200,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iFederalism, iSlavery, iAgrarianism, iProfiteering, iHomesteads],
		lEnemies=[iColombia],
		techs=techs.column(15).including(iGeology)
	),
	Civilization(
		iCanada,
		iGold=1000,
		iStateReligion=iProtestantism,
		lCivics=[iMonarchy, iFederalism, iIndustrialism, iFreeEnterprise, iOpportunity, iHomesteads],
		techs=techs.column(18)
	),
]

### Starting units ###

dStartingUnits = CivDict({
	iTiwanaku: {
		iSettle: 1,
		iWork: 1,
		iDefend: 1,
	},
	iWari: {
		iSettle: 1,
		iWork: 1,
		iDefend: 2,
	},
	iMississippi: {
		iSettle: 2,
		iWork: 1,
		iDefend: 2,
	},
	iPuebloan: {
		iSettle: 1,
		iWork: 1,
		iDefend: 1,
		iRecon: 1,
	},
	iMuisca: {
		iSettle: 1,
		iWork: 1,
		iDefend: 2,
		iBase: 1,
	},
	iNorse: {
	},
	iChimu: {
		iSettle: 2,
		iWork: 1,
		iDefend: 2,
		iBase: 1,
		iShock: 1,
	},
	iInuit: {
		iSettle: 2,
		iDefend: 2,
	},
	iInca: {
		iSettle: 1,
		iWork: 4,
		iDefend: 3,
		iBase: 3,
		iShock: 6,
		iHarass: 3,
		# if not human: 1 Settler
	},
	iPurepecha: {
		iSettle: 2,
		iWork: 2,
		iDefend: 3,
		iBase: 2,
		iShock: 4,
		iHarass: 2,
	},
	iAztecs: {
		iSettle: 2,
		iWork: 3,
		iDefend: 3,
		iBase: 4,
		iShock: 6,
		iHarass: 3,
	},
	iIroquois: {
		iSettle: 1,
		iWork: 1,
		iDefend: 1,
		iBase: 1,
		iShock: 1,
		iHarass: 1,
	},
	iSpain: {
	},
	iPortugal: {
	},
	iEngland: {
	},
	iFrance: {
	},
	iNetherlands: {
	},
	iHawaii: {
		iSettle: 2,
		iWork: 1,
		iDefend: 2,
		iBase: 2,
		iFerrySea: 1,
	},
	iRussia: {
	},
	iAmerica: {
		iSettle: 8,
		iWork: 5,
		iDefend: 4,
		iBase: 4,
		iShock: 4,
		iSiege: 2,
		iHarass: 2,
		iSiegeCity: 2,
		iWorkSea: 2,
		iFerrySea: 2,
		iEscortSea: 1,
		iMissionary: 3,
	},
	iHaiti: {
		iSettle: 1,
		iWork: 3,
		iDefend: 3,
		iBase: 2,
	},
	iArgentina: {
		iSettle: 5,
		iWork: 4,
		iDefend: 3,
		iBase: 4,
		iShock: 3,
		iSiege: 2,
		iShockCav: 2,
		iSiegeCity: 1,
		iMissionary: 2,
		iFerrySea: 1,
		iEscortSea: 2,
	},
	iMexico: {
		iSettle: 8,
		iWork: 3,
		iDefend: 4,
		iBase: 4,
		iShock: 4,
		iHarass: 2,
		iShockCav: 2,
		iSiegeCity: 3,
		iMissionary: 1,
	},
	iColombia: {
		iSettle: 4,
		iWork: 3,
		iDefend: 3,
		iBase: 3,
		iShock: 4,
		iSiege: 2,
		iSiegeCity: 3,
		iMissionary: 1,
	},
	iPeru: {
		iSettle: 3,
		iWork: 3,
		iDefend: 3,
		iBase: 3,
		iShock: 4,
		iSiege: 1,
		iSiegeCity: 2,
		iMissionary: 1,
		iFerrySea: 1,
		iEscortSea: 1,
	},
	iBrazil: {
		iSettle: 8,
		iWork: 3,
		iDefend: 4,
		iBase: 3,
		iHarass: 3,
		iSiege: 1,
		iSiegeCity: 2,
		iMissionary: 1,
		iWorkSea: 2,
		iFerrySea: 2,
		iEscortSea: 3,
	},
	iVenezuela: {
		iSettle: 3,
		iWork: 2,
		iDefend: 3,
		iBase: 3,
		iShock: 3,
		iSiege: 1,
		iSiegeCity: 1,
		iMissionary: 1,
		iFerrySea: 1,
		iEscortSea: 1,
	},
	iCanada: {
		iSettle: 8,
		iWork: 3,
		iDefend: 6,
		iBase: 5,
		iShock: 3,
		iHarassCav: 2,
		iMissionary: 1,
	},
}, {})

# Extra units for AI
dExtraAIUnits = CivDict({
	iAmerica: {
		iBase: 1,
	},
	iArgentina: {
		iBase: 3,
		iShock: 2,
		iSiege: 2,
	},
	iBrazil: {
		iBase: 1,
	}
}, {})

# Extra units if civ starts at war
dAdditionalUnits = CivDict({
	iMaya: {
		iBase: 2,
		iShock: 2,
	},
	iInca: {
		iShock: 5,
		iBase: 3,
	},
	iAztecs: {
		iShock: 5,
		iBase: 3,
	},
	iAmerica: {
		iShock: 3,
		iHarass: 3,
		iSiege: 2,
		iSiegeCity: 1,
	},
	iArgentina: {
		iShock: 2,
		iShockCav: 4,
	},
	iMexico: {
		iShock: 4,
		iSiege: 1,
		iSiegeCity: 1,
	},
	iColombia: {
		iShock: 4,
		iHarass: 4,
		iSiege: 1,
		iSiegeCity: 1,
	},
	iBrazil: {
		iShock: 3,
		iHarass: 2,
		iSiege: 1,
		iSiegeCity: 1,
	},
	iCanada: {
		iShock: 4,
		iShockCav: 2,
		iSiege: 1,
		iSiegeCity: 1,
	},
}, {})

dStartingExperience = CivDict({
	iArgentina: {
		iShockCav: 2,
		iShock: 2,
		iBase: 2,
		iSiege: 2,
	},
	iMexico: {
		iShock: 2,
		iBase: 2,
		iShockCav: 2,
		iHarass: 2,
	},
	iColombia: {
		iShock: 2,
		iHarass: 2,
		iSiege: 1,
		iSiegeCity: 1,
	},
}, {})

dAlwaysTrain = CivDict({
	iAztecs: [iJaguar],
	iMexico: [iGrenadier],
	iColombia: [iAlbionLegion],
	iBrazil: [iGrenadier],
}, [])

dAIAlwaysTrain = CivDict({
	iSpain: [iMusketman],
	iFrance: [iMusketman],
	iEngland: [iMusketman],
}, [])

dNeverTrain = CivDict({
}, [])

def createSpecificUnits(iPlayer, tile):
	iCiv = civ(iPlayer)
	bHuman = player(iPlayer).isHuman()
	
	if iCiv == iInca:
		if not bHuman:
			makeUnit(iPlayer, iSettler, tile)
	elif iCiv == iAmerica:	# American UP
		unit = makeUnit(iPlayer, iGreatStatesman, tile)
		GP.assignGreatPersonName(unit, iPlayer, None, False)
		unit = makeUnit(iPlayer, iGreatGeneral, tile)
		GP.assignGreatPersonName(unit, iPlayer, None, False)
		unit = makeUnit(iPlayer, iGreatScientist, tile)
		GP.assignGreatPersonName(unit, iPlayer, None, False)
		unit = makeUnit(iPlayer, iGreatMerchant, tile)
		GP.assignGreatPersonName(unit, iPlayer, None, False)
		unit = makeUnit(iPlayer, iGreatArtist, tile)
		GP.assignGreatPersonName(unit, iPlayer, None, False)
	elif iCiv == iColombia:
		makeUnits(iPlayer, iAlbionLegion, tile, 5).experience(2)

dSpecificAdditionalUnits = CivDict({
}, {})


### Tech Preferences ###

dTechPreferences = {
	iMaya : {
		iMathematics : 40,
		iCalendar: 40,
		iAesthetics: 30,
	},
	iZapotec : {
		iWriting: 40,
	},
	iSpain : {
		iCartography: 100,
		iExploration: 100,
		iFirearms: 100,
		iReplaceableParts: 30,
		iGunpowder: 15,
		iChemistry: 15,
	},
	iFrance : {
		iReplaceableParts: 30,
		iFirearms: 20,
		iExploration: 20,
		iGeography: 20,
		iLogistics: 20,
		iMeasurement: 20,
		iAcademia: 20,
		iEducation: 15,
		iChemistry: 15,
		iSociology: 15,
	},
	iEngland : {
		iExploration: 40,
		iGeography: 40,
		iFirearms: 40,
		iReplaceableParts: 30,
		iLogistics: 30,
		iCivilLiberties: 20,
		iEducation: 15,
		iChemistry: 15,
	},
	iPortugal : {
		iCartography: 100,
		iExploration: 100,
		iGeography: 100,
		iFirearms: 100,
		iCompanies: 50,
		iReplaceableParts: 20,
	},
	iInca : {
		iConstruction: 40,
		iCalendar: 40,
		iGunpowder: -20,
	},
	iAztecs : {
		iConstruction: 40,
		iGunpowder: -20,
	},
	iNetherlands : {
		iExploration: 20,
		iFirearms: 20,
		iOptics: 20,
		iGeography: 20,
		iReplaceableParts: 20,
		iLogistics: 20,
		iEconomics: 20,
		iCivilLiberties: 20,
		iHumanities: 20,
		iAcademia: 20,
		iChemistry: 15,
	},
	iAmerica : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
	},
	iArgentina : {
	},
	iBrazil : {
		iElectricity: 20,
	},
}

### Building Preferences ###

dDefaultWonderPreferences = {
	iFrance: -12,
	iEngland: -12,
	iNetherlands: -12,
	iAmerica: -12,
}

dBuildingPreferences = {
	iMaya : {
		iTempleOfKukulkan: 40,
		iMachuPicchu: -40,
		iSerpentMound: -40,
	},
	iTeotihuacan : {
		iTlachihualtepetl: 40,
		iSerpentMound: -40,
	},
	iTiwanaku : {
		iGateOfTheSun: 40,
		iSerpentMound: -40,
	},
	iWari : {
		iSerpentMound: -40,
	},
	iMississippi : {
		iSerpentMound: 40,
	},
	iPuebloan : {
		iSerpentMound: -40,
	},
	iMuisca : {
		iSerpentMound: -40,
	},
	iChimu : {
		iSerpentMound: -40,
	},
	iInca : {
		iMachuPicchu: 40,
		iSacsayhuaman: 40,
		iSerpentMound: -40,
	},
	iAztecs : {
		iFloatingGardens: 40,
		iHueyTeocalli: 30,
		iMachuPicchu: -40,
		iSerpentMound: -40,
	},
	iSpain : {
		iTemblequeAqueduct: 20,
		iLaFortaleza: 40,
		iGuadalupeBasilica: 30,
		iChapultepecCastle: 30,
		iCristoRedentor: 20,
	},
	iPortugal : {
		iSaoFranciscoSquare: 40,
		iCristoRedentor: 20,
	},
	iEngland : {
		iTradingCompanyBuilding: 50,
		iNationalGallery: 20,
	},
	iFrance : {
		iChateauFrontenac: 20,
		iFrenchQuarter: 20,
		iTradingCompanyBuilding: 40,
	},
	iNetherlands : {
		iTradingCompanyBuilding: 60,
	},
	iAmerica : {
		iIndendenceHall: 40,
		iMountVernon: 20,
		iMonticello: 20,
		iWestPoint: 20,
		iFortMcHenry: 20,
		iWashingtonMonument: 40,
		iFaneuilHall: 20,
		iCentralPark: 20,
		iEllisIsland: 20,
		iStatueOfLiberty: 30,
		iPentagon: 30,
		iBrooklynBridge: 30,
		iGoldenGateBridge: 30,
		iMenloPark: 20,
		iBiltmoreEstate: 20,
		iLeagueOfNations: 20,
	},
	iMexico : {
		iGuadalupeBasilica: 40,
		iChapultepecCastle: 40,
	},
	iArgentina : {
		iGuadalupeBasilica: 30,
	},
	iColombia : {
		iGuadalupeBasilica: 30,
	},
	iBrazil : {
		iCristoRedentor: 30,
	},
	iCanada : {
		iChateauFrontenac: 30,
	}
}