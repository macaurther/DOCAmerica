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
	def iGovernment(self):
		return self[0]
	
	@property
	def iLegitimacy(self):
		return self[1]
	
	@property
	def iSociety(self):
		return self[2]
	
	@property
	def iEconomy(self):
		return self[3]
	
	@property
	def iReligion(self):
		return self[4]
	
	@property
	def iTerritory(self):
		return self[5]


def civics(identifier):
	return Civics.player(identifier)
	
def notcivics(*civics):
	iCategory = infos.civic(civics[0]).getCivicOptionType()
	return tuple(iCivic for iCivic in infos.civics() if infos.civic(iCivic).getCivicOptionType() == iCategory and iCivic not in civics)

def isCommunist(iPlayer):
	civic = civics(iPlayer)
	
	if civic.iEconomy == iPublicWelfare and civic.iGovernment == iDespotism:
		return True
		
	return False
	
def isFascist(iPlayer):
	civic = civics(iPlayer)
	
	if civic.iSociety not in [iTolerance, iMulticulturalism] and civic.iExpansion in [iNationhood, iPuppeteering] and civic.Legal not iDemocracy:
		return True
	
	return False
	
def isRepublic(iPlayer):
	civic = civics(iPlayer)
	
	if civic.iLegal == iDemocracy:
		return True
	
	if civic.iGovernment in [iDespotism, iRepublic] and civic.iLegitimacy in [iFederalism, iSelfDetermination, iDemocracy]:
		return True
	
	return False
	
def isCityStates(iPlayer):
	civic = civics(iPlayer)
	
	if civic.iGovernment == iChiefdom and civ(iPlayer) in lCityStatesStart:
		return True
	
	return False