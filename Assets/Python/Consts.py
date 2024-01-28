# Rhye's and Fall of Civilization - Constants
# globals

from CvPythonExtensions import *
from DataStructures import *
from CoreTypes import *

gc = CyGlobalContext()

iWorldX = 59
iWorldY = 122

iNumPlayers = gc.getMAX_PLAYERS()

# civilizations, not players
iNumCivs = 37
#				2				3				4				5				6				7				8				9				10
(iAmerica, 		iArgentina, 	iAztecs, 		iBrazil, 		iCanada, 		iChimu,			iColombia, 		iEngland, 		iFrance, 		iHaiti,			
iHawaii,		iInca,			iInuit,			iIroquois,		iMaya,			iMexico, 		iMississippi,	iMuisca,		iNetherlands, 	iNorse,			
iPeru,			iPortugal, 		iPuebloan,		iPurepecha,		iRussia,		iSpain, 		iTeotihuacan,	iTiwanaku,		iVenezuela,		iWari,			
iZapotec,		iIndependent, 	iIndependent2, 	iIndependent3,	iNative,		iMinor, 		iBarbarian) = tuple(Civ(i) for i in range(iNumCivs))

lBirthOrder = [
	iMaya,
	iTeotihuacan,
	iZapotec,
	iTiwanaku,
	iWari,
	iMississippi,
	iPuebloan,
	iMuisca,
	iNorse,
	iChimu,
	iInuit,
	iInca,
	iPurepecha,
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
	iArgentina,
	iMexico,
	iColombia,
	iPeru,
	iBrazil,
	iVenezuela,
	iCanada,
]

lCivOrder = lBirthOrder + [
	iIndependent,
	iIndependent2,
	iIndependent3,
	iNative,
	iBarbarian
]

# used in: Congresses, DynamicCivs, Plague, RFCUtils, UniquePowers, Victory
# a civilisation can be in multiple civ groups
iNumCivGroups = 4
(iCivGroupEurope, iCivGroupNativeAmerica, iCivGroupAmerica, iCivGroupNATO) = range(iNumCivGroups)

dCivGroups = {
iCivGroupEurope : [iNorse, iSpain, iFrance, iEngland, iNetherlands, iPortugal, iRussia],
iCivGroupNativeAmerica : [iMaya, iInca, iAztecs, iTeotihuacan, iTiwanaku, iWari, iMississippi, iPuebloan, iMuisca, iChimu, iInuit, iIroquois, iZapotec, iPurepecha],
iCivGroupAmerica : [iAmerica, iArgentina, iMexico, iColombia, iBrazil, iCanada, iHaiti, iPeru, iVenezuela],
iCivGroupNATO : [iAmerica, iCanada, iNorse, iEngland, iFrance, iSpain, iPortugal, iNetherlands],
}

# used in: Stability
# tech groups share techs within each other on respawn
iNumTechGroups = 3
(iTechGroupWestern, iTechGroupLatinAmerica, iTechGroupNativeAmerica) = range(iNumTechGroups)

dTechGroups = {
iTechGroupWestern : [iNorse, iSpain, iFrance, iEngland, iNetherlands, iPortugal, iRussia, iAmerica, iCanada],
iTechGroupLatinAmerica: [iArgentina, iMexico, iColombia, iBrazil, iHaiti, iPeru, iVenezuela],
iTechGroupNativeAmerica : [iMaya, iInca, iAztecs, iTeotihuacan, iTiwanaku, iWari, iMississippi, iPuebloan, iMuisca, iChimu, iInuit, iIroquois, iHawaii, iZapotec, iPurepecha],
}

lBioNewWorld = [iMaya, iInca, iAztecs, iTeotihuacan, iTiwanaku, iWari, iMississippi, iPuebloan, iMuisca, iChimu, iInuit, iIroquois, iHawaii, iZapotec, iPurepecha]
lRevolutionaries = [iAmerica, iHaiti, iArgentina, iMexico, iColombia, iPeru]	# Europeans get expeditionary force at the spawn of these civs

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
iNumMinorCities = 4

# scripted conquerors
iNumConquests = 9

