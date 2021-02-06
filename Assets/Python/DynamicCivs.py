# coding: utf-8

from CvPythonExtensions import *
import CvUtil
import PyHelpers
from Consts import *
import Victory as vic
from StoredData import data
from RFCUtils import utils
import CityNameManager as cnm
import Areas

### Constants ###

gc = CyGlobalContext()
localText = CyTranslator()

encoding = "utf-8"

tBrazilTL = (32, 14)
tBrazilBR = (43, 30)
tNCAmericaTL = (3, 33)
tNCAmericaBR = (37, 63)

tBritainTL = (48, 53)
tBritainBR = (54, 60)

tEuropeanRussiaTL = (68, 50)
tEuropeanRussiaBR = (80, 62)
tEuropeanRussiaExceptions = ((68, 59), (68, 60), (68, 61), (68, 62))

tKhazariaTL = (71, 46)
tKhazariaBR = (79, 53)
tAnatoliaTL = (69, 41)
tAnatoliaBR = (75, 45)
iTurkicEastWestBorder = 89

tColombiaTL = (24, 26)
tColombiaBR = (28, 32)

### Setup methods ###

def findCapitalLocations(dCapitals):
	dLocations = {}
	for iPlayer in dCapitals:
		for sCapital in dCapitals[iPlayer]:
			dLocations[sCapital] = cnm.findLocations(iPlayer, sCapital)
	return dLocations

### Dictionaries with text keys

dDefaultInsertNames = {
}

dDefaultInsertAdjectives = {
}

dSpecificVassalTitles = {
	iSpain : {
		iFrance : "TXT_KEY_CIV_SPANISH_FRANCE",
		iAmerica : "TXT_KEY_CIV_SPANISH_AMERICA",
	},
	iFrance : {
		iEngland : "TXT_KEY_CIV_FRENCH_ENGLAND",
		iAmerica : "TXT_KEY_CIV_FRENCH_AMERICA",
	},
	iEngland : {
		iFrance : "TXT_KEY_CIV_ENGLISH_FRANCE",
		iAmerica : "TXT_KEY_CIV_ENGLISH_AMERICA",
	},
	iAmerica : {
		iEngland : "TXT_KEY_CIV_AMERICAN_ENGLAND",
	},
}

dMasterTitles = {
	iSpain : "TXT_KEY_CIV_SPANISH_VASSAL",
	iFrance : "TXT_KEY_ADJECTIVE_TITLE",
	iEngland : "TXT_KEY_CIV_ENGLISH_VASSAL",
}

dCommunistVassalTitlesGeneric = {
}

dCommunistVassalTitles = {
}

dFascistVassalTitlesGeneric = {
}

dFascistVassalTitles = {
}

dForeignAdjectives = {
}

dForeignNames = {
}

lRepublicOf = []
lRepublicAdj = [iSpain, iFrance]

lSocialistRepublicOf = []
lSocialistRepublicAdj = []

lPeoplesRepublicOf = []
lPeoplesRepublicAdj = []

lIslamicRepublicOf = []

lCityStatesStart = []

dEmpireThreshold = {
}

lChristianity = [iCatholicism, iOrthodoxy, iAnglicanism, iPuritanism, iBaptism, iMethodism, iMormonism]
lProtestant = [iAnglicanism, iPuritanism, iBaptism, iMethodism]

lRespawnNameChanges = []
lVassalNameChanges = []
lChristianityNameChanges = []

lRebirths = []
lColonies = []

dNameChanges = {
}

dAdjectiveChanges = {
}

dCapitals = {
	iSpain : ["La Paz", "Barcelona", "Valencia"],
}

dCapitalLocations = findCapitalLocations(dCapitals)

dStartingLeaders = [
# 1600 AD
{
	iSpain : iSpanishKing,
	iFrance : iFrenchKing,
	iEngland : iEnglishKing,
	iVirginia : iRolfe,
	iMassachusetts : iAdams,
	iNewHampshire : iWiggin,
	iMaryland : iCalvert,
	iConnecticut : iHooker,
	iRhodeIsland : iWilliams,
	iNorthCarolina : iRaleigh,
	iSouthCarolina : iSayle,
	iNewJersey : iHyde,
	iNewYork : iBurnet,
	iPennsylvania : iPenn,
	iDelaware : iBiggs,
	iGeorgia : iOglethorpe,
	iAmerica : iWashington,
	iCanada : iMacDonald,
}
]

### Event handlers

