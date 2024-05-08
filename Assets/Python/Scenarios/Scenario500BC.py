from Scenario import *
from Core import *


lCivilizations = [
	Civilization(
		iMaya,
		iGold=75,
		lCivics=[iCaptives1],
		techs=techs.column(2).including(iPottery, iAgriculture, iMythology, iMining, iTanning, iMasonry, iProperty).without(iTrapping, iPathfinding, iLinguistics, iLocalization, iShallowFishing, iFishing, iHerbalism)
	),
	Civilization(
		iZapotec,
		iGold=100,
		techs=techs.column(2).including(iPottery, iAgriculture, iMythology, iTanning, iMining, iSmelting).without(iTrapping, iLinguistics, iLocalization, iShallowFishing, iFishing)
	),
	Civilization(
		iNative,
		techs=techs.column(2).including(iTanning, iMythology)
	),
	Civilization(
		iIndependent
	),
	Civilization(
		iIndependent2
	),
	Civilization(
		iIndependent3
	),
]


scenario500BC = Scenario(
	iStartYear = -500,
	fileName = "RFC_500BC",
	
	lCivilizations = lCivilizations,
)
