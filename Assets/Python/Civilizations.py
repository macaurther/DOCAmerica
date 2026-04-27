from Core import *

from Events import events, handler
import GreatPeople as gp


### Unit spawn functions ###

def getStartingUnits(iPlayer):
	return [(iRole, iAmount) for iRole, iAmount in dStartingUnits[iPlayer].items() if (iRole != iWork or civ(iPlayer) in dSeaSpawns.keys())]	# MacAurther: Do give worker to civs that spawn at sea

def getAIStartingUnits(iPlayer):
	return dExtraAIUnits[iPlayer].items()
	
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
		self.iImmigration = kwargs.get("iImmigration")
		self.iStateReligion = kwargs.get("iStateReligion")
		self.iAdvancedStartPoints = kwargs.get("iAdvancedStartPoints")

		self.lCivics = kwargs.get("lCivics", [])
		self.lEnemies = kwargs.get("lEnemies", []) + [iBarbarian]	# MacAurther: Inidigenous player is not automatically an enemy
		#self.iMasterCiv = kwargs.get("iMasterCiv")		# MacAurther: Attempt to have master on spawn. Kind of worked
		
		self.dAttitudes = kwargs.get("dAttitudes", {})
		
		self.sLeaderName = kwargs.get("sLeaderName")
		
		self.techs = kwargs.get("techs", techs.none())
		self.extraTechs = kwargs.get("extraTechs", techs.none())
	
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
		
		if self.iImmigration is not None:
			self.player.changeImmigration(scale(self.iImmigration))
		
		if self.iStateReligion is not None:
			iOldStateReligion = self.player.getStateReligion()
			iNewStateReligion = self.iStateReligion
			
			if iNewStateReligion == iProtestantism and not game.isReligionFounded(iProtestantism):
				iNewStateReligion = iCatholicism
			
			if iNewStateReligion == iCatholicism and not game.isReligionFounded(iCatholicism):
				iNewStateReligion = iOrthodoxy
			
			if game.isReligionFounded(iNewStateReligion) or self.canFoundReligion(iNewStateReligion):
				self.player.setLastStateReligion(iNewStateReligion)
				events.fireEvent("playerChangeStateReligion", self.player.getID(), iNewStateReligion, iOldStateReligion)
		
		if self.techs:
			for iTech in self.techs:
				iTechCultureGroup = gc.getTechInfo(iTech).getCultureGroup()
				iCivCultureGroup = gc.getCivilizationInfo(self.iCiv).getCultureGroup()
				# MacAurther: do give native and colony techs that are not repeatable to nations
				if iCivCultureGroup == iCultureGroupNation and not gc.getTechInfo(iTech).isRepeat():
					pass
				# MacAurther: Don't give native techs to natives, they have to research them, unless explicitly stated
				elif iCivCultureGroup == iCultureGroupNative and iTechCultureGroup == iCultureGroupNative:
					continue
				# MacAurther: otherwise don't give tech here if it doesn't belong to a civ's culture group
				elif not iTechCultureGroup in [iCultureGroupNone, iCivCultureGroup]:
					continue
				self.team.setHasTech(iTech, True, self.player.getID(), False, False)

		if self.extraTechs:		# Extra techs are where things like culture group restrictions can be overridden
			for iTech in self.extraTechs:
				self.team.setHasTech(iTech, True, self.player.getID(), False, False)


		self.player.setStartingEra(self.player.getCurrentEra())
		
		for iCivic in self.lCivics:
			self.player.setCivics(infos.civic(iCivic).getCivicOptionType(), iCivic)
			
		for iEnemy in self.lEnemies:
			iEnemyPlayer = slot(iEnemy)
			if iEnemyPlayer >= 0 and self.iCiv != iEnemy:
				team(iEnemyPlayer).declareWar(self.player.getTeam(), False, WarPlanTypes.NO_WARPLAN)
		
		# MacAurther: Rare bug where master is assigned and then collapses??, causing bug in scoreboard??
		# I guess don't use this feature.
		'''if self.iMasterCiv is not None:
			iMasterPlayer = slot(self.iMasterCiv)
			if iMasterPlayer >= 0 and self.iCiv != self.iMasterCiv:
				team(iMasterPlayer).assignVassal(self.player.getTeam(), False)'''
		
		for iCiv, iAttitude in self.dAttitudes.items():
			self.player.AI_changeAttitudeExtra(slot(iCiv), iAttitude)
	
	def canFoundReligion(self, iReligion):
		return infos.religion(iReligion).getTechPrereq() in self.techs
	
	def advancedStart(self):
		if self.iAdvancedStartPoints is not None:
			self.player.setAdvancedStartPoints(scale(self.iAdvancedStartPoints))
			
			if not self.player.isHuman():
				self.player.AI_doAdvancedStart()

