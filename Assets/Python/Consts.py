# Rhye's and Fall of Civilization - Constants
# globals

from CvPythonExtensions import *
from DataStructures import *
from CoreTypes import *

gc = CyGlobalContext()

iWorldX = 80
iWorldY = 108

iNumPlayers = gc.getMAX_PLAYERS()

# civilizations, not players
iNumCivs = 37
#				2				3				4				5				6				7				8				9				10
(iAmerica, 		iArgentina, 	iAztecs, 		iBolivia,		iBrazil, 		iCanada, 		iChile,			iChimu,			iColombia, 		iCuba,			
iEngland, 		iFrance, 		iHaiti,			iHawaii,		iInca,			iInuit,			iIroquois,		iMaya,			iMexico, 		iMississippi,
iMuisca,		iNetherlands, 	iNorse,			iPeru,			iPortugal, 		iPuebloan,		iRussia,		iSpain, 		iTeotihuacan,	iTiwanaku,
iVenezuela,		iWari,			iIndependent, 	iIndependent2, 	iNative,		iMinor, 		iBarbarian) = tuple(Civ(i) for i in range(iNumCivs))

lBirthOrder = [
	iMaya,
	iTeotihuacan,
	iTiwanaku,
	iWari,
	iMississippi,
	iPuebloan,
	iMuisca,
	iNorse,
	iChimu,
	iInuit,
	iInca,
	iAztecs,
	iIroquois,
	iSpain,
	iPortugal,
	iEngland,
	iFrance,
	iNetherlands,
	iHawaii,
	iRussia,
	iAmerica,
	iHaiti,
	iBolivia,
	iArgentina,
	iMexico,
	iColombia,
	iChile,
	iPeru,
	iVenezuela,
	iBrazil,
	iCanada,
	iCuba
]

lCivOrder = lBirthOrder + [
	iIndependent,
	iIndependent2,
	iNative,
	iBarbarian
]

# used in: Congresses, DynamicCivs, Plague, RFCUtils, UniquePowers, Victory
# a civilisation can be in multiple civ groups
iNumCivGroups = 3
(iCivGroupEurope, iCivGroupNativeAmerica, iCivGroupAmerica) = range(iNumCivGroups)

dCivGroups = {
iCivGroupEurope : [iNorse, iSpain, iFrance, iEngland, iNetherlands, iPortugal, iRussia],
iCivGroupNativeAmerica : [iMaya, iInca, iAztecs, iTeotihuacan, iTiwanaku, iWari, iMississippi, iPuebloan, iMuisca, iChimu, iInuit, iIroquois],
iCivGroupAmerica : [iAmerica, iArgentina, iMexico, iColombia, iBrazil, iCanada, iHaiti, iBolivia, iChile, iPeru, iVenezuela, iCuba]
}

# used in: Stability
# tech groups share techs within each other on respawn
iNumTechGroups = 3
(iTechGroupWestern, iTechGroupLatinAmerica, iTechGroupNativeAmerica) = range(iNumTechGroups)

dTechGroups = {
iTechGroupWestern : [iNorse, iSpain, iFrance, iEngland, iNetherlands, iPortugal, iRussia, iAmerica, iCanada],
iTechGroupLatinAmerica: [iArgentina, iMexico, iColombia, iBrazil, iHaiti, iBolivia, iChile, iPeru, iVenezuela, iCuba],
iTechGroupNativeAmerica : [iMaya, iInca, iAztecs, iTeotihuacan, iTiwanaku, iWari, iMississippi, iPuebloan, iMuisca, iChimu, iInuit, iIroquois],
}

lBioNewWorld = [iMaya, iInca, iAztecs, iTeotihuacan, iTiwanaku, iWari, iMississippi, iPuebloan, iMuisca, iChimu, iInuit, iIroquois]

#for messages
iDuration = 14
iWhite = 0
iRed = 7
iGreen = 8
iBlue = 9
iLightBlue = 10
iYellow = 11
iDarkPink = 12
iLightRed = 20
iPurple = 25
iCyan = 44
iBrown = 55
iOrange = 88
iTan = 90
iLime = 100

# independent cities
iNumMinorCities = 1

# scripted conquerors
iNumConquests = 0

