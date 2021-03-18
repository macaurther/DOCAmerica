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
	
### Spawn ###	#MacAurther TODO: Idea: Palace doesn't spawn in first city, a Statehouse needs to be built to make a capital
tCapitals = (
(109, 74), # Madrid
(118, 74), # Paris
(127, 73), # London
(132, 39), # Jamestown
(145, 59), # Plymouth
(142, 65), # Portsmouth
(131, 43), # St. Mary's
(140, 57), # Hartford
(143, 57), # Providence
(128, 30), # Wilmington
(124, 25), # Charleston
(135, 52), # Trenton
(137, 54), # New York
(133, 50), # Philadelphia
(135, 46), # Dover
(121, 22), # Savannah
(128, 43), # Washington
(132, 69), # Montreal
)

dChangedCapitals = {
}

# new capital locations if changed during the game
# MacAurther TODO: new locations
dNewCapitals = {
}

# new capital locations on respawn
dRespawnCapitals = {
}

### Generic Areas ###
# This is lists of coordinates that are just generically States' boundaries, used in multiple places
# BL, TR
tGenericArea = (
((105, 71),	(112, 78)),	# Spain
((114, 70),	(119, 78)),	# France
((125, 73),	(131, 79)),	# England
((115, 35),	(135, 45)),	# Virginia
((136, 57),	(147, 63)),	# Massachusetts
((138, 62),	(142, 70)),	# New Hampshire
((122, 42),	(136, 48)),	# Maryland
((137, 55),	(141, 58)),	# Connecticut
((142, 56),	(144, 58)),	# Rhode Island
((113, 29),	(136, 36)),	# North Carolina
((116, 23),	(126, 30)),	# South Carolina
((133, 47),	(138, 55)),	# New Jersey
((121, 53),	(141, 67)),	# New York
((120, 47),	(134, 56)),	# Pennsylvania
((134, 44),	(136, 48)),	# Delaware
((111, 17),	(122, 29)),	# Georgia
((23, 45),	(32, 50)),	# America	TODO
((27, 50),	(35, 52)),	# Canada	TODO
)

