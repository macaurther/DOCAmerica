# Rhye's and Fall of Civilization - Constants
# globals

from CvPythonExtensions import *
from DataStructures import *
from CoreTypes import *

gc = CyGlobalContext()

iWorldX = 83
iWorldY = 122

iNumPlayers = gc.getMAX_PLAYERS()

# civilizations, not players
iNumCivs = 38
# 0				1				2				3				4				5				6				7				8				9
(iAmerica, 		iArgentina, 	iAztecs, 		iBrazil, 		iCanada, 		iChimu,			iColombia, 		iEngland, 		iFrance, 		iHaiti,			
iHaudenosaunee,	iHawaii,		iInca,			iInuit,			iLakota,		iMaya,			iMexico, 		iMississippi,	iMuisca,		iNetherlands, 	
iNorse,			iPeru,			iPortugal, 		iPuebloan,		iPurepecha,		iRussia,		iSpain, 		iTeotihuacan,	iTiwanaku,		iVenezuela,		
iWari,			iZapotec,		iIndependent, 	iIndependent2, 	iIndependent3,	iNative,		iMinor, 		iBarbarian) = tuple(Civ(i) for i in range(iNumCivs))

lBirthOrder = [
	iMaya,
	iZapotec,
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
	iPurepecha,
	iAztecs,
	iHaudenosaunee,
	iLakota,
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
iNumCivGroups = 6
(iCivGroupEurope, iCivGroupNative, iCivGroupAmerica, iCivGroupNATO, iCivGroupMesoamerica, iCivGroupAndes) = range(iNumCivGroups)

dCivGroups = {
iCivGroupEurope : [iNorse, iSpain, iFrance, iEngland, iNetherlands, iPortugal, iRussia],
iCivGroupNative : [iMaya, iInca, iAztecs, iTeotihuacan, iTiwanaku, iWari, iMississippi, iPuebloan, iMuisca, iChimu, iInuit, iHaudenosaunee, iLakota, iZapotec, iPurepecha],
iCivGroupAmerica : [iAmerica, iArgentina, iMexico, iColombia, iBrazil, iCanada, iHaiti, iPeru, iVenezuela],
iCivGroupNATO : [iAmerica, iCanada, iNorse, iEngland, iFrance, iSpain, iPortugal, iNetherlands],
iCivGroupMesoamerica : [iMaya, iAztecs, iTeotihuacan, iZapotec, iPurepecha],
iCivGroupAndes : [iInca, iTiwanaku, iWari, iMuisca, iChimu],
}

# used in: Stability
# tech groups share techs within each other on respawn
iNumTechGroups = 3
(iTechGroupWestern, iTechGroupLatinAmerica, iTechGroupNativeAmerica) = range(iNumTechGroups)

dTechGroups = {
iTechGroupWestern : [iNorse, iSpain, iFrance, iEngland, iNetherlands, iPortugal, iRussia, iAmerica, iCanada],
iTechGroupLatinAmerica: [iArgentina, iMexico, iColombia, iBrazil, iHaiti, iPeru, iVenezuela],
iTechGroupNativeAmerica : [iMaya, iInca, iAztecs, iTeotihuacan, iTiwanaku, iWari, iMississippi, iPuebloan, iMuisca, iChimu, iInuit, iHaudenosaunee, iLakota, iHawaii, iZapotec, iPurepecha],
}

lBioNewWorld = [iMaya, iInca, iAztecs, iTeotihuacan, iTiwanaku, iWari, iMississippi, iPuebloan, iMuisca, iChimu, iInuit, iHaudenosaunee, iLakota, iHawaii, iZapotec, iPurepecha]
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

# scripted conquerors
iNumConquests = 23

lNeighbours = [
	(iMaya, iAztecs),
	(iMaya, iMexico),
	(iMaya, iColombia),
	(iMaya, iZapotec),
	(iMaya, iTeotihuacan),
	(iZapotec, iTeotihuacan),
	(iZapotec, iMexico),
	(iZapotec, iAztecs),
	(iZapotec, iPurepecha),
	(iTeotihuacan, iAztecs),
	(iTeotihuacan, iMexico),
	(iTeotihuacan, iPurepecha),
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
	(iMississippi, iHaudenosaunee),
	(iMississippi, iLakota),
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
	(iHaudenosaunee, iLakota),
	(iHaudenosaunee, iEngland),
	(iHaudenosaunee, iFrance),
	(iHaudenosaunee, iNetherlands),
	(iHaudenosaunee, iAmerica),
	(iHaudenosaunee, iCanada),
	(iLakota, iEngland),
	(iLakota, iFrance),
	(iLakota, iAmerica),
	(iLakota, iCanada),
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
	(iAztecs, iZapotec),
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
	(iMexico, iZapotec),
	(iMexico, iAztecs),
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
iMaya : -500,
iZapotec : -500,
iTeotihuacan : -200,
iTiwanaku : 110,
iWari : 500,
iMississippi : 600,
iPuebloan : 750,
iMuisca : 800,
iNorse : 874,
iChimu : 900,
iInuit : 950,
iInca : 1100,
iPurepecha : 1150,
iAztecs : 1250,
iHaudenosaunee : 1450,
iLakota : 1475,
iSpain : 1492,
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
}, -500)

lBirthCivs = dBirth.keys()

