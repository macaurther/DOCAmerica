from Core import *
from RFCUtils import *

from Events import handler
from Resurrection import getResurrectionTechs


### Constants ###

iMinIntervalEarly = 10
iMaxIntervalEarly = 20
iMinIntervalLate = 40
iMaxIntervalLate = 60
iThreshold = 100
iMinValue = 30

# Spain
iSpainAztecsYear = 1519
tSpainAztecsTL = (11, 63)
tSpainAztecsBR = (16, 69)

iSpainIncaYear = 1532
tSpainIncaTL = (20, 24)
tSpainIncaBR = (28, 33)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
tConquestSpainAztecs = (0, iSpain, iAztecs, tSpainAztecsTL, tSpainAztecsBR, 3, iSpainAztecsYear, 10)
tConquestSpainInca = (1, iSpain, iInca, tSpainIncaTL, tSpainIncaBR, 4, iSpainIncaYear, 10)

# England
iEnglandNetherlandsYear = 1664
tEnglandNetherlandsTL = (39, 78)
tEnglandNetherlandsBR = (43, 86)

iEnglandAmericaNorthYear = 1776
tEnglandAmericaNorthTL = (41, 81)
tEnglandAmericaNorthBR = (45, 86)

iEnglandAmericaSouthYear = 1778
tEnglandAmericaSouthTL = (33, 71)
tEnglandAmericaSouthBR = (39, 78)

iEnglandAmerica1812WashingtonYear = 1814
tEnglandAmerica1812WashingtonTL = (38, 76)
tEnglandAmerica1812WashingtonBR = (14, 81)

iEnglandAmerica1812NewOrleansYear = 1815
tEnglandAmerica1812NewOrleansTL = (23, 72)
tEnglandAmerica1812NewOrleansBR = (29, 73)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
tConquestEnglandNetherlands = (2, iEngland, iNetherlands, tEnglandNetherlandsTL, tEnglandNetherlandsBR, 1, iEnglandNetherlandsYear, 10)
tConquestEnglandAmericaNorth = (3, iEngland, iAmerica, tEnglandAmericaNorthTL, tEnglandAmericaNorthBR, 2, iEnglandAmericaNorthYear, 10)
tConquestEnglandAmericaSouth = (4, iEngland, iAmerica, tEnglandAmericaSouthTL, tEnglandAmericaSouthBR, 1, iEnglandAmericaSouthYear, 10)
tConquestEngland1812Washington = (5, iEngland, iAmerica, tEnglandAmerica1812WashingtonTL, tEnglandAmerica1812WashingtonBR, 1, iEnglandAmerica1812WashingtonYear, 10)
tConquestEngland1812NewOrleans = (6, iEngland, iAmerica, tEnglandAmerica1812NewOrleansTL, tEnglandAmerica1812NewOrleansBR, 1, iEnglandAmerica1812NewOrleansYear, 10)

# France
iFranceMexicoYear = 1861
tFranceMexicoTL = (12, 60)
tFranceMexicoBR = (19, 70)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
tConquestFranceMexico = (7, iFrance, iMexico, tFranceMexicoTL, tFranceMexicoBR, 3, iFranceMexicoYear, 10)

# Netherlands
iNetherlandsNorseYear = 1655
tNetherlandsNorseTL = (39, 78)
tNetherlandsNorseBR = (41, 82)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
tConquestNetherlandsNorse = (8, iEngland, iNetherlands, tNetherlandsNorseTL, tNetherlandsNorseBR, 1, iNetherlandsNorseYear, 10)


lConquests = [tConquestSpainAztecs, tConquestSpainInca, 
tConquestEnglandNetherlands, tConquestEnglandAmericaNorth, tConquestEnglandAmericaSouth, tConquestEngland1812Washington, tConquestEngland1812NewOrleans, 
tConquestFranceMexico,
tConquestNetherlandsNorse]

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
		
	if not player(iPlayer).isAlive(): 
		return
	
	if team(iPlayer).isAVassal():
		return
	
	if data.lConquest[iID]:
		return
		
	if iPreferredTarget >= 0 and player(iPreferredTarget).isAlive() and team(iPreferredTarget).isVassal(iPlayer):
		return
	
	if tPrereqConquest and not isConquered(tPrereqConquest):
		return
	
	iStartTurn = year(iYear) + turns(data.iSeed % 10 - 5)
	
	if turn() == iStartTurn - turns(5):
		warnConquest(iPlayer, iCiv, iPreferredTargetCiv, tTL, tBR)
	
	if turn() < player(iPlayer).getLastBirthTurn() + turns(3): 
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
	
	if not player(iPlayer).isAlive():
		for iTech in getResurrectionTechs(iPlayer):
			team(iPlayer).setHasTech(iTech, True, iPlayer, False, False)
			
	targetPlots = plots.rectangle(tTL, tBR)
			
	targetCities = cities.rectangle(tTL, tBR).notowner(iPlayer).where(lambda city: not team(city).isVassal(iPlayer)).lowest(iNumTargets, lambda city: (city.getOwner() == iPreferredTarget, distance(city, capital(iPlayer))))
	owners = set(city.getOwner() for city in targetCities)
	
	if iPreferredTarget >= 0 and iPreferredTarget not in owners and player(iPreferredTarget).isAlive():
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
			createRoleUnit(iPlayer, tPlot, iShockCav, 2*iExtra)


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
	return players.major().alive().where(possibleTargets).maximum(lambda p: data.players[p].iAggressionLevel)


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
		if not pLoopPlayer.isAlive(): continue
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