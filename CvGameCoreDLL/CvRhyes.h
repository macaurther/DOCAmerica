//Rhye
#ifndef CVRHYES_H
#define CVRHYES_H

using namespace std;
typedef list<char*> LISTCHAR;

// rhyes.h
#define EARTH_X					(59)
#define EARTH_Y					(122)

#define MAX_COM_SHRINE			(20)

// MacAurther: Not using these macros anymore because they're easy to forget about. Now, each building type is listed in DOCBuildings enum
//#define BEGIN_WONDERS				(136) // increment if normal building (not for wonders) is added
//#define BEGIN_GREAT_WONDERS			(BEGIN_WONDERS+13) // increment if a national wonder is added

#define NUM_CIVS				(31)

#define NUM_ERAS				(ERA_INDUSTRIAL+1)

#define BUILDINGCLASS_PALACE	((BuildingClassTypes)0) // MacAurther

#define UNIT_COLONIST			((UnitTypes)GC.getInfoTypeForString("UNIT_COLONIST"))								// MacAurther
#define UNIT_TIWANAKU_SISQENO	((UnitTypes)GC.getInfoTypeForString("UNIT_TIWANAKU_SISQENO"))						// MacAurther
#define UNIT_HAWAIIAN_WAA_KAULUA	((UnitTypes)GC.getInfoTypeForString("UNIT_HAWAIIAN_WAA_KAULUA"))				// MacAurther
#define UNIT_AMERICAN_AGENT		((UnitTypes)GC.getInfoTypeForString("UNIT_AMERICAN_AGENT"))							// MacAurther
#define UNIT_CANNON				((UnitTypes)GC.getInfoTypeForString("UNIT_CANNON"))									// MacAurther
#define UNIT_MIGRANT_WORKER		((UnitTypes)GC.getInfoTypeForString("UNIT_MIGRANT_WORKER"))							// MacAurther

#define UNITCLASS_EXPLORER		((UnitClassTypes)GC.getInfoTypeForString("UNITCLASS_EXPLORER"))						// MacAurther
#define UNITCLASS_RANGER		((UnitClassTypes)GC.getInfoTypeForString("UNITCLASS_RANGER"))						// MacAurther
#define UNITCLASS_NATIVE_SLAVE	((UnitClassTypes)GC.getInfoTypeForString("UNITCLASS_NATIVE_SLAVE"))					// MacAurther
#define UNITCLASS_AFRICAN_SLAVE	((UnitClassTypes)GC.getInfoTypeForString("UNITCLASS_AFRICAN_SLAVE"))				// MacAurther

#define NUM_NATIVE_TECHS		((TechTypes)FISHING + 1)															// MacAurther

#define ESPIONAGEMISSION_COUP	((EspionageMissionTypes)GC.getInfoTypeForString("ESPIONAGEMISSION_COUP"))			// MacAurther

#define BUILD_ROAD				((BuildTypes)GC.getInfoTypeForString("BUILD_ROAD"))									// MacAurther
#define BUILD_CONTACT_TRIBE		((BuildTypes)GC.getInfoTypeForString("BUILD_CONTACT_TRIBE"))						// MacAurther
#define BUILD_FORT				((BuildTypes)GC.getInfoTypeForString("BUILD_FORT"))									// MacAurther
#define BUILD_PLANTATION		((BuildTypes)GC.getInfoTypeForString("BUILD_PLANTATION"))							// MacAurther

enum DoCTechs
{
	HUNTING,
	LANDMARKS,
	IRRIGATION,
	LINGUISTICS,
	CULTIVATION,
	SPIRITUALISM,
	SHALLOW_FISHING,

	TRAPPING,
	PATHFINDING,
	EARTHWORKS,
	LOCALIZATION,
	COMPANION_PLANTING,
	HERBALISM,
	FISHING,

	TANNING,
	MINING,
	POTTERY,
	PASTORALISM,
	AGRICULTURE,
	MYTHOLOGY,
	SAILING,

	SMELTING,
	MASONRY,
	PROPERTY,
	ARITHMETICS,
	CEREMONY,
	DIVINATION,
	SEAFARING,

	ALLOYS,
	CONSTRUCTION,
	MATHEMATICS,
	ASTRONOMY,
	WRITING,
	CALENDAR,
	TRADE,

