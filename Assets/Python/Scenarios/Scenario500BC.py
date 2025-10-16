from Scenario import *
from Core import *


lCivilizations = [
	Civilization(
		iMaya,
		iGold=75,
		lCivics=[iTlacotin1],
		techs=techs.column(2).including(iAgriculture, iMythology, iMining).without(iTrapping, iPathfinding, iLinguistics, iLocalization, iShallowFishing, iFishing)
	),
	Civilization(
		iZapotec,
		iGold=100,
		techs=techs.column(2).including(iAgriculture, iMythology, iTanning).without(iTrapping, iLinguistics, iLocalization, iShallowFishing, iFishing)
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
	Civilization(
		iIndigenous,
		techs=techs.column(2).including(iTanning, iMythology)
	),
	Civilization(
		iBarbarian,
	)
]

lTribalVillages = [
]


def createStartingUnits():
	if not player(iMaya).isHuman():
		makeUnit(iMaya, iArcher, plots.capital(iMaya))
	if not player(iZapotec).isHuman():
		makeUnit(iZapotec, iArcher, plots.capital(iZapotec))

scenario500BC = Scenario(
	iStartYear = -500,
	fileName = "RFC_500BC",
	
	lCivilizations = lCivilizations,
	lTribalVillages = lTribalVillages,
	
	createStartingUnits = createStartingUnits,
)
