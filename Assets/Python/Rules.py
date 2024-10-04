from Core import *
from Locations import *
from RFCUtils import *
from Events import handler


### CONSTANTS ###

dRelocatedCapitals = {
}


### CITY ACQUIRED ###

@handler("cityAcquired")
def resetSlaves(iOwner, iPlayer, city):
	freeSlaves(city, iPlayer)

# MacAurther: Don't let non-Natives keep all the settled Native great people on conquest (Spain becomes mega buff)
@handler("cityAcquired")
def resetGreatPeople(iOldOwner, iPlayer, city, bConquest, bTrade):
	if civ(iOldOwner) not in dCivGroups[iCivGroupNative]:
		return
	if civ(iPlayer) in dCivGroups[iCivGroupNative]:
		return
	
	for iGreatSpecialist in lGreatSpecialists:
		city.setFreeSpecialistCount(iGreatSpecialist, 0)

@handler("cityAcquired")
def resetAdminCenter(iOwner, iPlayer, city):
	if city.isCapital() and city.isHasRealBuilding(iAdministrativeCenter):
		city.setHasRealBuilding(iAdministrativeCenter, False)


@handler("cityAcquired")
def restoreCapital(iOwner, iPlayer, city):
	if player(iPlayer).isHuman() or is_minor(iPlayer):
		return
	
	capital = plots.capital(iPlayer)
	
	if data.civs[iPlayer].iResurrections > 0 or player(iPlayer).getPeriod() != -1:
		capital = plots.respawnCapital(iPlayer)
		
	if at(city, capital):
		relocateCapital(iPlayer, city)


@handler("cityAcquired")
def resetNationalWonders(iOwner, iPlayer, city, bConquest, bTrade):
	if bTrade:
		for iNationalWonder in range(iNumBuildings):
			if iNationalWonder != iPalace and isNationalWonderClass(infos.building(iNationalWonder).getBuildingClassType()) and city.hasBuilding(iNationalWonder):
				city.setHasRealBuilding(iNationalWonder, False)


@handler("cityAcquired")
def downgradeCottages(iOwner, iPlayer, city, bConquest, bTrade):
	if bConquest and player(iPlayer).getCurrentEra() <= iRevolutionaryEra:
		downgradeCityCottages(city)


### CITY ACQUIRED AND KEPT ###
	
@handler("cityAcquiredAndKept")
def spreadCultureOnConquest(iPlayer, city):
	for plot in plots.surrounding(city):
		if at(plot, city):
			convertTemporaryCulture(plot, iPlayer, 25, False)
		elif civ(plot) == city.getPreviousCiv():
			convertTemporaryCulture(plot, iPlayer, 50, True)
		else:
			convertTemporaryCulture(plot, iPlayer, 25, True)


### CITY BUILT ###

@handler("cityBuilt")
def clearMinorCulture(city):
	for iMinor in players.minor():
		plot(city).setCulture(iMinor, 0, True)


@handler("cityBuilt")
def spreadCulture(city):
	if not is_minor(city):
		spreadMajorCulture(city.getOwner(), location(city))


@handler("cityBuilt")
def updateFoundValues(city):
	if not is_minor(city) and player(city).getNumCities() <= 1:
		player(city).AI_updateFoundValues(False)


@handler("cityBuilt")
def createColonialDefenders(city):
	iPlayer = city.getOwner()
	if not player(iPlayer).isHuman():
		if civ(iPlayer) in dCivGroups[iCivGroupEurope]:
			createGarrisons(city, iPlayer, 1)
			createRoleUnit(iPlayer, city, iWork, 1)


@handler("cityBuilt")
def pioneeringAbility(city):
	iPlayer = city.getOwner()
	if team(iPlayer).isHasTech(iPioneering):
		createGarrisons(city, iPlayer, 1)
		createRoleUnit(iPlayer, city, iWork, 1)

@handler("cityBuilt")
# Providence and Manifest Destiny civics
def extraCultureOnFound(city):
	iExpansionCivic = player(city.getOwner()).getCivics(iCivicsExpansion)
	if iExpansionCivic in [iProvidence2, iManifestDestiny3]:
		city.changeCulture(city.getOwner(), int(50 * (3 - gc.getGame().getGameSpeedType())), True)

@handler("cityBuilt")
# Homestead civics
def extraCultureOnFound(city):
	iExpansionCivic = player(city.getOwner()).getCivics(iCivicsExpansion)
	if iExpansionCivic in [iHomesteads2, iHomesteads3]:
		iSettleImmigration = int(50 * (3 - gc.getGame().getGameSpeedType()))	# Scale based on game speed
		
		# England UP
		if civ(city.getOwner()) == iEngland:
			iSettleImmigration *= 2
		
		player(city.getOwner()).changeImmigration(iSettleImmigration)

