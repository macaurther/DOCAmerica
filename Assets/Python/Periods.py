from Core import *
from RFCUtils import *
from Locations import *

from Events import events, handler
from DynamicCivs import isCurrentCapital


dEvacuatePeriods = {
	iLakota : iLakotaReservation,
	iCherokee : iCherokeeReservation,
}

dPeriods1500AD = {
}

dPeriods1750AD = {
}
dScenarioPeriods = {
	0: {},
	1500: dPeriods1500AD,
	1750: dPeriods1750AD,
}
dPeriodNames = {
	iPeriodAntebellumUSA: "Antebellum_America",
	iUnifiedUSA: "Unified_America",
	iFederalBrazil: "Federal_Brazil",
	iLakotaReservation: "Sioux_Reservation",
	iCherokeeReservation: "Cherokee_Nation",
	iMayaGuatemala:   "Maya_Guatemala",
	iChimuEcuador:    "Chimu_Ecuador",
	iTiwanakuBolivia: "Tiwanaku_Bolivia",
	iTupiParaguay:    "Tupi_Paraguay",
	iArawakGuyana:    "Arawak_Guyana",
	iIncaChile:       "Inca_Chile",
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
	if civ(iPlayer) == iCSA:	
		setPeriod(iAmerica, iUnifiedUSA)

@handler("resurrection")
def onResurrection(iPlayer):
	dRespawnPeriods = {
		iMaya:     iMayaGuatemala,
		iChimu:    iChimuEcuador,
		iTiwanaku: iTiwanakuBolivia,
		iTupi:     iTupiParaguay,
		iArawak:   iArawakGuyana,
		iInca:     iIncaChile,
	}
	iCivPlayer = civ(iPlayer)
	if iCivPlayer in dRespawnPeriods:
		setPeriod(iCivPlayer, dRespawnPeriods[iCivPlayer])


@handler("cityAcquired")
def onCityAcquired(iOwner, iPlayer, city, bConquest):
	pass

	
@handler("firstCity")
def onCityBuilt(city):
	pass


@handler("vassalState")
def onVassalState(iMaster, iVassal, bVassal, bCapitulated):
	iMasterCiv = civ(iMaster)
	iVassalCiv = civ(iVassal)

	if bVassal:
		if iVassalCiv == iLakota and iMasterCiv in [iAmerica, iCanada, iEngland, iFrance]:
			setPeriod(iLakota, iLakotaReservation)

		if iVassalCiv == iCherokee and iMasterCiv in [iAmerica, iCanada, iEngland, iFrance]:
			setPeriod(iCherokee, iCherokeeReservation)
			

@handler("capitalMoved")
def onCapitalMoved(city):
	iOwner = city.getOwner()
	iOwnerCiv = civ(iOwner)

	if iOwnerCiv == iAmerica:
		# Move to DC gives larger core (but doesn't take away core if CSA is already defeated)
		if (city.getX(), city.getY()) == tDC and game.getPeriod(iOwnerCiv) != iUnifiedUSA:
			setPeriod(iAmerica, iPeriodAntebellumUSA)

	if iOwnerCiv == iBrazil:
		# Move to Brazilia gives larger core
		if (city.getX(), city.getY()) == tBrazilia:
			setPeriod(iBrazil, iFederalBrazil)


@handler("techAcquired")
def onTechAcquired(iTech, iTeam, iPlayer):
	iCiv = civ(iPlayer)
	iEra = infos.tech(iTech).getEra()