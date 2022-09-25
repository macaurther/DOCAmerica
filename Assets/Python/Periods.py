from Core import *
from RFCUtils import *
from Events import events, handler


dEvacuatePeriods = {
}

dPeriods600AD = {
}

dPeriods1700AD = {
}


def setPeriod(iCiv, iPeriod):
	if game.getPeriod(iCiv) == iPeriod:
		return

	game.setPeriod(iCiv, iPeriod)
	
	events.fireEvent("periodChange", iCiv, iPeriod)
	
	iPlayer = slot(iCiv)
	if iPlayer >= 0:
		events.fireEvent("playerPeriodChange", iPlayer, iPeriod)


def evacuate(iPlayer):
	if player(iPlayer).getPeriod() == -1:
		iCiv = civ(iPlayer)
		if iCiv in dEvacuatePeriods:
			setPeriod(iCiv, dEvacuatePeriods[iCiv])
			
			if cities.core(iPlayer).owner(iPlayer) > 0:
				return True
			else:
				setPeriod(iCiv, -1)
	return False


@handler("GameStart")
def setup():
	iScenario = scenario()
	
	if iScenario >= i600AD:
		for iCiv, iPeriod in dPeriods600AD.items():
			setPeriod(iCiv, iPeriod)
	
	if iScenario == i1700AD:
		for iCiv, iPeriod in dPeriods1700AD.items():
			setPeriod(iCiv, iPeriod)


@handler("birth")
def onBirth(iPlayer):
	pass


@handler("collapse")
def onCollapse(iPlayer):
	pass

@handler("resurrection")
def onResurrection(iPlayer):
	pass


@handler("cityAcquired")
def onCityAcquired(iOwner, iPlayer, city, bConquest):
	pass

	
@handler("firstCity")
def onCityBuilt(city):
	pass


@handler("vassalState")
def onVassalState(iMaster, iVassal, bVassal, bCapitulated):
	pass
			

@handler("capitalMoved")
def onCapitalMoved(city):
	pass


@handler("techAcquired")
def onTechAcquired(iTech, iTeam, iPlayer):
	iCiv = civ(iPlayer)
	iEra = infos.tech(iTech).getEra()
	
	if iCiv == iInca:
		if player(iCiv).getPeriod() == -1:
			if iEra == iRenaissance:
				setPeriod(iInca, iPeriodLateInca)