lNeighbours = [
	(iMaya, iAztecs),
	(iMaya, iMexico),
	(iMaya, iColombia),
	(iMaya, iTeotihuacan),
	(iMaya, iZapotec),
	(iTeotihuacan, iAztecs),
	(iTeotihuacan, iMexico),
	(iTeotihuacan, iZapotec),
	(iTeotihuacan, iPurepecha),
	(iZapotec, iMexico),
	(iZapotec, iAztecs),
	(iZapotec, iPurepecha),
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
	(iInuit, iRussia),
	(iInuit, iAmerica),
	(iInuit, iCanada),
	(iInca, iArgentina),
	(iInca, iColombia),
	(iInca, iBrazil),
	(iInca, iPeru),
	(iPurepecha, iMexico),
	(iPurepecha, iAmerica),
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
	(iAmerica, iHaiti),
	(iArgentina, iBrazil),
	(iColombia, iVenezuela),
	(iVenezuela, iBrazil),
	(iMexico, iColombia),
]

lInfluences = [
	(iWari, iTiwanaku),
	(iChimu, iTiwanaku),
	(iInca, iTiwanaku),
	(iAztecs, iTeotihuacan),
	(iAztecs, iZapotec),
	(iNetherlands, iSpain),
	(iAmerica, iEngland),
	(iAmerica, iFrance),
	(iAmerica, iNetherlands),
	(iAmerica, iNorse),
	(iHaiti, iFrance),
	(iArgentina, iSpain),
	(iMexico, iSpain),
	(iMexico, iFrance),
	(iMexico, iTeotihuacan),
	(iMexico, iMaya),
	(iMexico, iAztecs),
	(iMexico, iZapotec),
	(iMexico, iPurepecha),
	(iColombia, iSpain),
	(iColombia, iMuisca),
	(iPeru, iSpain),
	(iPeru, iTiwanaku),
	(iVenezuela, iSpain),
	(iBrazil, iPortugal),
	(iCanada, iFrance),
	(iCanada, iEngland),
]

dBirth = CivDict({
iMaya : 0,
iTeotihuacan : 0,
iZapotec : 0,
iTiwanaku : 110,
iWari : 500,
iMississippi : 600,
iPuebloan : 750,
iMuisca : 800,
iNorse : 874,
iChimu : 900,
iInuit : 1050,
iInca : 1100,
iPurepecha : 1150,
iAztecs : 1250,
iIroquois : 1350,
iSpain : 1496,
iPortugal : 1532,
iEngland : 1607,
iFrance : 1608,
iNetherlands : 1625,
iHawaii : 1650,
iRussia: 1743,
iAmerica : 1775,
iHaiti : 1804,
iArgentina : 1810,
iMexico : 1810,
iColombia : 1810,
iPeru : 1822,
iBrazil : 1822,
iVenezuela : 1831,
iCanada : 1867,
}, 0)

lBirthCivs = dBirth.keys()

dFall = CivDict({
iMaya : 1350,
iTeotihuacan : 1400,
iZapotec : 1550,
iTiwanaku : 1400,
iWari : 1400,
iMississippi : 1350,
iPuebloan : 1700,
iMuisca : 1600,
iChimu : 1600,
iInuit : 1750,
iInca : 1600,
iPurepecha : 1600,
iAztecs : 1600,
iIroquois : 1800,
iSpain : 1850,
iPortugal : 1850,
iFrance : 1850,
}, 2000)

# Leoreth: determine neighbour lists from pairwise neighbours for easier lookup
dNeighbours = dictFromEdges(lBirthCivs, lNeighbours)

# Leoreth: determine influence lists from pairwise influences for easier lookup
dInfluences = dictFromEdges(lBirthCivs, lInfluences)

dResurrections = CivDict({
}, [])

dEnemyCivsOnSpawn = CivDict({
iAztecs : [iTeotihuacan],
iInca : [iTiwanaku, iWari],
iAmerica : [iEngland, iIroquois, iIndependent, iIndependent2, iNative],
iHaiti : [iFrance],
iArgentina : [iSpain, iIndependent, iIndependent2],
iMexico : [iSpain, iIndependent, iIndependent2],
iColombia : [iSpain, iIndependent, iIndependent2],
iPeru : [iSpain, iIndependent, iIndependent2],
iBrazil : [iIndependent, iIndependent2],
iVenezuela : [iColombia],
}, [])

dTotalWarOnSpawn = CivDict({
iInca : [iWari, iTiwanaku],
iAztecs : [iTeotihuacan],
}, [])

