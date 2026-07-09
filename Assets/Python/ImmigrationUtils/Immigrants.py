#
# Immigrants
# MacAurther: replaces the old Mercenary class. Everything here is a function
# of iUnit (+ iPlayer/iHomeland where needed) computed on demand from the unit's
# XML data — there's no wrapper object rebuilt from scratch on every lookup.
#

from CvPythonExtensions import *
from Consts import *
from Core import *
from Civics import *
import PlayerUtil
import ImmigrantPool

gc = CyGlobalContext()


### CLASSIFICATION ###

def isShip(iUnit):
	return gc.getUnitInfo(iUnit).getDomainType() == DomainTypes.DOMAIN_SEA

def isMercenaryType(iUnit):
	return iUnit in dMercenarySchedule

def getName(iUnit):
	return str(gc.getUnitInfo(iUnit).getDescription())

def getTitle(iUnit, iCount=1):
	if iCount > 1:
		return getName(iUnit) + " (" + str(iCount) + ")"
	return getName(iUnit)

def getPromotions(iUnit):
	kUnit = gc.getUnitInfo(iUnit)
	lPromotions = [iPromo for iPromo in range(gc.getNumPromotionInfos()) if kUnit.getFreePromotions(iPromo)]
	if isMercenaryType(iUnit):
		lPromotions.append(gc.getInfoTypeForString("PROMOTION_MERCENARY"))
	return lPromotions

def getLevel(iUnit):
	return len(getPromotions(iUnit))


### PRICING ###

# Base immigration-point cost per unit type. Units not listed here cost their
# production cost in gold instead (see getBaseHireCost).
dUnitImmigrationCost = {
	iSettler: 4,
	iDogSled: 4,
	iPioneer: 6,
	iWorker: 2,
	iPromyshlenniki: 2,
	iLaborer: 3,
	iTrackman: 1,
	iOrthodoxMiss: 1,
	iCatholicMiss: 1,
	iProtestantMiss: 1,
}

# Missionaries additionally cost gold on top of their immigration price
lMissionaryUnits = [iOrthodoxMiss, iCatholicMiss, iProtestantMiss]

def getBaseHireCost(iUnit):
	' returns (iImmigrationCost, iGoldCost) before civic modifiers '
	if iUnit in dUnitImmigrationCost:
		iGoldCost = 0
		if iUnit in lMissionaryUnits:
			iGoldCost = scale(10)
		return (dUnitImmigrationCost[iUnit], iGoldCost)
	return (0, gc.getUnitInfo(iUnit).getProductionCost())

def getHireCost(iUnit, iPlayer):
	' returns (iImmigrationCost, iGoldCost) '
	iImmigrationCost, iGoldCost = getBaseHireCost(iUnit)

	if iPlayer == -1:
		return (iImmigrationCost, iGoldCost)

	civics = Civics.player(iPlayer)
	kUnit = gc.getUnitInfo(iUnit)

	if iIndenturedServitude in civics and iUnit in [iWorker, iPromyshlenniki, iLaborer]:
		iImmigrationCost -= 1
	if iImmigrationCost > 0 and iDecolonization in civics:
		iImmigrationCost += 1
	if civ(iPlayer) == iNorse and iUnit == iSettler:	# Norse UP
		iImmigrationCost -= 1
	if iProprietors in civics and kUnit.getUnitCombatType() != UnitCombatTypes.NO_UNITCOMBAT and kUnit.getDomainType() == DomainTypes.DOMAIN_LAND:
		iGoldCost = iGoldCost * 4 / 5
	if iAdmiralty in civics and kUnit.getDomainType() == DomainTypes.DOMAIN_SEA:
		iGoldCost = iGoldCost * 3 / 4

	return (iImmigrationCost, iGoldCost)

