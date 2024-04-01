from Scenario import *
from Core import *


lCivilizations = [
	Civilization(
		iMaya,
		iGold=75,
		lCivics=[iCaptives],
		techs=techs.column(2).including(iPottery, iAgriculture, iMythology, iMining, iTanning, iMasonry, iProperty).without(iTrapping, iPathfinding, iLinguistics, iLocalization, iShallowFishing, iFishing, iHerbalism)
	),
	Civilization(
		iTeotihuacan,
		iGold=50,
		techs=techs.column(2).including(iTanning, iPottery, iAgriculture, iTanning, iSmelting, iMasonry).without(iPathfinding, iLinguistics, iLocalization, iShallowFishing, iFishing)
	),
	Civilization(
		iZapotec,
		iGold=100,
		techs=techs.column(2).including(iPottery, iAgriculture, iMythology, iTanning, iMining, iSmelting).without(iTrapping, iPathfinding, iLinguistics, iLocalization, iShallowFishing, iFishing)
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


scenario0AD = Scenario(
	iStartYear = 0,
	fileName = "RFC_0AD",
	
	lCivilizations = lCivilizations,
)
