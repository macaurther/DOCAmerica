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

#define UNIT_IMMIGRANT			  ((UnitTypes)GC.getInfoTypeForString("UNIT_IMMIGRANT"))							// MacAurther
#define UNIT_TIWANAKU_SISQENO	  ((UnitTypes)GC.getInfoTypeForString("UNIT_TIWANAKU_SISQENO"))						// MacAurther Todo: Not needed?
#define UNIT_HAWAIIAN_WAA_KAULUA  ((UnitTypes)GC.getInfoTypeForString("UNIT_HAWAIIAN_WAA_KAULUA"))					// MacAurther
#define UNIT_AMERICAN_AGENT		  ((UnitTypes)GC.getInfoTypeForString("UNIT_AMERICAN_AGENT"))						// MacAurther
#define UNIT_CANNON				  ((UnitTypes)GC.getInfoTypeForString("UNIT_CANNON"))								// MacAurther
#define UNIT_CANOE				  ((UnitTypes)GC.getInfoTypeForString("UNIT_CANOE"))								// MacAurther
#define UNIT_TRACKMAN			  ((UnitTypes)GC.getInfoTypeForString("UNIT_TRACKMAN"))								// MacAurther

#define UNITCLASS_SETTLER		  ((UnitClassTypes)GC.getInfoTypeForString("UNITCLASS_SETTLER"))					// MacAurther
#define UNITCLASS_PIONEER		  ((UnitClassTypes)GC.getInfoTypeForString("UNITCLASS_PIONEER"))					// MacAurther
#define UNITCLASS_SLAVE			  ((UnitClassTypes)GC.getInfoTypeForString("UNITCLASS_SLAVE"))						// MacAurther
#define UNITCLASS_GREAT_STATESMAN ((UnitClassTypes)GC.getInfoTypeForString("UNITCLASS_GREAT_STATESMAN"))			// MacAurther

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
	REGION_NORTH_CASCADIA, // British Columbia
	REGION_NORTH_PLAINS, // Alberta, Manitoba, Saskatchewan
	REGION_ONTARIO, // Ontario
	REGION_QUEBEC, // Quebec
	REGION_NEW_FOUNDLAND, // New Foundland, Labrador, New Brunswick
	REGION_SOUTH_CASCADIA, // Oregon, Washington
	REGION_CALIFORNIA, // California
	REGION_ROCKIES, // Idaho, Montana, Wyoming, Colorado, Nevada, Utah
	REGION_SOUTHWEST, //Arizona, New Mexico
	REGION_TEXAS, // Texas, Oklahoma
	REGION_GREAT_PLAINS, // N/S Dakota, Nebraska, Kansas, Iowa, Missouri
	REGION_GREAT_LAKES, // Minnesota, Wisconsin, Illinois, Michigan, Indiana, Ohio
	REGION_NEW_ENGLAND, // Maine, New Hampshire, Vermont, Mass., Rhode Island, Connecticut
	REGION_MID_ATLANTIC, // New York, Pennsylvania, New Jersey
	REGION_MARYLAND, // Maryland, Delaware
	REGION_APPALACHIA, // West Virginia, Kentucky
	REGION_COASTAL_PLAIN, // Virginia, North Carolina, South Carolina
	REGION_DEEP_SOUTH, // Georgia, Louisiana, Arkansas, Alabama, Mississippi
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
	REGION_COLOMBIA, // Colombia
	REGION_ECUADOR, // Ecuador
	REGION_VENEZUELA, // Venezuela
	REGION_GUYANA, // Guyana, Suriname, French Guyana
	REGION_PERU, // Peru
	REGION_BOLIVIA, // Bolivia
	REGION_AMAZONAS, // Acre, Amazonas, Roraima, Rondonia
	REGION_PARA, // Para, Amapa
	REGION_BAHIA, // Maranhao, Piaui, Ceara, Rio Grande do Norte, Paraiba, Pernambuco, Alagoas, Sergipe, Bahia
	REGION_MINAS_GERAIS, // Minas Gerais, Espirito Santo, Rio de Janeiro
	REGION_MATO_GROSSO, // Mato Grosso, Mato Grosso do Sul, Tocantins, Goias
	REGION_PARANA, // Parana, Sao Paulo, Santa Catarina, Rio Grande do Sul
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

// FoB/MacAurther
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

// MacAurther
enum Homelands
{
	NO_HOMELAND = -1,
	HOMELAND_NORTH_EUROPE,
	HOMELAND_SOUTH_EUROPE,
	HOMELAND_AFRICA,
	HOMELAND_SIBERIA,
	HOMELAND_ASIA,
	NUM_HOMELANDS
};

#endif	// CVRHYES_H

static const int lTechLeaderPenalty[NUM_ERAS] = {0, 0, 20, 25, 30, 40, 50};
static const int lTechBackwardsBonus[NUM_ERAS] = {0, 20, 30, 40, 50, 60, 75};

// Leoreth: order of persecution
static const int persecutionOrder[NUM_RELIGIONS][NUM_RELIGIONS-1] = 
{
	// Judaism
	{HINDUISM, BUDDHISM, ISLAM, PROTESTANTISM, CATHOLICISM, ORTHODOXY},
	// Orthodoxy
	{ISLAM, PROTESTANTISM, CATHOLICISM, JUDAISM, HINDUISM, BUDDHISM},
	// Catholicism
	{ISLAM, PROTESTANTISM, ORTHODOXY, JUDAISM, HINDUISM, BUDDHISM},
	// Protestantism
	{ISLAM, CATHOLICISM, ORTHODOXY, JUDAISM, HINDUISM, BUDDHISM},
	// Islam
	{HINDUISM, PROTESTANTISM, CATHOLICISM, ORTHODOXY, JUDAISM, BUDDHISM},
	// Hinduism
	{ISLAM, ORTHODOXY, PROTESTANTISM, CATHOLICISM, JUDAISM, BUDDHISM},
	// Buddhism
	{ORTHODOXY, PROTESTANTISM, CATHOLICISM, JUDAISM, ISLAM, HINDUISM},
};

// Leoreth: persecution priority
static const int persecutionValue[NUM_RELIGIONS][NUM_RELIGIONS] =
{
	// JUD ORT CAT PRO ISL HIN BUD CON TAO ZOR
	{  -1,  1,  1,  1,  1,  1,  1}, // Judaism
	{   1, -1,  3,  3,  4,  1,  1}, // Orthodoxy
	{   2,  2, -1,  3,  4,  1,  1}, // Catholicism
	{   3,  2,  3, -1,  4,  1,  1}, // Protestantism
	{   1,  2,  2,  2, -1,  3,  1}, // Islam
	{   1,  3,  3,  3,  4, -1,  0}, // Hinduism
	{   1,  3,  3,  3,  4,  0, -1}, // Buddhism
};