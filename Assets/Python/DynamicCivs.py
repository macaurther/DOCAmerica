# coding: utf-8

from Civics import *
from RFCUtils import *
from Areas import *
from Locations import *
from Core import *

from Events import handler
from Core import name as short
from Core import adjective as civAdjective

import CityNameManager as cnm


### Constants ###

encoding = "utf-8"

### Dictionaries with text keys

dDefaultInsertNames = {
	iNetherlands : "TXT_KEY_CIV_NETHERLANDS_ARTICLE",
	iMaya : "TXT_KEY_CIV_MAYA_YUCATAN",
}

dDefaultInsertAdjectives = {
}

dSpecificVassalTitles = deepdict({
	iSpain : {
		iMaya : "TXT_KEY_CIV_SPANISH_MAYA",
		iFrance : "TXT_KEY_CIV_SPANISH_FRANCE",
		iNetherlands : "TXT_KEY_ADJECTIVE_TITLE",
		iPortugal : "TXT_KEY_CIV_SPANISH_PORTUGAL",
		iAmerica : "TXT_KEY_CIV_SPANISH_AMERICA",
		iArgentina : "TXT_KEY_CIV_SPANISH_ARGENTINA",
		iColombia : "TXT_KEY_CIV_SPANISH_COLOMBIA",
	},
	iFrance : {
		iEngland : "TXT_KEY_CIV_FRENCH_ENGLAND",
		iSpain : "TXT_KEY_CIV_FRENCH_SPAIN",
		iNetherlands : "TXT_KEY_CIV_FRENCH_NETHERLANDS",
		iPortugal : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iInca : "TXT_KEY_CIV_FRENCH_INCA",
		iAztecs : "TXT_KEY_CIV_FRENCH_AZTECS",
		iAmerica : "TXT_KEY_CIV_FRENCH_AMERICA",
	},
	iEngland : {
		iMaya : "TXT_KEY_CIV_ENGLISH_MAYA",
		iFrance : "TXT_KEY_CIV_ENGLISH_FRANCE",
		iNetherlands : "TXT_KEY_CIV_ENGLISH_NETHERLANDS",
		iAmerica : "TXT_KEY_CIV_ENGLISH_AMERICA",
	},
	iNetherlands : {
		iAmerica : "TXT_KEY_CIV_DUTCH_AMERICA",
		iBrazil : "TXT_KEY_CIV_DUTCH_BRAZIL",
	},
	iPortugal : {
		iBrazil : "TXT_KEY_CIV_PORTUGUESE_BRAZIL",
	},
	iAmerica : {
		iEngland : "TXT_KEY_CIV_AMERICAN_ENGLAND",
		iAztecs : "TXT_KEY_CIV_AMERICAN_MEXICO",
		iMaya : "TXT_KEY_CIV_AMERICAN_MAYA",
	},
	iBrazil : {
		iArgentina : "TXT_KEY_CIV_BRAZILIAN_ARGENTINA",
	},
})

dMasterTitles = {
	iSpain : "TXT_KEY_CIV_SPANISH_VASSAL",
	iFrance : "TXT_KEY_ADJECTIVE_TITLE",
	iEngland : "TXT_KEY_CIV_ENGLISH_VASSAL",
	iNetherlands : "TXT_KEY_ADJECTIVE_TITLE",
	iPortugal : "TXT_KEY_ADJECTIVE_TITLE",
}

dCommunistVassalTitlesGeneric = {
}

dCommunistVassalTitles = deepdict({
})

dFascistVassalTitlesGeneric = {
}

dFascistVassalTitles = deepdict({
})

dForeignAdjectives = deepdict({
})

dForeignNames = deepdict({
	iSpain : {
		iAztecs : "TXT_KEY_CIV_SPANISH_NAME_AZTECS",
	},
	iFrance : {
	},
	iEngland : {
	},
})

lRepublicOf = []
lRepublicAdj = [iSpain, iFrance, iPortugal, iInca, iAztecs, iArgentina]

lSocialistRepublicOf = [iBrazil, iColombia]
lSocialistRepublicAdj = [iAztecs, iArgentina]

lPeoplesRepublicOf = []
lPeoplesRepublicAdj = []

lIslamicRepublicOf = []

dEmpireThreshold = {
	iInca : 3,
}

