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
iNumCivs = 36
#				2				3				4				5				6				7				8				9				10
(iAmerica, 		iArgentina, 	iAztecs, 		iBrazil, 		iCanada, 		iChimu,			iColombia, 		iCuba,			iEngland, 		iFrance, 		
iHaiti,			iHawaii,		iInca,			iInuit,			iIroquois,		iMaya,			iMexico, 		iMississippi,	iMuisca,		iNetherlands, 	
iNorse,			iPeru,			iPortugal, 		iPuebloan,		iRussia,		iSpain, 		iTeotihuacan,	iTiwanaku,		iVenezuela,		iWari,			
iIndependent, 	iIndependent2, 	iIndependent3,	iNative,		iMinor, 		iBarbarian) = tuple(Civ(i) for i in range(iNumCivs))

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
	iArgentina,
	iMexico,
	iColombia,
	iPeru,
	iBrazil,
	iVenezuela,
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
iCivGroupAmerica : [iAmerica, iArgentina, iMexico, iColombia, iBrazil, iCanada, iHaiti, iPeru, iVenezuela, iCuba]
}

# used in: Stability
# tech groups share techs within each other on respawn
iNumTechGroups = 3
(iTechGroupWestern, iTechGroupLatinAmerica, iTechGroupNativeAmerica) = range(iNumTechGroups)

dTechGroups = {
iTechGroupWestern : [iNorse, iSpain, iFrance, iEngland, iNetherlands, iPortugal, iRussia, iAmerica, iCanada],
iTechGroupLatinAmerica: [iArgentina, iMexico, iColombia, iBrazil, iHaiti, iPeru, iVenezuela, iCuba],
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
	(iInuit, iRussia),
	(iInuit, iAmerica),
	(iInuit, iCanada),
	(iInca, iArgentina),
	(iInca, iColombia),
	(iInca, iBrazil),
	(iInca, iPeru),
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
	(iColombia, iSpain),
	(iColombia, iMuisca),
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
iArgentina : 1810,
iMexico : 1810,
iColombia : 1810,
iPeru : 1822,
iBrazil : 1822,
iVenezuela : 1831,
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
iPuebloan : 1650,
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
iArgentina : 1,
iMexico : 1,
iColombia : 2,
iPeru : 1,
iBrazil : 2,
iVenezuela : 1,
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
iArgentina : 40,
iMexico : 40,
iColombia : 30,
iPeru : 35,
iBrazil : 40,
iVenezuela : 20,
iCanada : 40,
iCuba : 25,
}, 100)

# Colonists - European Regional Power
dColonistSpawnPoints = CivDict({
iNorse : [(78, 103)],
iSpain : [(65, 64), (65, 64), (65, 64)],
iPortugal : [(79, 35), (79, 35)],
iEngland : [(61, 76), (66, 81), (73, 86)], 
iFrance : [(75, 86), (75, 86), (40, 66)],
iNetherlands : [(63, 78), (66, 59)],
iRussia : [(12, 94)],
})

# Only need to specify colonists past the first given, since the first is given on initial spawn
dColonistSpawnDates = CivDict({
iSpain : [1525, 1575],
iPortugal : [1550],
iEngland : [1620, 1650],
iFrance : [1650, 1718],
iNetherlands : [1650],
})

iNumExpeditionTypes = 8
(iCanoeSettle, iCaravelSettle, iCaravelSupport, iCaravelExplore, iCaravelConquer, iGalleonSettle, iGalleonSupport, iGalleonConquer) = range(iNumExpeditionTypes)

dColonistExpeditions = CivDict({
iNorse : [[iCanoeSettle]],
iSpain : [[iCaravelSettle, iCaravelSupport, iCaravelExplore], [iCaravelSettle, iCaravelConquer], [iGalleonSettle, iGalleonConquer]],
iPortugal : [[iCaravelSettle, iCaravelSupport], [iCaravelSettle, iCaravelSupport]],
iEngland : [[iGalleonSettle, iGalleonSupport], [iGalleonSettle], [iGalleonSettle]],
iFrance : [[iGalleonSettle, iGalleonSupport], [iGalleonSettle], [iGalleonSettle]],
iNetherlands : [[iGalleonSettle, iGalleonSupport], [iGalleonSettle]],
iRussia : [[iGalleonSettle, iGalleonSupport]],
})

