from Resources import setupScenarioResources

from Scenario import *
from Locations import *
from RFCUtils import *
from Core import *

lCivilizations = [
	Civilization(
		iZapotec,
		iGold=550,
		lCivics=[iAristocrats, iBureaucracy, iCraftsmen, iRedistribution, iHarmony, iIntegration],
		techs=techs.column(7).including(iArtisanry)
	),
	Civilization(
		iMuisca,
		iGold=175,
		lCivics=[iAristocrats, iBureaucracy, iCraftsmen, iRedistribution, iHarmony, iIntegration],
		techs=techs.column(7).including(iArtisanry, iLaw).without(iNavigation, iTrapping, iEarthworks, iLinguistics, iLocalization, iDiving, iFishing)
	),
	Civilization(
		iNorse,
		iGold=75,
		iImmigration=300,
		lCivics=[iViceroys, iEncomienda, iPlunder, iImperialism],
		techs=techs.column(10).without(iCartography, iLandmarks, iIrrigation, iLinguistics, iCultivation, iKnapping, iDiving, iTrapping, iPathfinding, iEarthworks, iLocalization, iCompanionPlanting, iHerbalism, iSouthEuropeAccess, iAfricaAccess, iSiberiaAccess, iAsiaAccess)
	),
	Civilization(
		iInuit,
		iGold=50,
		lCivics=[iDespot, iHarmony, iSacrifice],
		techs=techs.column(4).including(iCeremony, iSeafaring).without(iLandmarks, iPathfinding, iIrrigation, iEarthworks, iLinguistics, iLocalization, iCultivation, iCompanionPlanting, iHerbalism)
	),
	Civilization(
		iInca,
		iGold=1000,
		lCivics=[iGodKing, iClans, iMita, iRedistribution, iCosmopolitans, iConquest],
		techs=techs.column(7)
	),
	Civilization(
		iPurepecha,
		iGold=450,
		lCivics=[iAristocrats, iClans, iCraftsmen, iRedistribution, iCosmopolitans, iConquest],
		techs=techs.column(7).without(iTrapping)
	),
	Civilization(
		iAztecs,
		iGold=600,
		lCivics=[iAristocrats, iClans, iTlacotin, iRaiding, iOrganizedReligion, iSacrifice],
		techs=techs.column(7).including(iNobility).without(iAstronomy, iScholarship, iNavigation)
	),
	Civilization(
		iHaudenosaunee,
		iGold=300,
		lCivics=[iChief, iTribalConfederacy, iCalpulli, iHarmony, iIntegration],
		techs=techs.column(4).including(iProperty, iCeremony).without(iEarthworks, iIrrigation, iPathfinding)
	),
	Civilization(
		iLakota,
		iGold=100,
		lCivics=[iChief, iHarmony, iNomads],
		techs=techs.column(4).including(iCeremony).without(iLandmarks, iPathfinding, iIrrigation, iEarthworks)
	),
	Civilization(
		iSpain,
		iGold=500,
		iStateReligion=iCatholicism,
		lCivics=[iCaptains, iExpedition, iSerfdom, iPlunder, iJesuits, iImperialism],
		techs=techs.column(9).including(iGunpowder, iCompanies, iCartography, iEvangelism).without(iNorthEuropeAccess, iAfricaAccess, iSiberiaAccess, iAsiaAccess)
	),
	Civilization(
		iIndependent,
		iGold=100,
		techs=techs.column(6)
	),
	Civilization(
		iIndependent2,
		iGold=100,
		techs=techs.column(6)
	),
	Civilization(
		iIndependent3,
		iGold=100,
		techs=techs.column(9)
	),
	Civilization(
		iIndigenous,
		iGold=300,
		techs=techs.column(5)
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
	# Haudenosaunee tribe goal
	#if iCiv == iHaudenosaunee:
	#	goals[0].requirements[0].accumulate(1)

scenario1500AD = Scenario(
	iStartYear = 1500,
	fileName = "RFC_1500AD",
	
	lCivilizations = lCivilizations,
	lTribalVillages = lTribalVillages,
	
	iOwnerBaseCulture = 20,
	
	dGreatPeopleCreated = {
		# MacAurther TODO
	},
	dGreatGeneralsCreated = {
		# MacAurther TODO
	},
	
	lAllGoalsFailed = [iMaya, iZapotec, iTeotihuacan, iTiwanaku, iWari, iMississippi, iPuebloan, iChimu],
	setupGoals = setupGoals,
	
	createStartingUnits = createStartingUnits,
)
		
