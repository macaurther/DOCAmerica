from Definitions import *
from Locations import *

# second Portuguese goal: acquire 12 colonial resources by 1650 AD
lColonialResources = [iBanana, iSpices, iSugar, iCoffee, iTea, iTobacco]


# city names
BUENOS_AIRES = "TXT_KEY_VICTORY_NAME_BUENOS_AIRES"
MEXICO_CITY = "TXT_KEY_VICTORY_NAME_MEXICO_CITY"
TENOCHTITLAN = "TXT_KEY_VICTORY_NAME_TENOCHTITLAN"
CAHOKIA = "TXT_KEY_VICTORY_NAME_CAHOKIA"
NEW_AMSTERDAM = "TXT_KEY_VICTORY_NAME_NEW_AMSTERDAM"
HILO = "TXT_KEY_VICTORY_NAME_HILO"

# city descriptors
CAPITAL = "TXT_KEY_VICTORY_NAME_CAPITAL"
DIFFERENT_CAPITAL = "TXT_KEY_VICTORY_NAME_DIFFERENT_CAPITAL"
ANOTHER_CAPITAL = "TXT_KEY_VICTORY_NAME_ANOTHER_CAPITAL"
ITS_CITY = "TXT_KEY_VICTORY_NAME_ITS_CITY"

# area names
ATLANTIC_COAST = "TXT_KEY_VICTORY_NAME_ATLANTIC_COAST"
AMERICA = "TXT_KEY_VICTORY_NAME_AMERICA"
BRAZIL = "TXT_KEY_VICTORY_NAME_BRAZIL"
CARIBBEAN = "TXT_KEY_VICTORY_NAME_CARIBBEAN"
EASTER_ISLAND = "TXT_KEY_VICTORY_NAME_EASTER_ISLAND"
GRAN_COLOMBIA = "TXT_KEY_VICTORY_NAME_GRAN_COLOMBIA"
GUAYANAS = "TXT_KEY_VICTORY_NAME_GUAYANAS"
HAWAII = "TXT_KEY_VICTORY_NAME_HAWAII"
NORTH_AMERICA = "TXT_KEY_VICTORY_NAME_NORTH_AMERICA"
NORTH_CENTRAL_AMERICA = "TXT_KEY_VICTORY_NAME_NORTH_CENTRAL_AMERICA"
NORTH_WEST_INDIA = "TXT_KEY_VICTORY_NAME_NORTH_WEST_INDIA"
PACIFIC_COAST = "TXT_KEY_VICTORY_NAME_PACIFIC_COAST"
PERU = "TXT_KEY_VICTORY_NAME_PERU"
SOUTH_AMERICA = "TXT_KEY_VICTORY_NAME_SOUTH_AMERICA"
SOUTH_CENTRAL_AMERICA = "TXT_KEY_VICTORY_NAME_SOUTH_CENTRAL_AMERICA"
MESOAMERICA = "TXT_KEY_VICTORY_NAME_MESOAMERICA"
YUCATAN = "TXT_KEY_VICTORY_NAME_YUCATAN"
BAJIO = "TXT_KEY_VICTORY_NAME_BAJIO"
MISSISSIPPI_RIVER = "TXT_KEY_VICTORY_NAME_MISSISSIPPI_RIVER"
OHIO_RIVER = "TXT_KEY_VICTORY_NAME_OHIO_RIVER"

# area descriptors
ANDEAN_COAST = "TXT_KEY_VICTORY_NAME_ANDEAN_COAST"
CANADIAN_TERRITORY = "TXT_KEY_VICTORY_NAME_CANADIAN_TERRITORY"
CITIES_IN_CANADA = "TXT_KEY_VICTORY_NAME_CITIES_IN_CANADA"
COLONIAL = "TXT_KEY_VICTORY_NAME_COLONIAL"

# building descriptors
SHRINES = "TXT_KEY_VICTORY_NAME_SHRINES"
TEMPLES = "TXT_KEY_VICTORY_NAME_TEMPLES"
CHRISTIAN_CATHEDRALS = "TXT_KEY_VICTORY_NAME_CHRISTIAN_CATHEDRALS"
STATE_RELIGION_CATHEDRAL = "TXT_KEY_VICTORY_NAME_STATE_RELIGION_CATHEDRAL"

# resource descriptors
DIFFERENT_HAPPINESS_RESOURCES = "TXT_KEY_VICTORY_NAME_DIFFERENT_HAPPINESS_RESOURCES"
TRADING_COMPANY_RESOURCES = "TXT_KEY_VICTORY_NAME_TRADING_COMPANY_RESOURCES"

# routes descriptors
LAND_BASED_TRADE = "TXT_KEY_VICTORY_NAME_LAND_BASED_TRADE"

