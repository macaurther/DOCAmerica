from Events import handler
from RFCUtils import *
from Core import *
from Locations import *
from Stability import *
from Popups import popup
from Scenarios import SCENARIOS


dRelocatedCapitals = CivDict({
})

dCapitalInfrastructure = CivDict({
})

# List of plots where Tribes are not allowed to spawn, usually because it randomly makes a UHV impossible/very difficult
lBannedTribePlots = [
	(42, 43),		# Cotton for Wari
	(44, 41),		# Wari Alley
	(44, 42),		# Wari Alley
	(44, 43),		# Gold for Wari
	(46, 51),		# 1st Gold for Muisca
	(50, 53),		# 2nd Gold for Muisca
	(51, 50),		# 2nd Corn for Muisca
	(21, 81),		# Sante Fe for Pueblo
]

# Minimum number of Tribes guaranteed to spawn in each region.
# A region-specific pressure score builds as the region is traversed and resets
# each time a tribe is placed, driving placement when global score alone falls short.
dRegionMinTribes = {
	rHawaii: 3,
}

@handler("GameStart")
def updateCulture():
	for plot in plots.all():
		plot.updateCulture()

# Debug Prints
@handler("GameStart")
def debugPrints():
	if False:
		for iBuilding in range(iNumBuildings):
			print("iBuilding " + str(iBuilding) + " corresponds to XML entry: " + unicode(gc.getBuildingInfo(iBuilding).getDescription()))


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
		
 	# Skip over banned plots
	for tBannedPlot in lBannedTribePlots:
		lProhibitedPlots.append(plot(tBannedPlot[0], tBannedPlot[1]))

	# Make sure capital vicinity is clear for all civs
	for iCiv in dCapitals.keys():
		for i in range(-1,2):
			for j in range(-1,2):
				if dCapitals[iCiv][0]+i > iWorldX or dCapitals[iCiv][0]+i < 0 or dCapitals[iCiv][1]+j > iWorldY or dCapitals[iCiv][1]+j < 0:
					continue
				lProhibitedPlots.append(plot((dCapitals[iCiv][0]+i, dCapitals[iCiv][1]+j)))

	# Pre-count viable plots per tracked region and initialise per-region tracking
	dRegionRemainingTribes = dict(dRegionMinTribes)
	dRegionScore       = dict((r, 0) for r in dRegionMinTribes)
	dRegionViablePlots = dict(
		(r, sum(1 for p in plots.region(r)
		        if p.getOwner() == PlayerTypes.NO_PLAYER and not p.isWater() and not p.isImpassable()))
		for r in dRegionMinTribes
	)

	# Look at 3 rows and 3 cols at a time
	for y in range(0, iWorldY, 3):
		for x in range(0, iWorldX, 3):
			for y_ in range(y, min(y+3, iWorldY)):
				for x_ in range(x, min(x+3, iWorldX)):
					pPlot = plot(x_,y_)

					# Skip over owned tiles and water, and peaks
					if pPlot.getOwner() != PlayerTypes.NO_PLAYER or pPlot.isWater() or pPlot.isImpassable():
						continue

					# Region minimum tracking
					iPlotRegion    = pPlot.getRegionID()
					bTrackedRegion = iPlotRegion in dRegionMinTribes and dRegionRemainingTribes[iPlotRegion] > 0
					if bTrackedRegion:
						dRegionViablePlots[iPlotRegion] -= 1

					# Skip over prohibited tiles
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
							iQueuedPlotRegion = pPlot.getRegionID()
							if iQueuedPlotRegion in dRegionMinTribes and dRegionRemainingTribes[iQueuedPlotRegion] > 0:
								dRegionScore[iQueuedPlotRegion] = 0
								dRegionRemainingTribes[iQueuedPlotRegion] -= 1
						continue

					# Compute effective score: global score plus region pressure bonus
					iEffectiveScore = iScore
					if bTrackedRegion:
						iViableLeft      = max(dRegionViablePlots[iPlotRegion], 1)
						iEffectiveScore += dRegionScore[iPlotRegion] * dRegionRemainingTribes[iPlotRegion] / iViableLeft

					# Check if Tribe is earned if the current score is nonzero
					if iEffectiveScore >= iThreshold and iCurrScore > 0:
						if isTribeAdjacent(x_, y_):
							iQueuedTribes += 1
						else:
							spawnTribe(pPlot)
							if bTrackedRegion:
								dRegionScore[iPlotRegion] = 0
								dRegionRemainingTribes[iPlotRegion] -= 1

						iScore -= iThreshold
					elif bTrackedRegion:
						dRegionScore[iPlotRegion] += iCurrScore
			
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

# Help colonial AI by giving a Native Tech when conquering native cities (mostly helping Spain)
# MacAurther TODO: Make AI better so this isn't needed
@handler("cityAcquired")
def nativeTechOnConquest(iOwner, iPlayer, city):
	if not player(iPlayer).isHuman():
		if city.getPreviousCiv() in dCivGroups[iCivGroupNative] + [iIndigenous, iIndependent1]:
			for iTech in lNativeTechs:
				if not team(iPlayer).isHasTech(iTech):
					team(iPlayer).setHasTech(iTech, True, iPlayer, False, False)
					return

### FIRST CITY ###



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

### CITY BUILT ###

@handler("cityBuilt")
def relocateFoundedCapital(city):
	relocateCapitals(city.getOwner(), city)


@handler("cityBuilt")
def buildFoundedCapitalInfrastructure(city):
	buildCapitalInfrastructure(city.getOwner(), city)

### UNIT BUILT ###

### FIRST CONTACT ###

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
				createRoleUnit(iPlayer, plot, iCityAttack, 3)
				createRoleUnit(iPlayer, plot, iCitySiege, 2)
				
				message(city.getOwner(), "TXT_KEY_MESSAGE_AMERICAN_WEST_COAST_CONQUERORS", adjective(iPlayer), city.getName(), color=iRed, location=city, button=infos.unit(iMinuteman).getButton())
				
		if enemyCities.count() < 2:
			for plot in plots.of(lWestCoast).without(enemyCities).sample(2 - enemyCities.count()):
				createRoleUnit(iPlayer, plot, iSettle)
				createRoleUnit(iPlayer, plot, iDefend)


### COLLAPSE ###


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
		makeUnit(iPlayer, unique_unit(iPlayer, iMerchantman), seaPlot)