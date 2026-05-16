# coding: utf-8

from Core import *
from Core import periodic as core_periodic
from RFCUtils import *
from Locations import *
from CityNames import applyRelocation
from Events import handler


def periodic(iTurns, seed):
	return (turn() + hash(seed)) % turns(iTurns) == 0


def best_civ_of_group(iGroup):
	return civs.of(*dTechGroups[iGroup]).alive().maximum(lambda c: player(c).getScoreHistory(turn()))


def best_civ_of_same_tech_group(iCiv):
	iTechGroup = next(iGroup for iGroup in dTechGroups if iCiv in dTechGroups[iGroup])
	return best_civ_of_group(iTechGroup)


def add_city_buildings(tile, iCiv):
	city(tile).rebuild(player(iCiv).getCurrentEra())
	return
		
	for iDefensiveBuilding in infos.buildings().where(isDefensiveBuilding):
		if player(iCiv).canConstruct(iDefensiveBuilding, False, False, False):
			city(tile).setHasRealBuilding(iDefensiveBuilding, True)


def is_new_world_discovered(_):
	return True in data.dFirstContactConquerors.values()


def is_free_of_civ(iCiv):
	def func(barbarians):
		return iCiv not in cities.rectangle(barbarians.area).owners()
	
	return func


def is_other_civ(iCiv):
	def func(barbarians):
		return cities.rectangle(barbarians.target_area).owners().without(iCiv).any()
	
	return func


def is_target_existing(iCiv):
	def func(_):
		return iCiv in players.major().existing()
	
	return func


