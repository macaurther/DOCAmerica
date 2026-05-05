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
tIncaWariTL = (42, 35)
tIncaWariBR = (46, 43)

iIncaTiwanakuYear = 1438
tIncaTiwanakuTL = (49, 30)
tIncaTiwanakuBR = (53, 34)

iIncaChimuYear = 1450
tIncaChimuTL = (40, 39)
tIncaChimuBR = (42, 43)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
iConquestNum, tConquestIncaWari = processConquest(iConquestNum, iInca, iWari, tIncaWariTL, tIncaWariBR, 3, iIncaWariYear, 10)
iConquestNum, tConquestIncaTiwanaku = processConquest(iConquestNum, iInca, iTiwanaku, tIncaTiwanakuTL, tIncaTiwanakuBR, 2, iIncaTiwanakuYear, 10)
iConquestNum, tConquestIncaChimu = processConquest(iConquestNum, iInca, iChimu, tIncaChimuTL, tIncaChimuBR, 3, iIncaChimuYear, 10)

# Spain ------------------------------------------------------------------------------------------------------------------------
iSpainAztecsYear = 1519
tSpainAztecsTL = (22, 66)
tSpainAztecsBR = (26, 69)

iSpainPurepechansYear = 1522
tSpainPurepechansTL = (18, 66)
tSpainPurepechansBR = (21, 69)

iSpainZapotecYear = 1527
tSpainZapotecTL = (24, 63)
tSpainZapotecBR = (29, 65)

iSpainIncaYear = 1532
tSpainIncaTL = (45, 32)
tSpainIncaBR = (49, 37)

iSpainWariYear = 1532
tSpainWariTL = (41, 36)
tSpainWariBR = (46, 42)

iSpainChimuYear = 1532
tSpainChimuTL = (40, 39)
tSpainChimuBR = (43, 46)

iSpainMuiscaYear = 1537
tSpainMuiscaTL = (47, 49)
tSpainMuiscaBR = (50, 54)

iSpainPuebloYear = 1598
tSpainPuebloTL = (16, 81)
tSpainPuebloBR = (22, 86)

iSpainMayaYear = 1697
tSpainMayaTL = (32, 64)
tSpainMayaBR = (38, 70)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
iConquestNum, tConquestSpainAztecs = processConquest(iConquestNum, iSpain, iAztec, tSpainAztecsTL, tSpainAztecsBR, 2, iSpainAztecsYear, 10)
iConquestNum, tConquestSpainPurepechans = processConquest(iConquestNum, iSpain, iPurepecha, tSpainPurepechansTL, tSpainPurepechansBR, 1, iSpainPurepechansYear, 10)
iConquestNum, tConquestSpainZapotec = processConquest(iConquestNum, iSpain, iZapotec, tSpainZapotecTL, tSpainZapotecBR, 1, iSpainZapotecYear, 10)
iConquestNum, tConquestSpainInca = processConquest(iConquestNum, iSpain, iInca, tSpainIncaTL, tSpainIncaBR, 3, iSpainIncaYear, 10)
iConquestNum, tConquestSpainWari = processConquest(iConquestNum, iSpain, iWari, tSpainWariTL, tSpainWariBR, 1, iSpainWariYear, 10)
iConquestNum, tConquestSpainChimu = processConquest(iConquestNum, iSpain, iChimu, tSpainChimuTL, tSpainChimuBR, 1, iSpainChimuYear, 10)
iConquestNum, tConquestSpainMuisca = processConquest(iConquestNum, iSpain, iMuisca, tSpainMuiscaTL, tSpainMuiscaBR, 2, iSpainMuiscaYear, 10)
iConquestNum, tConquestSpainPueblo = processConquest(iConquestNum, iSpain, iPueblo, tSpainPuebloTL, tSpainPuebloBR, 2, iSpainPuebloYear, 10)
iConquestNum, tConquestSpainMaya = processConquest(iConquestNum, iSpain, iMaya, tSpainMayaTL, tSpainMayaBR, 1, iSpainMayaYear, 10)

# England ------------------------------------------------------------------------------------------------------------------------
iEnglandNetherlandsYear = 1670
tEnglandNetherlandsTL = (47, 90)
tEnglandNetherlandsBR = (49, 92)

iEnglandQuebecYear = 1758
tEnglandQuebecTL = (54, 45)
tEnglandQuebecBR = (53, 101)

