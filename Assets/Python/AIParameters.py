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


# MacAurther TODO:
dTargetDistanceValueModifier = CivDict({
iSpain : 3,
iFrance : 3,
iEngland : 3,
iNetherlands : 3,
iAmerica : 3,
}, default=10)

dReligiousTolerance = CivDict({
iSpain : 1,
iFrance : 2,
iEngland : 2,
iPortugal : 2,
iNetherlands : 4,
iAmerica : 4,
iCanada : 4,
}, default=3)