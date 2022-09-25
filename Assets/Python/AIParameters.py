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
	pPlayer.setTakenTilesThreshold(getTakenTilesThreshold(iPlayer))
	pPlayer.setDistanceSubtrahend(getDistanceSubtrahend(iPlayer))
	pPlayer.setDistanceFactor(getDistanceFactor(iPlayer))
	pPlayer.setCompactnessModifier(getCompactnessModifier(iPlayer))
	pPlayer.setTargetDistanceValueModifier(getTargetDistanceValueModifier(iPlayer))
	pPlayer.setReligiousTolerance(getReligiousTolerance(iPlayer))
		
@handler("playerCivAssigned")
def onPlayerCivAssigned(iPlayer):
	updateParameters(iPlayer)

@handler("techAcquired")
def onTechAcquired(iTech, iTeam, iPlayer):
	if iTech == iExploration:
		if iPlayer in dDistanceSubtrahendExploration: player(iPlayer).setDistanceSubtrahend(dDistanceSubtrahendExploration[iPlayer])
		if iPlayer in dDistanceFactorExploration: player(iPlayer).setDistanceFactor(dDistanceFactorExploration[iPlayer])
		if iPlayer in dCompactnessModifierExploration: player(iPlayer).setCompactnessModifier(dCompactnessModifierExploration[iPlayer])
	
dTakenTilesThreshold = CivDict({
iMaya : 12,
iPortugal : 15,
iInca : 10,
iNetherlands : 15,
}, default=13)

dDistanceSubtrahend = CivDict({
iMaya : 3,
iSpain : 3,
iFrance : 3,
iEngland : 3,
iInca : 3,
}, default=4)

dDistanceSubtrahendExploration = CivDict({
iSpain : 4,
iFrance : 4,
iEngland : 4,
}, default=4)

dDistanceFactor = CivDict({
iPortugal : 150,
iNetherlands : 150,
iAmerica : 200,
iArgentina : 150,
iBrazil : 150,
iCanada : 150,
}, default=500)

dDistanceFactorExploration = CivDict({
iSpain : 150,
iFrance : 150,
iEngland : 100,
}, default=500)

dCompactnessModifier = CivDict({
iPortugal : 5,
iNetherlands : 5,
iAmerica : 20,
}, default=40)

dCompactnessModifierExploration = CivDict({
iSpain : 10,
iFrance : 5,
iEngland : 5,
}, default=40)

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