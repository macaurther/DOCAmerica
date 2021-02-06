from Consts import *
from RFCUtils import utils
from sets import Set
from StoredData import data
import Victory as vic
from Religions import rel

### Class for easier tech specification ###

class Techs:

	def __init__(self, techs=[], column=0, era=-1, exceptions=[]):
		self.column = column
		self.era = era
		self.techs = techs
		self.exceptions = exceptions
		
	def list(self):
		lTechs = Set()
		lTechs.update([i for i in range(iNumTechs) if gc.getTechInfo(i).getGridX() <= self.column])
		lTechs.update([i for i in range(iNumTechs) if gc.getTechInfo(i).getEra() <= self.era])
		lTechs.update(self.techs)
		lTechs.difference_update(self.exceptions)
		
		return list(lTechs)

### Starting tech methods ###

def getScenarioTechs(iScenario, iPlayer):
	iCivilization = gc.getPlayer(iPlayer).getCivilizationType()
	for iScenarioType in reversed(range(iScenario+1)):
		if iCivilization in lStartingTechs[iScenarioType]:
			return lStartingTechs[iScenarioType][iCivilization].list()
		#else: #debug
			#return lStartingTechs[iScenarioType][iCivVirginia].list()	#Debug
			
def getStartingTechs(iPlayer):
	return getScenarioTechs(utils.getScenario(), iPlayer)
	
def initScenarioTechs(iScenario):
	for iPlayer in range(iNumTotalPlayers):
		if tBirth[iPlayer] > utils.getScenarioStartYear(): continue
	
		iCivilization = gc.getPlayer(iPlayer).getCivilizationType()
		if iCivilization in lStartingTechs[iScenario]:
			initTechs(iPlayer, lStartingTechs[iScenario][iCivilization].list())
			
def initPlayerTechs(iPlayer):
	initTechs(iPlayer, getStartingTechs(iPlayer))
	
def initTechs(iPlayer, lTechs):
	pPlayer = gc.getPlayer(iPlayer)

	for iTech in lTechs:
		initTech(iPlayer, iTech)
	
	iCurrentEra = pPlayer.getCurrentEra()
	pPlayer.setStartingEra(iCurrentEra)
	
def initTech(iPlayer, iTech):
	gc.getTeam(gc.getPlayer(iPlayer).getTeam()).setHasTech(iTech, True, iPlayer, False, False)
	vic.onTechAcquired(iPlayer, iTech)
	rel.onTechAcquired(iPlayer, iTech)

### Tech preference functions ###

def getDictValue(dDict, key):
	if key not in dDict: return 0
	
	return dDict[key]

def getTechPreferences(iPlayer):
	dPreferences = {}
	iCivilization = gc.getPlayer(iPlayer).getCivilizationType()
	
	if iCivilization not in dTechPreferences:
		return dPreferences
		
	for iTech, iValue in dTechPreferences[iCivilization].items():
		dPreferences[iTech] = iValue
		
	for iTech, iValue in dTechPreferences[iCivilization].items():
		for i in range(4):
			iOrPrereq = gc.getTechInfo(iTech).getPrereqOrTechs(i)
			iAndPrereq = gc.getTechInfo(iTech).getPrereqAndTechs(i)
			
			if iOrPrereq < 0 and iAndPrereq < 0: break
			
			updatePrereqPreference(dPreferences, iOrPrereq, iValue)
			updatePrereqPreference(dPreferences, iAndPrereq, iValue)
	
	return dPreferences
	
def updatePrereqPreference(dPreferences, iPrereqTech, iValue):
	if iPrereqTech < 0: return
	
	iPrereqValue = getDictValue(dPreferences, iPrereqTech)
	
	if iValue > 0 and iPrereqValue >= 0:
		iPrereqValue = min(max(iPrereqValue, iValue), iPrereqValue + iValue / 2)
		
	elif iValue < 0 and iPrereqValue <= 0:
		iPrereqValue = max(min(iPrereqValue, iValue), iPrereqValue + iValue / 2)
		
	dPreferences[iPrereqTech] = iPrereqValue
	
def initPlayerTechPreferences(iPlayer):
	initTechPreferences(iPlayer, getTechPreferences(iPlayer))
	
def initTechPreferences(iPlayer, dPreferences):
	for iTech, iValue in dPreferences.items():
		gc.getPlayer(iPlayer).setTechPreference(iTech, iValue)

### Wonder preference methods ###

