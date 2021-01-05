from Consts import *

# Peak that change to hills during the game, like Bogota
lPeakExceptions = [(31, 13), (32, 19), (27, 29), (88, 47), (40, 66)]

def isReborn(iPlayer):
	return gc.getPlayer(iPlayer).isReborn()
	
def getOrElse(dDictionary, key, default):
	if key in dDictionary: return dDictionary[key]
	return default
	
def getArea(iPlayer, tRectangle, dExceptions, bReborn=None, dChangedRectangle={}, dChangedExceptions={}):
	if bReborn is None: bReborn = isReborn(iPlayer)
	tBL, tTR = tRectangle[iPlayer]
	lExceptions = getOrElse(dExceptions, iPlayer, [])
	
	if bReborn:
		if iPlayer in dChangedRectangle:
			tBL, tTR = dChangedRectangle[iPlayer]
			lExceptions = getOrElse(dChangedExceptions, iPlayer, [])
	
	left, bottom = tBL
	right, top = tTR		
	return [(x, y) for x in range(left, right+1) for y in range(bottom, top+1) if (x, y) not in lExceptions]

def getCapital(iPlayer, bReborn=None):
	if bReborn is None: bReborn = isReborn(iPlayer)
	if bReborn and iPlayer in dChangedCapitals:
		return dChangedCapitals[iPlayer]
	return tCapitals[iPlayer]
	
def getRespawnCapital(iPlayer, bReborn=None):
	if iPlayer in dRespawnCapitals: return dRespawnCapitals[iPlayer]
	return getCapital(iPlayer, bReborn)
	
def getNewCapital(iPlayer, bReborn=None):
	if iPlayer in dNewCapitals: return dNewCapitals[iPlayer]
	return getRespawnCapital(iPlayer, bReborn)
	
def getBirthArea(iPlayer):
	return getArea(iPlayer, tBirthArea, dBirthAreaExceptions)
	
def getBirthRectangle(iPlayer, bExtended = None):
	if bExtended is None: bExtended = isExtendedBirth(iPlayer)
	if iPlayer in dChangedBirthArea and bExtended:
		return dChangedBirthArea[iPlayer]
	return tBirthArea[iPlayer]
	
def getBirthExceptions(iPlayer):
	if iPlayer in dBirthAreaExceptions: return dBirthAreaExceptions[iPlayer]
	return []
	
def getCoreArea(iPlayer, bReborn=None):
	return getArea(iPlayer, tCoreArea, dCoreAreaExceptions, bReborn, dChangedCoreArea, dChangedCoreAreaExceptions)
	
def getNormalArea(iPlayer, bReborn=None):
	return getArea(iPlayer, tNormalArea, dNormalAreaExceptions, bReborn, dChangedNormalArea, dChangedNormalAreaExceptions)

def getBroaderArea(iPlayer, bReborn=None):
	return getArea(iPlayer, tBroaderArea, {}, dChangedBroaderArea)
	
def getRespawnArea(iPlayer):
	if iPlayer in dRespawnArea: return getArea(iPlayer, dRespawnArea, {})
	return getNormalArea(iPlayer)
	
def getRebirthArea(iPlayer):
	if iPlayer in dRebirthArea: return getArea(iPlayer, dRebirthArea, dRebirthAreaExceptions)
	return getBirthArea(iPlayer)
	
def updateCore(iPlayer):
	lCore = getCoreArea(iPlayer)
	for x in range(iWorldX):
		for y in range(iWorldY):
			plot = gc.getMap().plot(x, y)
			if plot.isWater() or (plot.isPeak() and (x, y) not in lPeakExceptions): continue
			plot.setCore(iPlayer, (x, y) in lCore)
			
def isForeignCore(iPlayer, tPlot):
	x, y = tPlot
	plot = gc.getMap().plot(x, y)
	for iLoopPlayer in range(iNumPlayers):
		if iLoopPlayer == iPlayer: continue
		if plot.isCore(iLoopPlayer):
			return True
	return False
	
def isExtendedBirth(iPlayer):
	if gc.getGame().getActivePlayer() == iPlayer: return False
	
	return True
			