def setup():			
	iScenario = utils.getScenario()
	
	for iPlayer in range(iNumPlayers):
		setDesc(iPlayer, peoplesName(iPlayer))
		
		if gc.getPlayer(iPlayer).getNumCities() > 0:
			checkName(iPlayer)
		
		if (tBirth[iPlayer] >= gc.getGame().getGameTurnYear() or gc.getPlayer(iPlayer).getNumCities() > 0) and not gc.getPlayer(iPlayer).isHuman():
			setLeader(iPlayer, startingLeader(iPlayer))
		
def onCivRespawn(iPlayer, tOriginalOwners):
	data.players[iPlayer].iResurrections += 1
	
	if iPlayer in lRespawnNameChanges:
		nameChange(iPlayer)
		adjectiveChange(iPlayer)
		
	setDesc(iPlayer, defaultTitle(iPlayer))
	checkName(iPlayer)
	checkLeader(iPlayer)
	
def onVassalState(iMaster, iVassal):
	if iVassal in lVassalNameChanges:
	
		data.players[iVassal].iResurrections += 1
		nameChange(iVassal)
		adjectiveChange(iVassal)
		
	checkName(iVassal)
	
def onPlayerChangeStateReligion(iPlayer, iReligion):
	if iPlayer in lChristianityNameChanges and iReligion in lChristianity:
		data.players[iPlayer].iResurrections += 1
		nameChange(iPlayer)
		adjectiveChange(iPlayer)
		
	checkName(iPlayer)
	
def onRevolution(iPlayer):
	data.players[iPlayer].iAnarchyTurns += 1
	
	checkName(iPlayer)
	
	for iLoopPlayer in range(iNumPlayers):
		if gc.getTeam(iLoopPlayer).isVassal(iPlayer):
			checkName(iLoopPlayer)
	
def onCityAcquired(iPreviousOwner, iNewOwner):
	checkName(iPreviousOwner)
	checkName(iNewOwner)
	
def onCityRazed(iOwner):
	checkName(iOwner)
	
def onCityBuilt(iOwner):
	checkName(iOwner)
	
def onTechAcquired(iPlayer, iTech):
	iEra = gc.getTechInfo(iTech).getEra()

	checkName(iPlayer)
	
def onPalaceMoved(iPlayer):
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	iEra = gc.getPlayer(iPlayer).getCurrentEra()

	
	checkName(iPlayer)
	
def onReligionFounded(iPlayer):
	checkName(iPlayer)
	
def checkTurn(iGameTurn):
	for iPlayer in range(iNumPlayers):
		checkName(iPlayer)
		checkLeader(iPlayer)
		
def checkName(iPlayer):
	if not gc.getPlayer(iPlayer).isAlive(): return
	if iPlayer >= iNumPlayers: return
	if gc.getPlayer(iPlayer).getNumCities() == 0: return
	setDesc(iPlayer, desc(iPlayer, title(iPlayer)))
	
def checkLeader(iPlayer):
	if not gc.getPlayer(iPlayer).isAlive(): return
	if iPlayer >= iNumPlayers: return
	setLeader(iPlayer, leader(iPlayer))
	setLeaderName(iPlayer, leaderName(iPlayer))

### Setter methods for player object ###

def setDesc(iPlayer, sName):
	try:
		gc.getPlayer(iPlayer).setCivDescription(sName)
	except:
		pass
	
def setShort(iPlayer, sShort):
	gc.getPlayer(iPlayer).setCivShortDescription(sShort)
	
def setAdjective(iPlayer, sAdj):
	gc.getPlayer(iPlayer).setCivAdjective(sAdj)
	
def setLeader(iPlayer, iLeader):
	if not iLeader: return
	if gc.getPlayer(iPlayer).getLeader() == iLeader: return
	gc.getPlayer(iPlayer).setLeader(iLeader)
	
def setLeaderName(iPlayer, sName):
	if not sName: return
	if gc.getLeaderHeadInfo(gc.getPlayer(iPlayer).getLeader()).getText() != sName:
		gc.getPlayer(iPlayer).setLeaderName(sName)

### Utility methods ###

def getOrElse(dDictionary, iPlayer, sDefault=None):
	if iPlayer in dDictionary: return dDictionary[iPlayer]
	return sDefault

def key(iPlayer, sSuffix):
	if sSuffix: sSuffix = "_" + sSuffix
	return "TXT_KEY_CIV_" + short(iPlayer).replace(" ", "_").upper() + sSuffix

def text(sTextKey, tInput=()):
	return localText.getText(sTextKey.encode(encoding), tInput)
	
