from Core import *
from RFCUtils import *

from Events import handler
from Resurrection import getResurrectionTechs


def processConquest(iConquest, iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval):
	return iConquest + 1, (iConquest, iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval)

### Constants ###

iMinIntervalEarly = 10
iMaxIntervalEarly = 20
iMinIntervalLate = 40
iMaxIntervalLate = 60
iThreshold = 100
iMinValue = 30

iConquestNum = 0

# Inca ------------------------------------------------------------------------------------------------------------------------
iIncaWariYear = 1200
tIncaWariTL = (21, 31)
tIncaWariBR = (24, 35)

iIncaTiwanakuYear = 1438
tIncaTiwanakuTL = (25, 22)
tIncaTiwanakuBR = (28, 26)

iIncaChimuYear = 1450
tIncaChimuTL = (20, 36)
tIncaChimuBR = (23, 40)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
iConquestNum, tConquestIncaWari = processConquest(iConquestNum, iInca, iWari, tIncaWariTL, tIncaWariBR, 3, iIncaWariYear, 10)
iConquestNum, tConquestIncaTiwanaku = processConquest(iConquestNum, iInca, iTiwanaku, tIncaTiwanakuTL, tIncaTiwanakuBR, 2, iIncaTiwanakuYear, 10)
iConquestNum, tConquestIncaChimu = processConquest(iConquestNum, iInca, iChimu, tIncaChimuTL, tIncaChimuBR, 3, iIncaChimuYear, 10)

# Spain ------------------------------------------------------------------------------------------------------------------------
iSpainAztecsYear = 1519
tSpainAztecsTL = (11, 63)
tSpainAztecsBR = (16, 69)

iSpainPurepechansYear = 1522
tSpainPurepechansTL = (8, 66)
tSpainPurepechansBR = (11, 70)

iSpainZapotecYear = 1527
tSpainZapotecTL = (12, 60)
tSpainZapotecBR = (17, 62)

iSpainIncaYear = 1532
tSpainIncaTL = (20, 24)
tSpainIncaBR = (28, 33)

iSpainWariYear = 1532
tSpainWariTL = (20, 24)
tSpainWariBR = (28, 33)

iSpainChimuYear = 1532
tSpainChimuTL = (20, 24)
tSpainChimuBR = (28, 33)

iSpainMuiscaYear = 1537
tSpainMuiscaTL = (22, 41)
tSpainMuiscaBR = (34, 45)

iSpainPuebloYear = 1598
tSpainPuebloTL = (12, 83)
tSpainPuebloBR = (19, 89)

iSpainMayaYear = 1697
tSpainMayaTL = (20, 58)
tSpainMayaBR = (25, 63)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
iConquestNum, tConquestSpainAztecs = processConquest(iConquestNum, iSpain, iAztecs, tSpainAztecsTL, tSpainAztecsBR, 2, iSpainAztecsYear, 10)
iConquestNum, tConquestSpainPurepechans = processConquest(iConquestNum, iSpain, iPurepecha, tSpainPurepechansTL, tSpainPurepechansBR, 2, iSpainPurepechansYear, 10)
iConquestNum, tConquestSpainZapotec = processConquest(iConquestNum, iSpain, iZapotec, tSpainZapotecTL, tSpainZapotecBR, 2, iSpainZapotecYear, 10)
iConquestNum, tConquestSpainInca = processConquest(iConquestNum, iSpain, iInca, tSpainIncaTL, tSpainIncaBR, 3, iSpainIncaYear, 10)
iConquestNum, tConquestSpainWari = processConquest(iConquestNum, iSpain, iWari, tSpainWariTL, tSpainWariBR, 2, iSpainWariYear, 10)
iConquestNum, tConquestSpainChimu = processConquest(iConquestNum, iSpain, iChimu, tSpainChimuTL, tSpainChimuBR, 2, iSpainChimuYear, 10)
iConquestNum, tConquestSpainMuisca = processConquest(iConquestNum, iSpain, iMuisca, tSpainMuiscaTL, tSpainMuiscaBR, 2, iSpainMuiscaYear, 10)
iConquestNum, tConquestSpainPueblo = processConquest(iConquestNum, iSpain, iPuebloan, tSpainPuebloTL, tSpainPuebloBR, 2, iSpainPuebloYear, 10)
iConquestNum, tConquestSpainMaya = processConquest(iConquestNum, iSpain, iMaya, tSpainMayaTL, tSpainMayaBR, 2, iSpainMayaYear, 10)