	GENERALSHIP,
	CEMENT,
	AESTHETICS,
	SCHLARSHIP,
	CODICES,
	PRIESTHOOD,
	NAVIGATION,
	
	NOBILITY,
	SUBJUGATION,
	ARTISANRY,
	MEDICINE,
	LAW,
	ETHICS,
	PHILOSOPHY,

	OLD_WORLD_TACTICS,
	OLD_WORLD_SCIENCE,
	OLD_WORLD_CULTURE,

	GUNPOWDER,
	COMPANIES,
	FINANCE,
	CARTOGRAPHY,
	HUMANITIES,
	PRINTING,
	JUDICIARY,

	FIREARMS,
	LOGISTICS,
	EXPLORATION,
	OPTICS,
	DIPLOMACY,
	EVANGELISM,
	GOVERNORS,

	FORTIFICATION,
	ECONOMICS,
	COLONIZATION,
	SHIPBUILDING,
	CHARTER,
	COMMUNITY,
	INDENTURES,

	COMBINED_ARMS,
	TRIANGULAR_TRADE,
	EXPLOITATION,
	TIMEKEEPING,
	EDUCATION,
	POLITICS,
	HORTICULTURE,

	TACTICS,
	CURRENCY,
	GEOGRAPHY,
	ACADEMIA,
	URBAN_PLANNING,
	STATECRAFT,
	SOCIAL_CONTRACT,

	REPLACEABLE_PARTS,
	FREE_MARKET,
	NEWSPAPERS,
	SCIENTIFIC_METHOD,
	ARCHITECTURE,
	SOCIOLOGY,
	HERITAGE,

	REGIMENTS,
	BONDS,
	POSTAL_SERVICE,
	METEOROLOGY,
	SURVEYING,
	REPRESENTATION,
	INDEPENDENCE,

	METALLURGY,
	PROTECTIONISM,
	HYDROLOGY,
	PHYSICS,
	GEOLOGY,
	RIGHTS_OF_MAN,
	BALANCE_OF_POWER,

	MACHINE_TOOLS,
	THERMODYNAMICS,
	ENGINEERING,
	CHEMISTRY,
	PIONEERING,
	CIVIL_LIBERTIES,
	NATIONALISM,

	MEASUREMENT,
	ENGINE,
	RAILROAD,
	ELECTRICITY,
	CONSERVATION,
	EMANCIPATION,
	IMPERIALISM,

	BALLISTICS,
	ASSEMBLY_LINE,
	COMBUSTION,
	TELEGRAPH,
	BIOLOGY,
	ORGANIZED_LABOR,
	JOURNALISM,

	INFRASTRUCTURE,
	MACROECONOMICS,
	CIVIL_RIGHTS,

	POWER_PROJECTION
};