class MinorCity(object):

	def __init__(self, iYear, iOwner, tile, name, tileName=None, iPopulation=1, iCiv=None, iCulture=0, bIgnoreRuins=False, bForce=False, units={}, buildings=[], bUnique=True, adjective=None, condition=lambda: True):
		self.iYear = iYear
		self.iOwner = iOwner
		self.tile = tile
		self.name = name
		self.tileName = tileName
		self.iPopulation = iPopulation
		self.iCiv = iCiv
		self.iCulture = iCulture
		self.bIgnoreRuins = bIgnoreRuins
		self.bForce = bForce
		self.units = units
		self.buildings = buildings
		self.bUnique = bUnique
		self.adjective = adjective
		self.condition = condition
	
	def check(self):
		if self.canFound():
			self.found()
		
		city = city_(self.tile)
		if not city:
			return
		
		if not is_minor(city.getOwner()):
			return
		
		if self.every(10):
			self.add_unit()
		
		if self.every(25):
			self.add_buildings()
	
	def canFound(self):
		if not self.bIgnoreRuins and plot(self.tile).getImprovementType() == iCityRuins:
			return False
	
		if year() < year(self.iYear):
			return False
		
		if year() >= year(self.iYear) + turns(10):
			return False
		
		if not self.condition():
			return False
			
		if self.bForce:
			if not isFree(self.iOwner, self.tile, bNoCity=True):
				return False
		
		else:
			if not player(self.iOwner).canFound(*location(self.tile)):
				return False
		
			if not isFree(self.iOwner, self.tile, bNoCity=True, bNoCulture=True) and not isFree(self.iOwner, self.tile, bNoCity=True, iCityDistance=2):
				return False
		
		return True
		
	def get_tech_civ(self):
		if self.iCiv is None or since(year(dBirth[self.iCiv])) < 0:
			return self.iOwner
		
		if slot(self.iCiv) >= 0:
			return self.iCiv
		
		lNeighbours = dNeighbours[self.iCiv]
		lTechGroup = next(lTechGroupCivs for iTechGroup, lTechGroupCivs in dTechGroups.items() if self.iCiv in lTechGroupCivs)
		
		lValidCivs = [iCiv for iCiv in set(lNeighbours) & set(lTechGroup) if self.iCiv != iCiv and since(year(dBirth[self.iCiv])) >= 0 and slot(iCiv) >= 0 and infos.civ(iCiv).getImpact() >= infos.civ(self.iCiv).getImpact()]

		if not lValidCivs:
			return self.iOwner
		
		return sorted(lValidCivs, key=lambda iCiv: abs(year(dBirth[iCiv]) - year(dBirth[self.iCiv])))[0]
	
	def found(self):
		iOwnerPlayer = slot(self.iOwner)
		x, y = location(self.tile)
		
		convertPlotCulture(self.tile, iOwnerPlayer, 100, bOwner=True)
		expelUnits(iOwnerPlayer, plots.surrounding(self.tile).where(lambda p: not p.isOwned()).including(self.tile))
		
		player(iOwnerPlayer).found(x, y)
		founded = city(x, y)
		
		if founded:
			iTechEra = player(self.get_tech_civ()).getCurrentEra()
			
			founded.setName(self.name, False)
			founded.setPopulation(self.iPopulation)
			
			founded.setCulture(founded.getOwner(), scale(self.iCulture) + iTechEra * scale(100), True)
			
			self.add_buildings()
			self.create_units()
			
			if self.tileName:
				applyRelocation(founded, self.tileName)
			
	def every(self, iTurns):
		return periodic(iTurns, self)
	
	def get_units(self):
		iUnitCiv = self.get_tech_civ()
		bUnique = self.bUnique and self.iCiv == iUnitCiv
		
		for iRole, iNumUnits in self.units.items():
			for iUnit, iUnitAI in getUnitsForRole(iUnitCiv, iRole, bUnique=bUnique):
				if iUnit is None:
					iUnit = iMilitia
				
				if not bUnique:
					iUnit = base_unit(iUnit)
				
				yield iUnit, iNumUnits, iUnitAI
	
	def make_units(self, iUnit, iUnitAI, iNumUnits=1):
		for unit in units.at(self.tile).where(lambda unit: unit.upgradeAvailable(unit.getUnitType(), infos.unit(iUnit).getUnitClassType(), 0)).limit(iNumUnits):
			unit.kill(False, -1)
		
		city = city_(self.tile)
		if not city:
			return
	
		created_units = makeUnits(city.getOwner(), iUnit, self.tile, iNumUnits, iUnitAI)
		
		if self.adjective:
			created_units.adjective(self.adjective)
	
	def create_units(self):
		for iUnit, iNumUnits, iUnitAI in self.get_units():
			if self.is_human_proximity():
				iNumUnits += 1
			
			self.make_units(iUnit, iUnitAI, iNumUnits)
	
	def add_unit(self):
		if units.surrounding(self.tile).atwar(city(self.tile).getOwner()):
			return
	
		iTechCiv = self.get_tech_civ()
	
		for iUnit, iNumUnits, iUnitAI in self.get_units():
			if units.surrounding(self.tile).type(iUnit).count() < iNumUnits + max(0, player(iTechCiv).getCurrentEra() - 1):
				self.make_units(iUnit, iUnitAI)
	
	def add_buildings(self):
		iTechCiv = self.get_tech_civ()
		add_city_buildings(self.tile, iTechCiv)
		
		for iBuilding in self.buildings:
			city(self.tile).setHasRealBuilding(iBuilding, True)
	
	def is_human_proximity(self):
		return plot(self.tile).getRegionID() == plot(dCapitals[active()]).getRegionID() or plot(self.tile).getPlayerWarValue(active()) >= 5


NUM_BARBARIAN_TYPES = 8
(ANIMALS, NOMADS, MINORS, INVADERS, CLOSE_INVADERS, NATIVES, SEA_INVADERS, PIRATES) = range(NUM_BARBARIAN_TYPES)