lNeighbours = [
	(iMaya, iAztecs),
	(iMaya, iMexico),
	(iMaya, iColombia),
	(iMaya, iTeotihuacan),
	(iTeotihuacan, iAztecs),
	(iTeotihuacan, iMexico),
	(iTiwanaku, iWari),
	(iTiwanaku, iMuisca),
	(iTiwanaku, iChimu),
	(iTiwanaku, iInca),
	(iTiwanaku, iPeru),
	(iTiwanaku, iColombia),
	(iWari, iPeru),
	(iWari, iInca),
	(iWari, iColombia),
	(iWari, iMuisca),
	(iMississippi, iAmerica),
	(iMississippi, iIroquois),
	(iPuebloan, iMexico),
	(iMuisca, iColombia),
	(iNorse, iInuit),
	(iNorse, iAmerica),
	(iNorse, iCanada),
	(iChimu, iPeru),
	(iChimu, iBolivia),
	(iInuit, iRussia),
	(iInuit, iAmerica),
	(iInuit, iCanada),
	(iInca, iArgentina),
	(iInca, iColombia),
	(iInca, iBrazil),
	(iInca, iPeru),
	(iInca, iChile),
	(iAztecs, iAmerica),
	(iAztecs, iMexico),
	(iAztecs, iColombia),
	(iIroquois, iAmerica),
	(iIroquois, iCanada),
	(iSpain, iFrance),
	(iSpain, iPortugal),
	(iEngland, iNetherlands),
	(iFrance, iEngland),
	(iFrance, iNetherlands),
	(iRussia, iAmerica),
	(iRussia, iCanada),
	(iAmerica, iMexico),
	(iAmerica, iCanada),
	(iAmerica, iCuba),
	(iAmerica, iHaiti),
	(iHaiti, iCuba),
	(iBolivia, iPeru),
	(iBolivia, iBrazil),
	(iBolivia, iChile),
	(iBolivia, iArgentina),
	(iArgentina, iBrazil),
	(iArgentina, iChile),
	(iColombia, iVenezuela),
	(iVenezuela, iBrazil),
	(iMexico, iColombia),
]

lInfluences = [
	(iWari, iTiwanaku),
	(iChimu, iTiwanaku),
	(iInca, iTiwanaku),
	(iAztecs, iTeotihuacan),
	(iNetherlands, iSpain),
	(iAmerica, iEngland),
	(iAmerica, iFrance),
	(iAmerica, iNetherlands),
	(iAmerica, iNorse),
	(iHaiti, iFrance),
	(iBolivia, iSpain),
	(iBolivia, iTiwanaku),
	(iArgentina, iSpain),
	(iMexico, iSpain),
	(iMexico, iFrance),
	(iMexico, iTeotihuacan),
	(iMexico, iMaya),
	(iColombia, iSpain),
	(iColombia, iMuisca),
	(iChile, iSpain),
	(iPeru, iSpain),
	(iPeru, iTiwanaku),
	(iVenezuela, iSpain),
	(iBrazil, iPortugal),
	(iCanada, iFrance),
	(iCanada, iEngland),
	(iCuba, iSpain),
]

dBirth = CivDict({
iMaya : 250,
iTeotihuacan : 250,
iTiwanaku : 250,
iWari : 500,
iMississippi : 600,
iPuebloan : 750,
iMuisca : 800,
iNorse : 874,
iChimu : 900,
iInuit : 1050,
iInca : 1100,
iAztecs : 1250,
iIroquois : 1450,
iSpain : 1496,
iPortugal : 1532,
iEngland : 1607,
iFrance : 1608,
iNetherlands : 1625,
iHawaii : 1650,
iRussia: 1743,
iAmerica : 1775,
iHaiti : 1804,
iBolivia : 1810,
iArgentina : 1810,
iMexico : 1810,
iColombia : 1810,
iChile : 1810,
iPeru : 1811,
iVenezuela : 1811,
iBrazil : 1822,
iCanada : 1867,
iCuba : 1898,
}, 250)

lBirthCivs = dBirth.keys()

dFall = CivDict({
iMaya : 900,
iTeotihuacan : 1150,
iTiwanaku : 1000,
iWari : 1000,
iMississippi : 1400,
iPuebloan : 1600,
iMuisca : 1540,
iChimu : 1470,
iInuit : 1600,
iInca : 1533,
iAztecs : 1521,
iIroquois : 1750,
iSpain : 1807,
iPortugal : 1807,
iFrance : 1805,
iHawaii : 1893,
iRussia : 1867,
}, 2020)

# Leoreth: determine neighbour lists from pairwise neighbours for easier lookup
dNeighbours = dictFromEdges(lBirthCivs, lNeighbours)

# Leoreth: determine influence lists from pairwise influences for easier lookup
dInfluences = dictFromEdges(lBirthCivs, lInfluences)

dResurrections = CivDict({
}, [])

dEnemyCivsOnSpawn = CivDict({
iAztecs : [iMaya],
iInca : [iWari],
iAmerica : [iEngland, iIndependent, iIndependent2, iNative],
iArgentina : [iSpain, iIndependent, iIndependent2],
iMexico : [iSpain, iIndependent, iIndependent2],
iColombia : [iSpain, iIndependent, iIndependent2],
iBrazil : [iIndependent, iIndependent2],
}, [])

dTotalWarOnSpawn = CivDict({
iInca : [iWari],
}, [])

dAggressionLevel = CivDict({
iMaya : 1,
iTeotihuacan : 1,
iTiwanaku : 1,
iWari : 1,
iMississippi : 1,
iPuebloan : 1,
iMuisca : 1,
iNorse : 1,
iChimu : 1,
iInuit : 1,
iInca : 2,
iAztecs : 2,
iIroquois : 1,
iSpain : 2,
iEngland : 2,
iFrance : 2,
iNetherlands : 2,
iHawaii : 1,
iRussia : 2,
iAmerica : 2,
iHaiti : 1,
iBolivia : 1,
iArgentina : 1,
iMexico : 1,
iColombia : 2,
iChile : 1,
iPeru : 1,
iVenezuela : 1,
iBrazil : 2,
iCanada : 1,
iCuba : 1,
}, 0)

