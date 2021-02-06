# Rhye's and Fall of Civilization - Religions management

from CvPythonExtensions import *
import CvUtil
import PyHelpers       
import Popup
#import cPickle as pickle     	
from Consts import *
import CvTranslator
from RFCUtils import utils
from StoredData import data #edead

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

# initialise coordinates
# MacAurther TODO: For now, put all old world religion holy cities in Mexico City, but need to find a better solution
tJerusalem = (73, 2)
tJewishTL = (72, 3)
tJewishBR = (74, 1)
tCatholicTL = (72, 3)
tCatholicBR = (74, 1)
tOrthodoxTL = (72, 3)
tOrthodoxBR = (74, 1)
tAnglicanTL = (72, 3)
tAnglicanBR = (74, 1)
tBoston = (143, 61)
tPuritanTL = (142, 62)
tPuritanBR = (143, 60)
tProvidence = (142, 59)
tBaptistTL = (138, 59)
tBaptistBR = (142, 57)
tSavannah = (121, 22)
tMethodistTL = (120, 25)
tMethodistBR = (124, 21)

dCatholicPreference = {
iSpain		: 95,
iFrance		: 75,
iEngland	: 30,
iAmerica	: 20,
}

def getCatholicPreference(iPlayer):
	if iPlayer not in dCatholicPreference:
		return 50
	return dCatholicPreference[iPlayer]

lOrthodoxFounders = ()
lOrthodoxEast = []
lOrthodoxMiddle = []
lOrthodoxWest = [iFrance, iEngland]

class Religions:

#######################################
### Main methods (Event-Triggered) ###
#####################################
		
	def checkTurn(self, iGameTurn):

		self.checkJudaism(iGameTurn)

		self.checkCatholicism(iGameTurn)

		self.checkOrthodoxy(iGameTurn)

		self.checkAnglicanism(iGameTurn)

		self.checkPuritanism(iGameTurn)

		self.spreadJudaismAmerica(iGameTurn)



	def foundReligion(self, tPlot, iReligion):
		if not tPlot: return

		x, y = tPlot
		plot = gc.getMap().plot(x, y)
		if plot.isCity():
			gc.getGame().setHolyCity(iReligion, plot.getPlotCity(), True)
			return True
			
		return False
		
		
	def onReligionFounded(self, iReligion, iFounder):
		#MacAurther TODO: Religion onFound
		if gc.getGame().getGameTurn() == utils.getScenarioStartTurn(): return
	
		if iReligion == iCatholicism:
			utils.setStateReligionBeforeBirth(lCatholicStart, iCatholicism)
			
		elif iReligion == iAnglicanism:
			utils.setStateReligionBeforeBirth(lAnglicanStart, iAnglicanism)
					
	def getReligionCities(self, iReligion): # Unused
		lCities = []
		for iPlayer in range(iNumTotalPlayersB):
			lCities.extend(utils.getCityList(iPlayer))
			
		return [city for city in lCities if city.isHasReligion(iReligion)]

	def selectRandomCityCiv(self, iCiv): # Unused
		if gc.getPlayer(iCiv).isAlive():
			city = utils.getRandomEntry(utils.getCityList(iCiv))
			if city:
				return (city.getX(), city.getY())
		return False
	    

	def selectRandomCityArea(self, tTopLeft, tBottomRight): # Unused
		cityList = []
		for (x, y) in utils.getPlotList(tTopLeft, tBottomRight):
			pPlot = gc.getMap().plot(x, y)
			if pPlot.isCity():
				cityList.append((x, y))
		if cityList:
			return utils.getRandomEntry(cityList)
		return False


	def selectRandomCityAreaCiv(self, tTopLeft, tBottomRight, iCiv = -1): # Unused
		cityList = []
		for (x, y) in utils.getPlotList(tTopLeft, tBottomRight):
			pPlot = gc.getMap().plot( x, y )
			if pPlot.isCity():
				if (iCiv != -1 and pPlot.getPlotCity().getOwner() != iCiv): continue
				cityList.append((x, y))
		if cityList:
			return utils.getRandomEntry(cityList)
		return False



	def selectRandomCityReligion(self, iReligion): # Unused
		if gc.getGame().isReligionFounded(iReligion):
			cityList = []
			for iPlayer in range(iNumPlayers):
				for city in utils.getCityList(iPlayer):
					if city.isHasReligion(iReligion):
						cityList.append(city)
			if cityList:
				iCity = utils.getRandomEntry(cityList)
				return (city.getX(), city.getY())
		return False


	def selectRandomCityReligionCiv(self, iReligion, iCiv = -1): # Unused
		if gc.getGame().isReligionFounded(iReligion):
			cityList = []
			for iPlayer in range(iNumPlayers):
				if iCiv != -1 and iPlayer != iCiv: continue
				for city in utils.getCityList(iPlayer):
					if city.isHasReligion(iReligion):
						cityList.append(city)
			if cityList:
				city = utils.getRandomEntry(cityList)
				return (city.getX(), city.getY())
		return False


	def spreadReligion(self, tCoords, iNum, iMissionary): # Unused
		x, y = tCoords
		if not tCoords or not gc.getMap().plot(x, y).isCity(): return
		city = gc.getMap().plot(x, y).getPlotCity()
		#print city
		#print city.getOwner()
		utils.makeUnit(iMissionary, city.getOwner(), tCoords, iNum)
		
	def getTargetCities(self, lCities, iReligion):
		return [city for city in lCities if not city.isHasReligion(iReligion) and gc.getPlayer(city.getOwner()).getSpreadType(city.plot(), iReligion) > ReligionSpreadTypes.RELIGION_SPREAD_NONE]
		
	def selectHolyCity(self, tTL, tBR, tPreferredCity = None, bAIOnly = True):
		if tPreferredCity:
			x, y = tPreferredCity
			if gc.getMap().plot(x, y).isCity():
				if not bAIOnly or utils.getHumanID() != gc.getMap().plot(x, y).getPlotCity().getOwner():
					return tPreferredCity
		
		lCities = [city for city in utils.getAreaCities(utils.getPlotList(tTL, tBR)) if not bAIOnly or city.getOwner() != utils.getHumanID()]
		
		if lCities:
			city = utils.getRandomEntry(lCities)
			return (city.getX(), city.getY())
			
		return None
		
	def checkLateReligionFounding(self, iReligion, iTech):
		if gc.getReligionInfo(iReligion).getTechPrereq() != iTech:
			return
			
		if gc.getGame().isReligionFounded(iReligion):
			return
		
		iPlayerCount = 0
		iPrereqCount = 0
		for iPlayer in range(iNumPlayers):
			if gc.getPlayer(iPlayer).isAlive():
				iPlayerCount += 1
				if gc.getTeam(gc.getPlayer(iPlayer).getTeam()).isHasTech(iTech):
					iPrereqCount += 1
					
		if 2 * iPrereqCount >= iPlayerCount:
			self.foundReligionInCore(iReligion)
			
	def foundReligionInCore(self, iReligion):
		lCoreCities = [city for city in utils.getAllCities() if city.plot().getSpreadFactor(iReligion) == RegionSpreadTypes.REGION_SPREAD_CORE]
		
		if not lCoreCities: return
		
		city = utils.getRandomEntry(lCoreCities)
		
		self.foundReligion((city.getX(), city.getY()), iReligion)
					
