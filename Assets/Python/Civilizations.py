from RFCUtils import *
from Core import *

from Events import events, handler


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
		techs=techs.column(1).including(iPottery, iAgriculture, iMythology)
	),
	Civilization(
		iTeotihuacan,
		iGold=50,
		techs=techs.column(1).including(iPottery, iAgriculture)
	),
	Civilization(
		iTiwanaku,
		iGold=50,
		techs=techs.column(1).including(iAgriculture, iPastoralism)
	),
	Civilization(
		iWari,
		iGold=100,
		lCivics=[iMerchantTrade],
		techs=techs.column(2)
	),
	Civilization(
		iMississippi,
		iGold=50,
		lCivics=[iCouncil, iSpecialization],
		techs=techs.column(2)
	),
	Civilization(
		iPuebloan,
		iGold=50,
		lCivics=[iCouncil],
		techs=techs.column(2).including(iMasonry).without(iSailing)
	),
	Civilization(
		iMuisca,
		iGold=200,
		lCivics=[iMerchantTrade],
		techs=techs.column(2)
	),
	Civilization(
		iNorse,
		iGold=50,
		lCivics=[iColony, iCommonLaw, iMerchantTrade],
		techs=techs.column(4).without(iLandmarks, iLinguistics, iPathfinding, iCultivation, iHerbalism)
	),
	Civilization(
		iChimu,
		iGold=300,
		lCivics=[iDespotism, iSpecialization, iMerchantTrade, iCasteSystem],
		techs=techs.column(2)
	),
	Civilization(
		iInuit,
		iGold=25,
		lCivics=[iCouncil],
		techs=techs.column(2)
	),
	Civilization(
		iInca,
		iGold=700,
		lCivics=[iEmpire, iSlavery, iMerchantTrade, iCasteSystem, iConquest],
		techs=techs.column(2).including(iArtisanry, iMasonry).without(iSailing)
	),
	Civilization(
		iAztecs,
		iGold=600,
		lCivics=[iDespotism, iSlavery, iMerchantTrade, iCasteSystem, iTributaries],
		techs=techs.column(2).including(iCalendar).without(iNavigation)
	),
	Civilization(
		iSpain,
		iGold=200,
		iStateReligion=iCatholicism,
		lCivics=[iColony, iConquest],
		techs=techs.column(5).including(iCartography, iPrinting, iCompanies).without(*lNativeTechs)
	),
	Civilization(
		iPortugal,
		iGold=200,
		iStateReligion=iCatholicism,
		lCivics=[iColony, iSlavery, iMerchantTrade, iTributaries],
		techs=techs.column(5).including(iFirearms, iLogistics, iExploration).without(*lNativeTechs)
	),
	Civilization(
		iIroquois,
		iGold=600,
		lCivics=[iConfederacy, iCouncil],
		techs=techs.column(2).including(iCalendar).without(iNavigation)
	),
	Civilization(
		iEngland,
		iGold=200,
		iStateReligion=iCatholicism,
		lCivics=[iColony, iMerchantTrade],
		lEnemies=[],
		techs=techs.column(6).without(*lNativeTechs)
	),
	Civilization(
		iFrance,
		iGold=150,
		iStateReligion=iCatholicism,
		lCivics=[iColony, iMerchantTrade],
		techs=techs.column(6).without(*lNativeTechs)
	),
	Civilization(
		iNetherlands,
		iGold=600,
		iStateReligion=iProtestantism,
		lCivics=[iColony, iMercantilism],
		techs=techs.column(6).including(iEconomics, iShipbuilding).without(*lNativeTechs)
	),
	Civilization(
		iHawaii,
		iGold=700,
		lCivics=[iDespotism, iIsolationism],
		techs=techs.column(1).including(iNavigation).without(iTanning)
	),
	Civilization(
		iRussia,
		iGold=200,
		iStateReligion=iOrthodoxy,
		lCivics=[iColony, iIndenturedServitude, iAgrarianism],
		techs=techs.column(9).without(*lNativeTechs)
	),
	Civilization(
		iAmerica,
		iGold=1500,
		iAdvancedStartPoints=500,
		iStateReligion=iProtestantism,
		lCivics=[iConfederacy, iCommonLaw, iSlavery, iAgrarianism, iHaven, iHomesteads],
		techs=techs.column(11).including(iRepresentation, iIndependence)
	),
	Civilization(
		iHaiti,
		iGold=100,
		lCivics=[iMonarchy, iCouncil, iSpecialization, iAgrarianism, iIsolationism],
		techs=techs.column(6)
	),
	Civilization(
		iArgentina,
		iGold=1200,
		iAdvancedStartPoints=100,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iCommonLaw, iSlavery, iAgrarianism, iProfiteering],
		techs=techs.column(11).including(iGeology)
	),
	Civilization(
		iMexico,
		iGold=500,
		iAdvancedStartPoints=100,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iCommonLaw, iSlavery, iAgrarianism, iProfiteering],
		techs=techs.column(11).including(iFederalism)
	),
	Civilization(
		iColombia,
		iGold=750,
		iAdvancedStartPoints=150,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iCommonLaw, iSlavery, iAgrarianism, iProfiteering],
		techs=techs.column(11).including(iRightsOfMan)
	),
	Civilization(
		iPeru,
		iGold=1200,
		iAdvancedStartPoints=100,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iCommonLaw, iSlavery, iAgrarianism, iProfiteering],
		techs=techs.column(11).including(iGeology)
	),
	Civilization(
		iBrazil,
		iGold=1600,
		iAdvancedStartPoints=200,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iCommonLaw, iSlavery, iAgrarianism, iProfiteering],
		techs=techs.column(11).including(iMetallurgy, iProtectionism, iHydrology)
	),
	Civilization(
		iVenezuela,
		iGold=1200,
		iAdvancedStartPoints=100,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iCommonLaw, iSlavery, iAgrarianism, iProfiteering],
		techs=techs.column(11).including(iGeology)
	),
	Civilization(
		iCanada,
		iGold=1000,
		iAdvancedStartPoints=250,
		iStateReligion=iProtestantism,
		lCivics=[iConfederacy, iCommonLaw, iIndenturedServitude, iAgrarianism, iHaven, iHomesteads],
		techs=techs.column(14)
	),
	Civilization(
		iCuba,
		iGold=1200,
		iAdvancedStartPoints=100,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iCommonLaw, iSlavery, iAgrarianism, iProfiteering],
		techs=techs.column(11).including(iGeology)
	),
]