lCivilizations = [
	Civilization(
		iTiwanaku,
		iGold=50,
		lCivics=[iMita, iRedistribution],
		techs=techs.column(2).including(iAgriculture, iPottery, iPastoralism, iMythology, iArithmetics, iMining, iMasonry),
		extraTechs=techs.column(0).including(iLandmarks, iIrrigation, iEarthworks, iCultivation, iCompanionPlanting),
	),
	Civilization(
		iWari,
		iGold=100,
		lCivics=[iDespot, iMita, iRedistribution],
		techs=techs.column(3).including(iMasonry, iArithmetics, iProperty, iCeremony),
		extraTechs=techs.column(0).including(iLandmarks, iPathfinding, iIrrigation, iEarthworks, iCultivation, iCompanionPlanting, iInterpretation),
	),
	Civilization(
		iMississippi,
		iGold=25,
		lCivics=[iChief, iClans],
		techs=techs.column(2).including(iPottery, iAgriculture, iMythology, iDugouts, iTanning, iDivination, iNavigation),
		extraTechs=techs.column(0).including(iHunting, iTrapping, iCompanionPlanting, iDiving, iFishing),
	),
	Civilization(
		iMuisca,
		iGold=100,
		lCivics=[iMita, iRedistribution],
		techs=techs.column(3).including(iMasonry, iSmelting),
		extraTechs=techs.column(0).including(iHunting, iLandmarks, iPathfinding, iIrrigation, iCultivation, iCompanionPlanting, iKnapping),
	),
	Civilization(
		iToltec,
		iGold=150,
		techs=techs.column(4).including(iGeneralship, iConstruction, iMathematics),
		extraTechs=techs.column(0).including(iLandmarks, iPathfinding, iIrrigation, iCultivation, iCompanionPlanting, iKnapping),
	),
	Civilization(
		iNorse,
		iGold=50,
		lCivics=[iExpedition, iSerfdom],
		techs=techs.column(8),
		extraTechs=techs.column(0).including(iNorthEuropeAccess, iHunting, iTrapping, iFishing),
	),
	Civilization(
		iChimu,
		iGold=200,
		lCivics=[iDespot, iMerchantTrade, iCraftsmen, iConquest],
		techs=techs.column(4).including(iConstruction, iTradeRoutes, iGeneralship),
		extraTechs=techs.column(0).including(iLandmarks, iPathfinding, iCultivation, iCompanionPlanting, iDiving, iFishing),
	),
	Civilization(
		iPueblo,
		iGold=50,
		lCivics=[iSubsistance],
		techs=techs.column(2).including(iTanning, iMining, iPottery, iAgriculture, iMythology),
		extraTechs=techs.column(0).including(iHunting, iLandmarks, iPathfinding, iIrrigation, iEarthworks, iCompanionPlanting),
	),
	Civilization(
		iArawak,
		iGold=25,
		lCivics=[iChief, iClans, iHarmony, iNomads],
		techs=techs.column(3).including(iNavigation, iTradeRoutes).without(iMining),
		extraTechs=techs.column(0).including(iHunting, iTrapping, iCompanionPlanting, iInterpretation, iMediation, iFishing, iIrrigation, iHerbalism),
	),
	Civilization(
		iTupi,
		iGold=25,
		lCivics=[iChief, iClans, iHarmony, iNomads],
		techs=techs.column(3).including(iNavigation, iTradeRoutes).without(iMining),
		extraTechs=techs.column(0).including(iHunting, iTrapping, iCompanionPlanting, iInterpretation, iMediation, iFishing, iHerbalism),
	),
	Civilization(
		iPurepecha,
		iGold=250,
		lCivics=[iDespot, iTlacotin, iRedistribution],
		techs=techs.column(4).including(iConstruction, iMathematics, iWriting, iGeneralship),
		extraTechs=techs.column(0).including(iHunting, iLandmarks, iPathfinding, iIrrigation, iCompanionPlanting, iKnapping, iDiving, iFishing),
	),
	Civilization(
		iInuit,
		iGold=25,
		lCivics=[iHarmony, iClans],
		techs=techs.column(2).including(iTanning, iMythology, iDugouts),
		extraTechs=techs.column(0).including(iHunting, iTrapping, iFishing, iMediation),
	),
	Civilization(
		iInca,
		iGold=350,
		lCivics=[iDespot, iMita, iMerchantTrade, iConquest],
		lEnemies=[iWari, iTiwanaku],
		techs=techs.column(4).including(iConstruction, iMathematics, iWriting, iTradeRoutes, iGeneralship, iAlloys),
		extraTechs=techs.column(0).including(iLandmarks, iPathfinding, iIrrigation, iEarthworks, iCultivation, iCompanionPlanting, iInterpretation, iMediation),
	),
	Civilization(
		iAztec,
		iGold=300,
		lCivics=[iDespot, iTlacotin, iRaiding, iSacrifice, iConquest],
		lEnemies=[iTeotihuacan, iToltec],
		techs=techs.column(4).including(iWriting, iCalendar, iTradeRoutes, iPriesthood, iGeneralship, iMathematics, iAstronomy),
		extraTechs=techs.column(0).including(iHunting, iLandmarks, iPathfinding, iIrrigation, iCompanionPlanting, iKnapping, iFishing),
	),
	Civilization(
		iHaudenosaunee,
		iGold=150,
		lCivics=[iCouncil, iTribalConfederacy, iHarmony, iIntegration],
		techs=techs.column(3).including(iProperty, iCeremony),
		extraTechs=techs.column(0).including(iHunting, iTrapping, iCompanionPlanting, iInterpretation, iMediation, iFishing),
	),
	Civilization(
		iSpain,
		iGold=500,
		iStateReligion=iCatholicism,
		lCivics=[iCaptains, iExpedition, iSerfdom, iPlunder, iJesuits, iImperialism],
		techs=techs.column(8).including(iGunpowder, iCompanies, iCartography, iEvangelism),
		extraTechs=techs.column(0).including(iSouthEuropeAccess, iFishing, iDiving),
	),
	Civilization(
		iPortugal,
		iGold=300,
		iStateReligion=iCatholicism,
		lCivics=[iProprietors, iAdmiralty, iGrants, iSlavery],
		techs=techs.column(8).including(iGunpowder, iCompanies, iFinance, iCartography, iExchange, iExploration, iOptics, iTriangularTrade),
		extraTechs=techs.column(0).including(iSouthEuropeAccess, iFishing, iDiving),
	),
	Civilization(
		iCherokee,
		iGold=100,
		lCivics=[iChief, iClans, iHarmony],
		techs=techs.column(3).including(iProperty, iCeremony),
		extraTechs=techs.column(0).including(iHunting, iTrapping, iCompanionPlanting, iInterpretation, iMediation, iFishing),
	),
	Civilization(
		iEngland,
		iGold=300,
		iStateReligion=iProtestantism,
		lCivics=[iProprietors, iCharterColony, iIndenturedServitude, iMercantilism, iDivineRight, iGrants],
		techs=techs.column(10).including(iShipbuilding, iCharter, iIndentures),
		extraTechs=techs.column(0).including(iNorthEuropeAccess, iFishing, iDiving),
	),
	Civilization(
		iFrance,
		iGold=400,
		iStateReligion=iCatholicism,
		lCivics=[iExpedition, iAdmiralty, iSerfdom, iFactoryCivic, iJesuits, iOutposts],
		techs=techs.column(10).including(iShipbuilding, iFortification),
		extraTechs=techs.column(0).including(iNorthEuropeAccess, iSouthEuropeAccess, iFishing, iDiving),
	),
	Civilization(
		iNetherlands,
		iGold=600,
		iImmigration=15,
		iStateReligion=iProtestantism,
		lCivics=[iTrustees, iTradingCompany, iSerfdom, iFactoryCivic, iDivineRight, iOutposts],
		techs=techs.column(10).including(iFortification, iEconomics, iShipbuilding, iEducation),
		extraTechs=techs.column(0).including(iNorthEuropeAccess, iFishing, iDiving),
	),
	Civilization(
		iApache,
		iGold=50,
		lEnemies=[iPueblo],
		lCivics=[iChief, iSubsistance, iNomads],
		techs=techs.column(3).including(iCeremony, iContact, iRiding),
		extraTechs=techs.column(0).including(iHunting, iCompanionPlanting, iInterpretation),
	),
	Civilization(
		iLakota,
		iGold=100,
		lCivics=[iChief, iSubsistance, iHarmony, iNomads],
		techs=techs.column(3).including(iCeremony, iContact, iRiding),
		extraTechs=techs.column(0).including(iHunting, iTrapping, iCompanionPlanting, iInterpretation, iMediation),
	),
	Civilization(
		iHawaii,
		iGold=200,
		lCivics=[iTlacotin],
		techs=techs.column(3).including(iSeafaring, iArithmetics, iCeremony, iAstronomy, iTradeRoutes, iNavigation),
		extraTechs=techs.column(0).including(iKnapping, iDiving, iFishing, iAsiaAccess),
	),
	Civilization(
		iRussia,
		iGold=200,
		iImmigration=10,
		iStateReligion=iOrthodoxy,
		lCivics=[iTrustees, iTradingCompany, iIndenturedServitude, iFactoryCivic, iExtraction, iOutposts],
		techs=techs.column(12),
		extraTechs=techs.column(0).including(iSiberiaAccess, iHunting, iTrapping, iFishing, iDiving),
	),
	Civilization(
		iAmerica,
		iGold=1500,
		iImmigration=20,
		iStateReligion=iProtestantism,
		lCivics=[iPlutocrats, iConfederacy, iBondage, iAgrarianism, iProfiteering],
		techs=techs.column(14).without(iSouthEuropeAccess, iSiberiaAccess),
	),
	Civilization(
		iHaiti,
		iGold=100,
		lEnemies=[iFrance],
		techs=techs.column(12).including(iFreeMarket, iAcademia, iIndependence).without(iNorthEuropeAccess, iSouthEuropeAccess),
		extraTechs=techs.column(0).including(iAfricaAccess),
	),
	Civilization(
		iArgentina,
		iGold=1200,
		iStateReligion=iCatholicism,
		lCivics=[iSovereign, iConfederacy, iBondage, iAgrarianism, iProfiteering, iHomesteads],
		lEnemies=[iSpain],
		techs=techs.column(14).including(iHeritage, iSurveying).without(iNorthEuropeAccess, iSiberiaAccess),
	),
	Civilization(
		iMexico,
		iGold=500,
		iStateReligion=iCatholicism,
		lCivics=[iSovereign, iMartialLaw, iBondage, iAgrarianism, iProfiteering, iHomesteads],
		lEnemies=[iSpain],
		techs=techs.column(14).without(iNorthEuropeAccess, iSiberiaAccess),
	),
	Civilization(
		iColombia,
		iGold=750,
		iStateReligion=iCatholicism,
		lCivics=[iSovereign, iFederalism, iBondage, iAgrarianism, iProfiteering, iHomesteads],
		lEnemies=[iSpain],
		techs=techs.column(14).without(iNorthEuropeAccess, iSiberiaAccess),
	),
	Civilization(
		iPeru,
		iGold=1200,
		iStateReligion=iCatholicism,
		lCivics=[iSovereign, iFederalism, iBondage, iAgrarianism, iProfiteering, iHomesteads],
		lEnemies=[iSpain],
		techs=techs.column(15).without(iNorthEuropeAccess, iSiberiaAccess),
	),
	Civilization(
		iBrazil,
		iGold=1600,
		iStateReligion=iCatholicism,
		lCivics=[iSovereign, iFederalism, iBondage, iAgrarianism, iProfiteering, iHomesteads],
		techs=techs.column(15).including(iMetallurgy, iHydrology).without(iNorthEuropeAccess, iSiberiaAccess),
	),
	Civilization(
		iVenezuela,
		iGold=1200,
		iStateReligion=iCatholicism,
		lCivics=[iSovereign, iFederalism, iBondage, iAgrarianism, iProfiteering, iHomesteads],
		lEnemies=[iColombia],
		techs=techs.column(15).without(iNorthEuropeAccess, iSiberiaAccess),
	),
	Civilization(
		iCSA,
		iGold=1000,
		iImmigration=20,
		iStateReligion=iProtestantism,
		lCivics=[iPlutocrats, iConfederacy, iBondage, iFreeEnterprise, iProfiteering, iHomesteads],
		lEnemies=[iAmerica],
		techs=techs.column(17).including(iMeasurement, iEngine, iRailroad, iElectricity, iDoctrine).without(iSiberiaAccess),
	),
	Civilization(
		iCanada,
		iGold=1000,
		iImmigration=100,
		iStateReligion=iProtestantism,
		#iMasterCiv=iEngland,
		lCivics=[iRepresentatives, iFederalism, iIndustrialism, iFreeEnterprise, iOpportunity, iHomesteads],
		techs=techs.column(18).without(iSiberiaAccess),
	),
]

