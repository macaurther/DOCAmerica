from Resources import setupScenarioResources

from Scenario import *
from Locations import *
from RFCUtils import *
from Core import *

lCivilizations = [
	Civilization(
		iNorse,
		iGold=250,
		lCivics=[iGovernors, iAdmiralty, iIndenturedServitude, iFactoryCivic, iHaven, iOutposts],
		techs=techs.column(12),
		extraTechs=techs.column(2).including(iNorthEuropeAccess),
	),
	Civilization(
		iArawak,
		iGold=50,
		iStateReligion=iCatholicism,
		lCivics=[iChief, iClans, iDependency, iAcculturation, iAncestralLands],
		techs=techs.column(4).including(iTradeRoutes).without(iSmelting),
		extraTechs=techs.column(0).including(iHunting, iTrapping, iCompanionPlanting, iInterpretation, iMediation, iFishing, iIrrigation, iHerbalism, iContact),
		dAttitudes={iPortugal: -3, iSpain: -4},
	),
	Civilization(
		iTupi,
		iGold=50,
		iStateReligion=iCatholicism,
		lCivics=[iChief, iClans, iDependency, iAcculturation, iNomadic],
		techs=techs.column(4).including(iTradeRoutes).without(iSmelting),
		extraTechs=techs.column(0).including(iHunting, iTrapping, iCompanionPlanting, iInterpretation, iMediation, iFishing, iHerbalism, iContact),
		dAttitudes={iPortugal: -4},
	),
	Civilization(
		iInuit,
		iGold=150,
		iStateReligion=iProtestantism,
		lCivics=[iDespot, iClans, iDependency, iAcculturation, iIsolationism],
		techs=techs.column(4).including(iTradeRoutes, iSeafaring, iAstronomy, iIndoctrination).without(iSmelting),
		extraTechs=techs.column(0).including(iHunting, iTrapping, iFishing, iMediation, iHerbalism, iKnapping, iContact),
		dAttitudes={iRussia: -4, iNorse: -2, iEngland: -1, iFrance: 2},
	),
	Civilization(
		iHaudenosaunee,
		iGold=300,
		lCivics=[iCouncil, iTribalConfederacy, iTlacotin, iDependency, iHarmony, iIntegration],
		techs=techs.column(4).including(iTradeRoutes, iPriesthood, iGunpowder, iExchange).without(iSmelting),
		extraTechs=techs.column(0).including(iHunting, iTrapping, iCompanionPlanting, iInterpretation, iMediation, iFishing, iContact),
		dAttitudes={iEngland: 4, iFrance: -2},
	),
	Civilization(
		iSpain,
		iLeader=iPhilip,
		iGold=1500,
		iImmigration=50,
		iStateReligion=iCatholicism,
		lCivics=[iViceroys, iRoyalColony, iSlavery, iExtraction, iCastas, iProvidence],
		techs=techs.column(12),
		extraTechs=techs.column(2).including(iSouthEuropeAccess),
		dAttitudes={iPortugal: 2, iEngland: -4},
	),
	Civilization(
		iPortugal,
		iLeader=iJoao,
		iGold=450,
		iImmigration=25,
		iStateReligion=iCatholicism,
		lCivics=[iViceroys, iAdmiralty, iSlavery, iPlantationCivic, iCastas, iOutposts],
		techs=techs.column(12),
		extraTechs=techs.column(2).including(iSouthEuropeAccess),
		dAttitudes={iSpain: 2, iEngland: 2, iNetherlands: -2},
	),
	Civilization(
		iCherokee,
		iGold=150,
		lCivics=[iChief, iFirstNation, iDependency, iAcculturation],
		techs=techs.column(4).including(iTradeRoutes, iWriting, iGunpowder, iExchange).without(iSmelting),
		extraTechs=techs.column(0).including(iHunting, iTrapping, iCompanionPlanting, iInterpretation, iMediation, iFishing, iContact),
		dAttitudes={iFrance: 2, iEngland: -2},
	),
	Civilization(
		iEngland,
		iLeader=iVictoria,
		iGold=600,
		iImmigration=300,
		iStateReligion=iProtestantism,
		lCivics=[iGovernors, iCommonwealth, iSlavery, iMercantilism, iHaven, iProvidence],
		techs=techs.column(12),
		extraTechs=techs.column(2).including(iNorthEuropeAccess),
		dAttitudes={iFrance: -8, iPortugal: 2}
	),
	Civilization(
		iFrance,
		iLeader=iLouis,
		iGold=400,
		iImmigration=150,
		iStateReligion=iCatholicism,
		lCivics=[iGovernors, iCharterColony, iSlavery, iFactoryCivic, iHaven, iOutposts],
		techs=techs.column(12),
		extraTechs=techs.column(2).including(iNorthEuropeAccess, iSouthEuropeAccess),
		dAttitudes={iEngland: -8, iNetherlands: 2}
	),
	Civilization(
		iNetherlands,
		iLeader=iWilliam,
		iGold=800,
		iImmigration=25,
		iStateReligion=iProtestantism,
		lCivics=[iTrustees, iTradingCompany, iSlavery, iMercantilism, iExtraction, iOutposts],
		techs=techs.column(12),
		extraTechs=techs.column(2).including(iNorthEuropeAccess),
		dAttitudes={iFrance: 2, iPortugal: -2}
	),
	Civilization(
		iApache,
		iGold=50,
		lCivics=[iChief, iSubsistance, iHarmony, iNomadic],
		techs=techs.column(4).without(iSmelting),
		extraTechs=techs.column(0).including(iHunting, iTrapping, iInterpretation, iMediation, iFishing, iContact, iRiding),
		dAttitudes={iSpain: -4}
	),
	Civilization(
		iLakota,
		iGold=50,
		lCivics=[iChief, iSubsistance, iHarmony, iNomadic],
		techs=techs.column(4).without(iSmelting),
		extraTechs=techs.column(0).including(iHunting, iTrapping, iInterpretation, iMediation, iFishing, iContact, iRiding),
	),
	Civilization(
		iHawaii,
		iGold=250,
		lCivics=[iMonarch, iClans, iTlacotin, iMerchantTrade, iIsolationism, iConquest],
		techs=techs.column(4).including(iAstronomy, iTradeRoutes, iSeafaring).without(iSmelting),
		extraTechs=techs.column(0).including(iKnapping, iDiving, iFishing, iHerbalism, iAsiaAccess),
	),
	Civilization(
		iRussia,
		iGold=200,
		iImmigration=15,
		iStateReligion=iOrthodoxy,
		lCivics=[iTrustees, iTradingCompany, iIndenturedServitude, iFactoryCivic, iExtraction, iOutposts],
		techs=techs.column(12),
		extraTechs=techs.column(2).including(iSiberiaAccess),
	),
	Civilization(
		iIndependent1,
		iGold=500,
		techs=techs.column(15)
	),
	Civilization(
		iIndependent2,
		iGold=500,
		techs=techs.column(15)
	),
	Civilization(
		iIndependent3,
		iGold=500,
		techs=techs.column(15)
	),
	Civilization(
		iIndigenous,
		iGold=300,
		techs=techs.column(8)
	),
	Civilization(
		iBarbarian,
	)
]

