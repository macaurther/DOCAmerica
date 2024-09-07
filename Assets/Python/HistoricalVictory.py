from Definitions import *
from Locations import *

# second Portuguese goal: acquire 20 plantation resources by 1650 AD
#lColonialResources = [iBanana, iSpices, iSugar, iCoffee, iTea, iTobacco, iCocoa, iSalt, iCitrus]
lPlantationResources = [iBanana, iCocoa, iCoffee, iCotton, iDye, iIncense, iRubber, iSilk, iSpices, iSugar, iTea, iTobacco]


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
GREENLAND = "TXT_KEY_VICTORY_NAME_GREENLAND"
VINLAND = "TXT_KEY_VICTORY_NAME_VINLAND"
DELAWARE = "TXT_KEY_VICTORY_NAME_DELAWARE"
GREAT_LAKES = "TXT_KEY_VICTORY_NAME_GREAT_LAKES"
LAKE_SUPERIOR = "TXT_KEY_VICTORY_NAME_LAKE_SUPERIOR"
LAKE_MICHIGAN = "TXT_KEY_VICTORY_NAME_LAKE_MICHIGAN"
LAKE_HURON = "TXT_KEY_VICTORY_NAME_LAKE_HURON"
LAKE_ERIE = "TXT_KEY_VICTORY_NAME_LAKE_ERIE"
LAKE_ONTARIO = "TXT_KEY_VICTORY_NAME_LAKE_ONTARIO"
KIVALLIQ =  "TXT_KEY_VICTORY_NAME_KIVALLIQ"
QIKIQTAALUK =  "TXT_KEY_VICTORY_NAME_QIKIQTAALUK"
NUNAVIK =  "TXT_KEY_VICTORY_NAME_NUNAVIK"
KALAALLIT =  "TXT_KEY_VICTORY_NAME_KALAALLIT"
MID_ATLANTIC =  "TXT_KEY_VICTORY_NAME_MID_ATLANTIC"
VENEZUELA =  "TXT_KEY_VICTORY_NAME_VENEZUELA"
BAHIA =  "TXT_KEY_VICTORY_NAME_BAHIA"
ALASKA = "TXT_KEY_VICTORY_NAME_ALASKA"
NATO = "TXT_KEY_VICTORY_NAME_NATO"
GREAT_PLAINS = "TXT_KEY_VICTORY_NAME_GREAT_PLAINS"
ANDES = "TXT_KEY_VICTORY_NAME_ANDES"

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
PLANTATION_RESOURCES = "TXT_KEY_VICTORY_NAME_PLANTATION_RESOURCES"

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
		Wonder(iTempleOfKukulkan, by=800),
		BestTechPlayer(at=1490),
	),
	iZapotec: (
		FirstDiscover(iWriting),
		All(
			ControlledResourceCount(iJade, 1),
			ControlledResourceCount(iObsidian, 1),
			ControlledResourceCount(iGold, 1),
			ControlledResourceCount(iSilver, 1),
			by=1000
		),
		All(
			CitySpecialistCount(capital().named(CAPITAL), iSpecialistGreatProphet, 1),
			CitySpecialistCount(capital().named(CAPITAL), iSpecialistGreatGeneral, 1),
			CitySpecialistCount(capital().named(CAPITAL), iSpecialistGreatArtist, 1),
			CitySpecialistCount(capital().named(CAPITAL), iSpecialistGreatScientist, 1),
			by=1500,
		),
	),
	iTeotihuacan: (
		BuildingCount(wonders(), 1, by=500),
		GoldenAges(1, by=850),
		Control(
			plots.region(rBajio).named(BAJIO),
			plots.region(rYucatan).named(YUCATAN),
			at=1000,
		),
	),
	iTiwanaku: (
		CitySpecialistCount(capital().named(CAPITAL), iSpecialistGreatProphet, 1, by=700),
		All(
			Wonder(iKalasasaya),
			Wonder(iGateOfTheSun),
			Wonder(iPyramidOfTheSun),
			by=900,
		),
		GoldenAges(4, by=1100),
	),
	iWari: (
		All(
			ResourceCount((iGold, 1), (iDye, 1), (iCotton, 1), (iLlama, 1)),
			CultureAmount(250),
			by=900,
		),
		BuildingCount((iBarracks, 2), (iColcas, 4), (iMarket, 2), by=1000),
		All(
			CultureLevelCityCount(iCultureLevelDeveloping, 4),
			PopulationCityCount(5, 4),
			by=1100,
		),
	),
	iMississippi: (
		TerrainCount(iWideRiver, 20, by=1000),
		All(
			BuildingCount(iPlatformMound, 5),
			Wonder(iSerpentMound),
			by=1200,
		),
		All(
			CityBuilding(city(tCahokia).named(CAHOKIA), iPalace),
			CitySpecialistCount(city(tCahokia).named(CAHOKIA), iSpecialistGreatMerchant, 2),
			by=1400,
		),
	),
	iPuebloan: (
		All(
			CultureAmount(500, at=1200),
			BuildingCount(iKiva, 5),
			by=1200,
		),
		All(
			TradeConnection(),
			SpecialistCount(iSpecialistGreatMerchant, 4),
			by=1400,
		),
		UnitCount(iHorseArcher, 1, by=1680),
	),
	iMuisca: (
		ControlledResourceCount(iGold, 3, at=1150),
		AveragePopulation(10, at=1300),
		GoldAmount(2000, by=1450),
	),
	iNorse: (
		FirstSettle(plots.region(rGreenland).named(GREENLAND), by=1000),
		FirstSettle(plots.rectangle(tVinland).named(VINLAND), by=1100),
		All(
			ImprovementCount(iLumbermill, 10),
			Control(plots.rectangle(tDelaware).named(DELAWARE)),
			by=1640,
		),
	),
	iChimu: (
		BuildingCount((iKancha, 3), by=1100),
		Control(plots.region(rPeru).named(PERU), subject=VASSALS, at=1400),
		CitySpecialistCount(capital().named(CAPITAL), iSpecialistGreatArtist, 3, by=1500),
	),
	iInuit: (
		CityCount(
			(plots.rectangle(tKivalliq).named(KIVALLIQ), 1),										# Western Hudson Bay
			(plots.rectangle(tQikiqtaaluk).without(lQikiqtaalukExceptions).named(QIKIQTAALUK), 1),	# Baffin Island and islands
			(plots.rectangle(tNunavik).named(NUNAVIK), 1),											# Northern Quebec/ Eastern Hudson Bay
			(plots.region(rGreenland).named(KALAALLIT), 1),										# Greenland
			by=1500
		),
		ResourceCount(resources(), 22, by=1600),
		TerrainCount(sum(iOcean, iCoast, iArcticCoast, iFjord), 100, by=1700),
	),
	iInca: (
		All(
			TradeRouteCount(45),
			Wonders(iSacsayhuaman, iMachuPicchu),
			by=1400,
		),
		GoldAmount(2500, by=1500),
		AreaPopulationPercent(plots.regions(*lAndes).named(ANDES), 100, at=1550),
	),
	iPurepecha: (
		ControlledResourceCount(iFish, 2, by=1300),
		All(
			UnitLevelCount(3, 10),
			UnitCount(sum(iMacana, iArcher), 25),
			by=1500,
		),
		All(
			NoCityLost(),
			Control(plots.region(rBajio).named(BAJIO)),
			at=1600,
		)
	),
	iAztecs: (
		All(VassalCount(1), Control(plots.region(rBajio).named(BAJIO), subject=VASSALS), by=1450),
		CityPopulation(start(iAztecs).named(TENOCHTITLAN), 20, at=1500),
		EnslaveCount(50, by=1550),
	),
	iHaudenosaunee: (
		All(ContactTribe(5), by=1550),
		Control(
            (plots.rectangle(tLakeSuperior).without(lLakeSuperiorExceptions) + plots.of(lLakeSuperiorAdditional)).named(LAKE_SUPERIOR),
            (plots.rectangle(tLakeMichigan).without(lLakeSuperiorExceptions) + plots.of(lLakeMichiganAdditional)).named(LAKE_MICHIGAN),
            (plots.rectangle(tLakeHuron).without(lLakeHuronExceptions) + plots.of(lLakeHuronAdditional)).named(LAKE_HURON),
            (plots.rectangle(tLakeErie) + plots.of(lLakeErieAdditional)).named(LAKE_ERIE),
            (plots.rectangle(tLakeOntario).without(lLakeOntarioExceptions) + plots.of(lLakeOntarioAdditional)).named(LAKE_ONTARIO),
			at=1650),
		ControlledResourceCount(iFur, 10, by=1700),
	),
	iLakota: (
		Migrations(30, by=1700),
		AverageCultureAmount(500, by=1750),
		AllowNone(group(iCivGroupAmerica).named(EUROPEAN), plots.regions([rNorthPlains, rGreatPlains]).named(GREAT_PLAINS), at=1890),
	),
	iSpain: (
		RaidGold(3000, by=1600),
		All(
			ContactTribe(25),
			ReligionSpreads(50),
			by=1700
		),
		All(
			ControlledResourceCount(sum(iSilver, iGold), 15),
			LandPercent(50),
			by=1790,
		)
	),
	iPortugal: (
		ResourceCount(sum(lPlantationResources).named(PLANTATION_RESOURCES), 30, by=1650),
		CityCount(sum(
			plots.regions(*lBrazil).named(BRAZIL),
		), 15, by=1700),
		SpecialistCount(iSpecialistSlavePlanter, 40, by=1800),
	),
	iEngland: (
		CityCount(
			(plots.regions(*lNorthAmerica).named(NORTH_AMERICA), 10),
			(plots.regions(*(lSouthAmerica + lCentralAmerica)).named(SOUTH_CENTRAL_AMERICA), 5),
			by=1730,
		),
		PopulationCount(100, by=1760),
		All(
			UnitCount(sum(iFrigate, iShipOfTheLine), 25),
			SunkShips(50),
			by=1800,
		),
	),
	iFrance: (
		ControlledResourceCount(iFur, 15, by=1750),
		ImprovementCount(iContactedTribe, 20, by=1775),
		TerrainCount(iWideRiver, 40, by=1800),
	),
	iNetherlands: (
		CitySpecialistCount(city(tNewAmsterdam).named(NEW_AMSTERDAM), iSpecialistGreatMerchant, 1, at=1660),
		CityCount(
			(plots.regions(rMidAtlantic).named(MID_ATLANTIC), 1),
			(plots.regions(rCaribbean).named(CARIBBEAN), 1),
			(plots.regions(rVenezuela).named(VENEZUELA), 1),
			(plots.regions(rGuyana).named(GUAYANAS), 1),
			(plots.regions(rBahia).named(BAHIA), 1),
			by=1700,
		),
		TradeGold(5000, by=1800),
	),
	iHawaii: (
		UnitCount(iCannon, 1, by=1790),
		AreaPercent(plots.regions(rHawaii).named(HAWAII), 100, by=1810),
		All(
			CitySpecialistCount(start(iHawaii).named(HILO), iSpecialistGreatArtist, 1),
			CitySpecialistCount(start(iHawaii).named(HILO), iSpecialistGreatMerchant, 1),
			CitySpecialistCount(start(iHawaii).named(HILO), iSpecialistGreatGeneral, 1),
			at=1890,
		)
	),
	iRussia: (
		ImprovementCount(iCamp, 10, by=1800),
		AreaPercent(plots.region(rAlaska).named(ALASKA), 90, subject=VASSALS, at=1860),
		TradeGold(1000, by=1870),
	),
	iAmerica: (
		AllowNone(
			group(iCivGroupEurope).named(EUROPEAN),
			plots.regions(*lAmerica).named(AMERICA),
			at=1900,
		),
		All(
			ImmigrationSpent(10000),
			BuildingCount(wonders(), 10),
			by=1920
		),
		All(
			FreedSlaves(50),
			BuildingCount(iStateHouse, 50),
			by=1950
		)
	),
	iHaiti: (
		FirstDiscover(iEmancipation),
		FreedSlaves(20),
		Control(plots.region(rCaribbean).named(CARIBBEAN), at=1890),
	),
	iArgentina: (
		GoldenAges(2, by=1880),
		CityCultureLevel(start(iArgentina).named(BUENOS_AIRES), iCultureLevelLegendary, by=1900),
		GoldenAges(6, by=1950),
	),
	iMexico: (
		BuildingCount(state_religion_building(cathedral).named(STATE_RELIGION_CATHEDRAL), 3, by=1880),
		GreatGenerals(3, by=1900),
		BestPopulationCity(start(iMexico).named(MEXICO_CITY), at=1950),
	),
	iColombia: (
		AllowNone(
			group(iCivGroupEurope).named(EUROPEAN),
			plots.region(rPeru).named(PERU),
			plots.regions(*(rColombia, rVenezuela)).named(GRAN_COLOMBIA),
			plots.region(rGuyana).named(GUAYANAS),
			plots.region(rCaribbean).named(CARIBBEAN),
			at=1870,
		),
		Control(plots.regions(*lSouthAmerica).named(SOUTH_AMERICA), at=1900),
		ResourceTradeGold(3000, by=1900),
	),
	iPeru: (
		Control(plots.region(rPeru).named(PERU), at=1850),
		GoldAmount(5000, by=1866),
		PopulationCityCount(15, 1, by=1900),
	),
	iBrazil: (
		All(
			AreaPercent(plots.regions(*lBrazil).named(BRAZIL), 90, subject=VASSALS),
			FreedSlaves(50),
			by=1880
		),
		Wonders(iCristoRedentor, by=1931),
		All(
			ImprovementCount(iForestPreserve, 20),
			CityBuilding(capital().named(CAPITAL), iNationalPark),
			by=1950,
		),
	),
	iVenezuela: (
		BuildingCount(iCatholicCathedral, 1, by=1860),
		GreatGenerals(2, by=1900),
		ControlledResourceCount(iOil, 5, by=1950),
	),
	iCanada: (
		All(
			RouteConnection([iRouteRailroad], capital().named(CAPITAL), plots.all().coastal().regions(*lCanadaAtlanticCoast).named(ATLANTIC_COAST)),
			RouteConnection([iRouteRailroad], capital().named(CAPITAL), plots.all().coastal().regions(*lCanadaPacificCoast).named(PACIFIC_COAST)),
			by=1920,
		),
		All(
			Control((plots.regions(*lCanada)).named(CITIES_IN_CANADA)),
			AreaPercent((plots.regions(*lCanada)).named(CANADIAN_TERRITORY), 90),
			by=1920,
		),
		HappiestTurns(25, by=1950),
	),
}


for iCiv, goals in dGoals.items():
	for index, goal in enumerate(goals):
		title_key = "TXT_KEY_VICTORY_TITLE_%s%s" % (infos.civ(iCiv).getIdentifier(), index+1)
		goal.options["title_key"] = title_key


def descriptions(iCiv):
	for goal in dGoals[iCiv]:
		print goal.description()