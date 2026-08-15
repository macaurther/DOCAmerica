from Resources import setupScenarioResources

from Scenario import *
from Locations import *
from RFCUtils import *
from Core import *

lCivilizations = [
	Civilization(
		iMuisca,
		iGold=1000,
		lCivics=[iAristocrats, iBureaucracy, iCraftsmen, iRedistribution, iHarmony, iIntegration],
		techs=techs.column(6).without(iSeafaring),
		extraTechs=techs.column(0).including(iHunting, iLandmarks, iPathfinding, iIrrigation, iCultivation, iCompanionPlanting, iKnapping),
	),
	Civilization(
		iNorse,
		iGold=250,
		techs=techs.column(9).without(iExchange),
		extraTechs=techs.column(0).including(iNorthEuropeAccess, iHunting, iTrapping, iFishing),
	),
	Civilization(
		iPueblo,
		iGold=350,
		lCivics=[iSubsistance],
		techs=techs.column(5),
		extraTechs=techs.column(0).including(iHunting, iLandmarks, iPathfinding, iIrrigation, iEarthworks, iCompanionPlanting),
	),
	Civilization(
		iArawak,
		iGold=150,
		lCivics=[iChief, iClans, iHarmony, iNomadic],
		techs=techs.column(3).including(iNavigation, iTradeRoutes).without(iMining),
		extraTechs=techs.column(0).including(iHunting, iTrapping, iCompanionPlanting, iInterpretation, iMediation, iFishing, iIrrigation, iHerbalism),
	),
	Civilization(
		iTupi,
		iGold=150,
		lCivics=[iChief, iClans, iHarmony, iNomadic],
		techs=techs.column(3).including(iNavigation, iTradeRoutes).without(iMining),
		extraTechs=techs.column(0).including(iHunting, iTrapping, iCompanionPlanting, iInterpretation, iMediation, iFishing, iHerbalism),
	),
	Civilization(
		iPurepecha,
		iGold=450,
		lCivics=[iAristocrats, iVassalage, iCraftsmen, iRedistribution, iCosmopolitans, iConquest],
		techs=techs.column(7),
		extraTechs=techs.column(0).including(iHunting, iLandmarks, iPathfinding, iIrrigation, iCompanionPlanting, iKnapping, iDiving, iFishing),
	),
	Civilization(
		iInuit,
		iGold=100,
		lCivics=[iHarmony, iClans],
		techs=techs.column(4).including(iTradeRoutes),
		extraTechs=techs.column(0).including(iHunting, iTrapping, iFishing, iMediation),
	),
	Civilization(
		iInca,
		iGold=1000,
		lCivics=[iGodKing, iBureaucracy, iMita, iMerchantTrade, iOrganizedReligion, iConquest],
		techs=techs.column(7),
		extraTechs=techs.column(0).including(iLandmarks, iPathfinding, iIrrigation, iEarthworks, iCultivation, iCompanionPlanting, iInterpretation, iMediation),
	),
	Civilization(
		iAztec,
		iGold=600,
		lCivics=[iGodKing, iVassalage, iCasteSystem, iRedistribution, iSacrifice, iTributaries],
		techs=techs.column(7),
		extraTechs=techs.column(0).including(iHunting, iLandmarks, iPathfinding, iIrrigation, iCompanionPlanting, iKnapping, iFishing),
	),
	Civilization(
		iHaudenosaunee,
		iGold=200,
		lCivics=[iCouncil, iTribalConfederacy, iHarmony, iIntegration],
		techs=techs.column(3).including(iProperty, iCeremony, iDivination),
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
		iIndependent1,
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
	pass

def setupGoals(iCiv, goals):
	if iCiv == iNorse:
		goals[0].requirements[0].succeed()
		goals[0].requirements[1].succeed()
		goals[0].requirements[2].succeed()
	elif iCiv == iPurepecha:
		goals[1].requirements[1].requirements[0].accumulate(20)

scenario1500AD = Scenario(
	iStartYear = 1500,
	fileName = "RFC_1500AD",
	
	lCivilizations = lCivilizations,
	lTribalVillages = lTribalVillages,
	
	iOwnerBaseCulture = 20,
	
	dGreatPeopleCreated = {
		iInca: 2,
		iAztec: 1,
		iMuisca: 1,
		iPurepecha: 1,
		iHaudenosaunee: 1,
	},
	dGreatGeneralsCreated = {
		iInca: 1,
		iAztec: 2,
		iMuisca: 1,
		iPurepecha: 1,
	},
	
	lAllGoalsFailed = [iMaya, iZapotec, iTeotihuacan, iTiwanaku, iWari, iMississippi, iPueblo, iChimu],
	setupGoals = setupGoals,
	
	createStartingUnits = createStartingUnits,
)
		
