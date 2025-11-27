# coding: utf-8

from RFCUtils import *
import RFCUtils as RFCU
from Events import handler
from Core import *

import BugCore

AlertOpt = BugCore.game.MoreCiv4lerts


lTypes = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral, iGreatSpy]

tGreatPeople = None
tOffsets = None


@handler("greatPersonBorn")
def onGreatPersonBorn(unit, iPlayer, city):
	assignGreatPersonName(unit, iPlayer, city)

def assignGreatPersonName(unit, iPlayer, city, bAnnounceBirth = True):
	sName = getName(unit)
	if sName:
		game.addGreatPersonBornName(sName)
		
		# Leoreth: replace graphics for female GP names
		if sName[0] == "f":
			sName = sName[1:]
			unit = replace(unit, dFemaleGreatPeople[base_unit(unit)])
			unit = RFCU.replace(unit, dFemaleGreatPeople[base_unit(unit)])
		
		unit.setName(sName)
		
	# Leoreth: display notification
	if bAnnounceBirth:
		if not player(iPlayer).isMinorCiv() and not player(iPlayer).isBarbarian():
			text_key = 'TXT_KEY_MISC_GP_BORN'
			if city.isNone():
				text_key = 'TXT_KEY_MISC_GP_BORN_OUTSIDE'
				city = closestCity(unit)
		
			for iLoopPlayer in players.major().existing():
				if AlertOpt.isGreatPeopleOurs() and iPlayer != iLoopPlayer:
					continue
			
				if AlertOpt.isGreatPeopleKnown() and iPlayer != iLoopPlayer and not player(iLoopPlayer).canContact(iPlayer):
					continue
				
				if AlertOpt.isGreatPeopleNearby() and not game.isNeighbors(iPlayer, iLoopPlayer):
					continue
			
				if unit.plot().isRevealed(player(iLoopPlayer).getTeam(), False):
					message(iLoopPlayer, text_key, unit.getName(), '%s (%s)' % (city.getName(), name(city)), event=InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, button=unit.getButton(), color=infos.type('COLOR_UNIT_TEXT'), location=unit)
				else:
					message(iLoopPlayer, 'TXT_KEY_MISC_GP_BORN_SOMEWHERE', unit.getName(), event=InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, color=infos.type('COLOR_UNIT_TEXT'))

def create(iPlayer, iUnit, tile):
	x, y = location(tile)
	player(iPlayer).createGreatPeople(unique_unit(iPlayer, iUnit), True, True, x, y)

def getPrimary(iCiv):	
	return iCiv

def getNameCivs(iCiv):
	yield getPrimary(iCiv)
	
	for iSimilarCiv in civs.of(*(dNeighbours[iCiv] + dInfluences[iCiv])).sort(lambda c: any(iCiv in group and c in group for group in dCivGroups.values())):
		yield iSimilarCiv
	
def getType(iUnit):
	iUnitType = base_unit(iUnit)
	if iUnitType in lTypes: return lTypes.index(iUnitType)
	return -1

def getAvailableNames(iPlayer, iType):
	pPlayer = player(iPlayer)
	iEra = pPlayer.getCurrentEra()
	iCiv = civ(iPlayer)
	
	for iNameCiv in getNameCivs(iCiv):
		lNames = getEraNames(iNameCiv, iType, iEra)
		if lNames:
			return lNames
	
	return []

def getEraNames(iCiv, iType, iEra):
	lNames = tGreatPeople[iCiv][iType]
	
	if all(game.isGreatPersonBorn(sName) or sName in range(iNumEras) for sName in lNames):
		return []
	
	iOffset = tOffsets[iCiv][iType][iEra]
	iNextOffset = len(lNames)
	if iEra + 1 < iNumEras: iNextOffset = tOffsets[iCiv][iType][iEra+1]
	
	iSpread = max(iNextOffset - iOffset, min(iEra+2, 5))
	
	lBefore = [sName for sName in lNames[:iOffset] if not game.isGreatPersonBorn(sName)]
	lAfter = [sName for sName in lNames[iOffset:] if not game.isGreatPersonBorn(sName)]
	
	if len(lAfter) >= iSpread:
		return lAfter[:iSpread]
	
	iSpread -= len(lAfter)
	return lBefore[-iSpread:] + lAfter
	
def getName(unit):
	iType = getType(unit.getUnitType())
	if iType < 0: return None
	
	lAvailableNames = getAvailableNames(unit.getOwner(), iType)
	
	return random_entry(lAvailableNames)

