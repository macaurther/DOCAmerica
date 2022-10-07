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
iNumCivs = 22
#				2				3				4				5				6				7				8				9				10
(iAmerica, 		iArgentina, 	iAztecs, 		iBrazil, 		iCanada, 		iColombia, 		iEngland, 		iFrance, 		iHawaii,		iInca,
iMaya,			iMexico, 		iNativeAmericans, iNetherlands, iPortugal, 		iRussia,		iSpain, 		iIndependent, 	iIndependent2, 	iNative,
iMinor, iBarbarian) = tuple(Civ(i) for i in range(iNumCivs))

lBirthOrder = [
	iMaya,
	iInca,
	iAztecs,
	iSpain,
	iPortugal,
	iEngland,
	iFrance,
	iNetherlands,
	iHawaii,
	iRussia,
	iAmerica,
	iArgentina,
	iMexico,
	iColombia,
	iBrazil,
	iCanada
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
iCivGroupEurope : [iSpain, iFrance, iEngland, iNetherlands, iPortugal, iRussia],
iCivGroupNativeAmerica : [iMaya, iInca, iAztecs],
iCivGroupAmerica : [iAmerica, iArgentina, iMexico, iColombia, iBrazil, iCanada]
}

# used in: Stability
# tech groups share techs within each other on respawn
iNumTechGroups = 2
(iTechGroupWestern, iTechGroupNativeAmerica) = range(iNumTechGroups)

dTechGroups = {
iTechGroupWestern : [iSpain, iFrance, iEngland, iNetherlands, iPortugal, iRussia, iAmerica, iArgentina, iMexico, iColombia, iBrazil, iCanada],
iTechGroupNativeAmerica : [iMaya, iInca, iAztecs],
}

lBioNewWorld = [iMaya, iInca, iAztecs]

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
iNumMinorCities = 2

# scripted conquerors
iNumConquests = 0

lNeighbours = [
	(iMaya, iAztecs),
	(iMaya, iMexico),
	(iMaya, iColombia),
	(iInca, iArgentina),
	(iInca, iColombia),
	(iInca, iBrazil),
	(iAztecs, iAmerica),
	(iAztecs, iMexico),
	(iAztecs, iColombia),
	(iSpain, iFrance),
	(iSpain, iPortugal),
	(iEngland, iNetherlands),
	(iFrance, iEngland),
	(iFrance, iNetherlands),
	(iRussia, iAmerica),
	(iRussia, iCanada),
	(iAmerica, iMexico),
	(iAmerica, iCanada),
	(iArgentina, iBrazil),
	(iMexico, iColombia),
]

lInfluences = [
	(iMaya, iSpain),
	(iInca, iSpain),
	(iAztecs, iSpain),
	(iNetherlands, iSpain),
	(iAmerica, iEngland),
	(iAmerica, iFrance),
	(iAmerica, iNetherlands),
	(iArgentina, iSpain),
	(iMexico, iSpain),
	(iMexico, iFrance),
	(iColombia, iSpain),
	(iBrazil, iPortugal),
	(iCanada, iFrance),
	(iCanada, iEngland),
]

dBirth = CivDict({
iMaya : 250,
iInca : 1100,
iAztecs : 1250,
iSpain : 1496,
iPortugal : 1532,
iEngland : 1607,
iFrance : 1608,
iNetherlands : 1625,
iHawaii : 1650,
iRussia: 1743,
iAmerica : 1775,
iArgentina : 1810,
iMexico : 1810,
iColombia : 1810,
iBrazil : 1822,
iCanada : 1867,
}, 250)

lBirthCivs = dBirth.keys()

dFall = CivDict({
iMaya : 900,
iInca : 1533,
iAztecs : 1521,
}, 2020)

# Leoreth: determine neighbour lists from pairwise neighbours for easier lookup
dNeighbours = dictFromEdges(lBirthCivs, lNeighbours)

# Leoreth: determine influence lists from pairwise influences for easier lookup
dInfluences = dictFromEdges(lBirthCivs, lInfluences)

