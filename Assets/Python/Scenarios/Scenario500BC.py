from Scenario import *
from Core import *


lCivilizations = [
	Civilization(
		iMaya,
		iGold=75,
		lCivics=[iCaptives1],
		techs=techs.column(2).including(iAgriculture, iMythology, iMining).without(iTrapping, iPathfinding, iLinguistics, iLocalization, iShallowFishing, iFishing)
	),
	Civilization(
		iZapotec,
		iGold=100,
		techs=techs.column(2).including(iAgriculture, iMythology, iTanning).without(iTrapping, iLinguistics, iLocalization, iShallowFishing, iFishing)
	),
	Civilization(
		iNative,
		techs=techs.column(2).including(iTanning, iMythology)
	),
	Civilization(
		iIndependent,
		techs=techs.column(2)
	),
	Civilization(
		iIndependent2,
		techs=techs.column(2)
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
