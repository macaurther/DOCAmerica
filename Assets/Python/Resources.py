# Rhye's and Fall of Civilization - Dynamic resources

from CvPythonExtensions import *
import CvUtil
import PyHelpers  
#import Popup
from Consts import *
from RFCUtils import utils # edead
from StoredData import data

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
localText = CyTranslator()

### Constants ###


# initialise bonuses variables

iRoad = 0
#Orka: Silk Road road locations
lSilkRoute = [(85,48), (86,49), (87,48), (88,47), (89,46), (90,47), (90,45), (91,47), (91,45), (92,48), (93,48), (93,46), (94,47), (95,47), (96,47), (97,47), (98,47), (99,46)]
lNewfoundlandCapes = [(34, 52), (34, 53), (34, 54), (35, 52), (36, 52), (35, 55), (35, 56), (35, 57), (36, 51), (36, 58), (36, 59)]

class Resources:

	# Leoreth: bonus removal alerts by edead
	def createResource(self, iX, iY, iBonus, createTextKey="TXT_KEY_MISC_DISCOVERED_NEW_RESOURCE", removeTextKey="TXT_KEY_MISC_EVENT_RESOURCE_EXHAUSTED"):
		"""Creates a bonus resource and alerts the plot owner"""
		
		iRemovedBonus = gc.getMap().plot(iX,iY).getBonusType(-1) # for alert
		
		if iRemovedBonus == iBonus:
			return
		
		gc.getMap().plot(iX, iY).setBonusType(iBonus)
				
		if iBonus == -1:
			iImprovement = gc.getMap().plot(iX, iY).getImprovementType()
			if iImprovement >= 0:
				if gc.getImprovementInfo(iImprovement).isImprovementBonusTrade(iRemovedBonus):
					gc.getMap().plot(iX, iY).setImprovementType(-1)
			
		iOwner = gc.getMap().plot(iX,iY).getOwner()
		if iOwner >= 0: # only show alert to the tile owner
			bWater = gc.getMap().plot(iX, iY).isWater()
			city = gc.getMap().findCity(iX, iY, iOwner, TeamTypes.NO_TEAM, not bWater, bWater, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
			
			if iRemovedBonus >= 0:
				self.notifyResource(iOwner, city, iX, iY, iRemovedBonus, removeTextKey)
			
			if iBonus >= 0:
				self.notifyResource(iOwner, city, iX, iY, iBonus, createTextKey)
					
	def notifyResource(self, iPlayer, city, iX, iY, iBonus, textKey):
		if city.isNone(): return
		
		if gc.getBonusInfo(iBonus).getTechReveal() == -1 or gc.getTeam(gc.getPlayer(iPlayer).getTeam()).isHasTech(gc.getBonusInfo(iBonus).getTechReveal()):
			text = localText.getText(textKey, (gc.getBonusInfo(iBonus).getTextKey(), city.getName()))
			CyInterface().addMessage(iPlayer, False, iDuration, text, "AS2D_DISCOVERBONUS", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getBonusInfo(iBonus).getButton(), ColorTypes(iWhite), iX, iY, True, True)

	def removeResource(self, iX, iY):
		"""Removes a bonus resource and alerts the plot owner"""
		if gc.getMap().plot(iX, iY).getBonusType(-1) == -1: return
		self.createResource(iX, iY, -1)
       	
	def checkTurn(self, iGameTurn):
		
		#MacAurther TODO: All dynamic resources
		# Gujarati horses appear later so Harappa cannot benefit too early
		if iGameTurn == getTurnForYear(-1000):
			self.createResource(88, 37, iHorse)