def desc(iPlayer, sTextKey=str("%s1")):
	if isVassal(iPlayer): return text(sTextKey, (name(iPlayer), adjective(iPlayer), name(iPlayer, True), adjective(iPlayer, True)))

	return text(sTextKey, (name(iPlayer), adjective(iPlayer)))

def short(iPlayer):
	return gc.getPlayer(iPlayer).getCivilizationShortDescription(0)
	
def civAdjective(iPlayer):
	return gc.getPlayer(iPlayer).getCivilizationAdjective(0)

def capitalName(iPlayer):
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	if capital: 
		sCapitalName = cnm.getRenameName(iEngland, capital.getName())
		if sCapitalName: return sCapitalName
		else: return capital.getName()
	
	return short(iPlayer)
	
def nameChange(iPlayer):
	if iPlayer in dNameChanges:
		setShort(iPlayer, text(dNameChanges[iPlayer]))
	
def adjectiveChange(iPlayer):
	if iPlayer in dAdjectiveChanges:
		setAdjective(iPlayer, text(dAdjectiveChanges[iPlayer]))
	
def getColumn(iPlayer):
	lTechs = [gc.getTechInfo(iTech).getGridX() for iTech in range(iNumTechs) if gc.getTeam(iPlayer).isHasTech(iTech)]
	if not lTechs: return 0
	return max(lTechs)
	
### Utility methods for civilization status ###

def getCivics(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	return (pPlayer.getCivics(i) for i in range(6))

def isCommunist(iPlayer):
	iGovernment, iLegitimacy, iSociety, iEconomy, _, _ = getCivics(iPlayer)
	
	# MacAurther: Communist detected on American soil. Lethal force engaged
	# i.e. no communist civics
	
	#if iLegitimacy == iVassalage: return False
	
	#if iEconomy == iCentralPlanning: return True
	
	#if iGovernment == iStateParty and iSociety != iTotalitarianism and iEconomy not in [iMerchantTrade, iFreeEnterprise]: return True
		
	return False
	
def isFascist(iPlayer):
	iGovernment, _, iSociety, _, _, _ = getCivics(iPlayer)
	
	# MacAurther: Same deal, no fascist civics
	#if iSociety == iTotalitarianism: return True
	
	#if iGovernment == iStateParty: return True
		
	return False
	
def isRepublic(iPlayer):
	iGovernment, iLegitimacy, _, _, _, _ = getCivics(iPlayer)
	
	# MacAurther TODO: Cleanup
	#if iGovernment == iDemocracy: return True
	
	#if iGovernment in [iDespotism, iRepublic, iElective] and iLegitimacy == iConstitution: return True
	
	return False
	
def isCityStates(iPlayer):
	iGovernment, iLegitimacy, _, _, _, _ = getCivics(iPlayer)
	
	#if iLegitimacy not in [iAuthority, iCitizenship, iCentralism]: return False
	
	#if iGovernment in [iRepublic, iElective, iDemocracy]: return True
	
	#if iGovernment == iChiefdom and iPlayer in lCityStatesStart: return True
	
	return False
	
def isVassal(iPlayer):
	return utils.isAVassal(iPlayer)
	
def isCapitulated(iPlayer):
	return isVassal(iPlayer) and gc.getTeam(iPlayer).isCapitulated()
	
def getMaster(iPlayer):
	return utils.getMaster(iPlayer)
	
def isEmpire(iPlayer):
	if isVassal(iPlayer): return False

	return gc.getPlayer(iPlayer).getNumCities() >= getEmpireThreshold(iPlayer)
	
def getEmpireThreshold(iPlayer):
	if iPlayer in dEmpireThreshold: return dEmpireThreshold[iPlayer]
	
	if gc.getPlayer(iPlayer).isReborn():
		pass
		
	return 5
	
def isAtWar(iPlayer):
	for iTarget in range(iNumPlayers):
		if gc.getTeam(iPlayer).isAtWar(iTarget):
			return True
	return False
	
def isCapital(iPlayer, lNames):
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	if not capital: return False
	
	tLocation = (capital.getX(), capital.getY())
	
	for sName in lNames:
		if tLocation in dCapitalLocations[sName]:
			return True
			
	return False
	
def countAreaCities(lPlots):
	return len(utils.getAreaCities(lPlots))
	
def countPlayerAreaCities(iPlayer, lPlots):
	return len(utils.getAreaCitiesCiv(iPlayer, lPlots))
	
def isAreaControlled(iPlayer, tTL, tBR, iMinCities=1, tExceptions=()):
	lPlots = utils.getPlotList(tTL, tBR, tExceptions)
	return isPlotListControlled(iPlayer, lPlots, iMinCities)
	
def isRegionControlled(iPlayer, iRegion, iMinCities=1):
	lPlots = utils.getRegionPlots(iRegion)
	return isPlotListControlled(iPlayer, lPlots, iMinCities)
	
def isPlotListControlled(iPlayer, lPlots, iMinCities=1):
	iTotalCities = countAreaCities(lPlots)
	iPlayerCities = countPlayerAreaCities(iPlayer, lPlots)
	
	if iPlayerCities < iTotalCities: return False
	if iPlayerCities < iMinCities: return False
	
	return True
	
def capitalCoords(iPlayer):
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	if capital: return (capital.getX(), capital.getY())
	
	return (-1, -1)
	
def controlsHolyCity(iPlayer, iReligion):
	holyCity = gc.getGame().getHolyCity(iReligion)
	if holyCity and holyCity.getOwner() == iPlayer: return True
	
	return False
	
def controlsCity(iPlayer, tPlot):
	x, y = tPlot
	plot = gc.getMap().plot(x, y)
	
	return plot.isCity() and plot.getPlotCity().getOwner() == iPlayer
	
### Naming methods ###

def name(iPlayer, bIgnoreVassal = False):
	if isCapitulated(iPlayer) and not bIgnoreVassal:
		sVassalName = vassalName(iPlayer, getMaster(iPlayer))
		if sVassalName: return sVassalName
		
	if isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer):
		sRepublicName = republicName(iPlayer)
		if sRepublicName: return sRepublicName
		
	sSpecificName = specificName(iPlayer)
	if sSpecificName: return sSpecificName
	
	sDefaultInsertName = getOrElse(dDefaultInsertNames, iPlayer)
	if sDefaultInsertName: return sDefaultInsertName
	
	return short(iPlayer)
	
