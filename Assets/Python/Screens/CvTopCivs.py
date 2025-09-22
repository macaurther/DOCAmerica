## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
# Author - Jon Shafer
# Top Civilizations screen

import PyHelpers
import CvUtil
import CvScreenEnums
import random
from Core import *

NUM_CIVILIZATIONS = 8
# MacAurther TODO: Make mod-specific historians :/
HISTORIANS = {
	iNorse: {
		iExplorationEra: (
			"TXT_KEY_HISTORIAN_AGGESEN",
			"TXT_KEY_HISTORIAN_THORGILSSON",
			"TXT_KEY_HISTORIAN_SAXO_GRAMMATICUS",
			"TXT_KEY_HISTORIAN_SNORRI_STURLUSON",
		),
		iColonialEra: (
			"TXT_KEY_HISTORIAN_HOLBERG",
			"TXT_KEY_HISTORIAN_HUITFELDT",
		),
		iIndustrialEra: (
			"TXT_KEY_HISTORIAN_MUNCH",
		),
	},
	iSpain: {
		iExplorationEra: (
			"TXT_KEY_HISTORIAN_ISIDORE",
		),
		iColonialEra: (
			"TXT_KEY_HISTORIAN_DANGHIERA",
			"TXT_KEY_HISTORIAN_DE_MORGA",
			"TXT_KEY_HISTORIAN_DE_LAS_CASAS",
		),
	},
	iFrance: {
		iExplorationEra: (
			"TXT_KEY_HISTORIAN_GREGORY_OF_TOURS",
			"TXT_KEY_HISTORIAN_EINHARD",
			"TXT_KEY_HISTORIAN_FROISSART",
		),
		iIndustrialEra: (
			"TXT_KEY_HISTORIAN_RAMBAUD",
			"TXT_KEY_HISTORIAN_MICHELET",
			"TXT_KEY_HISTORIAN_BLOCH",
		),
		iModernEra: (
			"TXT_KEY_HISTORIAN_BRAUDEL",
			"TXT_KEY_HISTORIAN_DUBY",
			"TXT_KEY_HISTORIAN_LE_GOFF",
		),
	},
	iEngland: {
		iExplorationEra: (
			"TXT_KEY_HISTORIAN_BEDE",
			"TXT_KEY_HISTORIAN_ASSER",
			"TXT_KEY_HISTORIAN_AETHELWEARD",
			"TXT_KEY_HISTORIAN_GEOFFREY_OF_MONMOUTH",
		),
		iColonialEra: (
			"TXT_KEY_HISTORIAN_HOLINSHED",
			"TXT_KEY_HISTORIAN_HUME",
		),
		iIndustrialEra: (
			"TXT_KEY_HISTORIAN_GIBBON",
			"TXT_KEY_HISTORIAN_LORD_MACAULAY",
			"TXT_KEY_HISTORIAN_CARLYLE",
		),
		iModernEra: (
			"TXT_KEY_HISTORIAN_TOYNBEE",
			"TXT_KEY_HISTORIAN_HOBSBAWM",
		),
	},
	iRussia: {
		iExplorationEra: (
			"TXT_KEY_HISTORIAN_NIKITIN",
		),
		iColonialEra: (
			"TXT_KEY_HISTORIAN_KARAMZIN",
			"TXT_KEY_HISTORIAN_MULLER",
			"TXT_KEY_HISTORIAN_TATISHCHEV",
		),
		iIndustrialEra: (
			"TXT_KEY_HISTORIAN_SOLOVYOV",
			"TXT_KEY_HISTORIAN_KLYUCHEVSKY",
			"TXT_KEY_HISTORIAN_POKROVSKY",
		),
		iModernEra: (
			"TXT_KEY_HISTORIAN_VOLGIN",
		),
	},
	iPortugal: {
		iColonialEra: (
			"TXT_KEY_HISTORIAN_DE_BARROS",
		),
		iIndustrialEra: (
			"TXT_KEY_HISTORIAN_HERCULANO",
		),
	},
	iInca: {
		iColonialEra: (
			"TXT_KEY_HISTORIAN_DE_LA_VEGA",
		),
		iModernEra: (
			"TXT_KEY_HISTORIAN_BASADRE",
		),
	},
	iNetherlands: {
		iIndustrialEra: (
			"TXT_KEY_HISTORIAN_DE_JONGE",
			"TXT_KEY_HISTORIAN_FRUIN",
		),
	},
	iAmerica: {
		iColonialEra: (
			"TXT_KEY_HISTORIAN_MATHER",
		),
		iIndustrialEra: (
			"TXT_KEY_HISTORIAN_ADAMS",
			"TXT_KEY_HISTORIAN_BEARD",
		),
		iModernEra: (
			"TXT_KEY_HISTORIAN_SCHLESINGER",
		),
	},
	iArgentina: {
		iIndustrialEra: (
			"TXT_KEY_HISTORIAN_MITRE",
			"TXT_KEY_HISTORIAN_LOPEZ",
		),
		iModernEra: (
			"TXT_KEY_HISTORIAN_LUNA",
		),
	},
	iColombia: {
		iIndustrialEra: (
			"TXT_KEY_HISTORIAN_RESTREPO_VELEZ",
		),
		iModernEra: (
			"TXT_KEY_HISTORIAN_FRIEDE",
		),
	},
	iBrazil: {
		iIndustrialEra: (
			"TXT_KEY_HISTORIAN_DE_VARNHAGEN",
			"TXT_KEY_HISTORIAN_ROMERO",
			"TXT_KEY_HISTORIAN_DE_ABREU",
		),
		iModernEra: (
			"TXT_KEY_HISTORIAN_FREYRE",
			"TXT_KEY_HISTORIAN_DE_HOLANDA",
			"TXT_KEY_HISTORIAN_PRADO_JUNIOR",
		),
	},
	iCanada: {
		iIndustrialEra: (
			"TXT_KEY_HISTORIAN_GARNEAU",
			"TXT_KEY_HISTORIAN_GROULX",
		),
	},
}