### GOODY RECEIVED ###

@handler("goodyReceived")
def cooperationAbility(iPlayer, pPlot, pUnit, iGoodyType):
	iExpansionCivic = player(iPlayer).getCivics(iCivicsExpansion)
	if iExpansionCivic == iCooperation1:
		if player(iPlayer).getNumCities() > 0:
			pCity = closestCity(pPlot, iPlayer)
			if pCity and distance(pPlot, pCity) <= 10:
				pCity.changePopulation(1)
				
				message(iPlayer, 'TXT_KEY_COOPERATION_EFFECT', pCity.getName())


### COMBAT RESULT ###
		
@handler("combatResult")
def captureSlaves(winningUnit, losingUnit):
	if plot(winningUnit).isWater() and freeCargo(winningUnit, winningUnit) <= 0:
		return
	
	iSlave = getNativeSlaveType(winningUnit.getOwner())
	
	# Jaguar Ability
	if winningUnit.getUnitType() == iJaguar:
		captureUnit(losingUnit, winningUnit, iNativeSlaveMeso, 100)
		return
	
	# Captives Civic
	if player(winningUnit.getOwner()).getCivics(iCivicsLabor) == iCaptives1:
		captureUnit(losingUnit, winningUnit, iSlave, 50)
		return
	
	# Bandeirante Ability
	if civ(losingUnit) == iNative and winningUnit.getUnitType() == iBandeirante:
		captureUnit(losingUnit, winningUnit, iNativeSlave2, 100)
		return
	
	# Encomienda Civic
	if civ(losingUnit) == iNative and player(winningUnit.getOwner()).getCivics(iCivicsLabor) == iEncomienda2:
		captureUnit(losingUnit, winningUnit, iSlave, 50)
		return

@handler("combatResult")
def captureCannon(winningUnit, losingUnit):
	if losingUnit.getUnitType() in [iBombard, iCannon, iHeavyCannon, iRifledCannon, iArtillery, iLightCannon, iFieldGun, iGatlingGun, iMachineGun]:
		captureUnit(losingUnit, winningUnit, losingUnit.getUnitType(), 50)

@handler("combatResult")
def captureAdvancedWeapons(pWinningUnit, pLosingUnit):
	# Capture cannon
	if infos.unit(pLosingUnit).getUnitCombatType() in [UnitCombatTypes.UNITCOMBAT_SIEGE]:
		captureUnit(pLosingUnit, pWinningUnit, pLosingUnit.getUnitType(), 50)
		return
	
	# Upgrade melee and archery units when winning against horses and guns
	if infos.unit(pWinningUnit).getUnitCombatType() in [UnitCombatTypes.UNITCOMBAT_MELEE, UnitCombatTypes.UNITCOMBAT_ARCHER]:
		pNewUnit = None
		if infos.unit(pLosingUnit).getUnitCombatType() in [UnitCombatTypes.UNITCOMBAT_CAVALRY]:
			if civ(pWinningUnit.getOwner()) in dCivGroups[iCivGroupNative]:
				pNewUnit = captureUnit(pLosingUnit, pWinningUnit, iHorseArcher, 50)
			else:
				pNewUnit = captureUnit(pLosingUnit, pWinningUnit, iCuirassier, 50)
		elif infos.unit(pLosingUnit).getUnitCombatType() in [UnitCombatTypes.UNITCOMBAT_GUN]:
			pNewUnit = captureUnit(pLosingUnit, pWinningUnit, iArquebusier, 50)
		
		if pNewUnit:
			pNewUnit.convert(pWinningUnit)
		

@handler("combatResult")
def mayanHolkanAbility(winningUnit, losingUnit):
	if winningUnit.getUnitType() == iHolkan:
		iWinner = winningUnit.getOwner()
		if player(iWinner).getNumCities() > 0:
			city = closestCity(winningUnit, iWinner)
			if city and distance(winningUnit, city) <= 10:
				iFood = scale(5)
				city.changeFood(iFood)
				
				message(iWinner, 'TXT_KEY_MAYA_HOLKAN_EFFECT', adjective(losingUnit), losingUnit.getName(), iFood, city.getName())
				
				events.fireEvent("combatFood", iWinner, winningUnit, iFood)


### REVOLUTION ###

