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
		if city in cities.regions(*(lCentralAmerica + lSouthAmerica)):
			city.setOccupationTimer(0)


@handler("techAcquired")
def mayanPower(iTech, iTeam, iPlayer):
	iEra = player(iPlayer).getCurrentEra()
	if civ(iPlayer) == iMaya and iEra < iMedieval:
		iNumCities = player(iPlayer).getNumCities()
		if iNumCities > 0:
			iFood = scale(20) / iNumCities
			for city in cities.owner(iPlayer):
				city.changeFood(iFood)
			
			message(iPlayer, 'TXT_KEY_MAYA_UP_EFFECT', infos.tech(iTech).getText(), iFood)


@handler("immigration")
def canadianUP(_, city, iPopulation):
	if civ(city) == iCanada:
		iProgress = 5 * city.getPopulation() * iPopulation
		
		lSpecialists = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman]
		lProgress = [city.getGreatPeopleUnitProgress(unique_unit(city.getOwner(), iSpecialist)) for iSpecialist in lSpecialists]
		bAllZero = all(x <= 0 for x in lProgress)
			
		if bAllZero:
			iGreatPerson = random_entry(lSpecialists)
		else:
			iGreatPerson = lSpecialists[find_max(lProgress).index]
			
		iGreatPerson = unique_unit(city.getOwner(), iGreatPerson)
		
		city.changeGreatPeopleProgress(iProgress)
		city.changeGreatPeopleUnitProgress(iGreatPerson, iProgress)
		
		message(city.getOwner(), 'TXT_KEY_UP_MULTICULTURALISM', city.getName(), infos.unit(iGreatPerson).getText(), iProgress, event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.unit(iGreatPerson).getButton(), color=iGreen, location=city)