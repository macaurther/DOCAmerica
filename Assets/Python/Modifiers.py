from Consts import *
from RFCUtils import *
from Events import *

def getModifier(iCivilization, iModifier):
	if iCivilization in lCivOrder:
		return tModifiers[iModifier][lCivOrder.index(iCivilization)]
	return tDefaults[iModifier]
	
def getAdjustedModifier(iPlayer, iModifier):
	if scenario() > i1AD and dBirth[iPlayer] < dBirth[iSpain]:
		if iModifier in dLateScenarioModifiers:
			return getModifier(iPlayer, iModifier) * dLateScenarioModifiers[iModifier] / 100
	return getModifier(iPlayer, iModifier)
	
def setModifier(iPlayer, iModifier, iNewValue):
	player(iPlayer).setModifier(iModifier, iNewValue)
	
def changeModifier(iPlayer, iModifier, iChange):
	setModifier(iPlayer, iModifier, player(iPlayer).getModifier(iModifier) + iChange)
	
def adjustModifier(iPlayer, iModifier, iPercent):
	setModifier(iPlayer, iModifier, player(iPlayer).getModifier(iModifier) * iPercent / 100)
	
def adjustModifiers(iPlayer):
	for iModifier in dLateScenarioModifiers:
		adjustModifier(iPlayer, iModifier, dLateScenarioModifiers[iModifier])
		
def adjustInflationModifier(iPlayer):
	adjustModifier(iPlayer, iModifierInflationRate, dLateScenarioModifiers[iModifierInflationRate])
	
def updateModifier(iPlayer, iCivilization, iModifier):
	setModifier(iPlayer, iModifier, getModifier(iCivilization, iModifier))
	
def updateModifiers(iPlayer, iCivilization):
	for iModifier in range(iNumModifiers):
		updateModifier(iPlayer, iCivilization, iModifier)


@handler("playerCivAssigned")
def init(iPlayer, iCivilization):
	updateModifiers(iPlayer, iCivilization)
	
	if scenario() > i1AD and dBirth[iPlayer] < dBirth[iSpain]:
		adjustModifiers(iPlayer)
	
	player(iPlayer).updateMaintenance()


@handler("BeginGameTurn")
def updateLateModifiers(iGameTurn):			
	if scenario() == i1AD and iGameTurn == year(1700):
		for iPlayer in players.major().where(lambda p: dBirth[p] < dBirth[iSpain]):
			adjustInflationModifier(iPlayer)
		

### Modifier types ###

iNumModifiers = 14
(iModifierCulture, iModifierUnitUpkeep, iModifierResearchCost, iModifierDistanceMaintenance, iModifierColonyMaintenance,
iModifierCitiesMaintenance, iModifierCivicUpkeep, iModifierHealth, iModifierUnitCost, iModifierWonderCost, 
iModifierBuildingCost, iModifierInflationRate, iModifierGreatPeopleThreshold, iModifierGrowthThreshold) = range(iNumModifiers)

### Modifiers (by civilization, birth order!) ###
DMN = 75	# Distance Maintenance Native
DME = 50	# Distance Maintenance Euro
NCN = 100	# Num Cities Native
NCE = 80	# Num Cities Euro

# 				            MAY ZAP TEO TIW WAR MIS MUI TOL NOR CHI PUE ARA TUP PUR INU INC AZT HAU SPA POR CHE ENG FRA NET LAK APA HAW RUS AME HAI ARG MEX COL PER VEN BRA CSA CAN      IND IND IND NAT BAR 

tCulture =		          ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,     20, 20, 10, 20, 30 )	# Culture
                                                                                                                                                                            
tUnitUpkeep = 		      ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,     50, 50, 50,100,100 )	# Unit Upkeep
tResearchCost = 	      ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80,    125,125,500,125,110 )	# Research Cost
tDistanceMaintenance = 	  ( DMN,DMN,DMN,DMN,DMN,DMN,DMN,DMN,DME,DMN,DMN,DMN,DMN,DMN,DMN,DMN,DMN,DMN,DME,DME,DMN,DME,DME,DME,DMN,DMN,DMN,DME,DME,DME,DME,DME,DME,DME,DME,DME,DME,DME,    100,100,100,100, 20 )	# Distance Maintenance
tColonyMaintenance = 	  ( NCN,NCN,NCN,NCN,NCN,NCN,NCN,NCN,NCE,NCN,NCN,NCN,NCN,NCN,NCN,NCN,NCN,NCN,NCE,NCE,NCN,NCE,NCE,NCE,NCN,NCN,NCN,NCE,NCE,NCE,NCE,NCE,NCE,NCE,NCE,NCE,NCE,NCE,    100,100,100,100, 20 )	# Colony Maintenance
tCitiesMaintenance = 	  ( NCN,NCN,NCN,NCN,NCN,NCN,NCN,NCN,NCE,NCN,NCN,NCN,NCN,NCN,NCN,NCN,NCN,NCN,NCE,NCE,NCN,NCE,NCE,NCE,NCN,NCN,NCN,NCE,NCE,NCE,NCE,NCE,NCE,NCE,NCE,NCE,NCE,NCE,    100,100,100,100, 30 )	# Cities Maintenance
tCivicUpkeep = 		      ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100, 85,100, 85, 85, 85,100,100,100, 85, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70,    100,100,100,100, 70 )	# Civic Upkeep
tHealth = 		      	  (   2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,      0,  0,  0,  0,  0 )	# Health
                                                                                                                                                                            
tUnitCost = 		      ( 100,100,100,100,100,100,100,100, 90,100,100,100,100,100,100,100,100,100,100, 90,100, 90, 90, 90,100,100,100, 90, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80,    300,300,300,150,140 )	# Unit Cost
tWonderCost = 		      ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,    150,150,150,150,100 )	# Wonder Cost
tBuildingCost = 	      ( 100,100,100,100,100,100,100,100, 90,100,100,100,100,100,100,100,100,100,100, 90,100, 90, 90, 90,100,100,100, 90, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80,    100,100,150,150,100 )	# Building Cost
tInflationRate = 	      ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100, 85,100, 85, 85, 85,100,100,100, 85, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70,     95, 95, 95, 95, 95 )	# Inflation Rate
tGreatPeopleThreshold =   ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,    100,100,500,100,100 )	# Great People Threshold
tGrowthThreshold = 	      ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,    125,125,500,125,125 )	# Growth Threshold

tModifiers = (tCulture, tUnitUpkeep, tResearchCost, tDistanceMaintenance, tColonyMaintenance, tCitiesMaintenance, tCivicUpkeep, tHealth, tUnitCost, tWonderCost, tBuildingCost, tInflationRate, tGreatPeopleThreshold, tGrowthThreshold)

tDefaults = (100, 100, 100, 100, 100, 100, 100, 2, 100, 100, 100, 100, 100, 100)

dLateScenarioModifiers = {
iModifierUnitUpkeep :100,
iModifierDistanceMaintenance :100,
iModifierCitiesMaintenance :100,
iModifierCivicUpkeep :100,
iModifierInflationRate :100,
iModifierGreatPeopleThreshold :100,
iModifierGrowthThreshold :100,
}