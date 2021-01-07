# Rhye's and Fall of Civilization - Constants
# globals

from CvPythonExtensions import *
gc = CyGlobalContext()

iWorldX = 149
iWorldY = 79

# initialise player variables to player IDs from WBS
iNumPlayers = 18
(iSpain, iFrance, iEngland, iVirginia, iMassachusetts, iNewHampshire, iMaryland, iConnecticut, iRhodeIsland, 
iDelaware, iNorthCarolina, iSouthCarolina, iNewJersey, iNewYork, iPennsylvania, iGeorgia, iAmerica, iCanada) = range(iNumPlayers)

(pSpain, pFrance, pEngland, pVirginia, pMassachusetts, pNewHampshire, pMaryland, pConnecticut, pRhodeIsland, 
pDelaware, pNorthCarolina, pSouthCarolina, pNewJersey, pNewYork, pPennsylvania, pGeorgia, pAmerica, pCanada) = [gc.getPlayer(i) for i in range(iNumPlayers)]

(teamSpain, teamFrance, teamEngland, teamVirginia, teamMassachusetts, teamNewHampshire, teamMaryland, teamConnecticut, teamRhodeIsland, 
teamDelaware, teamNorthCarolina, teamSouthCarolina, teamNewJersey, teamNewYork, teamPennsylvania, teamGeorgia, teamAmerica, teamCanada) = [gc.getTeam(i) for i in range(iNumPlayers)]

iNumMajorPlayers = iNumPlayers
iNumActivePlayers = iNumPlayers

iIndependent = iNumPlayers
iIndependent2 = iNumPlayers+1
iNative = iNumPlayers+2
iNumTotalPlayers = iNumPlayers+3
iBarbarian = iNumPlayers+3
iNumTotalPlayersB = iBarbarian+1

(pIndependent, pIndependent2, pNative, pBarbarian) = [gc.getPlayer(i) for i in range(iIndependent, iNumTotalPlayersB)]
(teamIndependent, teamIndependent2, teamNative, teamBarbarian) = [gc.getTeam(i) for i in range(iIndependent, iNumTotalPlayersB)]

l0Array =       [0 for i in range(iNumPlayers)]
l0ArrayActive = [0 for i in range(iNumPlayers)]
l0ArrayTotal =  [0 for i in range(iNumTotalPlayers)]

lm1Array =      [-1 for i in range(iNumPlayers)]

# civilizations, not players
iNumCivilizations = 22
(iCivAmerica, iCivCanada, iCivConnecticut, iCivDelaware, iCivEngland, iCivFrance, iCivGeorgia, iCivMaryland, iCivMassachusetts,
iCivNewHampshire, iCivNewJersey, iCivNewYork, iCivNorthCarolina, iCivPennsylvania, iCivRhodeIsland, iCivSouthCarolina, iCivSpain,
iCivVirginia, iCivIndependent, iCivIndependent2, iCivNative, iCivBarbarian) = range(iNumCivilizations)

#for Congresses and Victory
lCivGroups = [[iSpain, iFrance, iEngland],  #Euros
		[iAmerica, iCanada, iCivConnecticut, iCivDelaware, iCivGeorgia, iCivMaryland, iCivMassachusetts, iCivNewHampshire, 
		iCivNewJersey, iCivNewYork, iCivNorthCarolina, iCivPennsylvania, iCivRhodeIsland, iCivSouthCarolina, iCivVirginia]] #American

lCivStabilityGroups = [[iSpain, iFrance, iEngland],  #Euros
		[iAmerica, iCanada, iCivConnecticut, iCivDelaware, iCivGeorgia, iCivMaryland, iCivMassachusetts, iCivNewHampshire, 
		iCivNewJersey, iCivNewYork, iCivNorthCarolina, iCivPennsylvania, iCivRhodeIsland, iCivSouthCarolina, iCivVirginia]] #American
		
