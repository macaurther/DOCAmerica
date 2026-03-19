#
# Mercenaries Mod
# By: The Lopez
# CvImmigrationManager
# 

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import time
import PyHelpers
import Popup as PyPopup
import ImmigrationUtils
#import CvConfigParser #Rhye
import math
from CvImmigrationScreensEnums import *
from Consts import *
from Core import *
from Civics import *
import BugUtil

from Events import handler

PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()
objImmigrationUtils = ImmigrationUtils.ImmigrationUtils()

# Set to true to print out debug messages in the logs
g_bDebug = false

# Default valus is 1 
g_bAIThinkPeriod = 1 #Rhye (5 in Warlords, 4 in vanilla)

def getHoverText(eWidgetType, iData1, iData2, bOption):
	if objImmigrationUtils.canEarnImmigrants(gc.getActivePlayer(), data.iCurrentImmigrationManagerTab):
		fThreshold = float(objImmigrationUtils.getImmigrationThreshold(gc.getActivePlayer(), data.iCurrentImmigrationManagerTab))
		fRate = float(gc.getActivePlayer().getCommerceRate(CommerceTypes.COMMERCE_IMMIGRATION))
		fFirst = float(gc.getActivePlayer().getImmigration())
		szText = BugUtil.getText("TXT_KEY_MISC_IMMIGRATION", (int(fFirst), int(fThreshold)))
		if (fRate > 0):
			iTurns = math.ceil((fThreshold - fFirst) / fRate)
			if iTurns < 0: iTurns = 0
			szText += u"\n%d%c%s " % (int(fRate), gc.getCommerceInfo(CommerceTypes.COMMERCE_IMMIGRATION).getChar(), BugUtil.getPlainText("TXT_KEY_PER_TURN"))
			szText += BugUtil.getText("INTERFACE_CITY_TURNS", (int(iTurns),))
	else:
		szText = "Cannot earn immigrants here"
	
	return szText