def vassalName(iPlayer, iMaster):
	
	if gc.getPlayer(iPlayer).isReborn(): return short(iPlayer)

	sSpecificName = getOrElse(getOrElse(dForeignNames, iMaster, {}), iPlayer)
	if sSpecificName: return sSpecificName
	
	return None
	
def republicName(iPlayer):

	return short(iPlayer)
	
def peoplesName(iPlayer):
	return desc(iPlayer, key(iPlayer, "PEOPLES"))
	
def specificName(iPlayer):
	iGameTurn = gc.getGame().getGameTurn()
	pPlayer = gc.getPlayer(iPlayer)
	tPlayer = gc.getTeam(pPlayer.getTeam())
	iCivicGovernment, iCivicLegal, iCivicLabor, iCivicEconomy, iCivicImmigration, iCivicDevelopment = getCivics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return short(iPlayer)
	
	bReborn = pPlayer.isReborn()
	iReligion = pPlayer.getStateReligion()
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	#bTheocracy = (iCivicReligion == iTheocracy)
	bResurrected = data.players[iPlayer].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.players[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = gc.getGame().getCurrentEra()
	bWar = isAtWar(iPlayer)

	# MacAurther TODO
	if iPlayer == iSpain:
		pass
			
	elif iPlayer == iFrance:
		pass
			
	elif iPlayer == iEngland:
		pass
	
def adjective(iPlayer, bIgnoreVassal = False):
	if isCapitulated(iPlayer):
		sForeignAdjective = getOrElse(getOrElse(dForeignAdjectives, getMaster(iPlayer), {}), iPlayer)
		if sForeignAdjective: return sForeignAdjective
		
		if not bIgnoreVassal: return adjective(getMaster(iPlayer))
		
	if isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer):
		sRepublicAdjective = republicAdjective(iPlayer)
		if sRepublicAdjective: return sRepublicAdjective
		
	sSpecificAdjective = specificAdjective(iPlayer)
	if sSpecificAdjective: return sSpecificAdjective
	
	#sDefaultInsertAdjective = getOrElse(dDefaultInsertAdjectives, iPlayer)
	#if sDefaultInsertAdjective: return sDefaultInsertAdjective
	
	return gc.getPlayer(iPlayer).getCivilizationAdjective(0)
	
def republicAdjective(iPlayer):
	
	return gc.getPlayer(iPlayer).getCivilizationAdjective(0)
	
