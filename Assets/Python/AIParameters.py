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

#MacAurther TODO: All these values \/
dTakenTilesThreshold = {
iCivSpain : 10,
iCivFrance : 10,
iCivEngland : 10,
iCivVirginia: 15,
iCivMassachusetts: 25,
iCivNewHampshire: 25,
iCivMaryland: 20,
iCivConnecticut: 25,
iCivRhodeIsland: 25,
iCivNorthCarolina: 15,
iCivSouthCarolina: 15,
iCivNewYork: 20,
iCivNewJersey: 20,
iCivPennsylvania: 20,
iCivDelaware: 25,
iCivGeorgia: 15,
}

dDistanceSubtrahend = {
iCivSpain : 3,
iCivFrance : 3,
iCivEngland : 3,
iCivVirginia: 4,
iCivMassachusetts: 3,
iCivNewHampshire: 6,
iCivMaryland: 5,
iCivConnecticut: 6,
iCivRhodeIsland: 6,
iCivNorthCarolina: 3,
iCivSouthCarolina: 3,
iCivNewYork: 4,
iCivNewJersey: 5,
iCivPennsylvania: 4,
iCivDelaware: 6,
iCivGeorgia: 4,
}

dDistanceSubtrahendExploration = {
iCivSpain : 4,
iCivFrance : 4,
iCivEngland : 4,
iCivVirginia: 4,
iCivMassachusetts: 4,
iCivNewHampshire: 4,
iCivMaryland: 4,
iCivConnecticut: 4,
iCivRhodeIsland: 4,
iCivNorthCarolina: 4,
iCivSouthCarolina: 4,
iCivNewYork: 4,
iCivNewJersey: 4,
iCivPennsylvania: 4,
iCivDelaware: 4,
iCivGeorgia: 4,
}

dDistanceFactor = {
iCivVirginia: 200,
iCivMassachusetts: 250,
iCivNewHampshire: 400,
iCivMaryland: 350,
iCivConnecticut: 400,
iCivRhodeIsland: 400,
iCivNorthCarolina: 200,
iCivSouthCarolina: 250,
iCivNewYork: 200,
iCivNewJersey: 400,
iCivPennsylvania: 250,
iCivDelaware: 400,
iCivGeorgia: 200,
iCivAmerica : 200,
iCivCanada : 150,
}

dDistanceFactorExploration = {
iCivSpain : 150,
iCivFrance : 150,
iCivEngland : 100,
iCivVirginia: 100,
iCivMassachusetts: 100,
iCivNewHampshire: 100,
iCivMaryland: 100,
iCivConnecticut: 100,
iCivRhodeIsland: 100,
iCivNorthCarolina: 100,
iCivSouthCarolina: 100,
iCivNewYork: 100,
iCivNewJersey: 100,
iCivPennsylvania: 100,
iCivDelaware: 100,
iCivGeorgia: 100,
}

dCompactnessModifier = {
iCivVirginia: 10,
iCivMassachusetts: 30,
iCivNewHampshire: 120,
iCivMaryland: 50,
iCivConnecticut: 120,
iCivRhodeIsland: 120,
iCivNorthCarolina: 10,
iCivSouthCarolina: 10,
iCivNewYork: 20,
iCivNewJersey: 50,
iCivPennsylvania: 20,
iCivDelaware: 120,
iCivGeorgia: 20,
iCivAmerica : 20,
}

dCompactnessModifierExploration = {
iCivSpain : 10,
iCivFrance : 5,
iCivEngland : 5,
iCivVirginia: 10,
iCivMassachusetts: 10,
iCivNewHampshire: 10,
iCivMaryland: 10,
iCivConnecticut: 10,
iCivRhodeIsland: 10,
iCivNorthCarolina: 10,
iCivSouthCarolina: 10,
iCivNewYork: 10,
iCivNewJersey: 10,
iCivPennsylvania: 10,
iCivDelaware: 10,
iCivGeorgia: 10,
}

dTargetDistanceValueModifier = {
iCivSpain : 3,
iCivFrance : 3,
iCivEngland : 3,
iCivVirginia: 1,
iCivMassachusetts: 2,
iCivNewHampshire: 5,
iCivMaryland: 3,
iCivConnecticut: 5,
iCivRhodeIsland: 5,
iCivNorthCarolina: 2,
iCivSouthCarolina: 2,
iCivNewYork: 1,
iCivNewJersey: 3,
iCivPennsylvania: 2,
iCivDelaware: 3,
iCivGeorgia: 2,
iCivAmerica : 3,
}

dReligiousTolerance = {
iCivSpain : 1,
iCivFrance : 2,
iCivEngland : 2,
iCivVirginia: 4,
iCivMassachusetts: 4,
iCivNewHampshire: 4,
iCivMaryland: 4,
iCivConnecticut: 4,
iCivRhodeIsland: 4,
iCivNorthCarolina: 4,
iCivSouthCarolina: 4,
iCivNewYork: 4,
iCivNewJersey: 4,
iCivPennsylvania: 4,
iCivDelaware: 4,
iCivGeorgia: 4,
iCivAmerica : 4,
iCivCanada : 4,
}