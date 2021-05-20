# Rhye's and Fall of Civilization - Revolution management

from CvPythonExtensions import *
import CvUtil
import PyHelpers       
import Popup
#import cPickle as pickle     	
from Consts import *
import CvTranslator
from RFCUtils import utils
from StoredData import data #edead
import Civilizations
import Areas
from Sentiments import sentiments

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

class Revolution:

#######################################
### Main methods (Event-Triggered) ###
#####################################
	
	def setup(self):
		pass
	
	def checkTurn(self, iGameTurn):
		pass
	
	def showPopup(self, popupID, title, message, labels):
		popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setHeaderString(title)
		popup.setBodyString(message)
		for i in labels:
		    popup.addButton( i )
		popup.launch(len(labels) == 0)

	def revolutionPopup(self):
		self.showPopup(7624, CyTranslator().getText("TXT_KEY_REVOLUTION_TITLE", ()), CyTranslator().getText("TXT_KEY_REVOLUTION_MESSAGE",()), (CyTranslator().getText("TXT_KEY_REVOLUTION_1", ()), CyTranslator().getText("TXT_KEY_REVOLUTION_2", ()), CyTranslator().getText("TXT_KEY_REVOLUTION_3", ())))

	# Revolution Event
	def eventApply7624(self, popupReturn):
		iHuman = utils.getHumanID()
		if popupReturn.getButtonClicked() == 0:
			self.chooseRevolution(iHuman)
		elif popupReturn.getButtonClicked() == 1:
			self.chooseLoyalist(iHuman)
	
	# Pre Revolution Event
	def eventApply7626(self, popupReturn):
		iHuman = utils.getHumanID()
		if popupReturn.getButtonClicked() == 0:
			self.chooseConveneCongress(iHuman)
		elif popupReturn.getButtonClicked() == 1:
			self.chooseSuppressRebellion(iHuman)

	def onTechAcquired(self, iTech, iPlayer):
		if iTech == iIndependence and iPlayer in lCivStates:
			print("Independence Researched")
			if data.iRevolutionState == -1:
				data.iRevolutionState = 0
				# Give all other States Independence tech
				for iPlayer in lCivStates:
					print("Giving Civ Independence Tech: ", iPlayer)
					Civilizations.initTech(iPlayer, iIndependence)
				
				self.preRevolution()
	
	def onBuildingBuilt(self, city, iPlayer, iBuilding):
		if iBuilding == iIndependenceHall and iPlayer in lCivStates:
			print("IndependenceHall Constructed")
			if data.iRevolutionState == 0:
				data.iRevolutionState = 1
				self.revolution()
	
	def preRevolution(self):
		print("Starting preRevolution")
		
		for iPlayer in lCivStates:
			self.preRevolutionChoice(iPlayer)
	
	def preRevolutionChoice(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		
		if utils.getHumanID() == iPlayer: return
		
		if iPlayer in lCivStates:
			if self.chooseConveneCongress(iPlayer):
				self.embraceConveneCongress(iPlayer)
			elif self.chooseSuppressRebellion(iPlayer):
				self.embraceSuppressRebellion(iPlayer)
			else:
				self.embraceTolerateDisobedience(iPlayer)
		else:
			self.embraceTolerateDisobedience(iPlayer)
	
	def chooseConveneCongress(self, iPlayer):
		# MacAurther TODO: Fancy self-assesment logic to see if AI wants to be loyalist ONLY if player did not attend Continental Convention
		iRand = gc.getGame().getSorenRandNum(100, 'Convene Congress')
		return data.iPreRevolutionChoice[iPlayer] != 2
	
	def chooseSuppressRebellion(self, iPlayer):
		# MacAurther TODO: Fancy self-assesment logic to see if AI wants to be loyalist ONLY if player did not attend Continental Convention
		iRand = gc.getGame().getSorenRandNum(100, 'Suppress Rebellion')
		return data.iPreRevolutionChoice[iPlayer] == 2
	
	def embraceConveneCongress(self, iPlayer):
		print("Civ chose Convene Congress: ", iPlayer)
		data.iPreRevolutionChoice[iPlayer] = 1
		pPlayer = gc.getPlayer(iPlayer)
		
		#All cities get the Patriots sentiment, allows construction of iIndependenceHall
		sentiments.infectAllCities(iPlayer, iPatriots)
	
	def embraceSuppressRebellion(self, iPlayer):
		print("Civ chose Suppress Rebellion: ", iPlayer)
		data.iPreRevolutionChoice[iPlayer] = 2
		pPlayer = gc.getPlayer(iPlayer)
		
		# Switch legal civic to iMartialLaw
		pPlayer = gc.getPlayer(iPlayer)
		pPlayer.setCivics(iCivicsLegal, iMartialLaw)
		# Receive a Militia in Capital
		tPlot = Areas.getCapital(iPlayer)
		utils.makeUnit(iMilitia, iPlayer, tPlot, 1)
	
	def embraceTolerateDisobedience(self, iPlayer):
		print("Civ chose Tolerate Disobedience: ", iPlayer)
		data.iPreRevolutionChoice[iPlayer] = 3
		pPlayer = gc.getPlayer(iPlayer)
		
		# 2 turns of Unrest in Capital (handled in CIV4EventInfos.xml)
	
	def revolution(self):
		print("Starting Revolution")
		
		for iPlayer in lCivStates:
			self.revolutionChoice(iPlayer)
		
	def revolutionChoice(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		
		if utils.getHumanID() == iPlayer: return
		
		if iPlayer in lCivStates:
			if self.chooseRevolution(iPlayer):
				self.embraceRevolution(iPlayer)
			elif self.chooseRevolution(iPlayer):
				self.embraceLoyalist(iPlayer)
		
	def chooseRevolution(self, iPlayer):
		# MacAurther TODO: Fancy self-assesment logic to see if AI wants to be loyalist ONLY if player did not attend Continental Convention
		iRand = gc.getGame().getSorenRandNum(100, 'Revolution')
		return data.iRevolutionChoice[iPlayer] == 1
		
	def chooseLoyalist(self, iPlayer):
		# MacAurther TODO: Fancy self-assesment logic to see if AI wants to be loyalist ONLY if player did not attend Continental Convention
		iRand = gc.getGame().getSorenRandNum(100, 'Loyalist')
		return data.iRevolutionChoice[iPlayer] == 2
	
	def embraceRevolution(self, iPlayer):
		print("Civ chose Revolution: ", iPlayer)
		data.iRevolutionChoice[iPlayer] = 1
		pPlayer = gc.getPlayer(iPlayer)
		
		#MacAurther TODO: expect Expeditionary forces
		# Become a Commonwealth
		pPlayer.setCivics(iCivicsGovernment, iCommonwealth)
		# Break British vassalage
		gc.getTeam(pPlayer.getTeam()).setVassal(iEngland, False, False)
		# Free Minuteman in every city
		for city in utils.getCityList(iPlayer):
			utils.makeUnit(iMinuteman, iPlayer, (city.getX(), city.getY()), 1)
		
	def embraceLoyalist(self, iPlayer):
		print("Civ chose Loyalist: ", iPlayer)
		data.iRevolutionChoice[iPlayer] = 2
		pPlayer = gc.getPlayer(iPlayer)
		
		# Declare war on all Partiots
		for iTargetPlayer in lCivStates:
			if data.iRevolutionChoice[iTargetPlayer] == 1 and utils.getHumanID() != iTargetPlayer:
				gc.getTeam(iPlayer).declareWar(iTargetPlayer, True, WarPlanTypes.WARPLAN_DOGPILE)
		# Receive 2 Militia and one Heavy Cannon in Capital
		tPlot = Areas.getCapital(iPlayer)
		utils.makeUnit(iMilitia, iPlayer, tPlot, 2)
		utils.makeUnit(iHeavyCannon, iPlayer, tPlot, 1)

rev = Revolution()