dWarOnFlipProbability = CivDict({
iMaya: 20,
iInca: 30,
iAztecs: 50,
iSpain: 20,
iPortugal: 60,
iEngland: 50,
iFrance: 20,
iNetherlands: 60,
iRussia: 50,
iAmerica: 50,
iArgentina: 40,
iMexico: 40,
iColombia: 40,
iBrazil: 40,
iCanada: 40,
}, 0)

dResurrectionProbability = CivDict({
})

dPatienceThreshold = CivDict({
iMaya : 35,
iTeotihuacan : 20,
iTiwanaku : 20,
iWari : 20,
iMississippi : 35,
iPuebloan : 35,
iMuisca : 35,
iNorse : 30,
iChimu : 20,
iInuit : 35,
iInca : 35,
iAztecs : 30,
iIroquois : 25,
iSpain : 20,
iPortugal : 30,
iEngland : 20,
iFrance : 20,
iNetherlands : 30,
iHawaii : 25,
iRussia: 35,
iAmerica : 30,
iHaiti : 35,
iBolivia : 30,
iArgentina : 40,
iMexico : 40,
iColombia : 30,
iChile : 35,
iPeru : 35,
iVenezuela : 20,
iBrazil : 40,
iCanada : 40,
iCuba : 25,
}, 100)

dMaxColonists = CivDict({
iNorse : 1,
iSpain : 7,
iPortugal : 6,
iEngland : 6, 
iFrance : 5,
iNetherlands : 6,
iRussia : 3,
})

# initialise religion variables to religion indices from XML
iNumReligions = 10
(iJudaism, iOrthodoxy, iCatholicism, iProtestantism, iIslam, iHinduism, iBuddhism, iConfucianism, iTaoism, iZoroastrianism) = range(iNumReligions)

#Persecution preference
tPersecutionPreference = (
(iHinduism, iBuddhism, iTaoism, iConfucianism, iZoroastrianism, iIslam, iProtestantism, iCatholicism, iOrthodoxy), # Judaism
(iIslam, iProtestantism, iCatholicism, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iTaoism, iConfucianism), # Orthodoxy
(iIslam, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iTaoism, iConfucianism), # Catholicism
(iIslam, iCatholicism, iOrthodoxy, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iTaoism, iConfucianism), # Protestantism
(iHinduism, iProtestantism, iCatholicism, iOrthodoxy, iJudaism, iTaoism, iConfucianism, iZoroastrianism, iBuddhism), # Islam
(iIslam, iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iTaoism, iConfucianism, iBuddhism), # Hinduism
(iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iTaoism, iIslam, iConfucianism, iHinduism), # Buddhism
(iIslam, iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iTaoism), # Confucianism
(iIslam, iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iConfucianism), # Taoism
(iIslam, iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iBuddhism, iHinduism, iTaoism, iConfucianism), # Zoroastrianism
)

# pagan religions
iNumPaganReligions = 12
#				2				3				4				5				6				7				8				9				10
(iAngakkuq, 	iAsatru, 		iAtua, 			iDruidism, 		iGaiwiio,		iInti, 			iKachin,		iMidewiwin, 	iRodnovery, 	iTeotlMaya, 
iTeotlAztec, 	iYoruba) = range(iNumPaganReligions)

iPaganVictory = iNumReligions
iSecularVictory = iNumReligions + 1

# corporations
iNumCorporations = 9
(iSilkRoute, iTradingCompany, iCerealIndustry, iFishingIndustry, iTextileIndustry, iSteelIndustry, iOilIndustry, iLuxuryIndustry, iComputerIndustry) = range(iNumCorporations)

# initialise tech variables to unit indices from XML