lTribalVillages = [
]
	

def createStartingUnits():
	# MacAurther TODO
	pass

def setupGoals(iCiv, goals):
	# MacAurther TODO
	pass
	

scenario1750AD = Scenario(
	iStartYear = 1750,
	fileName = "RFC_1750AD",
	
	lCivilizations = lCivilizations,
	lTribalVillages = lTribalVillages,
	
	dCivilizationDescriptions = {
		iEngland: "TXT_KEY_CIV_BRITAIN_DESC",
	},
	
	dOwnedTiles = {
	},
	iOwnerBaseCulture = 100,
	
	dRevealed = {
		iCivGroupEurope: Revealed(
			lLandRegions=lEuropeanRevealed1750AD,
			lCoastRegions=lAmerica,
			lSeaAreas=[((0, 0), (82, 121))],
		),
	},
	
	dGreatPeopleCreated = {
		iSpain: 4,
		iPortugal: 3,
		iFrance: 3,
		iEngland: 5,
		iNetherlands: 2,
	},
	dGreatGeneralsCreated = {
		iHaudenosaunee: 1,
		iSpain: 4,
		iPortugal: 2,
		iFrance: 1,
		iEngland: 1,
		iNetherlands: 1,
	},
	
	lInitialWars = [
	],
	
	lAllGoalsFailed = [iMaya, iZapotec, iTeotihuacan, iTiwanaku, iWari, iMississippi, iPueblo, iChimu, iPortugal, iEngland, iFrance, iNetherlands],
	lGoalsSucceeded = [],
	setupGoals = setupGoals,
	
	createStartingUnits = createStartingUnits,
)