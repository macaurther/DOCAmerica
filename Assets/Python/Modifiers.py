from Consts import *
from RFCUtils import *
from Events import *

def getModifier(iCivilization, iModifier):
	if iCivilization in lCivOrder:
		return tModifiers[iModifier][lCivOrder.index(iCivilization)]
	return tDefaults[iModifier]
	
def getAdjustedModifier(iPlayer, iModifier):
	if scenario() > i500BC and dBirth[iPlayer] < dBirth[iSpain]:
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
	
	if scenario() > i500BC and dBirth[iPlayer] < dBirth[iSpain]:
		adjustModifiers(iPlayer)
	
	player(iPlayer).updateMaintenance()


@handler("BeginGameTurn")
def updateLateModifiers(iGameTurn):			
	if scenario() == i500BC and iGameTurn == year(1700):
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
NCE = 90	# Num Cities Euro

# 				            MAY TEO ZAP TIW WAR MIS PUE MUI NOR CHI INU INC PUR AZT IRO SIO SPA POR ENG FRA NET HAW RUS AME HAI ARG MEX COL PER VEN BRA CAN     IND IND IND NAT BAR 

tCulture =		          ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,     20, 20, 20, 20, 30 )
                                                                                                                                                        
tUnitUpkeep = 		      ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,      0,  0,  0,100,100 )
tResearchCost = 	      ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,    110,110,999,110,110 )
tDistanceMaintenance = 	  ( DMN,DMN,DMN,DMN,DMN,DMN,DMN,DMN,DME,DMN, 25,DMN,DMN,DMN,DMN,DMN,DME,DME,DME,DME,DME,DMN,DME,DME,DME,DME,DME,DME,DME,DME,DME,DME,     25, 25, 25, 25, 25 )	# Larger map = make distance less of a penalty
tColonyMaintenance = 	  ( NCN,NCN,NCN,NCN,NCN,NCN,NCN,NCN,NCE,NCN,NCN,NCN,NCN,NCN,NCN,NCE,NCE,NCE,NCE,NCE,NCE,NCN,NCE,NCE,NCE,NCE,NCE,NCE,NCE,NCE,NCE,NCE,     50, 50, 50, 50, 50 )	# Larger map = make num cities less of a penalty
tCitiesMaintenance = 	  ( NCN,NCN,NCN,NCN,NCN,NCN,NCN,NCN,NCE,NCN,NCN,NCN,NCN,NCN,NCN,NCE,NCE,NCE,NCE,NCE,NCE,NCN,NCE,NCE,NCE,NCE,NCE,NCE,NCE,NCE,NCE,NCE,     50, 50, 50, 50, 50 )	# Larger map = make num cities less of a penalty
tCivicUpkeep = 		      ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,     70, 70, 70, 70, 70 )
tHealth = 		      	  (   2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,      0,  0,  0,  0,  0 )
                                                                                                                                                        
tUnitCost = 		      ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,    200,200,200,150,140 )
tWonderCost = 		      ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,    150,150,500,150,100 )
tBuildingCost = 	      ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,    100,100,500,150,100 )
tInflationRate = 	      ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,     95, 95, 95, 95, 95 )
tGreatPeopleThreshold =   ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,    100,100,500,100,100 )
tGrowthThreshold = 	      ( 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,    125,125,125,125,125 )

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