lTechGroups = [[iSpain, iFrance, iEngland],  #Euros
		[iAmerica, iCanada, iCivConnecticut, iCivDelaware, iCivGeorgia, iCivMaryland, iCivMassachusetts, iCivNewHampshire, 
		iCivNewJersey, iCivNewYork, iCivNorthCarolina, iCivPennsylvania, iCivRhodeIsland, iCivSouthCarolina, iCivVirginia]] #American


lCivBioOldWorld = [iSpain, iFrance, iEngland, iAmerica, iCanada, iIndependent, iIndependent2]
lCivBioNewWorld = [iNative, iBarbarian]


#for Victory and the handler
tAmericasTL = (3, 0)
tAmericasBR = (43, 63)

# Colombian UP
tSouthCentralAmericaTL = (13, 3)
tSouthCentralAmericaBR = (43, 39)

# English colonists
tCanadaTL = (10, 49)
tCanadaBR = (37, 58)
tAustraliaTL = (103, 5)
tAustraliaBR = (123, 22)

# new capital locations
tVienna = (62, 49)
tWarsaw = (65, 52)
tStockholm = (63, 59)
tIstanbul = (68, 45)
tBeijing = (102, 47)
tEsfahan = (81, 41)
tHamburg = (59, 53)
tMilan = (59, 47)
tBaghdad = (77, 40)
tMumbai = (88, 34)
tMysore = (90, 31)

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
iNumMinorCities = 40

# scripted conquerors
iNumConquests = 13

#neighbours
lNeighbours = [
[iFrance, iEngland], #Spain
[iSpain, iEngland], #France
[iSpain, iFrance], #England
[iAmerica, iMaryland, iPennsylvania, iNorthCarolina], # Virginia
[iAmerica, iNewHampshire, iNewYork, iConnecticut, iRhodeIsland], # Massachusetts
[iAmerica, iNewYork, iMassachusetts], # New Hampshire
[iAmerica, iPennsylvania, iVirginia, iDelaware], # Maryland
[iAmerica, iNewYork, iMassachusetts, iRhodeIsland], # Connecticut
[iAmerica, iMassachusetts, iConnecticut], # Rhode Island
[iAmerica, iMaryland, iNewJersey, iPennsylvania], # Delaware
[iAmerica, iSouthCarolina, iVirginia], # North Carolina
[iAmerica, iNorthCarolina, iGeorgia], # South Carolina
[iAmerica, iNewYork, iPennsylvania, iDelaware], # New Jersey
[iAmerica, iNewHampshire, iConnecticut, iMassachusetts, iPennsylvania, iNewJersey], # New York
[iAmerica, iNewYork, iVirginia, iNewJersey, iDelaware, iMaryland], # Pennsylvania
[iAmerica, iSpain, iSouthCarolina], # Georgia
[], #America
[], #Canada
]

#for stability hit on spawn
lOlderNeighbours = [
[], #Spain
[], #France
[], #England
[iSpain, iFrance, iEngland], #America
[iFrance, iEngland, iAmerica], #Canada
]

# civ birth dates

# converted to years - edead
# MacAurther TODO: Get the scenario years right
tBirth = (
1600,		# Spain
1600,		# France
1600,		# England
1607,		# Virginia
1620,		# Massachusetts
1623,		# New Hampshire
1634,		# Maryland
1635,		# Connecticut
1636,		# Rhode Island
1638,		# Delaware
1653,		# North Carolina
1663,		# South Carolina
1664,		# New Jersey
1664,		# New York
1682,		# Pennsylvania
1732,		# Georgia
1787,		# America
1867,		# Canada
1600, # 0,
1600, # 0,
1600, # 0,
1600, # 0,
1600
)

# Leoreth: stability penalty from this date on
tFall = (
2020,					# Spain
2020,					# France
2020,					# England
2020,					# Virginia
2020,					# Massachusetts
2020,					# New Hampshire
2020,					# Maryland
2020,					# Connecticut
2020,					# Rhode Island
2020,					# Delaware
2020,					# North Carolina
2020,					# South Carolina
2020,					# New Jersey
2020,					# New York
2020,					# Pennsylvania
2020,					# Georgia
2020,					# America
2020)					# Canada

