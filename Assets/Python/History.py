from Events import handler
from RFCUtils import *
from Core import *
from Locations import *
from Stability import *
from Popups import popup
from Scenarios import SCENARIOS
import CvScreensInterface


dRelocatedCapitals = CivDict({
})

dCapitalInfrastructure = CivDict({
})

@handler("GameStart")
def updateCulture():
	for plot in plots.all():
		plot.updateCulture()

@handler("GameStart")
def placeTribes():
	iScore = 0
	iThreshold = 100
	iQueuedTribes = 0	# Number of tribes to place ASAP

	# Aggregate prohibited tiles
	lProhibitedPlots = []

	# no Tribes in Iceland
	for pPlot in plots.region(rIceland):
		lProhibitedPlots.append(pPlot)

	# Make sure capital vicinity is clear for all civs
	for iCiv in dCapitals.keys():
		for i in range(-1,2):
			for j in range(-1,2):
				if dCapitals[iCiv][0]+i > iWorldX or dCapitals[iCiv][0]+i < 0 or dCapitals[iCiv][1]+j > iWorldY or dCapitals[iCiv][1]+j < 0:
					continue
				lProhibitedPlots.append(plot((dCapitals[iCiv][0]+i, dCapitals[iCiv][1]+j)))

	# Look at 3 rows and 3 cols at a time
	for y in range(0, iWorldY, 3):
		for x in range(0, iWorldX, 3):
			for y_ in range(y, min(y+3, iWorldY)):
				for x_ in range(x, min(x+3, iWorldX)):
					pPlot = plot(x_,y_)

					# Skip over owned tiles and water, and peaks
					if pPlot.getOwner() != PlayerTypes.NO_PLAYER or pPlot.isWater() or pPlot.isImpassable():
						continue

					# Skip over capital tiles
					bProhibited = False
					for pNoPlot in lProhibitedPlots:
						if pPlot.getX() == pNoPlot.getX() and pPlot.getY() == pNoPlot.getY():
							bProhibited = True
							break

					# Accumulate
					iCurrScore = pPlot.calculateNatureYield(YieldTypes.YIELD_FOOD, TeamTypes.NO_TEAM, False) * 3
					iCurrScore += pPlot.calculateNatureYield(YieldTypes.YIELD_PRODUCTION, TeamTypes.NO_TEAM, False) * 2
					iCurrScore += pPlot.calculateNatureYield(YieldTypes.YIELD_COMMERCE, TeamTypes.NO_TEAM, False)
					if pPlot.getBonusType(TeamTypes.NO_TEAM) != BonusTypes.NO_BONUS: iCurrScore += 5		# Incentivize bonuses

					iScore += iCurrScore
					
					iScore += CyGame().getSorenRandNum(2, "Tribe Placement")	# Random score insertion

					# If prohibited, still accumulate, but skip placement		
					if bProhibited:
						continue

					# Check if queue tribe
					if iQueuedTribes > 0:
						if not isTribeAdjacent(x_, y_):
							spawnTribe(pPlot)
							iQueuedTribes -= 1
						continue

					# Check if Tribe is earned if the current score is nonzero
					if iScore >= iThreshold and iCurrScore > 0:
						if isTribeAdjacent(x_, y_):
							iQueuedTribes += 1
						else:
							spawnTribe(pPlot)
						
						iScore -= iThreshold
			
def spawnTribe(pPlot):
	pPlot.setImprovementType(iTribe)
	# Give some initial defenders
	pPlot.setTribeStoredUnits(2)
	pPlot.setCulture(slot(iIndigenous), 100, True)

def isTribeAdjacent(x, y):
	for i in range(-1,2):
		for j in range(-1,2):
			if x+i > iWorldX or x+i < 0 or y+j > iWorldY or y+j < 0:
				continue
			if plot(x+i,y+j).getImprovementType() in [iTribe, iContactedTribe]:
				return True
	return False


### CITY ACQUIRED ###

@handler("cityAcquired")
def relocateAcquiredCapital(iOwner, iPlayer, city):
	relocateCapitals(iPlayer, city)


@handler("cityAcquired")
def buildAcquiredCapitalInfrastructure(iOwner, iPlayer, city):
	buildCapitalInfrastructure(iPlayer, city)