### Starting units ###

dStartingUnits = CivDict({
	iMaya: {
		iWork: 1,
	},
	iWari: {
		iSettle: 1,
		iWork: 1,
		iBase: 2,
	},
	iMississippi: {
		iSettle: 2,
		iWork: 1,
		iBase: 2,
	},
	iPuebloan: {
		iSettle: 1,
		iWork: 1,
		iBase: 2,
	},
	iMuisca: {
		iSettle: 1,
		iWork: 1,
		iBase: 2,
	},
	iNorse: {
	},
	iChimu: {
		iSettle: 1,
		iWork: 1,
		iBase: 2,
	},
	iInuit: {
		iSettle: 2,
		iWork: 1,
		iBase: 2,
	},
	iInca: {
		iSettle: 1,
		iWork: 4,
		iAttack: 4,
		iBase: 2,
		# if not human: 1 Settler
	},
	iAztecs: {
		iSettle: 2,
		iWork: 3,
		iAttack: 4,
		iBase: 2,
	},
	iIroquois: {
		iSettle: 1,
		iWork: 1,
		iBase: 2,
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
		iSettle: 1,
		iWork: 1,
		iBase: 2,
	},
	iRussia: {
	},
	iAmerica: {
		iSettle: 8,
		iWork: 5,
		iSkirmish: 2,
		iAttack: 4,
		iSiege: 2,
		iWorkerSea: 2,
		iFerry: 2,
		iEscort: 1,
	},
	iHaiti: {
		iSettle: 1,
		iWork: 1,
		iBase: 2,
	},
	iArgentina: {
		iSettle: 2,
		iWork: 2,
		iAttack: 1,
		iBase: 2,
		iSiege: 2,
		iMissionary: 1,
		iFerry: 1,
		iEscort: 2,
	},
	iMexico: {
		iSettle: 1,
		iWork: 2,
		iShock: 4,
		iBase: 3,
		iAttack: 2,
		iSkirmish: 2,
		iMissionary: 1,
	},
	iColombia: {
		iSettle: 1,
		iWork: 3,
		iBase: 2,
		iAttack: 3,
		iSiege: 3,
		iMissionary: 1,
		iFerry: 1,
		iAttackSea: 1,
	},
	iPeru: {
		iSettle: 1,
		iWork: 1,
		iBase: 2,
	},
	iBrazil: {
		iSettle: 5,
		iWork: 3,
		iSkirmish: 3,
		iBase: 3,
		iSiege: 2,
		iMissionary: 1,
		iWorkerSea: 2,
		iFerry: 2,
		iEscort: 3,
	},
	iVenezuela: {
		iSettle: 1,
		iWork: 1,
		iBase: 2,
	},
	iCanada: {
		iSettle: 5,
		iWork: 3,
		iShock: 3,
		iBase: 5,
		iMissionary: 1,
	},
	iCuba: {
		iSettle: 1,
		iWork: 1,
		iBase: 2,
	},
}, {})