iNumTechs = 145
#				2				3				4				5				6				7
(iTanning, 		iMining, 		iPottery, 		iPastoralism, 	iAgriculture, 	iMythology, 	iSailing,
iArtisanry, 	iMasonry, 		iMathematics, 	iProperty, 		iCeremony, 		iPriesthood, 	iNavigation,
iSmelting, 		iConstruction, 	iAesthetics, 	iCalendar, 		iWriting, 		iLaw, 			iMedicine,
iOldWorldTactics,iOldWorldScience,iOldWorldCulture,
iGunpowder, 	iCompanies, 	iFinance, 		iCartography, 	iHumanities, 	iPrinting, 		iJudiciary,
iFirearms, 		iLogistics, 	iExploration, 	iOptics, 		iDiplomacy, 	iEvangelism, 	iGovernors,
iFortification,	iEconomics, 	iColonization, 	iShipbuilding, 	iCharter, 		iCommunity, 	iIndentures,
iCombinedArms, 	iTriangularTrade, iExploitation, iTimekeeping, 	iEducation, 	iPolitics, 		iHorticulture,
iTactics,		iCurrency,		iGeography,		iAcademia,		iUrbanPlanning,	iStatecraft,	iSocialContract,
iReplaceableParts, iFreeMarket,	iNewspapers,	iScientificMethod, iArchitecture, iSociology,	iHeritage,
iRegiments, 	iBonds,			iPostalService,	iMeteorology,	iSurveying,		iRepresentation, iIndependence,
iMetallurgy,	iProtectionism,	iHydraulics,	iPhysics,		iGeology,		iRightsOfMan,	iFederalism,
iMachineTools, 	iThermodynamics, iEngineeing, 	iChemistry, 	iPioneering,	iCivilLiberties, iNationalism,
iMeasurement, 	iEngine, 		iRailroad, 		iElectricity, 	iConservation, 	iEmancipation, 	iImperialism,
iBallistics,	iAssemblyLine,	iCombustion,	iTelegraph,		iBiology,		iLaborUnions,	iJournalism,
iPneumatics, 	iFlight, 		iRefining, 		iFilm, 			iRefrigeration, iConsumerism, 	iCivilRights,
iInfrastructure, iAeronautics, 	iSynthetics, 	iRadio, 		iMicrobiology, 	iMacroeconomics, iSocialServices,
iAviation, 		iRocketry, 		iFission, 		iElectronics, 	iPsychology, 	iPowerProjection, iGlobalism,
iRadar, 		iSpaceflight, 	iNuclearPower, 	iLaser, 		iTelevision, 	iTourism, 		iEcology,
iAerodynamics, 	iSatellites, 	iSuperconductors, iTelecommunications, iComputers, iRenewableEnergy, iGenetics,
iSupermaterials, iFusion, 		iNanotechnology, iRobotics,		iAutomation, 
iUnifiedTheory, iArtificialIntelligence, iBiotechnology,
iTranshumanism) = range(iNumTechs)

# initialise unit variables to unit indices from XML

iNumUnits = 161
#				2				3				4				5				6				7				8				9				10
(iBear, 		iPanther, 		iWolf, 			iSettler, 		iCliffDweller,	iDogSled,		iPioneer,		iWorker, 		iArtisan,		iPromyshlenniki,
iLaborer, 		iMadeireiro, 	iScout, 		iExplorer, 		iBandeirante, 	iCoureurDesBois,iRanger,		iParatrooper,	iSpy, 			iSisqeno,
iAgent,			iInquisitor,	iJewishMiss, 	iOrthodoxMiss, 	iCatholicMiss, 	iProtestantMiss, iIslamicMiss, 	iHinduMiss, 	iBuddhistMiss,	iConfucianMiss, 
iTaoistMiss, 	iZoroastrianMiss, iMilitia1,	iFalconDancer,	iMilitia2,		iMilitia3,		iMilitia4,		iMinuteman,		iMilitia5,		iMilitia6,		
iMilitia7,		iWarrior, 		iArquebusier,	iArmedBrave,	iArmedSlave,	iMusketman,		iMusketeer,		iRifleman,		iInfantry,		iMechInfantry,	
iAxeman,		iAucac,			iDogSoldier,	iJaguar,		iTercio,		iMohawk,		iFusilier,		iCompagnies,	iLineInfantry,	iRedcoat,		
iMarine,		iSpearman,		iSuchucChiqui,	iPikeman,		iAntiTank,		iRPG,			iArcher,		iPicta,			iSlinger,		iCrossbowman,	
iLightCannon,	iFieldCannon,	iGattlingGun,	iMachineGun,	iAtlatlist,		iHolkan,		iGuecha,		iSkirmisher,	iGrenadier,		iAlbionLegion,	
iGuerilla,		iHorseArcher,	iHussar,		iMountedBrave,	iDragoon,		iLlanero,		iPistolier,		iLightTank,		iGunship,		iCuirassier,	
iConquistador,	iCarabineer,	iGrenadierCavalry,iCavalry,		iRural,			iTank,			iMainBattleTank,iBombard,		iCannon,		iHeavyCannon,	
iRifledCannon,	iArtillery,		iHowitzer,		iAAGun,			iMobileSAM,		iWorkboat,		iCanoe,			iLongship,		iWaaKaulua,		iCaravel,		
iCarrack,		iGalleon,		iWestIndianman,	iBrigantine,	iSteamship,		iTransport,		iCarrier,		iSloop,			iFrigate,		iIronclad,		
iDestroyer,		iCorvette,		iStealthDestroyer,iPrivateer,	iTorpedoBoat,	iSubmarine,		iNuclearSubmarine,iShipOfTheLine,iManOfWar,		iCruiser,		
iBattleship,	iMissileCruiser,iBiplane,		iFighter,		iJetFighter,	iDrone,			iBomber,		iStealthBomber,	iNuclearBomber,	iGuidedMissile,	
iICBM,			iSatellite,		iGreatProphet, 	iGreatArtist, 	iGreatScientist,iGreatMerchant, iGreatEngineer, iGreatStatesman,iGreatGeneral,	iArgentineGreatGeneral,
iGreatSpy,iFeGreatProphet,iFeGreatArtist, iFeGreatScientist, iFeGreatMerchant, iFeGreatEngineer, iFeGreatStatesman,iFeGreatGeneral,iFeGreatSpy,	iSlave,			
iAztecSlave) = range(iNumUnits)