@handler("revolution")
def validateSlaves(iPlayer):
	if not player(iPlayer).canUseSlaves():
		if player(iPlayer).getImprovementCount(iSlavePlantation) > 0:
			for plot in plots.owner(iPlayer).where(lambda plot: plot.getImprovementType() == iSlavePlantation):
				plot.setImprovementType(iPlantation)
		
		if player(iPlayer).getImprovementCount(iSlaveMine) > 0:
			for plot in plots.owner(iPlayer).where(lambda plot: plot.getImprovementType() == iSlaveMine):
				plot.setImprovementType(iMine)
		
		for city in cities.owner(iPlayer):
			iNumSlaves = city.getFreeSpecialistCount(iSpecialistSlave)
			city.setFreeSpecialistCount(iSpecialistSlave, 0)
			
			# Emancipation Civic
			if player(iPlayer).getCivics(iCivicsSociety) in [iEmancipation2, iEmancipation3]:
				city.changePopulation(iNumSlaves)
				
		for slave in units.owner(iPlayer).where(lambda unit: base_unit(unit) in [iAfricanSlave2, iAfricanSlave3]):
			slave.kill(False, iPlayer)


### CAPITAL MOVED ###

@handler("capitalMoved")
def resetAdminCenterOnPalaceBuilt(city):
	if city.isHasRealBuilding(iAdministrativeCenter):
		city.setHasRealBuilding(iAdministrativeCenter, False)



### PLOT FEATURE REMOVED ###


@handler("plotFeatureRemoved")
def brazilianMadeireiroAbility(plot, city, iFeature):
	dFeatureGold = defaultdict({
		iForest : 15,
		iPalmForest : 15,
		iJungle : 20,
		iRainforest : 20,
	}, 0)
	
	if civ(plot) == iBrazil:
		iGold = dFeatureGold[iFeature]
		
		if iGold > 0:
			player(plot).changeGold(iGold)
			message(plot.getOwner(), 'TXT_KEY_DEFORESTATION_EVENT', infos.feature(iFeature).getText(), city.getName(), iGold, type=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.commerce(0).getButton(), location=plot)


### BEGIN GAME TURN ###


### TECH ACQUIRED ###

@handler("techAcquired")
def relocateCapitals(iTech, iTeam, iPlayer):
	if not player(iPlayer).isHuman():
		iCiv = civ(iPlayer)
		iEra = infos.tech(iTech).getEra()
		if (iCiv, iEra) in dRelocatedCapitals:
			relocateCapital(iPlayer, dRelocatedCapitals[iCiv, iEra])


### END GAME TURN ###

@handler("EndGameTurn")
def startTimedConquests():
	for iConqueror, tPlot in data.lTimedConquests:
		colonialConquest(iConqueror, tPlot)
	
	data.lTimedConquests = []

@handler("EndGameTurn")
def drainLakeTexcoco():
	if turn() == year(1650):
		for pPlot in plots.rectangle(tLakeTexcocoTL, tLakeTexcocoBR):
			if pPlot.isPeak(): continue
			elif pPlot.isWater():
				lUnits = units.at(pPlot)
				# Move any ships
				for pUnit in lUnits:
					pCoastalCity = cities.owner(pUnit.getOwner()).coastal().closest(pPlot)
					if pCoastalCity:
						move(pUnit, pCoastalCity)
					else:
						pUnit.kill(False, -1)
				pPlot.setBonusType(BonusTypes.NO_BONUS)
				pPlot.setTerrainType(iMarsh, True, True)
				pPlot.setFeatureType(iFloodPlains, 0)
			elif pPlot.getTerrainType() == iLagoon:
				pPlot.setTerrainType(iMarsh, True, True)
				pPlot.setFeatureType(iFloodPlains, 0)
			else:
				pPlot.setTerrainType(iPlains, True, True)

### BEGIN PLAYER TURN ###

@handler("setPlayerAlive")
def updateLastTurnAlive(iPlayer, bAlive):
	if turn() == scenarioStartTurn():
		return

	if not bAlive and not (player(iPlayer).isHuman() and autoplay()):
		data.civs[iPlayer].iLastTurnAlive = game.getGameTurn()

### END PLAYER TURN ###