dAggressionLevel = CivDict({
iMaya : 1,
iTeotihuacan : 2,
iZapotec : 1,
iTiwanaku : 1,
iWari : 1,
iMississippi : 1,
iPuebloan : 1,
iMuisca : 1,
iNorse : 1,
iChimu : 1,
iInuit : 1,
iInca : 3,
iPurepecha : 2,
iAztecs : 3,
iIroquois : 2,
iSpain : 3,
iEngland : 2,
iFrance : 2,
iNetherlands : 2,
iHawaii : 1,
iRussia : 2,
iAmerica : 3,
iHaiti : 1,
iArgentina : 2,
iMexico : 2,
iColombia : 3,
iPeru : 1,
iBrazil : 2,
iVenezuela : 1,
iCanada : 1,
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
iZapotec : 20,
iTiwanaku : 20,
iWari : 20,
iMississippi : 35,
iPuebloan : 35,
iMuisca : 35,
iNorse : 30,
iChimu : 20,
iInuit : 35,
iInca : 35,
iPurepecha : 20,
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
iArgentina : 40,
iMexico : 40,
iColombia : 30,
iPeru : 35,
iBrazil : 40,
iVenezuela : 20,
iCanada : 40,
}, 100)

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
(iAngakkuq, 	iAsatru, 		iAtua, 			iDruidism, 		iGaiwiio,		iInti, 			iKachina,		iMidewiwin, 	iRodnovery, 	iTeotlMaya, 
iTeotlAztec, 	iYoruba) = range(iNumPaganReligions)

iPaganVictory = iNumReligions
iSecularVictory = iNumReligions + 1

# corporations
iNumCorporations = 8
(iFurTrade, iTradingCompany, iCerealIndustry, iFishingIndustry, iTextileIndustry, iSteelIndustry, iOilIndustry, iLuxuryIndustry) = range(iNumCorporations)

# initialise tech variables to unit indices from XML

iNumTechs = 133
#				2				3				4				5				6				7
(iHunting,		iLandmarks,		iIrrigation,	iLinguistics,	iCultivation,	iSpiritualism,	iShallowFishing,
iTrapping,      iPathfinding,   iEarthworks,    iLocalization,  iCompanionPlanting,iHerbalism,  iFishing,
iTanning, 		iMining, 		iPottery, 		iAgriculture, 	iPastoralism, 	iMythology, 	iSailing,
iSmelting,      iMasonry,       iProperty,      iArithmetics,   iCeremony,      iDivination,    iSeafaring,
iAlloys,        iConstruction,  iMathematics,   iAstronomy,     iWriting,       iCalendar,      iTrade,
iGeneralship,   iCement,        iAesthetics,    iScholarship,   iCodices,       iPriesthood,    iNavigation,
iNobility,      iEmpire,        iArtisanry,     iMedicine,      iLaw,           iEthics,        iPhilosophy,
iOldWorldTactics,iOldWorldScience,iOldWorldCulture,
iGunpowder, 	iCompanies, 	iFinance, 		iCartography, 	iHumanities, 	iPrinting, 		iJudiciary,
iFirearms, 		iLogistics, 	iExploration, 	iOptics, 		iDiplomacy, 	iEvangelism, 	iOfficials,
iFortification,	iEconomics, 	iColonization, 	iShipbuilding, 	iCharter, 		iCommunity, 	iIndentures,
iCombinedArms, 	iTriangularTrade, iExploitation, iTimekeeping, 	iEducation, 	iPolitics, 		iHorticulture,
iTactics,		iCurrency,		iGeography,		iAcademia,		iUrbanPlanning,	iStatecraft,	iSocialContract,
iReplaceableParts, iFreeMarket,	iNewspapers,	iScientificMethod, iArchitecture, iSociology,	iHeritage,
iRegiments, 	iBonds,			iPostalService,	iMeteorology,	iSurveying,		iRepresentation, iIndependence,
iMetallurgy,	iProtectionism,	iHydrology,		iPhysics,		iGeology,		iRightsOfMan,	iFederalism,
iMachineTools, 	iThermodynamics, iEngineeing, 	iChemistry, 	iPioneering,	iCivilLiberties, iNationalism,
iMeasurement, 	iEngine, 		iRailroad, 		iElectricity, 	iConservation, 	iEmancipation, 	iImperialism,
iBallistics,	iAssemblyLine,	iCombustion,	iTelegraph,		iBiology,		iLaborUnions,	iJournalism,
iInfrastructure,iMacroeconomics,iCivilRights,
iPowerProjection) = range(iNumTechs)

# Techs that Natives start the game with, but Europeans have to trade for
lNativeTechs = [iHunting, iLandmarks, iIrrigation, iLinguistics, iCultivation, iSpiritualism, iShallowFishing,
                iTrapping, iPathfinding, iEarthworks, iLocalization, iCompanionPlanting, iHerbalism, iFishing]

# initialise unit variables to unit indices from XML