dVictoryYears = {
iCivSpain : (-1, -1, -1),
iCivFrance : (-1, -1, -1),
iCivEngland : (-1, -1, -1),
iCivVirginia : (1900, 1950, 2000),
iCivMassachusetts : (1900, 1950, 2000),
iCivNewHampshire : (1900, 1950, 2000),
iCivMaryland : (1900, 1950, 2000),
iCivConnecticut : (1900, 1950, 2000),
iCivRhodeIsland : (1900, 1950, 2000),
iCivDelaware : (1900, 1950, 2000),
iCivNorthCarolina : (1900, 1950, 2000),
iCivSouthCarolina : (1900, 1950, 2000),
iCivNewJersey : (1900, 1950, 2000),
iCivNewYork : (1900, 1950, 2000),
iCivPennsylvania : (1900, 1950, 2000),
iCivGeorgia : (1900, 1950, 2000),
iCivAmerica : (1900, 1950, 2000),
iCivCanada : (1920, 1950, 2000),
}

# Leoreth: date-triggered respawn for certain civs
dRebirth = {
}

dRebirthCiv = {
}

tResurrectionIntervals = (
[(1700, 2020)], #Spain
[(1700, 2020)], #France
[(1700, 2020)], #England
[(1700, 2020)], #Virginia
[(1700, 2020)], #Massachusetts
[(1700, 2020)], #New Hampshire
[(1700, 2020)], #Maryland
[(1700, 2020)], #Connecticut
[(1700, 2020)], #Rhode Island
[(1700, 2020)], #Delaware
[(1700, 2020)], #North Carolina
[(1700, 2020)], #South Carolina
[(1700, 2020)], #New Jersey
[(1700, 2020)], #New York
[(1700, 2020)], #Pennsylvania
[(1700, 2020)], #Georgia
[(1770, 2020)], #America
[(1867, 2020)], #Canada
)

#rnf. Some civs have a double entry, for a higher chance
lEnemyCivsOnSpawn = [
[], #Spain
[], #France
[], #England
[], #Virginia
[], #Massachusetts
[], #New Hampshire
[], #Maryland
[], #Connecticut
[], #Rhode Island
[], #Delaware
[], #North Carolina
[], #South Carolina
[], #New Jersey
[], #New York
[], #Pennsylvania
[], #Georgia
[], #America
[], #Canada
]

# Leoreth
lTotalWarOnSpawn = [
[], #Spain
[], #France
[], #England
[], #Virginia
[], #Massachusetts
[], #New Hampshire
[], #Maryland
[], #Connecticut
[], #Rhode Island
[], #Delaware
[], #North Carolina
[], #South Carolina
[], #New Jersey
[], #New York
[], #Pennsylvania
[], #Georgia
[], #America
[], #Canada
]


#AIWars
tAggressionLevel = (
2, #Spain
1, #France
1, #England
1, #Virginia
1, #Massachusetts
1, #New Hampshire
1, #Maryland
1, #Connecticut
1, #Rhode Island
1, #Delaware
1, #North Carolina
1, #South Carolina
1, #New Jersey
1, #New York
1, #Pennsylvania
1, #Georgia
2, #America
0, #Canada
0,
0,
0,
0) #Barbs


#war during rise of new civs
tAIStopBirthThreshold = (
    80, #Spain  #60 in vanilla and Warlords
    80, #France #60 in vanilla and Warlords
    50, #England
	50, #Virginia
	50, #Massachusetts
	50, #New Hampshire
	50, #Maryland
	50, #Connecticut
	50, #Rhode Island
	50, #Delaware
	50, #North Carolina
	50, #South Carolina
	50, #New Jersey
	50, #New York
	50, #Pennsylvania
	50, #Georgia
    50, #America
    60, #Canada
    100,
    100,
    100,
    100)


