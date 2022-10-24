from Scenario import *
from Core import *


lCivilizations = [
	Civilization(
		iMaya,
		techs=techs.of(iMining, iPottery, iAgriculture)
	),
	Civilization(
		iTeotihuacan,
		techs=techs.of(iMining, iPottery, iAgriculture)
	),
	Civilization(
		iTiwanaku,
		techs=techs.of(iMining, iPottery, iAgriculture)
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