iNumUnits = 128
#				2				3				4				5				6				7				8				9				10
(iBear, 		iPanther, 		iWolf, 			iSettler, 		iDogSled,		iPioneer,		iWorker, 		iArtisan,		iPromyshlenniki,iLaborer, 		
iMadeireiro, 	iColonist,		iScout, 		iPathfinder,	iExplorer, 		iBandeirante, 	iCoureurDesBois,iRanger,		iSpy, 			iSisqeno,       
iAgent,			iInquisitor,	iOrthodoxMiss, 	iCatholicMiss, 	iProtestantMiss, iMilitia1,		iFalconDancer,	iMilitia2,		iMilitia3,		iMilitia4,		
iMinuteman,		iMilitia5,		iWarrior, 		iKoa,			iArquebusier,	iArmedBrave,	iArmedSlave,	iMusketman,		iMusketeer,		iGuardia,		
iRifleman,		iVencedores,	iAxeman,		iAucac,			iDogSoldier,	iJaguar,		iMacana,		iTercio,		iMohawk,		iFusilier,		
iCompagnies,	iLineInfantry,	iRedcoat,		iMarine,		iSpearman,		iSuchucChiqui,	iLightningWarrior,iPikeman,		iArcher,		iPicta,			
iSlinger,		iCrossbowman,	iLightCannon,	iFieldGun,		iGatlingGun,	iAtlatlist,		iHolkan,		iGuecha,		iSkirmisher,	iGrenadier,		
iCacos,			iAlbionLegion,	iHorseArcher,	iHussar,		iMountedBrave,	iDragoon,		iLlanero,		iPistolier,		iRural,			iCuirassier,	
iConquistador,	iCarabineer,	iGrenadierCavalry,iCavalry,		iBombard,		iCannon,		iArtillery,		iHowitzer,		iWorkboat,		iCanoe,			
iLongship,		iWaaKaulua,		iCaravel,		iCarrack,		iIndiaman,		iGalleon,       iFluyt,			iBrigantine,	iSteamship,		iSloop,			
iFrigate,		iIronclad,		iPrivateer,	    iTorpedoBoat,	iBarque,		iShipOfTheLine,iManOfWar,		iCruiser,		iGreatProphet, 	iGreatArtist, 	
iGreatScientist,iGreatMerchant, iGreatEngineer, iGreatStatesman,iGreatGeneral,	iArgentineGreatGeneral,iGreatSpy,iFeGreatProphet,iFeGreatArtist,iFeGreatScientist,
iFeGreatMerchant,iFeGreatEngineer,iFeGreatStatesman,iFeGreatGeneral,iFeGreatSpy, iAfricanSlave,  iNativeSlave, 	iMigrantWorker) = range(iNumUnits)

lGreatPeopleUnits = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman]

lWildernessRPGunUnits = [iMilitia3, iMilitia4, iMinuteman, iMilitia5, iArquebusier, iArmedSlave, iMusketman, iMusketeer, iGuardia, iRifleman, iVencedores, iTercio, iMohawk, iFusilier, iCompagnies, iLineInfantry, iRedcoat, iMarine]
lWildernessRPHorseUnits = [iHorseArcher, iCuirassier, iConquistador]
lWildernessRPHorseGunUnits = [iHussar, iMountedBrave, iDragoon, iLlanero, iPistolier, iRural, iCarabineer, iGrenadierCavalry, iCavalry]

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

iNumUnitRoles = 24
#				2				3				4				5				6				7				8				9				10
(iSettle,		iWork,			iRecon,			iMissionary,	iDefend,		iBase,			iShock,			iCounter,		iSiege,			iHarass,
iHarassCav,		iShockCav,		iSiegeCity,		iWorkSea,		iFerrySea,		iEscortSea,		iHarassSea,		iCapitalSea,	iColonistSettle,iColonistSupport, 
iColonistExplore, iColonistConquer, iColonistDefend, iColonistSlave) = range(iNumUnitRoles)

lColonistRoles = [iColonistSettle, iColonistSupport, iColonistExplore, iColonistConquer, iColonistDefend, iColonistSlave]

# initialise bonuses variables to bonuses IDs from WBS
iNumBonuses = 50
#				2				3				4				5				6				7				8				9				10
(iAluminium, 	iCitrus,		iCoal, 			iCopper, 		iHorse, 		iIron, 			iMarble, 		iOil, 			iStone, 		iUranium, 		
iBanana, 		iClam, 			iCorn, 			iCow, 			iCrab,			iCrustaceans,	iDeer, 			iFish, 			iPig, 			iPotato,		
iRice, 			iSheep, 		iLlama,			iWheat, 		iCocoa,			iCoffee, 		iCotton,		iDye, 			iFur,			iGems, 			
iGold, 			iIncense, 		iIvory, 		iJade,			iObsidian,		iPearls, 		iRubber,		iSalt,			iSilk, 			iSilver, 		
iSpices,		iSugar,			iTea, 			iTimber,		iTobacco, 		iWine, 			iWhales, 		iSoccer, 		iSongs, 		iMovies) = range(iNumBonuses)