#RiseAndFall
tResurrectionProb = (
100, #Spain
100, #France
100, #England
100, #Virginia
100, #Massachusetts
100, #New Hampshire
100, #Maryland
100, #Connecticut
100, #Rhode Island
100, #Delaware
100, #North Carolina
100, #South Carolina
100, #New Jersey
100, #New York
100, #Pennsylvania
100, #Georgia
100, #America
100, #Canada
100) #Barbs 


#Congresses.
tPatienceThreshold = (
20, #Spain
20, #France
20, #England
100, #Virginia
100, #Massachusetts
100, #New Hampshire
100, #Maryland
100, #Connecticut
100, #Rhode Island
100, #Delaware
100, #North Carolina
100, #South Carolina
100, #New Jersey
100, #New York
100, #Pennsylvania
100, #Georgia
30, #America
40, #Canada
100) #Barbs

dMaxColonists = {
iSpain : 7,
iFrance : 5,
iEngland : 6,
}

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

lCatholicStart = [iSpain, iFrance, iEngland, iCanada]
lProtestantStart = [iAmerica]

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

iNumUnits = 209
(iLion, iBear, iPanther, iWolf, iSettler, iCityBuilder, iPioneer, iWorker, iPunjabiWorker, iLabourer, 
iMadeireiro, iScout, iExplorer, iBandeirante, iSpy, iReligiousPersecutor, iJewishMissionary, iOrthodoxMissionary, iCatholicMissionary, iProtestantMissionary, 
iIslamicMissionary, iHinduMissionary, iBuddhistMissionary, iConfucianMissionary, iTaoistMissionary, iZoroastrianMissionary, iWarrior, iMilitia, iAxeman, iLightSwordsman, 
iVulture, iDogSoldier, iSwordsman, iJaguar, iLegion, iGallicWarrior, iAucac, iShotelai, iHeavySwordsman, iSamurai, 
iHuscarl, iGhazi, iPombos, iSpearman, iHoplite, iSacredBand, iImmortal, iImpi, iHeavySpearman, iPikeman, 
iLandsknecht, iArquebusier, iFirelancer, iTercio, iStrelets, iJanissary, iOromoWarrior, iQizilbash, iMohawk, iMusketeer, 
iRedcoat, iFusilier, iMinuteman, iRifleman, iMehalSefari, iGrenadier, iRocketeer, iGrenzer, iAlbionLegion, iAntiTank, 
iInfantry, iSamInfantry, iMobileSam, iMarine, iNavySeal, iParatrooper, iMechanizedInfantry, iArcher, iAsharittuBowman, iMedjay, 
iSkirmisher, iHolkan, iKelebolo, iLongbowman, iPatiyodha, iCrossbowman, iChokonu, iBalestriere, iChariot, iWarChariot, 
iHuluganni, iCidainh, iHorseman, iCompanion, iNumidianCavalry, iAsvaka, iCamelRider, iHorseArcher, iMangudai, iKhampa, 
iOghuz, iCamelArcher, iLancer, iVaru, iSavaran, iMobileGuard, iKeshik, iCataphract, iChangSuek, iFarari, 
iPistolier, iMountedBrave, iCamelGunner, iCuirassier, iGendarme, iConquistador, iWingedHussar, iHussar, iCossack, iLlanero, 
iDragoon, iGuard, iGrenadierCavalry, iCavalry, iRural, iWarElephant, iBallistaElephant, iTank, iPanzer, iMainBattleTank, 
iGunship, iCatapult, iBallista, iTrebuchet, iBombard, iHwacha, iSiegeElephant, iGreatBombard,iCannon, iArtillery, 
iMachineGun, iHowitzer, iMobileArtillery, iWorkboat, iGalley, iWaka, iBireme, iWarGalley, iHeavyGalley, iDromon, 
iLongship, iCog, iDharani, iGalleass, iDjong, iKobukson, iLanternas, iCaravel, iCarrack, iGalleon, 
iEastIndiaman, iPrivateer, iCorsair, iFrigate, iShipOfTheLine, iManOfWar, iSteamship, iIronclad, iTorpedoBoat, iCruiser, 
iTransport, iDestroyer, iCorvette, iBattleship, iMissileCruiser, iStealthDestroyer, iSubmarine, iNuclearSubmarine, iCarrier, iBiplane, 
iFighter, iZero, iJetFighter, iBomber, iStealthBomber, iGuidedMissile, iDrone, iNuclearBomber, iICBM, iSatellite, 
iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral, iArgentineGreatGeneral, iGreatSpy, iFemaleGreatProphet, 
iFemaleGreatArtist, iFemaleGreatScientist, iFemaleGreatMerchant, iFemaleGreatEngineer, iFemaleGreatStatesman, iFemaleGreatGeneral, iFemaleGreatSpy, iSlave, iAztecSlave) = range(iNumUnits)

