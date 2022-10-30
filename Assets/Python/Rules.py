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
	if player(iPlayer).canUseSlaves():
		freeSlaves(city, iPlayer)
	else:
		city.setFreeSpecialistCount(iSpecialistSlave, 0)
		

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
def spreadTradingCompanyCulture(iOwner, iPlayer, city, bConquest, bTrade):
	if bTrade and iPlayer in dTradingCompanyPlots and location(city) in dTradingCompanyPlots[iPlayer]:
		for plot in plots.surrounding(city):
			if location(plot) == location(city):
				convertPlotCulture(plot, iPlayer, 51, False)
			elif plot.isCity():
				pass
			elif distance(plot, city) == 1:
				convertPlotCulture(plot, iPlayer, 65, True)
			elif pPlot.getOwner() == iPreviousOwner:
				convertPlotCulture(plot, iPlayer, 15, False)


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
def americanPioneerAbility(city):
	iPlayer = city.getOwner()
	if civ(iPlayer) == iAmerica:
		if city.getRegionID() in lNorthAmerica:
			createGarrisons(city, iPlayer, 1)
			createRoleUnit(iPlayer, city, iWork, 1)


### COMBAT RESULT ###
		
@handler("combatResult")
def captureSlaves(winningUnit, losingUnit):
	if plot(winningUnit).isWater() and freeCargo(winningUnit, winningUnit) <= 0:
		return

	if civ(winningUnit) == iAztecs:
		captureUnit(losingUnit, winningUnit, iAztecSlave, 50)
		return
	
	if civ(losingUnit) == iNative and winningUnit.getUnitType() == iBandeirante and player(winningUnit).canUseSlaves():
		captureUnit(losingUnit, winningUnit, iSlave, 100)
		return
	
	if players.major().alive().none(lambda p: team(p).isHasTech(iOldWorldTactics)):
		return
		
	if civ(losingUnit) == iNative:
		if civ(winningUnit) not in lBioNewWorld or any(data.dFirstContactConquerors.values()):
			if player(winningUnit).isSlavery() or player(winningUnit).isColonialSlavery():
				captureUnit(losingUnit, winningUnit, iSlave, 50)


@handler("combatResult")
def mayanHolkanAbility(winningUnit, losingUnit):
	if winningUnit.getUnitType() == iHolkan:
		iWinner = winningUnit.getOwner()
		if player(iWinner).getNumCities() > 0:
			city = closestCity(winningUnit, iWinner)
			if city:
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
		
		for city in cities.owner(iPlayer):
			city.setFreeSpecialistCount(iSpecialistSlave, 0)
				
		for slave in units.owner(iPlayer).where(lambda unit: base_unit(unit) == iSlave):
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
		iJungle : 20,
		iRainforest : 20,
	}, 0)
	
	if civ(plot) == iBrazil:
		iGold = dFeatureGold[iFeature]
		
		if iGold > 0:
			player(plot).changeGold(iGold)
			message(plot.getOwner(), 'TXT_KEY_DEFORESTATION_EVENT', infos.feature(iFeature).getText(), city.getName(), iGold, type=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.commerce(0).getButton(), location=plot)


### BEGIN GAME TURN ###

@handler("BeginGameTurn")
def checkImmigration(iGameTurn):
	if iGameTurn < year(dBirth[iAmerica]) + turns(5):
		return

	data.iImmigrationTimer -= 1
	
	if data.iImmigrationTimer == 0:
		immigration()
		data.iImmigrationTimer = 3 + rand(turns(5))


### TECH ACQUIRED ###

@handler("techAcquired")
def relocateCapitals(iTech, iTeam, iPlayer):
	if not player(iPlayer).isHuman():
		iEra = infos.tech(iTech).getEra()
		if (iPlayer, iEra) in dRelocatedCapitals:
			relocateCapital(iPlayer, dRelocatedCapitals[iPlayer, iEra])


### END GAME TURN ###

@handler("EndGameTurn")
def startTimedConquests():
	for iConqueror, tPlot in data.lTimedConquests:
		colonialConquest(iConqueror, tPlot)
	
	data.lTimedConquests = []