enum DoCBuildings
{
	BUILDING_PALACE = 0,
	BUILDING_GOVERNORS_MANSION,
	BUILDING_CAPITOL,
	BUILDING_CHIEFTANS_HUT,
	BUILDING_GOVERNORS_RESIDENCE,
	BUILDING_CONTINENTAL_CONGRESS,
	BUILDING_GRANARY,
	BUILDING_COLCAS,
	BUILDING_IGLOO,
	BUILDING_MARKET,
	BUILDING_TAMBO,
	BUILDING_WEAVER,
	BUILDING_GOLDSMITH,
	BUILDING_STONEWORKS,
	BUILDING_ARENA,
	BUILDING_BALL_COURT,
	BUILDING_BARRACKS,
	BUILDING_KALLANKA,
	BUILDING_HERBALIST,
	BUILDING_PYRAMID,
	BUILDING_ALTAR,
	BUILDING_TOMB,
	BUILDING_TZOMPANTLI,
	BUILDING_YACATAS,
	BUILDING_PAGAN_TEMPLE,
	BUILDING_AQUEDUCT,
	BUILDING_CHINAMPA,
	BUILDING_BATH,
	BUILDING_TEMAZCAL,
	BUILDING_WALLS,
	BUILDING_KANCHA,
	BUILDING_PLAZA,
	BUILDING_PLATFORM_MOUND,
	BUILDING_KALASASAYA,
	BUILDING_KIVA,
	BUILDING_LONGHOUSE,
	BUILDING_HARBOR,
	BUILDING_SMOKEHOUSE,
	BUILDING_LUAU,
	BUILDING_STOCKS,
	BUILDING_TRADING_POST,
	BUILDING_HUNTING_POST,
	BUILDING_TRADING_FORT,
	BUILDING_FORGE,
	BUILDING_STABLE,
	BUILDING_PALISADE,
	BUILDING_MONUMENT,
	BUILDING_SCHOOLHOUSE,
	BUILDING_WELL,
	BUILDING_CONSTABULARY,
	BUILDING_ROYAL_MOUNTED_POLICE,
	BUILDING_SLAVE_MARKET_NATIVE,
	BUILDING_SLAVE_MARKET_COLONY,
	BUILDING_SLAVE_MARKET_NATION,
	BUILDING_WHARF,
	BUILDING_LIGHTHOUSE,
	BUILDING_WAREHOUSE,
	BUILDING_LUMBERMILL,
	BUILDING_SAWMILL,
	BUILDING_TAVERN,
	BUILDING_STAR_FORT,
	BUILDING_CITADELLE,
	BUILDING_ESTATE,
	BUILDING_FAZENDA,
	BUILDING_HACIENDA,
	BUILDING_UNIVERSITY,
	BUILDING_PHARMACY,
	BUILDING_DISTILLERY,
	BUILDING_COURTHOUSE,
	BUILDING_ASSEMBLY,
	BUILDING_THINGVELLIR,
	BUILDING_WHEELWRIGHT,
	BUILDING_POST_OFFICE,
	BUILDING_CUSTOMS_HOUSE,
	BUILDING_FEITORIA,
	BUILDING_BANK,
	BUILDING_LEVEE,
	BUILDING_SEIGNEUR,
	BUILDING_THEATRE,
	BUILDING_SILVERSMITH,
	BUILDING_MAGAZINE,
	BUILDING_SHIPYARD,
	BUILDING_OBSERVATORY,
	BUILDING_PRINTING_PRESS,
	BUILDING_MEETING_HALL,
	BUILDING_STATE_HOUSE,
	BUILDING_SLAUGHTERHOUSE,
	BUILDING_COLD_STORAGE_PLANT,
	BUILDING_SEWER,
	BUILDING_JAIL,
	BUILDING_IMMIGRATION_OFFICE,
	BUILDING_RAILWAY_STATION,
	BUILDING_TEXTILE_MILL,
	BUILDING_WOOL_MILL,
	BUILDING_STEEL_MILL,
	BUILDING_REFINERY,
	BUILDING_COAL_PLANT,
	BUILDING_RODEO,
	BUILDING_CHARREADA,
	BUILDING_ARSENAL,
	BUILDING_DRYDOCK,
	BUILDING_LIBRARY,
	BUILDING_NEWSPAPER,

	BUILDING_JEWISH_TEMPLE,
	BUILDING_JEWISH_CATHEDRAL,
	BUILDING_JEWISH_MONASTARY,
	BUILDING_JEWISH_SHRINE,
	BUILDING_ORTHODOX_TEMPLE,
	BUILDING_ORTHODOX_CATHEDRAL,
	BUILDING_ORTHODOX_MONASTERY,
	BUILDING_ORTHODOX_SHRINE,
	BUILDING_CATHOLIC_TEMPLE,
	BUILDING_CATHOLIC_CATHEDRAL,
	BUILDING_CATHOLIC_MONASTERY,
	BUILDING_MISSION,
	BUILDING_CATHOLIC_SHRINE,
	BUILDING_PROTESTANT_TEMPLE,
	BUILDING_PROTESTANT_CATHERAL,
	BUILDING_PROTESTANT_MONASTERY,
	BUILDING_PROTESTANT_SHRINE,
	BUILDING_ISLAMIC_TEMPLE,
	BUILDING_ISLAMIC_CATHERAL,
	BUILDING_ISLAMIC_MONASTERY,
	BUILDING_ISLAMIC_SHRINE,
	BUILDING_HINDU_TEMPLE,
	BUILDING_HINDU_CATHERAL,
	BUILDING_HINDU_MONASTERY,
	BUILDING_HINDU_SHRINE,
	BUILDING_BUDDHIST_TEMPLE,
	BUILDING_BUDDHIST_CATHERAL,
	BUILDING_BUDDHIST_MONASTERY,
	BUILDING_BUDDHIST_SHRINE,
	BUILDING_CONFUCIAN_TEMPLE,
	BUILDING_CONFUCIAN_CATHERAL,
	BUILDING_CONFUCIAN_MONASTERY,
	BUILDING_CONFUCIAN_SHRINE,
	BUILDING_TAOIST_TEMPLE,
	BUILDING_TAOIST_CATHERAL,
	BUILDING_TAOIST_MONASTERY,
	BUILDING_TAOIST_SHRINE,
	BUILDING_ZOROASTRIAN_TEMPLE,
	BUILDING_ZOROASTRIAN_CATHERAL,
	BUILDING_ZOROASTRIAN_MONASTERY,
	BUILDING_ZOROASTRIAN_SHRINE,