class Barbarians(object):

	SPAWN_LIMITS = {
		ANIMALS: 3,
		NOMADS: 3,
		MINORS: 5,
		NATIVES: 3,
		PIRATES: 3,
	}
	
	SPAWN_NOTIFICATIONS = {
		ANIMALS: "TXT_KEY_BARBARIAN_NOTIFICATION_ANIMALS",
		NOMADS: "TXT_KEY_BARBARIAN_NOTIFICATION_NOMADS",
		MINORS: "TXT_KEY_BARBARIAN_NOTIFICATION_MINORS",
		INVADERS: "TXT_KEY_BARBARIAN_NOTIFICATION_INVADERS",
		CLOSE_INVADERS: "TXT_KEY_BARBARIAN_NOTIFICATION_INVADERS",
		NATIVES: "TXT_KEY_BARBARIAN_NOTIFICATION_NATIVES",
		SEA_INVADERS: "TXT_KEY_BARBARIAN_NOTIFICATION_SEA_INVADERS",
		PIRATES: "TXT_KEY_BARBARIAN_NOTIFICATION_PIRATES"
	}

	def __init__(self, iStart, iEnd, units, area, iInterval, pattern, iOwner=iBarbarian, target_area=None, adjective=None, iAlternativeCiv=None, promotions=None, condition=None):
		self.iStart = iStart
		self.iEnd = iEnd
		self.units = units
		self.area = area
		self.iInterval = iInterval
		self.pattern = pattern
		self.iOwner = iOwner
		self.target_area = target_area
		self.adjective = adjective
		self.iAlternativeCiv = iAlternativeCiv
		self.promotions = promotions
		self.condition = condition
		
		if self.target_area is None:
			self.target_area = area
	
	def __repr__(self):
		return "%s barbarians: %s" % (text(self.adjective), format_separators(self.units.keys(), ", ", text("TXT_KEY_AND"), format=lambda iUnit: infos.unit(iUnit).getText()))
	
	def spawn_data(self):
		data = {
			"iStart": self.iStart,
			"iEnd": self.iEnd,
			"units": self.units,
			"iInterval": self.iInterval,
		}
		return data
	
	def check(self):
		if not self.is_active():
			return
		
		if self.can_spawn():
			self.spawn()
		
		elif self.can_cleanup():
			self.cleanup()
	
	def is_active(self):
		return year(self.iStart) <= year() <= year(self.iEnd)
	
	def can_spawn(self):
		if self.iAlternativeCiv is not None and player(self.iAlternativeCiv).isExisting():
			return False
		
		if self.condition is not None and not self.condition(self):
			return False
		
		if not self.every():
			return False
	
		if self.pattern in [NOMADS, INVADERS, CLOSE_INVADERS, SEA_INVADERS]:
			if not self.valid_targets():
				return False
		
		if self.spawn_limit():
			return False
		
		if self.pattern == MINORS:
			if plots.rectangle(self.area).land().all(lambda p: p.isOwned() and not owner(p, self.get_owner())):
				return False
	
		return True
	
	def every(self):
		return periodic(self.iInterval, self)
	
	def is_targeted(self):
		if self.pattern != INVADERS:
			return False
		
		if cities.rectangle(self.target_area).owner(active()).count() < cities.rectangle(self.target_area).count():
			return False
		
		if year() < year(dFall[active()]):
			return False
		
		return True
	
	def spawn(self):
		lSpawnPlots = self.get_spawn_plots()
		
		for iUnit, plot in zip(self.get_spawn_units(), lSpawnPlots):
			unit = makeUnit(self.get_owner(), iUnit, plot, self.get_unit_ai(iUnit, plot))
			
			data.units[unit].spawn_data = self.spawn_data()
			
			if self.adjective:
				set_unit_adjective(unit, self.adjective)
			
			if self.promotions:
				for iPromotion in self.promotions:
					unit.setHasPromotion(iPromotion, True)
		
		for plot in lSpawnPlots:
			if self.can_notify(plot):
				self.notify(plot)
	
	def can_cleanup(self):
		if self.condition and not self.condition(self):
			return True
		
		if self.iAlternativeCiv is not None and player(self.iAlternativeCiv).isExisting():
			return True
		
		return False
	
	def cleanup(self):
		if not player(self.iOwner).isExisting():
			return
		
		for unit in units.owner(self.iOwner).where(lambda unit: data.units[unit].spawn_data == self.spawn_data()):
			unit.kill(False, -1)
	
	def get_owner(self):
		if self.pattern == MINORS:
			minor_city = cities.rectangle(self.area).where(lambda city: is_minor(city.getOwner())).first()
			if minor_city:
				return civ(minor_city.getOwner())
		
		return self.iOwner
	
	def valid_targets(self):
		return cities.rectangle(self.target_area).any(lambda city: not is_minor(city.getOwner()))
	
	def count_existing(self, iUnit):
		return units.owner(self.iOwner).type(iUnit).where(lambda unit: data.units[unit].spawn_data == self.spawn_data()).count()
	
	def spawn_limit(self):
		iLimit = self.SPAWN_LIMITS.get(self.pattern)
		
		if iLimit is None:
			return False
			
		for iUnit, iNumUnits in self.units.items():
			if self.count_existing(iUnit) >= iLimit * iNumUnits:
				return True
		
		return False
	
	def get_units(self):
		for iUnit, iNumUnits in self.units.items():
			if self.is_targeted():
				iNumUnits += 1
			
			yield iUnit, iNumUnits
		
	def get_spawn_units(self):
		units = sum(([iUnit] * iNumUnits for iUnit, iNumUnits in self.get_units()), [])
		return sorted(units, key=lambda iUnit: infos.unit(iUnit).getDomainType())
	
	def get_spawn_plots(self):
		spawn_area = plots.rectangle(self.area).passable().where(self.valid_spawn)
		iNumUnits = sum(self.units.values())
		
		if not spawn_area:
			return []
		
		if self.pattern == MINORS:
			minor_city = spawn_area.cities().owner(self.get_owner()).random()
			if minor_city:
				return [minor_city] * iNumUnits
			
			return [spawn_area.random()] * iNumUnits
		
		elif self.pattern in [INVADERS, CLOSE_INVADERS, SEA_INVADERS]:
			return [spawn_area.random()] * iNumUnits
		
		else:
			return spawn_area.sample(iNumUnits)
	
	def get_unit_ai(self, iUnit, plot):
		if plot.isCity():
			return UnitAITypes.UNITAI_CITY_DEFENSE
	
		if self.pattern == PIRATES:
			return UnitAITypes.UNITAI_PIRATE_SEA
		
		elif self.pattern == ANIMALS:
			return UnitAITypes.UNITAI_ANIMAL
		
		elif self.pattern == SEA_INVADERS:
			if infos.unit(iUnit).getDomainType() == DomainTypes.DOMAIN_SEA:
				return UnitAITypes.UNITAI_ASSAULT_SEA
		
		return UnitAITypes.UNITAI_ATTACK
	
	@staticmethod
	def valid_unit_spawn_terrain(plot, iUnit):
		return Barbarians.valid_unit_spawn_terrain_plot(plot, iUnit) and plots.ring(plot).any(lambda p: Barbarians.valid_unit_spawn_terrain_plot(p, iUnit))
	
	@staticmethod
	def valid_unit_spawn_terrain_plot(plot, iUnit):
		if infos.unit(iUnit).getTerrainImpassable(plot.getTerrainType()) and not plot.isOwned():
			return False
		
		if plot.getFeatureType() >= 0 and infos.unit(iUnit).getFeatureImpassable(plot.getFeatureType()):
			return False
		
		return True
	
	def valid_spawn_terrain(self, plot):
		return all(self.valid_unit_spawn_terrain(plot, iUnit) for iUnit in self.units)
	
	def valid_spawn(self, plot):
		if plot.getBirthProtected() >= 0:
			return False
	
		if not self.valid_spawn_terrain(plot):
			return False
	
		if self.pattern in [SEA_INVADERS, PIRATES]:
			if plot.getTerrainType() not in [iCoast, iArcticCoast]:
				return False
			
			if map.getArea(plot.getArea()).isLake():
				return False
				
		else:
			if plot.isWater():
				return False
		
			if map.getArea(plot.getArea()).getNumCities() == 0:
				return False
		
		if units.at(plot).notowner(self.get_owner()):
			return False
			
		if self.pattern == CLOSE_INVADERS:
			if plot.isCity():
				return False
		elif cities.surrounding(plot):
			return False
		
		if self.pattern in [ANIMALS, NOMADS, MINORS, PIRATES]:
			if plot.isOwned():
				return False
		
		if self.pattern == ANIMALS:
			if cities.surrounding(plot, radius=3):
				return False
		
		if self.pattern == INVADERS:
			if not plots.surrounding(plot).where(lambda p: p.getOwner() != plot.getOwner() or p.isWater()):
				return False
		
		return True
	
	def can_notify(self, plot):
		if turn() <= self.iStart + turns(self.iInterval):
			if plot.isVisible(player().getTeam(), False):
				closest = closestCity(plot, owner=active(), same_continent=not plot.isWater(), coastal_only=plot.isWater())
				if closest and distance(plot, closest) <= 5:
					return True
		
		return False
	
	def notify(self, plot):
		adjective_text = text_if_exists(self.adjective, otherwise="TXT_KEY_ADJECTIVE_BARBARIAN")
		unit = infos.unit(self.units.items()[0][0])
		
		message(active(), self.SPAWN_NOTIFICATIONS[self.pattern], adjective_text, iColor=iRed, button=unit.getButton(), location=plot)