def initBuildingPreferences(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iCiv = pPlayer.getCivilizationType()
	if iCiv in dBuildingPreferences:
		for iBuilding, iValue in dBuildingPreferences[iCiv].iteritems():
			pPlayer.setBuildingPreference(iBuilding, iValue)
			
	if iCiv in dDefaultWonderPreferences:
		iDefaultPreference = dDefaultWonderPreferences[iCiv]
		for iWonder in range(iFirstWonder, iNumBuildings):
			if iCiv not in dBuildingPreferences or iWonder not in dBuildingPreferences[iCiv]:
				pPlayer.setBuildingPreference(iWonder, iDefaultPreference)
	
### General functions ###
		
def initBirthYear(iPlayer):
	gc.getPlayer(iPlayer).setBirthYear(tBirth[iPlayer])

def init():
	for iPlayer in range(iNumPlayers):
		initBirthYear(iPlayer)
		initPlayerTechPreferences(iPlayer)
		initBuildingPreferences(iPlayer)

### Starting technologies ###
#MacAurther TODO: Balance this
lStartingTechs = [
{
iCivNative : 		Techs([iTanning, iMythology]),
iCivSpain :			Techs(column=3),
iCivFrance :		Techs(column=3),
iCivEngland :		Techs(column=3),
iCivVirginia :		Techs(column=3),
iCivMassachusetts :	Techs(column=3),
iCivNewHampshire :	Techs(column=3),
iCivMaryland :		Techs([iCharter], column=3),
iCivConnecticut :	Techs([iCharter], column=3),
iCivRhodeIsland :	Techs([iCharter], column=3),
iCivNorthCarolina :	Techs([iCharter, iFinance], column=3),
iCivSouthCarolina :	Techs([iCharter, iFinance], column=3),
iCivNewJersey :		Techs([iCharter, iFinance], column=3),
iCivNewYork :		Techs([iCharter, iFinance], column=3),
iCivPennsylvania :	Techs([iCharter, iFinance, iCartography, iGunpowder], column=3),
iCivDelaware :		Techs([iCharter, iFinance, iCartography, iGunpowder], column=3),
iCivGeorgia :		Techs([iFortification, iLogistics, iUrbanPlanning], column=4),
iCivAmerica :		Techs(column=5),
iCivCanada :		Techs(column=5),
iCivIndependent :	Techs(column=3),
iCivIndependent2 :	Techs(column=3),
},
{
iCivIndependent:Techs(column=5),
iCivIndependent2:Techs(column=5),
},
{
iCivIndependent:Techs(column=10),
iCivIndependent2:Techs(column=10),
iCivSpain :		Techs(column=11),
iCivFrance :	Techs(column=11, exceptions=[iUrbanPlanning]),
iCivEngland :	Techs(column=11, exceptions=[iUrbanPlanning, iEconomics]),
}]

### Tech Preferences ###
#MacAurther TODO:
dTechPreferences = {
	iCivSpain : {
		iCartography: 100,
		iExploration: 100,
		iFirearms: 100,
	},
	iCivFrance : {
		iReplaceableParts: 30,
		iFirearms: 20,
		iExploration: 20,
	},
	iCivEngland : {
		iExploration: 40,
		iGeography: 40,
		iFirearms: 40,
	},
	iCivVirginia : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iCivMassachusetts : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iCivNewHampshire : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iCivMaryland : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iCivConnecticut : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iCivRhodeIsland : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iCivNorthCarolina : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iCivSouthCarolina : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iCivNewJersey : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iCivNewYork : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iCivPennsylvania : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iCivDelaware : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iCivGeorgia : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iCivAmerica : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
}

### Building Preferences ###

dDefaultWonderPreferences = {
	iCivFrance: -12,
	iCivAmerica: -12,
}

dBuildingPreferences = {
	iCivSpain : {
	},
	iCivFrance : {
		iPalaceOfNations: 20,
		iLargeHadronCollider: 20,
	},
	iCivEngland : {
		iTradingCompanyBuilding: 50,
		iNationalGallery: 20,
	},
	iCivVirginia : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
	},
	iCivMassachusetts : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
	},
	iCivNewHampshire : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
	},
	iCivMaryland : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
	},
	iCivConnecticut : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
	},
	iCivRhodeIsland : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
	},
	iCivNorthCarolina : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
	},
	iCivSouthCarolina : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
	},
	iCivNewJersey : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
	},
	iCivNewYork : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
	},
	iCivPennsylvania : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
	},
	iCivDelaware : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
	},
	iCivGeorgia : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
	},
	iCivAmerica : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
		iEmpireStateBuilding: 30,
		iBrooklynBridge: 30,
		iGoldenGateBridge: 30,
		iWorldTradeCenter: 30,
		iHubbleSpaceTelescope: 20,
		iCrystalCathedral: 20,
		iMenloPark: 20,
		iUnitedNations: 20,
		iGraceland: 20,
	},
	iCivCanada : {
		iCNTower: 30,
	}
}