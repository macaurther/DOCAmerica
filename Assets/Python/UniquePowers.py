from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
from StoredData import data # edead
from Consts import *
from RFCUtils import *
from operator import itemgetter
from Events import handler
import CvScreensInterface

from Locations import *
from Core import *


@handler("cityAcquired")
# Colombian UP
def colombianPower(iOwner, iPlayer, pCity, bConquest):
	if civ(iPlayer) == iColombia and bConquest:
		if pCity in cities.regions(*lLatinAmerica):
			pCity.setOccupationTimer(0)

@handler("cityAcquired")
# Inca UP
def incanPower(iOwner, iPlayer, pCity, bConquest):
	if civ(iPlayer) == iInca and bConquest:
		iNumCities = player(iPlayer).getNumCities()
		if iNumCities > 0:
			iFood = scale(60) / iNumCities
			for pCity in cities.owner(iPlayer):
				pCity.changeFood(iFood)
			
			message(iPlayer, 'TXT_KEY_INCA_UP_EFFECT', pCity.getName(), iFood)

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

@handler("cityHurry")
# Teotihuacan UP
def teotihuacanPowerHurry(pCity, iHurry):
	if iHurry == iHurryPopulation and civ(pCity) == iTeotihuacan:
		doTeotihuacanPower(pCity)

@handler("slaveExpended")
# Teotihuacan UP
def teotihuacanPowerSlave(pCity):
	if civ(pCity) == iTeotihuacan:
		doTeotihuacanPower(pCity)

def doTeotihuacanPower(pCity):
	pCity.changeCulture(pCity.getOwner(), scale(20), False)
	message(pCity.getOwner(), 'TXT_KEY_TEOTIHUACAN_UP_EFFECT', scale(20), pCity.getName(), sound='AS2D_WELOVEKING', event=1, button=infos.building(iAltar).getButton(), color=8, location=(pCity.getX(), pCity.getY()))

@handler("cityBuilt")
# Desert RP
def desertPower(pCity):
	if civ(pCity.getOwner()) in [iPueblo]:
		lFreeBuildings = [iGranary, iMarket, iStoneworks]
		for iBuilding in lFreeBuildings:
			if not pCity.isHasRealBuilding(iBuilding):
				pCity.setHasRealBuilding(iBuilding, True)
				# Make sure Pueblo UP has a chance to proc
				puebloPower(pCity, iBuilding)

# Pueblo UP
@handler("buildingBuilt")
def puebloPowerTrigger(pCity, iBuilding):
	puebloPower(pCity, iBuilding)

def puebloPower(pCity, iBuilding):
	if iBuilding == iStoneworks and civ(pCity.getOwner()) == iPueblo:
		iNumPeakCanyons = plots.city_radius(pCity).where(lambda plot: plot.isPeak() or plot.getFeatureType() == iCanyon).count()
		pCity.setBuildingCommerceChange(infos.building(iStoneworks).getBuildingClassType(), CommerceTypes.COMMERCE_CULTURE, int(iNumPeakCanyons/2))

@handler("cityAcquiredAndKept")
# Chimu UP
def chimuPowerCity(iOwner, pCity):
	if civ(iOwner) == iChimu and pCity.getPreviousCiv() != None and plot(pCity).getBirthProtected() == -1:	# Don't give artist for rise flipped cities
		chimuArtist(iOwner)

@handler("unitPillage")
# Chimu UP
def chimuPowerTribe(pUnit, iImprovement, iRoute, iOwner, iGold):
	if civ(pUnit) == iChimu:
		if iImprovement == iTribe or iImprovement == iContactedTribe:
			chimuArtist(pUnit.getOwner())

def chimuArtist(iPlayer):
	pCapital = player(iPlayer).getCapitalCity()
	pCapital.changeFreeSpecialistCount(iSpecialistArtist, 1)
	strMessage = "An Arist has arrived at your capital to recount your recent conquest"
	# Inform the player that the artist has arrived
	CyInterface().addMessage(iPlayer, False, 20, strMessage, "", 0, infos.unit(iGreatArtist).getButton(), ColorTypes(0), pCapital.getX(), pCapital.getY(), True, True) 

