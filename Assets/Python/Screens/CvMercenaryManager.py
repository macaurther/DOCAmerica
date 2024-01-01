#
# Mercenaries Mod
# By: The Lopez
# CvMercenaryManager
# 

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import time
import PyHelpers
import Popup as PyPopup
import MercenaryUtils
#import CvConfigParser #Rhye
import math
from CvMercenaryScreensEnums import *
from Consts import *
from Core import *

from Events import handler

PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()
objMercenaryUtils = MercenaryUtils.MercenaryUtils()

# Set to true to print out debug messages in the logs
g_bDebug = false

class CvMercenaryManager:
	"Mercenary Manager"
	
	def __init__(self, iScreenId):
	
		self.mercenaryName = None
		self.screenFunction = None
		
		# The different UI wiget names
		self.MERCENARY_MANAGER_SCREEN_NAME = "MercenaryManager"

		self.WIDGET_ID = "MercenaryManagerWidget"
		self.Z_BACKGROUND = -2.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.EventKeyDown=6
						
		self.iScreenId = iScreenId
		
		# When populated this dictionary will contain the information needed to build
		# the widgets for the current screen resolution.		
		self.screenWidgetData = {}
	
		self.nWidgetCount = 0
		self.iActivePlayer = -1
		
		self.currentScreen = MERCENARY_MANAGER
		
		
	# Returns the instance of the mercenary manager screen.						
	def getScreen(self):
		return CyGInterfaceScreen(self.MERCENARY_MANAGER_SCREEN_NAME, self.iScreenId)


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
		
		if(self.currentScreen == MERCENARY_MANAGER):
			self.drawMercenaryScreenContent(screen)
		elif(self.currentScreen == MERCENARY_GROUPS_MANAGER):
			self.drawMercenaryGroupsScreenContent(screen)
		

	# Populates the panel that shows all of the available Colonists
	def populateAvailableColonistsPanel(self, screen):
		# Get the available Colonists
		mercenaries = objMercenaryUtils.getAvailableColonists(self.iActivePlayer)
		
		# Get the ID for the current active player
		iPlayer = gc.getGame().getActivePlayer()
		
		# Get the actual current player object
		player = gc.getPlayer(iPlayer)
		
		# Get the players current gold amount
		currentGold = player.getGold()

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
						
			screen.attachPanel(AVAILABLE_COLONISTS_INNER_PANEL_ID, mercenaryName, "", "", False, False, PanelStyles.PANEL_STYLE_DAWN)
			screen.attachImageButton( mercenaryName, mercenaryName+"_InfoButton", 
										mercenary.objUnitInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
			screen.attachPanel(mercenaryName, mercenaryName+"Text",mercenaryName, "", True, False, PanelStyles.PANEL_STYLE_EMPTY)

			# Build the mercenary hire cost string
			strHCost = u"%d%c" %(mercenary.getHireCostXPlayer(iPlayer), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
			
			# Build the mercenary maintenance cost string
			strMCost = u"%d%c" %(mercenary.getMercenaryMaintenanceCostXPlayer(iPlayer), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
			
			screen.attachLabel( mercenaryName+"Text", mercenaryName  + "text3", "     Level: " + str(mercenary.getLevel()))			
			screen.attachLabel( mercenaryName+"Text", mercenaryName  + "text4", "     Hire Cost: " + strHCost + "  Maint. Cost: " + strMCost)

			bEnableHireMercenary = true

			# Check to see if the player has enough gold to hire the mercenary. If they don't then
			# don't let them hire the mercenary.
			if(	(currentGold-mercenary.getHireCostXPlayer(iPlayer)) <= 0):
				bEnableHireMercenary = False
				
			# Check if unit can spawn
			if not mercenary.hasValidSpawnTile(iPlayer):
				bEnableHireMercenary = False
			

			# Add the hire button for the mercenary
			if(bEnableHireMercenary):
				screen.attachPanel(mercenaryName, mercenaryName+"hireButtonPanel", "", "", False, True, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachImageButton( mercenaryName, mercenaryName+"_HireButton", 
											"Art/Interface/Buttons/Actions/Join.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, False )

			mercenaryCount = mercenaryCount + 1
			

		# Add the padding to the available mercenaries panel to improve the look of the screen
		if((4-mercenaryCount)>0):

			for i in range(4-mercenaryCount):
				screen.attachPanel(AVAILABLE_COLONISTS_INNER_PANEL_ID, "dummyPanelHire"+str(i), "", "", True, False, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachLabel( "dummyPanelHire"+str(i), "", "     ")
				screen.attachLabel( "dummyPanelHire"+str(i), "", "     ")
				screen.attachLabel( "dummyPanelHire"+str(i), "", "     ")


	# Populates the panel that shows all of the available Expeditionaries
	def populateAvailableExpeditionariesPanel(self, screen):

		# Get the available Colonists
		mercenaries = objMercenaryUtils.getAvailableExpeditionaries(self.iActivePlayer)
		
		# Get the ID for the current active player
		iPlayer = gc.getGame().getActivePlayer()
		
		# Get the actual current player object
		player = gc.getPlayer(iPlayer)
		
		# Get the players current gold amount
		currentGold = player.getGold()

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
						
			screen.attachPanel(AVAILABLE_EXPEDITIONARIES_INNER_PANEL_ID, mercenaryName, "", "", False, False, PanelStyles.PANEL_STYLE_DAWN)
			screen.attachImageButton( mercenaryName, mercenaryName+"_InfoButton", 
										mercenary.objUnitInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
			screen.attachPanel(mercenaryName, mercenaryName+"Text",mercenaryName, "", True, False, PanelStyles.PANEL_STYLE_EMPTY)

			# Build the mercenary hire cost string
			strHCost = u"%d%c" %(mercenary.getHireCostXPlayer(iPlayer), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
			
			# Build the mercenary maintenance cost string
			strMCost = u"%d%c" %(mercenary.getMercenaryMaintenanceCostXPlayer(iPlayer), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
			
			screen.attachLabel( mercenaryName+"Text", mercenaryName  + "text3", "     Level: " + str(mercenary.getLevel()))			
			screen.attachLabel( mercenaryName+"Text", mercenaryName  + "text4", "     Hire Cost: " + strHCost + "  Maint. Cost: " + strMCost)

			bEnableHireMercenary = true

			# Check to see if the player has enough gold to hire the mercenary. If they don't then
			# don't let them hire the mercenary.
			if(	(currentGold-mercenary.getHireCostXPlayer(iPlayer)) <= 0):
				bEnableHireMercenary = False
				
			# Check if unit can spawn
			if not mercenary.hasValidSpawnTile(iPlayer):
				bEnableHireMercenary = False
			

			# Add the hire button for the mercenary
			if(bEnableHireMercenary):
				screen.attachPanel(mercenaryName, mercenaryName+"hireButtonPanel", "", "", False, True, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachImageButton( mercenaryName, mercenaryName+"_HireButton", 
											"Art/Interface/Buttons/Actions/Join.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, False )

			mercenaryCount = mercenaryCount + 1
			

		# Add the padding to the available mercenaries panel to improve the look of the screen
		if((4-mercenaryCount)>0):

			for i in range(4-mercenaryCount):
				screen.attachPanel(AVAILABLE_EXPEDITIONARIES_INNER_PANEL_ID, "dummyPanelHire"+str(i), "", "", True, False, PanelStyles.PANEL_STYLE_EMPTY)
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

		# If the unit is hired then display their employeers information
		if(mercenary.isHired()):
			screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, "  Hired By: " + gc.getPlayer(mercenary.getOwner()).getName(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Otherwise show their hire cost information			
		else:
			# Build the unit hire cost string
			strHCost = u"%d%c" %(mercenary.getHireCost(), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
			screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, "  Contract Income: " + strHCost, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		
		# Show the contract income for the unit if it is in the game			
		if(mercenary.isPlaced()):
			strMCost = u"%d%c" %(mercenary.getMercenaryMaintenanceCost(), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
			screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, "  Income/Turn: " + strMCost, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

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
		screen.deleteWidget(MERCENARY_INFORMATION_PROMOTION_PANEL_ID)
		screen.deleteWidget(MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_ID)
		screen.deleteWidget(MERCENARY_INFORMATION_DETAILS_PANEL_ID)
		screen.deleteWidget(MERCENARIES_UNIT_GRAPHIC)		
		
			
	# Populates the mercenary information panel with the unit information details		
	def populateMercenaryInformation(self, screen, mercenary):

		screen.addPanel(MERCENARY_INFORMATION_PROMOTION_PANEL_ID, "", "", True, True, self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_X], self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_Y], self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_WIDTH], self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_ID, "Promotions", "", True, True, self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_X], self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_Y], self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_WIDTH], self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_EMPTY)
		screen.addPanel(MERCENARY_INFORMATION_DETAILS_PANEL_ID, "", "", True, False, self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_X], self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_Y], self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_WIDTH], self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_EMPTY)
		screen.attachListBoxGFC( MERCENARY_INFORMATION_DETAILS_PANEL_ID, MERCENARY_INFORMATION_DETAILS_LIST_ID, "", TableStyles.TABLE_STYLE_EMPTY )
		screen.enableSelect(MERCENARY_INFORMATION_DETAILS_LIST_ID, False)

                #Rhye - start Carthaginian UP
		# Build the mercenary hire cost string
		#strHCost = u"%d%c" %(mercenary.getHireCost(), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
		strHCost = u"%d%c" %(mercenary.getHireCostXPlayer(gc.getGame().getActivePlayer()), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
		#Rhye - end UP

                #Rhye - start Carthaginian UP
		# Build the mercenary maintenance cost string
		#strMCost = u"%d%c" %(mercenary.getMercenaryMaintenanceCost(), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
                strMCost = u"%d%c" %(mercenary.getMercenaryMaintenanceCostXPlayer(gc.getGame().getActivePlayer()), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
                #Rhye - end UP
		
		# Build the mercenary XP string
		strXP = u"%d/%d" %(mercenary.getExperienceLevel(), mercenary.getNextExperienceLevel())

		# Build the unit stats string
		strStats = u"%d%c    %d%c" %(mercenary.getUnitInfo().getCombat(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR),mercenary.getUnitInfo().getMoves(),CyGame().getSymbolID(FontSymbols.MOVES_CHAR))

		screen.appendListBoxString( MERCENARY_INFORMATION_DETAILS_LIST_ID, mercenary.getName(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		#screen.appendListBoxString( MERCENARY_INFORMATION_DETAILS_LIST_ID, "  Unit Type: " + mercenary.getUnitInfo().getDescription(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY ) #Rhye
		screen.appendListBoxString( MERCENARY_INFORMATION_DETAILS_LIST_ID, "  Level: " + str(mercenary.getLevel()) + "     XP: " + strXP, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString( MERCENARY_INFORMATION_DETAILS_LIST_ID, "  " + strStats, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString( MERCENARY_INFORMATION_DETAILS_LIST_ID, "  ", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString( MERCENARY_INFORMATION_DETAILS_LIST_ID, "  Hire Cost: " + strHCost, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Show the mercenary costs if it is in the game			
		if(mercenary.isPlaced()):
			screen.appendListBoxString( MERCENARY_INFORMATION_DETAILS_LIST_ID, "  Maint. Cost: " + strMCost, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
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
			screen.appendListBoxString( MERCENARY_INFORMATION_DETAILS_LIST_ID, "  " + strPlacement, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		
		# Get the promotion list for the mercenary
		promotionList = mercenary.getCurrentPromotionList()

		screen.attachMultiListControlGFC(MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_ID, MERCENARY_INFORMATION_PROMOTION_LIST_CONTROL_ID, "", 1, 64, 64, TableStyles.TABLE_STYLE_STANDARD)

		# Add all of the promotions the mercenary has.
		for promotion in promotionList:
			screen.appendMultiListButton( MERCENARY_INFORMATION_PROMOTION_LIST_CONTROL_ID, promotion.getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, gc.getInfoTypeForString(promotion.getType()), -1, false )
			
		screen.addUnitGraphicGFC(MERCENARIES_UNIT_GRAPHIC, mercenary.getUnitInfoID(), self.screenWidgetData[MERCENARY_ANIMATION_X], self.screenWidgetData[MERCENARY_ANIMATION_Y], self.screenWidgetData[MERCENARY_ANIMATION_WIDTH], self.screenWidgetData[MERCENARY_ANIMATION_HEIGHT], WidgetTypes.WIDGET_GENERAL, -1, -1, self.screenWidgetData[MERCENARY_ANIMATION_ROTATION_X], self.screenWidgetData[MERCENARY_ANIMATION_ROTATION_Z], self.screenWidgetData[MERCENARY_ANIMATION_SCALE], True)

	
	# Draws the gold information in the "Mercenary Manager" screens
	def drawGoldInformation(self, screen):
	
		iCost = 0
		strCost = ""		
		
		# Get the players current gold text		
		szText = self.getGoldText(gc.getGame().getActivePlayer())
		screen.setLabel( "GoldText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 12, 6, -1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.show( "GoldText" )
		screen.moveToFront( "GoldText" )

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
		screen.setText(MERCENARIES_TEXT_PANEL_ID, "Background", self.screenWidgetData[MERCENARIES_TEXT_PANEL], CvUtil.FONT_LEFT_JUSTIFY, self.screenWidgetData[MERCENARIES_TEXT_PANEL_X], self.screenWidgetData[MERCENARIES_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		# Commented out due to mercenary groups not being implemented yet.
		# screen.setText(MERCENARY_GROUPS_TEXT_PANEL_ID, "Background", self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL], CvUtil.FONT_LEFT_JUSTIFY, self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL_X], self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setText(EXIT_TEXT_PANEL_ID, "Background", self.screenWidgetData[EXIT_TEXT_PANEL], CvUtil.FONT_RIGHT_JUSTIFY, self.screenWidgetData[EXIT_TEXT_PANEL_X], self.screenWidgetData[EXIT_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )


	# Draws the mercenary groups screen content	
	def drawMercenaryGroupsScreenContent(self, screen):
	
		# Draw the top bar
		self.drawScreenTop(screen)

		# Draw the bottom bar
		self.drawScreenBottom(screen)

		screen.addPanel(AVAILABLE_MERCENARY_GROUPS_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_X], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_Y], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_X], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_Y], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)
		screen.addPanel(AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(AVAILABLE_MERCENARY_GROUPS_TEXT_PANEL_ID, "Background", self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_PANEL_X], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addPanel(HIRED_MERCENARY_GROUPS_PANEL_ID, "", "", True, True, self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_X], self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_Y], self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_WIDTH], self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(HIRED_MERCENARY_GROUPS_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_X], self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_Y], self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_WIDTH], self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)
		screen.addPanel(HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(HIRED_MERCENARY_GROUPS_TEXT_PANEL_ID, "Background", self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_PANEL_X], self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addPanel(MERCENARY_GROUP_INFORMATION_PANEL_ID, "", "", True, True, self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_X], self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_Y], self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_WIDTH], self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(MERCENARY_GROUP_INFORMATION_TEXT_PANEL_ID, "Background", self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_PANEL_X], self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.showWindowBackground(False)
	

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

		screen.addPanel(MERCENARY_INFORMATION_PANEL_ID, "", "", True, True, self.screenWidgetData[MERCENARY_INFORMATION_PANEL_X], self.screenWidgetData[MERCENARY_INFORMATION_PANEL_Y], self.screenWidgetData[MERCENARY_INFORMATION_PANEL_WIDTH], self.screenWidgetData[MERCENARY_INFORMATION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(MERCENARY_INFORMATION_TEXT_PANEL_ID, "Background", self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL_X], self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				
		screen.showWindowBackground(False)

		# Populate the available mercenaries panel
		self.populateAvailableColonistsPanel(screen)

		# Populate the hired mercenaries panel
		self.populateAvailableExpeditionariesPanel(screen)


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
		elif(iDelta < 0):
			strDelta = u"%s" %(localText.changeTextColor(" ("+str(iDelta)+"/Turn)",gc.getInfoTypeForString("COLOR_RED")))
		
		return strGoldText + strDelta
	
	# Hires a mercenary for a player
	def hireMercenary(self, screen, mercenaryName):

		# Get the active player ID
		iPlayer = gc.getGame().getActivePlayer()

		# Hire the mercenary for the player
		objMercenaryUtils.hireMercenary(mercenaryName,iPlayer) 

		# Get all of the available mercenaries for hire
		mercenaries = objMercenaryUtils.getAvailableColonists(iPlayer)
		i = 0

		# Add the padding to the available mercenaries panel to improve the look of the screen
		if((4-len(mercenaries))>0):
			for i in range(4-len(mercenaries)):
				screen.attachPanel(AVAILABLE_COLONISTS_INNER_PANEL_ID, "dummyPanelHire"+str(i), "", "", True, False, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachLabel( "dummyPanelHire"+str(i), "", "     ")
				screen.attachLabel( "dummyPanelHire"+str(i), "", "     ")
				screen.attachLabel( "dummyPanelHire"+str(i), "", "     ")
				
		# Draw the gold information for the screen
		self.drawGoldInformation(screen)

		# Update the available mercenaries in the available mercenaries panel
		self.updateAvailableColonists(screen)
		self.updateAvailableExpeditionaries(screen)

		# Clear the information in the mercenary information panel
		self.clearMercenaryInformation(screen)
				
	# Updates the available mercenaries panel, displays the hire button to the 
	# player only for the mercenaries they can hire.
	def updateAvailableColonists(self, screen):
	
		# Get the ID for the current player
		iPlayer = gc.getGame().getActivePlayer()
		
		# Get the mercenaries available for hire
		colonists = objMercenaryUtils.getAvailableColonists(iPlayer)
		
		# Get the actual player
		player = gc.getPlayer(iPlayer)
		
		# Get the current gold for the player
		currentGold = player.getGold()

		# Go through each of the available mercenaries
		for mercenaryName in colonists:

			mercenary = colonists[mercenaryName]
			
			mercenaryName = str(mercenaryName)
			
			# Continue if the mercenary was built by the current player
			if(mercenary.iBuilder == iPlayer):
				continue

			# Delete the hire button for the current mercenary we are processing.
			screen.deleteWidget(mercenaryName+"_HireButton")

			# To start off we'll assume that the player can hire the mercenary
			bEnableHireMercenary = true

			# If the player doesn't have enough money to hire the mercenary then
			# we won't allow them to hire the current mercenary being processed.
			if(	(currentGold-mercenary.getHireCost()) <= 0):
				bEnableHireMercenary = false
			
			# Check if unit can spawn
			if not mercenary.hasValidSpawnTile(iPlayer):
				bEnableHireMercenary = False

			if(bEnableHireMercenary):
				screen.attachPanel(mercenaryName, mercenaryName+"hireButtonPanel", "", "", False, True, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachImageButton( mercenaryName, mercenaryName+"_HireButton", 
											"Art/Interface/Buttons/Actions/Join.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
		
	# Updates the available mercenaries panel, displays the hire button to the 
	# player only for the mercenaries they can hire.
	def updateAvailableExpeditionaries(self, screen):
	
		# Get the ID for the current player
		iPlayer = gc.getGame().getActivePlayer()
		
		# Get the mercenaries available for hire
		expeditionaries = objMercenaryUtils.getAvailableExpeditionaries(iPlayer)
		
		# Get the actual player
		player = gc.getPlayer(iPlayer)
		
		# Get the current gold for the player
		currentGold = player.getGold()

		# Go through each of the available mercenaries
		for mercenaryName in expeditionaries:

			mercenary = expeditionaries[mercenaryName]
			
			mercenaryName = str(mercenaryName)
			
			# Continue if the mercenary was built by the current player
			if(mercenary.iBuilder == iPlayer):
				continue

			# Delete the hire button for the current mercenary we are processing.
			screen.deleteWidget(mercenaryName+"_HireButton")

			# To start off we'll assume that the player can hire the mercenary
			bEnableHireMercenary = true

			# If the player doesn't have enough money to hire the mercenary then
			# we won't allow them to hire the current mercenary being processed.
			if(	(currentGold-mercenary.getHireCost()) <= 0):
				bEnableHireMercenary = false
			
			# Check if unit can spawn
			if not mercenary.hasValidSpawnTile(iPlayer):
				bEnableHireMercenary = False

			if(bEnableHireMercenary):
				screen.attachPanel(mercenaryName, mercenaryName+"hireButtonPanel", "", "", False, True, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachImageButton( mercenaryName, mercenaryName+"_HireButton", 
											"Art/Interface/Buttons/Actions/Join.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
	
	# Handles the input to the mercenary manager screens
	def handleInput (self, inputClass):

		# Get the instance of the screen
		screen = self.getScreen()

		# Debug code - start
		if(g_bDebug):
			screen.setText( "TopPanelDebugMsg", "TopPanel", inputClass.getFunctionName()
						, CvUtil.FONT_RIGHT_JUSTIFY, 1010, 20, -10, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		# Debug code - end
		
		# Get the data
		theKey = int(inputClass.getData())

		# If the escape key was pressed then set the current screen to mercenary manager
		if (inputClass.getNotifyCode() == self.EventKeyDown and theKey == int(InputTypes.KB_ESCAPE)):
			self.currentScreen = MERCENARY_MANAGER

		# If the exit text was pressed then set the current screen to mercenary manager.
		if(inputClass.getFunctionName() == EXIT_TEXT_PANEL_ID):
			self.currentScreen = MERCENARY_MANAGER
		
		# If the mercenaries text was pressed and we aren't currently looking at 
		# the main mercenaries manager screen then set the current screen to 
		# mercenaries manager, hide the screen and redraw the screen.
		if(inputClass.getFunctionName() == MERCENARIES_TEXT_PANEL_ID and self.currentScreen != MERCENARY_MANAGER):
			self.currentScreen = MERCENARY_MANAGER
			self.hideScreen()
			self.interfaceScreen()
			return

		# If the mercenary groups text was pressed and we aren't currently looking 
		# at the mercenary groups screen then set the current screen to 
		# mercenary groups, hide the screen and redraw the screen.		
		if(inputClass.getFunctionName() == MERCENARY_GROUPS_TEXT_PANEL_ID and self.currentScreen != MERCENARY_GROUPS_MANAGER):
			self.currentScreen = MERCENARY_GROUPS_MANAGER
			self.hideScreen()
			self.interfaceScreen()
			return

		# If someone pressed one of the buttons in the screen then handle the
		# action
		if(inputClass.getFunctionName().endswith("Button")):
			# Split up the function name into the mercenary name and the actual
			# action that was performed
			mercenaryName, function = inputClass.getFunctionName().split("_")
			
			self.screenFunction = function
			self.mercenaryName = None

			# If the function was find, then close the screen and find the unit
			if(function == "FindButton"):
				mercenaryName, unitID  = mercenaryName.split("-")

				# Convert the unit ID string back into a number
				unitID = self.alphaToNumber(unitID)

				# Get the player ID
				iPlayer = gc.getGame().getActivePlayer()

				# Get the actual player reference
				player = gc.getPlayer(iPlayer)

				# Get the actual unit in the game
				objUnit = player.getUnit(unitID)

				# If the unit is not set to None then look at them and select
				# them.
				if(objUnit != None):
					CyCamera().LookAtUnit(objUnit)
					if(not CyGame().isNetworkMultiPlayer()):
						CyInterface().selectUnit(objUnit, true, false, false)

				self.currentScreen = MERCENARY_MANAGER
	
				return
				
			# If the function was hire, then hire the mercenary
			if(function == "HireButton"):
				self.hireMercenary(screen, mercenaryName) 

			# If the function was fire, then fire the mercenary
			if(function == "FireButton"):
				self.fireMercenary(screen, mercenaryName) 

			# If the function was show information then populate the
			# mercenary/unit information
			if(function == "UnitInfoButton"):
			
				# Get the player ID
				iPlayer = gc.getGame().getActivePlayer()

				# Get the actual player reference
				player = gc.getPlayer(iPlayer)

				# Split up the mercenary name into the actual mercenary name
				# and the unit ID string
				mercenaryName, id  = mercenaryName.split("-")

				# Convert the unit ID string back into a number
				id = self.alphaToNumber(id)
				
				# Get the mercenary 
				mercenary = objMercenaryUtils.getMercenary(mercenaryName)

				# If we didn't get a mercenary from the mercenary pool then
				# it is safe to assume that the unit has never been a 
				# mercenary.
				if(mercenary == None):
					
					# Create a blank mercenary
					mercenary = objMercenaryUtils.createBlankMercenary()

					# Populate the mercenary object with the data from 
					# the unit that we want to look at
					mercenary.loadUnitData(player.getUnit(id))
					mercenary.setName(mercenaryName)
					
				# Calculate the screen information
				self.calculateScreenWidgetData(screen)

				# Populate the unit information panel with the mercenary/unit
				# information.
				self.populateUnitInformation(screen,mercenary)					

										
			# If the function was to show the mercenary information then 
			# populate the mercenary information panel.
			if(function == "InfoButton"):
			
				self.mercenaryName = mercenaryName
			
				# If the mercenary name was actually set then get their 
				# information from the global mercenary pool.
				if(mercenaryName != None):
				
					# Get the mercenary from the global mercenary pool
					mercenary = objMercenaryUtils.getMercenary(mercenaryName)

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

		if(self.currentScreen == MERCENARY_MANAGER):
			strScreenTitle = localText.getText("TXT_KEY_MERCENARY_SCREEN_TITLE", ()).upper()
		elif(self.currentScreen == MERCENARY_GROUPS_MANAGER):
			strScreenTitle = localText.getText("TXT_KEY_MERCENARY_GROUPS_SCREEN_TITLE", ()).upper()
			
		# Screen title panel information
		self.screenWidgetData[SCREEN_TITLE_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH]
		self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] = 55
		self.screenWidgetData[SCREEN_TITLE_PANEL_X] = 0
		self.screenWidgetData[SCREEN_TITLE_PANEL_Y] = 0
		self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL] = u"<font=4b>" + localText.getText("TXT_KEY_MERCENARIES_SCREEN_TITLE", ()).upper() + ": " + strScreenTitle + "</font>"
		self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_X] = self.screenWidgetData[SCREEN_WIDTH]/2
		self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_Y] = 8


		# Exit panel information		
		self.screenWidgetData[BOTTOM_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH]
		self.screenWidgetData[BOTTOM_PANEL_HEIGHT] = 55
		self.screenWidgetData[BOTTOM_PANEL_X] = 0
		self.screenWidgetData[BOTTOM_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 55

		self.screenWidgetData[MERCENARIES_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_MERCENARY_SCREEN_TITLE", ()).upper() + "</font>"
		self.screenWidgetData[MERCENARIES_TEXT_PANEL_X] = 30
		self.screenWidgetData[MERCENARIES_TEXT_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 42

		self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_MERCENARY_GROUPS_SCREEN_TITLE", ()).upper() + "</font>"
		self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL_X] = 220
		self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 42

		self.screenWidgetData[EXIT_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"
		self.screenWidgetData[EXIT_TEXT_PANEL_X] = self.screenWidgetData[SCREEN_WIDTH] - 30
		self.screenWidgetData[EXIT_TEXT_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 42

		
		# Available Colonists panel information
		self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_WIDTH] = 450
		self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*3) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))/2
		self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_X] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_X] + (4*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_Y] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_Y] + (10*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_WIDTH] - (8*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_COLONISTS_INNER_PANEL_HEIGHT] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_HEIGHT] - (14*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_WIDTH] - (self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_AVAILABLE_COLONISTS", ()) + "</font>"
		self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_PANEL_X] = self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_PANEL_Y] = self.screenWidgetData[AVAILABLE_COLONISTS_TEXT_BACKGROUND_PANEL_Y] + 4		
		
		
		# Available Expeditionaries panel information
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_Y] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_Y] + self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_WIDTH] = 450
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*3) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))/2
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_INNER_PANEL_X] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_X] + (4*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_INNER_PANEL_Y] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_Y] + (10*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_INNER_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_WIDTH] - (8*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_INNER_PANEL_HEIGHT] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_HEIGHT] - (14*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_PANEL_WIDTH] - (self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_AVAILABLE_EXPEDITIONARIES", ()) + "</font>"
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_PANEL_X] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_PANEL_Y] = self.screenWidgetData[AVAILABLE_EXPEDITIONARIES_TEXT_BACKGROUND_PANEL_Y] + 4
		
		
		# Mercenary information panel information
		self.screenWidgetData[MERCENARY_INFORMATION_PANEL_X] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_X] + self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_X] + self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[MERCENARY_INFORMATION_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*2) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))
		self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[MERCENARY_INFORMATION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[MERCENARY_INFORMATION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[MERCENARY_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*6)
		self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_MERCENARY_INFORMATION", ()) + "</font>"
		self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL_X] = self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL_Y] = self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_Y] + 4
		
		self.screenWidgetData[MERCENARY_ANIMATION_X] = self.screenWidgetData[MERCENARY_INFORMATION_PANEL_X]+20
		self.screenWidgetData[MERCENARY_ANIMATION_Y] = self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL_Y]+40
		self.screenWidgetData[MERCENARY_ANIMATION_WIDTH] = 303
		self.screenWidgetData[MERCENARY_ANIMATION_HEIGHT] = 200
		self.screenWidgetData[MERCENARY_ANIMATION_ROTATION_X] = -20
		self.screenWidgetData[MERCENARY_ANIMATION_ROTATION_Z] = 30
		self.screenWidgetData[MERCENARY_ANIMATION_SCALE] = 1.0
		
		self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_X] = self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_X]
		self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_Y] = self.screenWidgetData[MERCENARY_ANIMATION_Y] + self.screenWidgetData[MERCENARY_ANIMATION_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[MERCENARY_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*18)
		self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_HEIGHT] = 128 + (self.screenWidgetData[BORDER_WIDTH]*9)

		self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_X] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_Y] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_HEIGHT] - (self.screenWidgetData[BORDER_WIDTH]*2)

		self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_X] = self.screenWidgetData[MERCENARY_ANIMATION_X] + self.screenWidgetData[MERCENARY_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_Y] = self.screenWidgetData[MERCENARY_ANIMATION_Y]
		self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[MERCENARY_ANIMATION_X] + self.screenWidgetData[MERCENARY_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH])*6)
		self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_HEIGHT] = self.screenWidgetData[MERCENARY_ANIMATION_HEIGHT]


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
		self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_X] = self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_X]
		self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_Y] = self.screenWidgetData[MERCENARY_ANIMATION_Y] + self.screenWidgetData[MERCENARY_ANIMATION_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[MERCENARY_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*18)
		self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_HEIGHT] = 128 + (self.screenWidgetData[BORDER_WIDTH]*9)

		self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_X] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_Y] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_HEIGHT] - (self.screenWidgetData[BORDER_WIDTH]*2)

		self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_X] = self.screenWidgetData[MERCENARY_ANIMATION_X] + self.screenWidgetData[MERCENARY_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_Y] = self.screenWidgetData[MERCENARY_ANIMATION_Y]
		self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[MERCENARY_ANIMATION_X] + self.screenWidgetData[MERCENARY_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH])*6)
		self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_HEIGHT] = self.screenWidgetData[MERCENARY_ANIMATION_HEIGHT]
		# Available mercenary groups panel information
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_WIDTH] = 450
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*3) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))/2
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_X] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_X] + (4*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_Y] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_Y] + (10*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_WIDTH] - (8*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_HEIGHT] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_HEIGHT] - (14*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_WIDTH] - (self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_AVAILABLE_MERCENARY_GROUPS", ()) + "</font>"
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_PANEL_X] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_PANEL_Y] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_Y] + 4		
		
		
		# Hired mercenary groups panel information
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_Y] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_Y] + self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_WIDTH] = 450
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*3) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))/2
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_X] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_X] + (4*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_Y] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_Y] + (10*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_WIDTH] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_WIDTH] - (8*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_HEIGHT] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_HEIGHT] - (14*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_WIDTH] - (self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_HIRED_MERCENARY_GROUPS", ()) + "</font>"
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_PANEL_X] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_PANEL_Y] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_Y] + 4

		# Mercenary groups information panel information
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_X] = self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_X] + self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_X] + self.screenWidgetData[AVAILABLE_COLONISTS_PANEL_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*2) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*6)
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_MERCENARY_GROUP_INFORMATION", ()) + "</font>"
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_PANEL_X] = self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_PANEL_Y] = self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_Y] + 4


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

	#Mercenaries - start
	global objMercenaryUtils        
	objMercenaryUtils = MercenaryUtils.MercenaryUtils()
	#Mercenaries - end
	
	return 0