# England ------------------------------------------------------------------------------------------------------------------------
iEnglandNetherlandsYear = 1670
tEnglandNetherlandsTL = (39, 78)
tEnglandNetherlandsBR = (43, 86)

iEnglandQuebecYear = 1758
tEnglandQuebecTL = (42, 89)
tEnglandQuebecBR = (47, 93)

iEnglandAmerica1812WashingtonYear = 1814
tEnglandAmerica1812WashingtonTL = (38, 76)
tEnglandAmerica1812WashingtonBR = (14, 81)

iEnglandAmerica1812NewOrleansYear = 1815
tEnglandAmerica1812NewOrleansTL = (23, 72)
tEnglandAmerica1812NewOrleansBR = (29, 73)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
iConquestNum, tConquestEnglandNetherlands = processConquest(iConquestNum, iEngland, iNetherlands, tEnglandNetherlandsTL, tEnglandNetherlandsBR, 2, iEnglandNetherlandsYear, 10)
iConquestNum, tConquestEnglandQuebec = processConquest(iConquestNum, iEngland, iFrance, tEnglandQuebecTL, tEnglandNetherlandsBR, 2, iEnglandNetherlandsYear, 10)
iConquestNum, tConquestEngland1812Washington = processConquest(iConquestNum, iEngland, iAmerica, tEnglandAmerica1812WashingtonTL, tEnglandAmerica1812WashingtonBR, 1, iEnglandAmerica1812WashingtonYear, 10)
iConquestNum, tConquestEngland1812NewOrleans = processConquest(iConquestNum, iEngland, iAmerica, tEnglandAmerica1812NewOrleansTL, tEnglandAmerica1812NewOrleansBR, 1, iEnglandAmerica1812NewOrleansYear, 10)

# France ------------------------------------------------------------------------------------------------------------------------
iFranceMexicoYear = 1861
tFranceMexicoTL = (12, 60)
tFranceMexicoBR = (19, 70)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
iConquestNum, tConquestFranceMexico = processConquest(iConquestNum, iFrance, iMexico, tFranceMexicoTL, tFranceMexicoBR, 3, iFranceMexicoYear, 10)

# Netherlands --------------------------------------------------------------------------------------------------------------------
iNetherlandsNorseYear = 1655
tNetherlandsNorseTL = (39, 78)
tNetherlandsNorseBR = (41, 82)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
iConquestNum, tConquestNetherlandsNorse = processConquest(iConquestNum, iEngland, iNetherlands, tNetherlandsNorseTL, tNetherlandsNorseBR, 1, iNetherlandsNorseYear, 10)

# America ------------------------------------------------------------------------------------------------------------------------
iAmericaCanadaYear = 1812
tAmericaCanadaTL = (35, 86)
tAmericaCanadaBR = (45, 92)

iAmericaMexicoYear = 1846
tAmericaMexicoTL = (14, 72)
tAmericaMexicoBR = (25, 80)

iAmericaLakotkaYear = 1875
tAmericaLakotkaTL = (19, 89)
tAmericaLakotkaBR = (31, 95)