dMaxColonists = CivDict({
iNorse : len(dColonistExpeditions[iNorse]),
iSpain : len(dColonistExpeditions[iSpain]),
iPortugal : len(dColonistExpeditions[iPortugal]),
iEngland : len(dColonistExpeditions[iEngland]), 
iFrance : len(dColonistExpeditions[iFrance]),
iNetherlands : len(dColonistExpeditions[iNetherlands]),
iRussia : len(dColonistExpeditions[iRussia]),
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

iNumTechs = 152
#				2				3				4				5				6				7
(iHunting,		iLandmarks,		iLinguistics,	iPathfinding,	iCultivation,	iHerbalism,		iFishing,
iTanning, 		iMining, 		iPottery, 		iPastoralism, 	iAgriculture, 	iMythology, 	iSailing,
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
iMetallurgy,	iProtectionism,	iHydrology,		iPhysics,		iGeology,		iRightsOfMan,	iFederalism,
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

# Techs that Natives start the game with, but Europeans have to trade for
lNativeTechs = (iHunting, iLandmarks, iLinguistics, iPathfinding, iCultivation, iHerbalism, iFishing)

# initialise unit variables to unit indices from XML

iNumUnits = 154
#				2				3				4				5				6				7				8				9				10
(iBear, 		iPanther, 		iWolf, 			iSettler, 		iDogSled,		iPioneer,		iWorker, 		iArtisan,		iPromyshlenniki,
iLaborer, 		iMadeireiro, 	iScout, 		iExplorer, 		iBandeirante, 	iCoureurDesBois,iRanger,		iParatrooper,	iSpy, 			iSisqeno,
iAgent,			iInquisitor,	iOrthodoxMiss, 	iCatholicMiss, 	iProtestantMiss, iMilitia1,		iFalconDancer,	iMilitia2,		iMilitia3,		iMilitia4,		
iMinuteman,		iMilitia5,		iMilitia6,		iMilitia7,		iWarrior, 		iArquebusier,	iArmedBrave,	iArmedSlave,	iMusketman,		iMusketeer,		
iRifleman,		iInfantry,		iMechInfantry,	iAxeman,		iAucac,			iDogSoldier,	iJaguar,		iTercio,		iMohawk,		iFusilier,		
iCompagnies,	iLineInfantry,	iRedcoat,		iMarine,		iSpearman,		iSuchucChiqui,	iPikeman,		iAntiTank,		iRPG,			iArcher,		
iPicta,			iSlinger,		iCrossbowman,	iLightCannon,	iFieldGun,		iGattlingGun,	iMachineGun,	iAtlatlist,		iHolkan,		iGuecha,		
iSkirmisher,	iGrenadier,		iAlbionLegion,	iGuerilla,		iHorseArcher,	iHussar,		iMountedBrave,	iDragoon,		iLlanero,		iPistolier,		
iLightTank,		iGunship,		iCuirassier,	iConquistador,	iCarabineer,	iGrenadierCavalry,iCavalry,		iRural,			iTank,			iMainBattleTank,
iBombard,		iCannon,		iHeavyCannon,	iRifledCannon,	iArtillery,		iHowitzer,		iAAGun,			iMobileSAM,		iWorkboat,		iCanoe,			
iLongship,		iWaaKaulua,		iCaravel,		iCarrack,		iGalleon,		iWestIndianman,	iBrigantine,	iSteamship,		iTransport,		iCarrier,		
iSloop,			iFrigate,		iIronclad,		iDestroyer,		iCorvette,		iStealthDestroyer,iPrivateer,	iTorpedoBoat,	iSubmarine,		iNuclearSubmarine,
iBarque,		iShipOfTheLine,iManOfWar,		iCruiser,		iBattleship,	iMissileCruiser,iBiplane,		iFighter,		iJetFighter,	iDrone,			
iBomber,		iStealthBomber,	iNuclearBomber,	iGuidedMissile,	iICBM,			iSatellite,		iGreatProphet, 	iGreatArtist, 	iGreatScientist,iGreatMerchant, 
iGreatEngineer, iGreatStatesman,iGreatGeneral,	iArgentineGreatGeneral,iGreatSpy,iFeGreatProphet,iFeGreatArtist, iFeGreatScientist, iFeGreatMerchant, iFeGreatEngineer, 
iFeGreatStatesman,iFeGreatGeneral,iFeGreatSpy,	iSlave,			iNativeSlave) = range(iNumUnits)

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
iOil, 			iStone, 		iUranium, 		iBanana, 		iClam, 			iCorn, 			iCow, 			iCrab,			iCrustaceans,	iDeer, 
iFish, 			iPig, 			iPotato,		iRice, 			iSheep, 		iLlama,			iWheat, 		iCocoa,			iCoffee, 		iCotton,
iDye, 			iCochineal,		iFur,			iGems, 			iGold, 			iIncense, 		iIvory, 		iJade,			iMillet,		iObsidian,
iOlives,		iOpium,			iPearls, 		iRareEarths,	iRubber,		iSalt,			iSilk, 			iSilver, 		iSpices,		iSugar,
iTea, 			iTimber,		iTobacco, 		iWine, 			iWhales, 		iSoccer, 		iSongs, 		iMovies) = range(iNumBonuses)
# Buildings

iNumBuildings = 228
# Buildings (114)
#				2				3				4				5				6				7				8				9				10
(iPalace, 		iGranary,		iChinampa,		iColcas,		iIgloo,			iBath,			iTemazcal,		iMarket,		iWeaver,		iStoneworks,	
iGoldsmith,		iArena,			iBallCourt,		iBarracks,		iKallanka,		iWalls,			iKancha,		iTambo,			iHerbalist,		iAltar,	
iTzompantli,	iCommon,		iEffigyMound,	iKalasasay,		iPaganTemple,	iHarbor,		iSmokehouse,	iStocks,		iHeadright,		iTradingPost,	
iTradingFort,	iForge,			iStable,		iPalisade,		iMonument,		iSchoolhouse,	iWell,			iConstabulary,	iRoyalMountedPolice,iSlaveMarket,
iWharf,			iLighthouse,	iWarehouse,		iLumbermill,	iSawmill,		iTavern,		iStarFort,		iEstate,		iFazenda,		iHacienda,		
iUniversity,	iPharmacy,		iDistillery,	iCourthouse,	iAssembly,		iWheelwright,	iPostOffice,	iCustomsHouse,	iFeitoria,		iBank,			
iLevee,			iSeigneur,		iTheatre,		iSilversmith,	iMagazine,		iShipyard,		iObservatory,	iPrintingPress,	iMeetingHall,	iStateHouse,	
iSlaughterhouse,iSewer,			iJail,			iImmigrationOffice,iRailwayStation,iTextileMill,iSteelMill,		iRodeo,			iLienzoCharro,	iArsenal,		
iDrydock,		iLibrary,		iNewspaper,		iSupermarket,	iColdStoragePlant,iHospital,	iIntelligenceAgency,iAirport,	iHotel,			iDepartmentStore,
iMall,			iElectricalGrid,iFactory,		iCoalPlant,		iHydroPlant,	iIndustrialPark,iPark,			iBunker,		iLaboratory,	iBroadcastTower,
iVerticalFarm,	iPublicTransportation,iRecyclingCenter,iSecurityBureau,iContainerTerminal,iFiberNetwork,iLogisticsCenter,iAutomatedFactory,iNuclearPlant,iSolarPlant,	
iStadium,		iBombShelters,	iSupercomputer,	iCinema,		
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
iCentralBank, 	iSpaceport, 	iGrandCentralStation,iSupremeCourt,
# Great Wonders (53)
#				2				3				4				5				6				7				8				9				10
iFloatingGardens,iTempleOfKukulkan,iMachuPicchu,iSacsayhuaman,	iHueyTeocalli,	iTlachihualtepetl,iGateOfTheSun,iPyramidOfTheSun,iSerpentMound,	iTemblequeAqueduct,
iLaFortaleza,	iSaoFranciscoSquare,iGuadalupeBasilica,iManzanaJesuitica,iIndendenceHall,iHospicioCabanas,iMountVernon,iMonticello,iSlaterMill,iChapultepecCastle,
iWestPoint,		iFortMcHenry,	iWashingtonMonument,iFaneuilHall,iStatueOfLiberty,iCentralPark,	iEllisIsland,	iBrooklynBridge,iChateauFrontenac,iMenloPark,
iBiltmoreEstate,iFrenchQuarter,	iUnitedNations,	iEmpireStateBuilding,iGoldenGateBridge,iHooverDam,iAlcatraz,	iMountRushmore,	iHollywood,		iSaltCathedral,
iLasLajasSanctuary,iCristoRedentor,iGatewayArch,iWorldTradeCenter,iItaipuDam,	iStrip,			iPentagon,		iHubbleSpaceTelescope,iNASA,	iAreciboObservatory,
iCNTower,		iGraceland,		iCrystalCathedral) = range(iNumBuildings)

iBeginWonders = iFloatingGardens # different from DLL constant because that includes national wonders

iTemple = iJewishTemple #generic
iCathedral = iJewishCathedral #generic
iMonastery = iJewishMonastery #generic
iShrine = iJewishShrine #generic

iFirstWonder = iFloatingGardens

iPlague = iNumBuildings
iNumBuildingsPlague = iNumBuildings+1

#Civics
iNumCivics = 42
(iChiefdom, iCouncil, iDespotism, iMonarchy, iViceroyality, iSelfDetermination, iDemocracy,
iAuthority, iEmpire, iColony, iCommonLaw, iConfederacy, iFederalism, iRepublic,
iTraditionalism, iSpecialization, iSlavery, iIndenturedServitude, iIndustrialism, iMigrantWorkers, iAutomation,
iReciprocity, iMerchantTrade, iMercantilism, iAgrarianism, iFreeEnterprise, iConsumerism, iPublicWelfare,
iAnimism, iCasteSystem, iIsolationism, iHaven, iProfiteering, iOpportunity, iMulticulturalism,
iSovereignty, iTributaries, iConquest, iHomesteads, iNationhood, iPuppeteering, iMultilateralism) = range(iNumCivics)

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
(iParameterCorePeriphery, iParameterAdministration, iParameterSeparatism, iParameterRecentExpansion, iParameterRazedCities, iParameterIsolationism,	iParameterMotherland, # Expansion
iParameterEconomicGrowth, iParameterTrade, iParameterMercantilism, iParameterCentralPlanning,								# Economy
iParameterHappiness, iParameterCivicCombinations, iParameterCivicsEraTech, iParameterReligion,								# Domestic
iParameterVassals, iParameterDefensivePacts, iParameterRelations, iParameterNationhood, iParameterMultilateralism,			# Foreign
iParameterWarSuccess, iParameterWarWeariness, iParameterBarbarianLosses) = range(iNumStabilityParameters)						# Military

#Regions
iNumRegions = 37
#				2				3				4				5				6				7				8				9				10
(rAlaska, 		rNunavut, 		rNorthPlains, 	rOntario, 		rQuebec, 		rNewFoundland, 	rNewEngland, 	rMidAtlantic, 	rDeepSouth, 	rGulfCoast, 
rMidwest, 		rSouthwest, 	rGreatPlains, 	rRockies, 		rCalifornia, 	rCascadia, 		rSierraMadre, 	rBajio, 		rYucatan, 		rMesoamerica,
rCaribbean, 	rHawaii, 		rColombia, 		rVenezuela, 	rGuyana, 		rPeru, 			rBolivia, 		rAmazon, 		rBrazilianHighlands, rPantanal, 
rChile, 		rParaguay, 		rUruguay, 		rPampas, 		rPatagonia, 	rGreenland,		rOldWorld) = range(iNumRegions)

lCanada = [rNunavut, rNorthPlains, rOntario, rQuebec, rNewFoundland]
lContinentalUS = [rNewEngland, rMidAtlantic, rDeepSouth, rGulfCoast, rMidwest, rSouthwest, rGreatPlains, rRockies, rCalifornia, rCascadia]
lUnitedStates = lContinentalUS + [rAlaska, rHawaii]
lMexico = [rSierraMadre, rBajio, rYucatan]
lBrazil = [rAmazon, rBrazilianHighlands, rPantanal]
lArgentina = [rPampas, rPatagonia]

lSouthAmerica = [rColombia, rVenezuela, rGuyana, rPeru, rBolivia, rChile, rParaguay, rUruguay] + lArgentina + lBrazil
lCentralAmerica = [rMesoamerica, rCaribbean]
lLatinAmerica = lCentralAmerica + lMexico
lNorthAmerica = lCanada + lContinentalUS + [rAlaska] + lMexico 

lAmerica = lSouthAmerica + lCentralAmerica + lNorthAmerica
lWest = lAmerica + [rHawaii, rGreenland]

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

iNumImprovements = 31
#				2				3				4				5				6				7				8				9				10
(iLandWorked, 	iWaterWorked, 	iCityRuins, 	iFarm, 			iPaddyField, 	iFishingBoats, 	iOceanFishery, 	iWhalingBoats, 	iMine, 			iWorkshop, 
iLoggingCamp, 	iWindmill, 		iWatermill, 	iPlantation, 	iSlavePlantation, iQuarry, 		iPasture, 		iCamp, 			iWell, 			iOffshorePlatform, 
iWinery, 		iCottage, 		iHamlet, 		iVillage, 		iTown, 			iFort, 			iForestPreserve, iMarinePreserve, iSolarCollector, iTribe,
iContactedTribe) = range(iNumImprovements)

iNumRoutes = 4
(iRouteRoad, iRouteRailroad, iRouteIncanRoad, iRouteHighway) = range(iNumRoutes)

#feature & terrain

iNumFeatures = 13
#				2				3				4				5				6				7				8				9				10
(iSeaIce, 		iJungle, 		iOasis, 		iFloodPlains, 	iForest, 		iBog, 			iSwamp, 		iCape, 			iIslands, 		iRainforest, 
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
iNumLeaders = 58
#				2				3				4				5				6				7				8				9				10
(iLeaderBarbarian,iSittingBull, iIndependentLeader,iWashington,	iJackson,		iLincoln,		iRoosevelt,		iFDR,			iKennedy,			iReagan,
iObama,			iSanMartin,		iPeron,			iMontezuma,		iPedro,			iVargas,		iMacDonald,		iTrudeau,		iTacaynamo,		iBolivar,
iCastro,		iElizabeth,		iVictoria,		iChurchill,		iLouis,			iNapoleon,		iDeGaulle,		iLOuverture,	iKamehameha,	iHuaynaCapac,
iPachacuti,		iAua,			iHiawatha,		iPacal,			iJuarez,		iSantaAnna,		iCardenas,		iRedHorn,		iSaguamanchica,	iWillemVanOranje,
iWilliam,		iRagnar,		iGustav,		iGerhardsen,	iCastilla,		iJoao,			iMaria,			iItzukuma,		iCatherine,		iAlexanderI,	
iStalin,		iIsabella,		iPhilip,		iFranco,		iAtlatlCauac,	iMalkuHuyustus,	iChavez,		iWariCapac) = range(iNumLeaders)

dResurrectionLeaders = CivDict({
})

iNumPeriods = 0
#() = range(iNumPeriods)

iNumImpacts = 5
(iImpactMarginal, iImpactLimited, iImpactSignificant, iImpactCritical, iImpactPlayer) = range(iNumImpacts)

lSecondaryCivs = [iChimu, iCuba, iHaiti, iHawaii, iInuit, iIroquois, iMississippi, iMuisca, iNorse, iPeru, iPuebloan, iVenezuela, iWari]

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