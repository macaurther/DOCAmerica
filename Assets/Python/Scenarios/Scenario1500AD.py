from Resources import setupScenarioResources

from Scenario import *
from Locations import *
from RFCUtils import *
from Core import *

lCivilizations = [
	Civilization(
		iZapotec,
		iGold=550,
		lCivics=[iAristocrats1, iBureaucracy1, iCraftsmen1, iRedistribution1, iHarmony1, iIntegration1],
		techs=techs.column(7).including(iArtisanry).without(*lImmigraitonTechs)
	),
	Civilization(
		iMuisca,
		iGold=175,
		lCivics=[iAristocrats1, iBureaucracy1, iCraftsmen1, iRedistribution1, iHarmony1, iIntegration1],
		techs=techs.column(7).including(iArtisanry, iLaw).without(iNavigation, iTrapping, iEarthworks, iLinguistics, iLocalization, iShallowFishing, iFishing, *lImmigraitonTechs)
	),
	Civilization(
		iNorse,
		iGold=75,
		iImmigration=300,
		lCivics=[iViceroys2, iEncomienda2, iPlunder2, iConquest2],
		techs=techs.column(10).without(iCartography, iLandmarks, iIrrigation, iLinguistics, iCultivation, iSpiritualism, iShallowFishing, iTrapping, iPathfinding, iEarthworks, iLocalization, iCompanionPlanting, iHerbalism, iSouthEuropeAccess, iAfricaAccess, iSiberiaAccess, iAsiaAccess)
	),
	Civilization(
		iInuit,
		iGold=50,
		lCivics=[iDespot1, iHarmony1, iSacrifice1],
		techs=techs.column(4).including(iCeremony, iSeafaring).without(iLandmarks, iPathfinding, iIrrigation, iEarthworks, iLinguistics, iLocalization, iCultivation, iCompanionPlanting, iHerbalism, *lImmigraitonTechs)
	),
	Civilization(
		iInca,
		iGold=1000,
		lCivics=[iGodKing1, iClans1, iMita1, iRedistribution1, iCosmopolitans1, iConquest1],
		techs=techs.column(7).without(*lImmigraitonTechs)
	),
	Civilization(
		iPurepecha,
		iGold=450,
		lCivics=[iAristocrats1, iClans1, iCraftsmen1, iRedistribution1, iCosmopolitans1, iConquest1],
		techs=techs.column(7).without(iTrapping, *lImmigraitonTechs)
	),
	Civilization(
		iAztecs,
		iGold=600,
		lCivics=[iAristocrats1, iClans1, iTlacotin1, iRaiding1, iOrganizedReligion1, iSacrifice1],
		techs=techs.column(7).including(iNobility).without(iAstronomy, iScholarship, iNavigation, *lImmigraitonTechs)
	),
	Civilization(
		iHaudenosaunee,
		iGold=300,
		lCivics=[iChief1, iTribalConfederacy1, iCalpulli1, iHarmony1, iIntegration1],
		techs=techs.column(4).including(iProperty, iCeremony).without(iEarthworks, iIrrigation, iPathfinding, *lImmigraitonTechs)
	),
	Civilization(
		iLakota,
		iGold=100,
		lCivics=[iChief1, iHarmony1, iNomads1],
		techs=techs.column(4).including(iCeremony).without(iLandmarks, iPathfinding, iIrrigation, iEarthworks, *lImmigraitonTechs)
	),
	Civilization(
		iSpain,
		iGold=500,
		iStateReligion=iCatholicism,
		lCivics=[iCaptains2, iExpedition2, iSerfdom2, iPlunder2, iJesuits2, iConquest2],
		techs=techs.column(9).including(iGunpowder, iCompanies, iCartography, iEvangelism).without(iNorthEuropeAccess, iAfricaAccess, iSiberiaAccess, iAsiaAccess, *lNativeTechs)
	),
	Civilization(
		iIndependent,
		iGold=100,
		techs=techs.column(6).without(*lImmigraitonTechs)
	),
	Civilization(
		iIndependent2,
		iGold=100,
		techs=techs.column(6).without(*lImmigraitonTechs)
	),
	Civilization(
		iIndependent3,
		iGold=100,
		techs=techs.column(9).without(*lImmigraitonTechs)
	),
	Civilization(
		iIndigenous,
		iGold=300,
		techs=techs.column(5).without(*lImmigraitonTechs)
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
		