iAmericaCubaYear = 1898
tAmericaCubaTL = (27, 58)
tAmericaCubaBR = (36, 63)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
iConquestNum, tConquestAmericaCanada = processConquest(iConquestNum, iAmerica, iCanada, tAmericaCanadaTL, tAmericaCanadaBR, 2, iAmericaCanadaYear, 10)
iConquestNum, tConquestAmericaMexico = processConquest(iConquestNum, iAmerica, iMexico, tAmericaMexicoTL, tAmericaMexicoBR, 4, iAmericaMexicoYear, 10)
iConquestNum, tConquestAmericaLakota = processConquest(iConquestNum, iAmerica, iLakota, tAmericaLakotkaTL, tAmericaLakotkaBR, 2, iAmericaLakotkaYear, 10)
iConquestNum, tConquestAmericaCuba = processConquest(iConquestNum, iAmerica, iSpain, tAmericaCubaTL, tAmericaCubaBR, 3, iAmericaCubaYear, 10)

# Canada ------------------------------------------------------------------------------------------------------------------------
iCanadaLakotaYear = 1880
tCanadaLakotaTL = (19, 96)
tCanadaLakotaBR = (28, 101)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
iConquestNum, tConquestCanadaLakota = processConquest(iConquestNum, iCanada, iLakota, tCanadaLakotaTL, tCanadaLakotaBR, 2, iCanadaLakotaYear, 10)


lConquests = [tConquestIncaWari, tConquestIncaTiwanaku, tConquestIncaChimu,
tConquestSpainAztecs, tConquestSpainPurepechans, tConquestSpainZapotec, tConquestSpainInca, tConquestSpainWari, tConquestSpainChimu, tConquestSpainMuisca, tConquestSpainPueblo, tConquestSpainMaya,
tConquestEnglandNetherlands, tConquestEngland1812Washington, tConquestEngland1812NewOrleans, 
tConquestFranceMexico,
tConquestNetherlandsNorse,
tConquestAmericaCanada, tConquestAmericaMexico, tConquestAmericaLakota, tConquestAmericaCuba,
tConquestCanadaLakota]


@handler("GameStart")
def setup():
	iTurn = year(400)
	if scenario() == i1500AD:  #late start condition
		iTurn = year(1550)
	elif scenario() == i1750AD:
		iTurn = year(1790)
	data.iNextTurnAIWar = iTurn + rand(iMaxIntervalEarly-iMinIntervalEarly)


@handler("BeginGameTurn")
def restorePeaceMinors(iGameTurn):
	if iGameTurn > turns(50):
		iMinor = players.independent().periodic(20)
		if iMinor:
			restorePeaceHuman(iMinor, False)
			
		iMinor = players.independent().periodic(60)
		if iMinor:
			restorePeaceAI(iMinor, False)


@handler("BeginGameTurn")
def startMinorWars(iGameTurn):
	if iGameTurn > turns(50):	
		iMinor = players.independent().periodic(13)
		if iMinor:
			minorWars(iMinor)


@handler("BeginGameTurn")
def checkConquests():
	for tConquest in lConquests:
		checkConquest(tConquest)
		
		
@handler("BeginGameTurn")
def checkWarPlans(iGameTurn):		
	if iGameTurn == data.iNextTurnAIWar:
		planWars(iGameTurn)


@handler("BeginGameTurn")
def increaseAggressionLevels():
	for iLoopPlayer in players.major():
		data.players[iLoopPlayer].iAggressionLevel = dAggressionLevel[iLoopPlayer] + rand(2)


@handler("techAcquired")	
def forgetMemory(iTech, iTeam, iPlayer):
	if year() <= year(1700):
		return

	if iTech in [iPsychology, iTelevision]:
		pPlayer = player(iPlayer)
		for iLoopPlayer in players.major().without(iPlayer):
			if pPlayer.AI_getMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR) > 0:
				pPlayer.AI_changeMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR, -1)
			
			if pPlayer.AI_getMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR_ON_FRIEND) > 0:
				pPlayer.AI_changeMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR_ON_FRIEND, -1)