def init():
	for iPlayer in range(iNumPlayers):
		updateCore(iPlayer)
	
### Capitals ###

tCapitals = (
(52, 44), # Madrid
(55, 50), # Paris
(53, 54), # London
(27, 46), # Washington
(30, 52), # Montreal
)

dChangedCapitals = {
}

# new capital locations if changed during the game
dNewCapitals = {
}

# new capital locations on respawn
dRespawnCapitals = {
}

### Birth Area ###

tBirthArea = (
((49, 43), 	(53, 46)), 	# Spain
((51, 46), 	(57, 52)), 	# France
((50, 53), 	(54, 60)), 	# England
((25, 43), 	(32, 50)), 	# America
((20, 50), 	(35, 60)), 	# Canada
)

dChangedBirthArea = {
}

dBirthAreaExceptions = {
iSpain : [(49, 41), (49, 42), (49, 43), (49, 44), (50, 43), (50, 44), (50, 42)],
iFrance : [(55, 46), (57, 46), (56, 45), (57, 45), (58, 48), (58, 49), (58, 50), (53, 46), (52, 46), (51, 46), (57, 46), (56, 52), (57, 52)],
iAmerica : [(25, 48), (25, 49), (25, 50), (26, 48), (26, 49), (27, 49), (27, 50), (28, 50), (29, 50), (30, 50)],
iCanada : [(20, 50), (21, 50), (22, 50), (23, 50), (24, 50), (25, 50), (29, 50), (30, 50), (31, 50), (32, 50), (20, 51), (21, 51), (22, 51), (23, 51), (24, 51), (32, 51), (35, 53), (35, 54), (34, 55), (34, 56), (33, 56), (33, 57)],
}

### Core Area ###

tCoreArea = (
((49, 43),	(53, 46)),	# Spain
((51, 46),	(57, 51)),	# France
((50, 53),	(54, 60)),	# England
((23, 45),	(32, 50)),	# America
((27, 50),	(35, 52)),	# Canada
)

dChangedCoreArea = {
iSpain : 	((49, 40),	(55, 46)),
}

dCoreAreaExceptions = {
iSpain : [(49, 43), (49, 44), (50, 43), (50, 44)],
iFrance : [(51, 46), (52, 46), (55, 46), (57, 46)],
iAmerica : [(23, 50), (27, 50), (29, 50), (30, 50)],
iCanada : [(29, 50), (30, 50), (31, 50), (32, 50), (32, 51)],
}

dChangedCoreAreaExceptions = {
}

### Normal Area ###

tNormalArea = (
((49, 40), 	(55, 46)), 	# Spain
((51, 46), 	(58, 52)), 	# France
((50, 53), 	(54, 60)), 	# England
((11, 43), 	(31, 49)), 	# America
(( 8, 50), 	(37, 67)), 	# Canada
)

dChangedNormalArea = {
}

dNormalAreaExceptions = {
iSpain : [(49, 44), (49, 43), (49, 42), (49, 41)],
iFrance : [(51, 46), (52, 46), (53, 46), (58, 47), (58, 46), (58, 51), (58, 52), (57, 52)],
iCanada : [(11,50), (12,50), (13,50), (14,50), (16,50), (17,50), (18,50), (19,50), (20,50), (21,50), (22,50), (23,50), (24,50), (25,50), (29,50), (30,50), (31,50), (32,50), (32,51), (8,59), (8,60), (8,61), (8,62), (8,63), (8,64), (8,65), (9,59), (9,60), (9,61), (9,62), (9,63), (9,64), (9,65), (37,66), (37,67)],
}

dChangedNormalAreaExceptions = {
}

### Broader Area ###

tBroaderArea = (
((49, 38), 	(55, 46)), 	# Spain
((49, 44), 	(61, 52)), 	# France
((48, 53), 	(54, 60)), 	# England
((10, 42), 	(37, 56)), 	# America
(( 8, 50), 	(37, 67)), 	# Canada
)

dChangedBroaderArea = {
}

### Respawn area ###

dRespawnArea = {
}

### Rebirth area ###

dRebirthPlot = {
}

dRebirthArea = {
}

dRebirthAreaExceptions = {
}