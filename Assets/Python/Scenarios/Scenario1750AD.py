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
		lCivics=[iGovernors2, iAdmiralty2, iIndenturedServitude2, iFactory2, iHaven2, iOutposts2],
		techs=techs.column(12),
	),
	Civilization(
		iInuit,
		iGold=50,
		lCivics=[iDespotism1, iHarmony1, iDiffusion1],
		techs=techs.column(6),
	),
	Civilization(
		iIroquois,
		iGold=300,
		lCivics=[iCouncil1, iConfederacy1, iCaptives1, iMerchants1, iAcculturation1, iCooperation1],
		techs=techs.column(6),
	),
	Civilization(
		iLakota,
		iGold=100,
		lCivics=[iChiefdom1, iCustomaryLaw1, iCaptives1, iMerchants1, iHarmony1, iNomads1],
		techs=techs.column(6),
	),
	Civilization(
		iSpain,
		iLeader=iPhilip,
		iGold=400,
		iImmigration=300,
		iStateReligion=iCatholicism,
		lCivics=[iViceroyalty2, iRoyalColony2, iEncomienda2, iPlunder2, iJesuits2, iConquest2],
		techs=techs.column(14),
		dAttitudes={iPortugal: 2}
	),
	Civilization(
		iPortugal,
		iLeader=iJoao,
		iGold=450,
		iImmigration=300,
		iStateReligion=iCatholicism,
		lCivics=[iProprietaries2, iAdmiralty2, iSlavery2, iFactory2, iProfiteering2, iHomesteads2],
		techs=techs.column(14),
		dAttitudes={iSpain: 2, iEngland: 2, iNetherlands: -2}
	),
	Civilization(
		iEngland,
		iLeader=iVictoria,
		iGold=600,
		iImmigration=300,
		iStateReligion=iProtestantism,
		lCivics=[iGovernors2, iCommonLaw2, iSlavery2, iMercantilism2, iHaven2, iProvidence2],
		techs=techs.column(14).including(iRegiments, iBonds, iMeteorology, iSurveying, iPhysics),
		dAttitudes={iFrance: -4, iPortugal: 2}
	),
	Civilization(
		iFrance,
		iLeader=iLouis,
		iGold=400,
		iImmigration=300,
		iStateReligion=iCatholicism,
		lCivics=[iGovernors2, iCharterColony2, iSlavery2, iFactory2, iHaven2, iOutposts2],
		techs=techs.column(14).including(iRegiments, iBonds, iMeteorology, iSurveying, iPhysics),
		dAttitudes={iEngland: -4, iNetherlands: 2}
	),
	Civilization(
		iNetherlands,
		iLeader=iWilliam,
		iGold=800,
		iImmigration=200,
		iStateReligion=iProtestantism,
		lCivics=[iTrustees2, iTradingCompany2, iSlavery2, iMercantilism2, iProfiteering2, iOutposts2],
		techs=techs.column(14).including(iRegiments, iBonds, iMeteorology),
		dAttitudes={iFrance: 2, iPortugal: -2}
	),
	Civilization(
		iIndependent,
		iGold=500,
		techs=techs.column(14)
	),
	Civilization(
		iIndependent2,
		iGold=500,
		techs=techs.column(14)
	),
	Civilization(
		iIndependent3,
		iGold=500,
		techs=techs.column(14)
	),
	Civilization(
		iNative,
		iGold=300,
		techs=techs.column(7)
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
		iPortugal : [(47, 45), (48, 45), (49, 40), (50, 42), (50, 43), (50, 44)],
		iNetherlands : [(58, 52), (58, 53)],
	},
	iOwnerBaseCulture = 100,
	
	dGreatPeopleCreated = {
		# MacAurther TODO
	},
	dGreatGeneralsCreated = {
		# MacAurther TODO
	},
	
	lInitialWars = [
	],
	
	lAllGoalsFailed = [iMaya, iZapotec, iTeotihuacan, iTiwanaku, iWari, iMississippi, iPuebloan, iChimu, iSpain, iPortugal],
	lGoalsSucceeded = [(iFrance, 0), (iNetherlands, 1)],
	setupGoals = setupGoals,
	
	createStartingUnits = createStartingUnits,
)