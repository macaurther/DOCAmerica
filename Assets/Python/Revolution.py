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

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

class Revolution:

#######################################
### Main methods (Event-Triggered) ###
#####################################
		
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
			self.embraceReformation(iHuman)
		elif popupReturn.getButtonClicked() == 1:
			self.chooseLoyalist(iHuman)
	
	# Pre Revolution Event
	def eventApply7626(self, popupReturn):
		iHuman = utils.getHumanID()
		if popupReturn.getButtonClicked() == 0:
			self.chooseConveneCongress(iHuman)
		elif popupReturn.getButtonClicked() == 1:
			self.chooseSurpressRebellion(iHuman)

	def onTechAcquired(self, iTech, iPlayer):
		if iTech == iIndependence and iPlayer in lCivStates:
			if data.iRevolutionTurn == 0:
				# Give all other States Independence tech
				for iPlayer in lCivStates:
					Civilizations.initTech(iPlayer, iIndependence, False)
				
				self.preRevolution()
	
	def onBuildingBuilt(self, city, iPlayer, iBuilding):
		if iBuilding == iIndependenceHall and iPlayer in lCivStates:
			if data.iRevolutionTurn == 0:
				data.iRevolutionTurn = 1
				self.revolution()
	
	def preRevolution(self):
		#MacAurther TODO
		pass
	
	def revolution(self):
		#MacAurther TODO
		pass
		
	def revolutionChoice(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		
		if utils.getHumanID() == iPlayer: return
		
		# MacAurther TODO: Fancy logic for states to choose Loyalists for more variation?
		if iPlayer in lCivStates:
			self.chooseRevolution(self, iCiv)
		else:
			self.chooseIndependent(self, iCiv)
		
	def chooseRevolution(self, iCiv):
		pass
		
	def chooseLoyalist(self, iCiv):
		pass
	
	def chooseIndependent(self, iCiv):
		pass
	
	def chooseConveneCongress(self, iCiv):
		pass
	
	def chooseSurpressRebellion(self, iCiv):
		pass
		


rev = Revolution()