class CvTopCivs:
	"The Greatest Civilizations screen"
	
	def __init__(self):
		
		self.X_SCREEN = 0#205
		self.Y_SCREEN = 0#27
		self.W_SCREEN = 1024#426
		self.H_SCREEN = 768#470

		self.X_MAIN_PANEL = 250
		self.Y_MAIN_PANEL = 70
		self.W_MAIN_PANEL = 550
		self.H_MAIN_PANEL = 500
		
		self.iMarginSpace = 15
		
		self.X_HEADER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
		self.Y_HEADER_PANEL = self.Y_MAIN_PANEL + self.iMarginSpace
		self.W_HEADER_PANEL = self.W_MAIN_PANEL - (self.iMarginSpace * 2)
		self.H_HEADER_PANEL = self.H_MAIN_PANEL - (self.iMarginSpace * 2)
		
#		iWHeaderPanelRemainingAfterLeader = self.W_HEADER_PANEL - self.W_LEADER_ICON + (self.iMarginSpace * 3)
#		iXHeaderPanelRemainingAfterLeader = self.X_LEADER_ICON + self.W_LEADER_ICON + self.iMarginSpace
		self.X_LEADER_TITLE_TEXT = 500#iXHeaderPanelRemainingAfterLeader + (iWHeaderPanelRemainingAfterLeader / 2)
		self.Y_LEADER_TITLE_TEXT = self.Y_HEADER_PANEL + self.iMarginSpace
		self.W_LEADER_TITLE_TEXT = self.W_HEADER_PANEL / 3
		self.H_LEADER_TITLE_TEXT = self.H_HEADER_PANEL / 3
		
		self.X_TEXT_PANEL = self.X_HEADER_PANEL + self.iMarginSpace
		self.Y_TEXT_PANEL = self.Y_HEADER_PANEL + 132
		self.W_TEXT_PANEL = self.W_HEADER_PANEL - (self.iMarginSpace * 2)
		self.H_TEXT_PANEL = 265#self.H_MAIN_PANEL - self.H_HEADER_PANEL - (self.iMarginSpace * 3) + 10 #10 is the fudge factor
		self.iTEXT_PANEL_MARGIN = 35
		
		self.X_RANK_TEXT = 430
		self.Y_RANK_TEXT = 230
		self.W_RANK_TEXT = 300
		self.H_RANK_TEXT = 30
		
		self.X_EXIT = 460
		self.Y_EXIT = self.Y_MAIN_PANEL + 440
		self.W_EXIT = 120
		self.H_EXIT = 30

	def showScreen(self):
			  
		'Use a popup to display the opening text'
		if ( CyGame().isPitbossHost() ):
			return

		# Text
		self.TITLE_TEXT = u"<font=3>" + text("TXT_KEY_TOPCIVS_TITLE").upper() + u"</font>"
		self.EXIT_TEXT = text("TXT_KEY_PEDIA_SCREEN_EXIT").upper()
					
		self.RankList = [
			text("TXT_KEY_TOPCIVS_RANK1"),
			text("TXT_KEY_TOPCIVS_RANK2"),
			text("TXT_KEY_TOPCIVS_RANK3"),
			text("TXT_KEY_TOPCIVS_RANK4"),
			text("TXT_KEY_TOPCIVS_RANK5"),
			text("TXT_KEY_TOPCIVS_RANK6"),
			text("TXT_KEY_TOPCIVS_RANK7"),
			text("TXT_KEY_TOPCIVS_RANK8")
		]

		self.TypeList = [
			"TXT_KEY_TOPCIVS_WEALTH",
			"TXT_KEY_TOPCIVS_POWER",
			"TXT_KEY_TOPCIVS_TECH",
			"TXT_KEY_TOPCIVS_CULTURE",
			"TXT_KEY_TOPCIVS_SIZE",
			"TXT_KEY_TOPCIVS_POPULATION",
		]

		# Randomly choose what category will be used
		szTypeRand = random.choice(self.TypeList)
		
		# Create screen
		
		self.screen = CyGInterfaceScreen( "CvTopCivs", CvScreenEnums.TOP_CIVS )

		self.screen.setSound("AS2D_TOP_CIVS")
		self.screen.showScreen(PopupStates.POPUPSTATE_QUEUED, False)
		self.screen.showWindowBackground( False )
		self.screen.setDimensions(self.screen.centerX(self.X_SCREEN), self.screen.centerY(self.Y_SCREEN), self.W_SCREEN, self.H_SCREEN)
		
		# Create panels
		
		# Main
		szMainPanel = "TopCivsMainPanel"
		self.screen.addPanel( szMainPanel, "", "", true, true,
			self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_MAIN )
		
		# Top
		szHeaderPanel = "TopCivsHeaderPanel"
		szHeaderText = ""#gc.getLeaderHeadInfo(self.player.getLeaderType()).getDescription() + "\n-" + self.player.getCivilizationDescription(0) + "-"
		self.screen.addPanel( szHeaderPanel, szHeaderText, "", true, true,
			self.X_HEADER_PANEL, self.Y_HEADER_PANEL, self.W_HEADER_PANEL, self.H_HEADER_PANEL, PanelStyles.PANEL_STYLE_DAWNBOTTOM )
		
		# Bottom
		szTextPanel = "TopCivsTextPanel"
		szHeaderText = ""#self.Text_Title
		self.screen.addPanel( szTextPanel, szHeaderText, "", true, true,
			self.X_TEXT_PANEL, self.Y_TEXT_PANEL, self.W_TEXT_PANEL, self.H_TEXT_PANEL, PanelStyles.PANEL_STYLE_DAWNTOP )
		
		self.screen.setButtonGFC("Exit", self.EXIT_TEXT, "", self.X_EXIT,self.Y_EXIT, self.W_EXIT, self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		
		# Title Text
		self.X_TITLE_TEXT = self.X_HEADER_PANEL + (self.W_HEADER_PANEL / 2)
		self.Y_TITLE_TEXT = self.Y_HEADER_PANEL + 15
		self.screen.setLabel("DawnTitle", "Background", self.TITLE_TEXT, CvUtil.FONT_CENTER_JUSTIFY,
				self.X_TITLE_TEXT, self.Y_TITLE_TEXT, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		self.populateList(szTypeRand)
		
		szHistorianKey = self.getHistorian()
		szHistorian = text(szHistorianKey)
		szType = text(szTypeRand)
		
		# 1 Text
		self.X_INFO_TEXT = self.X_TITLE_TEXT - 260#self.X_HEADER_PANEL + (self.W_HEADER_PANEL / 2)
		self.Y_INFO_TEXT = self.Y_TITLE_TEXT + 50
		self.W_INFO_TEXT = self.W_HEADER_PANEL
		self.H_INFO_TEXT = 70
		szText = text("TXT_KEY_TOPCIVS_TEXT1", szHistorian) + u"\n" + text("TXT_KEY_TOPCIVS_TEXT2", szType)
		self.screen.addMultilineText( "InfoText1", szText, self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
		
		self.printList()
		
	def populateList(self, szType):
		
		print "populateList for %s" % szType

		# Determine the list of top civs
		
		typeFunction = None
		
		if szType == "TXT_KEY_TOPCIVS_WEALTH":
			typeFunction = CyPlayer.getGold
		elif szType == "TXT_KEY_TOPCIVS_POWER":
			typeFunction = CyPlayer.getPower
		elif szType == "TXT_KEY_TOPCIVS_TECH":
			typeFunction = lambda p: team(p).getTotalTechValue()
		elif szType == "TXT_KEY_TOPCIVS_CULTURE":
			typeFunction = CyPlayer.countTotalCulture
		elif szType == "TXT_KEY_TOPCIVS_SIZE":
			typeFunction = CyPlayer.getTotalLand
		elif szType == "TXT_KEY_TOPCIVS_POPULATION":
			typeFunction = CyPlayer.getTotalPopulation
			
		self.topPlayers = players.major().existing().sort(lambda p: typeFunction(player(p)), reverse=True)
		
	def printList(self):
		for iRank, iPlayer in enumerate(self.topPlayers.limit(8)):
			if iPlayer == active() or team().isHasMet(player(iPlayer).getTeam()):
				szCivText = fullname(iPlayer)
			else:
				szCivText = text("TXT_KEY_TOPCIVS_UNKNOWN")
			
			szWidgetName = "Text" + str(iRank)
			szWidgetDesc = "%d) %s" % (iRank + 1, szCivText)
			
			iXLoc = self.X_RANK_TEXT
			iYLoc = self.Y_RANK_TEXT + iRank * self.H_RANK_TEXT
			
			self.screen.addMultilineText(szWidgetName, unicode(szWidgetDesc), iXLoc, iYLoc, self.W_RANK_TEXT, self.H_RANK_TEXT, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
	
	def getHistorian(self):
		iHistorianPlayer = self.topPlayers.where(lambda p: team().isHasMet(player(p).getTeam())).limit(4).where(lambda p: civ(p) in HISTORIANS).random(otherwise=active())
		
		tHistorianNames = self.getHistorianNames(iHistorianPlayer)
		if not tHistorianNames:
			return "TXT_KEY_HISTORIAN_GENERIC"
		
		return random_entry(tHistorianNames)
	
	def getHistorianNames(self, iPlayer):
		iCiv = civ(iPlayer)
		iCurrentEra = player(iPlayer).getCurrentEra()
		
		if iCiv not in HISTORIANS:
			return tuple()
		
		for iEra in reversed(range(iCurrentEra+1)):
			if iEra in HISTORIANS[iCiv]:
				return HISTORIANS[iCiv][iEra]
		
		for iEra in range(iCurrentEra+1, iNumEras):
			if iEra in HISTORIANS[iCiv]:
				return HISTORIANS[iCiv][iEra]
		
		return tuple()
		
				
	def turnChecker(self, iTurnNum):

		# Check to see if this is a turn when the screen should pop up (every 50 turns)
		if (not CyGame().isNetworkMultiPlayer() and CyGame().getActivePlayer()>=0):
			if (iTurnNum % 50 == 0 and iTurnNum > 0 and gc.getPlayer(CyGame().getActivePlayer()).isAlive()):
				self.showScreen()

	#####################################################################################################################################
	      
	def handleInput( self, inputClass ):
		self.screen = CyGInterfaceScreen( "CvTopCivs", CvScreenEnums.TOP_CIVS )		

		if ( inputClass.getFunctionName() == "Exit" and inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.screen.hideScreen()
			return 1
		elif ( inputClass.getData() == int(InputTypes.KB_RETURN) ):
			self.screen.hideScreen()
			return 1
		return 0

	def update(self, fDelta):
		return
