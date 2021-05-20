# Rhye's and Fall of Civilization - Sentiments

from CvPythonExtensions import *
import CvUtil
import PyHelpers
#import Popup
#import cPickle as pickle
from Consts import *
from StoredData import data #edead
from RFCUtils import utils
import random

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

class Sentiments:

######################################
### Main methods (Event-Triggered) ###
######################################

	def setup(self):
		# MacAurther TODO
		pass
			

	def infectAllCities(self, iPlayer, iSentiment):
		for iCity in utils.getCityList(iPlayer):
			self.infectCity(iCity, iSentiment)

	def infectCity(self, iCity, iSentiment):
		iCity.setHasRealBuilding(iSentiment, True)
		if gc.getPlayer(iCity.getOwner()).isHuman():
			sTxtKey = ""
			sAS2D = ""
			if iSentiment == iPatriots:
				sTxtKey = "TXT_KEY_PATRIOTS_SPREAD_CITY"
				sAS2D = "AS2D_CITY_REVOLT"
			elif iSentiment == iWarHawks:
				sTxtKey = "TXT_KEY_WAR_HAWKS_SPREAD_CITY"
				sAS2D = "AS2D_BUILD_BARRACKS"
			elif iSentiment == iDepression:
				sTxtKey = "TXT_KEY_DEPRESSION_SPREAD_CITY"
				sAS2D = "AS2D_STRIKE"
			elif iSentiment == iBoom:
				sTxtKey = "TXT_KEY_BOOM_SPREAD_CITY"
				sAS2D = "AS2D_UNITGIFTED"
			CyInterface().addMessage(iCity.getOwner(), True, iDuration/2, CyTranslator().getText(sTxtKey, ()) + " " + iCity.getName() + "!", sAS2D, 0, "", ColorTypes(iBlue), -1, -1, True, True)
		
		if iSentiment in [iDepression]:
			for (x, y) in utils.surroundingPlots((iCity.getX(), iCity.getY()), 2):
				pPlot = gc.getMap().plot( x, y )
				if pPlot.getUpgradeProgress() > 0:
					pPlot.setUpgradeProgress(0)
					iImprovement = pPlot.getImprovementType()
					if iImprovement == iTown:
						pPlot.setImprovementType(iVillage)
	
	def disinfectAllCities(self, iPlayer, iSentiment):
		for iCity in utils.getCityList(iPlayer):
			self.disinfectCity(self, iCity, iSentiment)
	
	def disinfectCity(self, iCity, iSentiment):
		iCity.setHasRealBuilding(iSentiment, False)

sentiments = Sentiments()