@handler("EndPlayerTurn")
# Muisca Ability
def muiscaAbility(iGameTurn, iPlayer):
	if civ(iPlayer) == iMuisca:
		pPlayer = player(iPlayer)
		iTreasury = pPlayer.getGold()
		lResourceCount = [0, 0, 0]
		for i, iResource in enumerate([iGold, iSilver, iCopper]):
			lResourceCount[i] += player(iPlayer).getNumAvailableBonuses(iResource) - \
						         player(iPlayer).getBonusImport(iResource) + \
						         player(iPlayer).getBonusExport(iResource)
		iExtraGold = int(iTreasury * 0.01 * min(lResourceCount))
		if iExtraGold > 0:
			pPlayer.changeGold(iExtraGold)
			message(iPlayer, "TXT_KEY_MUSICA_POWER", iExtraGold, sound='AS2D_BAGOMONEY')

@handler("buildingBuilt")
# Spanish UB
def missionPower(city, iBuilding):
	if iBuilding == iMission:
		makeUnits(city.getOwner(), iCatholicMiss, city.plot(), 1, UnitAITypes.UNITAI_MISSIONARY).adjective("")

@handler("firstContact")
# Spanish Ability
def conquistadors(iTeamX, iHasMetTeamY):
	if is_minor(iTeamX) or is_minor(iHasMetTeamY):
		return
	
	#if year().between(1490, 1800):
	if year().before(1700) and civ(iTeamX) in lBioNewWorld and civ(iHasMetTeamY) not in lBioNewWorld:	# MacAurther: don't trigger late conquerors
		iNewWorldTeam = iTeamX
		iOldWorldTeam = iHasMetTeamY
		
		iNewWorldCiv = civ(iNewWorldTeam)
		iOldWorldCiv = civ(iOldWorldTeam)
		
		if iOldWorldCiv != iSpain:
			return
		
		bAlreadyContacted = data.dFirstContactConquerors[iNewWorldCiv]
		
		# Can't first contact twice
		if bAlreadyContacted:
			return
		
		# MacAurther: Spain UP: Get free units when discovering Natives
		iTransportShip = iCaravel
		if team(player(iOldWorldCiv)).isHasTech(gc.getUnitInfo(iGalleon).getPrereqAndTech()):
			iTransportShip = iGalleon

		# Grant Extra units based on which civ
		lMercenaries = [iCatholicMiss]
		if iNewWorldCiv in [iTeotihuacan, iTiwanaku, iMississippi, iToltec, iChimu, iArawak, iCherokee, iApache]:
			lMercenaries += [iArquebusier]
		elif iNewWorldCiv in [iMaya, iZapotec, iWari, iMuisca, iPueblo, iPurepecha]:
			lMercenaries += [iTransportShip, iConquistador, iPikeman, iExplorer]
		elif iNewWorldCiv in [iAztec, iInca]:
			lMercenaries += [iTransportShip, iConquistador, iBombard]

		CvScreensInterface.immigrationManager.grantMercenaries(lMercenaries, iOldWorldTeam, iHomelandSouthEurope)	# Holy mole I don't know how to write code

		message(iNewWorldTeam, "TXT_KEY_FIRST_CONTACT_NEWWORLD")
		message(iOldWorldTeam, "TXT_KEY_FIRST_CONTACT_OLDWORLD")

		# Inform the player that the mercenaries have arrived.
		strMessage = "Conquistadors are waiting on the docks of South Europe!"
		CyInterface().addMessage(iOldWorldTeam, False, 20, strMessage, "AS2D_IMMIGRANTEARNED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, "", gc.getInfoTypeForString("COLOR_YELLOW"), -1, -1, False, False) 
		
		data.dFirstContactConquerors[iNewWorldCiv] = True

@handler("goodyReceived")
# Coureur des Bois ability
def coureurDesBoisPower(iPlayer, pPlot, pUnit, iGoodyType):
	if pUnit.getUnitType() == iCoureurDesBois:
		iImmigration = scale(25)
		player(iPlayer).changeImmigration(iImmigration)
		# Inform the player that they received Immigration.
		message(iPlayer, "TXT_KEY_COUREUR_DES_BOIS_POWER", iImmigration)

@handler("goodyReceived")
# French UP
def frenchUP(iPlayer, pPlot, pUnit, iGoodyType):
	if civ(iPlayer) == iFrance:
		iRegion = pPlot.getRegionID()
		pBestCity = None
		iBestDistance = 999
		for pCity in cities.owner(iPlayer):
			if pCity.getRegionID() == iRegion:
				if distance(pCity, pPlot) < iBestDistance:
					pBestCity = pCity
					iBestDistance = distance(pCity, pPlot)
		if pBestCity != None:
			pBestCity.changeExtraTradeRoutes(1)
			message(iPlayer, 'TXT_KEY_UP_FRANCE', sound='AS2D_REVOLTEND', event=1, button=infos.improvement(iTribe).getButton(), color=8, location=(pBestCity.getX(),pBestCity.getY()))


@handler("combatResult")
# Wa'a Kaulua Ability
def waaKauluaAbility(pWinner, pLoser):
	iWinner = pWinner.getOwner()
	
	if pWinner.getUnitType() == iWaaKaulua:
		if pLoser.getUnitType() in range(iCaravel, iBattleship):
			if not pWinner.isFull():
				pCannon = makeUnit(iWinner, unique_unit(iWinner, iCannon), (pWinner.getX(), pWinner.getY()), UnitAITypes.UNITAI_ATTACK)
				pCannon.setTransportUnit(pWinner)

@handler("unitSpreadReligionAttempt")
# Russian UP
def russiaUP(pUnit, iReligion, bSuccess):
	if not bSuccess:
		return
	if pUnit.plot().getImprovementType() != iContactedTribe:
		return
	if iReligion != iOrthodoxy:
		return
	iPlayer = pUnit.getOwner()
	if civ(iPlayer) != iRussia:
		return
	makeUnit(iPlayer, iSlave, (pUnit.getX(), pUnit.getY()), UnitAITypes.UNITAI_WORKER)
	message(iPlayer, 'TXT_KEY_UP_ENSLAVE_WIN', sound='AS2D_UNITGIFTED', event=1, button=infos.unit(iSlave).getButton(), color=8, location=(pUnit.getX(), pUnit.getY()))

# MacAurther: Inuit UP
@handler("cityBuilt")
def inuitUP(pCity):
	iPlayer = pCity.getOwner()
	if player(iPlayer).getCivilizationType() == iInuit:
		for i in range(gc.getNUM_CITY_PLOTS()):
			pPlot = pCity.getCityIndexPlot(i)
			if not pPlot.isWater() and pPlot.getImprovementType() in [-1, iTribe, iContactedTribe] and pPlot.getBonusType(player(iPlayer).getTeam()) in [iFur, iDeer, iBison, iSeal]:
				pPlot.setImprovementType(iCamp)

		# Help AI with defender (the NEED it)
		if not player(iPlayer).isHuman():
			makeUnit(iPlayer, iMilitia, pCity)

@handler("cityBuilt")
# CSA UP
def csaUPCityBuilt(pCity):
	doCSAUP(pCity)

@handler("cityAcquiredAndKept")
# CSA UP
def csaUPCityAcquired(iOwner, pCity):
	doCSAUP(pCity)

def doCSAUP(pCity):
	iPlayer = pCity.getOwner()
	if civ(iPlayer) != iCSA:
		return
	if not player(iPlayer).canUseSlaves():
		return
	if pCity.getFreeSpecialistCount(iSpecialistSlave) < 3:
		pCity.setFreeSpecialistCount(iSpecialistSlave, 3)