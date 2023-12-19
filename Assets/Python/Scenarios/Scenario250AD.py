from Scenario import *
from Core import *


lCivilizations = [
	Civilization(
		iMaya,
		iGold=50,
		techs=techs.column(2).including(iPottery, iAgriculture, iMythology).without(iTrapping, iPathfinding, iLocalization, iShallowFishing, iFishing)
	),
	Civilization(
		iTeotihuacan,
		iGold=50,
		techs=techs.column(2).including(iPottery, iAgriculture).without(iPathfinding, iLinguistics, iLocalization, iShallowFishing, iFishing)
	),
	Civilization(
		iTiwanaku,
		iGold=50,
		techs=techs.column(2).including(iAgriculture, iPastoralism, iMining).without(iTrapping, iLinguistics, iLocalization, iShallowFishing, iFishing)
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


scenario250AD = Scenario(
	iStartYear = 250,
	fileName = "RFC_250AD",
	
	lCivilizations = lCivilizations,
)