tGenericAreaExceptions = {
iSpain : [(49, 43), (49, 44), (50, 43), (50, 44)],
iFrance : [(51, 46), (52, 46), (55, 46), (57, 46)],
iVirginia : [
#North West Border
(115,45), (116,45), (117,45), (118,45), (119,45), (120,45), (121,45), (122,45), (123,45), (124,45), 
(115,44), (116,44), (117,44), (118,44), (119,44), (120,44), (121,44), (122,44), (123,44), (124,44), 
(115,43), (116,43), (117,43), (118,43), (119,43), (120,43), (121,43), (122,43), (123,43), 
(115,42), (116,42), (117,42), (118,42), (119,42), (120,42), (121,42), (122,42), (123,42), 
(115,41), (116,41), (117,41), (118,41), (119,41), (120,41), (121,41), (123,41), 
(115,40), (116,40), (117,40), (118,40), (119,40), (120,40), (121,40), 
(115,39), (116,39), (117,39), (118,39), (119,39), (120,39), (121,39), 
(115,38), (116,38), (117,38), (118,38), (119,38), (120,38), (121,38), 
(115,37), (116,37), (118,37), (119,37), 
(115,36), 
#North East Border
(128,45), (129,45), (130,45), (131,45), (132,45), (133,45), (134,45), (135,45), 
(128,44), (129,44), (130,44), (131,44), (132,44), (133,44), (134,44), (135,44), 
(129,43), (130,43), (131,43), (132,43), (133,43), (134,43), (135,43), 
(130,42), (131,42), (132,42), (133,42), (134,42), (135,42), 
#Southern Border
(129,36), (130,36), (131,36), (132,36), (133,36), (134,36), (135,36), 
(122,35), (123,35), (124,35), (125,35), (126,35), (127,35), (128,35), (129,35), (130,35), (131,35), (132,35), (133,35), (134,35), (135,35), 
],
iMassachusetts : [
#Northern Border
(136,63), (137,63), (138,63), (139,63), (140,63), (141,63), (142,63), 
(136,62), (137,62), (138,62), (139,62), 
(136,61), 
#Southern Border
(136,58), (139,58), (140,58), (141,58), (142,58), (143,58), 
(136,57), (137,57), (138,57), (139,57), (140,57), (141,57), (142,57), (143,57), 
],
iNewHampshire : [
#Northern Border
(138,70), (140,70), (141,70), (142,70), 
(138,69), (140,69), (141,69), (142,69), 
(138,68), (141,68), (142,68), 
(138,67), (141,67), (142,67), 
(138,66), (142,66), 
(138,65), 
#Southern Border
(140,62), (141,62), (142,62), 
],
iMaryland : [
#North Western Border
(122,48), (123,48), (124,48), (125,48), (126,48), (127,48), (128,48), 
(122,47), (123,47), (124,47), 
#North Eastern Border
(134,48), (135,48), (136,48), 
(134,47), (135,47), (136,47), 
(134,46), (135,46), (136,46), 
(134,45), (135,45), (136,45), 
(134,44), (135,44), (136,44), 
#Southern Border
(125,46), 
(123,45), (124,45), (125,45), (126,45), (127,45), 
(122,44), (123,44), (124,44), (125,44), (126,44), (127,44), (128,44), 
(122,43), (123,43), (124,43), (125,43), (126,43), (127,43), (128,43), 
(122,42), (123,42), (124,42), (125,42), (126,42), (127,42), (128,42), (129,42), 
],
iConnecticut : [
#Western Border
(137,58), (138,58), 
(137,56), (137,55), 
],
iRhodeIsland : [
#Eastern Border
(144,58), (144,57), 
],
iNorthCarolina : [
#Northern Border
(113,36), (114,36), (115,36), (116,36), (117,36), (118,36), (119,36), (120,36), (121,36), (122,36), (123,36), (124,36), (125,36), (126,36), (127,36), (128,36), 
(113,35), (114,35), (115,35), (116,35), (117,35), (118,35), (119,35), (120,35), (121,35), 
(113,34), (114,34), (115,34), (116,34), (117,34), (118,34), 
(113,33), (114,33), (115,33), (116,33), (117,33), 
(113,32), (114,32), (115,32), 
(113,31), 
#Southern Border
(118,30), (119,30), (120,30), (121,30), (122,30), (123,30), (124,30), 
(113,29), (114,29), (115,29), (116,29), (117,29), (118,29), (119,29), (120,29), (121,29), (122,29), (123,29), (124,29), (125,29), 
],
iSouthCarolina : [
#Western Border
(116,30), 
(116,28), 
(116,27), (117,27), 
(116,26), (117,26), (118,26), 
(116,25), (117,25), (118,25), (119,25), 
(116,24), (117,24), (118,24), (119,24), (120,24), 
(116,23), (117,23), (118,23), (119,23), (120,23), (121,23), 
#Eastern Border
(125,30), (126,30),
(126,29),
],
iNewJersey : [
#Western Border
(133,55), 
(133,52), 
(133,51), (134,51), 
(133,50), (134,50), 
(133,49), 
(133,48), (134,48), 
(133,47), (134,47), (135,47), (136,47), 
#Eastern Border
(135,55), (136,55), (137,55), (138,55), 
(137,54), (138,54), 
(137,53), (138,53), 
(137,52), (138,52), 
],
iNewYork : [
#North West Border
(121,67), (122,67), (123,67), (124,67), (125,67), (126,67), (127,67), (128,67), (129,67), (130,67), (131,67),
(121,66), (122,66), (123,66), (124,66), (125,66), (126,66), (127,66), (128,66), (129,66),
(121,65), (122,65), (123,65), (124,65), (125,65), (126,65), (127,65), (128,65),
(121,64), (122,64), (123,64), (124,64), (125,64), (126,64), (127,64),
(121,63), (122,63), (123,63), (124,63), (125,63), (126,63), (127,63),
(121,62), (122,62), (123,62), (124,62), (125,62),
(121,61), (122,61), (123,61), (124,61),
(121,60),
(121,57),
#North East Border
(134,67), (135,67), (136,67), (137,67), (138,67), (139,67), (140,67), (141,67), 
(134,66), (135,66), (136,66), (137,66), (138,66), (139,66), (140,66), (141,66), 
(134,65), (135,65), (136,65), (137,65), (138,65), (139,65), (140,65), (141,65), 
(135,64), (136,64), (137,64), (138,64), (139,64), (140,64), (141,64), 
(135,63), (136,63), (137,63), (138,63), (139,63), (140,63), (141,63), 
(136,62), (137,62), (138,62), (139,62), (140,62), (141,62), 
(136,61), (137,61), (138,61), (139,61), (140,61), (141,61), 
(136,60), (137,60), (138,60), (139,60), (140,60), (141,60), 
(136,59), (137,59), (138,59), (139,59), (140,59), (141,59),
(137,58), (138,58), (139,58), (140,58), (141,58),
(137,57), (138,57), (139,57), (140,57), (141,57),
(138,56), (139,56), (140,56), (141,56), 
(138,55), (139,55), (140,55), (141,55), 
(140,54), 
#Southern Border
(129,56), (130,56), (131,56), (132,56), 
(125,55), (126,55), (127,55), (128,55), (129,55), (130,55), (131,55), (132,55), (133,55), (134,55), 
(121,54), (122,54), (123,54), (124,54), (125,54), (126,54), (127,54), (128,54), (129,54), (130,54), (131,54), (132,54), (133,54), (134,54), (135,54), (136,54), 
(121,53), (122,53), (123,53), (124,53), (125,53), (126,53), (127,53), (128,53), (129,53), (130,53), (131,53), (132,53), (133,53), (134,53), (135,53), (136,53), 
],
iPennsylvania : [
#Northern Border
(120,56), (121,56), (122,56), (123,56), (124,56), (125,56), (126,56), (127,56), (128,56), 
(120,55), (121,55), (122,55), (123,55), (124,55), 
#Eastern Border
(133,56), (134,56), 
(134,55), 
(133,54), (134,54), 
(133,53), (134,53), 
(134,52), 
(134,49), 
#Southern Border
(129,48), (130,48), (131,48), (132,48), (133,48), (134,48), 
(120,47), (125,47), (126,47), (127,47), (128,47), (129,47), (130,47), (131,47), (132,47), (133,47), (134,47), 
],
iDelaware : [
#Eastern Border
(135,48), (136,48), 
],
iGeorgia : [
#Western Border
(111,24), (111,23),
(111,22), (112,22),
(111,21), (112,21),
(111,20), (112,20),
(111,19), (112,19),
(111,18), (112,18),
#North Eastern Border
(116,29), (117,29), (118,29), (119,29), (120,29), (121,29), (122,29),
(117,28), (118,28), (119,28), (120,28), (121,28), (122,28),
(118,27), (119,27), (120,27), (121,27), (122,27),
(119,26), (120,26), (121,26), (122,26),
(120,25), (121,25), (122,25),
(121,24), (122,24),
(122,23),
#Southern Border
(121,18), (122,18), 
(111,17), (112,17), (113,17), (114,17), (115,17), (116,17), (117,17), (118,17), (119,17), (121,17), (122,17), 
],
iAmerica : [(23, 50), (27, 50), (29, 50), (30, 50)],
iCanada : [(29, 50), (30, 50), (31, 50), (32, 50), (32, 51)],
}