iEnglandAmerica1812WashingtonYear = 1814
tEnglandAmerica1812WashingtonTL = (44, 85)
tEnglandAmerica1812WashingtonBR = (47, 89)

iEnglandAmerica1812NewOrleansYear = 1815
tEnglandAmerica1812NewOrleansTL = (32, 78)
tEnglandAmerica1812NewOrleansBR = (35, 80)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
iConquestNum, tConquestEnglandNetherlands = processConquest(iConquestNum, iEngland, iNetherlands, tEnglandNetherlandsTL, tEnglandNetherlandsBR, 2, iEnglandNetherlandsYear, 10)
iConquestNum, tConquestEnglandQuebec = processConquest(iConquestNum, iEngland, iFrance, tEnglandQuebecTL, tEnglandQuebecBR, 2, iEnglandQuebecYear, 10)
iConquestNum, tConquestEngland1812Washington = processConquest(iConquestNum, iEngland, iAmerica, tEnglandAmerica1812WashingtonTL, tEnglandAmerica1812WashingtonBR, 1, iEnglandAmerica1812WashingtonYear, 10)
iConquestNum, tConquestEngland1812NewOrleans = processConquest(iConquestNum, iEngland, iAmerica, tEnglandAmerica1812NewOrleansTL, tEnglandAmerica1812NewOrleansBR, 1, iEnglandAmerica1812NewOrleansYear, 10)

# France ------------------------------------------------------------------------------------------------------------------------
iFranceMexicoYear = 1861
tFranceMexicoTL = (23, 66)
tFranceMexicoBR = (28, 71)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
iConquestNum, tConquestFranceMexico = processConquest(iConquestNum, iFrance, iMexico, tFranceMexicoTL, tFranceMexicoBR, 3, iFranceMexicoYear, 10)

# Netherlands --------------------------------------------------------------------------------------------------------------------
iNetherlandsNorseYear = 1655
tNetherlandsNorseTL = (45, 88)
tNetherlandsNorseBR = (48, 92)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
iConquestNum, tConquestNetherlandsNorse = processConquest(iConquestNum, iEngland, iNetherlands, tNetherlandsNorseTL, tNetherlandsNorseBR, 1, iNetherlandsNorseYear, 10)

# America ------------------------------------------------------------------------------------------------------------------------
iAmericaHaudenosauneeYear = 1783
tAmericaHaudenosauneeTL = (43, 91)
tAmericaHaudenosauneeBR = (46, 94)

iAmericaCanadaYear = 1812
tAmericaCanadaTL = (40, 93)
tAmericaCanadaBR = (51, 100)

iAmericaCherokeeYear = 1839
tAmericaCherokeeTL = (37, 81)
tAmericaCherokeeBR = (41, 86)

iAmericaMexicoYear = 1846
tAmericaMexicoTL = (16, 79)
tAmericaMexicoBR = (25, 89)

iAmericaCSAYear = 1863
tAmericaCSATL = (21, 74)
tAmericaCSABR = (46, 88)

iAmericaLakotkaYear = 1875
tAmericaLakotkaTL = (21, 92)
tAmericaLakotkaBR = (30, 99)

iAmericaApacheYear = 1886
tAmericaApacheTL = (23, 81)
tAmericaApacheBR = (32, 87)

iAmericaCubaYear = 1898
tAmericaCubaTL = (40, 68)
tAmericaCubaBR = (51, 72)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
iConquestNum, tConquestAmericaHaudenosaunee = processConquest(iConquestNum, iAmerica, iHaudenosaunee, tAmericaHaudenosauneeTL, tAmericaHaudenosauneeBR, 2, iAmericaHaudenosauneeYear, 10)
iConquestNum, tConquestAmericaCanada = 	      processConquest(iConquestNum, iAmerica, iCanada, tAmericaCanadaTL, tAmericaCanadaBR, 2, iAmericaCanadaYear, 10)
iConquestNum, tConquestAmericaCherokee =      processConquest(iConquestNum, iAmerica, iCherokee, tAmericaCherokeeTL, tAmericaCherokeeBR, 2, iAmericaCherokeeYear, 10)
iConquestNum, tConquestAmericaMexico = 	      processConquest(iConquestNum, iAmerica, iMexico, tAmericaMexicoTL, tAmericaMexicoBR, 4, iAmericaMexicoYear, 10)
iConquestNum, tConquestAmericaCSA = 	      processConquest(iConquestNum, iAmerica, iCSA, tAmericaCSATL, tAmericaCSABR, 10, iAmericaCSAYear, 10)
iConquestNum, tConquestAmericaLakota = 	      processConquest(iConquestNum, iAmerica, iLakota, tAmericaLakotkaTL, tAmericaLakotkaBR, 4, iAmericaLakotkaYear, 10)
iConquestNum, tConquestAmericaApache = 	      processConquest(iConquestNum, iAmerica, iApache, tAmericaApacheTL, tAmericaApacheBR, 3, iAmericaApacheYear, 10)
iConquestNum, tConquestAmericaCuba = 	      processConquest(iConquestNum, iAmerica, iSpain, tAmericaCubaTL, tAmericaCubaBR, 3, iAmericaCubaYear, 10)