### FIRST CITY ###

@handler("firstCity")
def setupMexicoCity(city):
	if civ(city) == iMexico:
		if city.at(*tTenochtitlan):
			if game.getBuildingClassCreatedCount(infos.building(iFloatingGardens).getBuildingClassType()) == 0:
				city.setHasRealBuilding(iFloatingGardens, True)
			
			iStateReligion = player(city).getStateReligion()
			if iStateReligion >= 0 and city.isHasReligion(iStateReligion):
				city.setHasRealBuilding(monastery(iStateReligion), True)


### BEGIN GAME TURN ###

@handler("BeginGameTurn")
def defendTribes(iGameTurn):
	# Every 5 turns, attempt to replenish tribes' forces
	if iGameTurn % scale(5) == 0 and iGameTurn > 0:
		iHandicap = infos.handicap().getBarbarianSpawnModifier()
		iMaxUnits = 2 + iHandicap
		if year() > year(1): iMaxUnits += 1
		if year() > year(1000): iMaxUnits += 1
		if year() > year(1500): iMaxUnits += 1
		if year() > year(1750): iMaxUnits += 1

		for y in range(0, iWorldY):
			for x in range(0, iWorldX):
				pPlot = plot(x,y)
				if pPlot.getImprovementType() in [iTribe, iContactedTribe]:
					replenishTribe(pPlot, iMaxUnits)

					# If it has been a while since the tribe was threatened, pack units back in
					if(pPlot.getTribeThreatenTurn() + 8 < iGameTurn):
						for i in range(pPlot.getNumUnits()-1, -1, -1):
							pUnit = pPlot.getUnit(i)
							if civ(pUnit) == iIndigenous:
								pUnit.kill(False, -1)
								pPlot.setTribeStoredUnits(pPlot.getTribeStoredUnits() + 1)

def replenishTribe(pPlot, iMaxUnits):
	iNumIndigenous = 0
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if player(pUnit.getOwner()).getCivilizationType() == iIndigenous:
			iNumIndigenous += 1
	if iNumIndigenous + pPlot.getTribeStoredUnits() < iMaxUnits:
		pPlot.setTribeStoredUnits(pPlot.getTribeStoredUnits() + 1)


