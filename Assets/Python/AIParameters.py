from Core import *
from RFCUtils import *
from Events import handler

def getTakenTilesThreshold(iPlayer):
	return dTakenTilesThreshold[iPlayer]
	
def getDistanceSubtrahend(iPlayer):
	return dDistanceSubtrahend[iPlayer]
	
def getDistanceFactor(iPlayer):
	return dDistanceFactor[iPlayer]
	
def getCompactnessModifier(iPlayer):
	return dCompactnessModifier[iPlayer]
	
def getTargetDistanceValueModifier(iPlayer):
	return dTargetDistanceValueModifier[iPlayer]

def getReligiousTolerance(iPlayer):
	return dReligiousTolerance[iPlayer]
	
def updateParameters(iPlayer):
	pPlayer = player(iPlayer)
	pPlayer.setTargetDistanceValueModifier(getTargetDistanceValueModifier(iPlayer))
	pPlayer.setReligiousTolerance(getReligiousTolerance(iPlayer))
		
@handler("playerCivAssigned")
def onPlayerCivAssigned(iPlayer):
	updateParameters(iPlayer)


# MacAurther: The lower the value, the farther away civ will consider settling cities
dTargetDistanceValueModifier = CivDict({
iWari: 7,
iMississippi: 7,
iNorse: 3,
iInuit: 1,
iInca: 4,
iHaudenosaunee: 8,
iSpain : 0,
iFrance : 0,
iEngland : 0,
iNetherlands : 0,
iLakota: 7,
iHawaii: 8,
iRussia: 3,
iAmerica : 1,
iArgentina: 2,
iMexico : 2,
iColombia : 7,
iPeru : 7,
iBrazil : 1,
iVenezuela : 7,
iCanada : 1,
}, default=10)

# MacAurther: The higher the value, the less like to train persecutors
dReligiousTolerance = CivDict({
iSpain : 1,
iFrance : 2,
iEngland : 2,
iPortugal : 2,
iNetherlands : 4,
iAmerica : 4,
iCanada : 4,
}, default=3)