dResurrections = CivDict({
iMaya : [(1800, 2020)],
iInca : [(1800, 1930)],
iSpain : [(1700, 2020)],
iPortugal : [(1700, 2020)],
iEngland : [(1700, 2020)],
iFrance : [(1700, 2020)],
iNetherlands : [(1700, 2020)],
iAmerica : [(1776, 2020)],
iArgentina : [(1810, 2020)],
iMexico : [(1810, 2020)],
iColombia : [(1810, 2020)],
iBrazil : [(1820, 2020)],
iCanada : [(1867, 2020)],
}, [])

dEnemyCivsOnSpawn = CivDict({
iAztecs : [iMaya],
iAmerica : [iIndependent, iIndependent2],
iArgentina : [iSpain, iSpain, iIndependent, iIndependent2],
iMexico : [iSpain, iSpain, iIndependent, iIndependent2],
iColombia : [iSpain, iSpain, iIndependent, iIndependent2],
iBrazil : [iIndependent, iIndependent2],
}, [])

dTotalWarOnSpawn = CivDict({
iAztecs : [iMaya],
}, [])

dAggressionLevel = CivDict({
iMaya : 1,
iInca : 1,
iAztecs : 2,
iSpain : 2,
iEngland : 1,
iFrance : 1,
iRussia : 1,
iAmerica : 2,
iColombia : 2,
iMexico : 1,
iArgentina : 1,
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
iMaya : 30,
iInca : 70,
iAztecs : 70,
iSpain : 100,
iPortugal : 100,
iEngland : 100,
iFrance : 100,
iNetherlands : 100,
iAmerica : 100,
iArgentina : 100,
iMexico : 100,
iColombia : 80,
iBrazil : 100,
iCanada : 100,
})

dPatienceThreshold = CivDict({
iMaya : 35,
iInca : 35,
iAztecs : 30,
iSpain : 20,
iPortugal : 30,
iEngland : 20,
iFrance : 20,
iNetherlands : 30,
iAmerica : 30,
iArgentina : 40,
iMexico : 40,
iColombia : 30,
iBrazil : 40,
iCanada : 40,
}, 100)

