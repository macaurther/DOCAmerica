from Resources import setupScenarioResources

from Scenario import *
from Locations import *
from RFCUtils import *
from Core import *

lCivilizations = [
	Civilization(
		iZapotec,
		iGold=550,
		lCivics=[iAristocracy1, iBureaucracy1, iCraftsmen1, iRedistribution1, iHarmony1, iCooperation1],
		techs=techs.column(6).including(iArtisanry)
	),
	Civilization(
		iMuisca,
		iGold=175,
		lCivics=[iAristocracy1, iBureaucracy1, iCraftsmen1, iRedistribution1, iHarmony1, iCooperation1],
		techs=techs.column(6).including(iArtisanry, iLaw).without(iNavigation, iTrapping, iEarthworks, iLinguistics, iLocalization, iShallowFishing, iFishing)
	),
	Civilization(
		iNorse,
		iGold=75,
		iImmigration=300,
		lCivics=[iViceroyalty2, iEncomienda2, iPlunder2, iConquest2],
		techs=techs.column(9).without(iCartography, iLandmarks, iIrrigation, iLinguistics, iCultivation, iSpiritualism, iShallowFishing, iTrapping, iPathfinding, iEarthworks, iLocalization, iCompanionPlanting, iHerbalism)
	),
	Civilization(
		iInuit,
		iGold=50,
		lCivics=[iDespotism1, iHarmony1, iDiffusion1],
		techs=techs.column(3).including(iCeremony, iSeafaring).without(iLandmarks, iPathfinding, iIrrigation, iEarthworks, iLinguistics, iLocalization, iCultivation, iCompanionPlanting, iHerbalism)
	),
	Civilization(
		iInca,
		iGold=1000,
		lCivics=[iGodKing1, iCustomaryLaw1, iMita1, iRedistribution1, iCosmopolis1, iConquest1],
		techs=techs.column(6)
	),
	Civilization(
		iPurepecha,
		iGold=450,
		lCivics=[iAristocracy1, iCustomaryLaw1, iCraftsmen1, iRedistribution1, iCosmopolis1, iConquest1],
		techs=techs.column(6).without(iTrapping)
	),
	Civilization(
		iAztecs,
		iGold=600,
		lCivics=[iAristocracy1, iCustomaryLaw1, iCaptives1, iPlunder1, iOrganizedReligion1, iDiffusion1],
		techs=techs.column(6).including(iNobility).without(iAstronomy, iScholarship, iNavigation)
	),
	Civilization(
		iIroquois,
		iGold=300,
		lCivics=[iChiefdom1, iConfederacy1, iCommune1, iHarmony1, iCooperation1],
		techs=techs.column(3).including(iProperty, iCeremony).without(iEarthworks, iIrrigation, iPathfinding)
	),
	Civilization(
		iLakota,
		iGold=100,
		lCivics=[iChiefdom1, iHarmony1, iNomads1],
		techs=techs.column(3).including(iCeremony).without(iLandmarks, iPathfinding, iIrrigation, iEarthworks)
	),
	Civilization(
		iSpain,
		iGold=500,
		iStateReligion=iCatholicism,
		lCivics=[iCaptains2, iExpedition2, iSerfdom2, iPlunder2, iJesuits2, iConquest2],
		techs=techs.column(8).including(iGunpowder, iCompanies, iCartography, iEvangelism).without(*lNativeTechs)
	),
	Civilization(
		iIndependent,
		iGold=100,
		techs=techs.column(5)
	),
	Civilization(
		iIndependent2,
		iGold=100,
		techs=techs.column(5)
	),
	Civilization(
		iIndependent3,
		iGold=100,
		techs=techs.column(5)
	),
	Civilization(
		iNative,
		iGold=300,
		techs=techs.column(4)
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
		
