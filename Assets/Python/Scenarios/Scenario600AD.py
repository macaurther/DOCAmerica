from Resources import setupScenarioResources

from Scenario import *
from Locations import *
from RFCUtils import *
from Core import *

lCivilizations = [
	Civilization(
		iIndependent,
		iGold=100,
		techs=techs.column(5)
	),
	Civilization(
		iIndependent2,
		iGold=100,
		techs=techs.column(5)
	),
	Civilization(
		iNative,
		iGold=300,
		techs=techs.column(4)
	)
]


def createStartingUnits():
	pass

scenario600AD = Scenario(
	iStartYear = 600,
	fileName = "RFC_600AD",
	
	lCivilizations = lCivilizations,
	
	iOwnerBaseCulture = 20,
	
	createStartingUnits = createStartingUnits,
)
		
