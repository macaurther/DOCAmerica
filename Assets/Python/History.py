from Events import handler
from RFCUtils import *
from Core import *
from Locations import *
from Popups import popup


dRelocatedCapitals = CivDict({
})

dCapitalInfrastructure = CivDict({
	iPortugal : (5, [iLibrary, iMarket, iHarbor, iLighthouse, iForge, iWalls], [temple]),
	iNetherlands : (9, [iLibrary, iMarket, iWharf, iLighthouse, iBarracks, iPharmacy, iBank, iArena, iTheatre], [temple]),
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
			
			
### UNIT BUILT ###


### BEGIN GAME TURN ###

@handler("BeginGameTurn")
def placeGoodyHuts(iGameTurn):
	if iGameTurn == scenarioStartTurn() + 3:
			
		if scenario() <= i1500AD:
			placeHut((22, 48), (29, 51)) # Great Lakes
			placeHut((18, 44), (22, 52)) # Great Plains
			placeHut((34, 25), (39, 29)) # Amazonas Delta
			placeHut((25, 36), (32, 39)) # Caribbean


# TODO: revisit how this works
@handler("BeginGameTurn")
def checkEarlyColonists():
	dEarlyColonistYears = {
	}
	
	iYear = game.getGameTurnYear()
	if iYear in dEarlyColonistYears:
		iCiv = dEarlyColonistYears[iYear]
		giveEarlyColonists(iCiv)
		
		
@handler("BeginGameTurn")
def checkLateColonists():
	if year().between(1350, 1918):
		for iCiv in dTradingCompanyPlots:
			if player(iCiv).isAlive():
				iPlayer = slot(iCiv)
				if data.players[iPlayer].iExplorationTurn >= 0:
					if turn() == data.players[iPlayer].iExplorationTurn + 1 + data.players[iPlayer].iColonistsAlreadyGiven * 8:
						giveColonists(iPlayer)


### FIRST CONTACT ###

@handler("firstContact")
def conquistadors(iTeamX, iHasMetTeamY):
		if is_minor(iTeamX) or is_minor(iHasMetTeamY):
			return
		
		if year().between(600, 1800):
			if civ(iTeamX) in lBioNewWorld and civ(iHasMetTeamY) not in lBioNewWorld:
				iNewWorldPlayer = iTeamX
				iOldWorldPlayer = iHasMetTeamY
				
				if civ(iOldWorldPlayer) == iPolynesia:
					return
				
				iNewWorldCiv = civ(iNewWorldPlayer)
				
				bAlreadyContacted = data.dFirstContactConquerors[iNewWorldCiv]
				
				# avoid "return later" exploit
				if year() <= year(dBirth[iAztecs]) + turns(10):
					data.dFirstContactConquerors[iNewWorldCiv] = True
					return
					
				if not bAlreadyContacted:
					if iNewWorldCiv == iMaya:
						tContactZoneTL = (15, 30)
						tContactZoneBR = (34, 42)
					elif iNewWorldCiv == iAztecs:
						tContactZoneTL = (11, 31)
						tContactZoneBR = (34, 43)
					elif iNewWorldCiv == iInca:
						tContactZoneTL = (21, 11)
						tContactZoneBR = (36, 40)
						
					lArrivalExceptions = [(25, 32), (26, 40), (25, 42), (23, 42), (21, 42)]
						
					data.dFirstContactConquerors[iNewWorldCiv] = True
					
					events.fireEvent("conquerors", iOldWorldPlayer, iNewWorldPlayer)
					
					newWorldPlots = plots.start(tContactZoneTL).end(tContactZoneBR).without(lArrivalExceptions)
					contactPlots = newWorldPlots.where(lambda p: p.isVisible(iNewWorldPlayer, False) and p.isVisible(iOldWorldPlayer, False))
					arrivalPlots = newWorldPlots.owner(iNewWorldPlayer).where(lambda p: not p.isCity() and isFree(iOldWorldPlayer, p, bCanEnter=True) and map.getArea(p.getArea()).getCitiesPerPlayer(iNewWorldPlayer) > 0)
					
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
						
						# disable birth protection if still active
						player(iNewWorldPlayer).setBirthProtected(False)
						for p in plots.all():
							if p.getBirthProtected() == iNewWorldPlayer:
								p.resetBirthProtected()
							
						team(iOldWorldPlayer).declareWar(iNewWorldPlayer, True, WarPlanTypes.WARPLAN_TOTAL)
						
						dConquerorUnits = {
							iAttack: 1 + iModifier2,
							iCounter: 2,
							iSiege: 1 + iModifier1 + iModifier2,
							iShockCity: 2 + iModifier1,
						}
						units = createRoleUnits(iOldWorldPlayer, arrivalPlot, dConquerorUnits.items())
						units.promotion(infos.type("PROMOTION_MERCENARY"))
						
						iStateReligion = player(iOldWorldPlayer).getStateReligion()
						iMissionary = missionary(iStateReligion)
						
						if iMissionary:
							makeUnit(iOldWorldPlayer, iMissionary, arrivalPlot)
							
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

### TECH ACQUIRED ###

@handler("techAcquired")
def recordExplorationTurn(iTech, iTeam, iPlayer):
	if iTech == iExploration:
		data.players[iPlayer].iExplorationTurn = game.getGameTurn()


@handler("techAcquired")
def openIcelandRoute(iTech):		
	if iTech == iCompass:
		plot(49, 62).setTerrainType(iCoast, True, True)


@handler("techAcquired")
def americanWestCoastSettlement(iTech, iTeam, iPlayer):
	if iTech == iRailroad and civ(iPlayer) == iAmerica and not player(iPlayer).isHuman():
		lWestCoast = [(11, 50), (11, 49), (11, 48), (11, 47), (11, 46), (12, 45)]
				
		enemyCities = cities.of(lWestCoast).notowner(iAmerica)
		
		for iEnemy in enemyCities.owners():
			team(iPlayer).declareWar(iEnemy, True, WarPlanTypes.WARPLAN_LIMITED)
		
		for city in enemyCities:
			plot = plots.surrounding(city).without(city).land().passable().no_enemies(iPlayer).random()
			if plot:
				makeUnits(iPlayer, iMinuteman, plot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
				makeUnits(iPlayer, iCannon, plot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
				
				message(city.getOwner(), "TXT_KEY_MESSAGE_AMERICAN_WEST_COAST_CONQUERORS", adjective(iPlayer), city.getName(), color=iRed, location=city, button=infos.unit(iMinuteman).getButton())
				
		if enemyCities.count() < 2:
			for plot in plots.of(lWestCoast).without(enemyCities).sample(2 - enemyCities.count()):
				makeUnit(iPlayer, iSettler, plot)
				makeUnit(iPlayer, iMinuteman, plot)


@handler("techAcquired")
def earlyTradingCompany(iTech, iTeam, iPlayer):
	if turn() == scenarioStartTurn():
		return

	lCivs = [iSpain, iPortugal]
	lTechs = [iExploration, iFirearms]
	
	if civ(iPlayer) in lCivs:
		if iTech in lTechs and all(team(iTeam).isHasTech(iTech) for iTech in lTechs):
			if not player(iPlayer).isHuman() and not team(iTeam).isAVassal():
				handleColonialAcquisition(iPlayer)


@handler("techAcquired")
def lateTradingCompany(iTech, iTeam, iPlayer):
	if turn() == scenarioStartTurn():
		return

	lCivs = [iFrance, iEngland, iNetherlands]
	lTechs = [iEconomics, iReplaceableParts]
	
	if civ(iPlayer) in lCivs:
		if iTech in lTechs and all(team(iTeam).isHasTech(iTech) for iTech in lTechs):
			if not player(iPlayer).isHuman() and not team(iTeam).isAVassal():
				handleColonialConquest(iPlayer)


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
					
					
def giveEarlyColonists(iCiv):
	pPlayer = player(iCiv)
	
	if pPlayer.isAlive() and not pPlayer.isHuman():
		capital = pPlayer.getCapitalCity()
			
		if capital:
			tSeaPlot = findSeaPlots(capital, 1, iCiv)
			if tSeaPlot:
				makeUnit(iCiv, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iCiv, iSettler, tSeaPlot)
				makeUnit(iCiv, iArcher, tSeaPlot)


def giveColonists(iPlayer):
	pPlayer = player(iPlayer)
	pTeam = team(iPlayer)
	iCiv = civ(iPlayer)
	
	if pPlayer.isAlive() and not pPlayer.isHuman() and iCiv in dMaxColonists:
		if pTeam.isHasTech(iExploration) and data.players[iPlayer].iColonistsAlreadyGiven < dMaxColonists[iCiv]:
			sourceCities = cities.core(iCiv).owner(iPlayer)
			
			# help England with settling Canada and Australia
			if iCiv == iEngland:
				colonialCities = cities.regions(rCanada, rAustralia).owner(iPlayer)
				if colonialCities:
					sourceCities = colonialCities
					
			city = sourceCities.coastal().random()
			if city:
				tSeaPlot = findSeaPlots(city, 1, iCiv)
				if not tSeaPlot: tSeaPlot = city
				
				makeUnit(iPlayer, unique_unit(iPlayer, iGalleon), tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot, UnitAITypes.UNITAI_SETTLE)
				createRoleUnit(iPlayer, tSeaPlot, iDefend, 1)
				makeUnit(iPlayer, iWorker, tSeaPlot)
				
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
		makeUnit(iPlayer, unique_unit(iPlayer, iGalleon), seaPlot)


def placeHut(tTL, tBR):
	plotList = []
	
	for plot in plots.start(tTL).end(tBR):
		if plot.isFlatlands() or plot.isHills():
			if plot.getFeatureType() != iMud:
				if plot.getOwner() < 0:
					plotList.append(location(plot))
	
	if not plotList:
		return
	
	tPlot = random_entry(plotList)
	plot_(tPlot).setImprovementType(iHut)