dFall = CivDict({
iMaya : 1350,
iZapotec : 1550,
iTeotihuacan : 1400,
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
iHaudenosaunee : 1800,
iSpain : 1850,
iPortugal : 1850,
iFrance : 1850,
iLakota : 1875,
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
iAmerica : [iEngland, iHaudenosaunee, iIndependent, iIndependent2, iNative],
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
iZapotec : 1,
iTeotihuacan : 2,
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
iHaudenosaunee : 2,
iLakota : 2,
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
iZapotec : 20,
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
iPurepecha : 20,
iAztecs : 30,
iHaudenosaunee : 25,
iLakota : 30,
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
iNumPaganReligions = 13
# 0				1				2				3				4				5				6				7				8				9
(iAngakkuq, 	iAsatru, 		iAtua, 			iDruidism, 		iGaiwiio,		iInti, 			iKachina,		iMidewiwin, 	iRodnovery, 	iTeotlMaya, 
iTeotlAztec, 	iWocekiya,		iYoruba) = range(iNumPaganReligions)

iPaganVictory = iNumReligions
iSecularVictory = iNumReligions + 1

# corporations
iNumCorporations = 8
(iFurTrade, iTradingCompany, iCerealIndustry, iFishingIndustry, iTextileIndustry, iSteelIndustry, iOilIndustry, iLuxuryIndustry) = range(iNumCorporations)

# initialise tech variables to unit indices from XML

iNumTechs = 152
#				2				3				4				5				6				7
(iHunting,		iLandmarks,		iIrrigation,	iLinguistics,	iCultivation,	iSpiritualism,	iShallowFishing,
iTrapping,      iPathfinding,   iEarthworks,    iLocalization,  iCompanionPlanting,iHerbalism,  iFishing,
iNorthEuropeAccess, iSouthEuropeAccess, iAfricaAccess, iSiberiaAccess, iAsiaAccess,
iTanning, 		iMining, 		iPottery, 		iAgriculture, 	iPastoralism, 	iMythology, 	iSailing,
iSmelting,      iMasonry,       iProperty,      iArithmetics,   iCeremony,      iDivination,    iSeafaring,
iAlloys,        iConstruction,  iMathematics,   iAstronomy,     iWriting,       iCalendar,      iTrade,
iGeneralship,   iCement,        iAesthetics,    iScholarship,   iCodices,       iPriesthood,    iNavigation,
iNobility,      iSubjugation,   iArtisanry,     iMedicine,      iLaw,           iEthics,        iPhilosophy,
iMedievalTactics,iMedievalScience,iMedievalCulture,
iGunpowder, 	iCompanies, 	iFinance, 		iCartography, 	iExchange, 		iReductions,	iEvangelism,
iFirearms, 		iTriangularTrade,iExploration, 	iOptics, 		iTreaties, 		iOfficials, 	iIndoctrination,
iFortification,	iEconomics, 	iColonization, 	iShipbuilding, 	iEducation,		iCharter, 		iIndentures,
iCombinedArms, 	iLogistics,		iExploitation, iTimekeeping, 	iCommunity, 	iPolitics, 		iHorticulture,
iTactics,		iCurrency,		iGeography,		iScientificMethod,iUrbanPlanning,iStatecraft,	iSocialContract,
iReplaceableParts, iFreeMarket,	iNewspapers,	iAcademia, 		iArchitecture, 	iSociology,		iHeritage,
iRegiments, 	iBonds,			iPostalService,	iMeteorology,	iSurveying,		iRepresentation,iIndependence,
iMetallurgy,	iProtectionism,	iHydrology,		iPhysics,		iPioneering,	iJudiciary,		iHumanities,
iMachineTools, 	iThermodynamics, iEngineeing, 	iChemistry, 	iGeology,		iNationalism, 	iCivilLiberties,
iMeasurement, 	iEngine, 		iRailroad, 		iElectricity, 	iConservation, 	iImperialism, 	iEmancipation,
iBallistics,	iAssemblyLine,	iCombustion,	iTelegraph,		iBiology,		iLaborUnions,	iJournalism,
iFlight,		iMacroeconomics,iInfrastructure,iRadio,			iEcology,		iPowerProjection,iPsychology,
iAviation,		iGlobalism,		iFission,		iSynthetics,	iSocialServices,iCivilRights,	iTelevision,
iRocketry,		iNuclearPower,	iRadar,
iMultilateralism) = range(iNumTechs)

# Techs that Natives start the game with, but Europeans have to trade for
lNativeTechs = [iHunting, iLandmarks, iIrrigation, iLinguistics, iCultivation, iSpiritualism, iShallowFishing,
                iTrapping, iPathfinding, iEarthworks, iLocalization, iCompanionPlanting, iHerbalism, iFishing]
# Techs that allow immigration in certain regions
lImmigraitonTechs = [iNorthEuropeAccess, iSouthEuropeAccess, iAfricaAccess, iSiberiaAccess, iAsiaAccess]

# initialise unit variables to unit indices from XML

iNumUnits = 154
# Land Units (101)
# 0				1				2				3				4				5				6				7				8				9
(iGrizzlyBear, 	iPolarBear,		iPanther, 		iJaguar,		iCougar,		iWolf, 			iCoyote,		iClawdius,		iSettler, 		iDogSled,		
iPioneer,		iWorker, 		iArtisan,		iPromyshlenniki,iTrackman,		iLaborer, 		iMadeireiro, 	iSpy, 			iSisqeno,       iAgent,			
iInquisitor,	iOrthodoxMiss, 	iCatholicMiss, 	iProtestantMiss,iImmigrant,		iScout, 		iPathfinder,	iExplorer, 		iBandeirante, 	iCoureurDesBois,
iRanger,		iFactor,		iParatrooper,	iMilitia1,		iFalconDancer,	iMilitia2,		iMilitia3,		iMilitia4,		iMinuteman,		iMilitia5,		
iMilitia6,		iWarrior, 		iKoa,			iMohawk,		iMaceman,		iAucac,			iAztecJaguar,	iMacana,		iArquebusier,	iArmedSlave,	
iMusketman,		iCompagnies,	iFusilier,		iGuardia,		iRifleman,		iVencedores,	iInfantry,		iFARs,			iSpearman,		iSuchucChiqui,	
iLightningWarrior,iPikeman,		iEagle,			iPikeAndShot,	iLineInfantry,	iRedcoat,		iAntiTank,		iArcher,		iPicta,			iGuecha,		
iCrossbowman,	iGatlingGun,	iMachineGun,	iAtlatlist,		iHolkan,		iSlinger,		iLongbowman,	iSkirmisher,	iGrenadier,		iCacos,			
iAlbionLegion,	iMarine,		iHorseArcher,	iSwiftArrow,	iCuirassier,	iConquistador,	iDragoon,		iLlanero,		iCavalry,		iGrenadierCavalry,
iRural,			iLightTank,		iTank,			iBombard,		iCannon,		iHeavyCannon,	iLightCannon,	iRifledCannon,	iFieldGun,		iArtillery,		
iAAGun,		

# Naval Units (27)
# 0				1				2				3				4				5				6				7				8				9
iWorkboat,		iCanoe,			iLongship,		iWaaKaulua,		iKayak,			iCaravel,		iCarrack,		iIndiaman,		iGalleon,       iFluyt,			
iBrigantine,	iSteamship,		iTransport,		iCarrier,		iSloop,			iFrigate,		iIronclad,		iDestroyer,		iCorvette,		iPrivateer,	    
iMonitor,		iSubmarine,		iBarque,		iShipOfTheLine,	iManOfWar,		iCruiser,		iBattleship,	
# Air Units (4)
# 0				1				2				3				4				5				6				7				8				9
iBiplane,		iFighter,		iBomber,		iNuclearBomber,	
# Great People Units (17)
# 0				1				2				3				4				5				6				7				8				9
iGreatProphet, 	iGreatArtist, 	iGreatScientist,iGreatMerchant, iGreatEngineer, iGreatStatesman,iGreatGeneral,	iArgentineGreatGeneral,iGreatSpy,iFeGreatProphet,
iFeGreatArtist,iFeGreatScientist,iFeGreatMerchant,iFeGreatEngineer,iFeGreatStatesman,iFeGreatGeneral,iFeGreatSpy,
# Other Units (5)
# 0				1				2				3				4				5				6				7				8				9
iAfricanSlave2,	iAfricanSlave3,	iNativeSlave1,	iNativeSlaveMeso,iNativeSlave2) = range(iNumUnits)

lAnimalUnits = [iGrizzlyBear, 	iPolarBear,		iPanther, 		iJaguar,		iCougar,		iWolf, 			iCoyote]

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


iNumUnitRoles = 23
# 0				1				2				3				4				5				6				7				8				9
(iSettle,		iWork,			iRecon,			iMissionary,	iMilitia,		iBase,			iCounter,		iDefend,		iSkirmish,		iCav,			
iSiege,			iSiegeCity,		iWorkSea,		iFerrySea,		iEscortSea,		iHarassSea,		iCapitalSea,	iColonistSettle,iColonistSupport,iColonistExplore, 
iColonistConquer, iColonistDefend, iColonistSlave) = range(iNumUnitRoles)

lColonistRoles = [iColonistSettle, iColonistSupport, iColonistExplore, iColonistConquer, iColonistDefend, iColonistSlave]

# initialise bonuses variables to bonuses IDs from WBS
iNumBonuses = 49
# 0				1				2				3				4				5				6				7				8				9
(iAluminium, 	iBison,			iCitrus,		iCoal, 			iCopper, 		iHorse, 		iIron, 			iMarble, 		iOil, 			iStone, 		
iUranium, 		iBanana, 		iClam, 			iCorn, 			iCow, 			iCrab,			iDeer, 			iFish, 			iPig, 			iPotato,		
iRice, 			iSheep, 		iLlama,			iWheat, 		iCocoa,			iCoffee, 		iCotton,		iDye, 			iFur,			iGems, 			
iGold, 			iIncense, 		iJade,			iObsidian,		iPearls, 		iRubber,		iSalt,			iSilk, 			iSilver, 		iSpices,		
iSugar,			iTea, 			iTimber,		iTobacco, 		iWine, 			iWhales, 		iSoccer, 		iSongs, 		iMovies) = range(iNumBonuses)

iNumBonusVarieties = 3
# 0				1				2				3				4				5				6				7				8				9
(iDyeCochineal, iCitrusOranges, iCrabShrimp) = range(iNumBonuses, iNumBonuses + iNumBonusVarieties)

# Buildings
iNumBuildings = 224
# Buildings (118)
# 0				1				2				3				4				5				6				7				8				9
(iPalace,		iChieftansHut,	iGovernorsMansion,iCapitol,		iGranary,		iColcas,		iIgloo,			iTipi,			iMarket,		iWeaver,		
iStoneworks,	iArena,			iBallCourt,		iSambadrome,	iBarracks,		iKallanka,		iHerbalist,		iKuna,			iAltar,			iTomb,			
iTzompantli,	iYacatas,		iPaganTemple,	iAqueduct,		iSukaQullu,		iBath,			iTemazcal,		iJeweller,		iGoldsmith,		iWalls,			
iKancha,		iPlaza,			iPlatformMound,	iKiva,			iLonghouse,		iHarbor,		iSmokehouse,	iLuau,			iStocks,		iTradingPost,	
iHuntingPost,	iForge,			iTavern,		iStable,		iPalisade,		iFactorij,		iMonument,		iSchoolhouse,	iCalmecac,		iGrocer, 		
iConstabulary,	iRoyalMountedPolice,iSlaveMarket1,iSlaveMarket2,iSlaveMarket3,	iWharf,			iLighthouse,	iWarehouse,		iSilversmith,	iMagazine,		
iStarFort,		iCitadelle,		iEstate,		iHacienda,		iUniversity,	iPharmacy,		iDistillery,	iCourthouse,	iAssembly,		iThingvellir,	
iWheelwright,	iPostOffice,	iTambo,			iCustomsHouse,	iFeitoria,		iBank,			iLevee,			iSeigneur,		iTheatre,		iShipyard,		
iObservatory,	iPrintingPress,	iMeetingHall,	iStateHouse,	iSlaughterhouse,iColdStoragePlant,iSewer,		iJail,			iImmigrationOffice,iRailwayStation,
iTextileMill,	iWoolMill,		iSteelMill,		iRefinery,		iRodeo,			iCharreada,		iArsenal,		iDrydock,		iNewspaper,		iSupermarket,	
iHospital,		iIntelligenceAgency,iAirport,	iHotel,			iDepartmentStore,iMall,			iElectricalGrid,iFactory,		iMaquiladora,	iCoalPlant,		
iHydroPlant,	iIndustrialPark,iNuclearPlant,	iPark,			iStadium,		iBunker,		iLaboratory,	iBroadcastTower,
# Religious Buildings (41)
# 0				1				2				3				4				5				6				7				8				9
iJewishTemple, iJewishCathedral, iJewishMonastery, iJewishShrine, iOrthodoxTemple, iOrthodoxCathedral, iOrthodoxMonastery, iOrthodoxShrine, iCatholicTemple, iCatholicCathedral, 
iCatholicMonastery, iMission,	iCatholicShrine, iProtestantTemple, iProtestantCathedral, iProtestantMonastery, iProtestantShrine, iIslamicTemple, iIslamicCathedral, iIslamicMonastery, 
iIslamicShrine, iHinduTemple, iHinduCathedral, iHinduMonastery, iHinduShrine, iBuddhistTemple, iBuddhistCathedral, iBuddhistMonastery, iBuddhistShrine, iConfucianTemple, 
iConfucianCathedral, iConfucianMonastery, iConfucianShrine, iTaoistTemple, iTaoistCathedral, iTaoistMonastery, iTaoistShrine, iZoroastrianTemple, iZoroastrianCathedral, iZoroastrianMonastery, 
iZoroastrianShrine, 
# Great Buildings (6)
# 0				1				2				3				4				5				6				7				8				9
iAcademy, 		iAdministrativeCenter, iManufactory, iArmoury, 	iMuseum, 		iStockExchange, 
# Great Buildings/National Wonders (12)
# 0				1				2				3				4				5				6				7				8				9
iNationalMonument,iNationalTheatre,iNationalGallery,iNationalCollege,iMilitaryAcademy,iSecretService,iIronworks,iRedCross,		iNationalPark,	iCentralBank, 	
iGrandCentralStation,iSupremeCourt,
# Great Wonders (47)
# 0				1				2				3				4				5				6				7				8				9
iFloatingGardens,iTempleOfKukulkan,iMachuPicchu,iPuebloBonito,	iSacsayhuaman,	iHueyTeocalli,	iTlachihualtepetl,iYachaywasi,	iGateOfTheSun,	iGreatGeoglyph,	
iKalasasaya,	iPyramidOfTheSun,iSerpentMound,	iTemblequeAqueduct,iLaFortaleza,iSaoFranciscoSquare,iGuadalupeBasilica,iManzanaJesuitica,iIndendenceHall,iHospicioCabanas,
iMountVernon,	iMonticello,	iSlaterMill,	iChapultepecCastle,iWestPoint,	iFortMcHenry,	iWashingtonMonument,iFaneuilHall,iStatueOfLiberty,iCentralPark,	
iEllisIsland,	iBrooklynBridge,iChateauFrontenac,iMenloPark,	iBiltmoreEstate,iFrenchQuarter, iLeagueOfNations,iEmpireStateBuilding,iGoldenGateBridge,iHooverDam,
iAlcatraz,		iMountRushmore,	iHollywood,		iSaltCathedral,iCristoRedentor,	iLasLajasSanctuary,iPentagon	) = range(iNumBuildings)


iBeginWonders = iFloatingGardens # different from DLL constant because that includes national wonders

iTemple = iJewishTemple #generic
iCathedral = iJewishCathedral #generic
iMonastery = iJewishMonastery #generic
iShrine = iJewishShrine #generic

iFirstWonder = iFloatingGardens

iPlague = iNumBuildings
iNumBuildingsPlague = iPlague+1

iNumPaganTemples = 12
# Pagan Temples (12)
# 0				1				2				3				4				5				6				7				8				9
(iAtuaShrine,	iTeotlStepPyramid,iAsatruHof,	iDruidicNemeton,iPerunShrine,	iYorubaTemple,	iIntiTemple,	iMidewiwinMidewigaan,iAngakkuqQargi,iGaiwiioLonghouse,
iKachinaPithouse,iWocekiyaShrine) = range(iNumPaganTemples)

iNumBuildingsPaganTemples = iNumBuildingsPlague + iNumPaganTemples

#Civics
iNumCivics = 126
#				2				3				4				5				6				7				
# Native (Culture Group 1)
(iElders1,		iChiefdom1,		iDespotism1,	iMonarchy1,		iAristocracy1,	iCouncil1,		iGodKing1,
iAuthority1,	iCustomaryLaw1,	iCityStates1,	iConfederacy1,	iBureaucracy1,	iVassalage1,	iFirstNation1,
iTraditionalism1,iSubsistance1,	iCaptives1,		iMita1,			iCraftsmen1,	iCasteSystem1,	iSlavery1,	
iReciprocity1,	iCommune1,		iRedistribution1,iMerchants1,	iPlunder1,		iDependency1,	iTourism1,
iAnimism1,		iHarmony1,		iIsolationism1,	iOrganizedReligion1,iCosmopolis1,iAcculturation1,iSovereignty1,
iSettlement1,	iNomads1,		iDiffusion1,	iCooperation1,	iConquest1,		iTributaries1,	iAncestralLands1,
# Colony
iCaptains2,		iProprietaries2,iViceroyalty2,	iTrustees2,		iGovernors2,	iColonialAssembly2,iHomeRule2,
iExpedition2,	iAdmiralty2,	iCharterColony2,iTradingCompany2,iRoyalColony2,	iCommonLaw2,	iProvinces2,
iSerfdom2,		iEncomienda2,	iIndenturedServitude2,iSlavery2,iPenalColony2,	iIndustrialism2,iImmigrantLabor2,
iGoldRush2,		iPlunder2,		iFactory2,		iMercantilism2,	iCustomsUnion2,	iConsumerism2,	iPublicWelfare2,
iDivineRight2,	iJesuits2,		iZealotry2,		iHaven2,		iProfiteering2,	iOpportunity2,	iEmancipation2,
iClaims2,		iConquest2,		iProvidence2,	iOutposts2,		iHomesteads2,	iIntervention2,	iCommonwealth2,
# Nation
iStrongman3,	iJunta3,		iMonarchy3,		iPlutocracy3,	iDemocracy3,	iDictatorship3,	iStateParty3,
iMinarchy3,		iCommonLaw3,	iConfederacy3,	iKleptocracy3,	iFederalism3,	iMandate3,		iPoliceState3,
iTraditionalism3,iSubsistance3,	iApprenticeship3,iSlavery3,		iIndustrialism3,iImmigrantLabor3,iLaborUnions3,
iLaissezFaire3,	iAgrarianism3,	iExtraction3,	iFreeEnterprise3,iProtectionism3,iConsumerism3,	iPublicWelfare3,
iRevolution3,	iLibertarianism3,iProfiteering3,iOpportunity3,	iEmancipation3,	iNativism3,		iEgalitarianism3,
iDisplacement3,	iHomesteads3,	iAssimilation3,	iManifestDestiny3,iDecolonization3,iNationhood3,iHegemony3) = range(iNumCivics)

iNumCivicCategories = 6
(iCivicsExecutive, iCivicsAdministration, iCivicsLabor, iCivicsEconomy, iCivicsSociety, iCivicsExpansion) = range(iNumCivicCategories)

iNumCivicsPerCategory = 7


#Specialists
iNumSpecialists = 18
#				            2				            3				            4				            5
(iSpecialistCitizen,        iSpecialistPriest,          iSpecialistArtist,          iSpecialistScientist,       iSpecialistMerchant,
iSpecialistEngineer,        iSpecialistStatesman,       iSpecialistGreatProphet,    iSpecialistGreatArtist,     iSpecialistGreatScientist, 
iSpecialistGreatMerchant,   iSpecialistGreatEngineer,   iSpecialistGreatStatesman,  iSpecialistGreatGeneral,    iSpecialistGreatSpy,
iSpecialistSlave,			iSpecialistSharecropper,	iSpecialistImmigrant) = range(iNumSpecialists)

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
iParameterWarSuccess, iParameterWarWeariness, iParameterBarbarianLosses) = range(iNumStabilityParameters)					# Military

#Regions
iNumRegions = 52
# 0				1				2				3				4				5				6				7				8				9
(rAlaska, 		rYukon,         rNunavut, 		rGreenland,     rIceland,       rNorthCascadia, rNorthPlains, 	rOntario, 		rQuebec, 		rNewFoundland, 	
rSouthCascadia, rCalifornia,    rRockies,       rSouthwest,     rTexas,         rGreatPlains,   rGreatLakes,    rNewEngland,    rMidAtlantic,   rMaryland,
rRiverValley,    rCoastalPlain,  rDeepSouth,     rFlorida,       rBajaCalifornia,rSierraMadres,  rBajio,         rVeracruz,      rOaxaca,        rYucatan,       
rMesoamerica,   rCaribbean, 	rHawaii, 		rColombia, 		rVenezuela, 	rGuyana, 		rPeru, 			rBolivia, 		rAmazonas, 		rPara,          
rBahia,         rMinasGerais,   rMatoGrosso,    rParana,        rChile, 		rParaguay, 		rUruguay, 		rChaco,         rCuyo,          rPampas, 		
rPatagonia, 	rOldWorld		) = range(iNumRegions)

lCanadaAtlanticCoast = [rQuebec, rNewFoundland]
lCanadaPacificCoast = [rNorthCascadia]
lCanada = [rYukon, rNunavut, rNorthCascadia, rNorthPlains, rOntario, rQuebec, rNewFoundland]
lThirteenColonies = [rNewEngland, rMidAtlantic, rMaryland, rCoastalPlain]
lSouthernUS = [rCoastalPlain, rFlorida, rTexas, rDeepSouth]
lBorderStates = [rMaryland, rRiverValley]
lLouisianaPurchase = [rGreatLakes, rRiverValley, rDeepSouth, rCoastalPlain, rFlorida, rTexas, rGreatPlains]
lContinentalUS = [rSouthCascadia, rCalifornia, rRockies, rSouthwest, rTexas, rGreatPlains, rGreatLakes, rNewEngland, rMidAtlantic, rMaryland, rRiverValley, rCoastalPlain, rDeepSouth, rFlorida]
lUnitedStates = lContinentalUS + [rAlaska, rHawaii]
lMexico = [rBajaCalifornia, rSierraMadres, rBajio, rVeracruz, rOaxaca, rYucatan]
lBrazil = [rAmazonas, rPara, rBahia, rMinasGerais, rMatoGrosso, rParana,]
lArgentina = [rChaco, rCuyo, rPampas, rPatagonia]
lAndes = [rColombia, rPeru, rBolivia, rChile, rChaco]

lSouthAmerica = [rColombia, rVenezuela, rGuyana, rPeru, rBolivia, rChile, rParaguay, rUruguay] + lArgentina + lBrazil
lCentralAmerica = [rMesoamerica, rCaribbean]
lLatinAmerica = lCentralAmerica + lMexico + lSouthAmerica
lNorthAmerica = lCanada + lContinentalUS + [rAlaska] + lMexico

lAmerica = lSouthAmerica + lCentralAmerica + lNorthAmerica
lWest = lAmerica + [rHawaii, rGreenland]

# Revealed Tile Lists
lEuropeanRevealed1600AD = [rIceland, rNewFoundland, rNewEngland, rMidAtlantic, rMaryland, rCoastalPlain, rFlorida, rBajaCalifornia, rSierraMadres, rBajio, rVeracruz, \
						   rOaxaca, rYucatan, rMesoamerica, rCaribbean, rColombia, rVenezuela, rGuyana, rPeru, rBolivia, rMinasGerais, rChile, rUruguay, rPampas, rPatagonia]
lEuropeanRevealed1750AD = [rGreenland, rIceland, rOntario, rQuebec, rNewFoundland, rCalifornia, rTexas, rGreatLakes, rNewEngland, rMidAtlantic, rMaryland, rRiverValley, \
						   rCoastalPlain, rDeepSouth, rFlorida, rBajaCalifornia, rSierraMadres, rBajio, rVeracruz, rOaxaca, rYucatan, rMesoamerica, rCaribbean, rColombia, \
						   rVenezuela, rGuyana, rPeru, rBolivia, rBahia, rMinasGerais, rMatoGrosso, rParana, rChile, rParaguay, rUruguay, rChaco, rCuyo, rPampas, rPatagonia]
lEuropeanRevealed1850AD = lWest


#Projects

iNumProjects = 9
# 0				1				2				3				4				5				6				7				8				9
(iMigrateN,		iMigrateNE,		iMigrateE,		iMigrateSE,		iMigrateS,		iMigrateSW,		iMigrateW,		iMigrateNW,		iWorldsFair) = range(iNumProjects)

#Eras

iNumEras = 7
(iAncientEra, iClassicalEra, iExplorationEra, iColonialEra, iRevolutionaryEra, iIndustrialEra, iModernEra) = range (iNumEras)

# Culture

iNumCultureLevels = 7
(iCultureLevelNone, iCultureLevelPoor, iCultureLevelFledgling, iCultureLevelDeveloping, iCultureLevelRefined, iCultureLevelInfluential, iCultureLevelLegendary) = range(iNumCultureLevels)


#Improvements

iNumImprovements = 31
# 0				1				2				3				4				5				6				7				8				9
(iLandWorked, 	iWaterWorked, 	iCityRuins, 	iFarm, 			iPaddyField, 	iFishingBoats, 	iOceanFishery, 	iWhalingBoats, 	iMine, 			iSlaveMine, 
iWorkshop, 		iLumbermill, 	iWindmill, 		iWatermill, 	iPlantation, 	iSlavePlantation, iQuarry, 		iPasture, 		iCamp, 			iWell, 			
iOffshorePlatform,iOrchard,		iCottage, 		iHamlet, 		iVillage, 		iTown, 			iFort, 			iForestPreserve, iMarinePreserve,iTribe,		
iContactedTribe) = range(iNumImprovements)

iNumRoutes = 3
(iRouteRoad, iRouteRailroad, iRouteHighway) = range(iNumRoutes)

#feature & terrain

iNumFeatures = 19
# 0				1				2				3				4				5				6				7				8				9
(iSeaIce, 		iJungle, 		iCenote, 		iFloodPlains, 	iForest, 		iBog, 			iSwamp, 		iCape, 			iIslands, 		iRainforest, 
iFallout, 		iTaiga, 		iPalmForest,	iCanyon,		iTradewindNorthEurope,iTradewindSouthEurope,iTradewindAfrica,iTradewindSiberia,iTradewindAsia) = range(iNumFeatures)

lHomelandTradewinds = [iTradewindNorthEurope, iTradewindSouthEurope, iTradewindAfrica, iTradewindSiberia, iTradewindAsia]
iTradeWindsStart = iTradewindNorthEurope

iNumTerrains = 21
# 0				1				2				3				4				5				6				7				8				9
(iGrass, 		iPlains, 		iDesert, 		iTundra, 		iSnow, 			iCoast, 		iOcean, 		iTerrainPeak, 	iTerrainHills, 	iMarsh,
iLagoon,		iArcticCoast,	iSemidesert,	iPrairie,		iMoorland,		iSaltflat,		iSaltlake,		iAtoll,			iSavanna,		iWideRiver,
iFjord) = range(iNumTerrains)


#Plague
iImmunity = 20

# Victory
iVictoryPaganism = 10
iVictorySecularism = 11


#leaders
iNumLeaders = 60
# 0				1				2				3				4				5				6				7				8				9
(iLeaderBarbarian,iNativeLeader,iIndependentLeader,iWashington,	iJackson,		iLincoln,		iRoosevelt,		iFDR,			iKennedy,			iReagan,
iObama,			iSanMartin,		iPeron,			iMontezuma,		iPedro,			iVargas,		iMacDonald,		iTrudeau,		iTacaynamo,		iBolivar,
iElizabeth,		iVictoria,		iChurchill,		iLouis,			iNapoleon,		iDeGaulle,		iLOuverture,	iKamehameha,	iHuaynaCapac,	iPachacuti,		
iAua,			iHiawatha,		iPacal,			iJuarez,		iSantaAnna,		iCardenas,		iRedHorn,		iSaguamanchica,	iWillemVanOranje,iWilliam,		
iRagnar,		iGustav,		iGerhardsen,	iCastilla,		iJoao,			iMaria,			iItzukuma,		iCatherine,		iAlexanderI,	iStalin,		
iIsabella,		iPhilip,		iFranco,		iAtlatlCauac,	iMalkuHuyustus,	iChavez,		iWariCapac,		iCosijoeza,		iTariacuri,		iSittingBull) = range(iNumLeaders)

dResurrectionLeaders = CivDict({
})

iNumPeriods = 0
#() = range(iNumPeriods)

iNumImpacts = 5
(iImpactMarginal, iImpactLimited, iImpactSignificant, iImpactCritical, iImpactPlayer) = range(iNumImpacts)

lSecondaryCivs = [iChimu, iHaiti, iHawaii, iInuit, iHaudenosaunee, iMississippi, iMuisca, iNorse, iPeru, iPuebloan, iVenezuela, iWari, iLakota]

(i500BC, i1500AD, i1750AD) = range(3)

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
iNumImmigrantCategories = 28
# 0				1				2				3				4				5				6				7				8				9
(iSettlersCat,	iWorkersCat,	iMissionariesCat,iTransportsCat,iSlavesCat,		iColonistsCat,	iTrackmanCat,iExplorersCat,iMilitiaCat,	iMainlineCat,	
iEliteCat,		iCollateralCat,	iSkirmishCat,	iCavCat,		iSiegeCat,		iMainlineShipCat,iSkirmishShipCat,iCapitalShipCat,iEndowCatArt,	iEndowCatAssets,
iEndowCatInno,	iGPCatProphet,	iGPCatArtist,	iGPCatScientist,iGPCatMerchant,	iGPCatEngineer,	iGPCatStatesman,iGPCatGeneral) = range(iNumImmigrantCategories)

lSettlers = [iSettler, iPioneer]
lWorkers = [iWorker, iPromyshlenniki, iLaborer, iMadeireiro]
lMissionaries = [iOrthodoxMiss, iCatholicMiss, iProtestantMiss]
lTransports = [iLongship, iCaravel, iCarrack, iIndiaman, iGalleon, iFluyt, iBrigantine, iSteamship, iTransport]
lAfricanSlaves = [iAfricanSlave2, iAfricanSlave3]
lColonists = [iImmigrant]
lMigrantWorkers = [iTrackman]
lExplorers = [iExplorer, iBandeirante, iCoureurDesBois, iRanger, iFactor]
lMilitia = [iMilitia2, iMilitia3, iMilitia4, iMilitia5, iMilitia6]
lMainlineMercs = [iArquebusier, iMusketman, iCompagnies, iFusilier, iRifleman, iInfantry]
lEliteMercs = [iPikeman, iPikeAndShot, iLineInfantry, iRedcoat, iAntiTank]
lCollateralMercs = [iCrossbowman, iLightCannon, iFieldGun, iGatlingGun, iMachineGun]
lSkirmishMercs = [iSkirmisher, iGrenadier, iMarine]
lCavalryMercs = [iCuirassier, iConquistador, iDragoon, iCavalry, iLightTank, iTank]
lSiegeMercs = [iBombard, iCannon, iHeavyCannon, iRifledCannon, iArtillery]
lMainlineShips = [iSloop, iFrigate, iIronclad, iDestroyer]
lSkirmishShips = [iPrivateer, iSubmarine] # Note: Can't hire Monitors because they can't go in ocean
lCapitalShips = [iBarque, iShipOfTheLine, iManOfWar, iCruiser, iBattleship, iCarrier]
lGPProphet = [iGreatProphet]
lGPArtist = [iGreatArtist]
lGPScientist = [iGreatScientist]
lGPMerchant = [iGreatMerchant]
lGPEngineer = [iGreatEngineer]
lGPStatesman = [iGreatStatesman]
lGPGeneral = [iGreatGeneral]

lNativeSlaves = [iNativeSlave1, iNativeSlaveMeso, iNativeSlave2]	# Not used for Immigration
lSlaves = lAfricanSlaves + lNativeSlaves							# Not used for Immigration

lGreatPeople = lGPProphet + lGPArtist + lGPScientist + lGPMerchant + lGPEngineer + lGPStatesman + lGPGeneral

lPossibleColonists = [lSettlers, lWorkers, lMissionaries, lTransports, lAfricanSlaves, lColonists, lMigrantWorkers]

lPossibleMercenariesLand = [lExplorers, lMilitia, lMainlineMercs, lEliteMercs, lCollateralMercs, lSkirmishMercs, lCavalryMercs, lSiegeMercs]
lPossibleMercenariesSea = [lMainlineShips, lSkirmishShips, lCapitalShips]
lPossibleMercenaries = lPossibleMercenariesLand + lPossibleMercenariesSea

lPossibleImmigrants = lPossibleColonists + lPossibleMercenaries
lNoTrainingNeeded = lAfricanSlaves + lColonists + lMigrantWorkers

# A goal number of cities for an AI to build, used in Immigration Manager
dNumCitiesGoal = CivDict({
iMaya : 3,
iZapotec : 1,
iTeotihuacan : 2,
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
iHaudenosaunee : 5,
iLakota : 5,
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
iCanada : 15,
}, 0)

# Immigration Homelands
iNumImmigrationHomelands = 5
(iHomelandNorthEurope, iHomelandSouthEurope, iHomelandAfrica, iHomelandSiberia, iHomelandAsia) = range(iNumImmigrationHomelands)
lHomelandsEurope = [iHomelandNorthEurope, iHomelandSouthEurope]
lHomelandsEuropePlus = lHomelandsEurope + [iHomelandSiberia]
lHomelands = lHomelandsEuropePlus + [iHomelandAfrica, iHomelandAsia]

iEndDate = 2050
# Immigrant Schedule
dImmigrantSchedule = {
iSettler : 				[(1500, iEndDate), 	lHomelands],
iDogSled : 				[(-5000, 1500), 	[iHomelandSiberia]],
iPioneer : 				[(1850, iEndDate), 	lHomelands],
iWorker : 				[(1500, iEndDate),  [iHomelandNorthEurope, iHomelandSouthEurope, iHomelandAfrica]],
iPromyshlenniki : 		[(1700, iEndDate), 	[iHomelandSiberia]],
iLaborer : 				[(1850, iEndDate), 	lHomelands],
iTrackman : 			[(1800, iEndDate), 	[iHomelandAsia]],
iOrthodoxMiss : 		[(1500, iEndDate), 	[iHomelandSiberia]],
iCatholicMiss : 		[(1500, iEndDate), 	[iHomelandSouthEurope]],
iProtestantMiss : 		[(1500, iEndDate), 	[iHomelandNorthEurope]],
}

# Mercenary Schedule
dMercenarySchedule = {
iExplorer : 			[(1500, 1800), 		lHomelands],
iBandeirante : 			[(1530, 1800), 		[iHomelandSouthEurope]],
iCoureurDesBois : 		[(1620, 1800), 		[iHomelandSouthEurope]],
iRanger : 				[(1800, 1930), 		lHomelands],
iFactor : 				[(1800, 1930), 		[iHomelandNorthEurope]],
iParatrooper : 			[(1930, iEndDate), 	lHomelandsEuropePlus],
iMilitia2 : 			[(1500, 1550), 		lHomelandsEurope],
iMilitia3 : 			[(1550, 1700), 		lHomelandsEurope],
iMilitia4 : 			[(1700, 1800), 		lHomelandsEuropePlus],
iMilitia5 : 			[(1800, 1900), 		lHomelandsEuropePlus],
iMilitia6 : 			[(1900, iEndDate), 	lHomelandsEuropePlus],
iKoa : 					[(0, 	1800), 		[iHomelandAsia]],
iArquebusier : 			[(1500, 1550), 		lHomelandsEurope],
iMusketman : 			[(1550, 1700), 		lHomelandsEurope],
iCompagnies : 			[(1550, 1700), 		[iHomelandSouthEurope]],
iFusilier : 			[(1700, 1800), 		lHomelandsEuropePlus],
iRifleman : 			[(1800, 1900), 		lHomelandsEuropePlus],
iInfantry : 			[(1900, iEndDate), 	lHomelandsEuropePlus],
iPikeman : 				[(1500, 1550), 		lHomelandsEurope],
iPikeAndShot : 			[(1550, 1700), 		lHomelandsEurope],
iLineInfantry : 		[(1700, 1800), 		lHomelandsEuropePlus],
iRedcoat : 				[(1700, 1800), 		[iHomelandNorthEurope]],
iAntiTank : 			[(1930, iEndDate), 	lHomelandsEuropePlus],
iCrossbowman : 			[(1500, 1550), 		lHomelandsEurope],
iGatlingGun : 			[(1850, 1900), 		lHomelandsEuropePlus],
iMachineGun : 			[(1900, 1950), 		lHomelandsEuropePlus],
iSkirmisher : 			[(1550, 1700), 		lHomelandsEurope],
iGrenadier : 			[(1800, 1900), 		lHomelandsEuropePlus],
iAlbionLegion : 		[(1800, 1900), 		[iHomelandNorthEurope]],
iMarine : 				[(1930, iEndDate), 	lHomelandsEuropePlus],
iCuirassier : 			[(1500, 1650), 		lHomelandsEurope],
iConquistador : 		[(1500, 1650), 		[iHomelandSouthEurope]],
iDragoon : 				[(1650, 1800), 		lHomelandsEuropePlus],
iCavalry : 				[(1800, 1920), 		lHomelandsEuropePlus],
iLightTank : 			[(1920, iEndDate), 	lHomelandsEuropePlus],
iTank : 				[(1940, iEndDate), 	lHomelandsEuropePlus],
iBombard : 				[(1500, 1600), 		lHomelandsEurope],
iCannon : 				[(1600, 1700), 		lHomelandsEurope],
iHeavyCannon : 			[(1700, 1850), 		lHomelandsEuropePlus],
iLightCannon : 			[(1700, 1850), 		lHomelandsEuropePlus],
iRifledCannon : 		[(1850, 1900), 		lHomelandsEuropePlus],
iFieldGun : 			[(1850, 1900), 		lHomelandsEuropePlus],
iArtillery : 			[(1900, iEndDate), 	lHomelandsEuropePlus],
iAAGun : 				[(1930, iEndDate), 	lHomelandsEuropePlus],
iLongship : 			[(700,  1450), 		[iHomelandNorthEurope]],
iWaaKaulua : 			[(0, 	1800), 		[iHomelandAsia]],
iKayak : 				[(-5000, 1500), 	[iHomelandSiberia]],
iCaravel : 				[(1500, 1700), 		lHomelandsEurope],
iCarrack : 				[(1500, 1700), 		[iHomelandSouthEurope]],
iIndiaman : 			[(1600, 1700), 		lHomelandsEurope],
iGalleon : 				[(1550, 1700), 		[iHomelandSouthEurope]],
iFluyt : 				[(1600, 1700), 		[iHomelandNorthEurope]],		
iBrigantine : 			[(1700, 1800), 		lHomelandsEuropePlus],
iSteamship : 			[(1800, 1900), 		lHomelandsEuropePlus],
iTransport : 			[(1900, iEndDate), 	lHomelandsEuropePlus],
iCarrier : 				[(1935, iEndDate), 	lHomelandsEuropePlus],
iFrigate : 				[(1700, 1800), 		lHomelandsEuropePlus],
iSloop : 				[(1600, 1700), 		lHomelandsEurope],
iIronclad : 			[(1800, 1900), 		lHomelandsEuropePlus],
iDestroyer : 			[(1900, iEndDate), 	lHomelandsEuropePlus],
iPrivateer : 			[(1550, 1700), 		lHomelandsEurope],
iMonitor : 				[(1850, 1900), 		lHomelandsEuropePlus],
iSubmarine : 			[(1900, iEndDate), 	lHomelandsEuropePlus],
iBarque : 				[(1600, 1750), 		lHomelandsEurope],
iShipOfTheLine : 		[(1750, 1900), 		lHomelandsEuropePlus],
iManOfWar : 			[(1750, 1875), 		[iHomelandNorthEurope]],
iCruiser : 				[(1875, 1930), 		lHomelandsEuropePlus],
iBattleship : 			[(1930, iEndDate), 	lHomelandsEuropePlus],
}



# Homelands for each civ
dHomeland = CivDict({
iMaya : None,
iZapotec : None,
iTeotihuacan : None,
iTiwanaku : None,
iWari : None,
iMississippi : None,
iPuebloan : None,
iMuisca : None,
iNorse : iHomelandNorthEurope,
iChimu : None,
iInuit : None,
iInca : None,
iPurepecha : None,
iAztecs : None,
iHaudenosaunee : None,
iLakota : None,
iSpain : iHomelandSouthEurope,
iPortugal : iHomelandSouthEurope,
iEngland : iHomelandNorthEurope,
iFrance : iHomelandSouthEurope,
iNetherlands : iHomelandNorthEurope,
iHawaii : iHomelandAsia,
iRussia: iHomelandSiberia,
iAmerica : iHomelandNorthEurope,
iHaiti : iHomelandAfrica,
iArgentina : iHomelandSouthEurope,
iMexico : iHomelandSouthEurope,
iColombia : iHomelandSouthEurope,
iPeru : iHomelandSouthEurope,
iBrazil : iHomelandSouthEurope,
iVenezuela : iHomelandSouthEurope,
iCanada : iHomelandNorthEurope,
}, 0)