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

# Colonists - European Regional Power
dColonistSpawns = CivDict({
iNorse : 
		[[dBirth[iNorse], tColonistReykjavik, [iColonistSettle, iColonistSupport]],
		[950, tColonistReykjavik, [iColonistDefend]]],
iSpain : 
		[[dBirth[iSpain], tColonistCaribbean, [iColonistSettle, iColonistSupport, iColonistExplore]], 
		[1525, tColonistCuba, [iColonistSettle, iColonistSupport]], 
		[1565, tColonistBermuda, [iColonistSettle, iColonistSupport]], 
		[1580, tColonistArgentina, [iColonistSettle, iColonistSupport]]],
iPortugal : 
		[[dBirth[iPortugal], tColonistBrazil1, [iColonistSettle, iColonistSettle, iColonistExplore]], 
		[1550, tColonistBrazil2, [iColonistSettle, iColonistSettle, iColonistExplore]],
		[1630, tColonistBrazil2, [iColonistSlave]],
		[1730, tColonistBrazil2, [iColonistSlave]],
		[1770, tColonistBrazil1, [iColonistSlave]]],
iEngland : 
		[[dBirth[iEngland], tColonistVirginia, [iColonistSettle, iColonistSupport]], 
		[1620, tColonistMassachusetts, [iColonistSettle, iColonistSupport]], 
		[1650, tColonistNovaScotia, [iColonistSettle]],
		[1664, tColonistNewNetherlands, [iColonistConquer]],
		[1670, tColonistCarolina, [iColonistSettle, iColonistSlave]], 
		[1690, tColonistPennsylvania, [iColonistSettle]],
		[1750, tColonistCarolina, [iColonistSlave]]], 
iFrance : 
		[[dBirth[iFrance], tColonistQuebec, [iColonistSettle, iColonistSupport]], 
		[1650, tColonistQuebec, [iColonistSettle, iColonistSettle, iColonistSupport]], 
		[1718, tColonistLouisiana, [iColonistSettle, iColonistSettle, iColonistSupport]]],
iNetherlands : 
		[[dBirth[iNetherlands], tColonistNewNetherlands, [iColonistSettle, iColonistSupport]], 
		[1650, tColonistSuriname, [iColonistSettle]]],
iRussia : 
		[[dBirth[iRussia], tColonistAlaska, [iColonistSettle, iColonistSupport]],
		[1780, tColonistAlaska, [iColonistSettle, iColonistSupport]]],
})