@handler("EndPlayerTurn")
# Chance to remove worked feature/bonus is totalPop / 100 (if player has more than 100 pop, it's 1 loss every turn)
def extractionAbility(iGameTurn, iPlayer):
	pPlayer = player(iPlayer)
	iEconomyCivic = pPlayer.getCivics(iCivicsEconomy)
	if iEconomyCivic == iExtraction3:
		iPopulation = pPlayer.getTotalPopulation()
		if iPopulation > rand(100):
			# Search for a random city to check
			iCityNum = rand(pPlayer.getNumCities() - 1)
			if iCityNum < 1: return
			
			pCity = cities.owner(iPlayer)[iCityNum]
			if pCity == None: return
			
			for i in range(gc.getNUM_CITY_PLOTS()):
				pPlot = pCity.getCityIndexPlot(i)
				if pPlot and not pPlot.isNone() and pPlot.hasYield():
					if pCity.isWorkingPlot(pPlot):
						if pPlot.getFeatureType() != FeatureTypes.NO_FEATURE:
							message(iPlayer, 'TXT_KEY_EXTRACTION_FEATURE', sound='SND_REVOLTEND', event=1, button=infos.feature(pPlot.getFeatureType()).getButton(), color=iRed, location=pPlot)
							pPlot.setFeatureType(FeatureTypes.NO_FEATURE, 0)
							return
						elif pPlot.getBonusType(pPlayer.getTeam()) != BonusTypes.NO_BONUS:
							message(iPlayer, 'TXT_KEY_EXTRACTION_BONUS', sound='SND_REVOLTEND', event=1, button=infos.bonus(pPlot.getBonusType(pPlayer.getTeam())).getButton(), color=iRed, location=pPlot)
							pPlot.setBonusType(BonusTypes.NO_BONUS)
							return

### PROJECT BUILT ###

# Migration
@handler("projectBuilt")
def detectMigrateCity(pCity, iProject):
	# MacAurther TODO: Better way than just copying every field?
	if iProject in [iMigrateN, iMigrateNE, iMigrateE, iMigrateSE, iMigrateS, iMigrateSW, iMigrateW, iMigrateNW]:		
		# Calculate new plot
		iX = pCity.getX()
		iY = pCity.getY()
		iXNew = iX
		iYNew = iY
		if iProject == iMigrateN:
			iYNew += 1
		elif iProject == iMigrateNE:
			iXNew += 1
			iYNew += 1
		elif iProject == iMigrateE:
			iXNew += 1
		elif iProject == iMigrateSE:
			iXNew += 1
			iYNew -= 1
		elif iProject == iMigrateS:
			iYNew -= 1
		elif iProject == iMigrateSW:
			iXNew -= 1
			iYNew -= 1
		elif iProject == iMigrateW:
			iXNew -= 1
		elif iProject == iMigrateNW:
			iXNew -= 1
			iYNew += 1
		
		data.lMigrateCities.append(pCity)
		data.lMigrateX.append(iXNew)
		data.lMigrateY.append(iYNew)
		
@handler("EndGameTurn")
def lMigrateCities(iGameTurn):
	# Check if there's a city to migrate
	if data.lMigrateCities == []:
		return
	
	for iIndex, pCity in enumerate(data.lMigrateCities):
		iXNew = data.lMigrateX[iIndex]
		iYNew = data.lMigrateY[iIndex]
		
		iPlayer = pCity.getOwner()
		iCiv = civ(iPlayer)
		pPlayer = player(iPlayer)
		
		# Store temp city data
		# Don't get things like GameTurnFounded or GameTurnAcquired, we want to reset those
		iPopulation = pCity.getPopulation()
		iNumCityBuildings = pCity.getNumBuildings()
		lBuildings = []
		for i in range(iNumBuildingsPaganTemples):
			if pCity.hasBuilding(i):
				lBuildings.append(i)
				if len(lBuildings) == iNumCityBuildings + 1:
					break
		iCulture = pCity.getCulture(pCity.getOwner())
		
		# Get free specialists
		dFreeSpecialists = {}
		for iSpecialist in range(iNumSpecialists):
			iCount = pCity.getFreeSpecialistCount(iSpecialist)
			if iCount > 0:
				dFreeSpecialists[iSpecialist] = iCount
		
		# Get local temp unhappiness
		iHurryAngerTimer = pCity.getHurryAngerTimer()
		iConscriptAngerTimer = pCity.getConscriptAngerTimer()
		iDefyAngerTimer = pCity.getDefyResolutionAngerTimer()
		
		# Copy religions
		lReligions = []
		for iReligion in range(iNumReligions):
			if pCity.isHasReligion(iReligion):
				lReligions.append(iReligion)
		
		#sName = pCity.getName()	# Actually, don't copy name, let it take the name from the city name manager

		# Remove old city
		pPlayer.disband(pCity)
		pCity.plot().setRouteType(-1)
		pCity.plot().setImprovementType(-1)
		
		# Found city
		plot(iXNew, iYNew).setOwner(iPlayer)
		pPlayer.found(iXNew, iYNew)
		pNewCity = city(iXNew, iYNew)
		if pNewCity:
			#pNewCity.setName(sName, False)	# Actually, don't copy name, let it take the name from the city name manager
			pNewCity.setPopulation(iPopulation + 1)

			# Assign buildings to new city
			for iBuilding in lBuildings:
				if not pNewCity.isHasRealBuilding(iBuilding):
					print("Setting building in New City: " + str(iBuilding))
					pNewCity.setHasRealBuilding(iBuilding, True)
				# If capital was migrated, make sure Palace didn't end up in another city (janky, but how else to do it?)
				if iBuilding in [iPalace, iChieftansHut, iGovernorsMansion, iCapitol]:
					for pOtherCity in cities.owner(iPlayer):
						if pOtherCity.isHasRealBuilding(iBuilding) and not (pOtherCity.getX() == pNewCity.getX() and pOtherCity.getY() == pNewCity.getY()):
							pOtherCity.setHasRealBuilding(iBuilding, False)
		
			# Assign culture to new city
			if civ(iPlayer) == iLakota:
				iCulture += 10 * (3 - gc.getGame().getGameSpeedType())	# Scale based on Game Speed
			pNewCity.setCulture(iPlayer, iCulture, True)
			
			# Assign free specialists
			for iSpecialist in dFreeSpecialists:
				pNewCity.setFreeSpecialistCount(iSpecialist, dFreeSpecialists[iSpecialist]) 
			
			# Assign local temp unhappiness
			pNewCity.changeHurryAngerTimer(iHurryAngerTimer)
			pNewCity.changeConscriptAngerTimer(iConscriptAngerTimer)
			pNewCity.changeDefyResolutionAngerTimer(iDefyAngerTimer)
			
			# Assign religions
			for iReligion in lReligions:
				pNewCity.setHasReligion(iReligion, True, False, False)
			
			
		else:
			print("WARNING - Migration failed for iPlayer: " + str(iPlayer))
		
		events.fireEvent("migration", iPlayer, 1)

	# Clear migration data
	data.lMigrateCities = []
	data.lMigrateX = []
	data.lMigrateY = []

