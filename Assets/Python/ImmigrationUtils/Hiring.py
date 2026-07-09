#
# Hiring
# MacAurther: hire/place transactions for immigrants and mercenaries.
#

from CvPythonExtensions import *
from Consts import *
from Core import *
import ImmigrantPool
import Immigrants

gc = CyGlobalContext()

# Set to true to print out debug messages in the logs
g_bDebug = False


def hireMercenary(iUnit, iPlayer, iHomeland, bPay=True, bImmediate=False):
	' returns true if the unit was successfully hired'

	if iUnit == -1:
		return False

	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isAlive():
		return False

	iImmigrationCost, iGoldCost = Immigrants.getHireCost(iUnit, iPlayer)

	if bPay and not Immigrants.canAfford(iUnit, iPlayer, iHomeland):
		return False

	# Ships need a valid starting plot before they can be hired at all
	if Immigrants.isShip(iUnit):
		if Immigrants.getStartingLocation(iUnit, iPlayer, iHomeland) is None:
			return False

	if bPay:
		ImmigrantPool.changeImmigrants(iPlayer, iHomeland, iImmigrant, -iImmigrationCost)
		pPlayer.setGold(pPlayer.getGold() - iGoldCost)

	# Place immediately if ship or force immediate with space, otherwise add to earned Immigrants
	if Immigrants.isShip(iUnit) or (bImmediate and Immigrants.hasShipForPlacement(iPlayer, iHomeland)):
		placeMercenary(iUnit, iPlayer, iHomeland, bImmediate)
	else:
		# If not placed, add to earned immigrants list
		ImmigrantPool.changeImmigrants(iPlayer, iHomeland, iUnit, 1)

	if g_bDebug:
		print(pPlayer.getName() + " | Current Gold: " + str(pPlayer.getGold()) + " | Current Immigrants: " + str(ImmigrantPool.getNumImmigrants(iPlayer, iHomeland, iImmigrant)) + " | Hired " + Immigrants.getName(iUnit) + " for " + str(iImmigrationCost) + " immigration and " + str(iGoldCost) + " gold.")

	return True

def placeMercenary(iUnit, iPlayer, iHomeland, bImmediate=False):
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isAlive():
		return False

	# Reduce earned units by 1 if not a ship and not immediate
	if not Immigrants.isShip(iUnit) and not bImmediate:
		ImmigrantPool.changeImmigrants(iPlayer, iHomeland, iUnit, -1)

	# If unit is Mercenary and placed while AI owner is at war with another player, make it aggressive
	bAggressive = not pPlayer.isHuman() and team(iPlayer).getAtWarCount(True)

	Immigrants.spawnUnit(iUnit, iPlayer, iHomeland, bAggressive)
