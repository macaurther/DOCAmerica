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
def colombianPower(iOwner, iPlayer, pCity, bConquest):
	if civ(iPlayer) == iColombia and bConquest:
		if pCity in cities.regions(*lLatinAmerica):
			pCity.setOccupationTimer(0)


@handler("techAcquired")
# Mayan UP
def mayanPower(iTech, iTeam, iPlayer):
	if turn() > 0: # MacAurther: don't give food for starting techs
		iEra = player(iPlayer).getCurrentEra()
		if civ(iPlayer) == iMaya and iEra < iColonialEra:
			iNumCities = player(iPlayer).getNumCities()
			if iNumCities > 0:
				iFood = scale(20) / iNumCities
				for pCity in cities.owner(iPlayer):
					pCity.changeFood(iFood)
				
				message(iPlayer, 'TXT_KEY_MAYA_UP_EFFECT', infos.tech(iTech).getText(), iFood)

@handler("cityBuilt")
# Desert RP
def puebloanPower(pCity):
	if civ(pCity.getOwner()) in [iPuebloan]:
		lFreeBuildings = [iGranary, iMarket, iStoneworks]
		for iBuilding in lFreeBuildings:
			if not pCity.isHasRealBuilding(iBuilding):
				pCity.setHasRealBuilding(iBuilding, True)

@handler("cityAcquiredAndKept")
# Chimu UP
def chimuPower(iOwner, pCity):
	if civ(iOwner) == iChimu and pCity.getPreviousCiv() != None and plot(pCity).getBirthProtected() == -1:	# Don't give artist for rise flipped cities
		pCapital = player(iOwner).getCapitalCity()
		pCapital.changeFreeSpecialistCount(iSpecialistArtist, 1)
		strMessage = "An Arist has arrived at your capital to recount your recent conquest"
		# Inform the player that the artist has arrived
		CyInterface().addMessage(iOwner, False, 20, strMessage, "", 0, infos.unit(iGreatArtist).getButton(), ColorTypes(0), pCapital.getX(), pCapital.getY(), True, True) 


@handler("goodyReceived")
# Coureur des Bois ability
def coureurDesBoisPower(iPlayer, pPlot, pUnit, iGoodyType):
	if pUnit.getUnitType() == iCoureurDesBois:
		iImmigration = (3 - gc.getGame().getGameSpeedType()) * 25	# Normal: 25, Epic: 50, Marathon: 75
		player(iPlayer).changeImmigration(iImmigration)
		# Inform the player that they received Immigration.
		message(iPlayer, "TXT_KEY_COUREUR_DES_BOIS_POWER", iImmigration)

@handler("goodyReceived")
# Iroquois UP
def iroquoisPower(iPlayer, pPlot, pUnit, iGoodyType):
	if civ(iPlayer) == iHaudenosaunee:
		if year() > year(1600):
			makeUnits(iPlayer, iArquebusier, pPlot, 1, UnitAITypes.UNITAI_ATTACK)
		else:
			makeUnits(iPlayer, iMohawk, pPlot, 1, UnitAITypes.UNITAI_ATTACK)

@handler("improvementBuilt")
# Russian UP
def onImprovementBuilt(iImprovement, iOldImprovement, iX, iY):	# MacAurther: Added old improvement argument
	if iImprovement > -1 and iOldImprovement == iContactedTribe:
		iPlayer = plot(iX, iY).getOwner()
		if iPlayer > -1 and civ(iPlayer) == iRussia:
			makeUnit(iPlayer, iNativeSlave2, (iX, iY), UnitAITypes.UNITAI_WORKER)
			message(iPlayer, 'TXT_KEY_UP_ENSLAVE_WIN', sound='SND_REVOLTEND', event=1, button=infos.unit(iNativeSlave2).getButton(), color=8, location=(iX, iY))

# MacAurther: Inuit UP
@handler("cityBuilt")
def inuitUP(pCity):
	iPlayer = pCity.getOwner()
	if player(iPlayer).getCivilizationType() == iInuit:
		for i in range(gc.getNUM_CITY_PLOTS()):
			pPlot = pCity.getCityIndexPlot(i)
			if pPlot.getImprovementType() in [-1, iTribe] and pPlot.getBonusType(player(iPlayer).getTeam()) in [iFur, iDeer, iBison]:
				pPlot.setImprovementType(iCamp)