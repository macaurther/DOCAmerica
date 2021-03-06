# Rhye's and Fall of Civilization - Constants
# globals

from CvPythonExtensions import *
gc = CyGlobalContext()

iWorldX = 150
iWorldY = 80

# initialise player variables to player IDs from WBS
iNumPlayers = 18
(iSpain, iFrance, iEngland, iVirginia, iMassachusetts, iNewHampshire, iMaryland, iConnecticut, iRhodeIsland, 
iNorthCarolina, iSouthCarolina, iNewJersey, iNewYork, iPennsylvania, iDelaware, iGeorgia, iAmerica, iCanada) = range(iNumPlayers)

(pSpain, pFrance, pEngland, pVirginia, pMassachusetts, pNewHampshire, pMaryland, pConnecticut, pRhodeIsland, 
pNorthCarolina, pSouthCarolina, pNewJersey, pNewYork, pPennsylvania, pDelaware, pGeorgia, pAmerica, pCanada) = [gc.getPlayer(i) for i in range(iNumPlayers)]

(teamSpain, teamFrance, teamEngland, teamVirginia, teamMassachusetts, teamNewHampshire, teamMaryland, teamConnecticut, teamRhodeIsland, 
teamNorthCarolina, teamSouthCarolina, teamNewJersey, teamNewYork, teamPennsylvania, teamDelaware, teamGeorgia, teamAmerica, teamCanada) = [gc.getTeam(i) for i in range(iNumPlayers)]

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
[iAmerica, iSouthCarolina, iVirginia], # North Carolina
[iAmerica, iNorthCarolina, iGeorgia], # South Carolina
[iAmerica, iNewYork, iPennsylvania, iDelaware], # New Jersey
[iAmerica, iNewHampshire, iConnecticut, iMassachusetts, iPennsylvania, iNewJersey], # New York
[iAmerica, iNewYork, iVirginia, iNewJersey, iDelaware, iMaryland], # Pennsylvania
[iAmerica, iMaryland, iNewJersey, iPennsylvania], # Delaware
[iAmerica, iSpain, iSouthCarolina], # Georgia
[], #America
[], #Canada
]

