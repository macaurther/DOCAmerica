from Scenario import *
from Core import *


lCivilizations = [
	Civilization(
		iMaya,
		iGold=75,
		lCivics=[iTlacotin, iDespot],
		techs=techs.column(2).including(iTanning, iMining, iPottery, iAgriculture, iMythology, iDugouts, iProperty),
		extraTechs=techs.column(0).including(iHerbalism, iIrrigation, iEarthworks, iCultivation, iCompanionPlanting),
	),
	Civilization(
		iZapotec,
		iGold=100,
		lCivics=[iTlacotin, iRedistribution, iMonarch],
		techs=techs.column(2).including(iTanning, iMining, iPottery, iAgriculture, iMythology, iDugouts, iCeremony),
		extraTechs=techs.column(0).including(iLandmarks, iIrrigation, iEarthworks, iCultivation, iCompanionPlanting, iDiving),
	),
	Civilization(
		iTeotihuacan,
		iGold=50,
		lCivics=[iTlacotin, iRedistribution, iMonarch],
		techs=techs.column(2).including(iTanning, iMining, iPottery, iAgriculture, iMythology, iDugouts, iDivination),
		extraTechs=techs.column(0).including(iLandmarks, iPathfinding, iIrrigation, iEarthworks, iCultivation, iCompanionPlanting),
	),
	Civilization(
		iIndependent1,
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

scenario1AD = Scenario(
	iStartYear = 0,
	fileName = "RFC_1AD",
	
	lCivilizations = lCivilizations,
	lTribalVillages = lTribalVillages,
	
	createStartingUnits = createStartingUnits,
)
