from Resources import setupScenarioResources

from Scenario import *
from Locations import *
from RFCUtils import *
from Core import *

	
lCivilizations = [
	Civilization(
		iSpain,
		iLeader=iPhilip,
		iGold=400,
		iStateReligion=iCatholicism,
		lCivics=[],
		techs=techs.column(10).including(iCombinedArms, iGeography, iHorticulture),
		dAttitudes={iPortugal: 2}
	),
	Civilization(
		iFrance,
		iLeader=iLouis,
		iGold=400,
		iStateReligion=iCatholicism,
		lCivics=[],
		techs=techs.column(11).without(iUrbanPlanning, iEconomics),
		dAttitudes={iEngland: -4, iNetherlands: 2}
	),
	Civilization(
		iEngland,
		iLeader=iVictoria,
		iGold=600,
		iStateReligion=iProtestantism,
		lCivics=[],
		techs=techs.column(11).without(iUrbanPlanning, iHorticulture),
		dAttitudes={iFrance: -4, iPortugal: 2}
	),
	Civilization(
		iPortugal,
		iLeader=iJoao,
		iGold=450,
		iStateReligion=iCatholicism,
		lCivics=[],
		techs=techs.column(10).including(iGeography, iHorticulture),
		dAttitudes={iSpain: 2, iEngland: 2, iNetherlands: -2}
	),
	Civilization(
		iNetherlands,
		iLeader=iWilliam,
		iGold=800,
		iStateReligion=iProtestantism,
		lCivics=[],
		techs=techs.column(11).without(iHorticulture, iScientificMethod),
		dAttitudes={iFrance: 2, iPortugal: -2}
	),
	Civilization(
		iIndependent,
		iGold=500,
		techs=techs.column(10)
	),
	Civilization(
		iIndependent2,
		iGold=500,
		techs=techs.column(10)
	),
	Civilization(
		iIndependent3,
		iGold=500,
		techs=techs.column(10)
	),
	Civilization(
		iNative,
		iGold=300,
		techs=techs.column(7)
	),
]

lTribalVillages = [
]
	

def createStartingUnits():
	# MacAurther TODO
	pass

def setupGoals(iCiv, goals):
	# English tech goal
	if iCiv == iEngland:
		goals[2].requirements[0].accumulate(4)
	

scenario1750AD = Scenario(
	iStartYear = 1750,
	fileName = "RFC_1750AD",
	
	lCivilizations = lCivilizations,
	lTribalVillages = lTribalVillages,
	
	dCivilizationDescriptions = {
		iEngland: "TXT_KEY_CIV_BRITAIN_DESC",
	},
	
	dOwnedTiles = {
		iPortugal : [(47, 45), (48, 45), (49, 40), (50, 42), (50, 43), (50, 44)],
		iNetherlands : [(58, 52), (58, 53)],
	},
	iOwnerBaseCulture = 100,
	
	dGreatPeopleCreated = {
		# MacAurther TODO
	},
	dGreatGeneralsCreated = {
		# MacAurther TODO
	},
	
	lInitialWars = [
	],
	
	lAllGoalsFailed = [iSpain, iPortugal],
	lGoalsSucceeded = [(iFrance, 0), (iNetherlands, 1)],
	setupGoals = setupGoals,
	
	createStartingUnits = createStartingUnits,
)