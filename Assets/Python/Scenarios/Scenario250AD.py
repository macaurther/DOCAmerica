from Scenario import *
from Core import *


lCivilizations = [
	Civilization(
		iMaya,
		techs=techs.of(iMining, iPottery, iAgriculture)
	),
]


scenario250AD = Scenario(
	iStartYear = 250,
	fileName = "RFC_250AD",
	
	lCivilizations = lCivilizations,
)