# Buildings
iNumBuildings = 191
# Buildings (97)
#				2				3				4				5				6				7				8				9				10
(iPalace, 		iChieftansHut,	iGovernorsMansion,iCapitol,		iGranary,		iChinampa,		iColcas,		iIgloo,			iBath,			iTemazcal,		
iMarket,		iWeaver,		iStoneworks,	iGoldsmith,		iArena,			iBallCourt,		iBarracks,		iKallanka,		iWalls,			iKancha,		
iTambo,			iHerbalist,		iAltar,			iTomb,			iTzompantli,	iYacatas,		iCommon,		iPlatformMound,	iKalasasay,		iKiva,			
iLonghouse,		iPaganTemple,	iHarbor,		iSmokehouse,	iLuau,			iStocks,		iTradingPost,	iHuntingPost,	iTradingFort,	iForge,			
iStable,		iPalisade,		iMonument,		iSchoolhouse,	iWell,			iConstabulary,	iRoyalMountedPolice,iSlaveMarket,iWharf,		iLighthouse,	
iWarehouse,		iLumbermill,	iSawmill,		iTavern,		iStarFort,		iCitadelle,		iEstate,		iFazenda,		iHacienda,		iUniversity,	
iPharmacy,		iDistillery,	iCourthouse,	iAssembly,		iThingvellir,	iWheelwright,	iPostOffice,	iCustomsHouse,	iFeitoria,		iBank,			
iLevee,			iSeigneur,		iTheatre,		iSilversmith,	iMagazine,		iShipyard,		iObservatory,	iPrintingPress,	iMeetingHall,	iStateHouse,	
iSlaughterhouse,iColdStoragePlant,iSewer,		iJail,			iImmigrationOffice,iRailwayStation,iTextileMill,iWoolMill,		iSteelMill,		iRefinery,      
iCoalPlant,     iRodeo,			iCharreada,		iArsenal,		iDrydock,		iLibrary,		iNewspaper,				
# Religious Buildings (41)
#				2				3				4				5				6				7				8				9				10
iJewishTemple, iJewishCathedral, iJewishMonastery, iJewishShrine, iOrthodoxTemple, iOrthodoxCathedral, iOrthodoxMonastery, iOrthodoxShrine, iCatholicTemple, iCatholicCathedral, 
iCatholicMonastery, iMission,	iCatholicShrine, iProtestantTemple, iProtestantCathedral, iProtestantMonastery, iProtestantShrine, iIslamicTemple, iIslamicCathedral, iIslamicMonastery, 
iIslamicShrine, iHinduTemple, iHinduCathedral, iHinduMonastery, iHinduShrine, iBuddhistTemple, iBuddhistCathedral, iBuddhistMonastery, iBuddhistShrine, iConfucianTemple, 
iConfucianCathedral, iConfucianMonastery, iConfucianShrine, iTaoistTemple, iTaoistCathedral, iTaoistMonastery, iTaoistShrine, iZoroastrianTemple, iZoroastrianCathedral, iZoroastrianMonastery, 
iZoroastrianShrine, 
# Great Buildings (6)
#				2				3				4				5				6				7				8				9				10
iAcademy, 		iAdministrativeCenter, iManufactory, iArmoury, 	iMuseum, 		iStockExchange, 
# Great Buildings/National Wonders (14)
#				2				3				4				5				6				7				8				9				10
iTradingCompanyBuilding,iNationalMonument,iNationalTheatre,iNationalGallery,iNationalCollege,iMilitaryAcademy,iSecretService,iIronworks,iRedCross,iNationalPark,
iCentralBank, 	iGrandCentralStation,iSupremeCourt,
# Great Wonders (34)
#				2				3				4				5				6				7				8				9				10
iFloatingGardens,iTempleOfKukulkan,iMachuPicchu,iSacsayhuaman,	iHueyTeocalli,	iTlachihualtepetl,iGateOfTheSun,iPyramidOfTheSun,iSerpentMound,	iTemblequeAqueduct,
iLaFortaleza,	iSaoFranciscoSquare,iGuadalupeBasilica,iManzanaJesuitica,iIndendenceHall,iHospicioCabanas,iMountVernon,iMonticello,iSlaterMill,iChapultepecCastle,
iWestPoint,		iFortMcHenry,	iWashingtonMonument,iFaneuilHall,iStatueOfLiberty,iCentralPark,	iEllisIsland,	iBrooklynBridge,iChateauFrontenac,iMenloPark,
iBiltmoreEstate,iFrenchQuarter, iLeagueOfNations,iCristoRedentor) = range(iNumBuildings)