### Starting units ###

dStartingUnits = CivDict({
	iTeotihuacan: {
		iSettle: 1,
		iWork: 1,
		iBase: 2,
	},
	iTiwanaku: {
		iSettle: 1,
		iWork: 1,
		iBase: 2,
	},
	iWari: {
		iSettle: 2,
		iWork: 2,
		iBase: 2,
		iAttack: 1,
		iSkirmish: 3,
		iDefend: 1,
		iExplore: 1,
	},
	iMississippi: {
		iSettle: 1,
		iSettleSea: 1,
		iWorkSea: 1,
		iBase: 3,
		iDefend: 1,
	},
	iMuisca: {
		iSettle: 1,
		iWork: 1,
		iDefend: 2,
		iAttack: 1,
		iExplore: 1,
	},
	iToltec: {
		iSettle: 1,
		iWork: 1,
		iDefend: 2,
		iAttack: 3,
		iSkirmish: 2,
	},
	iNorse: {
		iSettleSea: 1,
	},
	iChimu: {
		iSettle: 2,
		iWork: 2,
		iDefend: 3,
		iSkirmish: 1,
		iAttack: 3,
	},
	iPueblo: {
		iSettle: 2,
		iWork: 1,
		iBase: 2,
		iDefend: 2,
		iExplore: 1,
	},
	iArawak: {
		iSettle: 1,
		iDefend: 2,
		iExplore: 1,
		iWork: 1,
		iSettleSea: 1,
	},
	iTupi: {
		iSettle: 2,
		iDefend: 2,
		iWork: 1,
		iExplore: 1,
	},
	iInuit: {
		iSettle: 1,
		iDefend: 1,
		iExplore: 1,
		iSettleSea: 1,
	},
	iInca: {
		iSettle: 1,
		iWork: 2,
		iAttack: 7,
		iDefend: 6,
		iCounter: 2,
		iSkirmish: 4,
	},
	iPurepecha: {
		iSettle: 2,
		iWork: 2,
		iAttack: 3,
		iSkirmish: 1,
		iDefend: 2,
		iCounter: 1,
		iSpyRole: 1,	# Represents the incorporated refugees from tribes the Aztecs conquered spying on the periphery for the Purepecha
	},
	iAztec: {
		iSettle: 1,
		iWork: 1,
		iAttack: 8,
		iSkirmish: 4,
		iDefend: 5,
		iCounter: 2,
	},
	iHaudenosaunee: {
		iSettle: 2,
		iWork: 1,
		iBase: 2,
		iDefend: 2,
		iAttack: 4,
		iSpyRole: 1,
	},
	iSpain: {
		iSettleSea: 1,
		iShockSea: 1,
		iMissionarySea: 1,
	},
	iPortugal: {
		iSettleSea: 1,
		iWorkSea: 1,
		iSlaveSea: 1,
		iMissionarySea: 1,
	},
	iCherokee: {
		iSettle: 1,
		iDefend: 2,
		iWork: 1,
	},
	iEngland: {
		iSettleSea: 1,
		iWorkSea: 1,
		iMissionarySea: 1,
	},
	iFrance: {
		iSettleSea: 1,
		iWorkSea: 1,
		iMissionarySea: 1,
	},
	iNetherlands: {
		iSettleSea: 1,
		iWorkSea: 1,
		iMissionarySea: 1,
	},
	iApache: {
		iSettle: 2,
		iDefend: 2,
		iSkirmish: 4,
	},
	iLakota: {
		iSettle: 2,
		iDefend: 2,
		iAttack: 3,
		iSkirmish: 2,
		iExplore: 1,
	},
	iHawaii: {
		iSettle: 1,
		iWork: 1,
		iBase: 2,
		iAttack: 2,
		iSettleSea: 1,
	},
	iRussia: {
		iSettleSea: 1,
		iWorkSea: 1,
		iMissionarySea: 1,
	},
	iAmerica: {
		iSettle: 8,
		iWork: 5,
		iBase: 8,
		iAttack: 2,
		iSkirmish: 2,
		iCitySiege: 2,
		iFerry: 1,
		iMissionary: 1,
	},
	iHaiti: {
		iSettle: 1,
		iWork: 2,
		iDefend: 3,
		iAttack: 2,
		iSkirmish: 4,
		iMissionary: 1,
	},
	iArgentina: {
		iSettle: 5,
		iWork: 4,
		iDefend: 3,
		iAttack: 7,
		iSiege: 2,
		iShock: 2,
		iCitySiege: 1,
		iMissionary: 1,
	},
	iMexico: {
		iSettle: 8,
		iWork: 3,
		iDefend: 4,
		iAttack: 8,
		iSkirmish: 2,
		iShock: 2,
		iCitySiege: 3,
		iMissionary: 1,
	},
	iColombia: {
		iSettle: 4,
		iWork: 3,
		iDefend: 3,
		iAttack: 7,
		iSiege: 2,
		iShock: 4,
		iCitySiege: 3,
		iMissionary: 1,
	},
	iPeru: {
		iSettle: 3,
		iWork: 3,
		iDefend: 3,
		iAttack: 7,
		iSiege: 1,
		iCitySiege: 2,
		iMissionary: 1,
	},
	iBrazil: {
		iSettle: 8,
		iWork: 3,
		iDefend: 4,
		iAttack: 3,
		iSkirmish: 3,
		iSiege: 1,
		iCitySiege: 2,
		iWorkerSea: 2,
		iFerry: 2,
		iEscort: 3,
		iMissionary: 1,
	},
	iVenezuela: {
		iSettle: 3,
		iWork: 2,
		iDefend: 3,
		iAttack: 6,
		iSiege: 1,
		iCitySiege: 1,
		iFerry: 1,
		iEscort: 1,
		iMissionary: 1,
	},
	iCSA: {
		iSettle: 8,
		iWork: 5,
		iDefend: 8,
		iHarass: 6,
		iCitySiege: 3,
		iFerry: 1,
	},
	iCanada: {
		iSettle: 8,
		iWork: 5,
		iDefend: 6,
		iHarass: 2,
		iMissionary: 1,
	},
}, {})