@handler("changeWar")
def resetAggressionLevel(bWar, iTeam, iOtherTeam):
	if bWar and not is_minor(iTeam) and not is_minor(iOtherTeam):
		data.players[iTeam].iAggressionLevel = 0
		data.players[iOtherTeam].iAggressionLevel = 0

		
def checkConquest(tConquest, tPrereqConquest = (), iWarPlan = WarPlanTypes.WARPLAN_TOTAL):
	iID, iCiv, iPreferredTargetCiv, tTL, tBR, iNumTargets, iYear, iIntervalTurns = tConquest
	
	iPlayer = slot(iCiv)
	if iPlayer < 0:
		return
		
	iPreferredTarget = slot(iPreferredTargetCiv)

	if player(iPlayer).isHuman():
		return
		
	if not player(iPlayer).isExisting(): 
		return
	
	if team(iPlayer).isAVassal():
		return
	
	if data.lConquest[iID]:
		return
		
	if iPreferredTarget >= 0 and player(iPreferredTarget).isExisting() and team(iPreferredTarget).isVassal(iPlayer):
		return
	
	if tPrereqConquest and not isConquered(tPrereqConquest):
		return
	
	if iCiv == iSpain and (iPreferredTarget < 0 or player(iPreferredTarget).isHuman()):
		return
	
	iStartTurn = year(iYear) + turns(data.iSeed % 10 - 5)
	
	if turn() == iStartTurn - turns(5):
		warnConquest(iPlayer, iCiv, iPreferredTargetCiv, tTL, tBR)
	
	if turn() < player(iCiv).getLastBirthTurn() + turns(3): 
		return
	
	if not (iStartTurn <= turn() <= iStartTurn + iIntervalTurns):
		return
	
	spawnConquerors(iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns, iWarPlan)
	data.lConquest[iID] = True


def warnConquest(iPlayer, iCiv, iPreferredTargetCiv, tTL, tBR):
	text = text_if_exists("TXT_KEY_MESSAGE_CONQUERORS_%s_%s" % (infos.civ(iCiv).getIdentifier(), infos.civ(iPreferredTargetCiv).getIdentifier()), adjective(iPlayer), otherwise="TXT_KEY_MESSAGE_CONQUERORS_GENERIC")
	conquerorCities = cities.owner(iPlayer)
	
	for iTarget, targetCities in cities.rectangle(tTL, tBR).notowner(iPlayer).grouped(CyCity.getOwner):
		message(iTarget, str(text), color=iRed, location=targetCities.closest_all(conquerorCities), button=infos.civ(iCiv).getButton())


def isConquered(tConquest):
	iID, iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns = tConquest

	iNumMinorCities = 0
	for city in cities.start(tTL).end(tBR):
		if city.getOwner() in players.minor(): iNumMinorCities += 1
		elif city.getOwner() != iPlayer: return False
		
	if 2 * iNumMinorCities > len(lAreaCities): return False
	
	return True


def conquerorWar(iPlayer, iTarget, iWarPlan):
	# reset at war counters because this is essentially a renewed war, will avoid cheap peace out of the conquerors
	if team(iPlayer).isAtWar(team(iTarget).getID()):
		team(iPlayer).AI_setAtWarCounter(team(iTarget).getID(), 0)
		team(iTarget).AI_setAtWarCounter(team(iPlayer).getID(), 0)
		
		team(iPlayer).AI_setWarPlan(team(iTarget).getID(), iWarPlan)
		
	# otherwise declare war
	else:
		declareWar(iPlayer, iTarget, iWarPlan)

	
