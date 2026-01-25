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
(iAmerica, 		iArgentina, 	iAztec, 		iBrazil, 		iCanada, 		iChimu,			iColombia, 		iEngland, 		iFrance, 		iHaiti,			
iHaudenosaunee,	iHawaii,		iInca,			iInuit,			iLakota,		iMaya,			iMexico, 		iMississippi,	iMuisca,		iNetherlands, 	
iNorse,			iPeru,			iPortugal, 		iPueblo,		iPurepecha,		iRussia,		iSpain, 		iTeotihuacan,	iTiwanaku,		iVenezuela,		
iWari,			iZapotec,		iIndependent1, 	iIndependent2, 	iIndependent3,	iIndigenous,	iMinor, 		iBarbarian) = tuple(Civ(i) for i in range(iNumCivs))

lBirthOrder = [
	iMaya,
	iZapotec,
	iTeotihuacan,
	iTiwanaku,
	iWari,
	iMississippi,
	iMuisca,
	iNorse,
	iChimu,
	iPueblo,
	iPurepecha,
	iInuit,
	iInca,
	iAztec,
	iHaudenosaunee,
	iSpain,
	iPortugal,
	iEngland,
	iFrance,
	iNetherlands,
	iLakota,
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
	iIndependent1,
	iIndependent2,
	iIndependent3,
	iIndigenous,
	iBarbarian
]

# used in: Congresses, DynamicCivs, Plague, RFCUtils, UniquePowers, Victory
# a civilisation can be in multiple civ groups
iNumCivGroups = 6
(iCivGroupEurope, iCivGroupNative, iCivGroupAmerica, iCivGroupNATO, iCivGroupMesoamerica, iCivGroupAndes) = range(iNumCivGroups)

dCivGroups = {
iCivGroupEurope : [iNorse, iSpain, iFrance, iEngland, iNetherlands, iPortugal, iRussia],
iCivGroupNative : [iMaya, iInca, iAztec, iTeotihuacan, iTiwanaku, iWari, iMississippi, iPueblo, iMuisca, iChimu, iInuit, iHaudenosaunee, iLakota, iZapotec, iPurepecha],
iCivGroupAmerica : [iAmerica, iArgentina, iMexico, iColombia, iBrazil, iCanada, iHaiti, iPeru, iVenezuela],
iCivGroupNATO : [iAmerica, iCanada, iNorse, iEngland, iFrance, iSpain, iPortugal, iNetherlands],
iCivGroupMesoamerica : [iMaya, iAztec, iTeotihuacan, iZapotec, iPurepecha],
iCivGroupAndes : [iInca, iTiwanaku, iWari, iMuisca, iChimu],
}

lNativeCivs = dCivGroups[iCivGroupNative] + [iIndigenous]

# MacAurther: Some civs are more nomadic/transient/not well known and don't have definitive city locations. For those civs, just use the city list from CIV4CivilizationInfos.xml
lTransientCivs = [iMississippi, iMuisca, iPueblo, iHaudenosaunee, iLakota]

# used in: Stability
# tech groups share techs within each other on respawn
iNumTechGroups = 3
(iTechGroupColony, iTechGroupNation, iTechGroupNative) = range(iNumTechGroups)

dTechGroups = {
iTechGroupColony : [iNorse, iSpain, iFrance, iEngland, iNetherlands, iPortugal, iRussia],
iTechGroupNation: [iAmerica, iCanada, iArgentina, iMexico, iColombia, iBrazil, iHaiti, iPeru, iVenezuela],
iTechGroupNative : [iMaya, iInca, iAztec, iTeotihuacan, iTiwanaku, iWari, iMississippi, iPueblo, iMuisca, iChimu, iInuit, iHaudenosaunee, iLakota, iHawaii, iZapotec, iPurepecha],
}

lBioNewWorld = [iMaya, iInca, iAztec, iTeotihuacan, iTiwanaku, iWari, iMississippi, iPueblo, iMuisca, iChimu, iInuit, iHaudenosaunee, iLakota, iHawaii, iZapotec, iPurepecha]
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
	(iMaya, iAztec),
	(iMaya, iMexico),
	(iMaya, iColombia),
	(iMaya, iZapotec),
	(iMaya, iTeotihuacan),
	(iZapotec, iTeotihuacan),
	(iZapotec, iMexico),
	(iZapotec, iAztec),
	(iZapotec, iPurepecha),
	(iTeotihuacan, iAztec),
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
	(iPueblo, iMexico),
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
	(iAztec, iAmerica),
	(iAztec, iMexico),
	(iAztec, iColombia),
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
	(iAztec, iZapotec),
	(iAztec, iTeotihuacan),
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
	(iMexico, iAztec),
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
iZapotec : 0,
iTeotihuacan : 0,
iTiwanaku : 110,
iWari : 500,
iMississippi : 600,
iMuisca : 800,
iNorse : 874,
iChimu : 900,
iPueblo : 950,
iPurepecha : 1150,
iInuit : 1200,
iInca : 1200,
iAztec : 1250,
iHaudenosaunee : 1450,
iSpain : 1492,
iPortugal : 1532,
iEngland : 1607,
iFrance : 1608,
iNetherlands : 1625,
iLakota : 1650,
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
iMaya : 950,
iZapotec : 800,
iTeotihuacan : 650,
iTiwanaku : 1100,
iWari : 1100,
iMississippi : 1400,
iMuisca : 1540,
iChimu : 1470,
iPueblo : 1600,
iPurepecha : 1530,
iInuit : 1700,
iInca : 1533,
iAztec : 1521,
iHaudenosaunee : 1800,
iSpain : 1825,
iPortugal : 1822,
iEngland : 1867,
iFrance : 1805,
iNetherlands : 1814,
iLakota : 1890,
iHawaii : 1893,
}, 1950)

