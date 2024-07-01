from Core import *
from RFCUtils import *
from Locations import *
from Events import events, handler


dEvacuatePeriods = {
}

dPeriods1500AD = {
}

dPeriods1750AD = {
}
dScenarioPeriods = {
	-500: {},
	1500: dPeriods1500AD,
	1750: dPeriods1750AD,
}
dPeriodNames = {
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