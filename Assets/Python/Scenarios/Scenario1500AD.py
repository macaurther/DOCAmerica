from Resources import setupScenarioResources

from Scenario import *
from Locations import *
from RFCUtils import *
from Core import *

lCivilizations = [
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
		iIroquois,
		iGold=600,
		lCivics=[iConfederacy, iCouncil],
		techs=techs.column(2).including(iCalendar).without(iNavigation)
	),
	Civilization(
		iSpain,
		iGold=200,
		iStateReligion=iCatholicism,
		lCivics=[iColony, iConquest],
		techs=techs.column(6).without(*lNativeTechs)
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


def createStartingUnits():
	pass

scenario1500AD = Scenario(
	iStartYear = 1500,
	fileName = "RFC_1500AD",
	
	lCivilizations = lCivilizations,
	
	iOwnerBaseCulture = 20,
	
	createStartingUnits = createStartingUnits,
)
		