# Leoreth: determine neighbour lists from pairwise neighbours for easier lookup
dNeighbours = dictFromEdges(lBirthCivs, lNeighbours)

# Leoreth: determine influence lists from pairwise influences for easier lookup
dInfluences = dictFromEdges(lBirthCivs, lInfluences)

dResurrections = CivDict({
}, [])

dEnemyCivsOnSpawn = CivDict({
iAztec : [iTeotihuacan],
iInca : [iTiwanaku, iWari],
iAmerica : [iEngland, iHaudenosaunee, iIndependent1, iIndependent2, iIndigenous],
iHaiti : [iFrance],
iArgentina : [iSpain, iIndependent1, iIndependent2],
iMexico : [iSpain, iIndependent1, iIndependent2],
iColombia : [iSpain, iIndependent1, iIndependent2],
iPeru : [iSpain, iIndependent1, iIndependent2],
iBrazil : [iIndependent1, iIndependent2],
iVenezuela : [iColombia],
}, [])

dTotalWarOnSpawn = CivDict({
iInca : [iWari, iTiwanaku],
iAztec : [iTeotihuacan],
}, [])

dAggressionLevel = CivDict({
iMaya : 2,
iZapotec : 1,
iTeotihuacan : 2,
iTiwanaku : 1,
iWari : 2,
iMississippi : 1,
iMuisca : 1,
iNorse : 1,
iChimu : 1,
iPueblo : 1,
iPurepecha : 2,
iInuit : 1,
iInca : 3,
iAztec : 3,
iHaudenosaunee : 2,
iSpain : 3,
iEngland : 2,
iFrance : 2,
iNetherlands : 2,
iLakota : 2,
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
iMaya : 20,
iZapotec : 20,
iTeotihuacan : 0,
iTiwanaku : 0,
iWari : 25,
iMississippi : 0,
iMuisca : 0,
iNorse : 0,
iChimu : 0,
iPueblo : 0,
iPurepecha : 0,
iInuit : 0,
iInca : 30,
iAztec : 50,
iHaudenosaunee : 100,
iSpain: 100,
iPortugal: 100,
iEngland: 0,
iFrance: 100,
iNetherlands: 100,
iRussia: 0,
iAmerica: 100,
iHaiti : 100,
iArgentina: 100,
iMexico: 100,
iColombia: 100,
iPeru : 100,
iBrazil: 100,
iVenezuela : 100,
iCanada: 100,
}, 0)

dResurrectionProbability = CivDict({
iMaya : 25,
iZapotec : 75,
iTeotihuacan : 0,
iTiwanaku : 0,
iWari : 0,
iMississippi : 75,
iMuisca : 0,
iNorse : 50,
iChimu : 0,
iPueblo : 75,
iPurepecha : 0,
iInuit : 100,
iInca : 0,
iAztec : 0,
iHaudenosaunee : 0,
iSpain : 75,
iEngland : 75,
iFrance : 75,
iNetherlands : 75,
iLakota : 50,
iHawaii : 50,
iRussia : 0,
iAmerica : 100,
iHaiti : 100,
iArgentina : 100,
iMexico : 100,
iColombia : 100,
iPeru : 100,
iBrazil : 100,
iVenezuela : 100,
iCanada : 100,
})