# Unit enumeration debug
print('iLaborer: ' + str(iLaborer))
print('iTaoistMiss: ' + str(iTaoistMiss))
print('iMechInfantry: ' + str(iMechInfantry))
print('iPicta: ' + str(iPicta))
print('iPistolier: ' + str(iPistolier))
print('iCaravel: ' + str(iCaravel))
print('iBattleship: ' + str(iBattleship))
print('iGreatSpy: ' + str(iGreatSpy))

lGreatPeopleUnits = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman]

dFemaleGreatPeople = {
iGreatProphet : iFeGreatProphet,
iGreatArtist : iFeGreatArtist,
iGreatScientist : iFeGreatScientist,
iGreatMerchant : iFeGreatMerchant,
iGreatEngineer : iFeGreatEngineer,
iGreatStatesman : iFeGreatStatesman,
iGreatGeneral : iFeGreatGeneral,
iGreatSpy : iFeGreatSpy,
}

iNumUnitRoles = 22
(iBase, iDefend, iAttack, iCounter, iShock, iHarass, iCityAttack, iWorkerSea, iSettle, iSettleSea, 
iAttackSea, iFerry, iEscort, iExplore, iShockCity, iSiege, iCitySiege, iExploreSea, iSkirmish, iLightEscort,
iWork, iMissionary) = range(iNumUnitRoles)

# initialise bonuses variables to bonuses IDs from WBS
iNumBonuses = 58
#				2				3				4				5				6				7				8				9				10
(iAluminium, 	iAmber,			iCamel, 		iCitrus,		iCoal, 			iCopper, 		iDates,			iHorse, 		iIron, 			iMarble, 
iOil, 			iStone, 		iUranium, 		iBanana, 		iClam, 			iCorn, 			iCow, 			iCrab,			iDeer, 			iFish, 
iPig, 			iPotato,		iRice, 			iSheep, 		iWheat, 		iCocoa,			iCoffee, 		iCotton, 		iDye, 			iFur, 
iGems, 			iGold, 			iIncense, 		iIvory, 		iJade,			iMillet,		iObsidian,		iOlives,		iOpium,			iPearls, 
iRareEarths,	iRubber,		iSalt,			iSilk, 			iSilver, 		iSpices,		iSugar, 		iTea, 			iTimber,		iTobacco, 
iWine, 			iWhales, 		iSoccer, 		iSongs, 		iMovies, 		iLlama, 		iShrimp, 		iCochineal) = range(iNumBonuses)
# Buildings

iNumBuildings = 173
# Buildings (90)
#				2				3				4				5				6				7				8				9				10
(iPalace, 		iBarracks, 		iGranary,		iTerrace, 		iColcas,		iIgloo,			iSmokehouse, 	iPaganTemple, 	iMonument,		iTotemPole, 
iWalls, 		iKancha,		iStable, 		iLibrary,		iHarbor, 		iAqueduct, 		iTheatre,		iArena, 		iBallCourt, 	iCharreadaArena, 
iLighthouse, 	iWeaver,		iMarket,		iJail, 			iSacrificialAltar, iBath, 		iTemazcal,		iForge, 		iGoldsmith,		iCastle, 		
iPharmacy, 		iPostOffice, 	iTambo,			iWharf,			iCoffeehouse,	iSalon, 		iBank, 			iRoyalExchange, iConstabulary, 	iMountedPolice, 
iCustomsHouse, 	iFeitoria, 		iUniversity,	iCivicSquare, 	iKalasasaya, 	iSewer, 		iStarFort, 		iEstate, 		iFazenda, 		iHacienda, 		
iDrydock, 		iLevee, 		iObservatory, 	iWarehouse, 	iCourthouse, 	iFactory, 		iDistillery, 	iPark,			iEffigyMound,	iCoalPlant, 	
iRailwayStation, iLaboratory, 	iNewsPress, 	iIndustrialPark, iCinema, 		iHospital, 		iSupermarket, 	iColdStoragePlant, iPublicTransportation, iDepartmentStore, 
iMall, 			iBroadcastTower, iIntelligenceAgency, iElectricalGrid, iAirport, iBunker, 		iBombShelters, 	iHydroPlant, 	iSecurityBureau, iStadium, 
iContainerTerminal, iNuclearPlant, iSupercomputer, iHotel, 		iRecyclingCenter, iLogisticsCenter, iSolarPlant,iFiberNetwork, iAutomatedFactory, iVerticalFarm, 
# Religious Buildings (40)
#				2				3				4				5				6				7				8				9				10
iJewishTemple, iJewishCathedral, iJewishMonastery, iJewishShrine, iOrthodoxTemple, iOrthodoxCathedral, iOrthodoxMonastery, iOrthodoxShrine, iCatholicTemple, iCatholicCathedral, 
iCatholicMonastery, iCatholicShrine, iProtestantTemple, iProtestantCathedral, iProtestantMonastery, iProtestantShrine, iIslamicTemple, iIslamicCathedral, iIslamicMonastery, iIslamicShrine, 
iHinduTemple, iHinduCathedral, iHinduMonastery, iHinduShrine, iBuddhistTemple, iBuddhistCathedral, iBuddhistMonastery, iBuddhistShrine, iConfucianTemple, iConfucianCathedral, 
iConfucianMonastery, iConfucianShrine, iTaoistTemple, iTaoistCathedral, iTaoistMonastery, iTaoistShrine, iZoroastrianTemple, iZoroastrianCathedral, iZoroastrianMonastery, iZoroastrianShrine, 
# Great Buildings (6)
#				2				3				4				5				6				7				8				9				10
iAcademy, 		iAdministrativeCenter, iManufactory, iArmoury, 	iMuseum, 		iStockExchange, 
# Great Buildings/National Wonders (13)
#				2				3				4				5				6				7				8				9				10
iTradingCompanyBuilding, iIberianTradingCompanyBuilding, iNationalMonument, iNationalTheatre, iNationalGallery, iNationalCollege, iMilitaryAcademy, iSecretService, iIronworks, iRedCross, 	
iNationalPark, 	iCentralBank, 	iSpaceport, 
# Great Wonders (24)
#				2				3				4				5				6				7				8				9				10
iTempleOfKukulkan, iMachuPicchu, iFloatingGardens, iGuadalupeBasilica, iSaltCathedral, iStatueOfLiberty, iChapultepecCastle, iMenloPark, iBrooklynBridge, iHollywood, 
iEmpireStateBuilding, iLasLajasSanctuary, iFrontenac, iCristoRedentor, iGoldenGateBridge, iItaipuDam, iGraceland, iCNTower, 	iPentagon, 		iUnitedNations, 
iCrystalCathedral, iWorldTradeCenter,  iHubbleSpaceTelescope, iSpaceElevator) = range(iNumBuildings)