lChristianity = [iCatholicism, iOrthodoxy, iProtestantism]

lRespawnNameChanges = [iInca, iAztecs] # TODO: this should be covered by period
lVassalNameChanges = [iInca, iAztecs] # TODO: this should be covered by period
lChristianityNameChanges = [iInca, iAztecs] # TODO: this should be covered by period

lColonies = [iAztecs, iInca, iMaya] # TODO: could be covered by more granular continental regions

dNameChanges = { # TODO: this should be covered by period
	iAztecs : "TXT_KEY_CIV_MEXICO_SHORT_DESC",
	iInca : "TXT_KEY_CIV_PERU_SHORT_DESC",
}

dAdjectiveChanges = {
	iAztecs : "TXT_KEY_CIV_MEXICO_ADJECTIVE",
	iInca : "TXT_KEY_CIV_PERU_ADJECTIVE",
}

dStartingLeaders = [
# 3000 BC
{
	iIndependent : iIndependentLeader,
	iIndependent2 : iIndependentLeader,
	iNative : iNativeLeader,
	iMaya : iPacal,
	iTeotihuacan : iAtlatlCauac,
	iTiwanaku : iMalkuHuyustus,
	iWari : iWariCapac,
	iMississippi : iRedHorn,
	iPuebloan : iLeaderBarbarian,	# TODO
	iMuisca : iSaguamanchica,
	iNorse : iRagnar,
	iChimu : iTacaynamo,
	iInuit : iAua,
	iInca : iHuaynaCapac,
	iAztecs : iMontezuma,
	iIroquois : iLeaderBarbarian,	# TODO: iHiawatha
	iSpain : iIsabella,
	iPortugal : iAfonso,
	iEngland : iAlfred,
	iFrance : iCharlemagne,
	iNetherlands : iWillemVanOranje,
	iAmerica : iWashington,
	iHaiti : iLeaderBarbarian,	# TODO: iLouverture
	iBolivia : iLeaderBarbarian,	# TODO
	iArgentina : iSanMartin,
	iMexico : iJuarez,
	iColombia : iBolivar,
	iChile : iLeaderBarbarian,	# TODO
	iPeru : iLeaderBarbarian,	# TODO
	iVenezuela : iLeaderBarbarian,	# TODO
	iBrazil : iPedro,
	iCanada : iMacDonald,
	iCuba : iLeaderBarbarian,	# TODO
},
# 600 AD
{
},
# 1700 AD
{
	iSpain : iPhilip,
	iFrance : iLouis,
	iEngland : iVictoria,
	iNetherlands : iWilliam,
	iPortugal : iJoao,
}]

### Event handlers

@handler("GameStart")
def setup():
	iScenario = scenario()
	
@handler("playerCivAssigned")
def initName(iPlayer):
	if not is_minor(iPlayer) and player(iPlayer).getNumCities() == 0:
		setDesc(iPlayer, peoplesName(iPlayer))
		checkName(iPlayer)
		checkLeader(iPlayer)

@handler("resurrection")
def onResurrection(iPlayer):
	onRespawn(iPlayer)

def onRespawn(iPlayer):
	data.civs[iPlayer].iResurrections += 1
	
	if civ(iPlayer) in lRespawnNameChanges:
		checkNameChange(iPlayer)
		checkAdjectiveChange(iPlayer)
		
	setDesc(iPlayer, defaultTitle(iPlayer))
	checkName(iPlayer)
	checkLeader(iPlayer)

@handler("vassalState")	
def onVassalState(iMaster, iVassal):
	iMasterCiv = civ(iMaster)
	iVassalCiv = civ(iVassal)

	if iVassalCiv in lVassalNameChanges:
		data.civs[iVassal].iResurrections += 1
		checkNameChange(iVassal)
		checkAdjectiveChange(iVassal)
		
	checkName(iVassal)

@handler("playerChangeStateReligion")
def onPlayerChangeStateReligion(iPlayer, iReligion):
	if is_minor(iPlayer):
		return

	if civ(iPlayer) in lChristianityNameChanges and iReligion in lChristianity:
		data.civs[iPlayer].iResurrections += 1
		checkNameChange(iPlayer)
		checkAdjectiveChange(iPlayer)
		
	checkName(iPlayer)

