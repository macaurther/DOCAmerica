from Events import handler
from RFCUtils import *
from Core import *
from Locations import *
from Popups import popup
from Secession import *


dRelocatedCapitals = CivDict({
})

dCapitalInfrastructure = CivDict({
})

# Colonists - Europeans spawn at sea
dColonistSpawns = CivDict({
iNorse :		[dBirth[iNorse], tColonistReykjavik, [iColonistSettle]],
iSpain : 		[dBirth[iSpain], tColonistCaribbean, [iColonistSettle, iColonistSupport, iColonistExplore]], 
iPortugal : 	[dBirth[iPortugal], tColonistBrazil1, [iColonistSettle, iColonistSettle, iColonistExplore]],
iEngland : 		[dBirth[iEngland], tColonistVirginia, [iColonistSettle, iColonistSupport]], 
iFrance :		[dBirth[iFrance], tColonistQuebec, [iColonistSettle, iColonistSupport]],
iNetherlands : 	[dBirth[iNetherlands], tColonistNewNetherlands, [iColonistSettle, iColonistSupport]],
iRussia : 		[dBirth[iRussia], tColonistAlaska, [iColonistSettle, iColonistSupport]],
})


@handler("GameStart")
def updateCulture():
	for plot in plots.all():
		plot.updateCulture()


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
		
		# No Immigration for Norse, it makes it too easy for them! And the AI might steal Spain's contact Immigration
		if iOldWorldCiv == iNorse:
			return
		
		bAlreadyContacted = data.dFirstContactConquerors[iNewWorldCiv]
		
		# Can't first contact twice
		if bAlreadyContacted:
			return
		
		# MacAurther: The European contactor no longer gets a bunch a free units; instead, they get a bunch of Immigration points they can use to buy units from Europe			
		# Generate Immigration based on this formula:
		#   Immigration = 25 * numCities + 2 * numPops
		iContactImmigration = 0
		pNewWorldPlayer = player(iNewWorldPlayer)
		
		(pCity, iter) = pNewWorldPlayer.firstCity(false)
		while(pCity):
			iContactImmigration += pCity.getPopulation() * 5
			iContactImmigration += 20
			(pCity, iter) = pNewWorldPlayer.nextCity(iter, false)
		
		iContactImmigration *= (3 - gc.getGame().getGameSpeedType())	# Scale based on Game Speed
		
		# England UP
		if civ(iOldWorldPlayer) == iEngland:
			iContactImmigration *= 2
		
		data.dFirstContactConquerors[iNewWorldCiv] = True
		
		events.fireEvent("conquerors", iOldWorldPlayer, iNewWorldPlayer)
		
		gc.getPlayer(iOldWorldPlayer).changeImmigration(iContactImmigration)

		message(iNewWorldPlayer, "TXT_KEY_FIRST_CONTACT_NEWWORLD")
		message(iOldWorldPlayer, "TXT_KEY_FIRST_CONTACT_OLDWORLD", iContactImmigration)

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
	if civ(iPlayer) == iAmerica and iOldCivic == iSlavery3:
		secedeCitiesByRegions(iPlayer, lSouthernUS, slot(iIndependent))
		
		# Let the player decided whether or not to declare war, but make the AI declare war on secession
		if not player(iPlayer).isHuman():
			team(iPlayer).declareWar(slot(iIndependent), True, WarPlanTypes.WARPLAN_TOTAL)

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


def giveColonists(iPlayer):
	pPlayer = player(iPlayer)
	pTeam = team(iPlayer)
	iCiv = civ(iPlayer)
	
	# MacAurther: This covers starting European colonists and later colonists as well
	if (pPlayer.isAlive() or (year() <= year(dBirth[iCiv]) + 1 and year() >= year(dBirth[iCiv]) - 1)) and iCiv in dColonistSpawns:
		if pPlayer.isHuman():
			tPlot = dColonistSpawns[iCiv][1][0]
		else:
			# MacAurther: Unfortunately, the AI has a hard time with spawning at sea. So they get to spawn on land
			tPlot = dColonistSpawns[iCiv][1][1]
		
		# European starter units spawn on edge of map at Capital's Y value (Not Using because AI can't handle it on spawn)
		'''tPlotX = iWorldX - 1
		if iCiv == iRussia:
			tPlotX = 0
		tPlotY = dCapitals[iCiv][1]
		tPlot = (tPlotX, tPlotY)'''
		
		for iRole in dColonistSpawns[iCiv][2]:
			units = createRoleUnit(iPlayer, tPlot, iRole, 1)
			#units.promotion(infos.type("PROMOTION_MERCENARY"))


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