class CvImmigrationManager:
	"Immigration Manager"
	
	def __init__(self, iScreenId):
	
		self.screenFunction = None
		self.bSmallScreen = False
		
		# The different UI wiget names
		self.IMMIGRATION_MANAGER_SCREEN_NAME = "ImmigrationManager"

		self.TAB_NORTH_EUROPE_ID = "NorthEuropeTabWidget"
		self.TAB_SOUTH_EUROPE_ID = "SouthEuropeTabWidget"
		self.TAB_AFRICA_ID = "AfricaTabWidget"
		self.TAB_SIBERIA_ID = "SiberiaTabWidget"
		self.TAB_ASIA_ID = "AsiaTabWidget"

		self.WIDGET_ID = "ImmigrationManagerWidget"
		self.Z_BACKGROUND = -2.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.EventKeyDown=6
						
		self.iScreenId = iScreenId
		
		# When populated this dictionary will contain the information needed to build
		# the widgets for the current screen resolution.		
		self.screenWidgetData = {}
	
		self.nWidgetCount = 0
		self.iActivePlayer = -1
		
		self.currentScreen = IMMIGRATION_MANAGER

		self.bScreenDataCalculated = False
		
	# Returns the instance of the immigration manager screen.						
	def getScreen(self):
		return CyGInterfaceScreen(self.IMMIGRATION_MANAGER_SCREEN_NAME, self.iScreenId)

	# Gets the instance of the immigration manager screen and hides it.
	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()

	# Returns true if the screen is active, false otherwise.	
	def isActive(self):
		return self.getScreen().isActive()

					
	# Screen construction function
	def interfaceScreen(self):
							
		# Create a new screen
		screen = self.getScreen()
				
		if screen.isActive():
			return
			
		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.nWidgetCount = 0
	
		screen = self.getScreen()

		# Calculate all of the screen position data if necessary
		if not self.bScreenDataCalculated:
			self.calculateScreenWidgetData(screen)
		
		if(self.currentScreen == IMMIGRATION_MANAGER):
			self.drawMercenaryScreenContent(screen)

	def computerGetNumImmigrantsToTransport(self, iPlayer, iHomeland):
		return objImmigrationUtils.computerGetNumImmigrantsToTransport(iPlayer, iHomeland)
		
	# Populates the panel that shows all of the available immigrants
	def populateAvailableColonistsPanel(self, screen):
		# Get the available Colonists
		dColonists = objImmigrationUtils.getAvailableImmigrants(self.iActivePlayer, data.iCurrentImmigrationManagerTab)
		
		# Refresh panel
		self.refreshAvailableColonistsInnerPanel(screen)
		self.populateAvailablePanel(screen, AVAILABLE_COLONISTS_INNER_PANEL_ID, dColonists, "AvailableColonists")

	def refreshAvailableColonistsInnerPanel(self, screen):
		screen.deleteWidget(AVAILABLE_COLONISTS_INNER_PANEL_ID)
		screen.addPanel(AVAILABLE_COLONISTS_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_X], self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_Y], self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)

	# Populates the panel that shows all of the available Mercenaries
	def populateAvailableMercenariesPanel(self, screen):

		# Get the available Mercenaries
		dMercenaries = objImmigrationUtils.getAvailableMercenaries(self.iActivePlayer, data.iCurrentImmigrationManagerTab)
		
		# Refresh panel
		self.refreshAvailableMercenariesInnerPanel(screen)
		self.populateAvailablePanel(screen, AVAILABLE_MERCENARIES_INNER_PANEL_ID, dMercenaries, "AvailableMercenaries")
	
	def refreshAvailableMercenariesInnerPanel(self, screen):
		screen.deleteWidget(AVAILABLE_MERCENARIES_INNER_PANEL_ID)
		screen.addPanel(AVAILABLE_MERCENARIES_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_X], self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_Y], self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)

	
	# Populates the panel that shows all of the earned immigrants
	def populateEarnedImmigrantsPanel(self, screen):
		# Get the earned immigrants
		dEarnedImmigrantGroups = objImmigrationUtils.getEarnedImmigrants(civ(self.iActivePlayer), data.iCurrentImmigrationManagerTab)
		
		# Refresh panel
		self.refreshEarnedImmigrantsInnerPanel(screen)
		self.populateAvailablePanel(screen, EARNED_IMMIGRANTS_INNER_PANEL_ID, dEarnedImmigrantGroups, "EarnedImmigrants")
	
	def refreshEarnedImmigrantsInnerPanel(self, screen):
		screen.deleteWidget(EARNED_IMMIGRANTS_INNER_PANEL_ID)
		screen.addPanel(EARNED_IMMIGRANTS_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[EARNED_IMMIGRANTS_INNER_PANEL_X], self.screenWidgetData[EARNED_IMMIGRANTS_INNER_PANEL_Y], self.screenWidgetData[EARNED_IMMIGRANTS_INNER_PANEL_WIDTH], self.screenWidgetData[EARNED_IMMIGRANTS_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)

	# Helper function that populates a panel (Colonist, Expeditionary, or Endowment)
	def populateAvailablePanel(self, screen, innerPanelId, dImmigrantGroups, panel):
		mercenaryCount = 0
		
		# Go through the mercenaries and populate the available mercenaries panel
		for sUnit in dImmigrantGroups.keys():
			unit = dImmigrantGroups[sUnit].getImmigrant()
			unitTitle = dImmigrantGroups[sUnit].getImmigrantTitle()
			panelName = unit.sUnitName + panel
			
			# Create Immigrant Panel
			screen.attachPanel(innerPanelId, panelName, "", "", False, False, PanelStyles.PANEL_STYLE_DAWN)
			screen.attachImageButton( panelName, unit.getUnitInfo().getType()+"-"+panelName+"-InfoButton", 
										unit.getUnitInfo().getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
			screen.attachPanel(panelName, panelName+"Text", unitTitle, "", True, False, PanelStyles.PANEL_STYLE_EMPTY)

			self.populateImmigrantXPString(unit, screen, panelName)
			if not panel == "EarnedImmigrants":
				self.populateImmigrantHireString(unit, self.iActivePlayer, screen, panelName)
				self.populateImmigrantHireButton(unit, screen, panelName)
			else:
				self.populateImmigrantLoadButton(unit, screen, panelName)

			mercenaryCount = mercenaryCount + 1
			

		# Add the padding to the available mercenaries panel to improve the look of the screen
		if((4-mercenaryCount)>0):

			for i in range(4-mercenaryCount):
				screen.attachPanel(innerPanelId, "dummyPanelHire"+str(i), "", "", True, False, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachLabel( "dummyPanelHire"+str(i), "", "     ")
				screen.attachLabel( "dummyPanelHire"+str(i), "", "     ")
				screen.attachLabel( "dummyPanelHire"+str(i), "", "     ")


	def populateImmigrantXPString(self, unit, screen, panelName):
		screen.attachLabel( panelName + "Text", panelName  + "text3", "     Level: " + str(unit.getLevel()))

	def populateImmigrantHireString(self, unit, iPlayer, screen, panelName):
		# Build the unit hire cost string
		strHCost = unit.getHireCostString(iPlayer)	
		screen.attachLabel( panelName + "Text", panelName  + "text4", "     Hire Cost: " + strHCost)

	def populateImmigrantHireButton(self, unit, screen, panelName):
		# Add the hire button for the unit
		if(unit.canAfford(self.iActivePlayer, data.iCurrentImmigrationManagerTab)):
			screen.attachPanel(panelName, panelName+"hireButtonPanel", "", "", False, True, PanelStyles.PANEL_STYLE_EMPTY)
			screen.attachImageButton( panelName, unit.getUnitInfo().getType()+"-"+panelName+"-HireButton", 
										"Art/Interface/Buttons/Actions/Join.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, False )

	def populateImmigrantLoadButton(self, unit, screen, panelName):
		# Ships don't load
		if unit.isShip():
			return
		
		# Ensure that player still has units left to load
		if not objImmigrationUtils.getHasEarnedImmigrant(civ(self.iActivePlayer), data.iCurrentImmigrationManagerTab, unit.getUnitId()):
			return

		# Ensure there's a ship to load onto
		if(not unit.hasShipForPlacement(self.iActivePlayer, data.iCurrentImmigrationManagerTab)):
			return

		# Add the load button for the unit
		screen.attachPanel(panelName, panelName+"hireButtonPanel", "", "", False, True, PanelStyles.PANEL_STYLE_EMPTY)
		screen.attachImageButton( panelName, unit.getUnitInfo().getType()+"-"+panelName+"-LoadButton", 
									"Art/Interface/Buttons/Actions/Load.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, False )


	# Clears out the mercenary information panel contents
	def clearMercenaryInformation(self, screen):
		screen.deleteWidget(IMMIGRANT_INFORMATION_PROMOTION_PANEL_ID)
		screen.deleteWidget(IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_ID)
		screen.deleteWidget(IMMIGRANT_INFORMATION_DETAILS_PANEL_ID)
		screen.deleteWidget(IMMIGRANT_INFORMATION_STRATEGY_PANEL_ID)
		screen.deleteWidget(IMMIGRANT_INFORMATION_INNER_STRATEGY_PANEL_ID)
		screen.deleteWidget(IMMIGRANT_UNIT_GRAPHIC)		
		
			
	# Populates the unit information panel with the unit information details		
	def populateMercenaryInformation(self, screen, unit):
		# Get the ID for the current active player
		iPlayer = gc.getGame().getActivePlayer()

		screen.addPanel(IMMIGRANT_INFORMATION_PROMOTION_PANEL_ID, "", "", True, True, self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_X], self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_Y], self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_WIDTH], self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		
		screen.addPanel(IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_ID, "Promotions", "", True, True, self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_X], self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_Y], self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_WIDTH], self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_EMPTY)
		screen.attachListBoxGFC(IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_ID, IMMIGRANT_INFORMATION_PROMOTION_LIST_ID, "", TableStyles.TABLE_STYLE_EMPTY )
		screen.enableSelect(IMMIGRANT_INFORMATION_PROMOTION_LIST_ID, False)
		
		screen.addPanel(IMMIGRANT_INFORMATION_DETAILS_PANEL_ID, "", "", True, False, self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_X], self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_Y], self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_WIDTH], self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_EMPTY)
		screen.attachListBoxGFC(IMMIGRANT_INFORMATION_DETAILS_PANEL_ID, IMMIGRANT_INFORMATION_DETAILS_LIST_ID, "", TableStyles.TABLE_STYLE_EMPTY )
		screen.enableSelect(IMMIGRANT_INFORMATION_DETAILS_LIST_ID, False)
		
		screen.addPanel(IMMIGRANT_INFORMATION_STRATEGY_PANEL_ID, "", "", True, True, self.screenWidgetData[IMMIGRANT_INFORMATION_STRATEGY_PANEL_X], self.screenWidgetData[IMMIGRANT_INFORMATION_STRATEGY_PANEL_Y], self.screenWidgetData[IMMIGRANT_INFORMATION_STRATEGY_PANEL_WIDTH], self.screenWidgetData[IMMIGRANT_INFORMATION_STRATEGY_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		
		screen.addPanel(IMMIGRANT_INFORMATION_INNER_STRATEGY_PANEL_ID, "Details", "", True, False, self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_STRATEGY_PANEL_X], self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_STRATEGY_PANEL_Y], self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_STRATEGY_PANEL_WIDTH], self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_STRATEGY_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_EMPTY)
		screen.attachListBoxGFC(IMMIGRANT_INFORMATION_INNER_STRATEGY_PANEL_ID, IMMIGRANT_INFORMATION_STRATEGY_LIST_ID, "", TableStyles.TABLE_STYLE_EMPTY )
		screen.enableSelect(IMMIGRANT_INFORMATION_STRATEGY_LIST_ID, False)

		# Build the unit hire cost string
		strHCost = unit.getHireCostString(iPlayer)
		
		# Build the unit XP string
		strXP = u"%d/%d" %(unit.getExperienceLevel(), unit.getNextExperienceLevel())

		# Build the unit stats string
		strStats = u"%d%c    %d%c" %(unit.getUnitInfo().getCombat(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR), unit.getUnitInfo().getMoves(),CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
		if unit.getUnitInfo().getAirCombat() > 0 and unit.getUnitInfo().getAirRange() > 0:
			strStats += u"    %d%c" % (unit.getUnitInfo().getAirCombat(), CyGame().getSymbolID(FontSymbols.RANGED_STRENGTH_CHAR))
			strStats += u"    %d%c" % (unit.getUnitInfo().getAirRange(), CyGame().getSymbolID(FontSymbols.RANGE_CHAR))

		screen.appendListBoxString(IMMIGRANT_INFORMATION_DETAILS_LIST_ID, unit.getName(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString(IMMIGRANT_INFORMATION_DETAILS_LIST_ID, "  Level: " + str(unit.getLevel()) + "     XP: " + strXP, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString(IMMIGRANT_INFORMATION_DETAILS_LIST_ID, "  " + strStats, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString(IMMIGRANT_INFORMATION_DETAILS_LIST_ID, "  ", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString(IMMIGRANT_INFORMATION_DETAILS_LIST_ID, "  Hire Cost: " + strHCost, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		
		szText = CyGameTextMgr().getUnitHelp(unit.getUnitId(), True, False, False, None)[1:]
		screen.appendListBoxString(IMMIGRANT_INFORMATION_STRATEGY_LIST_ID, szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString(IMMIGRANT_INFORMATION_STRATEGY_LIST_ID, "  " + unit.getUnitInfo().getStrategy(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Get the promotion list for the unit
		lPromotionList = unit.getCurrentPromotionList()

		screen.attachMultiListControlGFC(IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_ID, IMMIGRANT_INFORMATION_PROMOTION_LIST_CONTROL_ID, "", 1, 64, 64, TableStyles.TABLE_STYLE_STANDARD)

		# Add all of the promotions the unit has.
		for promotion in lPromotionList:
			screen.appendMultiListButton(IMMIGRANT_INFORMATION_PROMOTION_LIST_CONTROL_ID, gc.getPromotionInfo(promotion).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, promotion, -1, False)

		screen.addUnitGraphicGFC(IMMIGRANT_UNIT_GRAPHIC, unit.getUnitId(), self.screenWidgetData[IMMIGRANT_ANIMATION_X], self.screenWidgetData[IMMIGRANT_ANIMATION_Y], self.screenWidgetData[IMMIGRANT_ANIMATION_WIDTH], self.screenWidgetData[IMMIGRANT_ANIMATION_HEIGHT], WidgetTypes.WIDGET_GENERAL, -1, -1, self.screenWidgetData[IMMIGRANT_ANIMATION_ROTATION_X], self.screenWidgetData[IMMIGRANT_ANIMATION_ROTATION_Z], self.screenWidgetData[IMMIGRANT_ANIMATION_SCALE], True)

		# Add additional hire button (so 720 p screens can see if :P)
		if self.bSmallScreen:
			self.populateImmigrantHireButton(unit, screen, "ImmigrantInformationDetailsPanel")
			self.populateImmigrantLoadButton(unit, screen, "ImmigrantInformationDetailsPanel")

	
	# Draws the gold information in the "Immigration Manager" screens
	def drawGoldInformation(self, screen):
	
		iCost = 0
		strCost = ""		
		
		# Get the players current gold text		
		szText = self.getGoldText(gc.getGame().getActivePlayer())
		screen.setLabel( "GoldText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 12, 4, -1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.show( "GoldText" )
		screen.moveToFront( "GoldText" )
		
		szText = self.getImmigrationText(gc.getGame().getActivePlayer())
		screen.setLabel( "ImmigrationText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 12, 20, -1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.show( "ImmigrationText" )
		screen.moveToFront( "ImmigrationText" )

		screen.setLabel( "MaintainText", "Background", strCost, CvUtil.FONT_LEFT_JUSTIFY, 12, 24, -1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.show( "MaintainText" )
		screen.moveToFront( "MaintainText" )
		

	# Draws the top bar of the "Immigration Manager" screens
	def drawScreenTop(self, screen):
		screen.setDimensions(0, 0, self.screenWidgetData[SCREEN_WIDTH], self.screenWidgetData[SCREEN_HEIGHT])
		screen.addDrawControl(BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.screenWidgetData[SCREEN_WIDTH], self.screenWidgetData[SCREEN_HEIGHT], WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC(BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.screenWidgetData[SCREEN_WIDTH], self.screenWidgetData[SCREEN_HEIGHT], WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.addPanel(SCREEN_TITLE_PANEL_ID, u"", u"", True, False, self.screenWidgetData[SCREEN_TITLE_PANEL_X], self.screenWidgetData[SCREEN_TITLE_PANEL_Y], self.screenWidgetData[SCREEN_TITLE_PANEL_WIDTH], self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_TOPBAR )
		screen.setText(SCREEN_TITLE_TEXT_PANEL_ID, "Background", self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_X], self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Draw the gold information for the screen
		self.drawGoldInformation(screen)


	# Draws the bottom bar of the "Immigration Manager" screens
	def drawScreenBottom(self, screen):
		screen.addPanel(BOTTOM_PANEL_ID, "", "", True, True, self.screenWidgetData[BOTTOM_PANEL_X], self.screenWidgetData[BOTTOM_PANEL_Y], self.screenWidgetData[BOTTOM_PANEL_WIDTH], self.screenWidgetData[BOTTOM_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_BOTTOMBAR )
		self.drawTabs()
		screen.setText(EXIT_TEXT_PANEL_ID, "Background", self.screenWidgetData[EXIT_TEXT_PANEL], CvUtil.FONT_RIGHT_JUSTIFY, self.screenWidgetData[EXIT_TEXT_PANEL_X], self.screenWidgetData[EXIT_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

	# Draws the mercenary screen content
	def drawMercenaryScreenContent(self, screen):
		# If initial tab isn't set, set it
		if data.iCurrentImmigrationManagerTab == -1:
			data.iCurrentImmigrationManagerTab = objImmigrationUtils.getFirstOpenHomeland(self.iActivePlayer)

		# Draw the top bar
		self.drawScreenTop(screen)
 
		# Draw the bottom bar
		self.drawScreenBottom(screen)

		screen.addPanel(IMMIGRATION_PROGRESS_PANEL_ID, "", "", True, True, self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_X], self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_Y], self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_WIDTH], self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(IMMIGRATION_PROGRESS_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[IMMIGRATION_PROGRESS_INNER_PANEL_X], self.screenWidgetData[IMMIGRATION_PROGRESS_INNER_PANEL_Y], self.screenWidgetData[IMMIGRATION_PROGRESS_INNER_PANEL_WIDTH], self.screenWidgetData[IMMIGRATION_PROGRESS_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)
		screen.addPanel(IMMIGRATION_PROGRESS_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(IMMIGRATION_PROGRESS_TEXT_PANEL_ID, "Background", self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_PANEL_X], self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.addPanel(AVAILABLE_COLONISTS_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_X], self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_Y], self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(AVAILABLE_COLONISTS_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_X], self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_Y], self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)
		screen.addPanel(AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(AVAILABLE_COLONISTS_TEXT_PANEL_ID, "Background", self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_PANEL_X], self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addPanel(AVAILABLE_MERCENARIES_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X], self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_Y], self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(AVAILABLE_MERCENARIES_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_X], self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_Y], self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)
		screen.addPanel(AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(AVAILABLE_MERCENARIES_TEXT_PANEL_ID, "Background", self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL_X], self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.addPanel(EARNED_IMMIGRANTS_PANEL_ID, "", "", True, True, self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_X], self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_Y], self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_WIDTH], self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(EARNED_IMMIGRANTS_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[EARNED_IMMIGRANTS_INNER_PANEL_X], self.screenWidgetData[EARNED_IMMIGRANTS_INNER_PANEL_Y], self.screenWidgetData[EARNED_IMMIGRANTS_INNER_PANEL_WIDTH], self.screenWidgetData[EARNED_IMMIGRANTS_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)
		screen.addPanel(EARNED_IMMIGRANTS_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[EARNED_IMMIGRANTS_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[EARNED_IMMIGRANTS_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[EARNED_IMMIGRANTS_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[EARNED_IMMIGRANTS_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(EARNED_IMMIGRANTS_TEXT_PANEL_ID, "Background", self.screenWidgetData[EARNED_IMMIGRANTS_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[EARNED_IMMIGRANTS_TEXT_PANEL_X], self.screenWidgetData[EARNED_IMMIGRANTS_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addPanel(IMMIGRANT_INFORMATION_PANEL_ID, "", "", True, True, self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_X], self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_Y], self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_WIDTH], self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(IMMIGRANT_INFORMATION_TEXT_PANEL_ID, "Background", self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_PANEL_X], self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				
		screen.showWindowBackground(False)

		# Populate the available panels
		self.updateImmigrationBar(screen)
		self.populateAvailableColonistsPanel(screen)
		self.populateAvailableMercenariesPanel(screen)
		self.populateEarnedImmigrantsPanel(screen)
	
	def drawTabs(self):
		xLink = self.screenWidgetData[MARGIN]
		xLink = self.drawTab(IMMIGRATION_MANAGER_TAB_NORTH_EUROPE, self.TAB_NORTH_EUROPE_ID, "TXT_KEY_IMMIGRATION_MANAGER_NORTH_EUROPE", xLink)
		xLink = self.drawTab(IMMIGRATION_MANAGER_TAB_SOUTH_EUROPE, self.TAB_SOUTH_EUROPE_ID, "TXT_KEY_IMMIGRATION_MANAGER_SOUTH_EUROPE", xLink)
		xLink = self.drawTab(IMMIGRATION_MANAGER_TAB_AFRICA, self.TAB_AFRICA_ID, "TXT_KEY_IMMIGRATION_MANAGER_AFRICA", xLink)
		xLink = self.drawTab(IMMIGRATION_MANAGER_TAB_SIBERIA, self.TAB_SIBERIA_ID, "TXT_KEY_IMMIGRATION_MANAGER_SIBERIA", xLink)
		xLink = self.drawTab(IMMIGRATION_MANAGER_TAB_ASIA, self.TAB_ASIA_ID, "TXT_KEY_IMMIGRATION_MANAGER_ASIA", xLink)

	def drawTab(self, eTab, tabID, sTabText, xLink):
		if (data.iCurrentImmigrationManagerTab == eTab):
			szText = u"<font=4>" + localText.getColorText(sTabText, (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>"
		else:
			szText = u"<font=4>" + localText.getText(sTabText, ()).upper() + "</font>"
		self.getScreen().setText(tabID, "", szText, CvUtil.FONT_LEFT_JUSTIFY, xLink, self.screenWidgetData[SCREEN_HEIGHT] - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		return xLink + CyInterface().determineWidth(szText) + self.screenWidgetData[SPACING]

	def updateImmigrationBar(self, screen):
		screen.addStackedBarGFC( IMMIGRATION_PROGRESS_BAR, self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_X], self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_Y], self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_WIDTH], self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_HEIGHT], InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_IMMIGRATION_PROGRESS_BAR, -1, -1 )
		screen.setStackedBarColors( IMMIGRATION_PROGRESS_BAR, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_IMMIGRATION_STORED") )
		screen.setStackedBarColors( IMMIGRATION_PROGRESS_BAR, InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_IMMIGRATION_RATE") )
		screen.setStackedBarColors( IMMIGRATION_PROGRESS_BAR, InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( IMMIGRATION_PROGRESS_BAR, InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		
		if objImmigrationUtils.canEarnImmigrants(gc.getActivePlayer(), data.iCurrentImmigrationManagerTab):
			fThreshold = float(objImmigrationUtils.getImmigrationThreshold(gc.getActivePlayer(), data.iCurrentImmigrationManagerTab))
			fRate = float(gc.getActivePlayer().getCommerceRate(CommerceTypes.COMMERCE_IMMIGRATION))
			fFirst = float(gc.getActivePlayer().getImmigration())
			szText = u""
			if fRate > 0: 
				iTurns = math.ceil((fThreshold - fFirst) / fRate)
				if iTurns < 0: iTurns = 0
				szText = u"%c in %d Turns" %(CyTranslator().getText("[ICON_IMMIGRANT]", ()), iTurns)
			else:
				szText = u"%c in - Turns" %(CyTranslator().getText("[ICON_IMMIGRANT]", ()))

			szText = u"<font=20>%s</font>" % (szText)
			screen.setLabel("ImmigrationProgressBarText", "", szText, CvUtil.FONT_CENTER_JUSTIFY | CvUtil.FONT_CENTER_VERTICALLY, self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_TEXT_X], self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_TEXT_Y], 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_IMMIGRATION_PROGRESS_BAR, -1, -1)

			fFirstPercent = fFirst / fThreshold
			screen.setBarPercentage( IMMIGRATION_PROGRESS_BAR, InfoBarTypes.INFOBAR_STORED, fFirstPercent )
			if ( fFirstPercent == 1 ):
				screen.setBarPercentage( IMMIGRATION_PROGRESS_BAR, InfoBarTypes.INFOBAR_RATE, fRate / fThreshold )
			else:
				screen.setBarPercentage( IMMIGRATION_PROGRESS_BAR, InfoBarTypes.INFOBAR_RATE, fRate / fThreshold / ( 1 - fFirstPercent ) )

			screen.show( IMMIGRATION_PROGRESS_BAR )

		#screen.setText( "ImmigrationProgressBarText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_TEXT_X], self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_TEXT_Y], -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_IMMIGRATION_PROGRESS_BAR, -1, -1 )
		#screen.show( "ImmigrationProgressBarText" )

	# Returns the new version of the gold text that takes into account the
	# mercenary maintenance cost and contract income
	def getGoldText(self, iPlayer):

		# Get the player
		player = gc.getPlayer(iPlayer)
	
		# get the number of cities the player owns
		numCities = player.getNumCities()	
					
		totalUnitCost = player.calculateUnitCost()
		totalUnitSupply = player.calculateUnitSupply()
		totalMaintenance = player.getTotalMaintenance()
		totalCivicUpkeep = player.getCivicUpkeep([], False)
		totalPreInflatedCosts = player.calculatePreInflatedCosts()
		totalInflatedCosts = player.calculateInflatedCosts()
		goldCommerce = player.getCommerceRate(CommerceTypes.COMMERCE_GOLD)
		gold = player.getGold()

		goldFromCivs = player.getGoldPerTurn()

		iIncome = 0
		
		iExpenses = 0

		iIncome = goldCommerce
		
		if( goldFromCivs > 0):
			iIncome += goldFromCivs
		
		iInflation = totalInflatedCosts - totalPreInflatedCosts

		iExpenses = totalUnitCost + totalUnitSupply + totalMaintenance + totalCivicUpkeep + iInflation

		if (goldFromCivs < 0):
			iExpenses -= goldFromCivs
			
		iDelta = iIncome - iExpenses
		
		# Build the gold string
		strGoldText = u"%c: %d" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar(), gold)

		strDelta = ""
		
		# Set the color for the gold/turn.
		if(iDelta > 0):                
			strDelta = u"%s" %(localText.changeTextColor(" (+"+str(iDelta)+"/Turn)",gc.getInfoTypeForString("COLOR_GREEN")))
		elif(gold - iDelta < 0):
			strDelta = u"%s" %(localText.changeTextColor(" ("+str(iDelta)+"/Turn)",gc.getInfoTypeForString("COLOR_RED")))
		elif(iDelta < 0):
			strDelta = u"%s" %(localText.changeTextColor(" ("+str(iDelta)+"/Turn)",gc.getInfoTypeForString("COLOR_YELLOW")))
		
		return strGoldText + strDelta
	
	# Returns the new version of the gold text that takes into account the
	# mercenary maintenance cost and contract income
	def getImmigrationText(self, iPlayer):

		# Get the player
		player = gc.getPlayer(iPlayer)
	
		immigrationCommerce = player.getCommerceRate(CommerceTypes.COMMERCE_IMMIGRATION)
		immigration = player.getImmigration()
		
		# Build the gold string
		strGoldText = u"%c: %d" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_IMMIGRATION).getChar(), immigration)

		strDelta = ""
		
		# Set the color for the gold/turn.
		if(immigrationCommerce > 0):   
			strDelta = u"%s" %(localText.changeTextColor(" (+"+str(immigrationCommerce)+"/Turn)",gc.getInfoTypeForString("COLOR_GREEN")))
		else:
			strDelta = u"%s" %(localText.changeTextColor(" (+"+str(immigrationCommerce)+"/Turn)",gc.getInfoTypeForString("COLOR_GREEN")))
		
		return strGoldText + strDelta
	
	# Hire list of mercenaries
	def grantMercenaries(self, lMercenaries, iPlayer, iHomeland=-1, bImmediate=False):
		if iHomeland == -1:
			iHomeland = objImmigrationUtils.getFirstOpenHomeland(iPlayer)
		for iUnit in lMercenaries:
			self.hireMercenary(iUnit, iPlayer, iHomeland, False, bImmediate)

	# Useful method for use outside of Immigration Manager land as well
	def hireMercenary(self, iUnit, iPlayer, iHomeland, bPay = True, bImmediate=False):
		objImmigrationUtils.hireMercenary(iUnit, iPlayer, iHomeland, bPay, bImmediate)

	# Hires a mercenary for a player
	def hireMercenaryOnScreen(self, screen, iUnit, iHomeland):

		# Get the active player ID
		iPlayer = gc.getGame().getActivePlayer()

		# Hire the mercenary for the player
		self.hireMercenary(iUnit, iPlayer, iHomeland)

		# Draw the gold information for the screen
		self.drawGoldInformation(screen)

		# Update the available mercenaries in the available mercenaries panel
		self.populateAvailableColonistsPanel(screen)
		self.populateAvailableMercenariesPanel(screen)
		self.populateEarnedImmigrantsPanel(screen)

		# Clear the information in the mercenary information panel
		#self.clearMercenaryInformation(screen)
	
	# Places an immigrant onto game map
	def placeMercenary(self, screen, iUnit, iHomeland):
		# Get the active player ID
		iPlayer = gc.getGame().getActivePlayer()

		# Hire the mercenary for the player
		objImmigrationUtils.placeMercenary(iUnit, iPlayer, iHomeland)

		# Update the available mercenaries in the available mercenaries panel
		self.populateAvailableColonistsPanel(screen)
		self.populateAvailableMercenariesPanel(screen)
		self.populateEarnedImmigrantsPanel(screen)

				
	# Updates the available mercenaries panel, displays the hire button to the 
	# player only for the mercenaries they can hire.
	def updateAvailableColonists(self, screen):

		# Get the available Colonists
		dColonists = objImmigrationUtils.getAvailableImmigrants(self.iActivePlayer, data.iCurrentImmigrationManagerTab)

		self.updateAvailableUnits(screen, dColonists, "AvailableColonists")
		
	# Updates the available mercenaries panel, displays the hire button to the 
	# player only for the mercenaries they can hire.
	def updateAvailableMercenaries(self, screen):

		# Get the available Mercenaries
		dMercenaries = objImmigrationUtils.getAvailableMercenaries(self.iActivePlayer, data.iCurrentImmigrationManagerTab)

		self.updateAvailableUnits(screen, dMercenaries, "AvailableMercenaries")
	
	
	# Updates the available mercenaries panel, displays the hire button to the 
	# player only for the mercenaries they can hire.
	def updateEarnedImmigrants(self, screen):

		# Get the earned immigrants
		dEarnedImmigrantGroups = objImmigrationUtils.getEarnedImmigrants(civ(self.iActivePlayer), data.iCurrentImmigrationManagerTab)

		self.updateAvailableUnits(screen, dEarnedImmigrantGroups, "EarnedImmigrants")
	
	
	def updateAvailableUnits(self, screen, dImmigrantGroups, panel):
		# Go through the mercenaries and populate the available mercenaries panel
		for sUnit in dImmigrantGroups.keys():
			unit = dImmigrantGroups[sUnit].getImmigrant()
			unitTitle = dImmigrantGroups[sUnit].getImmigrantTitle()
			panelName = unit.sUnitName + panel
			print("Updating panelName: " + panelName)
			
			# Delete the cost string for the current unit we are processing.
			screen.deleteWidget(panelName + "Text")
			
			screen.attachPanel(panelName, panelName+"Text", unitTitle, "", True, False, PanelStyles.PANEL_STYLE_EMPTY)

			# Delete the hire button for the current unit we are processing.
			screen.deleteWidget(unit.getUnitInfo().getType()+"-"+panelName+"-HireButton")
			screen.deleteWidget(unit.getUnitInfo().getType()+"-"+panelName+"-LoadButton")

			self.populateImmigrantXPString(unit, screen, panelName)
			if not panel == "EarnedImmigrants":
				self.populateImmigrantHireString(unit, self.iActivePlayer, screen, panelName)
				self.populateImmigrantHireButton(unit, screen, panelName)
			else:
				self.populateImmigrantLoadButton(unit, screen, panelName)
	
	# Handles the input to the immigration manager screens
	def handleInput (self, inputClass):

		# Get the instance of the screen
		screen = self.getScreen()

		# Calculate all of the screen position data if necessary
		if not self.bScreenDataCalculated:
			self.calculateScreenWidgetData(screen)

		# Debug code - start
		if g_bDebug:
			screen.setText( "TopPanelDebugMsg", "TopPanel", inputClass.getFunctionName()
						, CvUtil.FONT_RIGHT_JUSTIFY, 1010, 20, -10, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		# Debug code - end
		
		# Get the data
		theKey = int(inputClass.getData())

		# If the escape key was pressed then set the current screen to immigration manager
		if (inputClass.getNotifyCode() == self.EventKeyDown and theKey == int(InputTypes.KB_ESCAPE)):
			self.currentScreen = IMMIGRATION_MANAGER

		# If the exit text was pressed then set the current screen to immigration manager.
		if(inputClass.getFunctionName() == EXIT_TEXT_PANEL_ID):
			self.currentScreen = IMMIGRATION_MANAGER
		
		# If the mercenaries text was pressed and we aren't currently looking at 
		# the main mercenaries manager screen then set the current screen to 
		# mercenaries manager, hide the screen and redraw the screen.
		if(inputClass.getFunctionName() == IMMIGRATION_TEXT_PANEL_ID and self.currentScreen != IMMIGRATION_MANAGER):
			self.currentScreen = IMMIGRATION_MANAGER
			self.hideScreen()
			self.interfaceScreen()
			return
		
		# Handle tab switching
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			bTabClicked = True
			if inputClass.getFunctionName() == self.TAB_NORTH_EUROPE_ID:
				data.iCurrentImmigrationManagerTab = IMMIGRATION_MANAGER_TAB_NORTH_EUROPE
			elif inputClass.getFunctionName() == self.TAB_SOUTH_EUROPE_ID:
				data.iCurrentImmigrationManagerTab = IMMIGRATION_MANAGER_TAB_SOUTH_EUROPE
			elif inputClass.getFunctionName() == self.TAB_AFRICA_ID:
				data.iCurrentImmigrationManagerTab = IMMIGRATION_MANAGER_TAB_AFRICA
			elif inputClass.getFunctionName() == self.TAB_SIBERIA_ID:
				data.iCurrentImmigrationManagerTab = IMMIGRATION_MANAGER_TAB_SIBERIA
			elif inputClass.getFunctionName() == self.TAB_ASIA_ID:
				data.iCurrentImmigrationManagerTab = IMMIGRATION_MANAGER_TAB_ASIA
			else:
				bTabClicked = False
			
			if bTabClicked:
				print("Tab name: " + inputClass.getFunctionName() + "Tab id: " + str(data.iCurrentImmigrationManagerTab))
				self.drawMercenaryScreenContent(self.getScreen())
				return

		# If someone pressed one of the buttons in the screen then handle the
		# action
		if(inputClass.getFunctionName().endswith("Button")):
			# Split up the function name into the mercenary name and the actual
			# action that was performed
			sMercenary, panel, function = inputClass.getFunctionName().split("-")
			
			self.screenFunction = function
			
			iUnit = gc.getInfoTypeForString(sMercenary)
				
			# If the function was hire, then hire the mercenary
			if(function == "HireButton"):
				self.hireMercenaryOnScreen(screen, iUnit, data.iCurrentImmigrationManagerTab) 

				# Populate the mercenary information panel if small screen
				if self.bSmallScreen:
					self.populateMercenaryInformation(screen, objImmigrationUtils.getImmigrant(iUnit))
			
			# If the function was hire, then hire the mercenary
			if(function == "LoadButton"):
				self.placeMercenary(screen, iUnit, data.iCurrentImmigrationManagerTab) 

				# Populate the mercenary information panel if small screen
				if self.bSmallScreen:
					self.populateMercenaryInformation(screen, objImmigrationUtils.getImmigrant(iUnit))
										
			# If the function was to show the mercenary information then 
			# populate the mercenary information panel.
			if(function == "InfoButton"):
				
				# Get the mercenary from the global mercenary pool
				mercenary = objImmigrationUtils.getImmigrant(iUnit)

				# Return immediately if we still couldn't get the mercenary information
				if(mercenary == None):
					return

				# Populate the mercenary information panel
				self.populateMercenaryInformation(screen, mercenary)
		return 0
 		
		
	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName
													
	def update(self, fDelta):
		screen = self.getScreen()
		
		
	# Calculates the screens widgets positions, dimensions, text, etc.
	def calculateScreenWidgetData(self, screen):
		' Calculates the screens widgets positions, dimensions, text, etc. '
		self.iActivePlayer = gc.getGame().getActivePlayer()
		
		# The border width should not be a hard coded number
		self.screenWidgetData[BORDER_WIDTH] = 4
		self.screenWidgetData[MARGIN] = 20
		self.screenWidgetData[SPACING] = 40
		
		self.screenWidgetData[SCREEN_WIDTH] = screen.getXResolution()
		self.screenWidgetData[SCREEN_HEIGHT] = screen.getYResolution()

		if self.screenWidgetData[SCREEN_WIDTH] < 1920:
			self.bSmallScreen = True

		strScreenTitle = ""

		if(self.currentScreen == IMMIGRATION_MANAGER):
			strScreenTitle = localText.getText("TXT_KEY_IMMIGRANT_SCREEN_TITLE", ()).upper()
			
		# Screen title panel information
		self.screenWidgetData[SCREEN_TITLE_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH]
		self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] = 55
		self.screenWidgetData[SCREEN_TITLE_PANEL_X] = 0
		self.screenWidgetData[SCREEN_TITLE_PANEL_Y] = 0
		self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL] = u"<font=4b>" + localText.getText("TXT_KEY_IMMIGRATION_SCREEN_TITLE", ()).upper() + ": " + strScreenTitle + "</font>"
		self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_X] = self.screenWidgetData[SCREEN_WIDTH]/2
		self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_Y] = 8


		# Exit panel information		
		self.screenWidgetData[BOTTOM_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH]
		self.screenWidgetData[BOTTOM_PANEL_HEIGHT] = 55
		self.screenWidgetData[BOTTOM_PANEL_X] = 0
		self.screenWidgetData[BOTTOM_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 55

		self.screenWidgetData[EXIT_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"
		self.screenWidgetData[EXIT_TEXT_PANEL_X] = self.screenWidgetData[SCREEN_WIDTH] - 30
		self.screenWidgetData[EXIT_TEXT_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 42

	
		# Immigration Progress panel information
		self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] * 2 / 3
		self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*3) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT])) / 4
		self.screenWidgetData[IMMIGRATION_PROGRESS_INNER_PANEL_X] = self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*4)
		self.screenWidgetData[IMMIGRATION_PROGRESS_INNER_PANEL_Y] = self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*10)
		self.screenWidgetData[IMMIGRATION_PROGRESS_INNER_PANEL_WIDTH] = self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*8)
		self.screenWidgetData[IMMIGRATION_PROGRESS_INNER_PANEL_HEIGHT] = self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_HEIGHT] - (self.screenWidgetData[BORDER_WIDTH]*14)
		self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*3)
		self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_WIDTH] - (self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_IMMIGRATION_PROGRESS", ()) + "</font>"
		self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_PANEL_X] = self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_PANEL_Y] = self.screenWidgetData[IMMIGRATION_PROGRESS_TEXT_BACKGROUND_PANEL_Y] + 4
		self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_WIDTH] = self.screenWidgetData[IMMIGRATION_PROGRESS_INNER_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*4)
		self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_HEIGHT] = 70
		self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_X] = self.screenWidgetData[IMMIGRATION_PROGRESS_INNER_PANEL_X] + (self.screenWidgetData[IMMIGRATION_PROGRESS_INNER_PANEL_WIDTH]/2) - (self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_WIDTH]/2)
		self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_Y] = self.screenWidgetData[IMMIGRATION_PROGRESS_INNER_PANEL_Y] + (self.screenWidgetData[IMMIGRATION_PROGRESS_INNER_PANEL_HEIGHT]/2) - (self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_HEIGHT]/2)
		self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_TEXT_X] = self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_X] + (self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_WIDTH]/2)
		self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_TEXT_Y] = self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_Y] + (self.screenWidgetData[IMMIGRATION_PROGRESS_BAR_HEIGHT]/2)

		# Available Colonists panel information
		self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_Y] = self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_Y] + self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_WIDTH] = self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_WIDTH] / 3
		self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_HEIGHT] = self.screenWidgetData[IMMIGRATION_PROGRESS_PANEL_HEIGHT] * 3
		self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_X] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*4)
		self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_Y] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*10)
		self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*8)
		self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_HEIGHT] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_HEIGHT] - (self.screenWidgetData[BORDER_WIDTH]*14)
		self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*3)
		self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_WIDTH] - (self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_AVAILABLE_COLONISTS", ()) + "</font>"
		self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_PANEL_X] = self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_PANEL_Y] = self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_Y] + 4		
		
		
		# Available Mercenaries panel information
		self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_X] + self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_Y] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_Y]
		self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_WIDTH]
		self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_HEIGHT] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_HEIGHT]
		self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_X] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*4)
		self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_Y] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*10)
		self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*8)
		self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_HEIGHT] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_HEIGHT] - (self.screenWidgetData[BORDER_WIDTH]*14)
		self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*3)
		self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*6)
		self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_AVAILABLE_MERCENARIES", ()) + "</font>"
		self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL_X] = self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL_Y] = self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_Y] + 4
		
		
		# Earned Immigrants panel information
		self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_X] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X] + self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_Y] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_Y]
		self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_WIDTH]
		self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_HEIGHT] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_HEIGHT]
		self.screenWidgetData[EARNED_IMMIGRANTS_INNER_PANEL_X] = self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*4)
		self.screenWidgetData[EARNED_IMMIGRANTS_INNER_PANEL_Y] = self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*10)
		self.screenWidgetData[EARNED_IMMIGRANTS_INNER_PANEL_WIDTH] = self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*8)
		self.screenWidgetData[EARNED_IMMIGRANTS_INNER_PANEL_HEIGHT] = self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_HEIGHT] - (self.screenWidgetData[BORDER_WIDTH]*14)
		self.screenWidgetData[EARNED_IMMIGRANTS_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*3)
		self.screenWidgetData[EARNED_IMMIGRANTS_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[EARNED_IMMIGRANTS_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*6)
		self.screenWidgetData[EARNED_IMMIGRANTS_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[EARNED_IMMIGRANTS_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_EARNED_IMMIGRANTS", ()) + "</font>"
		self.screenWidgetData[EARNED_IMMIGRANTS_TEXT_PANEL_X] = self.screenWidgetData[EARNED_IMMIGRANTS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[EARNED_IMMIGRANTS_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[EARNED_IMMIGRANTS_TEXT_PANEL_Y] = self.screenWidgetData[EARNED_IMMIGRANTS_TEXT_BACKGROUND_PANEL_Y] + 4
		

		# Immigrant information panel information
		self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_X] = self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_X] + self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_X] + self.screenWidgetData[EARNED_IMMIGRANTS_PANEL_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*2) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))
		self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*6)
		self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_IMMIGRANT_INFORMATION", ()) + "</font>"
		self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_PANEL_X] = self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_PANEL_Y] = self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_Y] + 4
		
		self.screenWidgetData[IMMIGRANT_ANIMATION_X] = self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_X]+20
		self.screenWidgetData[IMMIGRANT_ANIMATION_Y] = self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_PANEL_Y]+40
		self.screenWidgetData[IMMIGRANT_ANIMATION_WIDTH] = self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_WIDTH] / 2
		self.screenWidgetData[IMMIGRANT_ANIMATION_HEIGHT] = self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_HEIGHT] / 2
		self.screenWidgetData[IMMIGRANT_ANIMATION_ROTATION_X] = -20
		self.screenWidgetData[IMMIGRANT_ANIMATION_ROTATION_Z] = 30
		self.screenWidgetData[IMMIGRANT_ANIMATION_SCALE] = 1.0

		self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_X] = self.screenWidgetData[IMMIGRANT_ANIMATION_X] + self.screenWidgetData[IMMIGRANT_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_Y] = self.screenWidgetData[IMMIGRANT_ANIMATION_Y]
		self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[IMMIGRANT_ANIMATION_X] + self.screenWidgetData[IMMIGRANT_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH])*6)
		self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_HEIGHT] = self.screenWidgetData[IMMIGRANT_ANIMATION_HEIGHT]

		self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_X] = self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_X]
		self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_Y] = self.screenWidgetData[IMMIGRANT_ANIMATION_Y] + self.screenWidgetData[IMMIGRANT_ANIMATION_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*18)
		self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_HEIGHT] = 64 + (self.screenWidgetData[BORDER_WIDTH]*9)

		self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_X] = self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_Y] = self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT] = self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_HEIGHT] - (self.screenWidgetData[BORDER_WIDTH]*2)

		self.screenWidgetData[IMMIGRANT_INFORMATION_STRATEGY_PANEL_X] = self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_X]
		self.screenWidgetData[IMMIGRANT_INFORMATION_STRATEGY_PANEL_Y] = self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_Y] + self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRANT_INFORMATION_STRATEGY_PANEL_WIDTH] = self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*18)
		self.screenWidgetData[IMMIGRANT_INFORMATION_STRATEGY_PANEL_HEIGHT] = self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_HEIGHT] - self.screenWidgetData[IMMIGRANT_ANIMATION_HEIGHT] - self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_HEIGHT] - self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT] -  (self.screenWidgetData[BORDER_WIDTH]*12)

		self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_STRATEGY_PANEL_X] = self.screenWidgetData[IMMIGRANT_INFORMATION_STRATEGY_PANEL_X] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_STRATEGY_PANEL_Y] = self.screenWidgetData[IMMIGRANT_INFORMATION_STRATEGY_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_STRATEGY_PANEL_WIDTH] = self.screenWidgetData[IMMIGRANT_INFORMATION_STRATEGY_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_STRATEGY_PANEL_HEIGHT] = self.screenWidgetData[IMMIGRANT_INFORMATION_STRATEGY_PANEL_HEIGHT] - (self.screenWidgetData[BORDER_WIDTH]*2)

		self.bScreenDataCalculated = True

