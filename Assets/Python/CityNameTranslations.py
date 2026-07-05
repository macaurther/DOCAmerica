# coding: utf-8

from Consts import iAncientEra, iClassicalEra, iExplorationEra, iColonialEra, iRevolutionaryEra, iIndustrialEra, iModernEra
from Consts import iHinduism, iBuddhism, iJudaism, iOrthodoxy, iCatholicism, iProtestantism, iIslam
from Core import player, is_minor, cities, listify, none, game, city_
from StoredData import data
from Civics import isCommunist, isFascist, isRepublic, isAutocratic


### CONSTANTS ###

iNumLanguages = 17
lLanguages = (
	iAmerican, iArgentinian, iBrazilian, iDutch, iEnglish, iFrench, iLocal, iMayan, iMexican, iNahuatl, 
	iNative, iNordic, iPortuguese, iQuechua, iRussian, iSpanish, iSwedish, 
) = range(iNumLanguages)


### CLASSES ###

class Translation(object):
	
	def __init__(self, 
			name, 
			bRenaming=False, 
			bRelocation=False, 
			iBefore=None, 
			iAfter=None, 
			iReligion=None,
			iPeriod=None,
			iGreatGenerals=None,
			bFound=False, 
			bSmall=False, 
			bCommunist=False, 
			bOriginal=False, 
			bConquest=False, 
			bReconquest=False, 
			bAutocratic=False, 
			bCapital=False,
			bResurrected=False,
			bRepublican=False,
			bFascist=False,
		):
		self.name = name
		
		self.bRenaming = bRenaming
		self.bRelocation = bRelocation
		
		self.iBefore = iBefore
		self.iAfter = iAfter
		self.iReligion = iReligion
		self.iPeriod = iPeriod
		self.iGreatGenerals = iGreatGenerals
		
		self.bFound = bFound
		self.bSmall = bSmall
		self.bCommunist = bCommunist
		self.bOriginal = bOriginal
		self.bConquest = bConquest
		self.bReconquest = bReconquest
		self.bAutocratic = bAutocratic
		self.bCapital = bCapital
		self.bResurrected = bResurrected
		self.bRepublican = bRepublican
		self.bFascist = bFascist
	
	def __repr__(self):
		return u"%s(%s)" % (self.__class__.__name__, self.printableName())
	
	def printableName(self):
		if not self.name:
			return ""
		
		if self.name is _:
			return "_"
		
		return self.name.encode("ascii", "xmlcharrefreplace")
	
	def isEraSpecific(self, bFound=False):
		if self.bFound and not bFound:
			return False
		
		properties = (
			self.iReligion is not None, 
			self.iPeriod is not None, 
			self.iGreatGenerals is not None, 
			self.bSmall,
			self.bCommunist,
			self.bOriginal,
			self.bReconquest,
			self.bAutocratic,
			self.bCapital,
			self.bResurrected,
			self.bRepublican,
			self.bFascist
		)
		return none(properties)
		
	def isApplicable(self, iCiv, tile, bFound=False, bChange=True, bRenaming=True):
		# MacAurther: Translation not applicable if is None
		if self.name is None:
			return False

		city = city_(tile)
		iCurrentEra = is_minor(iCiv) and game.getCurrentEra() or player(iCiv).getCurrentEra()
		
		if self.iBefore is not None:
			if iCurrentEra > self.iBefore:
				return False
		
		if self.iAfter is not None:
			if iCurrentEra < self.iAfter:
				return False
				
		if self.iReligion is not None:
			if not is_minor(iCiv):
				if player(iCiv).getStateReligion() != self.iReligion:
					return False
		
		if self.iPeriod is not None:
			if player(iCiv).getPeriod() != self.iPeriod:
				return False
		
		if self.iGreatGenerals is not None:
			if player(iCiv).getGreatGeneralsCreated() < self.iGreatGenerals:
				return False
			
		if self.bRenaming and not bRenaming:
			return False
		
		if self.bFound and not bFound:
			return False
		
		if self.bCommunist:
			if not isCommunist(iCiv):
				return False
		
		if self.bAutocratic:
			if not isAutocratic(iCiv):
				return False
		
		if self.bResurrected:
			if data.civs[iCiv].iResurrections == 0:
				return False
		
		if self.bRepublican:
			if not isRepublic(iCiv):
				return False
		
		if self.bFascist:
			if not isFascist(iCiv):
				return False
		
		# city specific conditions
		
		if self.iReligion is not None:
			if is_minor(iCiv):
				if city is None or not city.isHasReligion(self.iReligion):
					return False
		
		if self.bSmall and city is not None:
			if city.getPopulation() > player(iCiv).getCurrentEra() + 1:
				return False
		
		if self.bOriginal and city is not None:
			if city.getOriginalCiv() != city.getCivilizationType():
				return False
		
		if self.bConquest:
			if city is None or city.getGameTurnAcquired() == city.getGameTurnFounded():
				return False
		
		if self.bReconquest:
			if city is None or city.getGameTurnCivLost(iCiv) < 0:
				return False
		
		if self.bCapital:
			if city is None:
				if cities.owner(iCiv).count() > 0:
					return False
			else:
				if not city.isCapital():
					return False
			
		return True