@handler("revolution")
def onRevolution(iPlayer):
	if is_minor(iPlayer):
		return

	data.civs[iPlayer].iAnarchyTurns += 1
	
	checkName(iPlayer)
	
	for iLoopPlayer in players.vassals(iPlayer):
		checkName(iLoopPlayer)
	
@handler("cityAcquired")
def onCityAcquired(iPreviousOwner, iNewOwner):
	checkName(iPreviousOwner)
	checkName(iNewOwner)

@handler("cityRazed")
def onCityRazed(city):
	iPreviousOwner = slot(Civ(city.getPreviousCiv()))
	if iPreviousOwner >= 0:
		checkName(iPreviousOwner)

@handler("cityBuilt")	
def onCityBuilt(city):
	checkName(city.getOwner())
	
@handler("playerPeriodChange")
def onPeriodChange(iPlayer, iPeriod):
	iCiv = civ(iPlayer)
	
	if iPeriod == -1:
		revertNameChange(iPlayer)
		revertAdjectiveChange(iPlayer)
	
	checkName(iPlayer)
	

@handler("religionFounded")
def onReligionFounded(_, iPlayer):
	if turn() == scenarioStartTurn():
		return

	checkName(iPlayer)

@handler("BeginGameTurn")
def checkTurn(iGameTurn):
	if every(10):
		for iPlayer in players.major():
			checkName(iPlayer)
			checkLeader(iPlayer)

		
def checkName(iPlayer):
	if not player(iPlayer).isAlive(): return
	if is_minor(iPlayer): return
	if player(iPlayer).getNumCities() == 0: return
	setDesc(iPlayer, desc(iPlayer, title(iPlayer)))
	
def checkLeader(iPlayer):
	if not player(iPlayer).isAlive(): return
	if is_minor(iPlayer): return
	setLeader(iPlayer, leader(iPlayer))
	setLeaderName(iPlayer, leaderName(iPlayer))

### Setter methods for player object ###

def setDesc(iPlayer, sName):
	try:
		player(iPlayer).setCivDescription(sName)
	except:
		pass
	
def setShort(iPlayer, sShort):
	player(iPlayer).setCivShortDescription(sShort)
	
def setAdjective(iPlayer, sAdj):
	player(iPlayer).setCivAdjective(sAdj)
	
def setLeader(iPlayer, iLeader):
	if not iLeader: return
	if player(iPlayer).getLeader() == iLeader: return
	player(iPlayer).setLeader(iLeader)
	
def setLeaderName(iPlayer, sName):
	if not sName: return
	if infos.leader(player(iPlayer)).getText() != sName:
		player(iPlayer).setLeaderName(sName)

### Utility methods ###

def key(iPlayer, sSuffix):
	if sSuffix: sSuffix = "_%s" % sSuffix
	return "TXT_KEY_CIV_%s%s" % (str(short(iPlayer).replace(" ", "_").upper()), sSuffix)
	
def desc(iPlayer, sTextKey=str("%s1")):
	if team(iPlayer).isAVassal():
		return text(sTextKey, name(iPlayer), adjective(iPlayer), name(iPlayer, True), adjective(iPlayer, True))

	return text(sTextKey, name(iPlayer), adjective(iPlayer))

def capitalName(iPlayer):
	capital = player(iPlayer).getCapitalCity()
	if capital: 
		sCapitalName = cnm.getLanguageRename(cnm.iLangEnglish, capital.getName())
		if sCapitalName: return sCapitalName
		else: return capital.getName()
	
	return short(iPlayer)
	