#MacAurther TODO Religion Immigrants
## JUDAISM

	def checkJudaism(self, iGameTurn):
		if gc.getGame().isReligionFounded(iJudaism): return

		if iGameTurn <= getTurnForYear(1605):
			self.foundReligion(self.selectHolyCity(tJewishTL, tJewishBR, tJerusalem, False), iJudaism)
			
	def spreadJudaismAmerica(self, iGameTurn):
		#self.spreadReligionToRegion(iJudaism, [rCanada, rAlaska, rUnitedStates], iGameTurn, 1850, 10, 4)
		pass
		
	def spreadReligionToRegion(self, iReligion, lRegions, iGameTurn, iStartDate, iInterval, iOffset):
		if not gc.getGame().isReligionFounded(iReligion): return
		if iGameTurn < getTurnForYear(iStartDate): return
		
		if iGameTurn % utils.getTurns(iInterval) != iOffset: return
		
		lRegionCities = utils.getRegionCities(lRegions)
		lReligionCities = [city for city in lRegionCities if city.isHasReligion(iReligion)]
		
		if 2 * len(lReligionCities) < len(lRegionCities):
			pSpreadCity = utils.getRandomEntry(self.getTargetCities(lRegionCities, iReligion))
			if pSpreadCity:
				pSpreadCity.spreadReligion(iReligion)
				
		
## CATHOLICISM

	def checkCatholicism(self, iGameTurn):
		if gc.getGame().isReligionFounded(iCatholicism): return

		if iGameTurn <= getTurnForYear(1605):
			self.foundReligion(self.selectHolyCity(tCatholicTL, tCatholicBR, tJerusalem, False), iCatholicism)

## ORTHODOXY

	def checkOrthodoxy(self, iGameTurn):
		if gc.getGame().isReligionFounded(iOrthodoxy): return

		if iGameTurn <= getTurnForYear(1605):
			self.foundReligion(self.selectHolyCity(tOrthodoxTL, tOrthodoxBR, tJerusalem, False), iOrthodoxy)

