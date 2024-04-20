from Core import *
from BaseRequirements import *


# First Tibetan UHV goal
class AcquiredCities(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ACQUIRE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_ACQUIRED_CITIES"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_ACQUIRED_CITIES"
	
	def __init__(self, *parameters, **options):
		TrackRequirement.__init__(self, *parameters, **options)
		
		self.recorded = set()
		
		self.handle("cityAcquired", self.record_city)
		self.handle("cityBuilt", self.record_city)
	
	def record_city(self, goal, city, *args):
		self.recorded.add(location(city))
		goal.check()
	
	def evaluate(self, evaluator):
		return len(self.recorded)
		

# Third Canadian UHV goal
class BrokeredPeace(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_BROKERED_PEACE"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_BROKERED_PEACE"

	def __init__(self, *parameters, **options):
		TrackRequirement.__init__(self, *parameters, **options)
		
		self.incremented("peaceBrokered")


# Third Vedic URV goal
class CelebrateTurns(TrackRequirement):

	TYPES = (COUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CELEBRATE_TURNS"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CELEBRATE_TURNS"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, turns(iRequired), **options)
		
		self.handle("BeginPlayerTurn", self.accumulate_celebrate_turns)
		
	def accumulate_celebrate_turns(self, goal, iGameTurn, iPlayer):
		iCelebratingCities = cities.owner(iPlayer).count(CyCity.isWeLoveTheKingDay)
		
		if iCelebratingCities > 0:
			self.accumulate(iCelebratingCities)
			goal.check()


# Third Maya Teotl URV goal
class CombatFood(TrackRequirement):

	TYPES = (AMOUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_GAIN"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_COMBAT_FOOD"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_COMBAT_FOOD"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, iRequired, **options)
		
		self.accumulated("combatFood")


# First Moorish UHV goal
# Second Dutch UHV goal
class ConqueredCities(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONQUER"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CONQUERED_CITIES"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CONQUERED_CITIES"
	
	def __init__(self, iRequired, civs=None, inside=None, outside=None, **options):
		TrackRequirement.__init__(self, iRequired, civs=civs, inside=inside, outside=outside, **options)
		
		self.recorded = set()
		self.civs = civs
		self.inside = inside
		self.outside = outside
		
		self.handle("cityAcquired", self.record_conquered_city)
		
	def valid_city(self, city):
		if self.civs is not None and Civ(city.getPreviousCiv()) not in self.civs:
			return False
	
		if self.inside is not None and city not in self.inside:
			return False
		
		if self.outside is not None and city in self.outside:
			return False
		
		return True
	
	def record_conquered_city(self, goal, city, bConquest):
		if bConquest and self.valid_city(city):
			self.recorded.add(location(city))
			goal.check()
	
	def evaluate(self, evaluator):
		return evaluator.sum(lambda p: cities.owner(p).where(lambda city: location(city) in self.recorded).count())
	
	def additional_formats(self):
		cities = text("TXT_KEY_VICTORY_CITIES")
		cities = qualify_adjective(cities, CIVS, self.civs)
		cities = in_area(cities, self.inside)
		cities = outside_area(cities, self.outside)
		
		return [cities]
	
	def areas(self):
		areas = {}
		
		if self.inside is not None:
			areas[self.inside.name()] = self.inside.create()
		
		if self.outside is not None:
			areas[self.outside.name()] = plots.all().without(self.outside.create())
		
		return areas


# Third Aztec UHV goal
class EnslaveCount(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ENSLAVE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_ENSLAVE_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_ENSLAVE_COUNT"
	
	def __init__(self, iRequired, excluding=None, **options):
		TrackRequirement.__init__(self, iRequired, **options)
		
		self.excluding = excluding
		
		self.handle("enslave", self.increment_enslaved)
	
	def increment_enslaved(self, goal, unit):
		if is_minor(unit):
			return
		
		if self.excluding and civ(unit) in self.excluding:
			return
		
		self.increment()
		goal.check()
	
	def additional_formats(self):
		units = text("TXT_KEY_VICTORY_UNITS")
		units = qualify_adjective(units, CIVS, self.excluding)
		
		return [units]
	

# Third Japanese UHV goal
# Third English UHV goal
# Third German UHV goal
class EraFirstDiscover(TrackRequirement):

	TYPES = (ERA, COUNT)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_FIRST_DISCOVER"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_ERA_FIRST_DISCOVER"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_ERA_FIRST_DISCOVER"
	
	def __init__(self, iEra, iRequired, **options):
		TrackRequirement.__init__(self, iEra, iRequired, **options)
		
		self.iEra = iEra
		
		self.handle("techAcquired", self.increment_first_discovered)
		self.expire("techAcquired", self.expire_insufficient_techs_left)
		
	def increment_first_discovered(self, goal, iTech):
		if self.iEra == infos.tech(iTech).getEra():
			if game.countKnownTechNumTeams(iTech) == 1:
				self.increment()
				goal.check()
	
	def expire_insufficient_techs_left(self, goal, iTech):
		if self.iEra == infos.tech(iTech).getEra():
			if self.iValue + self.remaining_techs() < self.required():
				goal.expire()
	
	def remaining_techs(self):
		return count(infos.tech(iTech).getEra() == self.iEra and game.countKnownTechNumTeams(iTech) == 0 for iTech in infos.techs())
		
	def progress(self, evaluator):
		return "%s (%s)" % (ThresholdRequirement.progress(self, evaluator), text("TXT_KEY_VICTORY_PROGRESS_REMAINING", self.remaining_techs()))


# Third Chinese UHV goal
# First Argentine UHV goal
# Third Argentine UHV goal
# Second Hindu URV goal
class GoldenAges(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_EXPERIENCE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_GOLDEN_AGES"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_GOLDEN_AGES"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, iRequired, **options)
		
		self.handle("BeginPlayerTurn", self.increment_golden_ages)
	
	def required(self):
		return scale(infos.constant("GOLDEN_AGE_LENGTH") * self.iRequired)
	
	def increment_golden_ages(self, goal, iGameTurn, iPlayer):
		if player(iPlayer).isGoldenAge() and not player(iPlayer).isAnarchy():
			self.increment()
			goal.check()
	
	def progress_value(self, evaluator):
		iGoldenAgeLength = infos.constant("GOLDEN_AGE_LENGTH")
		return "%d / %d" % (self.evaluate(evaluator) / scale(iGoldenAgeLength), self.iRequired)


# Second Mexican UHV goal
class GreatGenerals(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CREATE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_GREAT_GENERALS"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_GREAT_GENERALS"
	
	def __init__(self, *parameters, **options):
		TrackRequirement.__init__(self, *parameters, **options)
		
		self.handle("greatPersonBorn", self.increment_great_generals)
	
	def increment_great_generals(self, goal, unit):
		if infos.unit(unit).getGreatPeoples(iSpecialistGreatGeneral):
			self.increment()
			goal.check()


# Second Buddhist URV goal
class HappiestTurns(TrackRequirement):

	TYPES = (COUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_HAPPIEST_TURNS"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_HAPPIEST_TURNS"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, turns(iRequired), **options)
		
		self.handle("BeginPlayerTurn", self.increment_happiest)
		
	def increment_happiest(self, goal, iGameTurn, iPlayer):
		if players.major().alive().maximum(self.calculate_happiness_rating) == iPlayer:
			self.increment()
			goal.check()
	
	def calculate_happiness_rating(self, iPlayer):
		if not player(iPlayer).isAlive():
			return 0
		
		iHappy = player(iPlayer).calculateTotalCityHappiness()
		iUnhappy = player(iPlayer).calculateTotalCityUnhappiness()
		
		return (iHappy * 100) / max(1, iHappy + iUnhappy)


# First Taoist URV goal
class HealthiestTurns(TrackRequirement):

	TYPES = (COUNT,)
	
	DESC_KEY = "TXT_KEY_VICTORY_DESC_HEALTHIEST_TURNS"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_HEALTHIEST_TURNS"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, turns(iRequired), **options)
		
		self.handle("BeginPlayerTurn", self.increment_healthiest)
	
	def increment_healthiest(self, goal, iGameTurn, iPlayer):
		if players.major().alive().maximum(self.calculate_health_rating) == iPlayer:
			self.increment()
			goal.check()
		
	def calculate_health_rating(self, iPlayer):
		if not player(iPlayer).isAlive():
			return 0
		
		iHealthy = player(iPlayer).calculateTotalCityHealthiness()
		iUnhealthy = player(iPlayer).calculateTotalCityUnhealthiness()
		
		return (iHealthy * 100) / max(1, iHealthy + iUnhealthy)


# First Buddhist URV goal
class PeaceTurns(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_BE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_PEACE_TURNS"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_PEACE_TURNS"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, turns(iRequired), **options)
		
		self.handle("BeginPlayerTurn", self.increment_peace_turns)
		
	def increment_peace_turns(self, goal, iGameTurn, iPlayer):
		if players.major().alive().none(lambda p: team(iPlayer).isAtWar(p)):
			self.increment()
			goal.check()


# First Turkic UHV goal
class PillageCount(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_PILLAGE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_PILLAGE_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_PILLAGE_COUNT"
	
	def __init__(self, *parameters, **options):
		TrackRequirement.__init__(self, *parameters, **options)
		
		self.incremented("unitPillage")


# Third Moorish UHV goal
class PiracyGold(TrackRequirement):

	TYPES = (AMOUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ACQUIRE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_PIRACY_GOLD"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_PIRACY_GOLD"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, iRequired, **options)
		
		self.accumulated("unitPillage")
		self.accumulated("blockade")
		self.accumulated("combatGold")


# First Catholic URV goal
class PopeTurns(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_BE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_POPE_TURNS"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_POPE_TURNS"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, turns(iRequired), **options)
		
		self.handle("BeginPlayerTurn", self.increment_pope)
	
	def increment_pope(self, goal, iGameTurn, iPlayer):
		if game.getSecretaryGeneral(1) == iPlayer:
			self.increment()
			goal.check()


# Third Viking UHV goal
class RaidGold(TrackRequirement):

	TYPES = (AMOUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ACQUIRE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_RAID_GOLD"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_RAID_GOLD"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, iRequired, **options)
		
		self.accumulated("unitPillage")
		self.accumulated("cityCaptureGold")
		self.accumulated("combatGold")


# Second Mongol UHV goal
class RazeCount(TrackRequirement):

	TYPES = (COUNT,)

	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_RAZE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_RAZE_COUNT"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_RAZE_COUNT"
	
	def __init__(self, *parameters, **options):
		TrackRequirement.__init__(self, *parameters, **options)
		
		self.incremented("cityRazed")


# Third Colombian UHV goal
class ResourceTradeGold(TrackRequirement):

	TYPES = (AMOUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ACQUIRE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_RESOURCE_TRADE_GOLD"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_RESOURCE_TRADE_GOLD"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, iRequired, **options)
		
		self.handle("BeginPlayerTurn", self.accumulate_trade_deal_gold)
	
	def accumulate_trade_deal_gold(self, goal, iGameTurn, iPlayer):
		iGold = players.major().alive().sum(lambda p: player(iPlayer).getGoldPerTurnByPlayer(p))
		self.accumulate(iGold)
		goal.check()


# Third Aztec Teotl URV goal
class SacrificeHappiness(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_SACRIFICE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_SACRIFICE_HAPPINESS"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_SACRIFICE_HAPPINESS"
	
	def __init__(self, *parameters, **options):
		TrackRequirement.__init__(self, *parameters, **options)
		
		self.incremented("sacrificeHappiness")


# First Russian UHV goal
class SettledCities(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_SETTLE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_SETTLED_CITIES"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_SETTLED_CITIES"
	
	def __init__(self, iRequired, area=None, **options):
		TrackRequirement.__init__(self, iRequired, area=area, **options)
		
		self.recorded = set()
		self.area = area
		
		self.handle("cityBuilt", self.record_settled_city)
		
	def valid_city(self, city):
		return self.area is None or city in self.area
	
	def record_settled_city(self, goal, city):
		if self.valid_city(city):
			self.recorded.add(location(city))
			goal.check()
	
	def evaluate(self, evaluator):
		return evaluator.sum(lambda p: cities.owner(p).where(lambda city: location(city) in self.recorded).count())
	
	def additional_formats(self):
		cities = text("TXT_KEY_VICTORY_CITIES")
		cities = in_area(cities, self.area)
		
		return [cities]
	
	def areas(self):
		if self.area is not None:
			return {self.area.name(): self.area.create()}
		return {}


# Second Congolese UHV goal
class SlaveTradeGold(TrackRequirement):

	TYPES = (AMOUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ACQUIRE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_SLAVE_TRADE_GOLD"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_SLAVE_TRADE_GOLD"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, iRequired, **options)
		
		self.accumulated("playerSlaveTrade")
	

# Third Korean UHV goal
# Second English UHV goal
class SunkShips(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_SINK"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_SUNK_SHIPS"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_SUNK_SHIPS"
	
	def __init__(self, *parameters, **options):
		TrackRequirement.__init__(self, *parameters, **options)
		
		self.handle("combatResult", self.increment_ships_sunk)
		
	def increment_ships_sunk(self, goal, unit):
		if infos.unit(unit).getDomainType() == DomainTypes.DOMAIN_SEA:
			self.increment()
			goal.check()


# Third Tamil UHV goal
class TradeGold(TrackRequirement):

	TYPES = (AMOUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_ACQUIRE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_TRADE_GOLD"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_TRADE_GOLD"
	
	def __init__(self, iRequired, **options):
		TrackRequirement.__init__(self, iRequired, **options)
		
		self.handle("playerGoldTrade", self.accumulate_trade_gold)
		self.handle("tradeMission", self.accumulate_trade_mission_gold)
		self.handle("BeginPlayerTurn", self.accumulate_trade_deal_gold)
		self.handle("BeginPlayerTurn", self.accumulate_trade_route_gold)
	
	def accumulate_trade_gold(self, goal, iGold):
		self.accumulate(iGold * 100)
		goal.check()
	
	def accumulate_trade_mission_gold(self, goal, tile, iGold):
		self.accumulate(iGold * 100)
		goal.check()
	
	def accumulate_trade_deal_gold(self, goal, iGameTurn, iPlayer):
		iGold = players.major().alive().sum(lambda p: player(iPlayer).getGoldPerTurnByPlayer(p))
		self.accumulate(iGold * 100)
		goal.check()
	
	def accumulate_trade_route_gold(self, goal, iGameTurn, iPlayer):
		iGold = cities.owner(iPlayer).sum(lambda city: city.getTradeYield(YieldTypes.YIELD_COMMERCE)) * player(iPlayer).getCommercePercent(CommerceTypes.COMMERCE_GOLD)
		self.accumulate(iGold)
		goal.check()

	def evaluate(self, evaluator):
		return self.iValue / 100


class ContactTribe(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTACT"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_CONTACT_TRIBE"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_CONTACT_TRIBE"
	
	def __init__(self, *parameters, **options):
		TrackRequirement.__init__(self, *parameters, **options)
		
		self.handle("goodyReceived", self.increment_tribes_contacted)
		
	def increment_tribes_contacted(self, goal):
		self.increment()
		goal.check()


class ReligionSpreads(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_CONVERT"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_SPREAD_RELIGION"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_SPREAD_RELIGION"
	
	def __init__(self, *parameters, **options):
		TrackRequirement.__init__(self, *parameters, **options)
		
		self.handle("unitSpreadReligionAttempt", self.increment_religion_spreads)
		self.handle("cityAcquired", self.increment_religion_spreads_conquest)
		
	def increment_religion_spreads(self, goal, bSuccess):
		if bSuccess:
			self.increment()
			goal.check()
	
	def increment_religion_spreads_conquest(self, goal, city, bConquest):
		bZealotry = player(city.getOwner()).hasCivic(iZealotry2)
		if bConquest and bZealotry:
			self.increment()
			goal.check()


class FreedSlaves(TrackRequirement):

	TYPES = (COUNT,)
	
	GOAL_DESC_KEY = "TXT_KEY_VICTORY_DESC_FREE"
	DESC_KEY = "TXT_KEY_VICTORY_DESC_FREED_SLAVES"
	PROGR_KEY = "TXT_KEY_VICTORY_PROGR_FREED_SLAVES"
	
	def __init__(self, *parameters, **options):
		TrackRequirement.__init__(self, *parameters, **options)
		
		self.accumulated("freedSlaves")