minor_cities = [
	MinorCity(400, iIndependent1, (42, 40), "Moche", iPopulation=1, iCiv=iChimu, units={iDefend: 2}, iCulture=5, adjective="TXT_KEY_ADJECTIVE_MOCHE"),			# Moche Culture
	MinorCity(950, iIndigenous, (49, 18), "Mapuches", iPopulation=1, iCiv=iInca, units={iDefend: 2}, iCulture=5, adjective="TXT_KEY_ADJECTIVE_MAPUCHE"),	 	# Mapuche
	# MinorCity(1660, iBarbarian, (48, 65), "Port Royal", iPopulation=1, iCiv=iEngland, units={iDefend: 2}, iCulture=5, adjective="TXT_KEY_ADJECTIVE_PIRATE"), 	# Port Royal
	# MinorCity(1670, iBarbarian, (46, 74), "Nassau", iPopulation=1, iCiv=iEngland, units={iDefend: 2}, iCulture=5, adjective="TXT_KEY_ADJECTIVE_PIRATE"),	 	# Nassau
]

barbarians = [
	Barbarians(1650, 1800, {iPrivateer: 1}, ((39, 63), (66, 71)), 10, PIRATES),
]


@handler("BeginGameTurn")
def onBeginGameTurn():
	for minor_city in minor_cities:
		minor_city.check()
	
	for barbarian in barbarians:
		barbarian.check()
	
	maintainFallenCivilizations()