## ANGLICANISM

	def checkAnglicanism(self, iGameTurn):
		if gc.getGame().isReligionFounded(iAnglicanism): return

		if iGameTurn <= getTurnForYear(1605):
			self.foundReligion(self.selectHolyCity(tAnglicanTL, tAnglicanBR, tJerusalem, False), iAnglicanism)

## PURITANISM

	def checkPuritanism(self, iGameTurn):
		if gc.getGame().isReligionFounded(iPuritanism): return
		
		if iGameTurn <= getTurnForYear(1625):
			self.foundReligion(self.selectHolyCity(tPuritanTL, tPuritanBR, tBoston, False), iPuritanism)
			pMassachusetts.setLastStateReligion(iPuritanism)

## BAPTISM

	def checkBaptism(self, iGameTurn):
		if gc.getGame().isReligionFounded(iBaptism): return
		
		if iGameTurn <= getTurnForYear(1640):
			self.foundReligion(self.selectHolyCity(tBaptistTL, tBaptistBR, tProvidence, False), iBaptism)
			pRhodeIsland.setLastStateReligion(iBaptism)

## METHODISM

	def checkPuritanism(self, iGameTurn):
		if gc.getGame().isReligionFounded(iMethodism): return
		
		if iGameTurn <= getTurnForYear(1735):
			self.foundReligion(self.selectHolyCity(tMethodistTL, tMethodistBR, tSavannah, False), iMethodism)
			pGeorgia.setLastStateReligion(iMethodism)

## CATHOLICISM

	def checkSchism(self, iGameTurn):
		if not gc.getGame().isReligionFounded(iOrthodoxy): return
		if gc.getGame().isReligionFounded(iCatholicism): return
		
		if gc.getGame().countReligionLevels(iOrthodoxy) < 10: return
		
		lStateReligionCities = []
		lNoStateReligionCities = []
		lDifferentStateReligionCities = []
		lMinorCities = []
		
		for iPlayer in range(iNumTotalPlayersB):
			iStateReligion = gc.getPlayer(iPlayer).getStateReligion()
			lCities = [city for city in utils.getCityList(iPlayer) if city.isHasReligion(iOrthodoxy)]
			if iStateReligion == iOrthodoxy: lStateReligionCities.extend(lCities)
			elif gc.getPlayer(iPlayer).isMinorCiv() or gc.getPlayer(iPlayer).isBarbarian(): lMinorCities.extend(lCities)
			elif iStateReligion == -1: lNoStateReligionCities.extend(lCities)
			else: lDifferentStateReligionCities.extend(lCities)
			
		if not lStateReligionCities: return
		if not lNoStateReligionCities and not lMinorCities: return
		
		if len(lStateReligionCities) >= len(lNoStateReligionCities) + len(lMinorCities): return
		
		lOrthodoxCapitals = [city for city in lStateReligionCities if city.isCapital()]
		
		if lOrthodoxCapitals:
			pOrthodoxCapital = utils.getHighestEntry(lOrthodoxCapitals, lambda city: gc.getPlayer(city.getOwner()).getScoreHistory(iGameTurn))
		else:
			pOrthodoxCapital = gc.getGame().getHolyCity(iOrthodoxy)
		
		lCatholicCities = []
		lCatholicCities.extend(lNoStateReligionCities)
		lCatholicCities.extend(lMinorCities)
		pCatholicCapital = utils.getHighestEntry([city for city in lCatholicCities if city.plot().getSpreadFactor(iCatholicism) >= 3 and city != pOrthodoxCapital], lambda city: city.getPopulation())
		
		if not pCatholicCapital:
			pCatholicCapital = utils.getHighestEntry(lCatholicCities, lambda city: city.getPopulation())
		
		self.foundReligion((pCatholicCapital.getX(), pCatholicCapital.getY()), iCatholicism)
		
		lIndependentCities = []
		lIndependentCities.extend(lDifferentStateReligionCities)
		lIndependentCities.extend(lMinorCities)
				
		self.schism(pOrthodoxCapital, pCatholicCapital, lNoStateReligionCities, lIndependentCities)

	def schism(self, pOrthodoxCapital, pCatholicCapital, lReplace, lDistance):
		for city in lDistance:
			if stepDistance(city.getX(), city.getY(), pCatholicCapital.getX(), pCatholicCapital.getY()) <= stepDistance(city.getX(), city.getY(), pOrthodoxCapital.getX(), pOrthodoxCapital.getY()):
				lReplace.append(city)
				
		for city in lReplace:
			city.replaceReligion(iOrthodoxy, iCatholicism)
				
		if gc.getPlayer(utils.getHumanID()).getStateReligion() == iOrthodoxy and gc.getGame().getGameTurn() >= getTurnForYear(tBirth[utils.getHumanID()]):
			utils.popup(CyTranslator().getText("TXT_KEY_SCHISM_TITLE", ()), CyTranslator().getText("TXT_KEY_SCHISM_MESSAGE", (pCatholicCapital.getName(),)), ())
			
		for iPlayer in range(iNumPlayers):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isAlive() and pPlayer.getStateReligion() == iOrthodoxy:
				lConvertedCities = [city for city in lReplace if city.getOwner() == iPlayer]
				if 2 * len(lConvertedCities) >= gc.getPlayer(iPlayer).getNumCities():
					gc.getPlayer(iPlayer).setLastStateReligion(iCatholicism)