# This method creates a new instance of the MercenaryUtils class to be used later
@handler("OnLoad")
def onLoadGame():
	if (gc.getGame().getGameTurn() >= dBirth[active()]): #Rhye
		global objMercenaryUtils
		objMercenaryUtils = MercenaryUtils.MercenaryUtils()

@handler("BeginPlayerTurn")
def onBeginPlayerTurn(iGameTurn, iPlayer):        

	#Mercenaries - start

	# This method will display the mercenary manager screen
	# and provide the logic to make the computer players think.
	player = gc.getPlayer(iPlayer)

	if (gc.getGame().getGameTurn() >= dBirth[active()]): #Rhye

		# Debug code - start
		if(g_bDebug):
			CvUtil.pyPrint(player.getName() + " Gold: " + str(player.getGold()) + " is human: " + str(player.isHuman()))
		# Debug code - end        

		# if g_bDisplayMercenaryManagerOnBeginPlayerTurn is true the the player is human
		# then display the mercenary manager screen
		if(g_bDisplayMercenaryManagerOnBeginPlayerTurn and player.isHuman()):
			self.mercenaryManager.interfaceScreen()

		# if the player is not human then run the think method
		if(not player.isHuman()):
			
			#Rhye - start
			#objMercenaryUtils.computerPlayerThink(iPlayer)                                        
			if (player.isAlive()):
				if (iPlayer % (g_bAIThinkPeriod) == iGameTurn % (g_bAIThinkPeriod)):
					print ("AI thinking (Mercenaries)", iPlayer) #Rhye
					objMercenaryUtils.computerPlayerThink(iPlayer)                                                                
			#Rhye - end