	BUILDING_ACADEMY,
	BUILDING_ADMINISTRATIVE_CENTER,
	BUILDING_MANUFACTORY,
	BUILDING_ARMOURY,
	BUILDING_MUSEUM,
	BUILDING_STOCK_EXCHANGE,

	BUILDING_TRADING_COMPANY,
	BUILDING_NATIONAL_MONUMENT,
	BUILDING_NATIONAL_THEATRE,
	BUILDING_NATIONAL_GALLERY,
	BUILDING_NATIONAL_COLLEGE,
	BUILDING_MILITARY_ACADEMY,
	BUILDING_SECRET_SERVICE,
	BUILDING_IRONWORKS,
	BUILDING_RED_CROSS,
	BUILDING_NATIONAL_PARK,
	BUILDING_CENTRAL_BANK,
	BUILDING_GRAND_CENTRAL_STATION,
	BUILDING_SUPREME_COURT,

	BUILDING_FLOATING_GARDENS,
	BUILDING_TEMPLE_OF_KUKULKAN,
	BUILDING_MACHU_PICCHU,
	BUILDING_PUEBLO_BONITO,
	BUILDING_SACSAYHUAMAN,
	BUILDING_HUEY_TEOCALLI,
	BUILDING_TLACHIHUALTEPETL,
	BUILDING_GATE_OF_THE_SUN,
	BUILDING_GREAT_GEOGLYPH,
	BUILDING_PYRAMID_OF_THE_SUN,
	BUILDING_SERPENT_MOUND,
	BUILDING_CORICANCHA,
	BUILDING_TEMBLEQUE_AQUEDUCT,
	BUILDING_LA_FORTALEZA,
	BUILDING_SAO_FRANCISCO_SQUARE,
	BUILDING_GUADALUPE_BASILICA,
	BUILDING_MANZANA_JESUITICA,
	BUILDING_INDEPENDENCE_HALL,
	BUILDING_HOSPICIO_CABANAS,
	BUILDING_MOUNT_VERNON,
	BUILDING_MONTICELLO,
	BUILDING_SLATER_MILL,
	BUILDING_CHAPULTEPEC_CASTLE,
	BUILDING_WEST_POINT,
	BUILDING_FORT_MCHENRY,
	BUILDING_WASHINGTON_MONUMENT,
	BUILDING_FANEUIL_HALL,
	BUILDING_STATUE_OF_LIBERTY,
	BUILDING_CENTRAL_PARK,
	BUILDING_ELLIS_ISLAND,
	BUILDING_BROOKLYN_BRIDGE,
	BUILDING_FRONTENAC,
	BUILDING_MENLO_PARK,
	BUILDING_BILTMORE_ESTATE,
	BUILDING_FRENCH_QUARTER,
	BUILDING_LEAGUE_OF_NATIONS,
	BUILDING_CRISTO_REDENTOR,

	BUILDING_PLAGUE
};

enum DoCEras
{
	ERA_ANCIENT,
	ERA_CLASSICAL,
	ERA_EXPLORATION,
	ERA_COLONIAL,
	ERA_REVOLUTIONARY,
	ERA_INDUSTRIAL
};