@handler("BeginGameTurn")
def expeditionaryForce(iGameTurn):
	for iRevolutionaryCiv in lRevolutionaries:
		if turn() != year(dBirth[iRevolutionaryCiv]) + 1:
			continue

		iRevolutionaryPlayer = slot(iRevolutionaryCiv)
		
		# Only run if revolutionary civ is Human
		if not player(iRevolutionaryPlayer).isHuman():
			return

		if iRevolutionaryCiv == iAmerica:
			tExpeditionarySpawn = (45, 84)
			iExpeditionaryPlayer = slot(iEngland)
		elif iRevolutionaryCiv == iHaiti:
			tExpeditionarySpawn = (36, 56)
			iExpeditionaryPlayer = slot(iFrance)
		# The Spanish revolutionary wars were more about taking land away from Spain instead of a Spanish expeditionary force, so I guess this doesn't really fit for them
		# Also, at least in the 1750 AD Scenario, Spain is pretty buff already
		#elif iRevolutionaryCiv == iArgentina:
		#	tExpeditionarySpawn = (23, 8)
		#	iExpeditionaryPlayer = slot(iSpain)
		#elif iRevolutionaryCiv == iMexico:
		#	tExpeditionarySpawn = (16, 64)
		#	iExpeditionaryPlayer = slot(iSpain)
		#elif iRevolutionaryCiv == iColombia:
		#	tExpeditionarySpawn = (31, 48)
		#	iExpeditionaryPlayer = slot(iSpain)
		#elif iRevolutionaryCiv == iPeru:
		#	tExpeditionarySpawn = (20, 30)
		#	iExpeditionaryPlayer = slot(iSpain)
		else:
			return
		
		if iExpeditionaryPlayer == -1 or player(iExpeditionaryPlayer) is None:
			return
		
		if player(iRevolutionaryPlayer) is None:
			print("ERROR: player(iRevolutionaryPlayer) is None! iRevolutionaryPlayer: " + str(iRevolutionaryPlayer) + " iRevolutionaryCiv: " + str(iRevolutionaryCiv) + " Turn: " + str(iGameTurn))
		
		iModifier1 = 0
		iModifier2 = 0
		
		if player(iRevolutionaryPlayer).isHuman() and player(iRevolutionaryPlayer).getNumCities() > 6:
			iModifier1 = 2
		else:
			if iRevolutionaryCiv == iAmerica or player(iRevolutionaryPlayer).getNumCities() > 4:
				iModifier1 = 3
			if not player(iRevolutionaryPlayer).isHuman():
				iModifier2 = 1
				
		if year() < year(dBirth[active()]):
			iModifier1 += 1
			iModifier2 += 1
		
		# Make it easier for some civs
		if iRevolutionaryCiv in [iHaiti]:
			iModifier1 -= 1
			iModifier2 -= 1
		
		# disable birth protection if still active
		player(iRevolutionaryPlayer).setBirthProtected(False)
		for p in plots.all():
			if p.getBirthProtected() == iRevolutionaryPlayer:
				p.resetBirthProtected()
			
		team(iExpeditionaryPlayer).declareWar(iRevolutionaryPlayer, True, WarPlanTypes.WARPLAN_TOTAL)
		
		dExpeditionSeaUnits = {
			iEscortSea: 6 + iModifier1 + iModifier2,
			iFerrySea: 4 + iModifier1 + iModifier2,
		}
		
		dExpeditionUnits = {
			iBase: 6 + iModifier2,
			iCounter: 4 + iModifier1,
			iSkirmish: 4 + iModifier1 + iModifier2,
			iSiegeCity: 4 + iModifier1,
		}
		
		seaUnits = createRoleUnits(iExpeditionaryPlayer, tExpeditionarySpawn, dExpeditionSeaUnits.items())
		seaUnits.promotion(infos.type("PROMOTION_MERCENARY"))
		
		units = createRoleUnits(iExpeditionaryPlayer, tExpeditionarySpawn, dExpeditionUnits.items())
		units.promotion(infos.type("PROMOTION_MERCENARY"))
		
		if iRevolutionaryCiv == iAmerica:
			message(iRevolutionaryPlayer, 'TXT_KEY_EXPEDITIONARY_REVOLUTIONARIES_AMERICA')
		else:
			message(iRevolutionaryPlayer, 'TXT_KEY_EXPEDITIONARY_REVOLUTIONARIES')
		message(iExpeditionaryPlayer, 'TXT_KEY_EXPEDITIONARY_EXPEDITIONARIES')

### CITY BUILT ###

@handler("cityBuilt")
def relocateFoundedCapital(city):
	relocateCapitals(city.getOwner(), city)


@handler("cityBuilt")
def buildFoundedCapitalInfrastructure(city):
	buildCapitalInfrastructure(city.getOwner(), city)


# MacAurther: Help European AI by removing nearby Tribes when they settle cities
@handler("cityBuilt")
def convertTribesAroundCity(pCity):
	iPlayer = pCity.getOwner()
	if not player(iPlayer).isHuman() and player(iPlayer).getCivilizationType() in dCivGroups[iCivGroupEurope]:
		for i in range(gc.getNUM_CITY_PLOTS()):
			pPlot = pCity.getCityIndexPlot(i)
			if pPlot.getImprovementType() in [iTribe, iContactedTribe]:
				pPlot.setImprovementType(-1)

### UNIT BUILT ###


### FIRST CONTACT ###

