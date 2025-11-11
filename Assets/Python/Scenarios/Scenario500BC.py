from Scenario import *
from Core import *


lCivilizations = [
	Civilization(
		iMaya,
		iGold=75,
		lCivics=[iTlacotin],
		techs=techs.column(2).including(iAgriculture, iMythology, iMining),
		extraTechs=techs.column(0).including(iLandmarks, iIrrigation, iEarthworks, iCultivation, iCompanionPlanting),
	),
	Civilization(
		iZapotec,
		iGold=100,
		techs=techs.column(2).including(iAgriculture, iMythology, iTanning),
		extraTechs=techs.column(0).including(iLandmarks, iIrrigation, iEarthworks, iCultivation, iCompanionPlanting, iDiving),
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