enum Regions
{
	REGION_ALASKA, // Alaska
	REGION_YUKON,	// Yukon, Northwest Territory
	REGION_NUNAVUT, // Nunavut
	REGION_GREENLAND, // Greenland
	REGION_ICELAND, // Iceland
	REGION_NORTH_CASCADIA, // British Columbia, Alberta
	REGION_NORTH_PLAINS, // Manitoba, Saskatchewan
	REGION_ONTARIO, // Ontario
	REGION_QUEBEC, // Quebec
	REGION_NEW_FOUNDLAND, // New Foundland, Labrador, New Brunswick
	REGION_SOUTH_CASCADIA, // Oregon, Washington
	REGION_CALIFORNIA, // California
	REGION_ROCKIES, // Idaho, Montana, Wyoming, Colorado, Nevada, Utah
	REGION_SOUTHWEST, //Arizona, New Mexico
	REGION_TEXAS, // Texas, Oklahoma
	REGION_GREAT_PLAINS, // N/S Dakota, Nebraska, Kansas, Iowa
	REGION_GREAT_LAKES, // Minnesota, Wisconsin, Illinois, Michigan, Indiana, Ohio
	REGION_NEW_ENGLAND, // Maine, New Hampshire, Vermont, Mass., Rhode Island, Connecticut
	REGION_MID_ATLANTIC, // New York, Pennsylvania, New Jersey
	REGION_MARYLAND, // Maryland, Delaware
	REGION_RIVER_VALLEY, // West Virginia, Kentucky, Missouri
	REGION_COASTAL_PLAIN, // Virginia, North Carolina, South Carolina, Georgia
	REGION_DEEP_SOUTH, // Louisiana, Arkansas, Alabama, Mississippi
	REGION_FLORIDA, // Florida
	REGION_BAJA_CALIFORNIA, //Baja California
	REGION_SIERRA_MADRES, // North Mexico
	REGION_BAJIO, // Central Mexico
	REGION_VERACRUZ, // Mexican Atlantic Coast
	REGION_OAXACA, // Mexican Pacific Coast
	REGION_YUCATAN, // Yucatan
	REGION_MESOAMERICA, // Central America
	REGION_CARIBBEAN, // Caribbean
	REGION_HAWAII, // Hawaii
	REGION_COLOMBIA, // Colombia, Ecuador
	REGION_VENEZUELA, // Venezuela
	REGION_GUYANA, // Guyana, Suriname, French Guyana
	REGION_PERU, // Peru
	REGION_BOLIVIA, // Bolivia
	REGION_AMAZONAS, // Upper Amazon
	REGION_PARA, // Lower Amazon
	REGION_BAHIA, // North East Brazil
	REGION_MINAS_GERAIS, // East Central Brazil
	REGION_MATO_GROSSO, // West Central Brazil
	REGION_PARANA, // South Brazil
	REGION_CHILE, // Chile
	REGION_PARAGUAY, // Paraguay
	REGION_URUGUAY, // Uruguay
	REGION_CHACO, // North Argentina
	REGION_CUYO, // West Argentina
	REGION_PAMPAS, // Central Argentina
	REGION_PATAGONIA, // South Argentina, Falklands
	REGION_OLD_WORLD,
	NUM_REGIONS
};

// MacAurther
enum RegionPowers
{
	NO_RP = -1,
	RP_ANDES,
	RP_ANGLO_AMERICA,
	RP_ARCTIC,
	RP_EUROPE,
	RP_LATIN_AMERICA,
	RP_MESOAMERICA,
	RP_MINOR,
	RP_PACIFIC,
	RP_WILDERNESS,
	NUM_REGION_POWERS
};

enum ECSArtStyles
{
	ARTSTYLE_AFRICA,
	ARTSTYLE_ANGLO_AMERICA,
	ARTSTYLE_ARABIA,
	ARTSTYLE_ASIA,
	ARTSTYLE_BARBARIAN,
	ARTSTYLE_CRESCENT,
	ARTSTYLE_EGYPT,
	ARTSTYLE_EUROPE,
	ARTSTYLE_GRECO_ROMAN,
	ARTSTYLE_INDIA,
	ARTSTYLE_IBERIA,
	ARTSTYLE_JAPAN,
	ARTSTYLE_MESO_AMERICA,
	ARTSTYLE_MONGOLIA,
	ARTSTYLE_NATIVE_AMERICA,
	ARTSTYLE_NORSE,
	ARTSTYLE_RUSSIA,
	ARTSTYLE_SOUTH_AMERICA,
	ARTSTYLE_SOUTH_EAST_ASIA,
	ARTSTYLE_SOUTH_PACIFIC,
};