@handler("GameStart")
def onGameStart():
	'Called at the start of the game'
	global objImmigrationUtils        
	objImmigrationUtils = ImmigrationUtils.ImmigrationUtils()
	return 0


# This method creates a new instance of the ImmigrationUtils class to be used later
@handler("OnLoad")
def onLoadGame():
	if (gc.getGame().getGameTurn() >= dBirth[active()]): #Rhye
		global objImmigrationUtils
		objImmigrationUtils = ImmigrationUtils.ImmigrationUtils()

@handler("EndPlayerTurn")
def onEndPlayerTurn(iGameTurn, iPlayer):   
	# This method will display the immigration manager screen
	# and provide the logic to make the computer players think.
	pPlayer = gc.getPlayer(iPlayer)
	
	if pPlayer != None and objImmigrationUtils.canEarnImmigrants(iPlayer):

		if g_bDebug:
			CvUtil.pyPrint(pPlayer.getName() + " Gold: " + str(pPlayer.getGold()) + " is human: " + str(pPlayer.isHuman()))  

		# Process new immigrants
		objImmigrationUtils.processImmigration(iPlayer)

		# if the player is not human and not independent then run the think method
		if not pPlayer.isHuman() and civ(iPlayer) < iIndependent1:
			if pPlayer.isAlive():
				if iPlayer % (g_bAIThinkPeriod) == iGameTurn % (g_bAIThinkPeriod):
					objImmigrationUtils.computerPlayerThink(iPlayer)