def getHireCostString(iUnit, iPlayer):
	iImmigrationCost, iGoldCost = getHireCost(iUnit, iPlayer)
	strHCost = ""
	if iImmigrationCost > 0:
		strHCost += u"%d%c" % (iImmigrationCost, CyTranslator().getText("[ICON_IMMIGRANT]", ()))
	if iGoldCost > 0:
		strHCost += u"%d%c" % (iGoldCost, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
	return strHCost

def canAfford(iUnit, iPlayer, iHomeland):
	iImmigrationCost, iGoldCost = getHireCost(iUnit, iPlayer)
	iEarnedImmigrants = ImmigrantPool.getNumImmigrants(iPlayer, iHomeland, iImmigrant)
	bCanAffordImmigrants = iImmigrationCost == 0 or iImmigrationCost <= iEarnedImmigrants
	return iGoldCost <= gc.getPlayer(iPlayer).getGold() and bCanAffordImmigrants


### PLACEMENT ###

# Get the ship in which to place a hired land unit
def getPlacementShip(iPlayer, iHomeland):
	for pUnit in PlayerUtil.getPlayerUnits(iPlayer):
		if pUnit.plot().getFeatureType() - iTradeWindsStart == iHomeland:
			if not pUnit.isFull():
				return pUnit
	return None

# In order to place a hired land unit, the player must have a ship on the edge of the map
def hasShipForPlacement(iPlayer, iHomeland):
	return getPlacementShip(iPlayer, iHomeland) is not None

# Get the tile where hired ships appear
def getShipPlacementPlot(iPlayer, iHomeland):
	iCiv = civ(iPlayer)

	for x in range(iWorldX):
		pLoopPlot = plot(x, dCapitals[iCiv][1])
		if pLoopPlot.getFeatureType() - iTradeWindsStart == iHomeland:
			return pLoopPlot

	# If no plots were found that matched the given homeland at the latitude of the player's capital, return default
	return plot(dHomelandDefaultUnitSpawn[iHomeland])

def hasValidSpawnTile(iUnit, iPlayer, iHomeland):
	if isShip(iUnit):
		return getShipPlacementPlot(iPlayer, iHomeland) is not None
	if gc.getUnitInfo(iUnit).getDomainType() == DomainTypes.DOMAIN_LAND:
		return hasShipForPlacement(iPlayer, iHomeland)
	return False

def getStartingLocation(iUnit, iPlayer, iHomeland):
	if isShip(iUnit):
		return getShipPlacementPlot(iPlayer, iHomeland)
	if hasValidSpawnTile(iUnit, iPlayer, iHomeland):
		return getPlacementShip(iPlayer, iHomeland).plot()
	return None


### SPAWNING ###

def spawnUnit(iUnit, iPlayer, iHomeland, bAggressive=False):
	pPlot = getStartingLocation(iUnit, iPlayer, iHomeland)
	if pPlot is None:
		return None

	pPlayer = gc.getPlayer(iPlayer)
	objUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	objUnit.finishMoves()

	strMessage = getName(iUnit) + " has arrived"
	CyInterface().addMessage(iPlayer, False, 20, strMessage, "", 0, gc.getUnitInfo(iUnit).getButton(), ColorTypes(0), pPlot.getX(), pPlot.getY(), True, True)

	objUnit.setLevel(getLevel(iUnit))
	objUnit.setExperience(0, 0)
	objUnit.setName(getName(iUnit))

	if bAggressive:
		setAggressiveUnitAI(objUnit, iUnit)

	grantReadinessBonus(objUnit, iUnit, iPlayer)

	for iPromo in getPromotions(iUnit):
		objUnit.setHasPromotion(iPromo, True)

	return objUnit

def setAggressiveUnitAI(objUnit, iUnit):
	kUnit = gc.getUnitInfo(iUnit)
	if isShip(iUnit):
		if kUnit.getCargoSpace() > 0:
			objUnit.setUnitAIType(UnitAITypes.UNITAI_ASSAULT_SEA)
		else:
			objUnit.setUnitAIType(UnitAITypes.UNITAI_ESCORT_SEA)
	elif kUnit.getCombat() > 0:
		objUnit.setUnitAIType(UnitAITypes.UNITAI_ATTACK_CITY)

# Extra starting XP from civics that favor quick military integration of hired units
def grantReadinessBonus(objUnit, iUnit, iPlayer):
	civics = Civics.player(iPlayer)
	kUnit = gc.getUnitInfo(iUnit)
	iExp = 0

	# Conquest and Zealotry Civic
	if kUnit.getDomainType() == DomainTypes.DOMAIN_LAND and kUnit.getUnitCombatType() not in [UnitCombatTypes.NO_UNITCOMBAT, UnitCombatTypes.UNITCOMBAT_SPY]:
		if iConquest in civics or iImperialism in civics:
			iExp += 2
		if iPatronato in civics:
			iExp += 2

	# Admiralty Civic
	if iAdmiralty in civics and kUnit.getDomainType() == DomainTypes.DOMAIN_SEA:
		iExp += 4

	if iExp > 0:
		objUnit.changeExperience(iExp, -1, False, False, False)