### Birth Area ###
# This is Flip Zone
# BL, TR
tBirthArea = tGenericArea

dChangedBirthArea = {
}

dBirthAreaExceptions = tGenericAreaExceptions

### Core Area ###
# This is Core Area
# BL, TR
tCoreArea = (
((105, 71),	(112, 78)),	# Spain		TODO
((114, 70),	(119, 78)),	# France	TODO
((125, 73),	(131, 79)),	# England	TODO
((125, 37),	(133, 41)),	# Virginia
((142, 58),	(147, 62)),	# Massachusetts
((140, 63),	(142, 66)),	# New Hampshire
((129, 42),	(134, 48)),	# Maryland
((137, 55),	(141, 58)),	# Connecticut
((142, 56),	(144, 58)),	# Rhode Island
((125, 29),	(136, 36)),	# North Carolina
((120, 23),	(126, 29)),	# South Carolina
((133, 47),	(138, 55)),	# New Jersey
((133, 53),	(141, 62)),	# New York
((127, 48),	(134, 56)),	# Pennsylvania
((134, 44),	(136, 48)),	# Delaware
((116, 18),	(122, 23)),	# Georgia
((23, 45),	(32, 50)),	# America	TODO
((27, 50),	(35, 52)),	# Canada	TODO
)

dChangedCoreArea = {
iSpain : 	((49, 40),	(55, 46)),
}

dCoreAreaExceptions = tGenericAreaExceptions

dChangedCoreAreaExceptions = {
}

### Normal Area ###
# This is revealed plots on birth and used for fragmenting Barbarians
# MacAurther TODO: This is what is revealed on the map on birth, make more interesting
# BL, TR
tNormalArea = tGenericArea

dChangedNormalArea = {
}

dNormalAreaExceptions = tGenericAreaExceptions

dChangedNormalAreaExceptions = {
}

### Broader Area ###
# Used for flipping units on birth in foreign area
tBroaderArea = tGenericArea

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