dMaxColonists = CivDict({
iSpain : 7,
iPortugal : 6,
iEngland : 6, 
iFrance : 5,
iNetherlands : 6,
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
iNumPaganReligions = 19
(iAnunnaki, iAsatru, iAtua, iBaalism, iBon, iDruidism, iInti, iMazdaism, iMugyo, iOlympianism, 
iPesedjet, iRodnovery, iShendao, iShinto, iTengri, iTeotlMaya, iTeotlAztec, iVedism, iYoruba) = range(iNumPaganReligions)

iPaganVictory = iNumReligions
iSecularVictory = iNumReligions + 1

# corporations
iNumCorporations = 9
(iSilkRoute, iTradingCompany, iCerealIndustry, iFishingIndustry, iTextileIndustry, iSteelIndustry, iOilIndustry, iLuxuryIndustry, iComputerIndustry) = range(iNumCorporations)

# initialise tech variables to unit indices from XML

iNumTechs = 141
(iTanning, iMining, iPottery, iPastoralism, iAgriculture, iMythology, iSailing,
iSmelting, iMasonry, iLeverage, iProperty, iCeremony, iDivination, iSeafaring,
iAlloys, iConstruction, iRiding, iArithmetics, iWriting, iCalendar, iShipbuilding,
iBloomery, iCement, iMathematics, iContract, iLiterature, iPriesthood, iNavigation,
iGeneralship, iEngineering, iAesthetics, iCurrency, iLaw, iPhilosophy, iMedicine,
iNobility, iSteel, iArchitecture, iArtisanry, iPolitics, iScholarship, iEthics,
iFeudalism, iFortification, iMachinery, iAlchemy, iGuilds, iCivilService, iTheology,
iCommune, iCropRotation, iPaper, iCompass, iPatronage, iEducation, iDoctrine,
iGunpowder, iCompanies, iFinance, iCartography, iHumanities, iPrinting, iJudiciary,
iFirearms, iLogistics, iExploration, iOptics, iAcademia, iStatecraft, iHeritage,
iCombinedArms, iEconomics, iGeography, iScientificMethod, iUrbanPlanning, iCivilLiberties, iHorticulture,
iReplaceableParts, iHydraulics, iPhysics, iGeology, iMeasurement, iSociology, iSocialContract,
iMachineTools, iThermodynamics, iMetallurgy, iChemistry, iBiology, iRepresentation, iNationalism,
iBallistics, iEngine, iRailroad, iElectricity, iRefrigeration, iLabourUnions, iJournalism,
iPneumatics, iAssemblyLine, iRefining, iFilm, iMicrobiology, iConsumerism, iCivilRights,
iInfrastructure, iFlight, iSynthetics, iRadio, iPsychology, iMacroeconomics, iSocialServices,
iAviation, iRocketry, iFission, iElectronics, iTelevision, iPowerProjection, iGlobalism,
iRadar, iSpaceflight, iNuclearPower, iLaser, iComputers, iTourism, iEcology,
iAerodynamics, iSatellites, iSuperconductors, iRobotics, iTelecommunications, iRenewableEnergy, iGenetics,
iSupermaterials, iFusion, iNanotechnology, iAutomation, iBiotechnology,
iUnifiedTheory, iArtificialIntelligence,
iTranshumanism) = range(iNumTechs)

# initialise unit variables to unit indices from XML

iNumUnits = 133
#				2				3				4				5				6				7				8				9				10
(iLion, 		iBear, 			iPanther, 		iWolf, 			iSettler, 		iPioneer, 		iWorker, 		iLabourer, 		iMadeireiro, 	iScout, 
iExplorer, 		iBandeirante, 	iSpy, 			iReligiousPersecutor, iJewishMissionary, iOrthodoxMissionary, iCatholicMissionary, iProtestantMissionary, iIslamicMissionary, iHinduMissionary, 
iBuddhistMissionary, iConfucianMissionary, iTaoistMissionary, iZoroastrianMissionary, iWarrior, iNativeWarrior, iMilitia, iAxeman, iLightSwordsman, iDogSoldier, 
iSwordsman, 	iJaguar, 		iAucac, 		iHeavySwordsman,iSpearman, 		iNativeRaider, 	iHeavySpearman, iPikeman, 		iArquebusier, 	iTercio, 
iMohawk, 		iMusketeer, 	iRedcoat, 		iMinuteman, 	iRifleman, 		iGrenadier, 	iAlbionLegion, 	iAntiTank, 		iInfantry, 		iSamInfantry, 
iMobileSam, 	iMarine, 		iNavySeal, 		iParatrooper, 	iMechanizedInfantry, iArcher,  	iNativeArcher, 	iSkirmisher, 	iHolkan, 		iLongbowman, 
iCrossbowman, 	iHorseArcher,  	iPistolier, 	iMountedBrave, 	iCuirassier, 	iConquistador, 	iHussar, 		iLlanero, 		iDragoon, 		iGrenadierCavalry, 
iCavalry, 	iRural, 		iTank, 			iMainBattleTank, 	iGunship, 		iBombard, 		iCannon, 		iArtillery, 	iMachineGun, 	iHowitzer, 		
iMobileArtillery, iWorkboat, 	iCaravel, 		iCarrack, 		iWaaKaulua,		iGalleon, 		iEastIndiaman, 	iPrivateer, 	iFrigate, 		iShipOfTheLine, 
iManOfWar, 		iSteamship, 	iIronclad, 		iTorpedoBoat, 	iCruiser, 		iTransport, 	iDestroyer, 	iCorvette, 		iBattleship, 	iMissileCruiser, 
iStealthDestroyer,iSubmarine, 	iNuclearSubmarine, iCarrier, 	iBiplane, 		iFighter, 		iJetFighter, 	iBomber, 		iStealthBomber, iGuidedMissile, 
iDrone, 		iNuclearBomber, iICBM, 			iSatellite, 	iGreatProphet, 	iGreatArtist, 	iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, 
iGreatGeneral, 	iArgentineGreatGeneral, iGreatSpy, iFemaleGreatProphet, iFemaleGreatArtist, iFemaleGreatScientist, iFemaleGreatMerchant, iFemaleGreatEngineer, iFemaleGreatStatesman, iFemaleGreatGeneral, 
iFemaleGreatSpy, iSlave, 		iAztecSlave) = range(iNumUnits)

lGreatPeopleUnits = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman]

dFemaleGreatPeople = {
iGreatProphet : iFemaleGreatProphet,
iGreatArtist : iFemaleGreatArtist,
iGreatScientist : iFemaleGreatScientist,
iGreatMerchant : iFemaleGreatMerchant,
iGreatEngineer : iFemaleGreatEngineer,
iGreatStatesman : iFemaleGreatStatesman,
iGreatGeneral : iFemaleGreatGeneral,
iGreatSpy : iFemaleGreatSpy,
}

iNumUnitRoles = 22
(iBase, iDefend, iAttack, iCounter, iShock, iHarass, iCityAttack, iWorkerSea, iSettle, iSettleSea, 
iAttackSea, iFerry, iEscort, iExplore, iShockCity, iSiege, iCitySiege, iExploreSea, iSkirmish, iLightEscort,
iWork, iMissionary) = range(iNumUnitRoles)

# initialise bonuses variables to bonuses IDs from WBS
iNumBonuses = 41
(iAluminium, iCamel, iCoal, iCopper, iHorse, iIron, iMarble, iOil, iStone, iUranium, iBanana, iClam, iCorn, iCow, iCrab,
iDeer, iFish, iPig, iRice, iSheep, iWheat, iCoffee, iCotton, iDye, iFur, iGems, iGold, iIncense, iIvory, iPearls, iSilk, iSilver, iSpices,
iSugar, iTea, iTobacco, iWine, iWhales, iSoccer, iSongs, iMovies) = range(iNumBonuses)
# Buildings

iNumBuildings = 169
# Buildings (86)
#				2				3				4				5				6				7				8				9				10
(iPalace, 		iBarracks, 		iGranary,		iTerrace, 		iSmokehouse, 	iPaganTemple, 	iMonument,		iTotemPole, 	iWalls, 		iStable, 
iLibrary,		iHarbor, 		iAqueduct, 		iTheatre,		iArena, 		iBallCourt, 	iCharreadaArena, iGarden, 		iLighthouse, 	iWeaver,
iMarket, 		iJail, 			iSacrificialAltar, iBath, 		iForge, 		iMint, 			iCastle, 		iPharmacy, 		iPostOffice, 	iTambo,
iWharf, 		iCoffeehouse,	iSalon, 		iBank, 			iRoyalExchange, iConstabulary, 	iMountedPolice, iCustomsHouse, 	iFeitoria, 		iUniversity,	
iCivicSquare, 	iSewer, 		iStarFort, 		iEstate, 		iFazenda, 		iHacienda, 		iDrydock, 		iLevee, 		iObservatory, 	iWarehouse, 	
iCourthouse, 	iFactory, 		iAssemblyPlant, iDistillery, 	iPark, 			iCoalPlant, 	iRailwayStation, iLaboratory, 	iNewsPress, 	iIndustrialPark, 
iCinema, 		iHospital, 		iSupermarket, 	iColdStoragePlant, iPublicTransportation, iDepartmentStore, iMall, iBroadcastTower, iIntelligenceAgency, iElectricalGrid, 
iAirport, 		iBunker, 		iBombShelters, 	iHydroPlant, 	iSecurityBureau, iStadium, 		iContainerTerminal, iNuclearPlant, iSupercomputer, iHotel, 		
iRecyclingCenter, iLogisticsCenter, iSolarPlant, iFiberNetwork, iAutomatedFactory, iVerticalFarm, 
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
iNumRegions = 35
(rAlaska, rNunavut, rNorthPlains, rOntario, rQuebec, rNewFoundland, rNewEngland, rMidAtlantic, rDeepSouth, rGulfCoast, 
rMidwest, rSouthwest, rGreatPlains, rRockies, rCalifornia, rCascadia, rSierraMadre, rBajio, rYucatan, rMesoamerica,
rCaribbean, rHawaii, rColombia, rVenezuela, rGuyana, rPeru, rBolivia, rAmazon, rBrazilianHighlands, rPantanal, 
rChile, rParaguay, rUruguay, rPampas, rPatagonia) = range(iNumRegions)

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

iNumFeatures = 10
(iSeaIce, iJungle, iOasis, iFloodPlains, iForest, iMud, iCape, iIslands, iRainforest, iFallout) = range(iNumFeatures)

iGrass = 0
iPlains = 1
iDesert = 2
iTundra = 3
iSnow = 4
iCoast = 5
iOcean = 6
iTerrainPeak = 7
iTerrainHills = 8
iMarsh = 9

#Plague
iImmunity = 20

# Victory
iVictoryPaganism = 10
iVictorySecularism = 11


#leaders
iNumLeaders = 125
(iLeaderBarbarian, iNativeLeader, iIndependentLeader, iRamesses, iCleopatra, iBaibars, iNasser, iSargon, iHammurabi, iVatavelli,
iQinShiHuang, iTaizong, iHongwu, iMao, iPericles, iAlexanderTheGreat, iGeorge, iAsoka, iChandragupta, iShivaji, 
iGandhi, iHiram, iHannibal, iAhoeitu, iCyrus, iDarius, iKhosrow, iJuliusCaesar, iAugustus, iPacal,
iRajendra, iKrishnaDevaRaya, iEzana, iZaraYaqob, iMenelik, iWangKon, iSejong, iJustinian, iBasil, iKammu,
iOdaNobunaga, iMeiji, iRagnar, iGustav, iGerhardsen, iBumin, iAlpArslan, iTamerlane, iHarun, iSaladin,
iSongtsen, iLobsangGyatso, iDharmasetu, iHayamWuruk, iSuharto, iRahman, iYaqub, iIsabella, iPhilip, iFranco,
iCharlemagne, iLouis, iNapoleon, iDeGaulle, iSuryavarman, iAlfred, iElizabeth, iVictoria, iChurchill, iBarbarossa,
iCharles, iFrancis, iIvan, iPeter, iCatherine, iAlexanderI, iStalin, iMansaMusa, iCasimir, iSobieski,
iPilsudski, iWalesa, iAfonso, iJoao, iMaria, iHuaynaCapac, iCastilla, iLorenzo, iCavour, iMussolini,
iGenghisKhan, iKublaiKhan, iMontezuma, iTughluq, iAkbar, iBhutto, iMehmed, iSuleiman, iAtaturk, iNaresuan,
iMongkut, iMbemba, iAbbas, iKhomeini, iWillemVanOranje, iWilliam, iFrederick, iBismarck, iHitler, iWashington,
iLincoln, iRoosevelt, iSanMartin, iPeron, iJuarez, iSantaAnna, iCardenas, iBolivar, iPedro, iVargas,
iMacDonald, iTrudeau, iBoudica, iBrennus, iSittingBull) = range(iNumLeaders)

dResurrectionLeaders = CivDict({
})

iNumPeriods = 0
#() = range(iNumPeriods)

iNumImpacts = 5
(iImpactMarginal, iImpactLimited, iImpactSignificant, iImpactCritical, iImpactPlayer) = range(iNumImpacts)

dTradingCompanyPlots = CivDict({
iSpain : [(109, 33)],
iFrance : [(101, 37), (101, 36), (102, 36), (102, 35), (103, 35), (103, 34), (104, 34), (104, 33)],
iEngland : [(95, 37), (94, 37), (94, 36), (94, 35), (94, 34), (93, 34), (93, 33), (92, 33), (92, 32), (88, 33), (88, 34), (88, 35)],
iPortugal : [(82, 34), (89, 31), (101, 29), (105, 39), (93, 28), (93, 27), (71, 17), (69, 13), (54, 26), (62, 20)],
iNetherlands : [(99, 28), (99, 27), (100, 27), (100, 26), (101, 26), (104, 25), (105, 25), (106, 25), (107, 24), (104, 27), (105, 27), (106, 27), (104, 28), (106, 28), (105, 29), (106, 29)],
})

lSecondaryCivs = [iArgentina, iBrazil]

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