# Extra units for AI
dExtraAIUnits = CivDict({
	iToltec : {
		iAttack: 2,
		iSkirmish: 1,
	},
	iArawak : {
		iSettleSea: 1,
	},
	iInuit: {
		iSettleSea: 1,
	},
	iInca: {
		iDefend: 2,
		iAttack: 4,
		iSkirmish: 4,
	},
	iAztec: {
		iDefend: 2,
		iAttack: 6,
		iSkirmish: 4,
	},
	iAmerica: {
		iBase: 4,
		iAttack: 8,
		iSkirmish: 3,
		iShock: 4,
		iSiege: 2,
		iFerry: 1,
		iEscort: 3,
	},
	iArgentina: {
		iDefend: 3,
		iAttack: 5,
		iSkirmish: 3,
		iShock: 4,
		iSiege: 3,
		iFerry: 1,
		iEscort: 1,
	},
	iMexico: {
		iDefend: 4,
		iShock: 4,
		iSiege: 1,
	},
	iBrazil: {
		iDefend: 1,
	},
	iCSA: {
		iDefend: 2,
		iHarass: 2,
		iCitySiege: 1,
	},
}, {})

# Extra units if civ starts at war
dAdditionalUnits = CivDict({
}, {})

dStartingExperience = CivDict({
	iArgentina: {
		iShock: 2,
		iDefend: 4,
		iSiege: 2,
	},
	iMexico: {
		iDefend: 4,
		iShock: 2,
		iSkirmish: 2,
	},
	iColombia: {
		iDefend: 2,
		iSkirmish: 2,
		iSiege: 1,
		iCitySiege: 1,
	},
	iCSA: {
		iDefend: 2,
		iSkirmish: 5,
		iShock: 5,
		iSiege: 3,
		iCitySiege: 3,
	},
}, {})