iMissionary = iJewishMissionary # generic

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

# initialise bonuses variables to bonuses IDs from WBS
iNumBonuses = 41
(iAluminium, iCamel, iCoal, iCopper, iHorse, iIron, iMarble, iOil, iStone, iUranium, iBanana, iClam, iCorn, iCow, iCrab,
iDeer, iFish, iPig, iRice, iSheep, iWheat, iCoffee, iCotton, iDye, iFur, iGems, iGold, iIncense, iIvory, iPearls, iSilk, iSilver, iSpices,
iSugar, iTea, iTobacco, iWine, iWhales, iSoccer, iSongs, iMovies) = range(iNumBonuses)
# Buildings

iNumBuildings = 318
(iPalace, iBarracks, iIkhanda, iGranary, iTerrace, iSmokehouse, iPaganTemple, iMonument, iObelisk, iStele,
iCandi, iEdict, iMalae, iTotemPole, iWalls, iDun, iStable, iGer, iLibrary, iEdubba,
iTaixue, iHoTrai, iSangam, iHarbor, iAqueduct, iBaray, iNoria, iStepwell, iTheatre, iOdeon,
iHippodrome, iPavilion, iArena, iBallCourt, iCharreadaArena, iGarden, iLighthouse, iTradingPost, iWeaver, iMbwadi,
iMarket, iForum, iGlassmaker, iJail, iSacrificialAltar, iDivan, iBath, iReservoir, iHammam, iForge, 
iMint, iArtStudio, iCastle, iCitadel, iPharmacy, iApothecary, iAlchemist, iPostOffice, iTambo, iCaravanserai,
iWharf, iCoffeehouse, iSalon, iBank, iRoyalExchange, iConstabulary, iMountedPolice, iCustomsHouse, iFeitoria, iUniversity,
iSeowon, iGompa, iCivicSquare, iRathaus, iSejmik, iSewer, iStarFort, iEstate, iMausoleum, iFazenda, 
iHacienda, iDrydock, iLevee, iDike, iObservatory, iWarehouse, iCourthouse, iFactory, iAssemblyPlant, iZaibatsu, 
iDistillery, iPark, iCoalPlant, iRailwayStation, iLaboratory, iResearchInstitute, iNewsPress, iIndustrialPark, iCinema, iHospital, 
iSupermarket, iColdStoragePlant, iPublicTransportation, iDepartmentStore, iMall, iBroadcastTower, iIntelligenceAgency, iElectricalGrid, iAirport, iBunker, 
iBombShelters, iHydroPlant, iSecurityBureau, iStadium, iContainerTerminal, iNuclearPlant, iSupercomputer, iHotel, iRecyclingCenter, iLogisticsCenter, 
iSolarPlant, iFiberNetwork, iAutomatedFactory, iVerticalFarm, iJewishTemple, iJewishCathedral, iJewishMonastery, iJewishShrine, iOrthodoxTemple, iOrthodoxCathedral, 
iOrthodoxMonastery, iOrthodoxShrine, iCatholicChurch, iCatholicCathedral, iCatholicMonastery, iCatholicShrine, iProtestantTemple, iProtestantCathedral, iProtestantMonastery, iProtestantShrine, 
iIslamicTemple, iIslamicCathedral, iIslamicMonastery, iIslamicShrine, iHinduTemple, iHinduCathedral, iHinduMonastery, iHinduShrine, iBuddhistTemple, iBuddhistCathedral, 
iBuddhistMonastery, iBuddhistShrine, iConfucianTemple, iConfucianCathedral, iConfucianMonastery, iConfucianShrine, iTaoistTemple, iTaoistCathedral, iTaoistMonastery, iTaoistShrine, 
iZoroastrianTemple, iZoroastrianCathedral, iZoroastrianMonastery, iZoroastrianShrine, iAcademy, iAdministrativeCenter, iManufactory, iArmoury, iMuseum, iStockExchange, 
iTradingCompanyBuilding, iIberianTradingCompanyBuilding, iNationalMonument, iNationalTheatre, iNationalGallery, iNationalCollege, iMilitaryAcademy, iSecretService, iIronworks, iRedCross, 
iNationalPark, iCentralBank, iSpaceport, iGreatSphinx, iPyramids, iOracle, iGreatWall, iIshtarGate, iTerracottaArmy, iHangingGardens, 
iGreatCothon, iDujiangyan, iApadanaPalace, iColossus, iStatueOfZeus, iGreatMausoleum, iParthenon, iTempleOfArtemis, iGreatLighthouse, iMoaiStatues, 
iFlavianAmphitheatre, iAquaAppia, iAlKhazneh, iTempleOfKukulkan, iMachuPicchu, iGreatLibrary, iFloatingGardens, iGondeshapur, iJetavanaramaya, iNalanda, 
iTheodosianWalls, iHagiaSophia, iBorobudur, iMezquita, iShwedagonPaya, iMountAthos, iIronPillar, iPrambanan, iSalsalBuddha, iCheomseongdae, 
iHimejiCastle, iGrandCanal, iWatPreahPisnulok, iKhajuraho, iSpiralMinaret, iDomeOfTheRock, iHouseOfWisdom, iKrakDesChevaliers, iMonolithicChurch, iUniversityOfSankore, 
iNotreDame, iOldSynagogue, iSaintSophia, iSilverTreeFountain, iSantaMariaDelFiore, iAlamut, iSanMarcoBasilica, iSistineChapel, iPorcelainTower, iTopkapiPalace, 
iKremlin, iSaintThomasChurch, iVijayaStambha, iGurEAmir, iRedFort, iTajMahal, iForbiddenPalace, iVersailles, iBlueMosque, iEscorial, 
iTorreDeBelem, iPotalaPalace, iOxfordUniversity, iHarmandirSahib, iSaintBasilsCathedral, iBourse, iItsukushimaShrine, iImageOfTheWorldSquare, iLouvre, iEmeraldBuddha, 
iShalimarGardens, iTrafalgarSquare, iHermitage, iGuadalupeBasilica, iSaltCathedral, iAmberRoom, iStatueOfLiberty, iBrandenburgGate, iAbbeyMills, iBellRockLighthouse, 
iChapultepecCastle, iEiffelTower, iWestminsterPalace, iTriumphalArch, iMenloPark, iCrystalPalace, iTsukijiFishMarket, iBrooklynBridge, iHollywood, iEmpireStateBuilding, 
iLasLajasSanctuary, iPalaceOfNations, iMoleAntonelliana, iNeuschwanstein, iFrontenac, iWembley, iLubyanka, iCristoRedentor, iMetropolitain, iNobelPrize, 
iGoldenGateBridge, iBletchleyPark, iSagradaFamilia, iCERN, iItaipuDam, iGraceland, iCNTower, iPentagon, iUnitedNations, iCrystalCathedral, 
iMotherlandCalls, iBerlaymont, iWorldTradeCenter, iAtomium, iIronDome, iHarbourOpera, iLotusTemple, iGlobalSeedVault, iGardensByTheBay, iBurjKhalifa, 
iHubbleSpaceTelescope, iChannelTunnel, iSkytree, iOrientalPearlTower, iDeltaWorks, iSpaceElevator, iLargeHadronCollider, iITER) = range(iNumBuildings)