class Translations(object):
	
	@classmethod
	def of(cls, base_name):
		return cls(base_name, name_translations.get(base_name, {}))
	
	def __init__(self, base_name, translations):
		self.base_name = base_name
		self.translations = translations
	
	def __getitem__(self, iLanguage):
		names = listify(self.translations.get(iLanguage, []))
		
		if not names:
			names = [name for names in self.translations.values() for name in listify(names) if self.isRelocatedToLanguage(name, iLanguage)]
		
		return tuple(self.createTranslation(name) for name in names)
	
	def __contains__(self, iLanguage):
		return iLanguage in self.translations
	
	def isRelocatedToLanguage(self, name, iLanguage):
		if not name:
			return False
		
		if not isinstance(name, Translation):
			return False
		
		if not name.bRelocation:
			return False
		
		return iLanguage in name_translations.get(name.name, {})
	
	def createTranslation(self, name):
		if name is _:
			return Translation(self.base_name)
		
		if isinstance(name, (str, unicode)):
			return Translation(name)
		
		if name.name is _:
			name.name = self.base_name
		
		return name
	
	def getLanguages(self):
		return set(self.translations.keys())
	
	def isSingle(self):
		return len(self.translations) <= 1
	
	def getSingle(self):
		if not self.translations:
			return -1, (Translation(self.base_name),)
		
		iLanguage = self.translations.keys()[0]
		return iLanguage, self[iLanguage]


def translate(name, **kwargs):
	return Translation(name, **kwargs)


def rename(name, **kwargs):
	return translate(name, bRenaming=True, **kwargs)


def relocate(name, **kwargs):
	return translate(name, bRelocation=True, **kwargs)


def found(name, **kwargs):
	return relocate(name, bFound=True, **kwargs)
	

_ = object()


### NAME TRANSLATIONS ###