def spawnConquerors(iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns, iWarPlan = WarPlanTypes.WARPLAN_TOTAL):
	iCiv = civ(iPlayer)
	
	if not player(iPlayer).isExisting():
		for iTech in getResurrectionTechs(iPlayer):
			team(iPlayer).setHasTech(iTech, True, iPlayer, False, False)
			
	targetPlots = plots.rectangle(tTL, tBR)
			
	targetCities = cities.rectangle(tTL, tBR).notowner(iPlayer).where(lambda city: not team(city).isVassal(iPlayer)).lowest(iNumTargets, lambda city: (city.getOwner() == iPreferredTarget, distance(city, capital(iPlayer))))
	owners = set(city.getOwner() for city in targetCities)
	
	if iPreferredTarget >= 0 and iPreferredTarget not in owners and player(iPreferredTarget).isExisting():
		conquerorWar(iPlayer, iPreferredTarget, iWarPlan)
			
	for iOwner in owners:
		conquerorWar(iPlayer, iOwner, iWarPlan)
		message(iOwner, 'TXT_KEY_UP_CONQUESTS_TARGET', name(iPlayer))
		
	for city in targetCities:
		iExtra = 0
		if active() not in [iPlayer, city.getOwner()]: 
			iExtra += 1
			
		
		tPlot = findNearestLandPlot(city, iPlayer)
		
		dConquestUnits = {
			iBase: 2 + iExtra,
			iSiegeCity: 1 + 2*iExtra,
		}
		createRoleUnits(iPlayer, tPlot, dConquestUnits.items())
		
		if iCiv == iSpain:
			createRoleUnit(iPlayer, tPlot, iCav, 2*iExtra)


def declareWar(iPlayer, iTarget, iWarPlan):
	if team(iPlayer).isVassal(iTarget):
		team(iPlayer).setVassal(iTarget, False, False)
		
	team(iPlayer).declareWar(iTarget, True, iWarPlan)


def planWars(iGameTurn):
	# skip if there is a world war
	if iGameTurn > year(1500):
		iCivsAtWar = 0
		for iLoopPlayer in players.major():
			if team(iLoopPlayer).getAtWarCount(True) > 0:
				iCivsAtWar += 1
		if 100 * iCivsAtWar / game.countCivPlayersAlive() > 50:
			data.iNextTurnAIWar = iGameTurn + getNextInterval(iGameTurn)
			return

	iAttackingPlayer = determineAttackingPlayer()
	iTargetPlayer = determineTargetPlayer(iAttackingPlayer)
	
	if iAttackingPlayer is None:
		return

	data.players[iAttackingPlayer].iAggressionLevel = 0
	
	if iTargetPlayer == -1:
		return
		
	if team(iAttackingPlayer).canDeclareWar(iTargetPlayer):
		team(iAttackingPlayer).AI_setWarPlan(iTargetPlayer, WarPlanTypes.WARPLAN_PREPARING_LIMITED)
	
	data.iNextTurnAIWar = iGameTurn + getNextInterval(iGameTurn)


def determineAttackingPlayer():
	return players.major().existing().where(possibleTargets).maximum(lambda p: data.players[p].iAggressionLevel)


def possibleTargets(iPlayer):
	return players.major().without(iPlayer).where(lambda p: team(iPlayer).canDeclareWar(player(p).getTeam()))