iBeginWonders = iFloatingGardens # different from DLL constant because that includes national wonders

iTemple = iJewishTemple #generic
iCathedral = iJewishCathedral #generic
iMonastery = iJewishMonastery #generic
iShrine = iJewishShrine #generic

iFirstWonder = iFloatingGardens

iPlague = iNumBuildings
iNumBuildingsPlague = iNumBuildings+1

#Civics
iNumCivics = 63
(iChiefdom, iExpedition, iDespotism, iViceroyalty, iCouncil, iCharterColony, iMonarchy, iTradeCompany, iDemocracy, iRoyalColony, iDictatorship, iDominion, iStateParty, iCommonwealth,
iAuthority, iCustomaryLaw, iMaritimeLaw, iAristocracy, iCommonLaw, iConfederacy, iProprietaries, iFederalism, iGovernors, iSpoilsSystem, iColonialAssembly, iPoliceState, iProvinces,
iTraditionalism, iSerfdom, iCaptives, iEncomienda, iCraftsmen, iIndenturedServitude, iSlavery, iIndustrialism, iImmigrantLabor, iLaborUnions,
iReciprocity, iMerchantTrade, iMercantilism, iAgrarianism, iFreeEnterprise, iConsumerism, iPublicWelfare,
iAnimism, iDivineRight, iHarmony, iGloriaInDeo, iCasteSystem, iJesuits, iIsolationism, iHaven, iProfiteering, iOpportunity, iMulticulturalism,
iSovereignty, iTributaries, iConquest, iOutposts, iHomesteads, iDecolonization, iIntervention, iNationhood) = range(iNumCivics)

iNumCivicCategories = 6
(iCivicsGovernment, iCivicsLegitimacy, iCivicsSociety, iCivicsEconomy, iCivicsReligion, iCivicsTerritory) = range(iNumCivicCategories)

lCivicCountInCategory = [14, 13, 10, 7, 11, 8];
lCivicDefaultsInCateogry = [2, 1, 2, 1, 2, 1];


