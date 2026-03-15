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
			if iNationalWonder not in lCapitols and isNationalWonderClass(infos.building(iNationalWonder).getBuildingClassType()) and city.hasBuilding(iNationalWonder): # MacAurther: Multiple capitol types
				city.setHasRealBuilding(iNationalWonder, False)


@handler("cityAcquired")
def downgradeCottages(iOwner, iPlayer, city, bConquest, bTrade):
	if bConquest and player(iPlayer).getCurrentEra() <= iRevolutionaryEra:
		downgradeCityCottages(city)

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
def nativeCityConquered(iOldOwner, iNewOwner, pCity, bConquest, bTrade):
	if not bConquest:
		return
	
	# Check if city was taken from a Native
	if not civ(iOldOwner) in lNativeCivs:
		return
	
	# Check for any slave capturing
	# Need to somehow get conquering unit, just get the first unit on the plot and hope it's right?
	pPlot = pCity.plot()
	if pPlot.getNumUnits() > 0:
		pConqueringUnit = pPlot.getUnit(0)
		enslaveUnit(pConqueringUnit)


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

@handler("cityAcquiredAndKept")
# Partonato civic
def convertOnCityAcquired(iPlayer, pCity):
	if player(iPlayer).hasCivic(iPatronato):
		if player(iPlayer).getStateReligion() != -1:
			pCity.spreadReligion(player(iPlayer).getStateReligion())


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
def extraCultureOnFound(pCity):
	iExpansionCivic = player(pCity).getCivics(iCivicsExpansion)
	if iExpansionCivic in [iProvidence, iManifestDestiny]:
		pCity.changeCulture(pCity.getOwner(), scale(50), True)
	
	if iExpansionCivic in [iProvidence]:
		if player(pCity).getStateReligion() != -1:
			pCity.spreadReligion(player(pCity).getStateReligion())

@handler("cityBuilt")
# Homestead civics
def extraImmigrationOnFound(city):
	iExpansionCivic = player(city.getOwner()).getCivics(iCivicsExpansion)
	if iExpansionCivic in [iGrants, iHomesteads]:
		iSettleImmigration = scale(20)
		
		player(city.getOwner()).changeImmigration(iSettleImmigration)

### CITY GIFTED ###


@handler("cityGifted")
def giftedCityDefenders(city):
	if not player(city).isHuman():
		iNumDefenders = max(2, 1 + player(city).getCurrentEra() / 2)
		createGarrisons(city, city.getOwner(), iNumDefenders)

### GOODY RECEIVED ###



### COMBAT RESULT ###
		
@handler("combatResult")
def captureSlaves(winningUnit, losingUnit):
	if plot(winningUnit).isWater() and freeCargo(winningUnit, winningUnit) <= 0:
		return
	
	enslaveUnit(winningUnit, losingUnit)

@handler("combatResult")
def captureWeapons(pWinningUnit, pLosingUnit):
	# Don't capture if battle is between two AIs (hurts AI conquerors too much)
	if not player(pWinningUnit).isHuman() and not player(pLosingUnit).isHuman():
		return
	
	# Capture cannon
	if infos.unit(pLosingUnit).getUnitCombatType() in [UnitCombatTypes.UNITCOMBAT_SIEGE]:
		captureUnit(pLosingUnit, pWinningUnit, pLosingUnit.getUnitType(), 25)
		return
	
	# Upgrade melee and archery units when winning against horses and guns
	if infos.unit(pWinningUnit).getUnitCombatType() in [UnitCombatTypes.UNITCOMBAT_MELEE, UnitCombatTypes.UNITCOMBAT_ARCHER]:
		pNewUnit = None
		if infos.unit(pLosingUnit).getUnitCombatType() in [UnitCombatTypes.UNITCOMBAT_HEAVY_CAVALRY, UnitCombatTypes.UNITCOMBAT_LIGHT_CAVALRY]:
			if civ(pWinningUnit.getOwner()) in dCivGroups[iCivGroupNative]:
				pNewUnit = captureUnit(pLosingUnit, pWinningUnit, iHorseArcher, 50)
			else:
				pNewUnit = captureUnit(pLosingUnit, pWinningUnit, iCuirassier, 50)
		elif infos.unit(pLosingUnit).getUnitCombatType() in [UnitCombatTypes.UNITCOMBAT_GUN]:
			pNewUnit = captureUnit(pLosingUnit, pWinningUnit, iArquebusier, 50)
		
		if pNewUnit:
			pNewUnit.convert(pWinningUnit)