#for stability hit on spawn
lOlderNeighbours = [
[], #Spain
[], #France
[], #England
[], #Virginia
[], #Massachusetts
[], #New Hampshire
[], #Maryland
[], #Connecticut
[], #Rhode Island
[], #North Carolina
[], #South Carolina
[], #New Jersey
[], #New York
[], #Pennsylvania
[], #Delaware
[], #Georgia
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
1653,		# North Carolina
1663,		# South Carolina
1664,		# New Jersey
1664,		# New York
1682,		# Pennsylvania
1682,		# Delaware
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
2020,					# North Carolina
2020,					# South Carolina
2020,					# New Jersey
2020,					# New York
2020,					# Pennsylvania
2020,					# Delaware
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
iCivNorthCarolina : (1900, 1950, 2000),
iCivSouthCarolina : (1900, 1950, 2000),
iCivNewJersey : (1900, 1950, 2000),
iCivNewYork : (1900, 1950, 2000),
iCivPennsylvania : (1900, 1950, 2000),
iCivDelaware : (1900, 1950, 2000),
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
[(1700, 2020)], #North Carolina
[(1700, 2020)], #South Carolina
[(1700, 2020)], #New Jersey
[(1700, 2020)], #New York
[(1700, 2020)], #Pennsylvania
[(1700, 2020)], #Delaware
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
[], #North Carolina
[], #South Carolina
[], #New Jersey
[], #New York
[], #Pennsylvania
[], #Delaware
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
[], #North Carolina
[], #South Carolina
[], #New Jersey
[], #New York
[], #Pennsylvania
[], #Delaware
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
1, #North Carolina
1, #South Carolina
1, #New Jersey
1, #New York
1, #Pennsylvania
1, #Delaware
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
	50, #North Carolina
	50, #South Carolina
	50, #New Jersey
	50, #New York
	50, #Pennsylvania
	50, #Delaware
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
100, #North Carolina
100, #South Carolina
100, #New Jersey
100, #New York
100, #Pennsylvania
100, #Delaware
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
100, #North Carolina
100, #South Carolina
100, #New Jersey
100, #New York
100, #Pennsylvania
100, #Delaware
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
iNumReligions = 8
(iJudaism, iOrthodoxy, iCatholicism, iAnglicanism, iPuritanism, iBaptism, iMethodism, iMormonism) = range(iNumReligions)

#Persecution preference
tPersecutionPreference = (
(iOrthodoxy, iCatholicism, iAnglicanism, iPuritanism, iBaptism, iMethodism, iMormonism), # Judaism
(iJudaism, iCatholicism, iAnglicanism, iPuritanism, iBaptism, iMethodism, iMormonism), # Orthodoxy
(iJudaism, iMormonism, iOrthodoxy, iAnglicanism, iPuritanism, iBaptism, iMethodism), # Catholicism
(iJudaism, iMormonism, iCatholicism, iOrthodoxy, iPuritanism, iBaptism, iMethodism), # Anglicanism
(iJudaism, iMormonism, iCatholicism, iOrthodoxy, iAnglicanism, iBaptism, iMethodism), # Puritanism
(iJudaism, iMormonism, iCatholicism, iOrthodoxy, iAnglicanism, iPuritanism, iMethodism), # Baptism
(iJudaism, iMormonism, iCatholicism, iOrthodoxy, iAnglicanism, iPuritanism, iBaptism), # Methodism
(iJudaism, iCatholicism, iOrthodoxy, iAnglicanism, iPuritanism, iBaptism, iMethodism), # Mormonism
)

lCatholicStart = [iSpain, iFrance]
lAnglicanStart = [iEngland, iVirginia, iNorthCarolina, iSouthCarolina, iNewJersey, iNewYork, iDelaware, iCanada]

# corporations
iNumCorporations = 9
(iSilkRoute, iTradingCompany, iCerealIndustry, iFishingIndustry, iTextileIndustry, iSteelIndustry, iOilIndustry, iLuxuryIndustry, iComputerIndustry) = range(iNumCorporations)

# initialise tech variables to unit indices from XML

iNumTechs = 123
(iTanning, iMining, iPottery, iSailing, iAgriculture, iMythology, iPastoralism,				#Pre Columbian
iAlloys, iSteel, iRiding, iNavigation, iWriting, iPhilosophy, iProperty,					#Post Columbian
iGunpowder, iCompanies, iFinance, iCartography, iJudiciary, iPrinting, iHumanities,			#Exploration
iFirearms, iColonization, iExploration, iOptics, iCharter, iIndentures, iCommunity,						#Colonial 1
iFortification, iLogistics, iTriangularTrade, iAcademia, iStatecraft, iUrbanPlanning, iHorticulture,	#Colonial 2
iPioneering, iEconomics, iGeography, iScientificMethod, iRepresentation, iCivilLiberties, iHeritage,	#Colonial 3
iTactics, iReplaceableParts, iPhysics, iMeasurement, iPostalService, iIndependence, iSocialContract,	#Revolutionary 1
iCurrency, iMedicine, iGeology, iParties, iSociology, iFederalism, 										#Revolutionary 2
iManifestDestiny, iEngineering, iChemistry, iTranscendentalism,		#Expansion 1
iElectricity, iBiology, iNationalism,								#Expansion 2
iHydraulics, iRailroad, iTelegraph, iNativism,						#Expansion 3
iMachineTools, iThermodynamics, iMetallurgy,												#Industrial 1
iBallistics, iEngine, iIndustrialism, iRefrigeration, iLaborUnions, iJournalism,			#Industrial 2
iPneumatics, iAssemblyLine, iRefining, iFilm, iMicrobiology, iConsumerism, iConservation,	#Industrial 3
iCombinedArms, iFlight, iHydraulicCement, iRadio, iPsychology, iYellowJournalism,						#Modern 1
iInfrastructure, iNACA, iSynthetics, iSkyscrapers, iNationalMilitaryEstablishment, iExceptionalism,		#Modern 2
iAviation, iMilitaryIndustrialComplex, iPublicHealth, iMacroeconomics, iSocialServices,					#Modern 3
iRadar, iRocketry, iFission, iElectronics, iTelevision, iPowerProjection, iCivilRights,		#Atomic 1
iNASA, iNuclearPower, iGlobalism, iSensationalism,											#Atomic 2
iAerodynamics, iSpaceflight, iLaser, iComputers, iTourism, iEcology,						#Information 1
iSatellites, iSuperconductors, iRobotics, iTelecommunications, iRenewableEnergy, iGenetics,	#Information 2
iSocialPrograms,) = range(iNumTechs)														#Information 3

# initialise unit variables to unit indices from XML

iNumUnits = 132
(iLion, iBear, iPanther, iWolf, iSettler, iPioneer, iWorker, iLabourer, 
iScout, iExplorer, iSeasonedScout, iSpy, iReligiousPersecutor, iJewishMissionary, iOrthodoxMissionary, iCatholicMissionary, iAnglicanMissionary, 
iPuritanMissionary, iBaptistMissionary, iMethodistMissionary, iMormonMissionary, iWarrior, iAxeman, iLightSwordsman, 
iDogSoldier, iSwordsman,
iSpearman, iPikeman, 
iMusketman, iTercio, iMohawk, iFusilier, iMilitia, iRanger, 
iMusketeer, iMinuteman, iHessian, iLineInfantry, iContinental, iRedcoat, iGrenadier, iRifleman, 
iAntiTank, iInfantry, iSamInfantry, iMobileSam, iMarine, iNavySeal, iParatrooper, iMechanizedInfantry, 
iArcher, iSkirmisher, iCrossbowman, 
iHorseman, iHorseArcher, iLancer, iPistolier, iMountedBrave, iCuirassier, iConquistador, 
iDragoon, iGrenadierCavalry, iCarabineer, iLlanero, iCavalry, iRural, 
iTank, iMainBattleTank, iGunship, 
iBombard, iMortar, iEarlyCannon, iLightCannon, iHeavyCannon, iArtillery, iMachineGun, iHowitzer, iMobileArtillery, 
iWorkboat, iCaravel, iCarrack, iGalleon, iEastIndiaman, iPrivateer, iCorsair, iSloop, iBrigantine, iFrigate, 
iShipOfTheLine, iManOfWar, iSteamship, iIronclad, iTorpedoBoat, iCruiser, 
iTransport, iDestroyer, iCorvette, iBattleship, iMissileCruiser, iStealthDestroyer, iSubmarine, iNuclearSubmarine, iCarrier, iBiplane, 
iFighter, iZero, iJetFighter, iBomber, iStealthBomber, iGuidedMissile, iDrone, iNuclearBomber, iICBM, iSatellite, 
iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral, iArgentineGreatGeneral, iGreatSpy, iFemaleGreatProphet, 
iFemaleGreatArtist, iFemaleGreatScientist, iFemaleGreatMerchant, iFemaleGreatEngineer, iFemaleGreatStatesman, iFemaleGreatGeneral, iFemaleGreatSpy, iSlave) = range(iNumUnits)

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

iNumBuildings = 170
(iPalace, iBarracks, iGranary, iSmokehouse, iPaganTemple, iMonument,
iTotemPole, iWalls, iStable, iLibrary,
iHarbor, iTheatre,
iArena, iLighthouse, iWeaver,
iMarket, iJail, iForge, 
iPharmacy, iPostOffice,
iWharf, iCrabbery, iBank, iConstabulary, iMountedPolice, iCustomsHouse, iUniversity,
iCivicSquare, iSewer, iStarFort, iEstate,
iDrydock, iLevee, iObservatory, iWarehouse, iCourthouse, iFactory,
iDistillery, iPark, iCoalPlant, iRailwayStation, iLaboratory, iNewsPress, iIndustrialPark, iCinema, iHospital, 
iSupermarket, iPublicTransportation, iDepartmentStore, iMall, iBroadcastTower, iIntelligenceAgency, iElectricalGrid, iAirport, iBunker, 
iBombShelters, iHydroPlant, iSecurityBureau, iStadium, iContainerTerminal, iNuclearPlant, iSupercomputer, iHotel, iRecyclingCenter, iLogisticsCenter, 
iSolarPlant, iFiberNetwork, iAutomatedFactory, iVerticalFarm, iJewishTemple, iJewishCathedral, iJewishMonastery, iJewishShrine, iOrthodoxTemple, iOrthodoxCathedral, 
iOrthodoxMonastery, iOrthodoxShrine, iCatholicChurch, iCatholicCathedral, iCatholicMonastery, iCatholicShrine, iAnglicanTemple, iAnglicanCathedral, iAnglicanMonastery, iAnglicanShrine, 
iPuritanTemple, iPuritanCathedral, iPuritanMonastery, iPuritanShrine, iBaptistTemple, iBaptistCathedral, iBaptistMonastery, iBaptistShrine, iMethodistTemple, iMethodistCathedral,
iMethodistMonastery, iMethodistShrine, iMormonTemple, iMormonCathedral, iMormonMonastery, iMormonShrine,
iAcademy, iAdministrativeCenter, iManufactory, iArmoury, iMuseum, iStockExchange, 
iTradingCompanyBuilding, iIberianTradingCompanyBuilding, iNationalMonument, iNationalTheatre, iNationalGallery, iNationalCollege, iMilitaryAcademy, iSecretService, iIronworks, iRedCross, 
iNationalPark, iCentralBank, iSpaceport,
iAbbey, iArmory, iArsenal, iButchery, iSchoolhouse, iCitadel, iCollege, iFortress, iLumberMill, iMagazine, 
iNewspaper, iPrintingPress, iSaloon, iShipyard, iSlaughterhouse, iStockade, iTavern, iTextileMill, iWell, iWaystation, 
iMountVernon, iMonticello, iCapeHatterasLighthouse, iFortMcHenry, iWestPoint, iSlaterMill, iRainbowRow, iHarvard, iPrinceton, iCapitol, 
iWhiteHouse, iIndependenceHall, 
iStatueOfLiberty,
iTriumphalArch, iMenloPark, iBrooklynBridge, iHollywood, iEmpireStateBuilding, 
iPalaceOfNations,
iGoldenGateBridge, iGraceland, iCNTower, iPentagon, iUnitedNations, iCrystalCathedral, 
iWorldTradeCenter,
iHubbleSpaceTelescope, iSpaceElevator, iLargeHadronCollider, iITER) = range(iNumBuildings)

iBeginWonders = iStatueOfLiberty # different from DLL constant because that includes national wonders

iTemple = iJewishTemple #generic
iCathedral = iJewishCathedral #generic
iMonastery = iJewishMonastery #generic
iShrine = iJewishShrine #generic

iFirstWonder = iStatueOfLiberty

iPlague = iNumBuildings
iNumBuildingsPlague = iNumBuildings+1

#Civics
iNumCivics = 42
(iShire, iRoyalColony, iTerritory, iCommonwealth, iDominion, iState, iNation,
iSheriffdom, iCommonLaw, iMartialLaw, iStatesRights, iFederalism, iSegregation, iUniversalSufferage,
iSerfdom, iIndenturedServitude, iSlavery, iCaptainsOfIndustry, iWorkersRights, iOutsourcing, iAutomation,
iLaissezFaire, iMercantilism, iAgrarianism, iIndustrialism, iManifestDestinyCivic, iConsumerismCivic, iPublicWelfare,
iForGloryGodAndGold, iHaven, iPenalColony, iFreeReligion, iIsolationism, iMeltingPot, iMulticulturism,
iCompanies, iHeadright, iRuralism, iUrbanism, iHomesteads, iSuburbanism, iGentrification) = range(iNumCivics)

iNumCivicCategories = 6
(iCivicsGovernment, iCivicsLegal, iCivicsLabor, iCivicsEconomy, iCivicsImmigration, iCivicsDevelopment) = range(iNumCivicCategories)

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
iNumRegions = 48
(rVirginia, rMassachusetts, rNewHampshire, rMaryland, rConnecticut, rRhodeIsland, rNorthCarolina, rSouthCarolina, rNewJersey, rNewYork, 
rPennsylvania, rDelaware, rGeorgia, rVermont, rKentucky, rTennessee, rOhio, rLouisiana, rIndiana, rMississippi,
rIllinois, rAlabama, rMaine, rMissouri, rArkansas, rMichigan, rFlorida, rTexas, rIowa, rWisconsin,
rCalifornia, rMinnesota, rOregon, rKansas, rWestVirginia, rNevada, rNebraska, rColorado, rNorthDakota, rSouthDakota,
rMontana, rWashington, rIdaho, rWyoming, rUtah, rOklahoma, rNewMexico, rArizona) = range(iNumRegions)


lSouthAtlantic = [rDelaware, rMaryland, rVirginia, rNorthCarolina, rSouthCarolina, rGeorgia, rFlorida]
lSouthCentral = [rWestVirginia, rKentucky, rTennessee, rAlabama, rMississippi, rLouisiana]
lWestSouth = [rArkansas, rOklahoma, rTexas, rMissouri, rKansas, rNewMexico]
lSouth = lSouthCentral + lSouthAtlantic + lWestSouth

lNewEngland = [rMaine, rNewHampshire, rVermont, rMassachusetts, rRhodeIsland, rConnecticut]
lMiddleAtlantic = [rNewYork, rPennsylvania, rNewJersey]
lNorthEast = lNewEngland + lMiddleAtlantic

lEastNorthCentral = [rMichigan, rOhio, rIndiana, rIllinois, rWisconsin]
lWestNorthCentral = [rNorthDakota, rMinnesota, rSouthDakota, rNebraska]
lMidWest = lEastNorthCentral + lWestNorthCentral

lNorth = lNorthEast + lMidWest

lMountain = [rMontana, rIdaho, rWyoming, rColorado, rUtah, rArizona, rNevada]
lPacific = [rWashington, rOregon, rCalifornia]
lWest = lMountain + lPacific

lContiguous = lSouth + lNorth + lWest


iArea_South = 1000
iArea_North = 1001
iArea_West = 1002

mercRegions = {
	iArea_South : set(lSouth),
	iArea_North : set(lNorth),
	iArea_West : set(lWest),
}

#Projects

iNumProjects = 21
(iManhattanProject, iTheInternet, iHumanGenome, iSDI, iGPS, iISS, iBallisticMissile, iFirstSatellite, iManInSpace, iLunarLanding,
iGoldenRecord, iMarsMission, iLunarColony, iInterstellarProbe, iMarsFraming, iMarsPowerSource, iMarsExtractor, iMarsHabitat, iMarsHydroponics, iMarsLaboratory, iMarsControlCenter) = range(iNumProjects)

lMarsBaseComponents = [iMarsFraming, iMarsPowerSource, iMarsExtractor, iMarsHabitat, iMarsHydroponics, iMarsLaboratory, iMarsControlCenter]

#Eras

iNumEras = 9
(iPreColumbianEra, iExplorationEra, iColonialEra, iRevolutionaryEra, iExpansionEra, iIndustrialEra,
iModernEra, iAtomicEra, iInformationEra) = range (iNumEras)


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

iNumLeaders = 21
(iLeaderBarbarian, iNativeLeader, iIndependentLeader, 
iSpanishKing, iFrenchKing, iEnglishKing, iRolfe, iAdams, iWiggin, iCalvert, iHooker, iWilliams, iRaleigh,
iSayle, iHyde, iBurnet, iPenn, iBiggs, iOglethorpe, iWashington, iMacDonald
# Future Leaderheads:
#iCatherine,
#iChurchill, iDeGaulle, iElizabeth,
#iIsabella, iJoao, iLincoln,
#iLouis, iNapoleon, iPeter,
#iRoosevelt,iSittingBull, iStalin, iVictoria, 
#iWashington, iWillemVanOranje, iMeiji, iGustav, 
#iPhilip, iCharles, iFrancis, iAfonso, iMaria,
#iFranco, iAlexanderII,
#iTrudeau,
#iSantaAnna, iJuarez, iCardenas, iPedro, iSanMartin, iPeron, iBolivar,
#iVargas, iMacDonald, iCastilla, iWilliam,
#iGeorge,
) = range(iNumLeaders)

resurrectionLeaders = {
}

rebirthLeaders = {
}

tTradingCompanyPlotLists = (
[], #Spain
[], #France
[], #England
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