# Building enumeration debug
print('iStable: ' + str(iStable))
print('iMarket: ' + str(iMarket))
print('iCoffeehouse: ' + str(iCoffeehouse))
print('iSewer: ' + str(iSewer))
print('iFactory: ' + str(iFactory))
print('iSupermarket: ' + str(iSupermarket))
print('iBombShelters: ' + str(iBombShelters))
print('iSolarPlant: ' + str(iSolarPlant))
print('iVerticalFarm: ' + str(iVerticalFarm))
print('iCatholicCathedral: ' + str(iCatholicCathedral))
print('iIslamicShrine: ' + str(iIslamicShrine))
print('iConfucianCathedral: ' + str(iConfucianCathedral))
print('iZoroastrianShrine: ' + str(iZoroastrianShrine))
print('iStockExchange: ' + str(iStockExchange))
print('iRedCross: ' + str(iRedCross))
print('iSpaceport: ' + str(iSpaceport))
print('iHollywood: ' + str(iHollywood))
print('iUnitedNations: ' + str(iUnitedNations))
print('iSpaceElevator: ' + str(iSpaceElevator))

iBeginWonders = iTempleOfKukulkan # different from DLL constant because that includes national wonders

iTemple = iJewishTemple #generic
iCathedral = iJewishCathedral #generic
iMonastery = iJewishMonastery #generic
iShrine = iJewishShrine #generic

iFirstWonder = iTempleOfKukulkan

iPlague = iNumBuildings
iNumBuildingsPlague = iNumBuildings+1

#Civics
iNumCivics = 42
(iChiefdom, iDespotism, iMonarchy, iRepublic, iElective, iStateParty, iDemocracy,
iAuthority, iCitizenship, iVassalage, iMeritocracy, iCentralism, iRevolutionism, iConstitution,
iTraditionalism, iSlavery, iManorialism, iCasteSystem, iIndividualism, iTotalitarianism, iEgalitarianism,
iReciprocity, iRedistribution, iMerchantTrade, iRegulatedTrade, iFreeEnterprise, iCentralPlanning, iPublicWelfare,
iAnimism, iDeification, iClergy, iMonasticism, iTheocracy, iTolerance, iSecularism,
iSovereignty, iConquest, iTributaries, iIsolationism, iColonialism, iNationhood, iMultilateralism) = range(iNumCivics)

iNumCivicCategories = 6
(iCivicsGovernment, iCivicsLegitimacy, iCivicsSociety, iCivicsEconomy, iCivicsReligion, iCivicsTerritory) = range(iNumCivicCategories)

#Specialists
iNumSpecialists = 19
(iSpecialistCitizen, iSpecialistPriest, iSpecialistArtist, iSpecialistScientist, iSpecialistMerchant, iSpecialistEngineer, iSpecialistStatesman,
iSpecialistGreatProphet, iSpecialistGreatArtist, iSpecialistGreatScientist, iSpecialistGreatMerchant, iSpecialistGreatEngineer, iSpecialistGreatStatesman, iSpecialistGreatGeneral, iSpecialistGreatSpy, 
iSpecialistResearchSatellite, iSpecialistCommercialSatellite, iSpecialistMilitarySatellite, 
iSpecialistSlave) = range(iNumSpecialists)

