from Consts import *
from RFCUtils import utils

def getModifier(iPlayer, iModifier):
	iCivilization = gc.getPlayer(iPlayer).getCivilizationType()
	if iCivilization in lOrder:
		return tModifiers[iModifier][lOrder.index(iCivilization)]
	return tDefaults[iModifier]
	
def getAdjustedModifier(iPlayer, iModifier):
	if utils.getScenario() > i3000BC and iPlayer < iVikings:
		if iModifier in dLateScenarioModifiers:
			return getModifier(iPlayer, iModifier) * dLateScenarioModifiers[iModifier] / 100
	return getModifier(iPlayer, iModifier)
	
def setModifier(iPlayer, iModifier, iNewValue):
	gc.getPlayer(iPlayer).setModifier(iModifier, iNewValue)
	
def changeModifier(iPlayer, iModifier, iChange):
	setModifier(iPlayer, iModifier, gc.getPlayer(iPlayer).getModifier(iModifier) + iChange)
	
def adjustModifier(iPlayer, iModifier, iPercent):
	setModifier(iPlayer, iModifier, gc.getPlayer(iPlayer).getModifier(iModifier) * iPercent / 100)
	
def adjustModifiers(iPlayer):
	for iModifier in dLateScenarioModifiers:
		adjustModifier(iPlayer, iModifier, dLateScenarioModifiers[iModifier])
		
def adjustInflationModifier(iPlayer):
	adjustModifier(iPlayer, iModifierInflationRate, dLateScenarioModifiers[iModifierInflationRate])
	
def updateModifier(iPlayer, iModifier):
	setModifier(iPlayer, iModifier, getModifier(iPlayer, iModifier))
	
def updateModifiers(iPlayer):
	for iModifier in range(iNumModifiers):
		updateModifier(iPlayer, iModifier)
		
def init():
	for iPlayer in range(iNumTotalPlayersB):
		updateModifiers(iPlayer)
		
		if utils.getScenario() > i3000BC and iPlayer < iVikings:
			adjustModifiers(iPlayer)
		
		gc.getPlayer(iPlayer).updateMaintenance()
		

### Modifier types ###

iNumModifiers = 13
(iModifierCulture, iModifierUnitUpkeep, iModifierResearchCost, iModifierDistanceMaintenance, iModifierCitiesMaintenance,
iModifierCivicUpkeep, iModifierHealth, iModifierUnitCost, iModifierWonderCost, iModifierBuildingCost,
iModifierInflationRate, iModifierGreatPeopleThreshold, iModifierGrowthThreshold) = range(iNumModifiers)

### Sequence of spawns ###

lOrder = [iCivSpain, iCivFrance, iCivEngland, iCivAmerica, iCivCanada, iCivIndependent, iCivIndependent2, iCivNative, iCivBarbarian]

### Modifiers (by civilization!) ###

#                          SPA FRA ENG AME CAN     IND IND NAT SEL BAR 

tCulture =               ( 100,100,100,100,100,    100,100,100,100,100 )

tUnitUpkeep =            ( 100,100,100,100,100,    100,100,100,100,100 )
tResearchCost =          ( 100,100,100,100,100,    100,100,100,100,100 )
tDistanceMaintenance =   ( 100,100,100,100,100,    100,100,100,100,100 )
tCitiesMaintenance =     ( 100,100,100,100,100,    100,100,100,100,100 )
tCivicUpkeep =           ( 100,100,100,100,100,    100,100,100,100,100 )
tHealth =                ( 100,100,100,100,100,    100,100,100,100,100 )

tUnitCost =              ( 100,100,100,100,100,    100,100,100,100,100 )
tWonderCost =            ( 100,100,100,100,100,    100,100,100,100,100 )
tBuildingCost =          ( 100,100,100,100,100,    100,100,100,100,100 )
tInflationRate =         ( 100,100,100,100,100,    100,100,100,100,100 )
tGreatPeopleThreshold =  ( 100,100,100,100,100,    100,100,100,100,100 )
tGrowthThreshold =       ( 100,100,100,100,100,    100,100,100,100,100 )

tModifiers = (tCulture, tUnitUpkeep, tResearchCost, tDistanceMaintenance, tCitiesMaintenance, tCivicUpkeep, tHealth, tUnitCost, tWonderCost, tBuildingCost, tInflationRate, tGreatPeopleThreshold, tGrowthThreshold)

tDefaults = (100, 100, 100, 100, 100, 100, 2, 100, 100, 100, 100, 100, 100)

dLateScenarioModifiers = {
iModifierUnitUpkeep : 90,
iModifierDistanceMaintenance : 85,
iModifierCitiesMaintenance : 80,
iModifierCivicUpkeep : 90,
iModifierInflationRate : 85,
iModifierGreatPeopleThreshold : 85,
iModifierGrowthThreshold : 80,
}