# Canada ------------------------------------------------------------------------------------------------------------------------
iCanadaLakotaYear = 1880
tCanadaLakotaTL = (18, 99)
tCanadaLakotaBR = (30, 105)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
iConquestNum, tConquestCanadaLakota = processConquest(iConquestNum, iCanada, iLakota, tCanadaLakotaTL, tCanadaLakotaBR, 2, iCanadaLakotaYear, 10)


lConquests = [tConquestIncaWari, tConquestIncaTiwanaku, tConquestIncaChimu, # 3
tConquestSpainAztecs, tConquestSpainPurepechans, tConquestSpainZapotec, tConquestSpainInca, tConquestSpainWari, tConquestSpainChimu, tConquestSpainMuisca, tConquestSpainPueblo, tConquestSpainMaya, # 9
tConquestEnglandNetherlands, tConquestEnglandQuebec, tConquestEngland1812Washington, tConquestEngland1812NewOrleans, # 4
tConquestFranceMexico, # 1
tConquestNetherlandsNorse, # 1
tConquestAmericaHaudenosaunee, tConquestAmericaCanada, tConquestAmericaCherokee, tConquestAmericaMexico, tConquestAmericaCSA, tConquestAmericaLakota, tConquestAmericaApache, tConquestAmericaCuba, # 8
tConquestCanadaLakota] # 1


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
def checkTargetMinors():
	targetMinors()


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
	
	# MacAurther: Why single out Spain? So sad
	# if iCiv == iSpain and (iPreferredTarget < 0 or player(iPreferredTarget).isHuman()):
	# 	return
	
	iStartTurn = year(iYear) + max(turns(data.iSeed % 10 - 5), 0)	# MacAurther: Don't let year be early
	
	if turn() == iStartTurn - turns(5):
		warnConquest(iPlayer, iCiv, iPreferredTargetCiv, tTL, tBR)
	
	if turn() < player(iCiv).getLastBirthTurn(): # MacAurther: Allow conquerors for new civs
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
			iAttack: 2 + iExtra,
			iShock: 1 + iExtra,
			iCitySiege: 1 + 2*iExtra,
		}
		units = createRoleUnits(iPlayer, tPlot, dConquestUnits.items())
		
		units.promotion(iVolunteer)


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


def targetMinors():
	for iPlayer in players.major().ai().existing().periodic_iter(10):
		if players.major().existing().any(lambda p: team(iPlayer).isAtWar(player(p).getTeam())):
			continue
	
		if players.major().existing().any(lambda p: team(iPlayer).AI_getWarPlan(player(p).getTeam()) != WarPlanTypes.NO_WARPLAN):
			continue
		
		for city in cities.all().where(is_minor).revealed(iPlayer):
			if team(iPlayer).isAtWar(city.getTeam()):
				continue
		
			if plot(city).getPlayerSettlerValue(iPlayer) >= 5 or plot(city).getPlayerWarValue(iPlayer) >= 2:
				declareWar(iPlayer, city.getOwner(), WarPlanTypes.WARPLAN_LIMITED)
				break


def determineAttackingPlayer():
	return players.major().existing().where(isNotPlanning).where(possibleTargets).maximum(lambda p: data.players[p].iAggressionLevel)


def possibleTargets(iPlayer):
	return players.major().existing().without(iPlayer).where(lambda p: team(iPlayer).canDeclareWar(player(p).getTeam()))


def isNotPlanning(iPlayer):
	return players.major().existing().without(iPlayer).all(lambda p: team(iPlayer).AI_getWarPlan(player(p).getTeam()) == -1)


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
			dTargetValues[iOwner] += plot.getPlayerWarValue(iPlayer)
				
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