@handler("combatResult")
def animalHunting(winningUnit, losingUnit):
	if losingUnit.getUnitType() in lAnimalUnits:
		iWinner = winningUnit.getOwner()
		if team(iWinner).isHasTech(iHunting) and player(iWinner).getNumCities() > 0:
			city = closestCity(winningUnit, iWinner)
			if city and distance(winningUnit, city) <= 10:
				iFood = scale(10)
				city.changeFood(iFood)
				
				message(iWinner, 'TXT_KEY_ANIMAL_HUNT_EFFECT', losingUnit.getName(), iFood, city.getName())
				
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
			
			# Freed slaves turn into population and add temorary unhappiness
			city.changePopulation(iNumSlaves)
			city.changeHurryAngerTimer(turns(iNumSlaves * 3))
			message(city.getOwner(), "TXT_KEY_MESSAGE_FREED_SLAVES", iNumSlaves, city.getName(), color=iGreen, location=city, button=infos.unit(iSlave).getButton())

				
		for slave in units.owner(iPlayer).where(lambda unit: base_unit(unit) in [iSlave, iChattleSlave]):
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

### BEGIN GAME TURN ###

@handler("BeginGameTurn")
def drainLakeTexcocoNormal():
	if turn() == year(1650):
		drainLakeTexcoco()

### GAME START ###

@handler("GameStart")
def drainLakeTexcoco1750():
	if scenario() == i1750AD:
		drainLakeTexcoco()

def drainLakeTexcoco():
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

### BEGIN PLAYER TURN ###

@handler("setPlayerAlive")
def updateLastTurnAlive(iPlayer, bAlive):
	if turn() == scenarioStartTurn():
		return

	if not bAlive and not (player(iPlayer).isHuman() and autoplay()):
		data.civs[iPlayer].iLastTurnAlive = game.getGameTurn()

### END PLAYER TURN ###

### PROJECT BUILT ###

# Migration
@handler("projectBuilt")
def detectMigrateCity(pCity, iProject):
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
	
	for iIndex, pOldCity in enumerate(data.lMigrateCities):
		iXNew = data.lMigrateX[iIndex]
		iYNew = data.lMigrateY[iIndex]
		
		iPlayer = pOldCity.getOwner()
		pPlayer = player(iPlayer)

		pOldPlot = pOldCity.plot()
		pNewPlot = gc.getMap().plot(iXNew, iYNew)

		# Nomads effect: If there was a tribe on the tile previously, add a population
		bMovedToTribe = False
		if pNewPlot.getImprovementType() in [iTribe, iContactedTribe]:
			bMovedToTribe = True
		
		# Mostly copied from CvPlatyBuilderScreen
		if pNewPlot.isCity(): return
		if pOldCity:
			pNewPlot.setImprovementType(-1)	# Make sure to clear improvement first (matters for Tribes)
			x, y = location(pNewPlot)
			pNewCity = pPlayer.initCity(x, y)
			sName = pOldCity.getName()
			pOldCity.setName("ToBeRazed", False)
			pNewCity.setName(sName, True)
			copyCityStats(pOldCity, pNewCity, True)
			pOldPlot = pOldCity.plot()
			pOldCity.kill()
			pOldPlot.setImprovementType(-1)
			pOldPlot.setRouteType(-1)
			# Remove any Indigenous units that might have been on the plot (i.e. Tribe Defenders)
			for i in range(pNewPlot.getNumUnits()-1, -1, -1):
				pUnit = pNewPlot.getUnit(i)
				if civ(pUnit) == iIndigenous:
					pUnit.kill(False, -1)

			# Also move any units fortified on the plot
			for i in range(pOldPlot.getNumUnits()-1, -1, -1):
				pUnit = pOldPlot.getUnit(i)
				if pUnit.isWaiting():
					move(pUnit, pNewPlot)
			
			if bMovedToTribe:
				pNewCity.changePopulation(1)
				message(iPlayer, 'TXT_KEY_TRIBE_INTEGRATED', sName, sound='AS2D_UNITGIFTED', event=1, button=infos.improvement(iTribe).getButton(), color=8, location=pNewPlot)


		# Nomads effect: give food based off yields of plots surrounding new city (even if migration failed for whatever reason)
		iMovedFood = 0
		for iI in range(-1, 2):
			for iJ in range(-1, 2):
				iMovedFood += min(gc.getMap().plot(iXNew + iI, iYNew + iJ).getYield(YieldTypes.YIELD_FOOD), 1)	# Add 1 food for each tile that has food
		if iMovedFood > 0:
			pNewCity.changeFood(scale(iMovedFood))
			message(iPlayer, 'TXT_KEY_MIGRATION_FOOD', sName, scale(iMovedFood), sound='AS3D_UN_CAMEL_DIE_VOX', event=1, button=infos.tech(iHunting).getButton(), color=8, location=pNewPlot)
		
		# Lakota UP: Great General points for migration
		if civ(iPlayer) == iLakota:
			iExp = scale(2)
			pPlayer.changeCombatExperience(iExp)
			message(iPlayer, 'TXT_KEY_MIGRATION_GREAT_GENERAL', sName, iExp, sound='AS3D_UN_WARLORD_COMMAND_VOX', event=1, button=infos.tech(iHunting).getButton(), color=8, location=pNewPlot)
		
		events.fireEvent("migration", iPlayer, 1)

	# Clear migration data
	data.lMigrateCities = []
	data.lMigrateX = []
	data.lMigrateY = []