# civilization descriptors
ALL_EUROPEAN = "TXT_KEY_VICTORY_NAME_ALL_EUROPEAN"
EUROPEAN = "TXT_KEY_VICTORY_NAME_EUROPEAN"
EUROPEAN_CIVILIZATION = "TXT_KEY_VICTORY_NAME_EUROPEAN_CIVILIZATION"
LOCAL = "TXT_KEY_VICTORY_NAME_LOCAL"

# goal descriptors


dGoals = {
	iMaya: (
		FirstDiscover(iMathematics, iCalendar),
		Wonder(iTempleOfKukulkan, by=900),
		ContactBeforeRevealed(group(iCivGroupEurope).named(EUROPEAN_CIVILIZATION), plots.regions(*lAmerica).named(AMERICA)),
	),
	iTeotihuacan: (
		CultureAmount(500, at=550),
		GoldenAges(1, by=550),
		Control(
			plots.region(rBajio).named(BAJIO),
			plots.region(rYucatan).named(YUCATAN),
			at=1000,
		),
	),
	iTiwanaku: (
		All(
			CitySpecialistCount(capital().named(CAPITAL), iSpecialistGreatProphet, 1),
			Wonder(iGateOfTheSun),
			by=900,
		),
		CultureLevelCityCount(iCultureLevelRefined, 2, by=1000),
		GoldenAges(2, by=1100),
	),
	iWari: (
		All(
			ResourceCount((iGold, 1), (iDye, 1), (iCotton, 1), (iLlama, 1)),
			CultureAmount(500),
			by=900,
		),
		BuildingCount((iBarracks, 5), (iColcas, 5), (iMarket, 3), (iCommon, 2), by=1000),
		All(
			CultureLevelCityCount(iCultureLevelDeveloping, 4),
			PopulationCityCount(5, 4),
			by=1100,
		),
	),
	iMississippi: (
		All(
			Control((plots.rectangle(tMississippiRiver).without(lMississippiRiverExceptions) + plots.of(lMississippiRiverAdditional)).named(MISSISSIPPI_RIVER)),
			Control((plots.rectangle(tOhioRiver).without(lOhioRiverExceptions)).named(OHIO_RIVER)),
			by=1000,
		),
		All(
			BuildingCount(iEffigyMound, 5),
			Wonder(iSerpentMound),
			by=1070,
		),
		All(
			CityBuilding(city(tCahokia).named(CAHOKIA), iPalace),
			CitySpecialistCount(city(tCahokia).named(CAHOKIA), iSpecialistGreatMerchant, 2),
			by=1400,
		),
	),
	iPuebloan: (
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
	),
	iMuisca: (
		AveragePopulation(10, at=1500),
		TradeGold(2000, by=1540),
		GoldAmount(999999, by=2000),
	),
	iNorse: (
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
	),
	iChimu: (
		BuildingCount((iKancha, 2), by=1300),
		Control(plots.normal(iInca), subject=VASSALS, at=1475),
		CitySpecialistCount(capital().named(CAPITAL), iSpecialistGreatArtist, 3, by=1500),
	),
	iInuit: (
		GoldAmount(999999, by=2000),
		ResourceCount(resources(), 25),
		GoldAmount(999999, by=2000),
	),
	iInca: (
		All(
			BuildingCount(iTambo, 5),
			Route(plots.of(lAndeanCoast).named(ANDEAN_COAST), [iRouteRoad]),
			by=1550,
		),
		GoldAmount(2500, by=1550),
		AreaPopulationPercent(plots.regions(*lSouthAmerica).named(SOUTH_AMERICA), 90, by=1775),
	),
	iAztecs: (
		BestPopulationCity(start(iAztecs).named(TENOCHTITLAN), at=1520),
		BuildingCount((iPaganTemple, 6), (iTzompantli, 6), by=1650),
		EnslaveCount(20, excluding=group(iCivGroupAmerica).named(EUROPEAN)),
	),
	iIroquois: (
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
	),
	iSpain: (
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
		All(
			ControlledResourceCount(sum(iSilver, iGold), 15),
			LandPercent(50),
			by=1790,
		)
	),
	iPortugal: (
		OpenBorderCount(14, by=1550),
		ResourceCount(sum(lColonialResources).named(TRADING_COMPANY_RESOURCES), 20, by=1650),
		CityCount(sum(
			plots.regions(*lBrazil).named(BRAZIL),
		), 15, by=1700),
	),
	iEngland: (
		CityCount(
			(plots.regions(*lNorthAmerica).named(NORTH_AMERICA), 10),
			(plots.regions(*(lSouthAmerica + lCentralAmerica)).named(SOUTH_CENTRAL_AMERICA), 5),
			by=1730,
		),
		All(
			UnitCount(sum(iFrigate, iShipOfTheLine), 25),
			SunkShips(50),
			by=1800,
		),
		EraFirstDiscover((iRevolutionary, 8), (iIndustrial, 8)),
	),
	iFrance: (
		ControlledResourceCount(iFur, 15, by=1650),
		AreaPercent(plots.regions(lNorthAmerica).named(NORTH_AMERICA), 50, subject=VASSALS, at=1800),
		UnitCount(iSatellite, 1, by=1968),
	),
	iNetherlands: (
		CitySpecialistCount(city(tNewAmsterdam).named(NEW_AMSTERDAM), iSpecialistGreatMerchant, 1, at=1664),
		ResourceCount(iSpices, 7, by=1775),
		GoldAmount(1, by=2000),
	),
	iHawaii: (
		UnitCount(iCannon, 1, by=1790),
		Control(plots.regions(rHawaii).named(HAWAII), at=1810),
		All(
			CitySpecialistCount(start(iHawaii).named(HILO), iSpecialistGreatArtist, 1),
			CitySpecialistCount(start(iHawaii).named(HILO), iSpecialistGreatMerchant, 1),
			CitySpecialistCount(start(iHawaii).named(HILO), iSpecialistGreatGeneral, 1),
			at=1890,
		)
	),
	iRussia: (
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
	),
	iAmerica: (
		BuildingCount(iStateHouse, 50, by=1959),
		BuildingCount(wonders(), 15, by=1975),
		All(
			CommercePercent(95, subject=ALLIES),
			PowerPercent(95, subject=ALLIES),
			by=1990,
		),
	),
	iHaiti: (
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
	),
	iBolivia: (
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
	),
	iArgentina: (
		GoldenAges(2, by=1930),
		CityCultureLevel(start(iArgentina).named(BUENOS_AIRES), iCultureLevelLegendary, by=1960),
		GoldenAges(6, by=2000),
	),
	iMexico: (
		BuildingCount(state_religion_building(cathedral).named(STATE_RELIGION_CATHEDRAL), 3, by=1880),
		GreatGenerals(3, by=1940),
		BestPopulationCity(start(iMexico).named(MEXICO_CITY), at=1960),
	),
	iColombia: (
		AllowNone(
			group(iCivGroupEurope).named(EUROPEAN),
			plots.rectangle(tPeru).named(PERU),
			plots.rectangle(tGranColombia).named(GRAN_COLOMBIA),
			plots.rectangle(tGuayanas).named(GUAYANAS),
			plots.rectangle(tCaribbean).named(CARIBBEAN),
			at=1870,
		),
		Control(
			plots.rectangle(tSouthAmerica).without(lSouthAmericaExceptions).named(SOUTH_AMERICA),
			at=1920,
		),
		ResourceTradeGold(3000, by=1950),
	),
	iChile: (
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
	),
	iPeru: (
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
	),
	iBrazil: (
		ImprovementCount((iSlavePlantation, 8), (iPasture, 4), at=1880),
		Wonders(iCristoRedentor, iItaipuDam),
		All(
			ImprovementCount(iForestPreserve, 20),
			CityBuilding(capital().named(CAPITAL), iNationalPark),
			by=1950,
		),
	),
	iVenezuela: (
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
	),
	iCanada: (
		All(
			RouteConnection([iRouteRailroad], capital().named(CAPITAL), plots.of(lAtlanticCoast).named(ATLANTIC_COAST)),
			RouteConnection([iRouteRailroad], capital().named(CAPITAL), plots.of(lPacificCoast).named(PACIFIC_COAST)),
			by=1920,
		),
		All(
			Control((plots.rectangle(tCanadaWest).without(lCanadaWestExceptions) + plots.rectangle(tCanadaEast).without(lCanadaEastExceptions)).named(CITIES_IN_CANADA)),
			AreaPercent((plots.rectangle(tCanadaWest).without(lCanadaWestExceptions) + plots.rectangle(tCanadaEast).without(lCanadaEastExceptions)).named(CANADIAN_TERRITORY), 90),
			NoCityConquered(),
			by=1950,
		),
		BrokeredPeace(12, by=2000),
	),
	iCuba: (
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
		GoldAmount(999999, by=2000),
	),
}


for iCiv, goals in dGoals.items():
	for index, goal in enumerate(goals):
		title_key = "TXT_KEY_VICTORY_TITLE_%s%s" % (infos.civ(iCiv).getIdentifier(), index+1)
		goal.options["title_key"] = title_key


def descriptions(iCiv):
	for goal in dGoals[iCiv]:
		print goal.description()