### IMPLEMENTATIONS ###

def isBribableUnit(iPlayer, unit):
	if not unit.canFight():
		return False
	
	if unit.isInvisible(player(iPlayer).getTeam(), False):
		return False
	
	if unit.getDomainType() != DomainTypes.DOMAIN_LAND:
		return False
	
	return True


def getPossibleBribes(iPlayer, location):
	iTreasury = player(iPlayer).getGold()
	targets = [(unit, infos.unit(unit).getProductionCost() * 3 / 2) for unit in units.at(location).owner(iBarbarian)]
	return [(unit, iCost) for unit, iCost in targets if isBribableUnit(iPlayer, unit) and iCost <= iTreasury]


def canBribeUnits(spy):
	if not player(spy).canHurry(1):
		return False
	
	if plot(spy).isOwned() and plot(spy).getOwner() != spy.getOwner():
		return False

	if spy.getMoves() >= spy.maxMoves(): 
		return False
		
	if not getPossibleBribes(spy.getOwner(), location(spy)):
		return False
	
	return True


def applyUnitBribes(iChoice, iPlayer, x, y):
	targets = getPossibleBribes(iPlayer, (x, y))
	unit, iCost = targets[iChoice]
	
	newUnit = makeUnit(iPlayer, unit.getUnitType(), closestCity(unit, owner=iPlayer))
	player(iPlayer).changeGold(-iCost)

	unit.kill(False, -1)
	
	if newUnit:
		interface.selectUnit(newUnit, True, True, False)


def doUnitBribes(spy):
	# only once per turn
	spy.finishMoves()
			
	# launch popup
	bribePopup = unit_bribe_popup.launcher()
	
	for unit, iCost in getPossibleBribes(spy.getOwner(), location(spy)):
		bribePopup.text().applyUnitBribes(unit.getName(), unit.currHitPoints(), unit.maxHitPoints(), iCost, button=unit.getButton())
	
	x, y = location(spy)
	bribePopup.cancel().launch(spy.getOwner(), x, y)

@handler("civicChanged")
def onCivicChanged(iPlayer, iOldCivic, iNewCivic):
	if iNewCivic == iConfederacy1:
		for pPlot in plots.all().owner(iPlayer):
			# Convert Tribes to Allied Tribe
			if pPlot.getImprovementType() == iTribe:
				pPlot.setImprovementType(iTribe)
				player(iPlayer).doGoody(pPlot, None)

### POPUPS ###

unit_bribe_popup = popup.text("TXT_KEY_BRIBE_UNITS_POPUP") \
						.selection(applyUnitBribes, "TXT_KEY_BRIBE_UNITS_BUTTON") \
						.cancel("TXT_KEY_BRIBE_UNITS_BUTTON_NONE") \
						.build()