#endif	// CVRHYES_H

static const int lTechLeaderPenalty[NUM_ERAS] = {0, 0, 20, 25, 30, 40};
static const int lTechBackwardsBonus[NUM_ERAS] = {0, 20, 30, 40, 50, 60};

// Leoreth: order of persecution
static const int persecutionOrder[NUM_RELIGIONS][NUM_RELIGIONS-1] = 
{
	// Judaism
	{HINDUISM, BUDDHISM, TAOISM, CONFUCIANISM, ZOROASTRIANISM, ISLAM, PROTESTANTISM, CATHOLICISM, ORTHODOXY},
	// Orthodoxy
	{ISLAM, PROTESTANTISM, CATHOLICISM, JUDAISM, ZOROASTRIANISM, HINDUISM, BUDDHISM, CONFUCIANISM, TAOISM},
	// Catholicism
	{ISLAM, PROTESTANTISM, ORTHODOXY, JUDAISM, ZOROASTRIANISM, HINDUISM, BUDDHISM, CONFUCIANISM, TAOISM},
	// Protestantism
	{ISLAM, CATHOLICISM, ORTHODOXY, JUDAISM, ZOROASTRIANISM, HINDUISM, BUDDHISM, CONFUCIANISM, TAOISM},
	// Islam
	{ZOROASTRIANISM, HINDUISM, PROTESTANTISM, CATHOLICISM, ORTHODOXY, JUDAISM, BUDDHISM, CONFUCIANISM, TAOISM},
	// Hinduism
	{ISLAM, ORTHODOXY, PROTESTANTISM, CATHOLICISM, JUDAISM, CONFUCIANISM, TAOISM, ZOROASTRIANISM, BUDDHISM},
	// Buddhism
	{ORTHODOXY, PROTESTANTISM, CATHOLICISM, JUDAISM, ZOROASTRIANISM, TAOISM, ISLAM, CONFUCIANISM, HINDUISM},
	// Confucianism
	{ISLAM, ORTHODOXY, PROTESTANTISM, CATHOLICISM, JUDAISM, ZOROASTRIANISM, HINDUISM, BUDDHISM, TAOISM},
	// Taoism
	{ISLAM, ORTHODOXY, PROTESTANTISM, CATHOLICISM, JUDAISM, ZOROASTRIANISM, HINDUISM, BUDDHISM, CONFUCIANISM},
	// Zoroastrianism
	{ISLAM, PROTESTANTISM, CATHOLICISM, ORTHODOXY, JUDAISM, HINDUISM, BUDDHISM, CONFUCIANISM, TAOISM},
};

// Leoreth: persecution priority
static const int persecutionValue[NUM_RELIGIONS][NUM_RELIGIONS] =
{
	// JUD ORT CAT PRO ISL HIN BUD CON TAO ZOR
	{  -1,  1,  1,  1,  1,  1,  1,  1,  1,  1 }, // Judaism
	{   1, -1,  3,  3,  4,  1,  1,  1,  1,  2 }, // Orthodoxy
	{   2,  2, -1,  3,  4,  1,  1,  1,  1,  2 }, // Catholicism
	{   3,  2,  3, -1,  4,  1,  1,  1,  1,  2 }, // Protestantism
	{   1,  2,  2,  2, -1,  3,  1,  1,  1,  4 }, // Islam
	{   1,  3,  3,  3,  4, -1,  0,  1,  1,  2 }, // Hinduism
	{   1,  3,  3,  3,  4,  0, -1,  1,  1,  2 }, // Buddhism
	{   1,  2,  2,  2,  3,  1,  1, -1,  0,  1 }, // Confucianism
	{   1,  2,  2,  2,  3,  1,  1,  0, -1,  1 }, // Taoism
	{   1,  3,  3,  3,  4,  1,  1,  1,  1, -1 }, // Zoroastrianism
};