dPatienceThreshold = CivDict({
iMaya : 35,
iZapotec : 20,
iTeotihuacan : 20,
iTiwanaku : 20,
iWari : 20,
iMississippi : 35,
iMuisca : 35,
iNorse : 30,
iChimu : 20,
iPueblo : 35,
iPurepecha : 20,
iInuit : 35,
iInca : 35,
iAztec : 30,
iHaudenosaunee : 25,
iSpain : 20,
iPortugal : 30,
iEngland : 20,
iFrance : 20,
iNetherlands : 30,
iLakota : 30,
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
iNumReligions = 7
(iJudaism, iOrthodoxy, iCatholicism, iProtestantism, iIslam, iHinduism, iBuddhism) = range(iNumReligions)

#Persecution preference
tPersecutionPreference = (
(iHinduism, iBuddhism, iIslam, iProtestantism, iCatholicism, iOrthodoxy), # Judaism
(iIslam, iProtestantism, iCatholicism, iJudaism, iHinduism, iBuddhism), # Orthodoxy
(iIslam, iProtestantism, iOrthodoxy, iJudaism, iHinduism, iBuddhism), # Catholicism
(iIslam, iCatholicism, iOrthodoxy, iJudaism, iHinduism, iBuddhism), # Protestantism
(iHinduism, iProtestantism, iCatholicism, iOrthodoxy, iJudaism, iBuddhism), # Islam
(iIslam, iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iBuddhism), # Hinduism
(iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iIslam, iHinduism), # Buddhism
)

# pagan religions
iNumPaganReligions = 13
# 0				1				2				3				4				5				6				7				8				9
(iAngakkuq, 	iAsatru, 		iAtua, 			iDruidism, 		iGaiwiio,		iInti, 			iKachina,		iMidewiwin, 	iRodnovery, 	iTeotlMaya, 
iTeotlAztec, 	iWocekiya,		iYoruba) = range(iNumPaganReligions)

iPaganVictory = iNumReligions
iSecularVictory = iNumReligions + 1

# Culture Groups
iNumCultureGroups = 3
iCultureGroupNone = -1
(iCultureGroupNative, iCultureGroupColony, iCultureGroupNation) = range(iNumCultureGroups)

# corporations
iNumCorporations = 8
(iTrappingIndustry, iWestIndiesCompany, iCerealIndustry, iFishingIndustry, iTextileIndustry, iSteelIndustry, iOilIndustry, iLuxuryIndustry) = range(iNumCorporations)

# initialise tech variables to unit indices from XML

iNumTechs = 153
#				2				3				4				5				6				7
(iHunting,		iIrrigation,	iHerbalism,  	iCultivation,	iLinguistics,	iLandmarks,		iDiving,
iTrapping,      iKnapping,		iEarthworks,    iCompanionPlanting,iLocalization,iPathfinding,  iFishing,
iTanning, 		iMining, 		iPottery, 		iAgriculture, 	iPastoralism, 	iMythology, 	iDugouts,
iSmelting,      iMasonry,       iProperty,      iArithmetics,   iCeremony,      iDivination,    iNavigation,
iGeneralship,	iConstruction,  iMathematics,   iAstronomy,     iWriting,       iPriesthood,    iTradeRoutes,
iAlloys,   		iCement,        iAesthetics,    iCalendar,   	iCodices,       iPhilosophy,    iSeafaring,
iNorthEuropeAccess,iSubjugation,iArtisanry,     iScholarship,	iLaw,           iNobility,      iContact,
iSouthEuropeAccess,iMedievalTactics,iContinuance,iMedievalScience,iStewardship,iMedievalCulture,iRiding,
iGunpowder, 	iCompanies, 	iFinance, 		iCartography, 	iExchange, 		iReductions,	iEvangelism,
iFirearms, 		iTriangularTrade,iExploration, 	iOptics, 		iTreaties, 		iOfficials, 	iIndoctrination,
iFortification,	iEconomics, 	iColonization, 	iShipbuilding, 	iEducation,		iCharter, 		iIndentures,
iCombinedArms, 	iLogistics,		iExploitation, 	iTimekeeping, 	iCommunity, 	iPolitics, 		iHorticulture,
iTactics,		iCurrency,		iGeography,		iScientificMethod,iUrbanPlanning,iStatecraft,	iSocialContract,
iSiberiaAccess, iFreeMarket,	iAutonomy,		iAcademia, 		iModernization,	iIndependence,	iJudiciary,		
iReplaceableParts,iNewspapers,	iMeteorology,	iSociology,		iSurveying,		iRepresentation,iHeritage,
iMetallurgy,	iPostalService,	iHydrology,		iPhysics,		iPioneering,	iArchitecture, 	iHumanities,
iMachineTools, 	iThermodynamics, iEngineeing, 	iChemistry, 	iGeology,		iNationalism, 	iCivilLiberties,
iMeasurement, 	iEngine, 		iRailroad, 		iElectricity, 	iConservation, 	iDoctrine, 		iEmancipation,
iBallistics,	iAssemblyLine,	iCombustion,	iTelegraph,		iBiology,		iLaborUnions,	iJournalism,
iFlight,		iMacroeconomics,iInfrastructure,iRadio,			iEcology,		iPowerProjection,iPsychology,
iAviation,		iGlobalism,		iFission,		iSynthetics,	iSocialServices,iCivilRights,	iTelevision,
iRocketry,		iNuclearPower,	iAfricaAccess,	iRadar,			iAsiaAccess,
iMultilateralism) = range(iNumTechs)

# Techs that Natives start the game with, but Europeans have to trade for
lNativeTechs = [iHunting, iLandmarks, iIrrigation, iLinguistics, iCultivation, iKnapping, iDiving,
                iTrapping, iPathfinding, iEarthworks, iLocalization, iCompanionPlanting, iHerbalism, iFishing]
# Techs that allow immigration in certain regions
lImmigraitonTechs = [iNorthEuropeAccess, iSouthEuropeAccess, iAfricaAccess, iSiberiaAccess, iAsiaAccess]

# initialise unit variables to unit indices from XML

iNumUnits = 144
# Land Units (94)
# 0				1				2				3				4				5				6				7				8				9
(iGrizzlyBear, 	iPolarBear,		iPanther, 		iJaguar,		iCougar,		iWolf, 			iCoyote,		iClawdius,		iSettler, 		iDogSled,		
iPioneer,		iWorker, 		iArtisan,		iPromyshlenniki,iTrackman,		iLaborer, 		iMadeireiro, 	iSpy, 			iSisqeno,       iAgent,			
iInquisitor,	iOrthodoxMiss, 	iCatholicMiss, 	iProtestantMiss,iImmigrant,		iScout, 		iPathfinder,	iExplorer, 		iBandeirante, 	iCoureurDesBois,
iRanger,		iFactor,		iParatrooper,	iMilitia,		iFalconDancer,	iMinuteman,		iWarrior, 		iKoa,			iTomahawk,		iSwordsman,		
iAztecJaguar,	iAxeman,		iMaceman,		iAucac,			iQuangariecha,	iArquebusier,	iMohawk,		iArmedSlave,	iMusketman,		iCompagnies,	
iFusilier,		iRedcoat,		iGuardia,		iRifleman,		iVencedores,	iInfantry,		iFARs,			iSpearman,		iXhisxyag,		iPikeman,		
iHalberdier,	iEagle,			iTercio,		iAntiTank,		iArcher,		iGuecha,		iCrossbowman,	iGatlingGun,	iMachineGun,	iSkirmisher,	
iHolkan,		iSlinger,		iLongbowman,	iIrregular,		iCacos,			iGrenadier,		iAlbionLegion,	iMarine,		iHorseArcher,	iSwiftArrow,	
iCuirassier,	iConquistador,	iDragoon,		iLlanero,		iCavalry,		iGrenadierCavalry,iRural,		iLightTank,		iTank,			iBombard,		
iCannon,		iArtillery,		iHowitzer,		iAAGun,		

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
# Other Units (2)
# 0				1				2				3				4				5				6				7				8				9
iSlave,			iChattleSlave) = range(iNumUnits)

lAnimalUnits = [iGrizzlyBear, 	iPolarBear,		iPanther, 		iJaguar,		iCougar,		iWolf, 			iCoyote]
lSlaveUnits = [iSlave, iChattleSlave]
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


iNumUnitRoles = 27
# 0				1				2				3				4				5				6				7				8				9
(iBase, 		iDefend, 		iAttack, 		iCounter, 		iShock, 		iHarass, 		iCityAttack, 	iWorkerSea, 	iSettle, 		iSettleSea, 
iAttackSea, 	iAssaultSea, 	iWorkSea,		iMissionarySea,	iSlaveSea,		iFerry, 		iEscort, 		iExplore, 		iShockCity, 	iSiege, 		
iCitySiege, 	iExploreSea, 	iSkirmish, 		iLightEscort, 	iWork, 			iMissionary,	iSpyRole) = range(iNumUnitRoles)

iNumPromotions = 89
# 0				1				2				3				4				5				6				7				8				9
(iCombat1,		iCombat2,		iCombat3,		iCombat4,		iCombat5,		iCombat6,		iCover,			iShockPromo,	iPinch,			iFormation,
iCharge,		iAmbush,		iSkirmishPromo,	iAmphibious,	iMarch,			iBlitz,			iCommando,		iMedic1,		iMedic2,		iMedic3,		
iGuerilla1,		iGuerilla2,		iGuerilla3,		iWoodsman1,		iWoodsman2,		iWoodsman3,		iFlanking1,		iFlanking2,		iFlanking3,		iCityRaider1,		
iCityRaider2,	iCityRaider3,	iCityGarrison1,	iCityGarrison2,	iCityGarrison3,	iDrill1,		iDrill2,		iDrill3,		iDrill4,		iBarrage1,		
iBarrage2,		iBarrage3,		iAccuracy,		iDisengage1,	iDisengage2,	iRiverCombat,	iSentry,		iMobility,		iNavigation1,	iNavigation2,	
iRange1,		iRange2,		iInterception1,	iInterception2,	iAce,			iLogistics1,	iLogistics2,	iLogistics3,	iDeception1,	iDeception2,	iDeception3,
iSecurity1,		iSecurity2,		iSecurity3,		iImprovise1,	iImprovise2,	iImprovise3,	iImprovise4,	iImprovise5,	iLoyalty,		iInstigator1,
iInsitgator2,	iInstigator3,	iAlchemist1,	iAlchemist2,	iEscape1,		iEscape2,		iLeader,		iLeadership,	iTactics,		iMorale,
iMercenary,		iDesertAdaptation,iPrairieAdaptation,iVolunteer,iReconnaissance,iSwampFox1,		iSwampFox2,		iSwampFox3) = range(iNumPromotions)

# initialise bonuses variables to bonuses IDs from WBS
iNumBonuses = 49
# 0				1				2				3				4				5				6				7				8				9
(iAluminium, 	iBison,			iCitrus,		iCoal, 			iCopper, 		iHorse, 		iIron, 			iMarble, 		iOil, 			iStone, 		
iUranium, 		iBanana, 		iClam, 			iCorn, 			iCow, 			iCrab,			iDeer, 			iFish, 			iPig, 			iPotato,		
iRice, 			iSheep, 		iLlama,			iWheat, 		iCocoa,			iCoffee, 		iCotton,		iDye, 			iFur,			iGems, 			
iGold, 			iIncense, 		iJade,			iObsidian,		iPearls, 		iRubber,		iSalt,			iSeal,			iSilver, 		iSpices,
iSugar,			iTea, 			iTimber,		iTobacco, 		iWine, 			iWhales, 		iSoccer, 		iSongs, 		iMovies) = range(iNumBonuses)

iNumBonusVarieties = 10
# 0				1				2				3				4				5				6				7				8				9
(iDyeCochineal, iSpicesVanilla, iGemsTurquoise, iGemsDiamonds,	iGemsEmeralds,	iSheepBlack,	iCowBrown,		iPigFurry,		iCitrusOranges, iCrabShrimp) = range(iNumBonuses, iNumBonuses + iNumBonusVarieties)

# Buildings
iNumBuildings = 210
# Buildings (117)
# 0				1				2				3				4				5				6				7				8				9
(iPalace,		iPalaceZapotec,	iChieftansHut,	iGovernorsMansion,iCapitol,		iGranary,		iQollqa,		iSmokehouse,	iLuau,			iTipi,			
iTannery,		iIgloo,			iLonghouse,		iKiln,			iArena,			iBallCourt,		iSambadrome,	iBarracks,		iKallanka,		iHerbalist,		
iKuna,			iWeaver,		iPaganTemple,	iAqueduct,		iSukaQullu,		iBath,			iTemazcal,		iCompound,		iKancha,		iTomb,			
iMarket,		iStoneworks,	iJeweller,		iGoldsmith,		iPlaza,			iPlatformMound,	iKiva,			iAltar,			iTzompantli,	iYacatas,		
iHarbor,		iConstabulary,	iRoyalMountedPolice,iTradingPost,iHuntingPost,	iForge,			iTavern,		iStable,		iPalisade,		iFactorij,		
iMonument,		iSchoolhouse,	iCalmecac,		iGrocer, 		iCourthouse,	iAssembly,		iThingvellir,	iWharf,			iLighthouse,	iWarehouse,		
iSilversmith,	iMagazine,		iStarFort,		iCitadelle,		iEstate,		iHacienda,		iUniversity,	iPharmacy,		iDistillery,	iPostOffice,	
iTambo,			iWheelwright,	iCustomsHouse,	iFeitoria,		iBank,			iLevee,			iSeigneur,		iTheatre,		iShipyard,		iObservatory,	
iPrintingPress,	iMeetingHall,	iStateHouse,	iSlaughterhouse,iColdStoragePlant,iSewer,		iJail,			iImmigrationOffice,iRailwayStation,iTextileMill,
iWoolMill,		iSteelMill,		iRefinery,		iRodeo,			iCharreada,		iArsenal,		iDrydock,		iNewspaper,		iSupermarket,	iHospital,		
iIntelligenceAgency,iAirport,	iHotel,			iDepartmentStore,iMall,			iElectricalGrid,iFactory,		iMaquiladora,	iCoalPlant,		iHydroPlant,	
iIndustrialPark,iNuclearPlant,	iPark,			iStadium,		iBunker,		iLaboratory,	iBroadcastTower,
# Religious Buildings (29)
# 0				1				2				3				4				5				6				7				8				9
iJewishTemple, iJewishCathedral,iJewishMonastery,iJewishShrine, iOrthodoxTemple,iOrthodoxCathedral,iOrthodoxMonastery,iOrthodoxShrine,iCatholicTemple,iCatholicCathedral, 
iCatholicMonastery,iMission,	iCatholicShrine,iProtestantTemple,iProtestantCathedral,iProtestantMonastery,iProtestantShrine,iIslamicTemple,iIslamicCathedral,iIslamicMonastery, 
iIslamicShrine, iHinduTemple, 	iHinduCathedral, iHinduMonastery,iHinduShrine, iBuddhistTemple, iBuddhistCathedral,iBuddhistMonastery,iBuddhistShrine,
# Great Buildings (6)
# 0				1				2				3				4				5				6				7				8				9
iAcademy, 		iAdministrativeCenter, iManufactory, iArmoury, 	iMuseum, 		iStockExchange, 
# Great Buildings/National Wonders (12)
# 0				1				2				3				4				5				6				7				8				9
iNationalMonument,iNationalTheatre,iNationalGallery,iNationalCollege,iMilitaryAcademy,iSecretService,iIronworks,iRedCross,		iNationalPark,	iCentralBank, 	
iGrandCentralStation,iSupremeCourt,
# Great Wonders (46)
# 0				1				2				3				4				5				6				7				8				9
iFloatingGardens,iTempleOfKukulkan,iMachuPicchu,iPuebloBonito,	iSacsayhuaman,	iHueyTeocalli,	iTlachihualtepetl,iYachaywasi,	iGateOfTheSun,	iGreatGeoglyph,	
iKalasasaya,	iPyramidOfTheSun,iSerpentMound,	iTemblequeAqueduct,iLaFortaleza,iSaoFranciscoSquare,iGuadalupeBasilica,iManzanaJesuitica,iIndendenceHall,iHospicioCabanas,
iMountVernon,	iMonticello,	iSlaterMill,	iChapultepecCastle,iFortMcHenry,iWashingtonMonument,iFaneuilHall,iStatueOfLiberty,iCentralPark,	iEllisIsland,	
iBrooklynBridge,iChateauFrontenac,iMenloPark,	iBiltmoreEstate,iFrenchQuarter, iLeagueOfNations,iEmpireStateBuilding,iGoldenGateBridge,iHooverDam,iAlcatraz,		
iMountRushmore,	iHollywood,		iSaltCathedral,iCristoRedentor,	iLasLajasSanctuary,iPentagon	) = range(iNumBuildings)


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
(iElders,		iChief,			iDespot,		iMonarch,		iAristocrats,	iGodKing,		iCouncil,		
iDecentralization,iClans,		iCityStates,	iTribalConfederacy,iBureaucracy,iVassalage,		iFirstNation,
iTraditionalism,iSubsistance,	iTlacotin,		iMita,			iCraftsmen,		iCasteSystem,	iGuilds,	
iReciprocity,	iCalpulli,		iRedistribution,iMindalaes,		iRaiding,		iDependency,	iTourism,
iAnimism,		iHarmony,		iSacrifice,		iOrganizedReligion,iCosmopolitans,iAcculturation,iGhostDance,
iSettlement,	iNomads,		iIsolationism,	iConquest,		iIntegration,	iTributaries,	iAncestralLands,
# Colony
iCaptains,		iProprietors,	iViceroys,		iTrustees,		iGovernors,		iColonialAssembly,iHomeRule,
iExpedition,	iAdmiralty,		iCharterColony,	iTradingCompany,iRoyalColony,	iSecretariate,	iCommonwealth,	
iSerfdom,		iEncomienda,	iIndenturedServitude,iSlavery,	iConscription,	iPenalColony,	iApprenticeship,
iGoldRush,		iPlunder,		iExtraction,	iFactoryCivic,	iPlantationCivic,iMercantilism,	iCustomsUnion,
iDivineRight,	iJesuits,		iPatronato,		iHaven,			iCastas,		iCreolism,		iEmancipation,
iClaims,		iImperialism,	iGrants,		iOutposts,		iProvidence,	iIntervention,	iDependencies,
# Nation
iStrongman,		iJunta,			iSovereign,		iPlutocrats,	iRepresentatives,iDictator,		iStateParty,
iMinarchy,		iMartialLaw,	iConfederacy,	iFederalism,	iKleptocracy,	iUnitary,		iPoliceState,
iRuralism,		iBondage,		iSharecropping,	iIndustrialism,	iImmigrantLabor,iLaborUnions,	iMechanization,
iLaissezFaire,	iAgrarianism,	iFreeEnterprise,iProtectionism,	iConsumerism,	iDefenseComplex,iPublicWelfare,
iRevolution,	iLibertarianism,iProfiteering,	iOpportunity,	iSegregation,	iNativism,		iEgalitarianism,
iDisplacement,	iHomesteads,	iAssimilation,	iManifestDestiny,iDecolonization,iNationhood,	iHegemony) = range(iNumCivics)

iNumCivicCategories = 6
(iCivicsExecutive, iCivicsAdministration, iCivicsLabor, iCivicsEconomy, iCivicsSociety, iCivicsExpansion) = range(iNumCivicCategories)

iNumCivicsPerCategory = 7


#Specialists
iNumSpecialists = 17
#				            2				            3				            4				            5
(iSpecialistCitizen,        iSpecialistPriest,          iSpecialistArtist,          iSpecialistScientist,       iSpecialistMerchant,
iSpecialistEngineer,        iSpecialistStatesman,       iSpecialistGreatProphet,    iSpecialistGreatArtist,     iSpecialistGreatScientist, 
iSpecialistGreatMerchant,   iSpecialistGreatEngineer,   iSpecialistGreatStatesman,  iSpecialistGreatGeneral,    iSpecialistGreatSpy,
iSpecialistSlave,			iSpecialistImmigrant) = range(iNumSpecialists)

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
iNumRegions = 53
# 0				1				2				3				4				5				6				7				8				9
(rAlaska, 		rYukon,         rNunavut, 		rGreenland,     rIceland,       rNorthCascadia, rNorthPlains, 	rOntario, 		rQuebec, 		rNewFoundland, 	
rSouthCascadia, rCalifornia,    rRockies,       rSouthwest,     rTexas,         rGreatPlains,   rGreatLakes,    rNewEngland,    rMidAtlantic,   rMaryland,
rAppalachia,    rCoastalPlain,  rDeepSouth,     rFlorida,       rBajaCalifornia,rSierraMadres,  rBajio,         rVeracruz,      rOaxaca,        rYucatan,       
rMesoamerica,   rCaribbean, 	rHawaii, 		rColombia, 		rEcuador,		rVenezuela, 	rGuyana, 		rPeru, 			rBolivia, 		rAmazonas, 		
rPara,          rBahia,         rMinasGerais,   rMatoGrosso,    rParana,        rChile, 		rParaguay, 		rUruguay, 		rChaco,         rCuyo,          
rPampas, 		rPatagonia, 	rOldWorld		) = range(iNumRegions)

iNumWaterRegions = 44
# 0				1				2				3				4				5				6				7				8				9
(rArcticO,		rBaffinB,		rNorthwestPassage,rHudsonB,		rLabradorS,		rNorthAtlanticO,rGOfMexico,		rCaribbeanS,	rSouthAtlanticO,rSouthPacificO,
rNorthPacificO,	rGOfCalifornia,rGOfAlaska,		rBeringS,		rGreatBearL,	rGreatSlaveL,	rLAthabasca,	rLWinnipegosis,	rLWinnipeg,		rGOfStLawrence,
rLOntario,		rLErie,			rLHuron,		rLSuperior,		rLMichigan,		rPugetSound,	rGreatSaltL,	rLTahoe,		rLOkeechobee,	rLTexcoco,		
rLMaracaibo,	rLTiticaca,		rSmallLake,		rStLawrenceR,	rColumbiaR,		rMississippiR,	rMissouriR,		rOhioR,			rAmazonR,		rXinguR,		
rTocantinsR,	rAtlanticO,		rPacificO,		rDeepOcean,		
 ) = range(100, 100 + iNumWaterRegions)

lCanadaAtlanticCoast = [rQuebec, rNewFoundland]
lCanadaPacificCoast = [rNorthCascadia]
lCanada = [rYukon, rNunavut, rNorthCascadia, rNorthPlains, rOntario, rQuebec, rNewFoundland]
lThirteenColonies = [rNewEngland, rMidAtlantic, rMaryland, rCoastalPlain]
lSouthernUS = [rCoastalPlain, rFlorida, rTexas, rDeepSouth]
lBorderStates = [rMaryland, rAppalachia]
lLouisianaPurchase = [rGreatLakes, rAppalachia, rDeepSouth, rCoastalPlain, rFlorida, rTexas, rGreatPlains]
lContinentalUS = [rSouthCascadia, rCalifornia, rRockies, rSouthwest, rTexas, rGreatPlains, rGreatLakes, rNewEngland, rMidAtlantic, rMaryland, rAppalachia, rCoastalPlain, rDeepSouth, rFlorida]
lUnitedStates = lContinentalUS + [rAlaska, rHawaii]
lMexico = [rBajaCalifornia, rSierraMadres, rBajio, rVeracruz, rOaxaca, rYucatan]
lBrazil = [rAmazonas, rPara, rBahia, rMinasGerais, rMatoGrosso, rParana,]
lArgentina = [rChaco, rCuyo, rPampas, rPatagonia]
lAndes = [rColombia, rEcuador, rPeru, rBolivia, rChile]

lSouthAmerica = [rColombia, rEcuador, rVenezuela, rGuyana, rPeru, rBolivia, rChile, rParaguay, rUruguay] + lArgentina + lBrazil
lCentralAmerica = [rMesoamerica, rCaribbean]
lLatinAmerica = lCentralAmerica + lMexico + lSouthAmerica
lNorthAmerica = lCanada + lContinentalUS + [rAlaska] + lMexico

lAmerica = lSouthAmerica + lCentralAmerica + lNorthAmerica
lWest = lAmerica + [rHawaii, rGreenland]

dCivGroupRegions = {
	iCivGroupEurope: lWest,
	iCivGroupNative: lAmerica,
	iCivGroupAmerica: lAmerica,
	iCivGroupNATO: lAmerica,
	iCivGroupMesoamerica: lMexico,
	iCivGroupAndes: lAndes,
}

# Revealed Tile Lists
lInuitRevealedTiles = [rBeringS]
lInuitRevealedTilesAI = [rBeringS, rArcticO, rNorthwestPassage, rHudsonB, rAlaska, rYukon, rNunavut, rGreenland]
lEuropeanRevealed1600AD = [rIceland, rNewFoundland, rNewEngland, rMidAtlantic, rMaryland, rCoastalPlain, rFlorida, rBajio, \
                           rVeracruz, rOaxaca, rYucatan, rMesoamerica, rCaribbean, rColombia, rEcuador, rVenezuela, rGuyana, rPeru, \
                           rMinasGerais, rParana, rChile, rUruguay, rPampas, rPatagonia, rBaffinB, rLabradorS, rNorthAtlanticO, rGOfMexico, 
                           rCaribbeanS, rSouthAtlanticO, rAtlanticO]
lEuropeanRevealed1750AD = [rGreenland, rIceland, rOntario, rQuebec, rNewFoundland, rCalifornia, rTexas, rGreatLakes, rNewEngland, rMidAtlantic, \
                           rMaryland, rAppalachia, rCoastalPlain, rDeepSouth, rFlorida, rBajaCalifornia, rSierraMadres, rBajio, rVeracruz, rOaxaca, \
                           rYucatan, rMesoamerica, rCaribbean, rColombia, rEcuador, rVenezuela, rGuyana, rPeru, rBolivia, rBahia, \
                           rMinasGerais, rMatoGrosso, rParana, rChile, rParaguay, rUruguay, rChaco, rCuyo, rPampas, rPatagonia, \
                           rArcticO, rBaffinB, rNorthwestPassage, rHudsonB, rLabradorS,	rNorthAtlanticO, rGOfMexico, rCaribbeanS, rSouthAtlanticO, rSouthPacificO, \
						   rNorthPacificO, rGOfCalifornia, rGOfAlaska, rBeringS, rAtlanticO, rPacificO]
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

iNumFeatures = 23
# 0				1				2				3				4				5				6				7				8				9
(iSeaIce, 		iJungle, 		iCenote, 		iFloodPlains, 	iForest, 		iBog, 			iSwamp, 		iCape, 			iIslands, 		iRainforest, 
iFallout, 		iTaiga, 		iPalmForest,	iCanyon,		iReef,			iScrub,			iStraight,		iStraightIslands,iTradewindNorthEurope,iTradewindSouthEurope,
iTradewindAfrica,iTradewindSiberia,iTradewindAsia) = range(iNumFeatures)

iTradeWindsStart = iTradewindNorthEurope

iNumTerrains = 22
# 0				1				2				3				4				5				6				7				8				9
(iGrass, 		iPlains, 		iDesert, 		iTundra, 		iSnow, 			iCoast, 		iOcean, 		iTerrainPeak, 	iTerrainHills, 	iMarsh,
iLagoon,		iArcticCoast,	iSemidesert,	iPrairie,		iMoorland,		iSaltflat,		iSaltlake,		iAtoll,			iSavanna,		iWideRiver,
iFjord,			iDeepOcean) = range(iNumTerrains)


#Plague
iImmunity = 20

# Victory
iVictoryPaganism = 7
iVictorySecularism = 8


#leaders
iNumLeaders = 68
# 0				1				2				3				4				5				6				7				8				9
(iLeaderBarbarian,iNativeLeader,iIndependentLeader,iPacal,		iXoc,			iCosijoeza,		iAtlatlCauac,	iMalkuHuyustus,	iWariCapac,		iUwahcil,		
iTuskaloosa,	iKochininako,	iPopay,			iSaguamanchica,	iLiefErickson,	iGustav,		iGerhardsen,	iTacaynamo,		iTopiltzin,		iAua,			
iCunhambebe,	iAgueybana,		iPachacuti,		iHuaynaCapac,	iErendira,		iMontezuma,		iMangasColoradas,iHiawatha,		iSittingBull,   iIsabella,		
iPhilip,		iFranco,		iOconostota,	iJoao,			iMaria,			iElizabeth,		iVictoria,		iChurchill,		iLouis,			iNapoleon,		
iDeGaulle,		iWillemVanOranje,iWilliam,		iKamehameha,	iCatherine,		iAlexanderI,	iStalin,		iWashington,	iJackson,		iLincoln,		
iRoosevelt,		iFDR,			iKennedy,		iReagan,		iObama,			iLOuverture,	iSanMartin,		iPeron,			iJuarez,		iSantaAnna,		
iCardenas,		iBolivar,		iCastilla,		iPedro,			iVargas,		iChavez,		iMacDonald,		iTrudeau) = range(iNumLeaders)

dResurrectionLeaders = CivDict({
})

iNumPeriods = 0
#() = range(iNumPeriods)

iNumImpacts = 5
(iImpactMarginal, iImpactLimited, iImpactSignificant, iImpactCritical, iImpactPlayer) = range(iNumImpacts)

lSecondaryCivs = [iChimu, iHaiti, iHawaii, iInuit, iHaudenosaunee, iMississippi, iMuisca, iNorse, iPeru, iPueblo, iVenezuela, iWari, iLakota]

(i500BC, i1500AD, i1750AD) = range(3)

# Stability overlay and editor
iNumPlotStabilityTypes = 4
(iCoreArea, iHistoricalArea, iConquestArea, iForeignArea) = range(iNumPlotStabilityTypes)
lStabilityColors = ["COLOR_CYAN", "COLOR_GREEN", "COLOR_YELLOW", "COLOR_RED"]
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


# MacAurther: Update this if more hurry types are added
iNumHurries = 3
(iHurryPopulation,	iHurryGoldUnits, iHurryGoldBuilding) = range(iNumHurries)

# Immigration Homelands
iNumImmigrationHomelands = 5
(iHomelandNorthEurope, iHomelandSouthEurope, iHomelandAfrica, iHomelandSiberia, iHomelandAsia) = range(iNumImmigrationHomelands)
lHomelandsEurope = [iHomelandNorthEurope, iHomelandSouthEurope]
lHomelandsEuropePlus = lHomelandsEurope + [iHomelandSiberia]
lHomelands = lHomelandsEuropePlus + [iHomelandAfrica, iHomelandAsia]

iEndDate = 2050
# Immigrant Schedule
dImmigrantSchedule = {
iSettler : 				[(850, iEndDate), 	lHomelands],
iDogSled : 				[(-5000, 1500), 	[iHomelandSiberia]],
iPioneer : 				[(1850, iEndDate), 	lHomelands],
iWorker : 				[(850, iEndDate),   [iHomelandNorthEurope, iHomelandSouthEurope, iHomelandAfrica]],
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
iCoureurDesBois : 		[(1620, 1800), 		lHomelandsEurope],
iRanger : 				[(1800, 1930), 		lHomelands],
iFactor : 				[(1800, 1930), 		[iHomelandNorthEurope]],
iParatrooper : 			[(1930, iEndDate), 	lHomelandsEuropePlus],
iKoa : 					[(0, 	1800), 		[iHomelandAsia]],
iArquebusier : 			[(1500, 1550), 		lHomelandsEurope],
iMusketman : 			[(1550, 1700), 		lHomelandsEurope],
iCompagnies : 			[(1550, 1700), 		lHomelandsEurope],
iFusilier : 			[(1700, 1800), 		lHomelandsEuropePlus],
iRifleman : 			[(1800, 1900), 		lHomelandsEuropePlus],
iInfantry : 			[(1900, iEndDate), 	lHomelandsEuropePlus],
iPikeman : 				[(1500, 1550), 		lHomelandsEurope],
iTercio : 				[(1550, 1700), 		[iHomelandSouthEurope]],
iRedcoat : 				[(1700, 1800), 		[iHomelandNorthEurope]],
iAntiTank : 			[(1930, iEndDate), 	lHomelandsEuropePlus],
iCrossbowman : 			[(1500, 1550), 		lHomelandsEurope],
iGatlingGun : 			[(1850, 1900), 		lHomelandsEuropePlus],
iMachineGun : 			[(1900, 1950), 		lHomelandsEuropePlus],
iIrregular : 			[(1550, 1700), 		lHomelandsEurope],
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
iCannon : 				[(1600, 1800), 		lHomelandsEurope],
iArtillery : 			[(1800, 1900), 		lHomelandsEuropePlus],
iHowitzer : 			[(1900, iEndDate), 	lHomelandsEuropePlus],
iAAGun : 				[(1930, iEndDate), 	lHomelandsEuropePlus],
iLongship : 			[(850,  1450), 		[iHomelandNorthEurope]],
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
iChattleSlave:			[(1530, 1808), 		[iHomelandAfrica]],
}