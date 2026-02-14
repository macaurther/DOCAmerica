from Resources import setupScenarioResources

from Scenario import *
from Locations import *
from RFCUtils import *
from Core import *

lCivilizations = [
	Civilization(
		iNorse,
		iGold=75,
		iImmigration=300,
		lCivics=[iGovernors, iAdmiralty, iIndenturedServitude, iFactoryCivic, iHaven, iOutposts],
		techs=techs.column(13).without(iSouthEuropeAccess, iAfricaAccess, iSiberiaAccess, iAsiaAccess)
	),
	Civilization(
		iInuit,
		iGold=50,
		lCivics=[iDespot, iHarmony, iSacrifice],
		techs=techs.column(7).without(iNorthEuropeAccess, iSouthEuropeAccess, iAfricaAccess, iAsiaAccess)
	),
	Civilization(
		iHaudenosaunee,
		iGold=300,
		lCivics=[iCouncil, iTribalConfederacy, iTlacotin, iMerchantTrade, iAcculturation, iIntegration],
		techs=techs.column(7),
	),
	Civilization(
		iLakota,
		iGold=100,
		lCivics=[iChief, iClans, iTlacotin, iMerchantTrade, iHarmony, iNomads],
		techs=techs.column(7),
	),
	Civilization(
		iSpain,
		iLeader=iPhilip,
		iGold=400,
		iImmigration=300,
		iStateReligion=iCatholicism,
		lCivics=[iViceroys, iRoyalColony, iEncomienda, iPlunder, iJesuits, iImperialism],
		techs=techs.column(15).without(iNorthEuropeAccess, iAfricaAccess, iSiberiaAccess, iAsiaAccess),
		dAttitudes={iPortugal: 2}
	),
	Civilization(
		iPortugal,
		iLeader=iJoao,
		iGold=450,
		iImmigration=300,
		iStateReligion=iCatholicism,
		lCivics=[iProprietors, iAdmiralty, iSlavery, iFactoryCivic, iExtraction, iGrants],
		techs=techs.column(15).without(iNorthEuropeAccess, iAfricaAccess, iSiberiaAccess, iAsiaAccess),
		dAttitudes={iSpain: 2, iEngland: 2, iNetherlands: -2}
	),
	Civilization(
		iEngland,
		iLeader=iVictoria,
		iGold=600,
		iImmigration=300,
		iStateReligion=iProtestantism,
		lCivics=[iGovernors, iCommonwealth, iSlavery, iMercantilism, iHaven, iProvidence],
		techs=techs.column(15).including(iMeteorology, iSurveying, iPhysics).without(iSouthEuropeAccess, iAfricaAccess, iSiberiaAccess, iAsiaAccess),
		dAttitudes={iFrance: -4, iPortugal: 2}
	),
	Civilization(
		iFrance,
		iLeader=iLouis,
		iGold=400,
		iImmigration=300,
		iStateReligion=iCatholicism,
		lCivics=[iGovernors, iCharterColony, iSlavery, iFactoryCivic, iHaven, iOutposts],
		techs=techs.column(15).including(iMeteorology, iSurveying, iPhysics).without(iNorthEuropeAccess, iAfricaAccess, iSiberiaAccess, iAsiaAccess),
		dAttitudes={iEngland: -4, iNetherlands: 2}
	),
	Civilization(
		iNetherlands,
		iLeader=iWilliam,
		iGold=800,
		iImmigration=200,
		iStateReligion=iProtestantism,
		lCivics=[iTrustees, iTradingCompany, iSlavery, iMercantilism, iExtraction, iOutposts],
		techs=techs.column(15).including(iMeteorology).without(iSouthEuropeAccess, iAfricaAccess, iSiberiaAccess, iAsiaAccess),
		dAttitudes={iFrance: 2, iPortugal: -2}
	),
	Civilization(
		iHawaii,
		iGold=150,
		lCivics=[iMonarch, iClans, iTlacotin, iMerchantTrade, iIsolationism, iConquest],
		techs=techs.column(7).without(iNorthEuropeAccess, iSouthEuropeAccess, iAfricaAccess, iSiberiaAccess),
	),
	Civilization(
		iRussia,
		iGold=200,
		iImmigration=100,
		iStateReligion=iOrthodoxy,
		lCivics=[iTrustees, iTradingCompany, iIndenturedServitude, iFactoryCivic, iExtraction, iOutposts],
		techs=techs.column(14).without(iLandmarks, iCultivation, iHerbalism).without(iNorthEuropeAccess, iSouthEuropeAccess, iAfricaAccess, iAsiaAccess),
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
		iEngland : [(37, 80), (38, 80), (38, 81), (39, 81), (39, 82)],	# MacAurther TODO: This doesn't give England control of tiles east of the Appalachians
	},
	iOwnerBaseCulture = 100,
	
	dRevealed = {
		iCivGroupEurope: Revealed(
			lLandRegions=lEuropeanRevealed1750AD,
			lCoastRegions=lAmerica,
			lSeaAreas=[((0, 0), (58, 27)), ((0, 27), (23, 38)), ((50, 27), (58, 38)), ((0, 38), (58, 84)), ((0, 84), (10, 121)), ((31, 84), (58, 117)), ],
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