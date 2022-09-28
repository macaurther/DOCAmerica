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

scenario1500AD = Scenario(
	iStartYear = 1500,
	fileName = "RFC_1500AD",
	
	lCivilizations = lCivilizations,
	
	iOwnerBaseCulture = 20,
	
	createStartingUnits = createStartingUnits,
)
		
