#
# ImmigrationAI
# MacAurther: computer player policy for hiring, converting, and transporting
# immigrants.
#

from CvPythonExtensions import *
from Consts import *
from Core import *
import ImmigrantPool
import Immigrants
import Immigration
import Hiring
from Events import handler

gc = CyGlobalContext()

# Set to true to print out debug messages in the logs
g_bDebug = False

# AI think cadence (1 = every player, every turn)
g_bAIThinkPeriod = 1


# Performs the thinking for the computer players in regards to the mercenaries mod functionality.
# It will:
# 	- Load earned units on waiting ships
#   - Exchange Immigrants for Settlers, Workers, etc.
# It will not:
#	- Hire additional military units
def computerPlayerThink(iPlayer):
	# Get the player
	pPlayer = gc.getPlayer(iPlayer)

	# Return immediately if the player is a filthy human :p
	if pPlayer.isHuman():
		return

	# Return immediately if the player is a barbarian, independent, or native
	if pPlayer.isBarbarian() or pPlayer.isIndependent() or pPlayer.isNative():
		return

	# Return immediately if the player cannot earn immigrants
	if not Immigration.canEarnImmigrants(iPlayer):
		return

	# Compute want-flags once to avoid repeated full unit-list scans
	bWantsSettlers     = computerPlayerWantsSettlers(iPlayer)
	bWantsWorkers      = computerPlayerWantsWorkers(iPlayer)
	bWantsMissionaries = computerPlayerWantsMissionaries(iPlayer)
	bWantsImmigrants   = not bWantsSettlers and not bWantsWorkers and not bWantsMissionaries

	# Convert earned Immigrants into other units
	for iHomeland in lHomelands:
		computerPlayerHireImmigrants(iPlayer, iHomeland, bWantsSettlers, bWantsWorkers, bWantsMissionaries)
		if iHomeland == iHomelandAfrica:
			computerPlayerHireSlaves(iPlayer)

	# Load waiting units
	for iHomeland in lHomelands:
		computerPlayerLoadHomeland(iPlayer, iHomeland, bWantsImmigrants)

	if g_bDebug:
		print(pPlayer.getName() + " has the following earned immigrants:")
		for iHomeland in lHomelands:
			if ImmigrantPool.getTotalNumImmigrants(iPlayer, iHomeland) > 0:
				print("Homeland: " + str(iHomeland))
				pool = ImmigrantPool.getEarnedImmigrants(civ(iPlayer), iHomeland)
				for iUnit, iCount in pool.items():
					if iCount > 0:
						print(Immigrants.getTitle(iUnit, iCount))

def computerPlayerHireImmigrants(iPlayer, iHomeland, bWantsSettlers, bWantsWorkers, bWantsMissionaries):
	# Priority: Settlers, Workers, then Missionaries
	# Try to hire, if didn't work, just continue on
	if bWantsSettlers:
		Hiring.hireMercenary(unique_unit(iPlayer, iSettler), iPlayer, iHomeland, bPay=True)
	if bWantsWorkers:
		Hiring.hireMercenary(unique_unit(iPlayer, iWorker), iPlayer, iHomeland, bPay=True)
	if bWantsMissionaries:
		Hiring.hireMercenary(unique_unit(iPlayer, missionary(player(iPlayer).getStateReligion())), iPlayer, iHomeland, bPay=True)
	# TODO: if AI is extended to hire mercenaries, call Immigration.getAvailableMercenaries(iPlayer, iHomeland)
	# here — it already enforces the tradewind discovery gate via hasDiscoveredTradewind.

def computerPlayerHireSlaves(iPlayer):
	if computerPlayerWantsSlaves(iPlayer):
		Hiring.hireMercenary(iChattleSlave, iPlayer, iHomelandAfrica, bPay=True)

def computerPlayerLoadHomeland(iPlayer, iHomeland, bWantsImmigrants):
	pool = ImmigrantPool.getEarnedImmigrants(civ(iPlayer), iHomeland)
	for iUnit, iCount in list(pool.items()):
		# Heuristic: Don't load any Immigrants unless you don't want any more settlers, workers, or missionaries
		if iUnit == iImmigrant and not bWantsImmigrants:
			continue
		if iCount > 0:
			for _ in range(iCount):
				if Immigrants.hasShipForPlacement(iPlayer, iHomeland):
					Hiring.placeMercenary(iUnit, iPlayer, iHomeland)
				else:
					return

def computerPlayerWantsImmigrants(iPlayer):
	return (not computerPlayerWantsSettlers(iPlayer)) and \
		   (not computerPlayerWantsMissionaries(iPlayer)) and \
		   (not computerPlayerWantsWorkers(iPlayer))	# Evaluate workers last since it'll probably take the longest and there's a chance to escape earlier

def computerPlayerWantsSettlers(iPlayer):
	# Wants no more than 1 settler
	for unit in units.owner(iPlayer):
		if unit.isFound():
			return False
	return True

def computerPlayerWantsWorkers(iPlayer):
	# Wants no more than 1 worker per city
	iNumWorkers = 0
	for unit in units.owner(iPlayer):
		if base_unit(unit) in [iWorker, iLaborer]:
			iNumWorkers += 1
	return iNumWorkers < player(iPlayer).getNumCities()

def computerPlayerWantsMissionaries(iPlayer):
	# Doesn't want if no State religion
	if player(iPlayer).getStateReligion() == -1:
		return False
	# Wants no more than 1 missionary
	for unit in units.owner(iPlayer):
		if gc.getUnitInfo(unit.getUnitType()).getReligionSpreads(player(iPlayer).getStateReligion()) > 0:
			return False
	return True

def computerPlayerWantsSlaves(iPlayer):
	# Doesn't want if can't buy
	if not player(iPlayer).canBuySlaves():
		return False
	# Check if can hire
	if not Immigration.canHire(iChattleSlave, iPlayer, iHomelandAfrica):
		return False
	# Protect against Natives buying slaves they can't get
	if civ(iPlayer) in dCivGroups[iCivGroupNative]:
		return False
	# Don't hire crazy numbers of slaves
	iEarnedSlaves = ImmigrantPool.getNumImmigrants(iPlayer, iHomelandAfrica, iChattleSlave)
	if iEarnedSlaves > 0 and iEarnedSlaves < max(player(iPlayer).countRequiredSlaves(), 6):
		return False
	return True

def computerGetNumImmigrantsToTransport(iPlayer, iHomeland):
	bWantsImmigrants = computerPlayerWantsImmigrants(iPlayer)
	pool = ImmigrantPool.getEarnedImmigrants(civ(iPlayer), iHomeland)
	iNumUnitsToTransport = 0
	for iUnit in pool.keys():
		if bWantsImmigrants or iUnit != iImmigrant:
			iNumUnitsToTransport += 1
	return iNumUnitsToTransport


@handler("EndPlayerTurn")
def onEndPlayerTurn(iGameTurn, iPlayer):
	pPlayer = gc.getPlayer(iPlayer)

	if pPlayer != None and Immigration.canEarnImmigrants(iPlayer):
		# Process new immigrants
		Immigration.processImmigration(iPlayer)

		# if the player is not human and not independent then run the think method
		if not pPlayer.isHuman() and civ(iPlayer) < iIndependent1:
			if pPlayer.isAlive():
				if iPlayer % (g_bAIThinkPeriod) == iGameTurn % (g_bAIThinkPeriod):
					computerPlayerThink(iPlayer)
