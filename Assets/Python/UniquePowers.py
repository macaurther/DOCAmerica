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
def colombianPower(iOwner, iPlayer, city, bConquest):
	if civ(iPlayer) == iColombia and bConquest:
		if city in cities.regions(*lLatinAmerica):
			city.setOccupationTimer(0)


@handler("techAcquired")
def mayanPower(iTech, iTeam, iPlayer):
	iEra = player(iPlayer).getCurrentEra()
	if civ(iPlayer) == iMaya and iEra < iColonial:
		iNumCities = player(iPlayer).getNumCities()
		if iNumCities > 0:
			iFood = scale(20) / iNumCities
			for city in cities.owner(iPlayer):
				city.changeFood(iFood)
			
			message(iPlayer, 'TXT_KEY_MAYA_UP_EFFECT', infos.tech(iTech).getText(), iFood)
