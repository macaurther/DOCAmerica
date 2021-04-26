# Rhye's and Fall of Civilization - (a part of) Unique Powers

#Egypt in CvPlayer::canDoCivics() and in WBS
#India in CvPlayer::updateMaxAnarchyTurns()
#China (and England before the change) in CvPlayer::getProductionNeeded()
#Babylonia in CvPlayer.cpp::acquireCity()
# Babylonia now in CvPlayer::getCapitalYieldModifier(); +33% production and commerce in the capital after Code of Laws
#Greece CvCity:getGreatPeopleRate()
#Persia (USED TO BE in CvHandicapInfo::getDistanceMaintenancePercentByID(); THEN in RiseAndFall.py, collapseCapitals()), NOW in Stability.py, onCityAcquired()
#Rome in CvPlot::movementCost()
#Japan, Spain and England in CvUnit::init(). Turkey used to be there as well
# Japan now in CvUnit::experienceNeeded(); +50% promotion tempo
# England now in CvHandicapInfo::getDistanceMaintenancePercentByID()
#Ethiopia in Congresses.py (USED TO BE in CvUnit::init() and CvUnit::upgrade())
#Maya in CvHandicapInfo::getResearchPercentByID()
#Byzantium in Stability.checkImplosion()
#Khmer in CvUnit::canMoveInto()
#Germany (USED TO BE IN in CvUnit::init(), CvUnit::upgrade() and CvUnitAI::AI_pillageValue()); NOW IN CvUnit::upgradePrice()
#France in CvPlayerAI::AI_getAttitudeVal() and in Congresses.py
#Netherlands in CvUnit::canEnterTerritory()
#Mali in CvPlot::calculateYield() and Stability.py and CvInfos.cpp (CvHandicapInfo::getResearchPercentByID())
#Portugal in CvUnit::init()
#Inca in CvPlot::calculateNatureYield()
#Mongolia (USED TO BE IN in CvUnit::pillage()); now HERE and in CvRFCEventHandler.py (in OnCityRazed() and BeginPlayerTurn())
#Turkey HERE + in CvPlayer::canRazeCity()
#America HERE + in CvCity::getCulturePercentAnger()

#MacAurther: States:
#Virginia in CvCity:getGreatPeopleRate()
#Massachusetts in CvPlayer::canDoCivics() and in WBS
#New Hampshire in CvCity::getProductionModifier() and CvGameTextMgr::setProductionHelp()
#Rhode Island in CvPlot::calculateNatureYield()
#Maryland in CvPlayer::reset()
#Connecticut in UniquePowers.py getCivicStability()
#New York in CvPlot::calculateImprovementYieldChange()
#Pennsylvania in CvPlayer::reset()

from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
#import cPickle as pickle
from StoredData import data # edead
from Consts import *
from RFCUtils import utils
from operator import itemgetter
import Areas

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

### Constants ###

class UniquePowers:

#######################################
### Main methods (Event-Triggered) ###
#####################################  


	def checkTurn(self, iGameTurn):
		pass
					
	def onChangeWar(self, bWar, iTeam, iOtherTeam):
		pass
			
	def setup(self):
		pass
		
	def onBuildingBuilt(self, city, iOwner, iBuilding):
		pass
	
	def tradingCompanyCulture(self, city, iCiv, iPreviousOwner):
		tCity = (city.getX(), city.getY())
		x, y = tCity
		for (i, j) in utils.surroundingPlots(tCity):
			pPlot = gc.getMap().plot(i, j)
			if (i, j) == tCity:
				utils.convertPlotCulture(pPlot, iCiv, 51, False)
			elif pPlot.isCity():
				pass
			elif utils.calculateDistance(i, j, x ,y) == 1:
				utils.convertPlotCulture(pPlot, iCiv, 65, True)
			else:
				if pPlot.getOwner() == iPreviousOwner:
					utils.convertPlotCulture(pPlot, iCiv, 15, False)