# MacAurther: Copied from CvPlatyBuilderScreen
def copyCityStats(pOldCity, pNewCity, bMove):
		pNewCity.setPopulation(pOldCity.getPopulation())
		for iBuilding in xrange(gc.getNumBuildingInfos()):
			pNewCity.setBuildingProduction(iBuilding, pOldCity.getBuildingProduction(iBuilding))
			if gc.getBuildingInfo(iBuilding).isCapital() and not bMove: continue
			pNewCity.setNumRealBuilding(iBuilding, pOldCity.getNumRealBuilding(iBuilding))
		for iClass in xrange(gc.getNumBuildingClassInfos()):
			for iCommerce in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
				pNewCity.setBuildingCommerceChange(iClass, iCommerce, pOldCity.getBuildingCommerceChange(iClass, iCommerce))
			for iYield in xrange(YieldTypes.NUM_YIELD_TYPES):
				pNewCity.setBuildingYieldChange(iClass, iYield, pOldCity.getBuildingYieldChange(iClass, iYield))
	##		pNewCity.setBuildingHappyChange(iClass, pOldCity.getBuildingHappyChange(iClass))
	##		pNewCity.setBuildingHealthChange(iClass, pOldCity.getBuildingHealthChange(iClass))
		for iPlayerX in xrange(gc.getMAX_PLAYERS()):
			pNewCity.setCultureTimes100(iPlayerX, pOldCity.getCultureTimes100(iPlayerX), False)
		for iReligion in xrange(gc.getNumReligionInfos()):
			pNewCity.setHasReligion(iReligion, pOldCity.isHasReligion(iReligion), False, False)
			if bMove and pOldCity.isHolyCityByType(iReligion):
				CyGame().setHolyCity(iReligion, pNewCity, False)
			pNewCity.changeReligionInfluence(iReligion, pOldCity.getReligionInfluence(iReligion) - pNewCity.getReligionInfluence(iReligion))
			pNewCity.changeStateReligionHappiness(iReligion, pOldCity.getStateReligionHappiness(iReligion) - pNewCity.getStateReligionHappiness(iReligion))
		for iCorporation in xrange(gc.getNumCorporationInfos()):
			pNewCity.setHasCorporation(iCorporation, pOldCity.isHasCorporation(iCorporation), False, False)
			if bMove and pOldCity.isHeadquartersByType(iCorporation):
				CyGame().setHeadquarters(iCorporation, pNewCity, False)
		for iImprovement in xrange(gc.getNumImprovementInfos()):
			pNewCity.changeImprovementFreeSpecialists(iImprovement, pOldCity.getImprovementFreeSpecialists(iImprovement) - pNewCity.getImprovementFreeSpecialists(iImprovement))
		for iSpecialist in xrange(gc.getNumSpecialistInfos()):
			pNewCity.setFreeSpecialistCount(iSpecialist, pOldCity.getFreeSpecialistCount(iSpecialist))
			pNewCity.setForceSpecialistCount(iSpecialist, pOldCity.getForceSpecialistCount(iSpecialist))
		for iUnit in xrange(gc.getNumUnitInfos()):
			pNewCity.setUnitProduction(iUnit, pOldCity.getUnitProduction(iUnit))
			pNewCity.setGreatPeopleUnitProgress(iUnit, pOldCity.getGreatPeopleUnitProgress(iUnit))
		#for iCommerce in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
		#	pNewCity.changeSpecialistCommerce(iCommerce, pOldCity.getSpecialistCommerce(iCommerce) - pNewCity.getSpecialistCommerce(iCommerce))
		for iBonus in xrange(gc.getNumBonusInfos()):
			pNewCity.changeFreeBonus(iBonus, pOldCity.getFreeBonus(iBonus) - pNewCity.getFreeBonus(iBonus))
			while pOldCity.isNoBonus(iBonus) != pNewCity.isNoBonus(iBonus):
				if pOldCity.isNoBonus(iBonus):
					pNewCity.changeNoBonusCount(iBonus, 1)
				else:
					pNewCity.changeNoBonusCount(iBonus, -1)
		for iOrder in xrange(pOldCity.getOrderQueueLength()):
			OrderData = pOldCity.getOrderFromQueue(iOrder)
			pNewCity.pushOrder(OrderData.eOrderType, OrderData.iData1, OrderData.iData2, OrderData.bSave, False, True, False)
		pNewCity.changeBaseGreatPeopleRate(pOldCity.getBaseGreatPeopleRate() - pNewCity.getBaseGreatPeopleRate())
		pNewCity.changeConscriptAngerTimer(pOldCity.getConscriptAngerTimer() - pNewCity.getConscriptAngerTimer())
		pNewCity.changeDefenseDamage(pOldCity.getDefenseDamage() - pNewCity.getDefenseDamage())
		pNewCity.changeDefyResolutionAngerTimer(pOldCity.getDefyResolutionAngerTimer() - pNewCity.getDefyResolutionAngerTimer())
		pNewCity.changeEspionageHappinessCounter(pOldCity.getEspionageHappinessCounter() - pNewCity.getEspionageHappinessCounter())
		pNewCity.changeEspionageHealthCounter(pOldCity.getEspionageHealthCounter() - pNewCity.getEspionageHealthCounter())
		pNewCity.changeExtraHappiness(pOldCity.getExtraHappiness() - pNewCity.getExtraHappiness())
		pNewCity.changeExtraHealth(pOldCity.getExtraHealth() - pNewCity.getExtraHealth())
		pNewCity.changeExtraTradeRoutes(pOldCity.getExtraTradeRoutes() - pNewCity.getExtraTradeRoutes())
		pNewCity.changeGreatPeopleProgress(pOldCity.getGreatPeopleProgress() - pNewCity.getGreatPeopleProgress())
		pNewCity.changeHappinessTimer(pOldCity.getHappinessTimer() - pNewCity.getHappinessTimer())
		pNewCity.changeHurryAngerTimer(pOldCity.getHurryAngerTimer() - pNewCity.getHurryAngerTimer())
		pNewCity.setAirliftTargeted(pOldCity.isAirliftTargeted())
		pNewCity.setBombarded(pOldCity.isBombarded())
		pNewCity.setCitizensAutomated(pOldCity.isCitizensAutomated())
		pNewCity.setDrafted(pOldCity.isDrafted())
		pNewCity.setFeatureProduction(pOldCity.getFeatureProduction())
		pNewCity.setFood(pOldCity.getFood())
		pNewCity.setHighestPopulation(pOldCity.getHighestPopulation())
		pNewCity.setNeverLost(pOldCity.isNeverLost())
		pNewCity.setOccupationTimer(pOldCity.getOccupationTimer())
		pNewCity.setOverflowProduction(pOldCity.getOverflowProduction())
		pNewCity.setPlundered(pOldCity.isPlundered())
		pNewCity.setProduction(pOldCity.getProduction())
		pNewCity.setProductionAutomated(pOldCity.isProductionAutomated())
		pNewCity.setScriptData(pOldCity.getScriptData())
		pNewCity.setWallOverride(pOldCity.isWallOverride())

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
	targets = [(unit, infos.unit(unit).getProductionCost() * 3 / 2) for unit in units.at(location).owner(iIndigenous)]	# MacAurther: Can bribe indigenous instead of Barbs
	print("Targets: " + str(targets))
	return [(unit, iCost) for unit, iCost in targets if isBribableUnit(iPlayer, unit) and iCost <= iTreasury]


def canBribeUnits(spy):
	# MacAurther: Bribe-ability is now independent from being able to hurry units with gold
	if not (player(spy).hasCivic(iTribalConfederacy) or player(spy).hasCivic(iImperialism) or player(spy).hasCivic(iAssimilation)):
		return False
	
	# MacAurther: Don't care if it's someone elses territory
	# if plot(spy).isOwned() and plot(spy).getOwner() != spy.getOwner():
	# 	return False

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

### POPUPS ###

unit_bribe_popup = popup.text("TXT_KEY_BRIBE_UNITS_POPUP") \
						.selection(applyUnitBribes, "TXT_KEY_BRIBE_UNITS_BUTTON") \
						.cancel("TXT_KEY_BRIBE_UNITS_BUTTON_NONE") \
						.build()