def determineTargetPlayer(iPlayer):
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iCiv = civ(iPlayer)
	
	lPotentialTargets = []
	dTargetValues = defaultdict({}, 0)

	# determine potential targets
	for iLoopPlayer in possibleTargets(iPlayer):
		pLoopPlayer = player(iLoopPlayer)
		tLoopPlayer = team(iLoopPlayer)
		
		if iLoopPlayer == iPlayer: continue
		
		# requires live civ and past contact
		if not pLoopPlayer.isExisting(): continue
		if not tPlayer.isHasMet(iLoopPlayer): continue
		
		# no masters or vassals
		if tPlayer.isVassal(iLoopPlayer): continue
		if tLoopPlayer.isVassal(iPlayer): continue
		
		# not already at war
		if tPlayer.isAtWar(iLoopPlayer): continue
		
		# birth protected
		if pLoopPlayer.isBirthProtected(): continue
		
		lPotentialTargets.append(iLoopPlayer)
		
	if not lPotentialTargets: 
		return -1
		
	# iterate the map for all potential targets
	for plot in plots.all():
		iOwner = plot.getOwner()
		if iOwner in lPotentialTargets:
			dTargetValues[iOwner] += pPlayer.getWarValue(plot.getX(), plot.getY())
				
	# hard to attack with lost contact
	for iLoopPlayer in lPotentialTargets:
		if not pPlayer.canContact(iLoopPlayer):
			dTargetValues[iLoopPlayer] /= 8
		
	# normalization
	iMaxValue = max(dTargetValues.values())
	if iMaxValue == 0: 
		return -1
	
	for iLoopPlayer in lPotentialTargets:
		dTargetValues[iLoopPlayer] *= 500
		dTargetValues[iLoopPlayer] /= iMaxValue
		
	for iLoopPlayer in lPotentialTargets:
		iLoopCiv = civ(iLoopPlayer)
	
		# randomization
		if dTargetValues[iLoopPlayer] <= iThreshold:
			dTargetValues[iLoopPlayer] += rand(100)
		else:
			dTargetValues[iLoopPlayer] += rand(300)
		
		# balanced by attitude
		iAttitude = pPlayer.AI_getAttitude(iLoopPlayer) - 2
		if iAttitude > 0:
			dTargetValues[iLoopPlayer] /= 2 * iAttitude
			
		# exploit plague
		if data.players[iLoopPlayer].iPlagueCountdown > 0 or data.players[iLoopPlayer].iPlagueCountdown < -10:
			if turn() > player(iLoopPlayer).getLastBirthTurn() + turns(20):
				dTargetValues[iLoopPlayer] *= 3
				dTargetValues[iLoopPlayer] /= 2
	
		# determine master
		iMaster = master(iLoopPlayer)
				
		# master attitudes
		if iMaster >= 0:
			iAttitude = player(iMaster).AI_getAttitude(iLoopPlayer)
			if iAttitude > 0:
				dTargetValues[iLoopPlayer] /= 2 * iAttitude
		
		# peace counter
		if not tPlayer.isAtWar(iLoopPlayer):
			iCounter = min(7, max(1, tPlayer.AI_getAtPeaceCounter(iLoopPlayer)))
			if iCounter <= 7:
				dTargetValues[iLoopPlayer] *= 20 + 10 * iCounter
				dTargetValues[iLoopPlayer] /= 100
				
		# defensive pact
		if tPlayer.isDefensivePact(iLoopPlayer):
			dTargetValues[iLoopPlayer] /= 4
			
		# consider power
		iOurPower = tPlayer.getPower(True)
		iTheirPower = team(iLoopPlayer).getPower(True)
		if iOurPower > 2 * iTheirPower:
			dTargetValues[iLoopPlayer] *= 2
		elif 2 * iOurPower < iTheirPower:
			dTargetValues[iLoopPlayer] /= 2
			
		# spare smallish civs
		if iLoopCiv in [iNetherlands, iPortugal]:
			dTargetValues[iLoopPlayer] *= 4
			dTargetValues[iLoopPlayer] /= 5
			
		# no suicide
		if iCiv == iNetherlands:
			if iLoopCiv in [iEngland]:
				dTargetValues[iLoopPlayer] /= 2
		
		# Treaty of Tordesillas
		if iCiv in [iSpain, iPortugal]:
			if iLoopCiv in [iSpain, iPortugal]:
				dTargetValues[iLoopPlayer] /= 8
		
				
	return dict_max(dTargetValues)
				

def getNextInterval(iGameTurn):
	if iGameTurn > year(1600):
		iMinInterval = iMinIntervalLate
		iMaxInterval = iMaxIntervalLate
	else:
		iMinInterval = iMinIntervalEarly
		iMaxInterval = iMaxIntervalEarly
		
	iMinInterval = turns(iMinInterval)
	iMaxInterval = turns(iMaxInterval)
	
	return rand(iMinInterval, iMaxInterval)