dAlwaysTrain = CivDict({
	iAztec: [iAztecJaguar],
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

dSeaSpawns = CivDict({
	iNorse:	      (68, 118),
	iSpain:	      (70, 73),
	iPortugal:	  (80, 29),
	iEngland:	  (56, 87),
	iFrance:	  (56, 98),
	iNetherlands: (60, 91),
	iRussia:	  (1, 106),
})

def createSpecificUnits(iPlayer, tile):
	iCiv = civ(iPlayer)
	bHuman = player(iPlayer).isHuman()
	
	if iCiv == iAmerica:	# American UP
		for iGreatPerson in [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatSpy]:
			unit = makeUnit(iPlayer, iGreatPerson, tile)
			gp.assignGreatPersonName(unit, iPlayer, None, False)
	elif iCiv == iColombia:
		makeUnits(iPlayer, iAlbionLegion, tile, 5).experience(2)
	elif iCiv == iCSA:	# CSA UP
		for iGreatPerson in [iGreatGeneral, iGreatGeneral, iGreatGeneral, iGreatSpy]:
			unit = makeUnit(iPlayer, iGreatPerson, tile)
			gp.assignGreatPersonName(unit, iPlayer, None, False)


dSpecificAdditionalUnits = CivDict({
}, {})


### Tech Preferences ###

dTechPreferences = {
	iMaya : {
		iConstruction: -20, # Try to let Tiwanaku have it
		iMathematics : 20,
		iCalendar: 50,
		iAesthetics: 20,
	},
	iZapotec : {
		iConstruction: -20, # Try to let Tiwanaku have it
		iWriting: 40,
	},
	iWari : {
		iConstruction: -20, # Try to let Tiwanaku have it
	},
	iArawak: {
		iMining: -100,
	},
	iTupi: {
		iMining: -100,
	},
	iInuit: {
		iMining: -100,
	},
	iCherokee: {
		iMining: -100,
	},
	iApache: {
		iMining: -100,
	},
	iLakota: {
		iMining: -100,
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
	iAztec : {
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
		iSerpentMound: -80,
		iGateOfTheSun: -80,
		iPyramidOfTheSun: -80,
		iKalasasaya : -40,
		iMachuPicchu: -40,
		iSacsayhuaman: -40,
		iYachaywasi: -100, # They become too powerful!!
	},
	iZapotec : {
		iSerpentMound: -80,
		iPuebloBonito: -80,
		iGateOfTheSun: -80,
		iPyramidOfTheSun: -80,
		iKalasasaya : -40,
		iMachuPicchu: -40,
		iSacsayhuaman: -40,
	},
	iTeotihuacan : {
		iTlachihualtepetl: 40,
		iSerpentMound: -80,
		iPuebloBonito: -80,
		iGateOfTheSun: -100,
		iPyramidOfTheSun: -80,
		iKalasasaya : -40,
		iMachuPicchu: -40,
		iSacsayhuaman: -40,
	},
	iTiwanaku : {
		iGateOfTheSun: 40,
		iPyramidOfTheSun: 40,
		iKalasasaya : 40,
		iSerpentMound: -40,
		iMachuPicchu: -40,
		iSacsayhuaman: -40,
		iYachaywasi: -100, # They become too powerful!!
	},
	iWari : {
		iSerpentMound: -40,
		iPuebloBonito: -100,
		iGateOfTheSun: -80,
		iPyramidOfTheSun: -80,
		iMachuPicchu: -40,
		iSacsayhuaman: -40,
	},
	iMississippi : {
		iSerpentMound: 40,
		iGateOfTheSun: -80,
		iPyramidOfTheSun: -80,
		iMachuPicchu: -40,
		iSacsayhuaman: -40,
	},
	iMuisca : {
		iSerpentMound: -40,
		iGateOfTheSun: -80,
		iPyramidOfTheSun: -80,
		iMachuPicchu: -40,
		iSacsayhuaman: -40,
	},
	iChimu : {
		iSerpentMound: -40,
		iGateOfTheSun: -80,
		iPyramidOfTheSun: -80,
		iMachuPicchu: -40,
		iSacsayhuaman: -40,
	},
	iPueblo : {
		iPuebloBonito: 40,
		iSerpentMound: -40,
		iGateOfTheSun: -80,
		iPyramidOfTheSun: -80,
		iMachuPicchu: -40,
		iSacsayhuaman: -40,
	},
	iInca : {
		iMachuPicchu: 40,
		iSacsayhuaman: 40,
		iSerpentMound: -40,
	},
	iAztec : {
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
		iNationalGallery: 20,
	},
	iFrance : {
		iChateauFrontenac: 20,
		iFrenchQuarter: 20,
	},
	iNetherlands : {
	},
	iAmerica : {
		iIndendenceHall: 40,
		iMountVernon: 20,
		iMonticello: 20,
		iFortMcHenry: 20,
		iWashingtonMonument: 40,
		iFaneuilHall: 20,
		iCentralPark: 20,
		iEllisIsland: 20,
		iStatueOfLiberty: 30,
		iBrooklynBridge: 30,
		iMenloPark: 20,
		iBiltmoreEstate: 20,
		iLeagueOfNations: 20,
		iHollywood: 30,
		iPentagon: 30,
		iEmpireStateBuilding: 30,
		iGoldenGateBridge: 30,
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
		iGuadalupeBasilica: 30,
		iLasLajasSanctuary: 30,
	},
	iBrazil : {
		iCristoRedentor: 30,
	},
	iCanada : {
		iChateauFrontenac: 30,
	},
}