#REFORMATION

	def showPopup(self, popupID, title, message, labels):
		popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setHeaderString(title)
		popup.setBodyString(message)
		for i in labels:
		    popup.addButton( i )
		popup.launch(len(labels) == 0)

	def reformationPopup(self):
		self.showPopup(7624, CyTranslator().getText("TXT_KEY_REFORMATION_TITLE", ()), CyTranslator().getText("TXT_KEY_REFORMATION_MESSAGE",()), (CyTranslator().getText("TXT_KEY_REFORMATION_1", ()), CyTranslator().getText("TXT_KEY_REFORMATION_2", ()), CyTranslator().getText("TXT_KEY_REFORMATION_3", ())))

	def eventApply7624(self, popupReturn):
		iHuman = utils.getHumanID()
		if popupReturn.getButtonClicked() == 0:
			self.embraceReformation(iHuman)
		elif popupReturn.getButtonClicked() == 1:
			self.tolerateReformation(iHuman)
		elif popupReturn.getButtonClicked() == 2:
			self.counterReformation(iHuman)

	def onTechAcquired(self, iTech, iPlayer):
		#MacAurther TODO
		#if iTech == iAcademia:
		#	if gc.getPlayer(iPlayer).getStateReligion() == iCatholicism:
		#		if not gc.getGame().isReligionFounded(iProtestantism):
		#			gc.getPlayer(iPlayer).foundReligion(iProtestantism, iProtestantism, True)
		#			self.reformation()
					
		for iReligion in range(iNumReligions):
			self.checkLateReligionFounding(iReligion, iTech)
					
	def onBuildingBuilt(self, city, iPlayer, iBuilding):
		pass
	
	def chooseProtestantism(self, iCiv):
		iRand = gc.getGame().getSorenRandNum(100, 'Protestantism Choice')
		return iRand >= getCatholicPreference(iCiv)
		
	def isProtestantAnyway(self, iCiv):
		iRand = gc.getGame().getSorenRandNum(100, 'Protestantism anyway')
		return iRand >= (getCatholicPreference(iCiv)+50)/2

	def reformation(self):
		#MacAurther TODO
		'''for iPlayer in range(iNumPlayers):
			if [city for city in utils.getCityList(iPlayer) if city.getOwner() == iPlayer]:
				self.reformationChoice(iPlayer)
		
		for iPlayer in range(iNumPlayers):
			if data.players[iPlayer].iReformationDecision == 2:
				for iTargetPlayer in range(iNumPlayers):
					if data.players[iTargetPlayer].iReformationDecision == 0 and utils.getHumanID() != iTargetPlayer and not utils.isAVassal(iTargetPlayer):
						gc.getTeam(iPlayer).declareWar(iTargetPlayer, True, WarPlanTypes.WARPLAN_DOGPILE)
						
		pHolyCity = gc.getGame().getHolyCity(iProtestantism)
		if data.players[pHolyCity.getOwner()].iReformationDecision == 0:
			pHolyCity.setNumRealBuilding(iProtestantShrine, 1)'''
		
	def reformationChoice(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		
		if utils.getHumanID() == iPlayer: return
	
		if pPlayer.getStateReligion() == iCatholicism:
			if self.chooseProtestantism(iPlayer):
				self.embraceReformation(iPlayer)
			elif self.isProtestantAnyway(iPlayer) or utils.isAVassal(iPlayer):
				self.tolerateReformation(iPlayer)
			else:
				self.counterReformation(iPlayer)
		else:
			self.tolerateReformation(iPlayer)
					
	def embraceReformation(self, iCiv):
		pass
		
	def tolerateReformation(self, iCiv):
		pass
					
	def counterReformation(self, iCiv):
		pass
		

	def reformationyes(self, iCiv): # Unused
		pass

	def reformationno(self, iCiv): # Unused
		pass
					
rel = Religions()