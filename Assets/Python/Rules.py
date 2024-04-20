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
			if iNationalWonder != iPalace and isNationalWonderClass(infos.building(iNationalWonder).getBuildingClassType()) and city.hasBuilding(iNationalWonder):
				city.setHasRealBuilding(iNationalWonder, False)


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


### COMBAT RESULT ###
		
@handler("combatResult")
def captureSlaves(winningUnit, losingUnit):
	if plot(winningUnit).isWater() and freeCargo(winningUnit, winningUnit) <= 0:
		return

	# Mesoamerica RP
	if civ(winningUnit) in (iAztecs, iMaya, iTeotihuacan, iZapotec, iPurepecha):
		captureUnit(losingUnit, winningUnit, iNativeSlave1, 50)
		return
	
	if civ(losingUnit) == iNative and winningUnit.getUnitType() == iBandeirante and player(winningUnit).canUseSlaves():
		captureUnit(losingUnit, winningUnit, iNativeSlave2, 100)
		return
	
	if players.major().alive().none(lambda p: team(p).isHasTech(iOldWorldTactics)):
		return
		
	if civ(losingUnit) == iNative:
		if civ(winningUnit) not in lBioNewWorld or any(data.dFirstContactConquerors.values()):
			if player(winningUnit).isSlavery() or player(winningUnit).isColonialSlavery():
				captureUnit(losingUnit, winningUnit, iNativeSlave2, 50)

@handler("combatResult")
def captureCannon(winningUnit, losingUnit):
	if losingUnit.getUnitType() in [iBombard, iCannon, iArtillery, iHowitzer, iLightCannon, iFieldGun, iGatlingGun]:
		captureUnit(losingUnit, winningUnit, losingUnit.getUnitType(), 50)

@handler("combatResult")
def captureAdvancedUnit(winningUnit, losingUnit):
	# Wilderness RP
	if civ(winningUnit) in (iIroquois, iPuebloan, iMississippi):
		if losingUnit.getUnitType() in lWildernessRPGunUnits:
			captureUnit(losingUnit, winningUnit, iArmedBrave, 50)
		elif losingUnit.getUnitType() in lWildernessRPHorseUnits:
			captureUnit(losingUnit, winningUnit, iHorseArcher, 50)
		elif losingUnit.getUnitType() in lWildernessRPHorseGunUnits:
			captureUnit(losingUnit, winningUnit, iMountedBrave, 50)

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
		city.changePopulation(1)


### REVOLUTION ###

@handler("revolution")
def validateSlaves(iPlayer):
	if not player(iPlayer).canUseSlaves():
		if player(iPlayer).getImprovementCount(iSlavePlantation) > 0:
			for plot in plots.owner(iPlayer).where(lambda plot: plot.getImprovementType() == iSlavePlantation):
				plot.setImprovementType(iPlantation)
		
		for city in cities.owner(iPlayer):
			city.setFreeSpecialistCount(iSpecialistSlave, 0)
				
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
