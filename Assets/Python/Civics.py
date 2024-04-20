from Core import *

lCityStatesStart = [iMaya, iAztecs]


class Civics(object):

	@classmethod
	def of(cls, *items):
		civics = [-1 for _ in range(iNumCivicCategories)]
		for iCivic in items:
			civics[infos.civic(iCivic).getCivicOptionType()] = iCivic
		return cls(civics)
	
	@classmethod
	def player(cls, identifier):
		return cls(player(identifier).getCivics(iCategory) for iCategory in range(iNumCivicCategories))

	def __init__(self, civics):
		self.civics = tuple(civics)
	
	def __getitem__(self, item):
		return self.civics[item]
		
	def __contains__(self, items):
		if isinstance(items, int):
			items = (items,)
		
		category_civics = dict((iCategory, [item for item in items if infos.civic(item).getCivicOptionType() == iCategory]) for iCategory in set(infos.civic(item).getCivicOptionType() for item in items))
		return all(any(self.active(iCivic) for iCivic in civics) for iCategory, civics in category_civics.items())
		
	def active(self, iCivic):
		return self[infos.civic(iCivic).getCivicOptionType()] == iCivic
	
	@property
	def iExecutive(self):
		return self[0]
	
	@property
	def iAdministration(self):
		return self[1]
	
	@property
	def iLabor(self):
		return self[2]
	
	@property
	def iEconomy(self):
		return self[3]
	
	@property
	def iSociety(self):
		return self[4]
	
	@property
	def iExpansion(self):
		return self[5]


def civics(identifier):
	return Civics.player(identifier)
	
def notcivics(*civics):
	iCategory = infos.civic(civics[0]).getCivicOptionType()
	return tuple(iCivic for iCivic in infos.civics() if infos.civic(iCivic).getCivicOptionType() == iCategory and iCivic not in civics)

def isCommunist(iPlayer):
	civic = civics(iPlayer)
	
	if civic.iEconomy == iPublicWelfare3 and civic.iExecutive == iStateParty3:
		return True
		
	return False

def isAmerican(iPlayer):
	if gc.getPlayer(iPlayer).getCivilizationType() == iAmerica:
		return True
	return False
	
def isFascist(iPlayer):
	civic = civics(iPlayer)

	if civic.iExecutive == iDictatorship3:
		return True

	if civic.iAdministration == iPoliceState3 and civic.iExecutive not in [iMonarchy3, iStateParty3]:
		return True
	
	return False
	
def isRepublic(iPlayer):
	civic = civics(iPlayer)
	
	if civic.iExecutive == iDemocracy3:
		return True
	
	return False
	
def isCityStates(iPlayer):
	civic = civics(iPlayer)
	
	if civic.iAdministration == iCityStates1:
		return True
	
	return False