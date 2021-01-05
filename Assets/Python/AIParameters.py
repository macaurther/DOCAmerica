from Consts import *
from RFCUtils import utils

def getTakenTilesThreshold(iPlayer):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	return utils.getOrElse(dTakenTilesThreshold, iCiv, 13)
	
def getDistanceSubtrahend(iPlayer):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	return utils.getOrElse(dDistanceSubtrahend, iCiv, 4)
	
def getDistanceFactor(iPlayer):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	return utils.getOrElse(dDistanceFactor, iCiv, 500)
	
def getCompactnessModifier(iPlayer):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	return utils.getOrElse(dCompactnessModifier, iCiv, 40)
	
def getTargetDistanceValueModifier(iPlayer):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	return utils.getOrElse(dTargetDistanceValueModifier, iCiv, 10)

def getReligiousTolerance(iPlayer):
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	return utils.getOrElse(dReligiousTolerance, iCiv, 3)
	
def updateParameters(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	pPlayer.setTakenTilesThreshold(getTakenTilesThreshold(iPlayer))
	pPlayer.setDistanceSubtrahend(getDistanceSubtrahend(iPlayer))
	pPlayer.setDistanceFactor(getDistanceFactor(iPlayer))
	pPlayer.setCompactnessModifier(getCompactnessModifier(iPlayer))
	pPlayer.setTargetDistanceValueModifier(getTargetDistanceValueModifier(iPlayer))
	pPlayer.setReligiousTolerance(getReligiousTolerance(iPlayer))
	
def init():
	for iPlayer in range(iNumTotalPlayersB):
		updateParameters(iPlayer)
		
def onTechAcquired(iPlayer, iTech):
	if iTech == iExploration:
		pPlayer = gc.getPlayer(iPlayer)
		iCiv = pPlayer.getCivilizationType()
		
		if iCiv in dDistanceSubtrahendExploration: pPlayer.setDistanceSubtrahend(dDistanceSubtrahendExploration[iCiv])
		if iCiv in dDistanceFactorExploration: pPlayer.setDistanceFactor(dDistanceFactorExploration[iCiv])
		if iCiv in dCompactnessModifierExploration: pPlayer.setCompactnessModifier(dCompactnessModifierExploration[iCiv])
	
dTakenTilesThreshold = {
}

dDistanceSubtrahend = {
iCivSpain : 3,
iCivFrance : 3,
iCivEngland : 3,
}

dDistanceSubtrahendExploration = {
iCivSpain : 4,
iCivFrance : 4,
iCivEngland : 4,
}

dDistanceFactor = {
iCivAmerica : 200,
iCivCanada : 150,
}

dDistanceFactorExploration = {
iCivSpain : 150,
iCivFrance : 150,
iCivEngland : 100,
}

dCompactnessModifier = {
iCivAmerica : 20,
}

dCompactnessModifierExploration = {
iCivSpain : 10,
iCivFrance : 5,
iCivEngland : 5,
}

dTargetDistanceValueModifier = {
iCivSpain : 3,
iCivFrance : 3,
iCivEngland : 3,
iCivAmerica : 3,
}

dReligiousTolerance = {
iCivSpain : 1,
iCivFrance : 2,
iCivEngland : 2,
iCivAmerica : 4,
iCivCanada : 4,
}