# MacAurther TODO: Add more mod-specific great people :)
# WARNING: AI-GENERATED TABLES - I KNOW IT'S BAD AND HALLUCINATES PEOPLE WHO NEVER EXISTED BUT WHAT AM I GOING TO DO MY OWN RESEARCH I DON'T THINK SO
#  They're the ones with detail on where the names are from, details that are unverifiable at times...
dGreatPeople = {
	iMaya : {
		iGreatProphet : (
			"Junajpu", # mythological
			"Xb'alanke", # mythological
			"Jasaw Chan K'awiil", # 8th
			"Kukulkan", # 10th, named after the god
		),
		iGreatArtist : (
			"Uaxaclajuun Ub'aah K'awiil", # 8th
			"Chakalte'", # 8th
			"Jun Nat Omootz", # 8th
			"Asan Winik Tu'ub", # 8th
			"Chan Ch'ok Wayib Xok", # 8th
			"Waj Tan Chak", # 8th
			"K'ak' Tiliw Chan Chaak", # 8th
			iModernEra,
			"fMarisol Ceh Moo", # 20th
			u"Miguel Ángel Asturias", # 20th
		),
		iGreatScientist : (
			"Itzamna", # mythological
		),
		iGreatMerchant : (
			"Ek Chuaj", # mythological
			"Apoxpalon", # 16th
			"Tabscoob", # 16th
		),
		iGreatEngineer : (
			"Chan Imix K'awiil", # 7th
			"K'inich Kan Bahlam", # 7th
			"fK'ab'al Xook", # 8th
			"Ha' K'in Xook", # 8th
			"Itzam K'an Ahk", # 8th
			"K'inich Yat Ahk", # 8th
			"K'inich Ahkal Mo' Nahb", # 8th
			"Chan Chak K'ak'nal Ajaw", # 10th
		),
		iGreatStatesman : (
			"Yax Ehb Xook", # 1st
			"fYohl Ik'nal", # 6th
			"Yuknoom Ch'een", # 7th
			"Jasaw Chan K'awiil", # 8th
			"Apoch'waal", # 8th
			iModernEra,
			u"fRigoberta Menchú", # 20th
		),
		iGreatGeneral : (
			"Uneh Chan", # 6th
			"K'inich Yo'nal Ahk", # 7th
			"Wak Chanil Ajaw", # 8th
			"Hunac Ceel", # 12th
			iRevolutionaryEra,
			"Napuc Chi", # 16th
			"Tecun Uman", # 16th
		),
	},
	iInca : {
		iGreatProphet : (
			"Yahuar Huacac", # 14th
			"fAsarpay", # 16th
		),
		iGreatArtist : (
			"Viracocha", # legendary
			"Ninan Cuyochi", # 16th
			"fPalla Chimpu Ocllo", # 16th
			"Kronk", # Easter Egg
		),
		iGreatScientist : (
			"Sinchi Roca", # 12th
			"Mayta Qhapaq Inka", # 13th
			"Manqu Qhapaq", # 13th
			"Inka Roq'a", # 14th
			"Waskar Inka", # 16th
			"Titu Cusi", # 16th
			"fYzma", # Easter Egg
		),
		iGreatMerchant : (
			"Tupaq Inka Yupanki", # 15th
			"Felipillo", # 16th
			"Pacha", # Easter Egg
		),
		iGreatEngineer : (
			"Qhapaq Yunpanki Inka", # 14th
			"Sayri Tupaq Inka", # 16th
		),
		iGreatStatesman : (
			u"Mayta Cápac", # 14th
			"Kuzco", # Easter Egg
			iRevolutionaryEra,
			"Manco Inca Yupanqui", # 16th
			"fMama Huaco", # 16th
			u"Tápac Amaru", # 18th
		),
		iGreatGeneral : (
			"Pachakutiq Inka Yupanki", # 15th
			"Atawallpa", # 16th
			"Manqu Inka Yupanki", # 16th
			"Thupaq Amaru", # 16th
			"Chalcuchimaq", # 16th
			"Quisquis", # 16th
			iRevolutionaryEra,
			"fBartolina Sisa", # 18th
			u"Túpac Amaru", # 18th
			iIndustrialEra,
			"fJuana Azurduy de Padilla", # 19th
		),
	},
	iAztec : {
		iGreatProphet : (
			"Tenoch", # 14th
			"Tlacateotl", # 15th
			"fPapantzin", # 15th
			"Ixtlilxochitl", # 15th
			"fYacotzin", # 16th
		),
		iGreatArtist : (
			"Cuacuauhtzin", # 15th
			"Nezahualcoyotl", # 15th
			"Xayacamach", # 15th
			"fMacuilxochitzin", # 15th
		),
		iGreatScientist : (
			"Axayacatl", # 15th
			"Ixtlilxochitl", # 16th
			"Coanacochtzin", # 16th
		),
		iGreatMerchant : (
			"Cuauhtemoc", # 16th
			"Tlacotzin", # 16th
			"fTecuichpoch Ixcaxochitzin", # 16th
		),
		iGreatEngineer : (
			"Itzcatl", # 15th
			"Tlacaelel", # 15th
			"Moquihuix", # 15th
		),
		iGreatStatesman : (
			"Acamapichtli", # 14th
			"Quaquapitzahuac", # 15th
			"Tezozomoctli", # 15th
			"Nezahualcoyotl", # 15th
			"Nezahualpilli", # 15th
		),
		iGreatGeneral : (
			"Tezozomoc", # 14th
			"Ahuitzotl", # 15th
			"Itzcoatl", # 15th
			"Maxtla", # 15th
			"Huitzilhuitl", # 15th
			"Chimalpopoca", # 15th
		),
	},
	iSpain : {
		iGreatProphet : (
			u"Juan de Zumárraga",   # 16th – first bishop of Mexico, protector of indigenous peoples
			"Pedro de Gante",       # 16th – Franciscan missionary, educator of natives
			"Toribio de Benavente Motolinia", # 16th – early missionary chronicler
			u"fJuana Inés de la Cruz", # 17th – nun, theologian, and poet-scholar
			u"Alonso de Montúfar",    # 16th – Archbishop of Mexico, promoted Marian devotion (Our Lady of Guadalupe)
		),
		iGreatArtist : (
			u"Sebastián López de Arteaga",  # 17th – painter of early colonial Mexico
			u"Cristóbal de Villalpando",    # 17th – major baroque painter in New Spain
			"Miguel Cabrera",              # 18th – leading painter, known for casta paintings
			u"Manuel Tolsá",                # 18th–19th – sculptor and architect of the Mexico City cathedral façade
			"Juan Correa",                 # 17th – Afro-Mexican painter of religious works
		),
		iGreatScientist : (
			u"Carlos de Sigüenza y Góngora", # 17th – polymath, astronomer, cartographer
			u"José Antonio Alzate",          # 18th – naturalist, physicist, and journalist
			u"Francisco Hernández de Toledo",# 16th – royal physician, documented New World plants
			u"Andrés Manuel del Río",        # 18th – mineralogist, discovered vanadium in Mexico
			u"José Longinos Martínez",       # 18th – naturalist who catalogued flora and fauna of New Spain
		),
		iGreatMerchant : (
			u"Simón de Haro",               # 16th – early merchant in Veracruz trade
			"Juan de la Torre",            # 17th – Mexico City merchant tied to Manila Galleons
			u"Manuel Fernández de Jáuregui",# 18th – prominent colonial entrepreneur
			"Antonio de Ulloa",            # 18th – explorer and administrator involved in colonial commerce
			u"Tomás de la Barrera",         # 18th – mine owner and silver trader
		),
		iGreatEngineer : (
			u"Enrico Martínez",             # 17th – hydraulic engineer, drained Mexico Valley lakes
			u"Manuel Tolsá",                # 18th–19th – also as architect/engineer, built Palacio de Minería
			u"José de la Cruz",             # 18th – fortifications engineer in New Spain
			u"Agustín de Betancourt",       # 18th – Spanish engineer involved in colonial projects
			u"Lorenzo Rodríguez",           # 18th – architect of the Sagrario Metropolitano
		),
		iGreatStatesman : (
			"Antonio de Mendoza",          # 16th – first viceroy of New Spain
			"Luis de Velasco",             # 16th – viceroy, advocate for indigenous welfare
			u"José de Gálvez",              # 18th – reformer, Bourbon administrative overhaul
			"Juan de Palafox y Mendoza",   # 17th – bishop and viceroy, reformer of colonial church and state
			"Francisco Javier de Lizana y Beaumont", # 19th – viceroy during Napoleonic crisis
		),
		iGreatGeneral : (
			u"Hernán Cortés",               # 16th – conqueror and first governor of New Spain
			"Pedro de Alvarado",           # 16th – conquistador in Mexico and Guatemala
			"Gonzalo de Sandoval",         # 16th – key commander under Cortés
			u"Nuño de Guzmán",              # 16th – conqueror of western Mexico
			"Antonio de Leyva",            # 16th – Spanish general linked to colonial defense
			"Melchor Portocarrero",        # 17th – viceroy and military commander
		),
	},
	iPortugal : {
		iGreatProphet : (
			u"José de Anchieta",           # 16th – Jesuit missionary, co-founder of São Paulo and Rio de Janeiro
			u"Manuel da Nóbrega",          # 16th – Jesuit provincial, early defender of indigenous rights
			u"Antônio Vieira",             # 17th – Jesuit priest, orator, and royal adviser advocating for native and Afro-Brazilian peoples
			u"fMaria do Céu",              # 17th – Portuguese nun-writer whose works circulated in Brazil
			"Frei Vicente do Salvador",   # 17th – Franciscan historian and theologian of colonial Brazil
		),
		iGreatArtist : (
			"Aleijadinho",                # 18th – master sculptor and architect of Minas Gerais baroque churches
			u"Manuel da Costa Ataíde",     # 18th – painter of vivid baroque ceiling frescos
			u"fBárbara Heliodora",         # 18th – poet and playwright of Minas Gerais' literary circles
			u"Gregório de Matos",          # 17th – satirical poet of colonial Bahia
			"Manuel Botelho de Oliveira", # 17th – early Brazilian baroque poet and musician
		),
		iGreatScientist : (
			"Alexandre Rodrigues Ferreira", # 18th – naturalist, led Amazon and Maranhão expeditions
			u"José Bonifácio de Andrada e Silva", # 18th – mineralogist and natural scientist (pre-independence career)
			"Domingos Vandelli",             # 18th – Italian-born naturalist directing studies on Brazil's flora
			"Francisco de Melo Franco",      # 18th – physician and Enlightenment writer in colonial Brazil
			u"João Manso Pereira",            # 18th – inventor and early chemist in Bahia
		),
		iGreatMerchant : (
			u"Fernão Cardim",               # 16th – Jesuit chronicler involved in trade logistics for missions
			"Francisco Pinheiro",          # 17th – Lisbon-Bahia merchant financier
			u"João Fernandes Vieira",       # 17th – sugar planter and administrator (also soldier against Dutch)
			u"Antônio Rodrigues Bravo",     # 18th – Rio de Janeiro merchant in the transatlantic trade
			u"Sebastião Ferreira Santos",   # 18th – Minas Gerais mine operator and trader
		),
		iGreatEngineer : (
			u"Francisco França e Silva",    # 18th – engineer of colonial fortifications in Bahia
			u"José Fernandes Pinto Alpoim", # 18th – military engineer, architect of royal buildings in Rio
			"Manuel Pereira Ramos",        # 18th – designer of bridges and aqueducts in Minas Gerais
			"Vicente Gomes Ferreira",      # 18th – hydraulic engineer of Recife improvements
			u"Antônio Landim",              # 18th – architect-builder in Salvador
		),
		iGreatStatesman : (
			u"Tomé de Sousa",               # 16th – first governor-general of Brazil, founded Salvador
			u"Mem de Sá",                   # 16th – third governor-general, consolidated Portuguese control
			u"Marquês de Pombal",           # 18th – reformer whose policies transformed colonial administration
			"Luís de Vasconcelos e Sousa", # 18th – viceroy of Brazil, improved defenses and infrastructure
			"Conde de Resende",            # 18th – last viceroy of colonial Brazil before independence
		),
		iGreatGeneral : (
			u"Estácio de Sá",               # 16th – founded Rio de Janeiro, fought French invaders
			"Francisco Barreto",           # 16th – led military expeditions in Brazil and Angola
			u"Salvador Correia de Sá e Benevides", # 17th – expelled the Dutch from Luanda and supported Brazil's defense
			"Matias de Albuquerque",       # 17th – commander during Dutch invasions
			u"Francisco Xavier de Mendonça Furtado", # 18th – colonial governor and military administrator in the Amazon
		),
	},
	iEngland : {
		iGreatProphet : (
			"John Winthrop",              # 17th – Puritan leader, founder of Massachusetts Bay Colony
			"Cotton Mather",              # 17th–18th – influential Puritan minister and theologian
			"Roger Williams",             # 17th – theologian, advocate of religious freedom, founded Providence
			"Jonathan Edwards",           # 18th – Great Awakening preacher and philosopher
			"George Whitefield",          # 18th – English evangelist, central to the Great Awakening
		),
		iGreatArtist : (
			"John Smibert",               # 18th – early colonial portrait painter from Scotland
			"John Singleton Copley",      # 18th – leading American colonial painter, loyalist in England
			"William Byrd II",            # 18th – Virginia planter and writer, founder of Richmond
			"fAnne Bradstreet",           # 17th – Puritan poet, first published writer in British America
			"John Trumbull",              # 18th – painter of colonial and imperial subjects before independence
		),
		iGreatScientist : (
			"John Winthrop the Younger",  # 17th – governor and early scientist/alchemist
			"Benjamin Thompson",          # 18th – loyalist scientist (Count Rumford), pioneer in thermodynamics
			"John Bartram",               # 18th – botanist, royal botanist for the American colonies
			"Cadwallader Colden",         # 18th – scientist and colonial administrator, studied natural philosophy
			"Alexander Garden",           # 18th – naturalist and physician in South Carolina
		),
		iGreatMerchant : (
			"Peter Faneuil",              # 18th – wealthy Boston merchant and philanthropist
			"Robert Livingston the Elder",# 17th–18th – New York merchant and land magnate
			"Elihu Yale",                 # 17th–18th – Boston-born merchant and governor of Madras (namesake of Yale)
			"Humphrey Morice",            # 18th – London merchant involved in colonial trade
			"Henry Darnall",              # 17th – Maryland merchant and planter
		),
		iGreatEngineer : (
			"John Harrison",              # 18th – horologist whose inventions aided colonial navigation
			"Peter Harrison",             # 18th – architect of colonial public buildings, e.g., Newport and King's Chapel
			"Benjamin Henry Latrobe",     # 18th – British-born architect active in colonial America
			"Robert Livingston",          # 18th – engineer and land developer in New York colonies
			"William Strickland",         # 18th – architect of early colonial buildings
		),
		iGreatStatesman : (
			"William Penn",               # 17th – founder of Pennsylvania, proponent of self-governance and tolerance
			"John Rolfe",                 # 17th – Jamestown planter and tobacco pioneer
			"Edmund Andros",              # 17th – royal governor, Dominion of New England
			"Francis Nicholson",          # 17th–18th – colonial governor of multiple provinces
			"Cadwallader Colden",         # 18th – scientist and acting governor of New York
		),
		iGreatGeneral : (
			"John Smith",                 # 17th – soldier, explorer, leader of Jamestown Colony
			"Miles Standish",             # 17th – military officer for Plymouth Colony
			"Edward Braddock",            # 18th – British commander in North America during the French and Indian War
			"James Wolfe",                # 18th – captured Quebec in the Seven Years' War
			"William Shirley",            # 18th – governor and commander-in-chief during French and Indian War
		),
	},
	iFrance : {
		iGreatProphet : (
			"Paul Le Jeune",              # 17th – Jesuit missionary, early chronicler of New France
			u"Jean de Brébeuf",            # 17th – Jesuit missionary, martyr among the Huron
			"fMarie de l'Incarnation",    # 17th – Ursuline nun, founder of the first girls' school in New France
			u"François de Laval",          # 17th – first bishop of Quebec, organized the colonial church
			"Antoine Daniel",             # 17th – Jesuit missionary, early convert educator
		),
		iGreatArtist : (
			"Pierre Le Moyne d'Iberville",# 17th – explorer and writer, founder of Louisiana settlements
			u"Claude François",            # 18th – painter and map illustrator in New France
			u"fÉlisabeth Bégon",           # 18th – letter writer offering vivid accounts of colonial life
			"fMarie-Catherine d'Aulnoy",  # 17th – author of travel-inspired stories about the New World
			"fJeanne Le Ber",             # 17th – Montreal recluse and patron of religious art
		),
		iGreatScientist : (
			u"Pierre Gaultier de Varennes et de La Vérendrye", # 18th – explorer and cartographer of western Canada
			"Michel Sarrazin",            # 17th–18th – physician and naturalist, described Canadian flora and fauna
			"Charles-Marie de La Condamine", # 18th – explorer and geodesist, studied the Amazon and equator
			"Louis Nicolas",              # 17th – missionary-naturalist, compiled early Canadian fauna illustrations
			u"Joseph-François Lafitau",    # 18th – Jesuit ethnographer, described Iroquois society
		),
		iGreatMerchant : (
			"Samuel de Champlain",        # 17th – founder of Quebec, geographer, and fur trade organizer
			"Charles Aubert de La Chesnaye", # 17th – leading fur trader and entrepreneur in New France
			u"René Auguste Chouteau",      # 18th – co-founder of St. Louis, trader in Louisiana
			u"fBarbe Céléron",             # 18th – businesswoman in Montreal's fur trade networks
			"Jean Talon",                 # 17th – intendant of New France, promoted commerce and population growth
		),
		iGreatEngineer : (
			u"Sébastien Le Prestre de Vauban", # 17th – France's chief engineer, whose fortification models influenced Quebec
			"Gaspard-Joseph Chaussegros de Léry", # 18th – chief engineer of New France, designed Quebec fortifications
			"Louis de Buade de Frontenac",  # 17th – governor and builder of defensive works
			u"François de Chenneville",      # 18th – engineer for Montreal's early defenses
			"fMarguerite d'Youville",       # 18th – founder of Grey Nuns, improved colonial hospitals and social works
		),
		iGreatStatesman : (
			"Jean Talon",                  # 17th – first intendant, established industry and census
			"Louis de Buade de Frontenac", # 17th – governor and defender of New France
			"Pierre de Rigaud de Vaudreuil", # 18th – last governor of New France
			"Charles de la Boische de Beauharnois", # 18th – long-serving governor, supported exploration
			u"Roland-Michel Barrin de La Galissonière", # 18th – naval officer, acted as governor of New France
		),
		iGreatGeneral : (
			"Charles de Montmagny",        # 17th – first governor of New France, established fortifications
			"Louis-Joseph de Montcalm",    # 18th – commander at Quebec during Seven Years' War
			"Pierre Le Moyne d'Iberville", # 17th – naval officer, founder of Louisiana settlements
			"Jean-Baptiste Le Moyne de Bienville", # 18th – co-founder and governor of New Orleans
			"Daniel de Rémy de Courcelle",  # 17th – governor and military leader against Iroquois
		),
	},
	iNetherlands : {
		iGreatProphet : (
			"Johannes Megapolensis",      # 17th – Reformed minister in New Netherland, mediator with Native peoples
			"Franciscus Gomarus",         # 17th – theologian whose followers influenced colonial clergy
			"fMaria Sibylla Merian",      # 17th–18th – naturalist and illustrator who studied Suriname's insects
			"Willem Usselincx",           # 17th – founder of the Dutch West India Company, Protestant visionary for colonization
			"Abraham Calovius",           # 17th – theologian whose writings circulated in Dutch colonial missions
		),
		iGreatArtist : (
			"Albert Eckhout",             # 17th – painter in Dutch Brazil, depicted local peoples and fauna
			"Frans Post",                 # 17th – landscape painter of Dutch Brazil under Nassau-Siegen
			"fRachel Ruysch",             # 17th–18th – still-life painter, works sent to colonies and trade patrons
			"fMaria Schalcken",           # 17th – portraitist connected to merchant families with American ties
			"Dirck Valkenburg",           # 17th – painted Suriname plantations and slave life
		),
		iGreatScientist : (
			"Georg Marcgraf",             # 17th – astronomer and naturalist, surveyed Brazil under Nassau-Siegen
			"Willem Piso",                # 17th – physician, co-author of *Historia Naturalis Brasiliae*
			"Anton de Kom",               # 20th – Surinamese intellectual and ethnographer (non-revolutionary scholar)
			"Nikolaas Laurens Burman",    # 18th – botanist studying Caribbean flora
			"François Valentijn",         # 18th – chronicler and geographer of Dutch colonial regions
		),
		iGreatMerchant : (
			"Peter Stuyvesant",           # 17th – last director-general of New Netherland, expanded trade and defenses
			"Johannes de Laet",           # 17th – historian and director of Dutch West India Company
			"fElisabeth Heijns",          # 17th – merchant widow active in West India Company trade
			"Benjamin Cohen Henriques",   # 18th – Amsterdam merchant with Caribbean trade networks
			"Cornelis Lampsins",          # 17th – Zeeland shipowner, colonial trader, governor of Tobago
		),
		iGreatEngineer : (
			"Johan Maurits van Nassau-Siegen", # 17th – governor of Dutch Brazil, built Recife's fortifications
			"Hendrick van Reede tot Drakenstein", # 17th – colonial official and engineer-naturalist
			"Dirck Corneliszoon Rijk",     # 17th – naval architect for colonial fleets
			"Jacob Binckes",               # 17th – naval officer, rebuilt forts in Suriname and Tobago
			"fElisabeth Samson",           # 18th – wealthy free woman of color in Suriname, funded civic projects
		),
		iGreatStatesman : (
			"Willem Usselincx",            # 17th – founder and theorist of Dutch West India Company
			"Johan Maurits van Nassau-Siegen", # 17th – governor of Dutch Brazil, enlightened administrator
			"Laurens Reael",               # 17th – governor of Dutch possessions, advocated fair treatment of natives
			"Cornelis van Aerssen van Sommelsdijck", # 17th – governor of Suriname, reorganized colony
			"Isaac Lamoureux",             # 17th – merchant-politician in New Netherland's council
		),
		iGreatGeneral : (
			"Piet Pieterszoon Hein",       # 17th – naval commander, captured Spanish treasure fleet in Caribbean
			"Adriaen Banckert",            # 17th – admiral active in West Indies campaigns
			"Johan Maurits van Nassau-Siegen", # 17th – also served as military commander in Dutch Brazil
			"Michiel de Ruyter",           # 17th – admiral, fought in Caribbean and North American waters
			"Hendrick Lonck",              # 17th – captured Salvador, Brazil from the Portuguese
		),
	},
	iAmerica : {
		iGreatProphet : (
			"Joseph Smith", # 19th
			"fMary Baker Eddy", # 19th
			"fEllen G. White", # 19th
			"Charles Taze Russell", # 19th
			iModernEra,
			"Menachem Mendel Schneerson", # 20th
			"L. Ron Hubbard", # 20th
			"Billy Graham", # 20th
			"Malcolm Little", # 20th
		),
		iGreatArtist : (
			"Edgar Allan Poe", # 19th
			"Mark Twain", # 19th
			"fEmily Dickinson", # 19th
			"Herman Melville", # 19th
			"fMary Cassatt", # 19th
			iModernEra,
			"Howard Phillips Lovecraft", # 20th
			"Ernest Hemingway", # 20th
			"Charlie Chaplin", # 20th
			"Elvis Presley", # 20th
			"fHarper Lee", # 20th
			"Andy Warhol", # 20th
			"Miles Davis", # 20th
			"Jimi Hendrix", # 20th
		),
		iGreatScientist : (
			"Benjamin Franklin", # 18th
			"fNettie Stevens", # 19th
			iModernEra,
			"Arthur Compton", # 20th
			"Edwin Hubble", # 20th
			"John von Neumann", # 20th
			"Glenn Seaborg", # 20th
			"Robert Oppenheimer", # 20th
			"Richard Feynman", # 20th
			"fBarbara McClintock", # 20th
			"fGrace Hopper", # 20th
		),
		iGreatMerchant : (
			"Stephen Girard", # 18th
			"Nathaniel Bowditch", # 18th
			iIndustrialEra,
			"Cornelius Vanderbilt", # 19th
			"Cyrus W. Field", # 19th
			"Andrew Carnegie", # 19th
			"John D. Rockefeller", # 19th
			"Andrew Carnegie", # 19th
			"fHetty Green", # 19th
			"John Pierpont Morgan", # 19th
			iModernEra,
			"fHelena Rubinstein", # 20th
			"William Edward Boeing", # 20th
			"Walt Disney", # 20th
			"Ray Kroc", # 20th
			"Thomas Watson", # 20th
			"Sam Walton", # 20th
			"Bill Gates", # 20th
		),
		iGreatEngineer : (
			"Samuel Morse", # 19th
			"Charles Goodyear", # 19th
			"Thomas Edison", # 19th
			"Nikola Tesla", # 19th
			"Louis Sullivan", # 19th
			"Henry Ford", # 19th
			iModernEra,
			"Orville Wright", # 20th
			"Frank Lloyd Wright", # 20th
			"fLillian Moller Gilbreth", # 20th
			"Robert Moses", # 20th
			"Eero Saarinen", # 20th
			"fMargaret Hutchinson Rousseau", # 20th
			"fHedy Lamarr", # 20th
			"Frank Gehry", # 20th
		),
		iGreatStatesman : (
			"Thomas Paine", # 18th
			"Thomas Jefferson", # 18th
			"Benjamin Franklin", # 18th
			iIndustrialEra,
			"Andrew Jackson", # 19th
			"fSojourner Truth", # 19th
			"Frederick Douglass", # 19th
			"fVictoria Claflin Woodhull", # 19th
			"fSusan B. Anthony", # 19th
			"fJane Addams", # 19th
			iModernEra,
			"fEleanor Roosevelt", # 20th
			"George Kennan", # 20th
			"Martin Luther King", # 20th
			"Henry Kissinger", # 20th
		),
		iGreatGeneral : (
			"Winfield Scott", # 19th
			"Ulysses S. Grant", # 19th
			"Robert E. Lee", # 19th
			iModernEra,
			"John J. Pershing", # 20th
			"Dwight D. Eisenhower", # 20th
			"George Patton", # 20th
			"Douglas MacArthur", # 20th
			"Matthew Ridgway", # 20th
			"Norman Schwarzkopf", # 20th
		),
		iGreatSpy : (
			"Benjamin Tallmadge", # 18th
			"Allan Pinkerton", # 19th
			"fBelle Boyd", # 19th
			"fElizabeth Van Lew", # 19th
			iModernEra,
			"William J. Donovan", # 20th
			"J. Edgar Hoover", # 20th
			"James Jesus Angleton", # 20th
			"fVirginia Hall", # 20th
			"fElizabeth Friedman", # 20th
		),
	},
	iMexico : {
		iGreatProphet : (
			"Juan Diego", # 16th
			"Francisco Javier Clavijero", # 18th
			u"Cristóbal Magallanes Jara", # 19th
			iModernEra,
			u"Rafael Guízar Valencia", # 20th
			"Miguel Pro", # 20th
			"Samuel Ruiz", # 20th
			u"Javier Lozano Barragán", # 20th
		),
		iGreatArtist : (
			u"fÁngela Peralta", # 19th
			iModernEra,
			u"José Clemente Orozco", # 20th
			"Diego Rivera", # 20th
			"fFrida Kahlo", # 20th
			"Octavio Paz", # 20th
			"fRemedios Varo", # 20th
			u"fDolores del Río", # 20th
			"Pedro Infante", # 20th
			"Carlos Fuentes", # 20th
			u"Vicente Fernández", # 20th
		),
		iGreatScientist : (
			"Gabino Barreda", # 19th
			u"Lucas Alamán", # 19th
			iModernEra,
			"Manuel Sandoval Vallarta", # 20th
			"Ricardo Miledi", # 20th
			u"Mario José Molina", # 20th
			"Rodolfo Neri Vela", # 20th
		),
		iGreatMerchant : (
			u"Víctor Urquidi", # 20th
			u"Jerónimo Arango", # 20th
			"Carlos Slim", # 20th
			"Everardo Elizondo", # 20th
			u"Alberto Baillères", # 20th
			u"Emilio Azcárraga Jean", # 20th
		),
		iGreatEngineer : (
			u"José Villagrán García", # 20th
			u"Luis Barragán", # 20th
			"Juan O'Gorman", # 20th
			"Mario Pani", # 20th
			u"Pedro Ramírez Vázquez", # 20th
			"Bernardo Quintana Arrioja", # 20th
		),
		iGreatStatesman : (
			u"José María Pino Suárez", # 19th
			"Pascual Orozco", # 19th
			iModernEra,
			u"José Vasconcelos", # 20th
			"Octavio Paz", # 20th
			"fElvia Carrillo Puerto", # 20th
			"fRosario Castellanos", # 20th
			u"Alfonso García Robles", # 20th
			u"Gilberto Bosques Saldívar", # 20th
		),
		iGreatGeneral : (
			"Miguel Hidalgo", # 18th
			u"Agustín de Iturbide", # 19th
			u"fJosefa Ortiz de Domínguez", # 19th
			u"Porfirio Díaz", # 19th
			"Pancho Villa", # 19th
			"Emiliano Zapata Salazar", # 19th
		),
		iGreatSpy : (
			"fMargarita Ortega", # 19th
		),
	},
	iArgentina : {
		iGreatProphet : (
			"Gauchito Gil", # 19th
			iModernEra,
			"Enrique Angelelli", # 20th
			"Carlos Mugica", # 20th
			"Jorge Mario Bergoglio", # 20th
		),
		iGreatArtist : (
			u"José Hernández", # 19th
			"fLola Mora", # 19th
			iModernEra,
			"Carlos Gardel", # 20th
			"fGabriela Mistral", # 20th
			"Jorge Luis Borges", # 20th
			"Antonio Berni", # 20th
			"Daniel Barenboim", # 20th
			u"Juan José Campanella", # 20th
			"Gustavo Cerati", # 20th
		),
		iGreatScientist : (
			"Francisco Moreno", # 19th
			"Florentino Ameghino", # 19th
			iModernEra,
			"Luis Federico Leloir", # 20th
			u"László Bíró", # 20th
			u"René Favaloro", # 20th
		),
		iGreatMerchant : (
			"Juan Las Heras", # 19th
			"Otto Bemberg", # 19th
			"Ernesto Tornquist", # 19th
			iModernEra,
			u"José Ber Gelbard", # 20th
			"Roberto Alemann", # 20th
			"Jorge Wehbe", # 20th
			"Aldo Ferrer", # 20th
			"Antonio Cafiero", # 20th
		),
		iGreatEngineer : (
			"Luis Huergo", # 19th
			"Jorge Newbery", # 19th
			iModernEra,
			"Amancio Williams", # 20th
			"Livio Dante Porta", # 20th
			"Clorindo Testa", # 20th
			u"César Pelli", # 20th
		),
		iGreatStatesman : (
			"Juan Manuel de Rosas", # 19th
			"Domingo Faustino Sarmiento", # 19th
			"Estanislao Zeballos", # 19th
			iModernEra,
			"Carlos Saavedra Lamas", # 20th
			"Juan Atilio Bramuglia", # 20th
			u"fEva Perón", # 20th
			"Ernesto Guevara", # 20th
			u"fIsabel Martínez de Perón", # 20th
			"fEstela Barnes de Carlotto", # 20th
		),
		iGreatGeneral : (
			"Cornelio Saavedra", # 18th
			"Manuel Belgrano", # 18th
			u"Juan José Castelli", # 18th
			u"Martín Miguel de Güemes", # 18th
			u"José Gervasio Artigas", # 19th
			iModernEra, 
			u"Juan Carlos Onganía", # 20th
			"Jorge Rafael Videla", # 20th
			"Leopoldo Galtieri", # 20th
			"Jorge Anaya", # 20th
		),
		iGreatSpy : (
			"Emilio Eduardo Massera", # 20th
			"Guillermo Gaede", # 20th
		),
	},
	iColombia : {
		iGreatProphet : (
			"fLaura Montoya", # 20th
			u"Félix Restrepo Mejía", # 20th
			"Camilo Torres Restrepo", # 20th
			u"Alfonso López Trujillo", # 20th
			u"Julio Enrique Dávila", # 20th
			u"fMaría Luisa Piraquive", # 20th
			u"César Castellanos", # 20th
		),
		iGreatArtist : (
			"Jorge Isaacs", # 19th
			u"Andrés de Santa Maria", # 19th
			iModernEra,
			"Rodrigo Arenas", # 20th
			u"Álvaro Mutis", # 20th
			u"Gabriel García Márquez", # 20th
			"Fernando Botero", # 20th
			"Rafael Orozco", # 20th
			u"Rodrigo García", # 20th
			"fShakira", # 20th
		),
		iGreatScientist : (
			u"José Jéronimo Triana", # 19th
			"Julio Garavito Armero", # 19th
			iModernEra,
			u"Rodolfo Llinás", # 20th
			"Jorge Reynolds Pombo", # 20th
		),
		iGreatMerchant : (
			"James Martin Eder", # 19th
			iModernEra,
			"Julio Mario Santo Domingo", # 20th
			u"Carlos Ardila Lülle", # 20th
			"Luis Carlos Sarmiento Angulo", # 20th
			"Pablo Escobar", # 20th
		),
		iGreatEngineer : (
			u"Carlos Albán", # 19th
			iModernEra, 
			u"Carlos Raúl Villanueva", # 20th
			"Rogelio Salmona", # 20th
		),
		iGreatStatesman : (
			u"Tomás Cipriano de Mosquera", # 19th
			u"Rafael Núñez", # 19th
			iModernEra,
			u"Jorge Eliécer Gaitán", # 20th
			u"Nicolás Gómez Dávila", # 20th
			u"Mario Lanserna Pinzón", # 20th
		),
		iGreatGeneral : (
			"fAntonia Santos", # 19th
			u"Antonio Nariño", # 19th
			"Francisco de Paula Santander", # 19th
		),
		iGreatSpy : (
			"fPolicarpa Salavarrieta", # 19th
			u"fManuela Sáenz", # 19th
		),
	},
	iBrazil : {
		iGreatProphet : (
			u"António Conselheiro", # 19th
			iModernEra,
			u"Hélder Câmara", # 20th
			u"fIrmã Dulce Pontes", # 20th
			"Chico Xavier", # 20th
			"Edir Macedo", # 20th
		),
		iGreatArtist : (
			"Aleijadinho", # 18th
			u"António Carlos Gomes", # 19th
			"Machado de Assis", # 19th
			iModernEra,
			"fTarsila do Amaral", # 20th
			"fCarmen Miranda", # 20th
			"Tom Jobim", # 20th
			"Romero Britto", # 20th
		),
		iGreatScientist : (
			"Oswaldo Cruz", # 19th
			"Carlos Chagas", # 19th
			iModernEra,
			"Alberto Santos-Dumont", # 20th
			"Urbano Ernesto Stumpf", # 20th
			u"Aziz Ab'Sáber", # 20th
			"Marcelo Gleiser", # 20th
		),
		iGreatMerchant : (
			"Roberto Marinho", # 20th
			"Jorge Lemann", # 20th
			"Eike Batista", # 20th
		),
		iGreatEngineer : (
			u"André Rebouças", # 19th
			iModernEra,
			u"Cândido Rondon", # 20th
			"Oscar Niemeyer", # 20th
			"Norberto Odebrecht", # 20th
		),
		iGreatStatesman : (
			u"José Bonifácio de Andrada", # 18th
			iIndustrialEra,
			"Rodrigo Augusto da Silva", # 19th
			u"José Paranhos", # 19th
			u"fIsabel Bragança", # 19th
			"Miguel Reale", # 19th
			iModernEra,
			"Roberto Mangabeira Unger", # 20th
		),
		iGreatGeneral : (
			u"Luís Alves de Lima e Silva", # 19th
			"Joaquim Marques Lisboa", # 19th
			u"fMaria Quitéria", # 19th
			iModernEra,
			u"João Baptista Mascarenhas de Morais", # 20th
			"Eurico Gaspar Dutra", # 20th
			"Artur da Costa e Silva", # 20th
		),
	},
	iCanada : {
		iGreatProphet : (
			"Ignace Bourget", # 19th
			u"André Bessette", # 20th
			iModernEra,
			"Lionel Groulx", # 20th
			"George C. Pidgeon", # 20th
			u"fRúhíyyih Khánum", # 20th
			"Marshall McLuhan", # 20th
		),
		iGreatArtist : (
			"Cornelius Krieghoff", # 19th
			u"Calixa Lavallée", # 19th
			"Tom Thomson", # 19th
			u"Émile Nelligan", # 19th
			iModernEra,
			"fLucy Maud Montgomery", # 20th
			"Lawren Harris", # 20th
			"fEmily Carr", # 20th
			"Jean-Paul Riopelle", # 20th
			"Neil Young", # 20th
			"fGabrielle Roy", # 20th
			"fAlice Munro", # 20th
		),
		iGreatScientist : (
			"John William Dawson", # 19th
			"fMaude Abbott", # 19th
			iModernEra,
			"Frederick Banting", # 20th
			"Norman Bethune", # 20th
			"Wilder Penfield", # 20th
			"Pierre Dansereau", # 20th
			"fShirley Tilghman", # 20th
			"David Suzuki", # 20th
		),
		iGreatMerchant : (
			"William McMaster", # 19th
			"Timothy Eaton", # 19th
			"Alphonse Desjardins", # 19th
			iModernEra,
			"fElizabeth Arden", # 20th
			"Max Aitken", # 20th
			"Ted Rogers", # 20th
			u"Guy Laliberté", # 20th
		),
		iGreatEngineer : (
			"Sandford Fleming", # 19th
			"William Cornelius Van Horne", # 19th
			"Alexander Graham Bell", # 19th
			"Reginald Fessenden", # 19th
			iModernEra,
			"Ernest Cormier", # 20th
			"Joseph-Armand Bombardier", # 20th
			"fElsie MacGill", # 20th
		),
		iGreatStatesman : (
			u"George-Étienne Cartier", # 19th
			"Louis Riel", # 19th
			"Henri Bourassa", # 19th
			iModernEra,
			"Lester B. Pearson", # 20th
			"fEmily Murphy", # 20th
			"fNellie McClung", # 20th
			"Tommy Douglas", # 20th
			u"René Lévesque", # 20th
			"fLouise Arbour", # 20th
		),
		iGreatGeneral : (
			"Arthur Currie", # 20th
			"Andrew McNaughton", # 20th
			"Billy Bishop", # 20th
			u"Roméo Dallaire", # 20th
		),
		iGreatSpy : (
			"William Stephenson", # 20th
			"Guy D'Artois", # 20th
			"Igor Gouzenko", # 20th
		),
	},
}