dExtraAIUnits = CivDict({
	iEngland: {
		iAttack: 2,
	},
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

dAdditionalUnits = CivDict({
	iMaya: {
		iBase: 2,
		iAttack: 2,
	},
	iSpain: {
		iBase: 3,
		iAttack: 3,
	},
	iFrance: {
		iBase: 3,
		iAttack: 3,
	},
	iEngland: {
		iBase: 3,
		iAttack: 3,
	},
	iPortugal: {
		iBase: 3,
		iCounter: 3,
	},
	iInca: {
		iAttack: 5,
		iBase: 3,
	},
	iAztecs: {
		iAttack: 5,
		iBase: 3,
	},
	iNetherlands: {
		iAttack: 3,
		iCounter: 3,
	},
	iAmerica: {
		iAttack: 3,
		iSkirmish: 3,
		iSiege: 3,
	},
	iArgentina: {
		iAttack: 2,
		iShock: 4,
	},
	iMexico: {
		iShock: 4,
		iSiege: 2,
	},
	iColombia: {
		iAttack: 4,
		iSkirmish: 4,
		iSiege: 2,
	},
	iBrazil: {
		iAttack: 3,
		iSkirmish: 2,
		iSiege: 2,
	},
	iCanada: {
		iAttack: 4,
		iShock: 2,
		iSiege: 2,
	},
}, {})

dStartingExperience = CivDict({
	iArgentina: {
		iAttack: 2,
		iShock: 2,
		iBase: 2,
		iSiege: 2,
	},
	iMexico: {
		iShock: 2,
		iBase: 2,
		iAttack: 2,
		iSkirmish: 2,
	},
	iColombia: {
		iAttack: 2,
		iSkirmish: 2,
		iSiege: 2,
	},
}, {})

dAlwaysTrain = CivDict({
	iAztecs: [iJaguar],
	iMexico: [iGrenadier],
	iColombia: [iVoltigeros],
	iBrazil: [iGrenadier],
}, [])

dAIAlwaysTrain = CivDict({
	iSpain: [iCrossbowman],
	iFrance: [iCrossbowman],
	iEngland: [iCrossbowman],
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
		makeUnit(iPlayer, iGreatStatesman, tile)
		makeUnit(iPlayer, iGreatGeneral, tile)
		makeUnit(iPlayer, iGreatScientist, tile)
		makeUnit(iPlayer, iGreatMerchant, tile)
		makeUnit(iPlayer, iGreatArtist, tile)
	elif iCiv == iColombia:
		makeUnits(iPlayer, iVoltigeros, tile, 5).experience(2)

dSpecificAdditionalUnits = CivDict({
}, {})


### Tech Preferences ###

dTechPreferences = {
	iMaya : {
		iCalendar: 40,
		iAesthetics: 30,
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
		iFission: 12,
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
		iFission: 12,
	},
	iArgentina : {
		iRefrigeration: 30,
		iTelevision: 20,
		iElectricity: 20,
		iPsychology: 20,
	},
	iBrazil : {
		iRadio: 20,
		iSynthetics: 20,
		iElectricity: 20,
		iEngine: 20,
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
	},
	iSpain : {
		iGuadalupeBasilica: 30,
		iChapultepecCastle: 30,
		iCristoRedentor: 20,
	},
	iFrance : {
		iTradingCompanyBuilding: 40,
	},
	iEngland : {
		iTradingCompanyBuilding: 50,
		iNationalGallery: 20,
	},
	iPortugal : {
		iCristoRedentor: 40,
	},
	iInca : {
		iMachuPicchu: 40,
		iTempleOfKukulkan: 20,
	},
	iAztecs : {
		iFloatingGardens: 40,
		iTempleOfKukulkan: 30,
		
		iMachuPicchu: -40,
	},
	iNetherlands : {
		iTradingCompanyBuilding: 60,
	},
	iAmerica : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
		iEmpireStateBuilding: 30,
		iBrooklynBridge: 30,
		iGoldenGateBridge: 30,
		iWorldTradeCenter: 30,
		iHubbleSpaceTelescope: 20,
		iCrystalCathedral: 20,
		iMenloPark: 20,
		iUnitedNations: 20,
		iGraceland: 20,
	},
	iMexico : {
		iGuadalupeBasilica: 40,
		iChapultepecCastle: 40,
		iLasLajasSanctuary: 20,
	},
	iArgentina : {
		iGuadalupeBasilica: 30,
		iLasLajasSanctuary: 30,
	},
	iColombia : {
		iLasLajasSanctuary: 40,
		iGuadalupeBasilica: 30,
	},
	iBrazil : {
		iCristoRedentor: 30,
		iItaipuDam: 30,
	},
	iCanada : {
		iChateauFrontenac: 30,
		iCNTower: 30,
	}
}