//Rhye
#ifndef CVRHYES_H
#define CVRHYES_H

using namespace std;
typedef list<char*> LISTCHAR;

// rhyes.h
#define EARTH_X					(83)
#define EARTH_Y					(122)

#define MAX_COM_SHRINE			(20)

// MacAurther: Not using these macros anymore because they're easy to forget about. Now, each building type is listed in DOCBuildings enum
//#define BEGIN_WONDERS				(136) // increment if normal building (not for wonders) is added
//#define BEGIN_GREAT_WONDERS			(BEGIN_WONDERS+13) // increment if a national wonder is added

#define NUM_CIVS				  (32)
#define NUM_MINORS				  (4)

#define NUM_ERAS				  (ERA_MODERN+1)

#define BUILDINGCLASS_PALACE	  ((BuildingClassTypes)GC.getInfoTypeForString("BUILDINGCLASS_PALACE"))				// MacAurther

#define UNIT_IMMIGRANT			  ((UnitTypes)GC.getInfoTypeForString("UNIT_IMMIGRANT"))								// MacAurther
#define UNIT_TIWANAKU_SISQENO	  ((UnitTypes)GC.getInfoTypeForString("UNIT_TIWANAKU_SISQENO"))						// MacAurther
#define UNIT_HAWAIIAN_WAA_KAULUA  ((UnitTypes)GC.getInfoTypeForString("UNIT_HAWAIIAN_WAA_KAULUA"))					// MacAurther
#define UNIT_AMERICAN_AGENT		  ((UnitTypes)GC.getInfoTypeForString("UNIT_AMERICAN_AGENT"))						// MacAurther
#define UNIT_CANNON				  ((UnitTypes)GC.getInfoTypeForString("UNIT_CANNON"))								// MacAurther
#define UNIT_CANOE				  ((UnitTypes)GC.getInfoTypeForString("UNIT_CANOE"))								// MacAurther
#define UNIT_TRACKMAN		  ((UnitTypes)GC.getInfoTypeForString("UNIT_TRACKMAN"))						// MacAurther
#define UNIT_NATIVE_SLAVE_COLONY  ((UnitTypes)GC.getInfoTypeForString("UNIT_NATIVE_SLAVE_COLONY"))					// MacAurther

#define UNITCLASS_SETTLER		  ((UnitClassTypes)GC.getInfoTypeForString("UNITCLASS_SETTLER"))					// MacAurther
#define UNITCLASS_PIONEER		  ((UnitClassTypes)GC.getInfoTypeForString("UNITCLASS_PIONEER"))					// MacAurther
#define UNITCLASS_NATIVE_SLAVE	  ((UnitClassTypes)GC.getInfoTypeForString("UNITCLASS_NATIVE_SLAVE"))				// MacAurther
#define UNITCLASS_AFRICAN_SLAVE	  ((UnitClassTypes)GC.getInfoTypeForString("UNITCLASS_AFRICAN_SLAVE"))				// MacAurther
#define UNITCLASS_GREAT_STATESMAN ((UnitClassTypes)GC.getInfoTypeForString("UNITCLASS_GREAT_STATESMAN"))			// MacAurther
#define UNITCLASS_SLAVE_REVOLT	  ((UnitClassTypes)GC.getInfoTypeForString("UNITCLASS_SLAVE_REVOLT"))				// MacAurther

#define NUM_NATIVE_TECHS		  ((TechTypes)FISHING + 1)															// MacAurther

#define ESPIONAGEMISSION_COUP	  ((EspionageMissionTypes)GC.getInfoTypeForString("ESPIONAGEMISSION_COUP"))			// MacAurther

#define BUILD_ROAD				  ((BuildTypes)GC.getInfoTypeForString("BUILD_ROAD"))								// MacAurther
#define BUILD_CONTACT_TRIBE		  ((BuildTypes)GC.getInfoTypeForString("BUILD_CONTACT_TRIBE"))						// MacAurther
#define BUILD_FORT				  ((BuildTypes)GC.getInfoTypeForString("BUILD_FORT"))								// MacAurther
#define BUILD_PLANTATION		  ((BuildTypes)GC.getInfoTypeForString("BUILD_PLANTATION"))							// MacAurther

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

enum RegionGroup
{
	NO_REGION_GROUP = -1,
	REGION_GROUP_NORTH_AMERICA,
	REGION_GROUP_CENTRAL_AMERICA,
	REGION_GROUP_SOUTH_AMERICA,
	REGION_GROUP_EUROPE,
	REGION_GROUP_OCEANIA,
	NUM_REGION_GROUPS,
};

enum CultureGroups
{
	NO_CULTURE_GROUP = -1,
	CULTURE_GROUP_NATIVE,
	CULTURE_GROUP_COLONY,
	CULTURE_GROUP_NATION,
	NUM_CULTURE_GROUPS,
};

// MacAurther
enum RegionPowers
{
	NO_RP = -1,
	RP_ANDES,
	RP_ANGLO_AMERICA,
	RP_ARCTIC,
	RP_DESERT,
	RP_EUROPE,
	RP_LAKES_AND_RIVERS,
	RP_LATIN_AMERICA,
	RP_MESOAMERICA,
	RP_MINOR,
	RP_PACIFIC,
	RP_PLAINS,
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