iBeginWonders = iGreatSphinx # different from DLL constant because that includes national wonders

iTemple = iJewishTemple #generic
iCathedral = iJewishCathedral #generic
iMonastery = iJewishMonastery #generic
iShrine = iJewishShrine #generic

iFirstWonder = iGreatSphinx

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
iSpecialistGreatProphet, iSpecialistGreatArtist, iSpecialistGreatScientist, iSpecialistGreatMerchant, iSpecialistGreatEngineer, iSpecialistGreatStatesman, iSpecialistGreatGeneral, iSpecialistGreatSpy, iSpecialistResearchSatellite, iSpecialistCommercialSatellite, iSpecialistMilitarySatellite, iSpecialistSlave) = range(iNumSpecialists)

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
(iParameterCorePeriphery, iParameterCoreScore, iParameterPeripheryScore, iParameterRecentExpansion, iParameterRazedCities, iParameterIsolationism,	# Expansion
iParameterEconomicGrowth, iParameterTrade, iParameterMercantilism, iParameterCentralPlanning,								# Economy
iParameterHappiness, iParameterCivicCombinations, iParameterCivicsEraTech, iParameterReligion,								# Domestic
iParameterVassals, iParameterDefensivePacts, iParameterRelations, iParameterNationhood, iParameterTheocracy, iParameterMultilateralism,			# Foreign
iParameterWarSuccess, iParameterWarWeariness, iParameterBarbarianLosses) = range(iNumStabilityParameters)						# Military