lGreatSpecialists = [iSpecialistGreatProphet, iSpecialistGreatArtist, iSpecialistGreatScientist, iSpecialistGreatMerchant, iSpecialistGreatEngineer, iSpecialistGreatStatesman, iSpecialistGreatGeneral, iSpecialistGreatSpy]

#Stability Levels
iNumStabilityLevels = 5
(iStabilityCollapsing, iStabilityUnstable, iStabilityShaky, iStabilityStable, iStabilitySolid) = range(iNumStabilityLevels)
StabilityLevelTexts = ["TXT_KEY_STABILITY_COLLAPSING", "TXT_KEY_STABILITY_UNSTABLE", "TXT_KEY_STABILITY_SHAKY", "TXT_KEY_STABILITY_STABLE", "TXT_KEY_STABILITY_SOLID"]

#Stability Types
iNumStabilityTypes = 5
(iStabilityExpansion, iStabilityEconomy, iStabilityDomestic, iStabilityForeign, iStabilityMilitary) = range(iNumStabilityTypes)
StabilityTypesTexts = ["TXT_KEY_STABILITY_CATEGORY_EXPANSION", "TXT_KEY_STABILITY_CATEGORY_ECONOMY", "TXT_KEY_STABILITY_CATEGORY_DOMESTIC", "TXT_KEY_STABILITY_CATEGORY_FOREIGN", "TXT_KEY_STABILITY_CATEGORY_MILITARY"]

#Stability Parameters
iNumStabilityParameters = 23
(iParameterCorePeriphery, iParameterAdministration, iParameterSeparatism, iParameterRecentExpansion, iParameterRazedCities, iParameterIsolationism,	# Expansion
iParameterEconomicGrowth, iParameterTrade, iParameterMercantilism, iParameterCentralPlanning,								# Economy
iParameterHappiness, iParameterCivicCombinations, iParameterCivicsEraTech, iParameterReligion,								# Domestic
iParameterVassals, iParameterDefensivePacts, iParameterRelations, iParameterNationhood, iParameterTheocracy, iParameterMultilateralism,			# Foreign
iParameterWarSuccess, iParameterWarWeariness, iParameterBarbarianLosses) = range(iNumStabilityParameters)						# Military

#Regions
iNumRegions = 36
(rAlaska, rNunavut, rNorthPlains, rOntario, rQuebec, rNewFoundland, rNewEngland, rMidAtlantic, rDeepSouth, rGulfCoast, 
rMidwest, rSouthwest, rGreatPlains, rRockies, rCalifornia, rCascadia, rSierraMadre, rBajio, rYucatan, rMesoamerica,
rCaribbean, rHawaii, rColombia, rVenezuela, rGuyana, rPeru, rBolivia, rAmazon, rBrazilianHighlands, rPantanal, 
rChile, rParaguay, rUruguay, rPampas, rPatagonia, rGreenland) = range(iNumRegions)

lCanada = [rNunavut, rNorthPlains, rOntario, rQuebec, rNewFoundland]
lUnitedStates = [rAlaska, rNewEngland, rMidAtlantic, rDeepSouth, rGulfCoast, rMidwest, rSouthwest, rGreatPlains, rRockies, rCalifornia, rCascadia, rHawaii]
lMexico = [rSierraMadre, rBajio, rYucatan]
lBrazil = [rAmazon, rBrazilianHighlands, rPantanal]
lArgentina = [rPampas, rPatagonia]

lSouthAmerica = [rColombia, rVenezuela, rGuyana, rPeru, rBolivia, lBrazil, rChile, rParaguay, rUruguay, lArgentina]
lCentralAmerica = [rMesoamerica, rCaribbean]
lNorthAmerica = [lCanada, lUnitedStates, lMexico]

lAmerica = [lSouthAmerica, lCentralAmerica, lNorthAmerica]


#Projects

iNumProjects = 21
(iManhattanProject, iTheInternet, iHumanGenome, iSDI, iGPS, iISS, iBallisticMissile, iFirstSatellite, iManInSpace, iLunarLanding,
iGoldenRecord, iMarsMission, iLunarColony, iInterstellarProbe, iMarsFraming, iMarsPowerSource, iMarsExtractor, iMarsHabitat, iMarsHydroponics, iMarsLaboratory, iMarsControlCenter) = range(iNumProjects)

lMarsBaseComponents = [iMarsFraming, iMarsPowerSource, iMarsExtractor, iMarsHabitat, iMarsHydroponics, iMarsLaboratory, iMarsControlCenter]

#Eras

iNumEras = 7
(iPreColumbian, iExploration, iColonial, iRevolutionary, iIndustrial, iModern, iAtomic) = range (iNumEras)

# Culture

iNumCultureLevels = 7
(iCultureLevelNone, iCultureLevelPoor, iCultureLevelFledgling, iCultureLevelDeveloping, iCultureLevelRefined, iCultureLevelInfluential, iCultureLevelLegendary) = range(iNumCultureLevels)