def checkNameChange(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv in dNameChanges:
		setShort(iPlayer, text(dNameChanges[iCiv]))
	
def checkAdjectiveChange(iPlayer):
	iCiv = civ(iPlayer)
	if iCiv in dAdjectiveChanges:
		setAdjective(iPlayer, text(dAdjectiveChanges[iCiv]))
		
def revertNameChange(iPlayer):
	iCiv = civ(iPlayer)
	if iCiv in dNameChanges:
		setShort(iPlayer, infos.civ(iCiv).getShortDescription(0))

def revertAdjectiveChange(iPlayer):
	iCiv = civ(iPlayer)
	if iCiv in dAdjectiveChanges:
		setAdjective(iPlayer, infos.civ(iCiv).getAdjective(0))
	
def getColumn(iPlayer):
	lTechs = [infos.tech(iTech).getGridX() for iTech in range(iNumTechs) if team(iPlayer).isHasTech(iTech)]
	if not lTechs: return 0
	return max(lTechs)
	
### Utility methods for civilization status ###
	
def isCapitulated(iPlayer):
	return team(iPlayer).isAVassal() and team(iPlayer).isCapitulated()
	
def isEmpire(iPlayer):
	if team(iPlayer).isAVassal(): return False

	return player(iPlayer).getNumCities() >= getEmpireThreshold(iPlayer)
	
def getEmpireThreshold(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv in dEmpireThreshold: 
		return dEmpireThreshold[iCiv]
		
	return 5
	
def isAtWar(iPlayer):
	for iTarget in players.major():
		if team(iPlayer).isAtWar(iTarget):
			return True
	return False
	
def capitalCoords(iPlayer):
	capital = player(iPlayer).getCapitalCity()
	if capital: return location(capital)
	
	return (-1, -1)
	
def controlsHolyCity(iPlayer, iReligion):
	holyCity = game.getHolyCity(iReligion)
	if holyCity and holyCity.getOwner() == iPlayer: return True
	
	return False
	
def controlsCity(iPlayer, (x, y)):
	plot = plot_(x, y)
	return plot.isCity() and plot.getPlotCity().getOwner() == iPlayer
	
### Naming methods ###

def name(iPlayer, bIgnoreVassal = False):
	iCiv = civ(iPlayer)

	if isCapitulated(iPlayer) and not bIgnoreVassal:
		sVassalName = vassalName(iPlayer, master(iPlayer))
		if sVassalName: return sVassalName
		
	if isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer):
		sRepublicName = republicName(iPlayer)
		if sRepublicName: return sRepublicName
		
	sSpecificName = specificName(iPlayer)
	if sSpecificName: return sSpecificName
	
	sDefaultInsertName = dDefaultInsertNames.get(iCiv)
	if sDefaultInsertName: return sDefaultInsertName
	
	return short(iPlayer)
	
def vassalName(iPlayer, iMaster):
	iMasterCiv = civ(iMaster)
	iCiv = civ(iPlayer)
		
	if iCiv == iNetherlands:
		return short(iPlayer)

	sSpecificName = dForeignNames[iMasterCiv].get(iCiv)
	if sSpecificName:
		return sSpecificName
	
	return None
	
def republicName(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv == iEngland: return None
	
	if iCiv == iInca and data.civs[iPlayer].iResurrections > 0: return None
	
	if iCiv == iNetherlands and isCommunist(iPlayer): return "TXT_KEY_CIV_NETHERLANDS_ARTICLE"


	return short(iPlayer)
	
def peoplesName(iPlayer):
	return desc(iPlayer, key(iPlayer, "PEOPLES"))
	
def specificName(iPlayer):
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	civic = civics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return short(iPlayer)
	
	iReligion = pPlayer.getStateReligion()
	capital = player(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = (civic.iReligion == iTheocracy)
	bResurrected = data.civs[iPlayer].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.civs[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = game.getCurrentEra()
	bWar = isAtWar(iPlayer)
			
	if iCiv == iSpain:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_SPAIN_AL_ANDALUS"
			
		if isCurrentCapital(iPlayer, "Barcelona", "Valencia"):
			return "TXT_KEY_CIV_SPAIN_ARAGON"
			
		if not bSpain:
			return "TXT_KEY_CIV_SPAIN_CASTILE"
			
	elif iCiv == iEngland:
		if getColumn(iPlayer) >= 11 and cities.rectangle(tBritain).owner(iPlayer) >= 3:
			return "TXT_KEY_CIV_ENGLAND_GREAT_BRITAIN"
			
	elif iCiv == iInca:
		if bResurrected:
			if isCurrentCapital(iPlayer, "La Paz"):
				return "TXT_KEY_CIV_INCA_BOLIVIA"
				
		else:
			if not bEmpire:
				return capitalName(iPlayer)
			
	elif iCiv == iNetherlands:
		if bCityStates:
			return short(iPlayer)
			
		if isCurrentCapital(iPlayer, "Brussels", "Antwerpen"):
			return "TXT_KEY_CIV_NETHERLANDS_BELGIUM"
			
def adjective(iPlayer, bIgnoreVassal = False):
	iCiv = civ(iPlayer)

	if isCapitulated(iPlayer):
		iMaster = master(iPlayer)
	
		sForeignAdjective = dForeignAdjectives[civ(iMaster)].get(iPlayer)
		if sForeignAdjective: return sForeignAdjective
		
		if not bIgnoreVassal: return adjective(iMaster)
		
	if isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer):
		sRepublicAdjective = republicAdjective(iPlayer)
		if sRepublicAdjective: return sRepublicAdjective
		
	sSpecificAdjective = specificAdjective(iPlayer)
	if sSpecificAdjective: return sSpecificAdjective
	
	sDefaultInsertAdjective = dDefaultInsertAdjectives.get(iCiv)
	if sDefaultInsertAdjective: return sDefaultInsertAdjective
	
	return player(iPlayer).getCivilizationAdjective(0)
	
def republicAdjective(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv in [iEngland]: return None
	
	if iCiv == iInca and data.civs[iPlayer].iResurrections > 0: return None
	
	return player(iPlayer).getCivilizationAdjective(0)
	
def specificAdjective(iPlayer):
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iCiv = civ(iPlayer)
	
	civic = civics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return player(iPlayer).getCivilizationAdjective(0)
	
	iReligion = pPlayer.getStateReligion()
	capital = player(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = (civic.iReligion == iTheocracy)
	bResurrected = data.civs[iPlayer].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.civs[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = game.getCurrentEra()
	bWar = isAtWar(iPlayer)
	
	bMonarchy = not isCommunist(iPlayer) and not isFascist(iPlayer) and not isRepublic(iPlayer)

	if iCiv == iSpain:
		bSpain = not player(iMoors).isAlive() or not player(iMoors).getCapitalCity() in plots.rectangle(tIberia)
	
		if bSpain:
			if not player(iPortugal).isAlive() or master(iPortugal) == iPlayer or not player(iPortugal).getCapitalCity() in plots.rectangle(tIberia):
				return "TXT_KEY_CIV_SPAIN_IBERIAN"
			
		if isCurrentCapital(iPlayer, "Barcelona", "Valencia"):
			return "TXT_KEY_CIV_SPAIN_ARAGONESE"
			
		if not bSpain:
			return "TXT_KEY_CIV_SPAIN_CASTILIAN"
			
	elif iCiv == iFrance:
		if iEra == iColonial:
			return "TXT_KEY_CIV_FRANCE_FRANKISH"
	
	elif iCiv == iEngland:
		if getColumn(iPlayer) >= 11 and cities.rectangle(tBritain).owner(iPlayer) >= 3:
			return "TXT_KEY_CIV_ENGLAND_BRITISH"
			
	elif iCiv == iInca:
		if bResurrected:
			if isCurrentCapital(iPlayer, "La Paz"):
				return "TXT_KEY_CIV_INCA_BOLIVIAN"
				
	elif iCiv == iNetherlands:
		if isCurrentCapital(iPlayer, "Brussels", "Antwerpen"):
			return "TXT_KEY_CIV_NETHERLANDS_BELGIAN"
			
	
### Title methods ###

def title(iPlayer):
	if isCapitulated(iPlayer):
		sVassalTitle = vassalTitle(iPlayer, master(iPlayer))
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
	iMasterCiv = civ(iMaster)
	iCiv = civ(iPlayer)

	if isCommunist(iMaster):
		sCommunistTitle = dCommunistVassalTitles[iMasterCiv].get(iCiv)
		if sCommunistTitle: return sCommunistTitle
		
		sCommunistTitle = dCommunistVassalTitlesGeneric.get(iMasterCiv)
		if sCommunistTitle: return sCommunistTitle
		
	if isFascist(iMaster):
		sFascistTitle = dFascistVassalTitles[iMasterCiv].get(iCiv)
		if sFascistTitle: return sFascistTitle
		
		sFascistTitle = dFascistVassalTitlesGeneric.get(iMasterCiv)
		if sFascistTitle: return sFascistTitle

	sSpecificTitle = dSpecificVassalTitles[iMasterCiv].get(iCiv)
	if sSpecificTitle: return sSpecificTitle

	sMasterTitle = dMasterTitles.get(iMasterCiv)
	if sMasterTitle: return sMasterTitle
		
	if iCiv in lColonies:
		return "TXT_KEY_COLONY_OF"
	
	return "TXT_KEY_PROTECTORATE_OF"
	
def communistTitle(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv in lSocialistRepublicOf: return "TXT_KEY_SOCIALIST_REPUBLIC_OF"
	if iCiv in lSocialistRepublicAdj: return "TXT_KEY_SOCIALIST_REPUBLIC_ADJECTIVE"
	if iCiv in lPeoplesRepublicOf: return "TXT_KEY_PEOPLES_REPUBLIC_OF"
	if iCiv in lPeoplesRepublicAdj: return "TXT_KEY_PEOPLES_REPUBLIC_ADJECTIVE"

	return key(iPlayer, "COMMUNIST")
	
def fascistTitle(iPlayer):
	return key(iPlayer, "FASCIST")
	
def republicTitle(iPlayer):
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)

	if iCiv == iEngland:
		iEra = pPlayer.getCurrentEra()
		if isEmpire(iPlayer) and iEra == iIndustrial:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra >= iAtomic:
			return "TXT_KEY_CIV_ENGLAND_UNITED_REPUBLIC"
	
	if iCiv == iAmerica:
		if civics(iPlayer).iSociety in [iManorialism, iSlavery]:
			return key(iPlayer, "CSA")
			
	if iCiv == iColombia:
		if isControlled(iPlayer, plots.region(rPeru)) and isControlled(iPlayer, plots.rectangle(tColombia)):
			return "TXT_KEY_CIV_COLOMBIA_FEDERATION_ANDES"
			
	if pPlayer.getStateReligion() == iIslam:
		if iCiv in lIslamicRepublicOf: return "TXT_KEY_ISLAMIC_REPUBLIC_OF"
		
	if iCiv in lRepublicOf: return "TXT_KEY_REPUBLIC_OF"
	if iCiv in lRepublicAdj: return "TXT_KEY_REPUBLIC_ADJECTIVE"
	
	return key(iPlayer, "REPUBLIC")

def defaultTitle(iPlayer):
	return desc(iPlayer, key(iPlayer, "DEFAULT"))
	
def specificTitle(iPlayer, lPreviousOwners=[]):
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iCiv = civ(iPlayer)
	
	civic = civics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return defaultTitle(iPlayer)
	
	iReligion = pPlayer.getStateReligion()
	capital = player(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = (civic.iReligion == iTheocracy)
	bResurrected = data.civs[iPlayer].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.civs[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = game.getCurrentEra()
	bWar = isAtWar(iPlayer)

	if iCiv == iColombia:
		if bEmpire:
			if isControlled(iPlayer, plots.region(rPeru)) and isControlled(iPlayer, plots.rectangle(tColombia)):
				return "TXT_KEY_CIV_COLOMBIA_EMPIRE_ANDES"
		
			return "TXT_KEY_CIV_COLOMBIA_EMPIRE"
			
	elif iCiv == iSpain:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
			
		if bEmpire and iEra > iColonial:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra == iColonial and isCurrentCapital(iPlayer, "Barcelona", "Valencia"):
			return "TXT_KEY_CIV_SPAIN_CROWN_OF"
			
	elif iCiv == iFrance:
		if not capital in cities.normal(iFrance):
			return "TXT_KEY_CIV_FRANCE_EXILE"
			
		if iEra >= iIndustrial and bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if civic.iLegitimacy == iRevolutionism:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iEngland:
		if capital not in cities.core(iEngland):
			return "TXT_KEY_CIV_ENGLAND_EXILE"
			
		if iEra == iColonial and player(iFrance).isAlive() and team(iFrance).isAVassal() and civ(master(iFrance)) == iEngland:
			return "TXT_KEY_CIV_ENGLAND_ANGEVIN_EMPIRE"
			
		if getColumn(iPlayer) >= 11:
			if bEmpire:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
		
			if cities.rectangle(tBritain).owner(iPlayer) >= 3:
				return "TXT_KEY_CIV_ENGLAND_UNITED_KINGDOM_OF"
			
	elif iCiv == iNetherlands:
		if bCityStates:
			return "TXT_KEY_CIV_NETHERLANDS_REPUBLIC"
		
		if capital not in cities.core(iNetherlands):
			return "TXT_KEY_CIV_NETHERLANDS_EXILE"
			
		if bEmpire:
			if iEra >= iIndustrial:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
			return "TXT_KEY_CIV_NETHERLANDS_UNITED_KINGDOM_OF"
			
	elif iCiv == iPortugal:
		if capital in cities.core(iBrazil) and not player(iBrazil).isAlive():
			return "TXT_KEY_CIV_PORTUGAL_BRAZIL"
			
		if not capital in plots.rectangle(tIberia):
			return "TXT_KEY_CIV_PORTUGAL_EXILE"
			
		if bEmpire and iEra >= iRevolutionary:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iInca:
		if not bResurrected:
			if bEmpire:
				return "TXT_KEY_CIV_INCA_FOUR_REGIONS"
				
	elif iCiv == iAztecs:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_CIV_AZTECS_ALTEPETL"
				
	elif iCiv == iAmerica:
		if civic.iSociety in [iSlavery, iManorialism]:
			if isControlled(iPlayer, plots.region(rMesoamerica)) and isControlled(iPlayer, plots.region(rCaribbean)):
				return "TXT_KEY_CIV_AMERICA_GOLDEN_CIRCLE"
		
			return "TXT_KEY_CIV_AMERICA_CSA"
			
	elif iCiv == iArgentina:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if not at(capital, plots.capital(iCiv)):
			return "TXT_KEY_CIV_ARGENTINA_CONFEDERATION"
	
	elif iCiv == iMexico:
		if bEmpire or iDespotism in civic:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iBrazil:
		if bEmpire:
			return "TXT_KEY_EMPIRE_OF"
			
	return None
			
### Leader methods ###

def startingLeader(identifier):
	if not isinstance(identifier, Civ):
		identifier = civ(identifier)
		
	return dStartingLeaders[scenario()].get(identifier, dStartingLeaders[i250AD][identifier])
	
def leader(iPlayer):
	iCiv = civ(iPlayer)

	if is_minor(iPlayer): return None
	
	if not player(iPlayer).isAlive(): return None
	
	if player(iPlayer).isHuman(): return None
	
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iReligion = pPlayer.getStateReligion()
	capital = player(iPlayer).getCapitalCity()
	tCapitalCoords = (capital.getX(), capital.getY())
	civic = civics(iPlayer)
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = (civic.iReligion == iTheocracy)
	bResurrected = data.civs[iPlayer].iResurrections > 0
	bMonarchy = not (isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer))
	iAnarchyTurns = data.civs[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = game.getCurrentEra()
	
	if iCiv == iSpain:
		if isFascist(iPlayer): return iFranco
		
		if any(data.dFirstContactConquerors.values()): return iPhilip
		
	elif iCiv == iFrance:
		if iEra >= iAtomic: return iDeGaulle
		
		if iEra >= iIndustrial: return iNapoleon
		
		if iEra >= iRevolutionary: return iLouis
		
	elif iCiv == iEngland:
		if iEra >= iAtomic: return iChurchill
		
		if iEra >= iIndustrial: return iVictoria
		
		if scenario() == i1770AD: return iVictoria
		
		if iEra >= iRevolutionary: return iElizabeth
		
	elif iCiv == iNetherlands:
		if year() >= year(1650): return iWilliam
			
	elif iCiv == iPortugal:
		if iEra >= iIndustrial: return iMaria
		
		if tPlayer.isHasTech(iCartography): return iJoao
		
	elif iCiv == iInca:
		if iEra >= iIndustrial: return iCastilla
		
		if bResurrected and year() >= year(1600): return iCastilla
	
	elif iCiv == iMexico:
		if bMonarchy: return iSantaAnna
		
		if isFascist(iPlayer): return iSantaAnna
		
		if iEra >= iAtomic: return iCardenas
			
	elif iCiv == iAmerica:
		if iEra >= iAtomic: return iRoosevelt
		
		if year() >= year(1850): return iLincoln
		
	elif iCiv == iArgentina:
		if iEra >= iAtomic: return iPeron
	
	elif iCiv == iBrazil:
		if iEra >= iAtomic: return iVargas
		
	elif iCiv == iCanada:
		if iEra >= iAtomic: return iTrudeau
		
	return startingLeader(iPlayer)
		
	
def leaderName(iPlayer):
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)
	iLeader = pPlayer.getLeader()
	
	return None