#Specialists
iNumSpecialists = 16
#				            2				            3				            4				            5
(iSpecialistCitizen,        iSpecialistPriest,          iSpecialistArtist,          iSpecialistScientist,       iSpecialistMerchant,
iSpecialistEngineer,        iSpecialistStatesman,       iSpecialistGreatProphet,    iSpecialistGreatArtist,     iSpecialistGreatScientist, 
iSpecialistGreatMerchant,   iSpecialistGreatEngineer,   iSpecialistGreatStatesman,  iSpecialistGreatGeneral,    iSpecialistGreatSpy,
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
(iParameterCorePeriphery, iParameterAdministration, iParameterSeparatism, iParameterRecentExpansion, iParameterRazedCities, iParameterIsolationism,	iParameterMotherland, # Expansion
iParameterEconomicGrowth, iParameterTrade, iParameterMercantilism, iParameterCentralPlanning,								# Economy
iParameterHappiness, iParameterCivicCombinations, iParameterCivicsEraTech, iParameterReligion,								# Domestic
iParameterVassals, iParameterDefensivePacts, iParameterRelations, iParameterNationhood, iParameterMultilateralism,			# Foreign
iParameterWarSuccess, iParameterWarWeariness, iParameterBarbarianLosses) = range(iNumStabilityParameters)						# Military

#Regions
iNumRegions = 52
#				2				3				4				5				6				7				8				9				10
(rAlaska, 		rYukon,         rNunavut, 		rGreenland,     rIceland,       rNorthCascadia, rNorthPlains, 	rOntario, 		rQuebec, 		rNewFoundland, 	
rSouthCascadia, rCalifornia,    rRockies,       rSouthwest,     rTexas,         rGreatPlains,   rGreatLakes,    rNewEngland,    rMidAtlantic,   rMaryland,
rRiverValley,    rCoastalPlain,  rDeepSouth,     rFlorida,       rBajaCalifornia,rSierraMadres,  rBajio,         rVeracruz,      rOaxaca,        rYucatan,       
rMesoamerica,   rCaribbean, 	rHawaii, 		rColombia, 		rVenezuela, 	rGuyana, 		rPeru, 			rBolivia, 		rAmazonas, 		rPara,          
rBahia,         rMinasGerais,   rMatoGrosso,    rParana,        rChile, 		rParaguay, 		rUruguay, 		rChaco,         rCuyo,          rPampas, 		
rPatagonia, 	rOldWorld		) = range(iNumRegions)

lCanada = [rYukon, rNunavut, rNorthCascadia, rNorthPlains, rOntario, rQuebec, rNewFoundland]
lThirteenColonies = [rNewEngland, rMidAtlantic, rMaryland, rCoastalPlain]
lSouthernUS = [rCoastalPlain, rFlorida, rTexas, rDeepSouth]
lBorderStates = [rMaryland, rRiverValley]
lContinentalUS = [rSouthCascadia, rCalifornia, rRockies, rSouthwest, rTexas, rGreatPlains, rGreatLakes, rNewEngland, rMidAtlantic, rMaryland, rRiverValley, rCoastalPlain, rDeepSouth, rFlorida]
lUnitedStates = lContinentalUS + [rAlaska, rHawaii]
lMexico = [rBajaCalifornia, rSierraMadres, rBajio, rVeracruz, rOaxaca, rYucatan]
lBrazil = [rAmazonas, rPara, rBahia, rMinasGerais, rMatoGrosso, rParana,]
lArgentina = [rChaco, rCuyo, rPampas, rPatagonia]

lSouthAmerica = [rColombia, rVenezuela, rGuyana, rPeru, rBolivia, rChile, rParaguay, rUruguay] + lArgentina + lBrazil
lCentralAmerica = [rMesoamerica, rCaribbean]
lLatinAmerica = lCentralAmerica + lMexico + lSouthAmerica
lNorthAmerica = lCanada + lContinentalUS + [rAlaska] + lMexico 

lAmerica = lSouthAmerica + lCentralAmerica + lNorthAmerica
lWest = lAmerica + [rHawaii, rGreenland]

#Projects

iNumProjects = 1
(iWorldsFair) = range(iNumProjects)

#Eras

iNumEras = 6
(iAncientEra, iClassicalEra, iExplorationEra, iColonialEra, iRevolutionaryEra, iIndustrialEra) = range (iNumEras)

# Culture

iNumCultureLevels = 7
(iCultureLevelNone, iCultureLevelPoor, iCultureLevelFledgling, iCultureLevelDeveloping, iCultureLevelRefined, iCultureLevelInfluential, iCultureLevelLegendary) = range(iNumCultureLevels)


#Improvements

iNumImprovements = 30
#				2				3				4				5				6				7				8				9				10
(iLandWorked, 	iWaterWorked, 	iCityRuins, 	iFarm, 			iPaddyField, 	iFishingBoats, 	iOceanFishery, 	iWhalingBoats, 	iMine, 			iWorkshop, 
iLoggingCamp, 	iWindmill, 		iWatermill, 	iPlantation, 	iSlavePlantation, iQuarry, 		iPasture, 		iCamp, 			iWell, 			iOffshorePlatform, 
iWinery, 		iCottage, 		iHamlet, 		iVillage, 		iTown, 			iFort, 			iForestPreserve, iMarinePreserve, iTribe,       iContactedTribe) = range(iNumImprovements)

iNumRoutes = 3
(iRouteRoad, iRouteRailroad, iRouteHighway) = range(iNumRoutes)

#feature & terrain

iNumFeatures = 13
#				2				3				4				5				6				7				8				9				10
(iSeaIce, 		iJungle, 		iCenote, 		iFloodPlains, 	iForest, 		iBog, 			iSwamp, 		iCape, 			iIslands, 		iRainforest, 
iFallout, 		iTaiga, 		iPalmForest) = range(iNumFeatures)

iNumTerrains = 20
#				2				3				4				5				6				7				8				9				10
(iGrass, 		iPlains, 		iDesert, 		iTundra, 		iSnow, 			iCoast, 		iOcean, 		iTerrainPeak, 	iTerrainHills, 	iMarsh,
iLagoon,		iArcticCoast,	iSemidesert,	iPrairie,		iMoorland,		iSaltflat,		iSaltlake,		iAtoll,			iSavanna,		iWideRiver,) = range(iNumTerrains)


#Plague
iImmunity = 20

# Victory
iVictoryPaganism = 10
iVictorySecularism = 11


#leaders
iNumLeaders = 59
#				2				3				4				5				6				7				8				9				10
(iLeaderBarbarian,iSittingBull, iIndependentLeader,iWashington,	iJackson,		iLincoln,		iRoosevelt,		iFDR,			iKennedy,			iReagan,
iObama,			iSanMartin,		iPeron,			iMontezuma,		iPedro,			iVargas,		iMacDonald,		iTrudeau,		iTacaynamo,		iBolivar,
iElizabeth,		iVictoria,		iChurchill,		iLouis,			iNapoleon,		iDeGaulle,		iLOuverture,	iKamehameha,	iHuaynaCapac,	iPachacuti,		
iAua,			iHiawatha,		iPacal,			iJuarez,		iSantaAnna,		iCardenas,		iRedHorn,		iSaguamanchica,	iWillemVanOranje,iWilliam,		
iRagnar,		iGustav,		iGerhardsen,	iCastilla,		iJoao,			iMaria,			iItzukuma,		iCatherine,		iAlexanderI,	iStalin,		
iIsabella,		iPhilip,		iFranco,		iAtlatlCauac,	iMalkuHuyustus,	iChavez,		iWariCapac,		iCosijoeza,		iTariacuri) = range(iNumLeaders)

dResurrectionLeaders = CivDict({
})

iNumPeriods = 0
#() = range(iNumPeriods)

iNumImpacts = 5
(iImpactMarginal, iImpactLimited, iImpactSignificant, iImpactCritical, iImpactPlayer) = range(iNumImpacts)

lSecondaryCivs = [iChimu, iHaiti, iHawaii, iInuit, iIroquois, iMississippi, iMuisca, iNorse, iPeru, iPuebloan, iVenezuela, iWari]

(i0AD, i1500AD, i1750AD) = range(3)

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

# Immigration
iNumImmigrantCategories = 12
#				2				3				4				5				6				7				8				9				10
(iSettlersCat,	iWorkersCat,	iMissionariesCat,iTransportsCat,iGreatPeopleCat,iSlavesCat,		iColonistsCat,	iMigrantWorkerCat,iExplorersCat,iMilitiaCat,	
iMainlineCat,	iSpecialtyCat) = range(iNumImmigrantCategories)

lSettlers = [iSettler, iPioneer]
lWorkers = [iWorker, iPromyshlenniki, iLaborer, iMadeireiro]
lMissionaries = [iOrthodoxMiss, iCatholicMiss, iProtestantMiss]
lTransports = [iLongship, iCaravel, iCarrack, iIndiaman, iGalleon, iFluyt, iBrigantine, iSteamship]
lGreatPeople = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral]
lSlaves = [iAfricanSlave]
lColonists = [iColonist]
lMigrantWorkers = [iMigrantWorker]
lExplorers = [iExplorer, iBandeirante, iCoureurDesBois, iRanger]
lMilitia = [iMilitia2, iMilitia3, iMilitia4, iMilitia5]
lMainlineUnits = [iArquebusier, iMusketman, iMusketeer, iRifleman]
lSpecialtyUnits = [iTercio, iFusilier, iCompagnies, iLineInfantry, iRedcoat, iMarine, iCrossbowman, iLightCannon, iFieldGun, iGatlingGun, iSkirmisher, iGrenadier, iHussar, iDragoon, iPistolier, iCuirassier, iConquistador, iCarabineer, iCavalry, iBombard, iCannon, iArtillery, iHowitzer, iSloop, iFrigate, iIronclad, iPrivateer, iTorpedoBoat, iBarque, iShipOfTheLine, iManOfWar, iCruiser]

lPossibleColonists = [lSettlers, lWorkers, lMissionaries, lTransports, lGreatPeople, lSlaves, lColonists, lMigrantWorkers]

lPossibleExpeditionaries = [lExplorers, lMilitia, lMainlineUnits, lSpecialtyUnits]

lPossibleImmigrants = lPossibleColonists + lPossibleExpeditionaries

# A goal number of cities for an AI to build, used in Immigration Manager
dNumCitiesGoal = CivDict({
iMaya : 3,
iTeotihuacan : 2,
iZapotec : 1,
iTiwanaku : 2,
iWari : 3,
iMississippi : 5,
iPuebloan : 3,
iMuisca : 2,
iNorse : 4,
iChimu : 2,
iInuit : 8,
iInca : 10,
iPurepecha : 3,
iAztecs : 5,
iIroquois : 5,
iSpain : 30,
iPortugal : 20,
iEngland : 15,
iFrance : 10,
iNetherlands : 5,
iHawaii : 3,
iRussia: 5,
iAmerica : 30,
iHaiti : 2,
iArgentina : 10,
iMexico : 10,
iColombia : 5,
iPeru : 5,
iBrazil : 20,
iVenezuela : 5,
iCanada : 10,
}, 0)