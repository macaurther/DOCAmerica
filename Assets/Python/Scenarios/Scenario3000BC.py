from Scenario import *
from Core import *


lCivilizations = [
	Civilization(
		iMaya,
		techs=techs.of(iMining, iPottery, iAgriculture)
	),
]


scenario3000BC = Scenario(
	iStartYear = 250,
	fileName = "RFC_3000BC",
	
	lCivilizations = lCivilizations,
)
