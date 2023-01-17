from Scenario import *
from Core import *


lCivilizations = [
	Civilization(
		iMaya,
		iGold=200,
		techs=techs.column(1).including(iPottery, iAgriculture, iMythology)
	),
	Civilization(
		iTeotihuacan,
		iGold=50,
		techs=techs.column(1).including(iPottery, iAgriculture, iMining)
	),
	Civilization(
		iTiwanaku,
		iGold=50,
		techs=techs.column(1).including(iPottery, iAgriculture, iPastoralism)
	),
	Civilization(
		iNative,
		techs=techs.of(iTanning, iMythology)
	),
	Civilization(
		iIndependent
	),
	Civilization(
		iIndependent2
	),
]


scenario250AD = Scenario(
	iStartYear = 250,
	fileName = "RFC_250AD",
	
	lCivilizations = lCivilizations,
)
