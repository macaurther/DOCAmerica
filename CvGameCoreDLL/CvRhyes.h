//Rhye
#ifndef CVRHYES_H
#define CVRHYES_H

using namespace std;
typedef list<char*> LISTCHAR;

// rhyes.h
#define EARTH_X					(80)
#define EARTH_Y					(108)

#define MAX_COM_SHRINE			(20)

#define BEGIN_WONDERS				(132) // increment if normal building (not for wonders) is added
#define BEGIN_GREAT_WONDERS			(BEGIN_WONDERS+13) // increment if a national wonder is added

#define NUM_CIVS				(17)

#define NUM_ERAS				(ERA_ATOMIC+1)

#define PAGAN_TEMPLE			((BuildingTypes)GC.getInfoTypeForString("BUILDING_PAGAN_TEMPLE"))
#define BUILDING_PALACE			((BuildingClassTypes)0)
#define BUILDING_PLAGUE			((BuildingTypes)GC.getInfoTypeForString("BUILDING_PLAGUE"))

#define UNITCLASS_SLAVE			((UnitClassTypes)GC.getInfoTypeForString("UNITCLASS_SLAVE"))

enum DoCTechs
{
	TANNING,
	MINING,
	POTTERY,
	PASTORALISM,
	AGRICULTURE,
	MYTHOLOGY,
	SAILING,

	ARTISNARY,
	MASONRY,
	MATHEMATICS,
	PROPERTY,
	CEREMONY,
	PRIESTHOOD,
	NAVIGATION,

	SMELTING,
	CONSTRUCTION,
	AESTHETICS,
	CALENDAR,
	WRITING,
	LAW,
	MEDICINE,

	OLD_WORLD_KNOWLEDGE,

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
	HYDRAULICS,
	PHYSICS,
	GEOLOGY,
	RIGHTS_OF_MAN,
	FEDERALISM,

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
	LABOR_UNIONS,
	JOURNALISM,

	PNEUMATICS,
	FLIGHT,
	REFINING,
	FILM,
	REFRIGERATION,
	CONSUMERISM,
	CIVIL_RIGHTS,

	INFRASTRUCTURE,
	AERONAUTICS,
	SYNTHETICS,
	RADIO,
	MICROBIOLOGY,
	MACROECONOMICS,
	SOCIAL_SERVICES,

	AVIATION,
	ROCKETRY,
	FISSION,
	ELECTRONICS,
	PSYCHOLOGY,
	POWER_PROJECTION,
	GLOBALISM,

	RADAR,
	SPACEFLIGHT,
	NUCLEAR_POWER,
	LASER,
	TELEVISION,
	TOURISM,
	ECOLOGY,

	AERODYNAMICS,
	SATELLITES,
	SUPERCONDUCTORS,
	TELECOMMUNICATIONS,
	COMPUTERS,
	RENEWABLE_ENERGY,
	GENETICS,

	SUPERMATERIALS,
	FUSION,
	NANTECHNOLOGY,
	ROBOTICS,
	AUTOMATION,

	UNIFIED_THEORY,
	ARTIFICIAL_INTELLIGENCE,
	BIOTECHNOLOGY,

	TRANSHUMANISM,
};

enum DoCBuildings
{
	TRADING_COMPANY = BEGIN_WONDERS,
	IBERIAN_TRADING_COMPANY, 
	NATIONAL_MONUMENT, 
	NATIONAL_THEATRE, 
	NATIONAL_GALLERY, 
	NATIONAL_COLLEGE, 
	MILITARY_ACADEMY,
	SECRET_SERVICE, 
	IRONWORKS, 
	RED_CROSS, 

	NATIONAL_PARK, 
	CENTRAL_BANK, 
	SPACEPORT,
	TEMPLE_OF_KUKULKAN, 
	MACHU_PICCHU, 
	FLOATING_GARDENS, 
	GUADALUPE_BASILICA, 
	SALT_CATHEDRAL, 
	STATUE_OF_LIBERTY, 
	CHAPULTEPEC_CASTLE,

	MENLO_PARK, 
	BROOKLYN_BRIDGE, 
	HOLLYWOOD, 
	EMPIRE_STATE_BUILDING,
	LAS_LAJAS_SANCTUARY, 
	FRONTENAC,
	CRISTO_REDENTOR, 
	GOLDEN_GATE_BRIDGE, 
	BLETCHLEY_PARK, 
	ITAIPU_DAM, 

	GRACELAND, 
	CN_TOWER, 
	PENTAGON, 
	UNITED_NATIONS, 
	CRYSTAL_CATHEDRAL, 
	WORLD_TRADE_CENTER, 
	HUBBLE_SPACE_TELESCOPE,
	SPACE_ELEVATOR
};

enum DoCEras
{
	ERA_PRECOLUMBIAN,
	ERA_EXPLORATION,
	ERA_COLONIAL,
	ERA_REVOLUTIONARY,
	ERA_INDUSTRIAL,
	ERA_MODERN,
	ERA_ATOMIC,
	ERA_NATIVE_AMERICA
};

enum Regions
{
	REGION_ALASKA,
	REGION_NUNAVUT,
	REGION_NORTH_PLAINS,
	REGION_ONTARIO,
	REGION_QUEBEC,
	REGION_NEW_FOUNDLAND,
	REGION_NEW_ENGLAND,
	REGION_MID_ATLANTIC,
	REGION_DEEP_SOUTH,
	REGION_GULF_COAST,
	REGION_MIDWEST,
	REGION_SOUTHWEST,
	REGION_GREAT_PLAINS,
	REGION_ROCKIES,
	REGION_CALIFORNIA,
	REGION_CASCADIA,
	REGION_SIERRA_MADRE,
	REGION_BAJIO,
	REGION_YUCATAN,
	REGION_MESOAMERICA,
	REGION_CARIBBEAN,
	REGION_HAWAII,
	REGION_COLOMBIA,
	REGION_VENEZUELA,
	REGION_GUYANA,
	REGION_PERU,
	REGION_BOLIVIA,
	REGION_AMAZON,
	REGION_BRAZILIAN_HIGHLANDS,
	REGION_PANTANAL,
	REGION_CHILE,
	REGION_PARAGUAY,
	REGION_URUGUAY,
	REGION_PAMPAS,
	REGION_PATAGONIA,
	NUM_REGIONS
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

static const int lTechLeaderPenalty[NUM_ERAS] = {0, 0, 20, 25, 30, 40, 50};
static const int lTechBackwardsBonus[NUM_ERAS] = {0, 20, 30, 40, 50, 60, 75};

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