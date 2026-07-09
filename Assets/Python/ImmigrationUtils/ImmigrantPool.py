#
# ImmigrantPool
# MacAurther: inventory of earned units per civ and homeland. Plain
# {iUnit: iCount} dicts — no wrapper object; a count is just an int.
#

from CvPythonExtensions import *
from StoredData import data
from Core import *

gc = CyGlobalContext()


def changeImmigrants(iPlayer, iHomeland, iUnit, iChange):
	pool = data.civs[civ(iPlayer)].dEarnedUnits[iHomeland]
	iNewCount = pool.get(iUnit, 0) + iChange

	if iNewCount <= 0:
		if iUnit in pool:
			del pool[iUnit]
		return

	pool[iUnit] = iNewCount

def getTotalNumImmigrants(iPlayer, iHomeland):
	return sum(data.civs[civ(iPlayer)].dEarnedUnits[iHomeland].values())

def getNumImmigrants(iPlayer, iHomeland, iUnit):
	return data.civs[civ(iPlayer)].dEarnedUnits[iHomeland].get(iUnit, 0)

def getEarnedImmigrants(iCiv, iHomeland):
	return data.civs[iCiv].dEarnedUnits[iHomeland]

def getHasEarnedImmigrant(iCiv, iHomeland, iUnit):
	return getEarnedImmigrants(iCiv, iHomeland).get(iUnit, 0) > 0
