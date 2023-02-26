from Events import handler
from RFCUtils import *
from Core import *
from Locations import *
from Popups import popup


dRelocatedCapitals = CivDict({
})

dCapitalInfrastructure = CivDict({
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


# Help AI by removing nearby Tribes when they settle cities
@handler("cityBuilt")
def convertTribesAroundCity(pCity):
	iPlayer = pCity.getOwner()
	if not player(iPlayer).isHuman():
		for i in range(gc.getNUM_CITY_PLOTS()):
			pPlot = pCity.getCityIndexPlot(i)
			if pPlot.getImprovementType() == iTribe or pPlot.getImprovementType() == iContactedTribe:
				pPlot.setImprovementType(iCottage)

### UNIT BUILT ###


### BEGIN GAME TURN ###
@handler("BeginGameTurn")
def checkColonists():
	if year().between(1500, 1800):
		for iCiv in dColonistSpawnDates:
				if player(iCiv).isAlive():
					iPlayer = slot(iCiv)
					if data.players[iPlayer].iColonistsAlreadyGiven < dMaxColonists[iCiv]:
						if turn() == turn(dColonistSpawnDates[iCiv][data.players[iPlayer].iColonistsAlreadyGiven - 1]):
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
						tContactZoneTL = (33, 54)
						tContactZoneBR = (40, 64)
					elif iNewWorldCiv == iTeotihuacan:
						tContactZoneTL = (28, 60)
						tContactZoneBR = (33, 66)
					elif iNewWorldCiv == iTiwanaku:
						tContactZoneTL = (49, 28)
						tContactZoneBR = (55, 36)
					elif iNewWorldCiv == iWari:
						tContactZoneTL = (40, 31)
						tContactZoneBR = (49, 45)
					elif iNewWorldCiv == iChimu:
						tContactZoneTL = (40, 31)
						tContactZoneBR = (49, 45)
					elif iNewWorldCiv == iMuisca:
						tContactZoneTL = (42, 43)
						tContactZoneBR = (53, 54)
					elif iNewWorldCiv == iAztecs:
						tContactZoneTL = (25, 55)
						tContactZoneBR = (33, 66)
					elif iNewWorldCiv == iInca:
						tContactZoneTL = (41, 18)
						tContactZoneBR = (55, 44)
					else:
						return	# Some natives don't generate conquerors
						
					lArrivalExceptions = []
						
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
		
		if not player(iExpeditionaryPlayer) is None:
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
			iAttackSea: 8 + iModifier1 + iModifier2,
			iFerry: 6 + iModifier1 + iModifier2,
		}
		
		dExpeditionUnits = {
			iAttack: 6 + iModifier2,
			iCounter: 4,
			iSiege: 3 + iModifier1 + iModifier2,
			iShockCity: 4 + iModifier1,
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
				createRoleUnit(iPlayer, plot, iAttack, 3)
				createRoleUnit(iPlayer, plot, iCitySiege, 2)
				
				message(city.getOwner(), "TXT_KEY_MESSAGE_AMERICAN_WEST_COAST_CONQUERORS", adjective(iPlayer), city.getName(), color=iRed, location=city, button=infos.unit(iMinuteman).getButton())
				
		if enemyCities.count() < 2:
			for plot in plots.of(lWestCoast).without(enemyCities).sample(2 - enemyCities.count()):
				makeUnit(iPlayer, iSettler, plot)
				createRoleUnit(iPlayer, plot, iBase)


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


def giveColonists(iPlayer):
	pPlayer = player(iPlayer)
	pTeam = team(iPlayer)
	iCiv = civ(iPlayer)
	
	# MacAurther: This covers starting European colonists and later colonists as well
	if (pPlayer.isAlive() or (year() <= year(dBirth[iCiv]) + 1 and year() >= year(dBirth[iCiv]) - 1)) and iCiv in dMaxColonists:
		if data.players[iPlayer].iColonistsAlreadyGiven < dMaxColonists[iCiv]:
			
			
			if pPlayer.isHuman():
				tUnitPlot = dColonistSpawnPoints[iCiv][data.players[iPlayer].iColonistsAlreadyGiven]
				tSeaPlot = tUnitPlot
			else:
				# MacAurther: Unfortunately, the AI has a hard time with spawning at sea. So they get to spawn on land
				tUnitPlot = dAIColonistSpawnPoints[iCiv][data.players[iPlayer].iColonistsAlreadyGiven]
				tSeaPlot = getRoleLocation(iFerry, location(tUnitPlot))
			
			iReligion = player(iPlayer).getStateReligion()
			
			for iExpeditionType in dColonistExpeditions[iCiv][data.players[iPlayer].iColonistsAlreadyGiven]:
				if iExpeditionType == iCanoeSettle:		# Canoe, Settler
					makeUnit(iPlayer, unique_unit(iPlayer, iCanoe), tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
					makeUnit(iPlayer, iSettler, tUnitPlot, UnitAITypes.UNITAI_SETTLE)
				elif iExpeditionType == iCaravelSettle:	# Caravel, Settler, Militia (Portugal: Carrack, Settler, Settler, Militia)
					makeUnit(iPlayer, unique_unit(iPlayer, iCaravel), tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
					makeUnit(iPlayer, iSettler, tUnitPlot, UnitAITypes.UNITAI_SETTLE)
					createRoleUnit(iPlayer, tUnitPlot, iBase, 1)
					if iCiv == iPortugal:
						makeUnit(iPlayer, iSettler, tUnitPlot, UnitAITypes.UNITAI_SETTLE)
				elif iExpeditionType == iCaravelSupport:	# Caravel, Work, Missionary (Portugal: Carrack, Work, Missionary, Militia)
					makeUnit(iPlayer, unique_unit(iPlayer, iCaravel), tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
					createRoleUnit(iPlayer, tUnitPlot, iWork, 1)
					if iReligion > -1:
						makeUnits(iPlayer, missionary(iReligion), tUnitPlot, 1)
					if iCiv == iPortugal:
						createRoleUnit(iPlayer, tUnitPlot, iBase, 1)
				elif iExpeditionType == iCaravelExplore:	# Caravel, Explore, Missionary (Portugal: Carrack, Explore, Missionary, Missionary)
					makeUnit(iPlayer, unique_unit(iPlayer, iCaravel), tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
					createRoleUnit(iPlayer, tUnitPlot, iExplore, 1)
					if iReligion > -1:
						makeUnits(iPlayer, missionary(iReligion), tUnitPlot, 1)
						if iCiv == iPortugal:
							makeUnits(iPlayer, missionary(iReligion), tUnitPlot, 1)
				elif iExpeditionType == iCaravelConquer:	# Caravel, Attack, CitySiege (Portugal: Carrack, Attack, Attack, CitySiege)
					makeUnit(iPlayer, unique_unit(iPlayer, iCaravel), tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
					createRoleUnit(iPlayer, tUnitPlot, iAttack, 1)
					createRoleUnit(iPlayer, tUnitPlot, iCitySiege, 1)
					if iCiv == iPortugal:
						createRoleUnit(iPlayer, tUnitPlot, iAttack, 1)
				elif iExpeditionType == iGalleonSettle:	# Galleon, Settler, Militia, Work
					makeUnit(iPlayer, unique_unit(iPlayer, iGalleon), tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
					makeUnit(iPlayer, iSettler, tUnitPlot, UnitAITypes.UNITAI_SETTLE)
					createRoleUnit(iPlayer, tUnitPlot, iBase, 1)
					createRoleUnit(iPlayer, tUnitPlot, iWork, 1)
				elif iExpeditionType == iGalleonSupport:	# Galleon, Explore, Work, Missionary
					makeUnit(iPlayer, unique_unit(iPlayer, iGalleon), tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
					createRoleUnit(iPlayer, tUnitPlot, iExplore, 1)
					createRoleUnit(iPlayer, tUnitPlot, iWork, 1)
					if iReligion > -1:
						makeUnits(iPlayer, missionary(iReligion), tUnitPlot, 1)
				elif iExpeditionType == iGalleonConquer:	# Galleon, Attack, Shock, CitySiege
					makeUnit(iPlayer, unique_unit(iPlayer, iGalleon), tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
					createRoleUnit(iPlayer, tUnitPlot, iAttack, 1)
					createRoleUnit(iPlayer, tUnitPlot, iShock, 1)
					createRoleUnit(iPlayer, tUnitPlot, iCitySiege, 1)
			
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