@handler("unitBuilt")
def assignMinorUnitAdjective(city, unit):
	if not is_minor(city.getOwner()):
		return

	minor_city_adjective = next(minor_city.adjective for minor_city in minor_cities if at(city, minor_city.tile))
	if minor_city_adjective:
		set_unit_adjective(unit, minor_city_adjective)
	

# MacAurther: Because indpendents are now unique (i.e. some being native independents, some being European),
# 	Do not fragment
# @handler("BeginGameTurn")
# def fragmentIndependents():
# 	if year() >= year(50) and core_periodic(15):
# 		iLargestMinor = players.independent().maximum(lambda p: player(p).getNumCities())
# 		iSmallestMinor = players.independent().minimum(lambda p: player(p).getNumCities())
# 		if player(iLargestMinor).getNumCities() > 2 * player(iSmallestMinor).getNumCities():
# 			for city in cities.owner(iLargestMinor).sample(3):
# 				completeCityFlip(city, iSmallestMinor, iLargestMinor, 50, bBarbarianDecay=False, bBarbarianConversion=True, bAlwaysOwnPlots=True, bFlipUnits=True)


@handler("BeginGameTurn")
def checkMinorTechs():
	iMinor = players.civs(iIndependent1, iIndependent2, iIndigenous).existing().periodic(8)
	if iMinor:
		updateMinorTechs(iMinor, barbarian())


def maintainFallenCivilizations():
	fallen_civs = civs.major().past_birth().notalive().where(canEverRespawn)
	
	for iFallenCiv in fallen_civs:
		if periodic(20, iFallenCiv):
			fallen_cities = cities.respawn(iFallenCiv).where(is_minor).where(lambda city: plot(city).getExpansion() == -1)
			
			if fallen_cities:
				iTechCiv = best_civ_of_same_tech_group(iFallenCiv)
				if iTechCiv < 0:
					iTechCiv = iFallenCiv
				
				if slot(iTechCiv) < 0:
					continue
				
				iNumDesiredUnits = 2 + player(iTechCiv).getCurrentEra() / 2
				bUnique = iFallenCiv == iTechCiv
				iDefender, iDefenseAI = getUnitForRole(iTechCiv, iDefend, bUnique=bUnique)
				
				for city in fallen_cities:
					add_city_buildings(city, iTechCiv)
					
					iNumCurrentUnits = units.at(city).where(CyUnit.canFight).count()
					if iNumCurrentUnits < iNumDesiredUnits:
						makeUnits(city.getOwner(), iDefender, city, iNumDesiredUnits-iNumCurrentUnits, iDefenseAI)