def setup():
	global dGreatPeople
	
	global tGreatPeople
	tGreatPeople = tuple(determineGreatPeopleNames(dGreatPeople.get(iCiv, {})) for iCiv in range(iNumCivs))
	
	global tOffsets
	tOffsets = tuple(calculateOffsets(dGreatPeople.get(iCiv, {})) for iCiv in range(iNumCivs))
	
	del dGreatPeople

			
def determineGreatPeopleNames(dCivGreatPeople):
	return tuple(determineTypeGreatPeopleNames(dCivGreatPeople.get(iType, [])) for iType in lTypes)

def determineTypeGreatPeopleNames(tEntries):
	return tuple(entry for entry in tEntries if entry not in range(iNumEras))

def calculateOffsets(dCivGreatPeople):
	return tuple(calculateTypeOffsets(dCivGreatPeople.get(iType, [])) for iType in lTypes)

def calculateTypeOffsets(tEntries):
	dOffsets = dict((entry, index) for index, entry in enumerate(tEntries) if entry in range(iNumEras))
	iCount = 0
	
	lOffsets = []
	for iEra in range(iNumEras):
		if iEra in dOffsets:
			iOffset = dOffsets[iEra] - iCount
			iCount += 1
		elif iEra == iAncientEra:
			iOffset = 0
		else:
			iOffset = lOffsets[-1]
		
		lOffsets.append(iOffset)
	
	return tuple(lOffsets)


setup()