@handler("firstContact")
def conquistadors(iTeamX, iHasMetTeamY):
	if is_minor(iTeamX) or is_minor(iHasMetTeamY):
		return
	
	#if year().between(1490, 1800):
	if year().before(1700) and civ(iTeamX) in lBioNewWorld and civ(iHasMetTeamY) not in lBioNewWorld:	# MacAurther: don't trigger late conquerors
		iNewWorldPlayer = iTeamX
		iOldWorldPlayer = iHasMetTeamY
		
		iNewWorldCiv = civ(iNewWorldPlayer)
		iOldWorldCiv = civ(iOldWorldPlayer)
		
		# Don't count the Norse (they might discover natives very early)
		if iOldWorldCiv == iNorse:
			return
		
		bAlreadyContacted = data.dFirstContactConquerors[iNewWorldCiv]
		
		# Can't first contact twice
		if bAlreadyContacted:
			return
		
		# MacAurther: Spain UP: Get free units when discovering Natives
		if iOldWorldCiv == iSpain:
			# Holy mole I don't know how to write code
			CvScreensInterface.immigrationManager.hireMercenary(iConquistador, iOldWorldPlayer, iHomelandSouthEurope)

			message(iNewWorldPlayer, "TXT_KEY_FIRST_CONTACT_NEWWORLD")
			message(iOldWorldPlayer, "TXT_KEY_FIRST_CONTACT_OLDWORLD")

			# Inform the player that the mercenaries have arrived.
			strMessage = "Conquistadors are waiting on the docks of South Europe!"
			CyInterface().addMessage(iOldWorldPlayer, False, 20, strMessage, "AS2D_IMMIGRANTEARNED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, "", gc.getInfoTypeForString("COLOR_YELLOW"), -1, -1, False, False) 
		
		data.dFirstContactConquerors[iNewWorldCiv] = True

### TECH ACQUIRED ###

@handler("techAcquired")
def recordExplorationTurn(iTech, iTeam, iPlayer):
	if iTech == iExploration:
		data.players[iPlayer].iExplorationTurn = game.getGameTurn()


@handler("techAcquired")
def americanWesternSettlement(iTech, iTeam, iPlayer):
	if iTech == iRailroad and civ(iPlayer) == iAmerica and not player(iPlayer).isHuman():
		lWestCoast = plots.region(rCalifornia)
				
		enemyCities = cities.of(lWestCoast).notowner(iAmerica)
		
		for iEnemy in enemyCities.owners():
			team(iPlayer).declareWar(iEnemy, True, WarPlanTypes.WARPLAN_LIMITED)
		
		for city in enemyCities:
			plot = plots.surrounding(city).without(city).land().passable().no_enemies(iPlayer).random()
			if plot:
				createRoleUnit(iPlayer, plot, iBase, 3)
				createRoleUnit(iPlayer, plot, iSiegeCity, 2)
				
				message(city.getOwner(), "TXT_KEY_MESSAGE_AMERICAN_WEST_COAST_CONQUERORS", adjective(iPlayer), city.getName(), color=iRed, location=city, button=infos.unit(iMinuteman).getButton())
				
		if enemyCities.count() < 2:
			for plot in plots.of(lWestCoast).without(enemyCities).sample(2 - enemyCities.count()):
				makeUnit(iPlayer, iSettler, plot)
				createRoleUnit(iPlayer, plot, iBase)


### COLLAPSE ###

@handler("civicChanged")
def doAmericanCivilWar(iPlayer, iOldCivic, iNewCivic):
	if civ(iPlayer) == iAmerica and iOldCivic == iBondage and player(iPlayer).isHuman():	# Don't have AI do Civil War, it can't handle it
		secedeCitiesByRegions(iPlayer, lSouthernUS, slot(iIndependent))
		
		# Let the player decided whether or not to declare war, but make the AI declare war on secession
		'''if not player(iPlayer).isHuman():
			team(iPlayer).declareWar(slot(iIndependent), True, WarPlanTypes.WARPLAN_TOTAL)'''

### BIRTH ###
			

### FLIP ###


### IMPLEMENTATION ###

def relocateCapitals(iPlayer, city):
	if player(iPlayer).isHuman():
		return
	
	if iPlayer in dRelocatedCapitals:
		tCapital = dRelocatedCapitals[iPlayer]
		
		if location(city) == tCapital:
			relocateCapital(iPlayer, tCapital)
			

def buildCapitalInfrastructure(iPlayer, city):
	if iPlayer in dCapitalInfrastructure:
		if at(city, plots.capital(iPlayer)) and year() <= year(dBirth[iPlayer]) + turns(5):
			iPopulation, lBuildings, lReligiousBuildings = dCapitalInfrastructure[iPlayer]
			
			if city.getPopulation() < iPopulation:
				city.setPopulation(iPopulation)
			
			for iBuilding in lBuildings:
				city.setHasRealBuilding(iBuilding, True)
			
			iStateReligion = player(iPlayer).getStateReligion()
			if iStateReligion >= 0:
				for religiosBuilding in lReligiousBuildings:
					city.setHasRealBuilding(religiosBuilding(iStateReligion), True)

def giveRaiders(iCiv):
	pPlayer = player(iCiv)
	pTeam = team(iCiv)
	
	if pPlayer.isAlive() and not pPlayer.isHuman():
		city = cities.owner(iCiv).coastal().random()
		if city:
			seaPlot = findSeaPlots(location(city), 1, iCiv)
			if seaPlot:
				makeUnit(iCiv, unique_unit(iCiv, iGalley), seaPlot, UnitAITypes.UNITAI_ASSAULT_SEA)
				if pTeam.isHasTech(iSteel):
					makeUnit(iCiv, unique_unit(iCiv, iHeavySwordsman), seaPlot, UnitAITypes.UNITAI_ATTACK)
					makeUnit(iCiv, unique_unit(iCiv, iHeavySwordsman), seaPlot, UnitAITypes.UNITAI_ATTACK_CITY)
				else:
					makeUnit(iCiv, unique_unit(iCiv, iSwordsman), seaPlot, UnitAITypes.UNITAI_ATTACK)
					makeUnit(iCiv, unique_unit(iCiv, iSwordsman), seaPlot, UnitAITypes.UNITAI_ATTACK_CITY)

def acceptColonialAcquisition(iPlayer):
	for city in data.players[iPlayer].colonialAcquisitionCities:
		if city.isHuman():
			colonialAcquisition(iPlayer, city)
			
	player().changeGold(data.players[iPlayer].colonialAcquisitionCities.count() * 200)

def refuseColonialAcquisition(iPlayer):
	for city in data.players[iPlayer].colonialAcquisitionCities:
		if city.isHuman():
			colonialConquest(iPlayer, city)

colonialAcquisitionPopup = popup.text("TXT_KEY_ASKCOLONIALCITY_MESSAGE") \
							.option(acceptColonialAcquisition, "TXT_KEY_POPUP_YES") \
							.option(refuseColonialAcquisition, "TXT_KEY_POPUP_NO") \
							.build()

def handleColonialAcquisition(iPlayer):
	pPlayer = player(iPlayer)
	iCiv = civ(iPlayer)
	
	targets = getColonialTargets(iPlayer, bEmpty=True)
	if not targets:
		return
	
	iGold = targets.count() * 200
	
	targetPlayers = targets.cities().owners()
	freePlots, cityPlots = targets.split(lambda plot: not city(plot))
	
	for plot in freePlots:
		colonialAcquisition(iPlayer, plot)

	for iTarget in targetPlayers:
		if player(iTarget).isHuman():
			askedCities = cityPlots.cities().owner(iTarget)
			askedCityNames = askedCities.format(formatter=CyCity.getName)
					
			iAskGold = askedCities.count() * 200
			
			data.players[iPlayer].colonialAcquisitionCities = askedCities
			colonialAcquisitionPopup.text(adjective(iPlayer), adjective(iPlayer), iAskGold, askedCityNames) \
				.acceptColonialAcquisition() \
				.refuseColonialAcquisition() \
				.launch(iPlayer)
			
		else:
			bAccepted = is_minor(iTarget) or (rand(100) >= dPatienceThreshold[iTarget] and not team(iPlayer).isAtWar(iTarget))
			iNumCities = targets.cities().owner(iTarget).count()
					
			if iNumCities >= player(iTarget).getNumCities():
				bAccepted = False
			
			for plot in targets.cities().owner(iTarget):
				if bAccepted:
					colonialAcquisition(iPlayer, plot)
					player(iTarget).changeGold(200)
				else:
					data.timedConquest(iPlayer, location(plot))

	iNewGold = pPlayer.getGold() - iGold
	pPlayer.setGold(max(0, iNewGold))


def handleColonialConquest(iPlayer):
	targets = getColonialTargets(iPlayer)
	
	if not targets:
		handleColonialAcquisition(iPlayer)
		return

	for plot in targets:
		data.timedConquest(iPlayer, location(plot))
		
	seaPlot = plots.surrounding(targets[0]).water().random()

	if seaPlot:
		makeUnit(iPlayer, unique_unit(iPlayer, iIndiaman), seaPlot)