# MacAurther: Tribes
@handler("tribeAttacked")
def spawnTribeDefenders(pPlot, iAttacker):
	iNumDefenders = pPlot.getTribeStoredUnits()

	lSpecialUnits = []	# List of special units that can be spawned on this plot

	iTechLevel = 0	# How advanced spawned units should be - <=0: early game (ancient), =1: mid game (medieval), >=2: late game (gunpowder/horse)
	if pPlot.getRegionID() in [rYukon, rNunavut, rQuebec, rNewFoundland, rHawaii] + lBrazil + lArgentina + [rGuyana, rParaguay, rUruguay]: iTechLevel -= 1
	if year() >= year(1350): iTechLevel += 1
	if year() >= year(1820): iTechLevel += 1
	# Contacted tribes get +1 Tech Level
	if pPlot.getImprovementType() == iContactedTribe: iTechLevel += 1

	# Put tech level in bounds
	iTechLevel = max(iTechLevel, 0)
	iTechLevel = min(iTechLevel, 2)

	# Build list of possible unique units to plut in plot based off of historical area
	for iCiv in dCivGroups[iCivGroupNative]:
		if iCiv == civ(iAttacker): continue		# don't spawn the unique unit of the attacker
		if pPlot.getSettlerValue(iCiv) > 0:
			for iUnit in range(iMilitia, iWorkboat):	# Don't consider special settlers, works, scouts, spies, naval units, etc.
				# Civilization unique units
				iUniqueUnit = unique_unit_civ(iCiv, iUnit)
				if base_unit(iUnit) == iUnit and iUniqueUnit != iUnit:
					# Tech Level 0 excludes any units that require bonuses
					if iTechLevel == 0 and (infos.unit(iUniqueUnit).getPrereqOrBonuses(0) != -1 or infos.unit(iUniqueUnit).getPrereqAndBonus() != -1): continue
					# Tech Level 1 excludes any Gunpowder or Mounted units
					if iTechLevel <= 1 and (infos.unit(iUniqueUnit).getUnitCombatType() in \
					   [UnitCombatTypes.UNITCOMBAT_GUN, UnitCombatTypes.UNITCOMBAT_LIGHT_CAVALRY, UnitCombatTypes.UNITCOMBAT_HEAVY_CAVALRY]): 
						continue
					lSpecialUnits.append(iUniqueUnit)
	
	# See if Horse Archers are viable
	if iTechLevel == 2 and pPlot.getTerrainType() in [iPlains, iPrairie] and pPlot.getFeatureType() == FeatureTypes.NO_FEATURE and pPlot.getSettlerValue(iLakota) == 0:
		lSpecialUnits.append(iHorseArcher)
					
	# Select basic defender based on tech level
	lBasicDefender = [iMilitia, iArcher, iLongbowman]
	lAdvancedDefender = [iArcher, iLongbowman, iArquebusier]
	for iI in range(iNumDefenders):
		# First two defenders are basic
		if iI < 2: iUnit = lBasicDefender[iTechLevel]
		# Next defender is advanced
		elif iI < 3: iUnit = lAdvancedDefender[iTechLevel]
		# The rest are either unique or advanced
		else:
			if len(lSpecialUnits) > 0:
				iUnit = lSpecialUnits[(iI - 3) % len(lSpecialUnits)]	# Cycle through available unique units
			else:
				iUnit = lAdvancedDefender[iTechLevel]

		makeUnits(slot(iIndigenous), iUnit, pPlot, 1, UnitAITypes.UNITAI_SIT_FOREVER)
	
	message(iAttacker, 'TXT_KEY_TRIBE_DEFENDERS', sound='AS2D_GOODY_HOSTILE', event=1, button=infos.unit(iUnit).getButton(), color=7, location=pPlot)
	pPlot.setTribeStoredUnits(0)

@handler("unitPillage")
def tribePillage(pUnit, iImprovement, iRoute, iOwner, iGold):
	# If pillage a tribe, do cleanup and enslavement
	if iImprovement == iTribe or iImprovement == iContactedTribe:
		# Check for any slave capturing
		enslaveUnit(pUnit)