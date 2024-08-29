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

class CvImmigrationManager:
	"Mercenary Manager"
	
	def __init__(self, iScreenId):
	
		self.screenFunction = None
		
		# The different UI wiget names
		self.IMMIGRATION_MANAGER_SCREEN_NAME = "ImmigrationManager"

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
		
		
	# Returns the instance of the mercenary manager screen.						
	def getScreen(self):
		return CyGInterfaceScreen(self.IMMIGRATION_MANAGER_SCREEN_NAME, self.iScreenId)


	# Gets the instance of the mercenary manager screen and hides it.
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
	
		self.iActivePlayer = gc.getGame().getActivePlayer()
		
		screen = self.getScreen()

		# Calculate all of the screen position data
		self.calculateScreenWidgetData(screen)
		
		if(self.currentScreen == IMMIGRATION_MANAGER):
			self.drawMercenaryScreenContent(screen)
		

	# Populates the panel that shows all of the available Colonists
	def populateAvailableColonistsPanel(self, screen):
		# Get the available Colonists
		mercenaries = objImmigrationUtils.getAvailableMercenaries(self.iActivePlayer, lPossibleColonists)
		
		self.populateAvailablePanel(screen, AVAILABLE_COLONISTS_INNER_PANEL_ID, mercenaries)


	# Populates the panel that shows all of the available Expeditionaries
	def populateAvailableExpeditionariesPanel(self, screen):

		# Get the available Expeditionaries
		mercenaries = objImmigrationUtils.getAvailableMercenaries(self.iActivePlayer, lPossibleExpeditionaries)
		
		self.populateAvailablePanel(screen, AVAILABLE_EXPEDITIONARIES_INNER_PANEL_ID, mercenaries)
	
	
	# Populates the panel that shows all of the available Endowments
	def populateAvailableEndowmentsPanel(self, screen):

		# Get the available Endowments
		mercenaries = objImmigrationUtils.getAvailableMercenaries(self.iActivePlayer, lPossibleEndowments)
		
		self.populateAvailablePanel(screen, AVAILABLE_ENDOWMENTS_INNER_PANEL_ID, mercenaries)
		
	
	# Helper function that populates a panel (Colonist, Expeditionary, or Endowment)
	def populateAvailablePanel(self, screen, innerPanelId, mercenaries):
		# Get the ID for the current active player
		iPlayer = gc.getGame().getActivePlayer()

		mercenaryCount = 0
		
		# Go through the mercenaries and populate the available mercenaries panel
		for mercenaryName in mercenaries:

			# Get the mercenary from the dictionary	
			mercenary = mercenaries[mercenaryName]
			mercenaryName = str(mercenaryName)
			
			# Don't add the mercenary to the list if they were built by the current player
			if(mercenary.getBuilder() == iPlayer):
				continue

			if (not mercenary.canHireUnit(iPlayer)):
				continue
						
			screen.attachPanel(innerPanelId, mercenaryName, "", "", False, False, PanelStyles.PANEL_STYLE_DAWN)
			screen.attachImageButton( mercenaryName, mercenary.objUnitInfo.getType()+"-InfoButton", 
										mercenary.objUnitInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
			screen.attachPanel(mercenaryName, mercenaryName+"Text",mercenaryName, "", True, False, PanelStyles.PANEL_STYLE_EMPTY)

			# Build the mercenary hire cost string
			strHCost = mercenary.getHireCostString(iPlayer)
			
			screen.attachLabel( mercenaryName+"Text", mercenaryName  + "text3", "     Level: " + str(mercenary.getLevel()))			
			screen.attachLabel( mercenaryName+"Text", mercenaryName  + "text4", "     Hire Cost: " + strHCost)

			bEnableHireMercenary = true

			# Check to see if the player has enough gold to hire the mercenary. If they don't then
			# don't let them hire the mercenary.
			if not mercenary.canAfford(iPlayer):
				bEnableHireMercenary = False
				
			# Check if unit can spawn
			if not mercenary.hasValidSpawnTile(iPlayer):
				bEnableHireMercenary = False
			

			# Add the hire button for the mercenary
			if(bEnableHireMercenary):
				screen.attachPanel(mercenaryName, mercenaryName+"hireButtonPanel", "", "", False, True, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachImageButton( mercenaryName, mercenary.objUnitInfo.getType()+"-HireButton", 
											"Art/Interface/Buttons/Actions/Join.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, False )

			mercenaryCount = mercenaryCount + 1
			

		# Add the padding to the available mercenaries panel to improve the look of the screen
		if((4-mercenaryCount)>0):

			for i in range(4-mercenaryCount):
				screen.attachPanel(innerPanelId, "dummyPanelHire"+str(i), "", "", True, False, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachLabel( "dummyPanelHire"+str(i), "", "     ")
				screen.attachLabel( "dummyPanelHire"+str(i), "", "     ")
				screen.attachLabel( "dummyPanelHire"+str(i), "", "     ")
				
				
	# Clears out the unit information panel contents
	def clearUnitInformation(self, screen):
		screen.deleteWidget(UNIT_INFORMATION_PROMOTION_PANEL_ID)
		screen.deleteWidget(UNIT_INFORMATION_INNER_PROMOTION_PANEL_ID)
		screen.deleteWidget(UNIT_INFORMATION_DETAILS_PANEL_ID)
		screen.deleteWidget(UNIT_GRAPHIC)
		

	# Populates the unit information panel with the unit information details		
	def populateUnitInformation(self, screen, mercenary):
		# Get the ID for the current active player
		iPlayer = gc.getGame().getActivePlayer()
		
		screen.addPanel(UNIT_INFORMATION_PROMOTION_PANEL_ID, "", "", True, True, self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(UNIT_INFORMATION_INNER_PROMOTION_PANEL_ID, "Promotions", "", True, True, self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_EMPTY)
		screen.addPanel(UNIT_INFORMATION_DETAILS_PANEL_ID, "", "", True, False, self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_EMPTY)
		screen.attachListBoxGFC( UNIT_INFORMATION_DETAILS_PANEL_ID, UNIT_INFORMATION_DETAILS_LIST_ID, "", TableStyles.TABLE_STYLE_EMPTY )
		screen.enableSelect(UNIT_INFORMATION_DETAILS_LIST_ID, False)

		# Build the unit XP string
		strXP = u"%d/%d" %(mercenary.getExperienceLevel(), mercenary.getNextExperienceLevel())

		# Build the unit stats string
		strStats = u"%d%c    %d%c" %(mercenary.getUnitInfo().getCombat(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR),mercenary.getUnitInfo().getMoves(),CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
		screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, mercenary.getName(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		#screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, "  Unit Type: " + mercenary.getUnitInfo().getDescription(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY ) #Rhye
		screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, "  Level: " + str(mercenary.getLevel()) + "     XP: " + strXP, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, "  " + strStats, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, "  ", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Build the unit hire cost string
		strHCost = mercenary.getHireCostString(iPlayer)
		screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, "  Contract Income: " + strHCost, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		
		# Show the contract income for the unit if it is in the game			
		if(mercenary.isPlaced()):
			screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Otherwise, show the number of turns until the unit is placed in the game
		else:

			# Get the number of turns until the unit/mercenary is placed in the game
			placementTurns = mercenary.getPlacementTurns()
			strPlacement = ""
			
			# Build the placement string
			if(placementTurns <= 1):
				strPlacement = "Arrives next turn"
			else:
				strPlacement = u"Arrival in %d turns" %(placementTurns)
			screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, "  " + strPlacement, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		
		# Get the promotion list for the mercenary/unit
		promotionList = mercenary.getCurrentPromotionList()

		screen.attachMultiListControlGFC(UNIT_INFORMATION_INNER_PROMOTION_PANEL_ID, UNIT_INFORMATION_PROMOTION_LIST_CONTROL_ID, "", 1, 64, 64, TableStyles.TABLE_STYLE_STANDARD)

		# Add all of the promotions the mercenary/unit has.
		for promotion in promotionList:
			screen.appendMultiListButton( UNIT_INFORMATION_PROMOTION_LIST_CONTROL_ID, promotion.getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, gc.getInfoTypeForString(promotion.getType()), -1, false )
			
		screen.addUnitGraphicGFC(UNIT_GRAPHIC, mercenary.getUnitInfoID(), self.screenWidgetData[UNIT_ANIMATION_X], self.screenWidgetData[UNIT_ANIMATION_Y], self.screenWidgetData[UNIT_ANIMATION_WIDTH], self.screenWidgetData[UNIT_ANIMATION_HEIGHT], WidgetTypes.WIDGET_GENERAL, -1, -1, self.screenWidgetData[UNIT_ANIMATION_ROTATION_X], self.screenWidgetData[UNIT_ANIMATION_ROTATION_Z], self.screenWidgetData[UNIT_ANIMATION_SCALE], True)


	# Clears out the mercenary information panel contents
	def clearMercenaryInformation(self, screen):
		screen.deleteWidget(IMMIGRANT_INFORMATION_PROMOTION_PANEL_ID)
		screen.deleteWidget(IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_ID)
		screen.deleteWidget(IMMIGRANT_INFORMATION_DETAILS_PANEL_ID)
		screen.deleteWidget(IMMIGRANT_UNIT_GRAPHIC)		
		
			
	# Populates the mercenary information panel with the unit information details		
	def populateMercenaryInformation(self, screen, mercenary):
		# Get the ID for the current active player
		iPlayer = gc.getGame().getActivePlayer()

		screen.addPanel(IMMIGRANT_INFORMATION_PROMOTION_PANEL_ID, "", "", True, True, self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_X], self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_Y], self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_WIDTH], self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_ID, "Promotions", "", True, True, self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_X], self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_Y], self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_WIDTH], self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_EMPTY)
		screen.addPanel(IMMIGRANT_INFORMATION_DETAILS_PANEL_ID, "", "", True, False, self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_X], self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_Y], self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_WIDTH], self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_EMPTY)
		screen.attachListBoxGFC( IMMIGRANT_INFORMATION_DETAILS_PANEL_ID, IMMIGRANT_INFORMATION_DETAILS_LIST_ID, "", TableStyles.TABLE_STYLE_EMPTY )
		screen.enableSelect(IMMIGRANT_INFORMATION_DETAILS_LIST_ID, False)

		# Build the mercenary hire cost string
		strHCost = mercenary.getHireCostString(iPlayer)
		
		# Build the mercenary XP string
		strXP = u"%d/%d" %(mercenary.getExperienceLevel(), mercenary.getNextExperienceLevel())

		# Build the unit stats string
		strStats = u"%d%c    %d%c" %(mercenary.getUnitInfo().getCombat(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR),mercenary.getUnitInfo().getMoves(),CyGame().getSymbolID(FontSymbols.MOVES_CHAR))

		screen.appendListBoxString( IMMIGRANT_INFORMATION_DETAILS_LIST_ID, mercenary.getName(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		#screen.appendListBoxString( IMMIGRANT_INFORMATION_DETAILS_LIST_ID, "  Unit Type: " + mercenary.getUnitInfo().getDescription(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY ) #Rhye
		screen.appendListBoxString( IMMIGRANT_INFORMATION_DETAILS_LIST_ID, "  Level: " + str(mercenary.getLevel()) + "     XP: " + strXP, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString( IMMIGRANT_INFORMATION_DETAILS_LIST_ID, "  " + strStats, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString( IMMIGRANT_INFORMATION_DETAILS_LIST_ID, "  ", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString( IMMIGRANT_INFORMATION_DETAILS_LIST_ID, "  Hire Cost: " + strHCost, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Show the mercenary costs if it is in the game			
		if(mercenary.isPlaced()):
			screen.appendListBoxString( IMMIGRANT_INFORMATION_DETAILS_LIST_ID, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		# Otherwise, show the number of turns until the unit is placed in the game
		else:
			# Get the number of turns until the unit/mercenary is placed in the game
			placementTurns = mercenary.getPlacementTurns()
			strPlacement = ""

			# Build the placement string
			if(placementTurns <= 1):
				strPlacement = "Arrives next turn"
			else:
				strPlacement = u"Arrival in %d turns" %(placementTurns)
			screen.appendListBoxString( IMMIGRANT_INFORMATION_DETAILS_LIST_ID, "  " + strPlacement, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		
		# Get the promotion list for the mercenary
		promotionList = mercenary.getCurrentPromotionList()

		screen.attachMultiListControlGFC(IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_ID, IMMIGRANT_INFORMATION_PROMOTION_LIST_CONTROL_ID, "", 1, 64, 64, TableStyles.TABLE_STYLE_STANDARD)

		# Add all of the promotions the mercenary has.
		for promotion in promotionList:
			screen.appendMultiListButton( IMMIGRANT_INFORMATION_PROMOTION_LIST_CONTROL_ID, promotion.getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, gc.getInfoTypeForString(promotion.getType()), -1, false )
			
		screen.addUnitGraphicGFC(IMMIGRANT_UNIT_GRAPHIC, mercenary.getUnitInfoID(), self.screenWidgetData[IMMIGRANT_ANIMATION_X], self.screenWidgetData[IMMIGRANT_ANIMATION_Y], self.screenWidgetData[IMMIGRANT_ANIMATION_WIDTH], self.screenWidgetData[IMMIGRANT_ANIMATION_HEIGHT], WidgetTypes.WIDGET_GENERAL, -1, -1, self.screenWidgetData[IMMIGRANT_ANIMATION_ROTATION_X], self.screenWidgetData[IMMIGRANT_ANIMATION_ROTATION_Z], self.screenWidgetData[IMMIGRANT_ANIMATION_SCALE], True)

	
	# Draws the gold information in the "Mercenary Manager" screens
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
		

	# Draws the top bar of the "Mercenary Manager" screens
	def drawScreenTop(self, screen):
		screen.setDimensions(0, 0, self.screenWidgetData[SCREEN_WIDTH], self.screenWidgetData[SCREEN_HEIGHT])
		screen.addDrawControl(BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.screenWidgetData[SCREEN_WIDTH], self.screenWidgetData[SCREEN_HEIGHT], WidgetTypes.WIDGET_GENERAL, -1, -1 )
 		screen.addDDSGFC(BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.screenWidgetData[SCREEN_WIDTH], self.screenWidgetData[SCREEN_HEIGHT], WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.addPanel(SCREEN_TITLE_PANEL_ID, u"", u"", True, False, self.screenWidgetData[SCREEN_TITLE_PANEL_X], self.screenWidgetData[SCREEN_TITLE_PANEL_Y], self.screenWidgetData[SCREEN_TITLE_PANEL_WIDTH], self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_TOPBAR )
		screen.setText(SCREEN_TITLE_TEXT_PANEL_ID, "Background", self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_X], self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Draw the gold information for the screen
		self.drawGoldInformation(screen)


	# Draws the bottom bar of the "Mercenary Manager" screens
	def drawScreenBottom(self, screen):
		screen.addPanel(BOTTOM_PANEL_ID, "", "", True, True, self.screenWidgetData[BOTTOM_PANEL_X], self.screenWidgetData[BOTTOM_PANEL_Y], self.screenWidgetData[BOTTOM_PANEL_WIDTH], self.screenWidgetData[BOTTOM_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.setText(IMMIGRATION_TEXT_PANEL_ID, "Background", self.screenWidgetData[IMMIGRATION_TEXT_PANEL], CvUtil.FONT_LEFT_JUSTIFY, self.screenWidgetData[IMMIGRATION_TEXT_PANEL_X], self.screenWidgetData[IMMIGRATION_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setText(EXIT_TEXT_PANEL_ID, "Background", self.screenWidgetData[EXIT_TEXT_PANEL], CvUtil.FONT_RIGHT_JUSTIFY, self.screenWidgetData[EXIT_TEXT_PANEL_X], self.screenWidgetData[EXIT_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

	# Draws the mercenary screen content
	def drawMercenaryScreenContent(self, screen):

		# Draw the top bar
		self.drawScreenTop(screen)
 
		# Draw the bottom bar
		self.drawScreenBottom(screen)
				
		screen.addPanel(AVAILABLE_COLONISTS_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_X], self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_Y], self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(AVAILABLE_COLONISTS_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_X], self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_Y], self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)
		screen.addPanel(AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(AVAILABLE_COLONISTS_TEXT_PANEL_ID, "Background", self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_PANEL_X], self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addPanel(AVAILABLE_EXPEDITIONARIES_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_X], self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_Y], self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(AVAILABLE_EXPEDITIONARIES_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_INNER_PANEL_X], self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_INNER_PANEL_Y], self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_INNER_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)
		screen.addPanel(AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(AVAILABLE_EXPEDITIONARIES_TEXT_PANEL_ID, "Background", self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_PANEL_X], self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.addPanel(AVAILABLE_ENDOWMENTS_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_X], self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_Y], self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(AVAILABLE_ENDOWMENTS_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_ENDOWMENTS_INNER_PANEL_X], self.screenWidgetData[AVAILABLE_ENDOWMENTS_INNER_PANEL_Y], self.screenWidgetData[AVAILABLE_ENDOWMENTS_INNER_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_ENDOWMENTS_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)
		screen.addPanel(AVAILABLE_ENDOWMENTS_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[AVAILABLE_ENDOWMENTS_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[AVAILABLE_ENDOWMENTS_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[AVAILABLE_ENDOWMENTS_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_ENDOWMENTS_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(AVAILABLE_ENDOWMENTS_TEXT_PANEL_ID, "Background", self.screenWidgetData[AVAILABLE_ENDOWMENTS_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[AVAILABLE_ENDOWMENTS_TEXT_PANEL_X], self.screenWidgetData[AVAILABLE_ENDOWMENTS_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		
		screen.addPanel(IMMIGRANT_INFORMATION_PANEL_ID, "", "", True, True, self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_X], self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_Y], self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_WIDTH], self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(IMMIGRANT_INFORMATION_TEXT_PANEL_ID, "Background", self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_PANEL_X], self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				
		screen.showWindowBackground(False)

		# Populate the available panels
		self.populateAvailableColonistsPanel(screen)
		self.populateAvailableExpeditionariesPanel(screen)
		self.populateAvailableEndowmentsPanel(screen)


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
	
	# Hires a mercenary for a player
	def hireMercenary(self, screen, iMercenary):

		# Get the active player ID
		iPlayer = gc.getGame().getActivePlayer()

		# Hire the mercenary for the player
		objImmigrationUtils.hireMercenary(iMercenary, iPlayer) 

		# Draw the gold information for the screen
		self.drawGoldInformation(screen)

		# Update the available mercenaries in the available mercenaries panel
		self.updateAvailableColonists(screen)
		self.updateAvailableExpeditionaries(screen)
		self.updateAvailableEndowments(screen)

		# Clear the information in the mercenary information panel
		self.clearMercenaryInformation(screen)
				
	# Updates the available mercenaries panel, displays the hire button to the 
	# player only for the mercenaries they can hire.
	def updateAvailableColonists(self, screen):
	
		# Get the ID for the current player
		iPlayer = gc.getGame().getActivePlayer()
		
		# Get the mercenaries available for hire
		mercenaries = objImmigrationUtils.getAvailableMercenaries(iPlayer, lPossibleColonists)

		self.updateAvailableUnits(screen, mercenaries, iPlayer)
		
	# Updates the available mercenaries panel, displays the hire button to the 
	# player only for the mercenaries they can hire.
	def updateAvailableExpeditionaries(self, screen):
	
		# Get the ID for the current player
		iPlayer = gc.getGame().getActivePlayer()
		
		# Get the mercenaries available for hire
		mercenaries = objImmigrationUtils.getAvailableMercenaries(iPlayer, lPossibleExpeditionaries)

		self.updateAvailableUnits(screen, mercenaries, iPlayer)
	
	
	# Updates the available mercenaries panel, displays the hire button to the 
	# player only for the mercenaries they can hire.
	def updateAvailableEndowments(self, screen):
	
		# Get the ID for the current player
		iPlayer = gc.getGame().getActivePlayer()
		
		# Get the mercenaries available for hire
		mercenaries = objImmigrationUtils.getAvailableMercenaries(iPlayer, lPossibleEndowments)

		self.updateAvailableUnits(screen, mercenaries, iPlayer)
	
	
	def updateAvailableUnits(self, screen, mercenaries, iPlayer):
		# Go through each of the available mercenaries
		for mercenaryName in mercenaries:

			mercenary = mercenaries[mercenaryName]
			
			mercenaryName = str(mercenaryName)
			
			# Continue if the mercenary was built by the current player
			if(mercenary.iBuilder == iPlayer):
				continue
				
			# Delete the cost string for the current mercenary we are processing.
			screen.deleteWidget(mercenaryName+"Text")
			
			screen.attachPanel(mercenaryName, mercenaryName+"Text",mercenaryName, "", True, False, PanelStyles.PANEL_STYLE_EMPTY)
			
			# Build the mercenary hire cost string
			strHCost = mercenary.getHireCostString(iPlayer)
			
			screen.attachLabel( mercenaryName+"Text", mercenaryName  + "text3", "     Level: " + str(mercenary.getLevel()))			
			screen.attachLabel( mercenaryName+"Text", mercenaryName  + "text4", "     Hire Cost: " + strHCost)

			# Delete the hire button for the current mercenary we are processing.
			screen.deleteWidget(mercenary.objUnitInfo.getType()+"-HireButton")

			# To start off we'll assume that the player can hire the mercenary
			bEnableHireMercenary = true

			# If the player doesn't have enough money to hire the mercenary then
			# we won't allow them to hire the current mercenary being processed.
			if not mercenary.canAfford(iPlayer):
				bEnableHireMercenary = False
			
			# Check if unit can spawn
			if not mercenary.hasValidSpawnTile(iPlayer):
				bEnableHireMercenary = False

			if(bEnableHireMercenary):
				screen.attachPanel(mercenaryName, mercenaryName+"hireButtonPanel", "", "", False, True, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachImageButton( mercenaryName, mercenary.objUnitInfo.getType()+"-HireButton", 
											"Art/Interface/Buttons/Actions/Join.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
	
	# Handles the input to the mercenary manager screens
	def handleInput (self, inputClass):

		# Get the instance of the screen
		screen = self.getScreen()

		# Debug code - start
		if g_bDebug:
			screen.setText( "TopPanelDebugMsg", "TopPanel", inputClass.getFunctionName()
						, CvUtil.FONT_RIGHT_JUSTIFY, 1010, 20, -10, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		# Debug code - end
		
		# Get the data
		theKey = int(inputClass.getData())
		
		print("TEMP: inputClass.getFunctionName(): " + inputClass.getFunctionName())

		# If the escape key was pressed then set the current screen to mercenary manager
		if (inputClass.getNotifyCode() == self.EventKeyDown and theKey == int(InputTypes.KB_ESCAPE)):
			self.currentScreen = IMMIGRATION_MANAGER

		# If the exit text was pressed then set the current screen to mercenary manager.
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

		# If someone pressed one of the buttons in the screen then handle the
		# action
		if(inputClass.getFunctionName().endswith("Button")):
			# Split up the function name into the mercenary name and the actual
			# action that was performed
			sMercenary, function = inputClass.getFunctionName().split("-")
			
			print("TEMP: function: " + function + "and sMercenary: " + sMercenary)
			
			self.screenFunction = function
			
			iMercenary = gc.getInfoTypeForString(sMercenary)
				
			# If the function was hire, then hire the mercenary
			if(function == "HireButton"):
				self.hireMercenary(screen, iMercenary) 
										
			# If the function was to show the mercenary information then 
			# populate the mercenary information panel.
			if(function == "InfoButton"):
				
				# Get the mercenary from the global mercenary pool
				mercenary = objImmigrationUtils.getMercenary(iMercenary)

				# Return immediately if we still couldn't get the mercenary information
				if(mercenary == None):
					return
					
				# Calculate the screen information
				self.calculateScreenWidgetData(screen)

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
		
		# The border width should not be a hard coded number
		self.screenWidgetData[BORDER_WIDTH] = 4
		
		self.screenWidgetData[SCREEN_WIDTH] = screen.getXResolution()
		self.screenWidgetData[SCREEN_HEIGHT] = screen.getYResolution()

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

		self.screenWidgetData[IMMIGRATION_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_IMMIGRANT_SCREEN_TITLE", ()).upper() + "</font>"
		self.screenWidgetData[IMMIGRATION_TEXT_PANEL_X] = 30
		self.screenWidgetData[IMMIGRATION_TEXT_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 42

		self.screenWidgetData[EXIT_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"
		self.screenWidgetData[EXIT_TEXT_PANEL_X] = self.screenWidgetData[SCREEN_WIDTH] - 30
		self.screenWidgetData[EXIT_TEXT_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 42

		
		# Available Colonists panel information
		self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_WIDTH] = 350
		self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*3) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))
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
		
		
		# Available Expeditionaries panel information
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_X] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_X] + self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_WIDTH] = 350
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*3) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_INNER_PANEL_X] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*4)
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_INNER_PANEL_Y] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*10)
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_INNER_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*8)
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_INNER_PANEL_HEIGHT] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_HEIGHT] - (self.screenWidgetData[BORDER_WIDTH]*14)
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*3)
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*6)
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_AVAILABLE_EXPEDITIONARIES", ()) + "</font>"
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_PANEL_X] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_PANEL_Y] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_Y] + 4
		
		
		# Available Endowments panel information
		self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_X] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_X] + self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_WIDTH] = 350
		self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*3) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))
		self.screenWidgetData[AVAILABLE_ENDOWMENTS_INNER_PANEL_X] = self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*4)
		self.screenWidgetData[AVAILABLE_ENDOWMENTS_INNER_PANEL_Y] = self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*10)
		self.screenWidgetData[AVAILABLE_ENDOWMENTS_INNER_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*8)
		self.screenWidgetData[AVAILABLE_ENDOWMENTS_INNER_PANEL_HEIGHT] = self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_HEIGHT] - (self.screenWidgetData[BORDER_WIDTH]*14)
		self.screenWidgetData[AVAILABLE_ENDOWMENTS_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*3)
		self.screenWidgetData[AVAILABLE_ENDOWMENTS_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[AVAILABLE_ENDOWMENTS_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*6)
		self.screenWidgetData[AVAILABLE_ENDOWMENTS_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[AVAILABLE_ENDOWMENTS_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_AVAILABLE_ENDOWMENTS", ()) + "</font>"
		self.screenWidgetData[AVAILABLE_ENDOWMENTS_TEXT_PANEL_X] = self.screenWidgetData[AVAILABLE_ENDOWMENTS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[AVAILABLE_ENDOWMENTS_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[AVAILABLE_ENDOWMENTS_TEXT_PANEL_Y] = self.screenWidgetData[AVAILABLE_ENDOWMENTS_TEXT_BACKGROUND_PANEL_Y] + 4
		
		
		# Mercenary information panel information
		self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_X] = self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_X] + self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_X] + self.screenWidgetData[AVAILABLE_ENDOWMENTS_PANEL_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2))
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
		self.screenWidgetData[IMMIGRANT_ANIMATION_WIDTH] = 303
		self.screenWidgetData[IMMIGRANT_ANIMATION_HEIGHT] = 200
		self.screenWidgetData[IMMIGRANT_ANIMATION_ROTATION_X] = -20
		self.screenWidgetData[IMMIGRANT_ANIMATION_ROTATION_Z] = 30
		self.screenWidgetData[IMMIGRANT_ANIMATION_SCALE] = 1.0
		
		self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_X] = self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_X]
		self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_Y] = self.screenWidgetData[IMMIGRANT_ANIMATION_Y] + self.screenWidgetData[IMMIGRANT_ANIMATION_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*18)
		self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_HEIGHT] = 128 + (self.screenWidgetData[BORDER_WIDTH]*9)

		self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_X] = self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_Y] = self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT] = self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_HEIGHT] - (self.screenWidgetData[BORDER_WIDTH]*2)

		self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_X] = self.screenWidgetData[IMMIGRANT_ANIMATION_X] + self.screenWidgetData[IMMIGRANT_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_Y] = self.screenWidgetData[IMMIGRANT_ANIMATION_Y]
		self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[IMMIGRANT_ANIMATION_X] + self.screenWidgetData[IMMIGRANT_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH])*6)
		self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_HEIGHT] = self.screenWidgetData[IMMIGRANT_ANIMATION_HEIGHT]


		# Units contracted out panel information
		self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_WIDTH] = 450
		self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*3) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))/2
		self.screenWidgetData[UNITS_CONTRACTED_OUT_INNER_PANEL_X] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_X] + (4*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[UNITS_CONTRACTED_OUT_INNER_PANEL_Y] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_Y] + (10*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[UNITS_CONTRACTED_OUT_INNER_PANEL_WIDTH] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_WIDTH] - (8*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[UNITS_CONTRACTED_OUT_INNER_PANEL_HEIGHT] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_HEIGHT] - (14*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_WIDTH] - (self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_UNITS_CONTRACTED_OUT", ()) + "</font>"
		self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_PANEL_X] = self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_PANEL_Y] = self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_Y] + 4		

		
		# Hired mercenaries panel information
		self.screenWidgetData[AVAILABLE_UNITS_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_UNITS_PANEL_Y] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_Y] + self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_UNITS_PANEL_WIDTH] = 450
		self.screenWidgetData[AVAILABLE_UNITS_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*3) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))/2
		self.screenWidgetData[AVAILABLE_UNITS_INNER_PANEL_X] = self.screenWidgetData[AVAILABLE_UNITS_PANEL_X] + (4*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_UNITS_INNER_PANEL_Y] = self.screenWidgetData[AVAILABLE_UNITS_PANEL_Y] + (10*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_UNITS_INNER_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_UNITS_PANEL_WIDTH] - (8*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_UNITS_INNER_PANEL_HEIGHT] = self.screenWidgetData[AVAILABLE_UNITS_PANEL_HEIGHT] - (14*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[AVAILABLE_UNITS_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[AVAILABLE_UNITS_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_UNITS_PANEL_WIDTH] - (self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[AVAILABLE_UNITS_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_AVAILABLE_UNITS", ()) + "</font>"
		self.screenWidgetData[AVAILABLE_UNITS_TEXT_PANEL_X] = self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[AVAILABLE_UNITS_TEXT_PANEL_Y] = self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_Y] + 4
		
				
		# Unit information panel information
		self.screenWidgetData[UNIT_INFORMATION_PANEL_X] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_X] + self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_X] + self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[UNIT_INFORMATION_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*2) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))
		self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[UNIT_INFORMATION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[UNIT_INFORMATION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[UNIT_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*6)
		self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_UNIT_INFORMATION", ()) + "</font>"
		self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_X] = self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_Y] = self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_Y] + 4

		self.screenWidgetData[UNIT_ANIMATION_X] = self.screenWidgetData[UNIT_INFORMATION_PANEL_X]+20
		self.screenWidgetData[UNIT_ANIMATION_Y] = self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_Y]+40
		self.screenWidgetData[UNIT_ANIMATION_WIDTH] = 303
		self.screenWidgetData[UNIT_ANIMATION_HEIGHT] = 200
		self.screenWidgetData[UNIT_ANIMATION_ROTATION_X] = -20
		self.screenWidgetData[UNIT_ANIMATION_ROTATION_Z] = 30
		self.screenWidgetData[UNIT_ANIMATION_SCALE] = 1.0
		
		self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_X] = self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_X]
		self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_Y] = self.screenWidgetData[UNIT_ANIMATION_Y] + self.screenWidgetData[UNIT_ANIMATION_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[UNIT_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*18)
		self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_HEIGHT] = 128 + (self.screenWidgetData[BORDER_WIDTH]*9)

		self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_X] = self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_Y] = self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT] = self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_HEIGHT] - (self.screenWidgetData[BORDER_WIDTH]*2)

		self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_X] = self.screenWidgetData[UNIT_ANIMATION_X] + self.screenWidgetData[UNIT_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_Y] = self.screenWidgetData[UNIT_ANIMATION_Y]
		self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[UNIT_ANIMATION_X] + self.screenWidgetData[UNIT_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH])*6)
		self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_HEIGHT] = self.screenWidgetData[UNIT_ANIMATION_HEIGHT]
		self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_X] = self.screenWidgetData[IMMIGRANT_INFORMATION_TEXT_BACKGROUND_PANEL_X]
		self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_Y] = self.screenWidgetData[IMMIGRANT_ANIMATION_Y] + self.screenWidgetData[IMMIGRANT_ANIMATION_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[IMMIGRANT_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*18)
		self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_HEIGHT] = 128 + (self.screenWidgetData[BORDER_WIDTH]*9)

		self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_X] = self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_Y] = self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[IMMIGRANT_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT] = self.screenWidgetData[IMMIGRANT_INFORMATION_PROMOTION_PANEL_HEIGHT] - (self.screenWidgetData[BORDER_WIDTH]*2)

		self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_X] = self.screenWidgetData[IMMIGRANT_ANIMATION_X] + self.screenWidgetData[IMMIGRANT_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_Y] = self.screenWidgetData[IMMIGRANT_ANIMATION_Y]
		self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[IMMIGRANT_ANIMATION_X] + self.screenWidgetData[IMMIGRANT_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH])*6)
		self.screenWidgetData[IMMIGRANT_INFORMATION_DETAILS_PANEL_HEIGHT] = self.screenWidgetData[IMMIGRANT_ANIMATION_HEIGHT]

	# Converts a number into its string representation. This is needed since
	# for whatever reason, numbers did not work very well when using them 
	# for all of the different panels in the mercenary manager screen. The
	# unit ID number 382343 is converted to: CHBCDC.
	def numberToAlpha(self, iNum):
		#             1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26
		alphaList = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		strNum = str(iNum)
		strAlpha = ""
		
		# Go though the alphaList and convert the numbers to letters
		for i in range (len(strNum)):
			strAlpha = strAlpha + alphaList[int(strNum[i])]
			
		return strAlpha
	
	
	# Converts a number into its string representation. This is needed since
	# for whatever reason, numbers did not work very well when using them 
	# for all of the different panels in the mercenary manager screen. The
	# string "CHBCDC" is converted to: 382343.
	def alphaToNumber(self, strAlpha):
		#             1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26
		alphaList = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		
		strNum = ""

		# Go though the alphaList and convert the letters to numbers
		for i in range (len(strAlpha)):
			strNum = strNum + str(alphaList.index(strAlpha[i]))
		
		return int(strNum)


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
	# This method will display the mercenary manager screen
	# and provide the logic to make the computer players think.
	pPlayer = gc.getPlayer(iPlayer)
	
	# TEMP DEBUG
	#return
	
	if pPlayer != None and gc.getTeam(pPlayer.getTeam()).isHasTech(iOldWorldCulture):

		if g_bDebug:
			CvUtil.pyPrint(pPlayer.getName() + " Gold: " + str(pPlayer.getGold()) + " is human: " + str(pPlayer.isHuman()))     

		# if the player is not human and not independent then run the think method
		if not pPlayer.isHuman() and civ(iPlayer) < iIndependent:
			if pPlayer.isAlive():
				if iPlayer % (g_bAIThinkPeriod) == iGameTurn % (g_bAIThinkPeriod):
					print("Turn: " + str(iGameTurn) + " AI thinking about Immigrants, iPlayer: " + str(iPlayer))
					objImmigrationUtils.computerPlayerThink(iPlayer)                                                                