dMaxColonists = CivDict({
iNorse : len(dColonistSpawns[iNorse]),
iSpain : len(dColonistSpawns[iSpain]),
iPortugal : len(dColonistSpawns[iPortugal]),
iEngland : len(dColonistSpawns[iEngland]), 
iFrance : len(dColonistSpawns[iFrance]),
iNetherlands : len(dColonistSpawns[iNetherlands]),
iRussia : len(dColonistSpawns[iRussia]),
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


# MacAurther: Help AI by removing nearby Tribes when they settle cities
@handler("cityBuilt")
def convertTribesAroundCity(pCity):
	iPlayer = pCity.getOwner()
	if not player(iPlayer).isHuman() and player(iPlayer).getCivilizationType() != iIroquois:	# Don't make AI Iroquois sad
		for i in range(gc.getNUM_CITY_PLOTS()):
			pPlot = pCity.getCityIndexPlot(i)
			if pPlot.getImprovementType() in [iTribe, iContactedTribe]:
				pPlot.setImprovementType(iCottage)

# MacAurther: Inuit UP
@handler("cityBuilt")
def inuitUP(pCity):
	iPlayer = pCity.getOwner()
	if player(iPlayer).getCivilizationType() == iInuit:
		for i in range(gc.getNUM_CITY_PLOTS()):
			pPlot = pCity.getCityIndexPlot(i)
			if pPlot.getImprovementType() == -1 and pPlot.getBonusType(player(iPlayer).getTeam()) in [iFur, iDeer]:
				pPlot.setImprovementType(iCamp)

### UNIT BUILT ###


### BEGIN GAME TURN ###
@handler("BeginGameTurn")
def checkColonists():
	if year().between(1500, 1800) or turn() == turn(dColonistSpawns[iNorse][1][0]):	# Special check for Norse spawn, don't need to check otherwise
		for iCiv in dCivGroups[iCivGroupEurope]:
			if player(iCiv).isAlive():
				iPlayer = slot(iCiv)
				if data.players[iPlayer].iColonistsAlreadyGiven < dMaxColonists[iCiv]:
					if turn() == turn(dColonistSpawns[iCiv][data.players[iPlayer].iColonistsAlreadyGiven][0]):
						giveColonists(iPlayer)

### FIRST CONTACT ###

@handler("firstContact")
def conquistadors(iTeamX, iHasMetTeamY):
		if is_minor(iTeamX) or is_minor(iHasMetTeamY):
			return
		
		if year().between(1490, 1800):
			if civ(iTeamX) in lBioNewWorld and civ(iHasMetTeamY) not in lBioNewWorld:
				iNewWorldPlayer = iTeamX
				iOldWorldPlayer = iHasMetTeamY
				
				iNewWorldCiv = civ(iNewWorldPlayer)
				
				bAlreadyContacted = data.dFirstContactConquerors[iNewWorldCiv]
				
				if not bAlreadyContacted:
					if iNewWorldCiv == iMaya:
						tContactZoneTL = (31, 53)
						tContactZoneBR = (42, 65)
						tContactPlot = (37, 59)
					elif iNewWorldCiv == iTeotihuacan:
						tContactZoneTL = (25, 54)
						tContactZoneBR = (40, 66)
						tContactPlot = (30, 63)
					elif iNewWorldCiv == iTiwanaku:
						tContactZoneTL = (47, 24)
						tContactZoneBR = (57, 37)
						tContactPlot = (50, 32)
					elif iNewWorldCiv == iWari:
						tContactZoneTL = (40, 29)
						tContactZoneBR = (57, 45)
						tContactPlot = (45, 38)
					#elif iNewWorldCiv == iMuisca:
					#	tContactZoneTL = (43, 42)
					#	tContactZoneBR = (56, 56)
					#	tContactPlot = (51, 51)
					elif iNewWorldCiv == iChimu:
						tContactZoneTL = (40, 31)
						tContactZoneBR = (52, 48)
						tContactPlot = (44, 41)
					elif iNewWorldCiv == iAztecs:
						tContactZoneTL = (23, 54)
						tContactZoneBR = (40, 67)
						tContactPlot = (31, 61)
					elif iNewWorldCiv == iInca:
						tContactZoneTL = (40, 13)
						tContactZoneBR = (57, 45)
						tContactPlot = (46, 36)
					else:
						return	# Some natives don't generate conquerors
						
					lArrivalExceptions = []
						
					data.dFirstContactConquerors[iNewWorldCiv] = True
					
					events.fireEvent("conquerors", iOldWorldPlayer, iNewWorldPlayer)
					
					newWorldPlots = plots.start(tContactZoneTL).end(tContactZoneBR).without(lArrivalExceptions)
					contactPlots = newWorldPlots.where(lambda p: p.isVisible(iNewWorldPlayer, False) and p.isVisible(iOldWorldPlayer, False))
					arrivalPlots = newWorldPlots.owner(iNewWorldPlayer).where(lambda p: not p.isCity() and isFree(iOldWorldPlayer, p, bCanEnter=True) and map.getArea(p.getArea()).getCitiesPerPlayer(iNewWorldPlayer) > 0)
					
					# MacAurther: if OldWorldPlayer meets an AI NewWorldPlayer before seeing their territory, spawn the OldWorldPlayer's units on a pre-determined plot. This is to prevent random units/work boats cancelling the Conquistadors event
					if not player(iNewWorldPlayer).isHuman() and not contactPlots:
						contactPlots = plots.start(tContactPlot).end(tContactPlot)
					
					if contactPlots and arrivalPlots:
						contactPlot = contactPlots.random()
						arrivalPlot = arrivalPlots.closest(contactPlot)
						
						iModifier1 = 0
						iModifier2 = 0
						
						if player(iNewWorldPlayer).isHuman() and player(iNewWorldPlayer).getNumCities() > 6:
							iModifier1 = 1
						else:
							if iNewWorldCiv == iInca or player(iNewWorldPlayer).getNumCities() > 4:
								iModifier1 = 1
							if not player(iNewWorldPlayer).isHuman():
								iModifier2 = 1
								
						if year() < year(dBirth[active()]):
							iModifier1 += 1
							iModifier2 += 1
						
						# Help AI
						if not player(iOldWorldPlayer).isHuman():
							iModifier1 += 1
							iModifier2 += 1
						
						# disable birth protection if still active
						player(iNewWorldPlayer).setBirthProtected(False)
						for p in plots.all():
							if p.getBirthProtected() == iNewWorldPlayer:
								p.resetBirthProtected()
							
						team(iOldWorldPlayer).declareWar(iNewWorldPlayer, True, WarPlanTypes.WARPLAN_TOTAL)
						
						dConquerorUnits = {
							iBase: 1 + iModifier2,
							iCounter: 2,
							iSiegeCity: 1 + iModifier1 + iModifier2,
							iShockCav: 2 + iModifier1,
						}
						units = createRoleUnits(iOldWorldPlayer, arrivalPlot, dConquerorUnits.items())
						units.promotion(infos.type("PROMOTION_MERCENARY"))
						
						if iNewWorldCiv == iInca:
							makeUnits(iOldWorldPlayer, iAucac, arrivalPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
						elif iNewWorldCiv == iAztecs:
							makeUnits(iOldWorldPlayer, iJaguar, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
							makeUnit(iOldWorldPlayer, iHolkan, arrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY)
						elif iNewWorldCiv == iMaya:
							makeUnits(iOldWorldPlayer, iHolkan, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
							makeUnit(iOldWorldPlayer, iJaguar, arrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY)
							
						message(iNewWorldPlayer, 'TXT_KEY_FIRST_CONTACT_NEWWORLD')
						message(iOldWorldPlayer, 'TXT_KEY_FIRST_CONTACT_OLDWORLD')

### REVOLUTION ###
def expeditionaryForce(iRevolutionaryPlayer):
	if civ(iRevolutionaryPlayer) in lRevolutionaries:
		iRevolutionaryCiv = civ(iRevolutionaryPlayer)
		bAlreadyExpeditioned = data.dExpeditionaryConquerors[iRevolutionaryCiv]
		
		if not bAlreadyExpeditioned:
			if iRevolutionaryCiv == iAmerica:
				tExpeditionarySpawn = (66, 81)
				iExpeditionaryPlayer = slot(iEngland)
			elif iRevolutionaryCiv == iHaiti:
				tExpeditionarySpawn = (56, 65)
				iExpeditionaryPlayer = slot(iFrance)
			elif iRevolutionaryCiv == iArgentina:
				tExpeditionarySpawn = (66, 13)
				iExpeditionaryPlayer = slot(iSpain)
			elif iRevolutionaryCiv == iMexico:
				tExpeditionarySpawn = (37, 65)
				iExpeditionaryPlayer = slot(iSpain)
			elif iRevolutionaryCiv == iColombia:
				tExpeditionarySpawn = (45, 56)
				iExpeditionaryPlayer = slot(iSpain)
			elif iRevolutionaryCiv == iPeru:
				tExpeditionarySpawn = (41, 32)
				iExpeditionaryPlayer = slot(iSpain)
			else:
				return
		
		data.dExpeditionaryConquerors[iRevolutionaryCiv] = True
		
		if iExpeditionaryPlayer == -1 or player(iExpeditionaryPlayer) is None:
			return
		
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
		
		if iRevolutionaryCiv == iHaiti or iRevolutionaryCiv == iPeru:
			iModifier1 -= 2
			iModifier2 -= 2
		
		# disable birth protection if still active
		player(iRevolutionaryPlayer).setBirthProtected(False)
		for p in plots.all():
			if p.getBirthProtected() == iRevolutionaryPlayer:
				p.resetBirthProtected()
			
		team(iExpeditionaryPlayer).declareWar(iRevolutionaryPlayer, True, WarPlanTypes.WARPLAN_TOTAL)
		
		dExpeditionSeaUnits = {
			iEscortSea: 8 + iModifier1 + iModifier2,
			iFerrySea: 6 + iModifier1 + iModifier2,
		}
		
		dExpeditionUnits = {
			iBase: 6 + iModifier2,
			iShock: 4,
			iSiege: 3 + iModifier1 + iModifier2,
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
	if civ(iPlayer) == iAmerica and iOldCivic == iSlavery:
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
	if (pPlayer.isAlive() or (year() <= year(dBirth[iCiv]) + 1 and year() >= year(dBirth[iCiv]) - 1)) and iCiv in dMaxColonists:
		iColonistIndex = data.players[iPlayer].iColonistsAlreadyGiven
		if iColonistIndex < dMaxColonists[iCiv]:
			if pPlayer.isHuman():
				tPlot = dColonistSpawns[iCiv][iColonistIndex][1][0]
			else:
				# MacAurther: Unfortunately, the AI has a hard time with spawning at sea. So they get to spawn on land
				tPlot = dColonistSpawns[iCiv][iColonistIndex][1][1]
			
			iReligion = player(iPlayer).getStateReligion()
			
			for iRole in dColonistSpawns[iCiv][iColonistIndex][2]:
				units = createRoleUnit(iPlayer, tPlot, iRole, 1)
				units.promotion(infos.type("PROMOTION_MERCENARY"))
			
			data.players[iPlayer].iColonistsAlreadyGiven += 1


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