def specificAdjective(iPlayer):
	iGameTurn = gc.getGame().getGameTurn()
	pPlayer = gc.getPlayer(iPlayer)
	tPlayer = gc.getTeam(pPlayer.getTeam())
	iCivicGovernment, iCivicLegal, iCivicLabor, iCivicEconomy, iCivicImmigration, iCivicDevelopment = getCivics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return gc.getPlayer(iPlayer).getCivilizationAdjective(0)
	
	bReborn = pPlayer.isReborn()
	iReligion = pPlayer.getStateReligion()
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	#bTheocracy = (iCivicReligion == iTheocracy)
	bResurrected = data.players[iPlayer].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.players[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = gc.getGame().getCurrentEra()
	bWar = isAtWar(iPlayer)
	
	bMonarchy = not isCommunist(iPlayer) and not isFascist(iPlayer) and not isRepublic(iPlayer)
	
	# MacAurther TODO
	if iPlayer == iSpain:
		pass
			
	elif iPlayer == iFrance:
		pass
			
	elif iPlayer == iEngland:
		pass
	
### Title methods ###

def title(iPlayer):
	if isCapitulated(iPlayer):
		sVassalTitle = vassalTitle(iPlayer, getMaster(iPlayer))
		if sVassalTitle: return sVassalTitle
		
	if isCommunist(iPlayer):
		sCommunistTitle = communistTitle(iPlayer)
		if sCommunistTitle: return sCommunistTitle
		
	if isFascist(iPlayer):
		sFascistTitle = fascistTitle(iPlayer)
		if sFascistTitle: return sFascistTitle
		
	if isRepublic(iPlayer):
		sRepublicTitle = republicTitle(iPlayer)
		if sRepublicTitle: return sRepublicTitle
		
	sSpecificTitle = specificTitle(iPlayer)
	if sSpecificTitle: return sSpecificTitle
	
	return defaultTitle(iPlayer)
	
def vassalTitle(iPlayer, iMaster):
	if isCommunist(iMaster):
		sCommunistTitle = getOrElse(getOrElse(dCommunistVassalTitles, iMaster, {}), iPlayer)
		if sCommunistTitle: return sCommunistTitle
		
		sCommunistTitle = getOrElse(dCommunistVassalTitlesGeneric, iMaster)
		if sCommunistTitle: return sCommunistTitle
		
	if isFascist(iMaster):
		sFascistTitle = getOrElse(getOrElse(dFascistVassalTitles, iMaster, {}), iPlayer)
		if sFascistTitle: return sFascistTitle
		
		sFascistTitle = getOrElse(dFascistVassalTitlesGeneric, iMaster)
		if sFascistTitle: return sFascistTitle
			

	if iMaster not in lRebirths or not gc.getPlayer(iMaster).isReborn():
		sSpecificTitle = getOrElse(getOrElse(dSpecificVassalTitles, iMaster, {}), iPlayer)
		if sSpecificTitle: return sSpecificTitle
	
		sMasterTitle = getOrElse(dMasterTitles, iMaster)
		if sMasterTitle: return sMasterTitle
		
	if iPlayer in lColonies:
		return "TXT_KEY_COLONY_OF"
	
	return "TXT_KEY_PROTECTORATE_OF"
	
def communistTitle(iPlayer):
	if iPlayer in lSocialistRepublicOf: return "TXT_KEY_SOCIALIST_REPUBLIC_OF"
	if iPlayer in lSocialistRepublicAdj: return "TXT_KEY_SOCIALIST_REPUBLIC_ADJECTIVE"
	if iPlayer in lPeoplesRepublicOf: return "TXT_KEY_PEOPLES_REPUBLIC_OF"
	if iPlayer in lPeoplesRepublicAdj: return "TXT_KEY_PEOPLES_REPUBLIC_ADJECTIVE"

	return key(iPlayer, "COMMUNIST")
	
def fascistTitle(iPlayer):
	return key(iPlayer, "FASCIST")
	
def republicTitle(iPlayer):
	
	if iPlayer == iEngland:
		iEra = gc.getPlayer(iPlayer).getCurrentEra()
		if isEmpire(iEngland) and iEra == iIndustrialEra:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra >= iInformation:
			return "TXT_KEY_CIV_ENGLAND_UNITED_REPUBLIC"
	
	#MacAurther TODO:
	#if iPlayer == iAmerica:
	#	_, _, iCivicLabor, _, _, _ = getCivics(iPlayer)
	#	if iCivicSociety in [iSlavery]:
	#		return key(iPlayer, "CSA")
	
	if iPlayer in lRepublicOf: return "TXT_KEY_REPUBLIC_OF"
	if iPlayer in lRepublicAdj: return "TXT_KEY_REPUBLIC_ADJECTIVE"
	
	return key(iPlayer, "REPUBLIC")

def defaultTitle(iPlayer):
	return desc(iPlayer, key(iPlayer, "DEFAULT"))
	
def specificTitle(iPlayer, lPreviousOwners=[]):
	iGameTurn = gc.getGame().getGameTurn()
	pPlayer = gc.getPlayer(iPlayer)
	tPlayer = gc.getTeam(pPlayer.getTeam())
	iCivicGovernment, iCivicLegal, iCivicLabor, iCivicEconomy, iCivicImmigration, iCivicDevelopment = getCivics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return defaultTitle(iPlayer)
	
	bReborn = pPlayer.isReborn()
	iReligion = pPlayer.getStateReligion()
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	#bTheocracy = (iCivicReligion == iTheocracy)
	bResurrected = data.players[iPlayer].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.players[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = gc.getGame().getCurrentEra()
	bWar = isAtWar(iPlayer)

	# MacAurther TODO
	if iPlayer == iSpain:
			
		if bEmpire and iEra > iExplorationEra:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra == iExplorationEra and isCapital(iPlayer, ["Barcelona", "Valencia"]):
			return "TXT_KEY_CIV_SPAIN_CROWN_OF"
			
	elif iPlayer == iFrance:
		if not tCapitalCoords in Areas.getNormalArea(iPlayer):
			return "TXT_KEY_CIV_FRANCE_EXILE"
			
		if iEra >= iIndustrialEra and bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iPlayer == iEngland:
		if not utils.isPlotInCore(iPlayer, tCapitalCoords):
			return "TXT_KEY_CIV_ENGLAND_EXILE"
			
		if iEra == iExplorationEra and getMaster(iFrance) == iEngland:
			return "TXT_KEY_CIV_ENGLAND_ANGEVIN_EMPIRE"
			
		if getColumn(iPlayer) >= 11:
			if bEmpire:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
		
			if countPlayerAreaCities(iPlayer, utils.getPlotList(tBritainTL, tBritainBR)) >= 3:
				return "TXT_KEY_CIV_ENGLAND_UNITED_KINGDOM_OF"
	
	#MacAurther TODO
	#elif iPlayer == iAmerica:
	#	if iCivicSociety in [iSlavery, iManorialism]:
	#		if isRegionControlled(iAmerica, rMesoamerica) and isRegionControlled(iAmerica, rCaribbean):
	#			return "TXT_KEY_CIV_AMERICA_GOLDEN_CIRCLE"
		
			return "TXT_KEY_CIV_AMERICA_CSA"
			
	return None
			
### Leader methods ###

def startingLeader(iPlayer):
	if iPlayer in dStartingLeaders[utils.getScenario()]: return dStartingLeaders[utils.getScenario()][iPlayer]

	return dStartingLeaders[i1600AD][iPlayer]
	
def leader(iPlayer):
	if iPlayer >= iNumPlayers: return None
	
	if not gc.getPlayer(iPlayer).isAlive(): return None
	
	if gc.getPlayer(iPlayer).isHuman(): return None
	
	pPlayer = gc.getPlayer(iPlayer)
	tPlayer = gc.getTeam(pPlayer.getTeam())
	bReborn = pPlayer.isReborn()
	iReligion = pPlayer.getStateReligion()
	capital = gc.getPlayer(iPlayer).getCapitalCity()
	tCapitalCoords = (capital.getX(), capital.getY())
	iCivicGovernment, iCivicLegal, iCivicLabor, iCivicEconomy, iCivicImmigration, iCivicDevelopment = getCivics(iPlayer)
	iGameTurn = gc.getGame().getGameTurn()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	#bTheocracy = (iCivicReligion == iTheocracy)
	bResurrected = data.players[iPlayer].iResurrections > 0
	bMonarchy = not (isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer))
	iAnarchyTurns = data.players[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = gc.getGame().getCurrentEra()
	
	#MacAurther TODO: Change of leaders
	if iPlayer == iSpain:
		pass
		
	elif iPlayer == iFrance:
		pass
		
	elif iPlayer == iEngland:
		pass
			
	elif iPlayer == iAmerica:
		pass
		
	return startingLeader(iPlayer)
		
	
def leaderName(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = pPlayer.getLeader()
	
	iGameTurn = gc.getGame().getGameTurn()
	
	return None