#Regions
iNumRegions = 38
(rBritain, rIberia, rItaly, rBalkans, rEurope, rScandinavia, rRussia, rAnatolia, rMesopotamia, rArabia, rEgypt, rMaghreb,
rPersia, rIndia, rDeccan, rIndochina, rIndonesia, rChina, rKorea, rJapan, rManchuria, rTibet, rCentralAsia, rSiberia,
rAustralia, rOceania, rEthiopia, rWestAfrica, rSouthAfrica, rCanada, rAlaska, rUnitedStates, rCaribbean, rMesoamerica,
rBrazil, rArgentina, rPeru, rColombia) = range(iNumRegions)

lNewWorld = [rAustralia, rOceania, rCanada, rAlaska, rUnitedStates, rCaribbean, rMesoamerica, rBrazil, rArgentina, rPeru, rColombia]

lEurope = [rBritain, rIberia, rItaly, rBalkans, rEurope, rScandinavia, rRussia]
lMiddleEast = [rAnatolia, rMesopotamia, rArabia, rPersia, rCentralAsia]
lIndia = [rIndia, rDeccan]
lEastAsia = [rIndochina, rIndonesia, rChina, rKorea, rJapan, rManchuria, rTibet]
lNorthAfrica = [rEgypt, rMaghreb]
lSubSaharanAfrica = [rEthiopia, rSouthAfrica, rWestAfrica]
lSouthAmerica = [rCaribbean, rMesoamerica, rBrazil, rArgentina, rPeru, rColombia]
lNorthAmerica = [rCanada, rAlaska, rUnitedStates]
lOceania = [rAustralia, rOceania]

lAfrica = lNorthAfrica + lSubSaharanAfrica
lAsia = lMiddleEast + lIndia + lEastAsia

iArea_Europe = 1000
iArea_MiddleEast = 1001
iArea_India = 1002
iArea_EastAsia = 1003
iArea_Africa = 1004
iArea_SouthAmerica = 1005
iArea_NorthAmerica = 1006

mercRegions = {
	iArea_Europe : set([rBritain, rIberia, rItaly, rBalkans, rEurope, rScandinavia, rRussia]),
	iArea_MiddleEast : set([rAnatolia, rMesopotamia, rArabia, rEgypt, rMaghreb, rPersia, rCentralAsia]),
	iArea_India : set([rIndia, rDeccan]),
	iArea_EastAsia : set([rIndochina, rIndonesia, rChina, rKorea, rJapan, rManchuria, rTibet]),
	iArea_Africa : set([rEgypt, rMaghreb, rEthiopia, rSouthAfrica, rWestAfrica]),
	iArea_SouthAmerica : set([rCaribbean, rMesoamerica, rBrazil, rArgentina, rPeru, rColombia]),
	iArea_NorthAmerica : set([rCanada, rAlaska, rUnitedStates]),
}