#Improvements

iNumImprovements = 30
(iLandWorked, iWaterWorked, iCityRuins, iHut, iFarm, iPaddyField, iFishingBoats, iOceanFishery, iWhalingBoats, iMine, 
iWorkshop, iLumbermill, iWindmill, iWatermill, iPlantation, iSlavePlantation, iQuarry, iPasture, iCamp, iWell, 
iOffshorePlatform, iWinery, iCottage, iHamlet, iVillage, iTown, iFort, iForestPreserve, iMarinePreserve, iSolarCollector) = range(iNumImprovements)

iNumRoutes = 4
(iRouteRoad, iRouteRailroad, iRouteRomanRoad, iRouteHighway) = range(iNumRoutes)

#feature & terrain

iNumFeatures = 13
#				2				3				4				5				6				7				8				9				10
(iSeaIce, 		iJungle, 		iOasis, 		iFloodPlains, 	iForest, 		iBog, 			iSwamp, 		iCape, 			iIslands, 		iRainforest, 
iFallout, 		iTaiga, 		iPalmForest) = range(iNumFeatures)

iNumTerrains = 19
#				2				3				4				5				6				7				8				9				10
(iGrass, 		iPlains, 		iDesert, 		iTundra, 		iSnow, 			iCoast, 		iOcean, 		iTerrainPeak, 	iTerrainHills, 	iMarsh,
iLagoon,		iArcticCoast,	iSemidesert,	iPrairie,		iMoorland,		iSaltflat,		iSaltlake,		iAtoll,			iSavanna) = range(iNumTerrains)


#Plague
iImmunity = 20

# Victory
iVictoryPaganism = 10
iVictorySecularism = 11


#leaders
iNumLeaders = 54
#				2				3				4				5				6				7				8				9				10
(iLeaderBarbarian, iNativeLeader, iIndependentLeader, iAhoeitu, iPacal,			iRagnar,		iGustav, 		iGerhardsen, 	iIsabella, 		iPhilip, 
iFranco,		iCharlemagne, 	iLouis, 		iNapoleon, 		iDeGaulle, 		iAlfred, 		iElizabeth, 	iVictoria, 		iChurchill, 	iIvan, 	
iPeter, 		iCatherine, 	iAlexanderI, 	iStalin, 		iAfonso, 		iJoao, 			iMaria, 		iHuaynaCapac, 	iPachacuti,		iMontezuma, 
iWillemVanOranje, iWilliam, 	iWashington,	iLincoln, 		iRoosevelt, 	iSanMartin, 	iPeron, 		iJuarez, 		iSantaAnna, 	iCardenas, 
iBolivar, 		iPedro, 		iVargas,		iMacDonald, 	iTrudeau, 		iSittingBull,	iMalkuHuyustus,	iWariCapac,		iTacaynamo,		iRedHorn,
iAua,			iSaguamanchica,	iAtlatlCauac,	iCastilla) = range(iNumLeaders)

dResurrectionLeaders = CivDict({
})

iNumPeriods = 0
#() = range(iNumPeriods)

iNumImpacts = 5
(iImpactMarginal, iImpactLimited, iImpactSignificant, iImpactCritical, iImpactPlayer) = range(iNumImpacts)

lSecondaryCivs = [iBolivia, iChile, iChimu, iCuba, iHaiti, iHawaii, iInuit, iIroquois, iMississippi, iMuisca, iNorse, iPeru, iPuebloan, iVenezuela, iWari]

(i250AD, i1500AD, i1770AD) = range(3)

# Stability overlay and editor
iNumPlotStabilityTypes = 5
(iCore, iHistorical, iContest, iForeignCore, iAIForbidden) = range(iNumPlotStabilityTypes)
lStabilityColors = ["COLOR_CYAN", "COLOR_GREEN", "COLOR_YELLOW", "COLOR_RED", "COLOR_PLAYER_LIGHT_PURPLE"]
lPresetValues = [3, 20, 90, 200, 500, 700]

iMaxWarValue = 12
lWarMapColors = ["COLOR_RED", "COLOR_PLAYER_ORANGE", "COLOR_YELLOW", "COLOR_GREEN", "COLOR_PLAYER_DARK_GREEN", "COLOR_BLUE"]

lReligionMapColors = ["COLOR_PLAYER_ORANGE", "COLOR_YELLOW", "COLOR_GREEN", "COLOR_CYAN"]
lReligionMapTexts = ["TXT_KEY_CULTURELEVEL_NONE", "TXT_KEY_WB_RELIGIONMAP_MINORITY", "TXT_KEY_WB_RELIGIONMAP_PERIPHERY", "TXT_KEY_WB_RELIGIONMAP_HISTORICAL", "TXT_KEY_WB_RELIGIONMAP_CORE"]

lNetworkEvents = {
	"CHANGE_COMMERCE_PERCENT" :	1200,
}

newline = "[NEWLINE]"
bullet = "[ICON_BULLET]"
event_bullet = "INTERFACE_EVENT_BULLET"
event_cancel = "INTERFACE_BUTTONS_CANCEL"