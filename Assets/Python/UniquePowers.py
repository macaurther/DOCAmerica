from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
from StoredData import data # edead
from Consts import *
from RFCUtils import *
from operator import itemgetter
from Events import handler

from Locations import *
from Core import *


@handler("cityAcquired")
# Colombian UP
def colombianPower(iOwner, iPlayer, city, bConquest):
	if civ(iPlayer) == iColombia and bConquest:
		if city in cities.regions(*lLatinAmerica):
			city.setOccupationTimer(0)


@handler("techAcquired")
# Mayan UP
def mayanPower(iTech, iTeam, iPlayer):
	iEra = player(iPlayer).getCurrentEra()
	if civ(iPlayer) == iMaya and iEra < iColonial:
		iNumCities = player(iPlayer).getNumCities()
		if iNumCities > 0:
			iFood = scale(20) / iNumCities
			for city in cities.owner(iPlayer):
				city.changeFood(iFood)
			
			message(iPlayer, 'TXT_KEY_MAYA_UP_EFFECT', infos.tech(iTech).getText(), iFood)

@handler("cityBuilt")
# Puelboan UP
def puebloanPower(city):
	if civ(city.getOwner()) == iPuebloan and city.plot().isHills():
		lFreeBuildings = [iGranary, iMarket, iStoneworks, iWalls]
		for iBuilding in lFreeBuildings:
			if not city.isHasRealBuilding(iBuilding):
				city.setHasRealBuilding(iBuilding, True)
				return

@handler("cityAcquiredAndKept")
# Chimu UP
def chimuPower(iOwner, city):
	print ("City aquired and kept by player " + str(iOwner) + ", or civ " + str(civ(iOwner)))
	if civ(iOwner) == iChimu:
		print ("Chimu will get 1 artist in capital at: x=" + str(player(iOwner).getCapitalCity().getX()) + ", y=" + str(player(iOwner).getCapitalCity().getY()))
		player(iOwner).getCapitalCity().changeFreeSpecialistCount(iSpecialistArtist, 1)