### BEGIN PLAYER TURN ###

@handler("setPlayerAlive")
def updateLastTurnAlive(iPlayer, bAlive):
	if turn() == scenarioStartTurn():
		return

	if not bAlive and not (player(iPlayer).isHuman() and autoplay()):
		data.civs[iPlayer].iLastTurnAlive = game.getGameTurn()


### IMPLEMENTATIONS ###

def getImmigrationValue(city):
	iFoodDifference = city.foodDifference(False)
	iHappinessDifference = city.happyLevel() - city.unhappyLevel(0)
	
	iValue = 0
	
	iValue += max(0, iHappinessDifference)
	iValue += max(0, iFoodDifference / 2)
	iValue += city.getPopulation() / 2
	
	if city.getRegionID() in lNorthAmerica:
		iValue += 5
		
	return iValue
	
	
def getEmigrationValue(city):
	iFoodDifference = city.foodDifference(False)
	iHappinessDifference = city.happyLevel() - city.unhappyLevel(0)
	
	iValue -= min(0, iHappinessDifference)
	iValue -= min(0, iFoodDifference / 2)
	iValue += city.getPopulation() / 5
	
	return iValue


def immigration():
	sourcePlayers = players.major().alive().where(lambda p: player(p).getCapitalCity().getRegionID() not in lNewWorld).where(lambda p: cities.owner(p).any(lambda city: getEmigrationValue(city) > 0))
	targetPlayers = players.major().alive().where(lambda p: player(p).getCapitalCity().getRegionID() in lNewWorld).where(lambda p: cities.owner(p).any(lambda city: getImmigrationValue(city) > 0))
	
	iNumMigrations = min(sourcePlayers.count(), targetPlayers.count())
	
	sourceCities = sourcePlayers.cities().where(lambda city: city.getPopulation() > 1).highest(iNumMigrations, getEmigrationValue)
	targetCities = targetPlayers.cities().highest(iNumMigrations, getImmigrationValue)
	
	for sourceCity, targetCity in zip(sourceCities, targetCities):
		iPopulation = 1
		if sourceCity.getPopulation() >= 9:
			iPopulation += 1
	
		sourceCity.changePopulation(-iPopulation)
		targetCity.changePopulation(iPopulation)
			
		# extra cottage growth for target city's vicinity
		for pCurrent in plots.surrounding(targetCity, radius=2):
			if pCurrent.getWorkingCity() == targetCity:
				pCurrent.changeUpgradeProgress(turns(10))
					
		# migration brings culture
		targetPlot = plot(city)
		iTargetPlayer = targetCity.getOwner()
		iSourcePlayer = sourceCity.getOwner()
		
		iCultureChange = targetPlot.getCulture(iTargetPlayer) / targetCity.getPopulation()
		targetPlot.changeCulture(iSourcePlayer, iCultureChange, False)
		
		iCultureChange = targetCity.getCulture(iTargetPlayer) / targetCity.getPopulation()
		targetCity.changeCulture(iSourcePlayer, iCultureChange, False, False)
		
		# chance to spread religions in source city
		lReligions = [iReligion for iReligion in range(iNumReligions) if sourceCity.isHasReligion(iReligion) and not targetCity.isHasReligion(iReligion)]
		if player(iSourcePlayer).getStateReligion() in lReligions:
			lReligions.append(player(iSourcePlayer).getStateReligion())
		
		if rand(1, 4) <= len(lReligions):
			targetCity.setHasReligion(random_entry(lReligions), True, True, True)
					
		# notify affected players
		message(iSourcePlayer, 'TXT_KEY_UP_EMIGRATION', sourceCity.getName(), event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.unit(iSettler).getButton(), color=iYellow, location=sourceCity)
		message(iTargetPlayer, 'TXT_KEY_UP_IMMIGRATION', targetCity.getName(), event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.unit(iSettler).getButton(), color=iYellow, location=targetCity)

		events.fireEvent("immigration", sourceCity, targetCity, iPopulation, iCultureChange)