#Projects

iNumProjects = 21
(iManhattanProject, iTheInternet, iHumanGenome, iSDI, iGPS, iISS, iBallisticMissile, iFirstSatellite, iManInSpace, iLunarLanding,
iGoldenRecord, iMarsMission, iLunarColony, iInterstellarProbe, iMarsFraming, iMarsPowerSource, iMarsExtractor, iMarsHabitat, iMarsHydroponics, iMarsLaboratory, iMarsControlCenter) = range(iNumProjects)

lMarsBaseComponents = [iMarsFraming, iMarsPowerSource, iMarsExtractor, iMarsHabitat, iMarsHydroponics, iMarsLaboratory, iMarsControlCenter]

#Eras

iNumEras = 7
(iAncient, iClassical, iMedieval, iRenaissance, iIndustrial, iGlobal, iDigital) = range (iNumEras)


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
(iLeaderBarbarian, iNativeLeader, iIndependentLeader, iAlexanderTheGreat, iAsoka, iAugustus, iBismarck, iBoudica, iBrennus, iCatherine, 
iCharlemagne, iChurchill, iCyrus, iDarius, iDeGaulle, iElizabeth, iFrederick, iGandhi, iGenghisKhan, iSargon, 
iHammurabi, iHannibal, iCleopatra, iHuaynaCapac, iIsabella, iJoao, iJuliusCaesar, iJustinian, iKublaiKhan, iLincoln, 
iLouis, iMansaMusa, iMao, iMehmed, iMontezuma, iNapoleon, iPacal, iPericles, iPeter, iQinShiHuang, 
iRamesses, iRagnar, iRoosevelt, iSaladin, iSittingBull, iStalin, iSuleiman, iSuryavarman, iOdaNobunaga, iVictoria, 
iWangKon, iWashington, iWillemVanOranje, iZaraYaqob, iKammu, iMeiji, iAkbar, iHiram, iMenelik, iGustav, 
iMongkut, iPhilip, iBarbarossa, iCharles, iFrancis, iIvan, iAfonso, iAtaturk, iMaria, iHitler,
iFranco, iAlexanderII, iCavour, iAbbas, iKhomeini, iTaizong, iHongwu, iDharmasetu, iHayamWuruk, iSuharto, 
iShahuji, iNaresuan, iAlpArslan, iBaibars, iNasser, iAlfred, iTrudeau, iChandragupta, iTughluq, iBasil, 
iRahman, iRajendra, iLobsangGyatso, iSobieski, iVatavelli, iMbemba, iHarun, iSongtsen, iCasimir, iYaqub, 
iLorenzo, iSantaAnna, iJuarez, iCardenas, iPedro, iSanMartin, iPeron, iBolivar, iAhoeitu, iKrishnaDevaRaya, 
iMussolini, iSejong, iBhutto, iPilsudski, iWalesa, iGerhardsen, iVargas, iMacDonald, iCastilla, iWilliam,
iGeorge, iKhosrow, iBumin, iTamerlane, iEzana) = range(iNumLeaders)

resurrectionLeaders = {
}

rebirthLeaders = {
}

tTradingCompanyPlotLists = (
[(109, 33)], #Spain
[(101, 37), (101, 36), (102, 36), (102, 35), (103, 35), (103, 34), (104, 34), (104, 33)], #France
[(95, 37), (94, 37), (94, 36), (94, 35), (94, 34), (93, 34), (93, 33), (92, 33), (92, 32), (88, 33), (88, 34), (88, 35)], #England
)

lSecondaryCivs = []

lMongolCivs = []

# MacAurther TODO: Add more starting dates?
(i1600AD, i1770AD, i1850AD) = range(3)

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