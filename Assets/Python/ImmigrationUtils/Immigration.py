#
# Immigration
# MacAurther: earning mechanics (thresholds, immigrant grants, tradewind discovery)
# and hire availability.
#

from CvPythonExtensions import *
from Consts import *
from StoredData import data
from Core import *
from Civics import *
import ImmigrantPool

gc = CyGlobalContext()

dHomelandNames = {
	iHomelandNorthEurope: "North Europe",
	iHomelandSouthEurope: "South Europe",
	iHomelandAfrica: "Africa",
	iHomelandSiberia: "Siberia",
	iHomelandAsia: "Asia",
}


def getImmigrationThreshold(iPlayer, iHomeland):
	return int(calculateBaseImmigrationThreshold(iPlayer, iHomeland) * getHomelandImmigrationThresholdModifier(iPlayer, iHomeland))

def getHomelandImmigrationThresholdModifier(iPlayer, iHomeland):
	iModifier = 0

	# Civics
	if iPlayer == -1:
		bPenalColony = False
	else:
		# Get the actual current player object
		civics = Civics.player(iPlayer)
		bPenalColony = iPenalColony in civics
	if bPenalColony: iModifier -= 50

	# England UP:
	if civ(iPlayer) == iEngland and iHomeland == iHomelandNorthEurope:
		iModifier -= 50

	return max(100 + iModifier, 20) / 100.0

def calculateBaseImmigrationThreshold(iPlayer, iHomeland):
	iThreshold = 10
	iThreshold += data.civs[civ(iPlayer)].numImmigrations
	iThreshold += 2 * data.civs[civ(iPlayer)].lNumImmigrantsEared[iHomeland]
	return scale(iThreshold)

def canEarnImmigrants(iPlayer, iHomeland=-1):
	pPlayer = player(iPlayer)
	if iHomeland in [-1, None]:
		return any(gc.getTeam(pPlayer.getTeam()).isHasTech(iTech) for iTech in lImmigraitonTechs)
	return gc.getTeam(pPlayer.getTeam()).isHasTech(lImmigraitonTechs[iHomeland])

def getFirstOpenHomeland(iPlayer):
	for iHomeland in lHomelands:
		if canEarnImmigrants(iPlayer, iHomeland):
			return iHomeland

def processImmigration(iPlayer):
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)
	iBestHomeland = 0
	while iBestHomeland != -1:
		iBestHomeland = -1
		iBestThreshold = 0
		for iHomeland in lHomelands:
			if not canEarnImmigrants(iPlayer, iHomeland):
				continue
			iThreshold = getImmigrationThreshold(iPlayer, iHomeland)
			if pPlayer.getImmigration() < iThreshold:
				continue
			if iBestHomeland == -1:
				iBestHomeland = iHomeland
				iBestThreshold = iThreshold
			elif iBestThreshold > iThreshold:
				iBestHomeland = iHomeland
				iBestThreshold = iThreshold

		if iBestHomeland != -1:
			# Grant Immigrant
			ImmigrantPool.changeImmigrants(iPlayer, iBestHomeland, iImmigrant, 1)
			# Subtract cost
			pPlayer.changeImmigration(-1 * iBestThreshold)
			# Increment num immigrant trackers
			data.civs[iCiv].numImmigrations += 1
			data.civs[iCiv].lNumImmigrantsEared[iBestHomeland] += 1
			# Notify player (if human)
			if pPlayer.isHuman():
				strMessage = "A new Immigrant is waiting on the docks of " + dHomelandNames[iBestHomeland] + "!"
				CyInterface().addMessage(iPlayer, False, 20, strMessage, "AS2D_IMMIGRANTEARNED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, "", gc.getInfoTypeForString("COLOR_YELLOW"), -1, -1, False, False)

def hasDiscoveredTradewind(iPlayer, iHomeland):
	iCiv = civ(iPlayer)
	if data.civs[iCiv].lTradewindDiscovered[iHomeland]:
		return True  # cached — skip the scan
	iTeam = player(iPlayer).getTeam()
	iTradewindFeature = iTradeWindsStart + iHomeland
	for plot in plots.all():
		if plot.isRevealed(iTeam, False) and plot.getFeatureType() == iTradewindFeature:
			data.civs[iCiv].lTradewindDiscovered[iHomeland] = True
			return True
	return False

# Returns {iUnit: iCount} for units available given a homeland and date.
# iCount is always 1 today (a unit is either available or it isn't); this is where
# a future limited-mercenary-stock system would report remaining supply instead.
def getAvailableUnit(iPlayer, iHomeland, dSchedule):
	dUnits = {}
	iCurrentTurn = turn()

	for iUnit in dSchedule.keys():
		if not iHomeland in dSchedule[iUnit][1]:
			continue
		iYearStart = year(dSchedule[iUnit][0][0])
		iYearEnd   = year(dSchedule[iUnit][0][1])
		if not (iYearStart <= iCurrentTurn <= iYearEnd):
			continue
		if not canHire(iUnit, iPlayer, iHomeland):
			continue
		if unique_unit(iPlayer, iUnit) != iUnit and not iUnit in lUniqueOverride:
			continue
		dUnits[iUnit] = 1

	return dUnits

# Extra check for special can hire cases
def canHire(iUnit, iPlayer, iHomeland):
	# slaves available unless player runs a civic with bNoSlavery
	if iUnit == iChattleSlave and gc.getPlayer(iPlayer).isNoSlavery():
		return False
	return True

# Returns a list of available immigrants given a homeland and date
def getAvailableImmigrants(iPlayer, iHomeland):
	return getAvailableUnit(iPlayer, iHomeland, dImmigrantSchedule)

# Returns a list of available mercenaries given a homeland and date.
# Requires the player to have revealed at least one tradewind tile for that homeland.
def getAvailableMercenaries(iPlayer, iHomeland):
	if not hasDiscoveredTradewind(iPlayer, iHomeland):
		return {}
	return getAvailableUnit(iPlayer, iHomeland, dMercenarySchedule)