name_translations = {

	### A ###
	"Albany": {
		iEnglish: _,
		iAmerican: _,
		iDutch: "Fort Oranje",
	},
	"Aniak": {
		iLocal: _,
		iNative: "Anyaraq",
		iAmerican: "Bethel",
	},
	"Apatzingan": {
		iLocal: _,
		iNative: _,
		iSpanish: "Puerto Vallarta",
	},
	"Atqasuk": {
		iLocal: _,
		iAmerican: "Barrow",
	},

	### B ###
	"Baltimore": {
		iEnglish: _,
		iAmerican: "Washington",
	},
	"Baton Rouge": {
		iFrench: _,
		iAmerican: _,
		iEnglish: "New Richmond",
		iSpanish: "San Carlos",
	},
	"Biloxi": {
		iEnglish: _,
		iAmerican: _,
		iFrench: "Fort Maurepas",
	},
	"Bogota": {
		iLocal: _,
		iNative: _,
		iSpanish: u"Bogotá",
	},
	"Brooklyn": {
		iEnglish: _,
		iAmerican: _,
		iDutch: "Breukelen",
	},

	### C ###
	"Cahal Pech": {
		iMayan: _,
		iSpanish: u"Belmopán",
		iEnglish: "Belmopan",
	},
	"Caral": {
		iLocal: _,
		iNative: _,
		iQuechua: "Pachacamac",
		iSpanish: "Lima",
	},
	"Castries": {
		iEnglish: _,
		iAmerican: _,
		iFrench: "Fort-Royal",
	},
	"Catarpe": {
		iQuechua: _,
		iNative: _,
		iSpanish: "San Pedro de Atacama",
	},
	"Chalchuapa": {
		iMayan: _,
		iNahuatl: _,
		iSpanish: "San Miguel",
	},
	"Chan Chan": {
		iQuechua: _,
		iNative: _,
		iSpanish: "Trujillo",
	},
	"Charleston": {
		iEnglish: _,
		iAmerican: _,
		iFrench: "Charlesfort",
		iSpanish: "Santa Elena",
	},
	"Charlotte Amalie": {
		iNordic: _,
		iAmerican: _,
		iEnglish: "Road Town",
		iFrench: "Sainte-Croix",
		iSpanish: "Santa Cruz",
	},
	"Chena Pukara": {
		iLocal: _,
		iNative: _,
		iFrench: "Santiago du Chili",
		iPortuguese: "Santiago do Chile",
		iRussian: "Santyago",
		iSpanish: "Santiago",
	},
	"Chichen Itza": {
		iMayan: _,
		iNative: _,
		iNahuatl: _,
		iSpanish: "Merida",
	},
	"Cholula": {
		iLocal: _,
		iNative: _,
		iSpanish: "Puebla",
	},
	"Coba": {
		iMayan: _,
		iNative: _,
		iNahuatl: _,
		iSpanish: u"Cancún",
	},
	"Copan": {
		iMayan: _,
		iNahuatl: _,
		iSpanish: "Coban",
	},
	"Cuello": {
		iMayan: _,
		iNative: _,
		iNahuatl: _,
		iSpanish: "Ciudad de Belice",
		iEnglish: "Belize City",
	},

	### D ###
	"Danibaan": {
		iLocal: _,
		iNative: _,
		iNahuatl: _,
		iMayan: _,
		iSpanish: "Oaxaca",
	},
	"Deer Lake": {
		iEnglish: _,
		iSwedish: found("Vinland"),
	},
	"Detroit": {
		iEnglish: _,
		iAmerican: _,
		iFrench: u"Détroit",
	},
	"Dover": {
		iEnglish: _,
		iSwedish: found("Zwaanendael"),
		iDutch: found("Zwaanendael"),
	},

	### E ###

	### F ###
	"Fort Christina": {
		iNordic: _,
		iDutch: "Fort Altena",
		iEnglish: "Wilmington",
		iAmerican: "Wilmington",
	},
	"Fortaleza": {
		iBrazilian: _,
		iPortuguese: _,
		iDutch: "Schoonenborch",
	},

	### G ###
	"Georgetown": {
		iEnglish: _,
		iAmerican: _,
		iDutch: "Stabroek",
	},

	### H ###
	"Hatun Canar": {
		iQuechua: _,
		iNative: _,
		iSpanish: "Ingapirca",
	},
	"Huari": {
		iQuechua: _,
		iNative: _,
		iSpanish: "Huaraz",
	},

	### I ###
	"Iximche": {
		iMayan: _,
		iNative: _,
		iNahuatl: _,
		iSpanish: "San Salvador",
	},
	"Izamal": {
		iMayan: _,
		iNative: _,
		iNahuatl: _,
		iSpanish: "Progreso",
	},
	"Izapa": {
		iMayan: _,
		iNative: _,
		iNahuatl: _,
		iSpanish: "Tapachula",
	},

	### J ###
	"Jamestown": {
		iEnglish: _,
		iAmerican: "Richmond",
	},

	### K ###
	"Kitu": {
		iQuechua: _,
		iNative: _,
		iRussian: "Kito",
		iSpanish: "Quito",
	},

	### L ###
	"L'Anse aux Meadows": {
		iNordic: _,
		iEnglish: "St. Anthony",
	},

	### M ###
	"Marcahuamachuco": {
		iQuechua: _,
		iNative: _,
		iSpanish: "Cajamarca",
	},
	"Medellin": {
		iLocal: _,
		iNative: _,
		iSpanish: u"Medellín",
	},
	"Mobile": {
		iEnglish: _,
		iAmerican: _,
		iFrench: "La Mobile",
		iSpanish: "Movila",
	},

	### N ###
	"Naco": {
		iMayan: _,
		iNahuatl: _,
		iSpanish: "San Pedro Sula",
	},
	"Nanasqa": {
		iQuechua: _,
		iNative: _,
		iSpanish: "Nazca",
	},
	"Natal": {
		iBrazilian: _,
		iPortuguese: _,
		iDutch: "Fort Ceulen",
	},
	"New Amsterdam": {
		iDutch: "Nieuw-Amsterdam",
		iEnglish: "New York",
		iAmerican: "New York",
		iFrench: u"La Nouvelle-Angoulême",
		iRussian: "Nowy Jork",
	},
	"New Orleans": {
		iEnglish: _,
		iAmerican: _,
		iFrench: u"La Nouvelle-Orléans",
		iSpanish: "Nueva Orleans",
	},

	### O ###

	### P ###
	"Palenque": {
		iMayan: _,
		iNative: _,
		iLocal: _,
		iNahuatl: _,
		iSpanish: "Villahermosa",
	},
	"Paramaribo": {
		iDutch: _,
		iEnglish: "Torarica",
	},
	"Petatlan": {
		iMayan: _,
		iNative: _,
		iNahuatl: _,
		iSpanish: u"Petatlán",
	},
	"Philadelphia": {
		iEnglish: _,
		iAmerican: _,
		iDutch: "Fort Nassau",
		iFrench: "Philadelphie",
		iPortuguese: u"Filadélfia",
		iSpanish: "Filadelfia",
		iSwedish: u"Nya Göteborg",
	},
	"Porco": {
		iLocal: _,
		iSpanish: "Sucre",
	},
	"Port of Spain": {
		iEnglish: _,
		iAmerican: _,
		iSpanish: u"Puerto España",
	},

	### Q ###
	"Qosqo": {
		iQuechua: _,
		iNative: _,
		iSpanish: "Cusco",
	},
	"Quirigua": {
		iMayan: _,
		iNative: _,
		iNahuatl: _,
		iSpanish: "Puerto Barrios",
	},

	### R ###
	"Recife": {
		iBrazilian: _,
		iPortuguese: _,
		iDutch: "Mauritsstad",
	},

	### S ###
	"Sacramento": {
		iMexican: "Nueva Helvecia",
	},
	"Sagwon": {
		iLocal: _,
		iNative: _,
		iAmerican: "Prudhoe Bay",
	},
	"San Francisco": {
		iEnglish: _,
		iAmerican: _,
		iMexican: "Yerba Buena",
	},
	"San Lorenzo": {
		iLocal: _,
		iNative: _,
		iNahuatl: _,
		iMayan: _,
		iSpanish: "Coatzacoalcos",
	},
	"Santa Rosa": {
		iRussian: "Krepost Ross",
	},
	"Sao Luis": {
		iBrazilian: _,
		iPortuguese: _,
		iFrench: "Saint-Louis",
	},
	"Sitka": {
		iRussian: "Novo-Arkhangelsk",
		iAmerican: "Juneau",
	},
	"St. Augustine": {
		iSpanish: u"San Agustín",
		iFrench: "Saint-Augustin",
		iEnglish: "Jacksonville",
		iAmerican: "Jacksonville",
	},
	"St. John's": {
		iEnglish: _,
		iAmerican: _,
		iDutch: "Oranjestad",
		iFrench: "Basse-Terre",
	},
	"St. Louis": {
		iEnglish: _,
		iAmerican: _,
		iFrench: "Saint-Louis",
	},

	### T ###
	"Tacoma": {
		iEnglish: "Fort Nisqually",
		iAmerican: _,
	},
	"Tallahassee": {
		iEnglish: _,
		iAmerican: _,
		iSpanish: "San Luis",
	},
	"Tenochtitlan": {
		iDutch: "Mexico-Stad",
		iEnglish: "Mexico City",
		iFrench: "Mexico",
		iNahuatl: _,
		iNative: _,
		iLocal: _,
		iPortuguese: u"Cidade do México",
		iRussian: "Mekhiko",
		iSpanish: u"Ciudad de México",
	},
	"Teotihuacan": {
		iLocal: _,
		iNative: _,
		iMayan: "Puh",
		iNahuatl: _,
		iSpanish: "Texcoco"
	},
	"Tiahuanaco": {
		iLocal: _,
		iNative: _,
		iQuechua: "Chuqiyapu",
		iRussian: "La-Pas",
		iSpanish: "La Paz",
	},
	"Tiayo": {
		iLocal: _,
		iNative: _,
		iSpanish: "Tampico",
	},
	"Tres Zapotes": {
		iLocal: _,
		iNative: _,
		iNahuatl: _,
		iMayan: _,
		iSpanish: "Veracruz",
	},
	"Trois-Rivieres": {
		iFrench: _,
		iEnglish: "Three Rivers",
		iAmerican: "Three Rivers",
	},
	"Tucume": {
		iQuechua: _,
		iNative: _,
		iSpanish: "Piura",
	},
	"Tula": {
		iLocal: _,
		iNative: _,
		iNahuatl: _,
		iSpanish: "Leon",
	},
	"Tumipampa": {
		iQuechua: _,
		iNative: _,
		iSpanish: "Cuenca",
	},
	"Tututepec": {
		iLocal: _,
		iNative: _,
		iNahuatl: _,
		iMayan: _,
		iSpanish: "Puerto Escondido",
	},
	"Tzintzuntan": {
		iLocal: _,
		iNative: _,
		iNahuatl: _,
		iMayan: _,
		iRussian: "Gvadalakhara",
		iSpanish: "Guadalajara",
	},

	### U ###
	"Utalan": {
		iMayan: _,
		iNative: _,
		iNahuatl: _,
		iDutch: "Guatemala-Stad",
		iEnglish: "Guatemala City",
		iFrench: "Guatemala",
		iPortuguese: "Cidade da Guatemala",
		iRussian: "Gvatemala",
		iSpanish: "Guatemala",
	},
	"Uxmal": {
		iMayan: _,
		iNative: _,
		iNahuatl: _,
		iSpanish: "Campeche",
	},

	### V ###

	### W ###

	### X ###

	### Y ###

	### Z ###
	"Zempoala": {
		iLocal: _,
		iNative: _,
		iNahuatl: _,
		iMayan: _,
		iSpanish: "Xalapa",
	},

}
