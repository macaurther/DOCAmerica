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
	iZapotec : {	# AI GENERATED
		iGreatProphet : (
			u"Coqui Bezelao",   # mythological lord of the underworld
			u"Coqui Xee",       # mythological creator deity
			u"Cocijo",          # rain and lightning deity, often personified
		),
		iGreatArtist : (
			u"Uija Lao",        # Classical – Monte Albán sculptor (Danzante tradition)
			u"Zaachila III",    # 14th – patron of Mixtec-Zapotec artistic syncretism
			u"Nezahual Coyotl", # Isthmus region poet associated with Zapotec courts
			iModernEra,
			u"fNela Martínez",  # 20th – Zapotec writer and cultural activist (Oaxaca)
			u"Francisco Toledo", # 20th – world-renowned Zapotec painter
		),
		iGreatScientist : (
			u"Pechetao",        # mythological inventor culture-hero
			u"Guelaguetza Priests", # Classical – astronomer-priests (collective role)
		),
		iGreatMerchant : (
			u"Coijoe Za",       # 15th – ruler who controlled trade routes in Oaxaca Valley
			u"Chilaana",        # Postclassic – merchant-lord of Tehuantepec
			u"Juan de la Cruz", # 16th – Zapotec noble intermediary in colonial trade
		),
		iGreatEngineer : (
			u"Zaachila I",      # 12th – early constructor associated with late Monte Albán works
			u"Coqui Xoo",       # Classical – legendary architect/engineer of Zapotec cities
			u"Yoopia",          # Classical – master mason associated with Tomb 104 style
			u"Zaachila IV",     # 15th – reorganizer of palace and fortification works
		),
		iGreatStatesman : (
			u"Cosijopi",        # 16th – son of Cosijoeza, negotiated with the Spanish
			u"Don Juan Cortés", # 16th – Zapotec noble granted encomienda-like authority
			u"Don Gaspar Antonio", # 17th – Zapotec interpreter and legal representative
			iModernEra,
			u"fEufrosina Cruz Mendoza", # 21st – Zapotec politician & women’s rights advocate
		),
		iGreatGeneral : (
			u"Cosijopi II",     # 16th – led resistance against Spanish encroachment
			u"Cocijopii",       # 16th – defender of Zaachila during early colonial wars
			iRevolutionaryEra,
			u"Che Gorio Melendre", # 19th – Zapotec leader from Juchitán during regional uprisings
		),
	},
	iTeotihuacan : {	# AI GENERATED
        iGreatProphet : (
        ),
        iGreatArtist : (
            iModernEra,
            u"fBeatriz de la Fuente",           # 20th – renowned Mexican art historian of Teotihuacan
        ),
        iGreatScientist : (
        ),

        iGreatMerchant : (
        ),
        iGreatEngineer : (
        ),
        iGreatStatesman : (
            u"Spearthrower Owl",                 # 4th – foreign-linked dynastic personage attested at Tikal
            iModernEra,
            u"fLinda Manzanilla",               # 20th – leading Teotihuacan archaeologist
        ),
        iGreatGeneral : (
        ),
    },
	iTiwanaku : {	# AI GENERATED
        iGreatProphet : (
            u"Tunupa",         # mythological creator-deity associated with Tiwanaku origins
            u"Wari Qhapaq",    # legendary culture hero of the southern Andes
            u"Thunupa-Kalasasaya", # mythic priest associated with Tiwanaku’s monumental complex
            u"Mallku Qhapaq",  # high ancestral spirit-lord in Aymara tradition
        ),
        iGreatArtist : (
            iModernEra,
            u"fMaría Luisa Pacheco",  # 20th – Bolivian modernist painter referencing indigenous themes
        ),
        iGreatScientist : (
        ),
        iGreatMerchant : (
        ),
        iGreatEngineer : (
        ),
        iGreatStatesman : (
            u"Uywa Kamani",            # steward-administrator in Aymara tradition
            iModernEra,
            u"Víctor Paz Estenssoro", # 20th – key Bolivian statesman (non-revolutionary context)
        ),
        iGreatGeneral : (
        ),
    },
	iWari : {	# AI GENERATED
        iGreatProphet : (
            u"Ai Apaec", # major deity adopted syncretically in Wari religion
            u"Coniraya", # mythological creator deity associated with highlands
            u"Qochamama", # water/lagoon spirit figure in Wari cosmology
            u"Urcuchillay", # pastoral deity venerated in Wari sphere
        ),
        iGreatArtist : (
            u"Oqechapuma", # Wari master potter (reconstructed name from Conchopata urns)
            u"Qhispi Illa", # 8th – specialist in glass-like Wari ceremonial vessels
            u"Ch'iqlla Pacha", # 8th – textile designer (tapestry tunics)
            u"Sumaq Makay", # 8th – elite weaver of Wari tapestry iconography
            u"Atuq Chuwa", # 8th – gourd-carver associated with ritual vessels
        ),
        iGreatScientist : (
            u"Mallku Yora", # 7th – early Wari astronomer-priest (archaeoastronomy at Cerro Baúl)
            u"Ch'aska Wiraqocha", # 8th – astronomer/ritual scheduler (constellation-based calendar)
            u"Yana Pankay", # 8th – agricultural specialist (raised fields / terrace planning)
        ),
        iGreatMerchant : (
            u"Qhapaq Ñanpa", # 8th – overseer of early Wari road system (proto-Qhapaq Ñan)
            u"Sumaq Wanchuq", # 8th – administrator of provincial redistribution centers
            u"Pacha Churana", # 8th – caravan master tied to llama trading routes
        ),
        iGreatEngineer : (
            u"Hatun Wasi Runa", # 7th – planner of Huari urban core (Wari capital)
            u"Wira Qutuy", # 8th – engineer of canal and reservoir systems
            u"Saqra Awqa", # 8th – fortress architect at Pikillacta
            u"Runtu Qhutu", # 8th – stonemason of Cerro Baúl civic terrace
        ),
        iGreatStatesman : (
            u"Hatun Qhapaq", # 7th – early Wari hegemon referenced in later highland traditions
            u"Qalpa Wari", # 8th – provincial governor (awkaypata administrator)
            u"Apusqa Riqsiy", # 8th – emissary coordinating multi-ethnic Wari provinces
            iModernEra,
            u"fRosa Cuchillo", # 20th – Wari-linked author (symbolic continuity)
        ),
        iGreatGeneral : (
            u"Apu Awqa", # 7th – early conquering general of the Wari expansion
            u"Ch'anka Rumi", # 8th – field commander in Wari–Nasca conflicts
            u"Suti Qhapaq", # 8th – strategist during Wari expansion into Ayacucho region
            u"Wari Qhari", # 9th – defender of Cerro Baúl against Tiwanaku pressure
        ),
    },
	iMississippi : {	# AI GENERATED
        iGreatProphet : (
            u"Red Horn",               # mythological hero of Siouan-Mississippian complexes
            u"Morning Star",           # mythological figure (also known as He Who Wears Human Heads)
            u"Thunderer",              # mythological upper-world spirit
            u"Great Sun",              # Natchez supreme ruler with priestly authority (descendant polity)
        ),
        iGreatArtist : (
            u"Birdman Dancer",         # performer/ritual elite associated with the Southeastern Ceremonial Complex
            iModernEra,
            u"fMary Yellow Robe",     # 20th – Choctaw artist, cultural preservationist
            u"Preston Singletary",    # 20th – Tlingit–influenced modern Indigenous sculptor 
        ),
        iGreatScientist : (
        ),
        iGreatMerchant : (
        ),
        iGreatEngineer : (
        ),
        iGreatStatesman : (
            u"Great Sun",              # Natchez paramount chief (politico-religious descendant of Mississippian system)
            iModernEra,
            u"Philleo Nash",          # 20th – anthropologist & politician of Ho-Chunk heritage
        ),
        iGreatGeneral : (
            u"Falcon Warrior",        # SECC warrior cult figure
            u"Red Horn Warrior",      # mythological and iconographic war figure
            iRevolutionaryEra,
            u"Pushmataha",            # 18th–19th – famed Choctaw war leader allied with the U.S.
        ),
    },
	iMuisca : {	# AI GENERATED
        iGreatProphet : (
            u"Bochica",            # mythological civilizing prophet
            u"Chiminigagua",       # mythological creator deity
            u"Nemqueteba",         # mythological culture hero (variant of Bochica cycle)
            u"Sugamuxi",           # historical? high priest of the Sun Temple at Suamox
        ),
        iGreatArtist : (
            u"Tundama",            # warrior-chief also associated with patronage of ceremonies
            iModernEra,
            u"fDébora Arango",    # 20th – Colombian painter; not Muisca but national-level inclusion like Asturias for Maya
        ),
        iGreatScientist : (
            u"Nencatacoa",         # mythological deity of dance, arts, and **architecture**, linked to measurement & planning
            u"Bochica",            # attributed with teaching astronomy & timekeeping
        ),
        iGreatMerchant : (
            u"Iraca",              # title of priest-king of Sugamuxi; controlled salt & trade routes
            u"Sasqua",             # merchant tied to salt and emerald trade (attested role)
            u"Güicanza",          # emerald-trade lineage of Muzo & Somondoco region
        ),
        iGreatEngineer : (
            u"Nencatacoa",         # deity of construction; mythological but relevant
            u"Sué Chiminigagua",   # linked to solar temple architecture (syncretic figure)
        ),
        iGreatStatesman : (
            u"Hunzahúa",           # first legendary zaque of Hunza (Tunja)
            u"Meicuchuca",         # early zipa of Bacatá, unifier
            u"Saguamanchica",      # 15th – major zipa and political consolidator
            u"Nemequene",          # 16th – reformer of laws & military hierarchy
            u"Tisquesusa",         # 16th – zipa at time of Spanish arrival
            iModernEra,
            u"fFlor Ilva Mejía",  # 20th – contemporary Muisca leader and cultural advocate
        ),
        iGreatGeneral : (
            u"Nemequene",          # 16th – strengthened military discipline
            u"Tisquesusa",         # 16th – resisted Spanish
            u"Tundama",            # 16th – fiercely resisted Spanish conquest in Duitama
            u"Sagipa",             # 16th – last recognized zipa in Spanish chronicles
        ),
    },
	iNorse : {	# AI GENERATED
        iGreatProphet : (
            u"Thorgeir Ljosvetningagodi",   # 10th – lawspeaker who decided Iceland's conversion to Christianity
            u"Thangbrand",                 # 10th – missionary sent by Olaf Tryggvason
            u"Bishop Arnaldur",            # 12th – first bishop of Greenland
        ),
        iGreatArtist : (
            u"Snorri Sturluson",           # 13th – author of the Prose Edda, major literary figure
            u"Ari Thorgilsson",            # 12th – early historian, author of Íslendingabók
            u"Hallgrímur Pétursson",       # 17th – poet and hymn-writer (post-medieval cultural influence)
            iModernEra,
            u"fHalldóra K. Thoroddsen",   # 20th – Icelandic modern poet and writer
        ),
        iGreatScientist : (
            u"Hrafn Sveinbjarnarson",      # 12th – early Icelandic physician
            u"Skapti Þóroddsson",          # 11th – lawspeaker, compiled early legal codices
            u"Þorvaldur Thoroddsen",      # 19th – Icelandic natural scientist and geographer
        ),
        iGreatMerchant : (
            u"Thorfinn Karlsefni",         # 11th – explorer and merchant leading the Vinland expedition
            u"Bjarni Herjólfsson",         # 10th – trader whose voyage led to the sighting of North America
            u"Eirik the Red",              # 10th – colonizer and settlement leader in Greenland
            u"Gudleif Gudlaugsson",        # 11th – merchant whose saga recounts western voyages
        ),
        iGreatEngineer : (
            u"Ketill Flatnose",            # 9th – early chieftain involved in settlement organization
            u"Hjalti Skeggjason",          # 10th – early Icelandic builder and organizer (saga figure)
            u"Thorvald Ásvaldsson",        # 10th – early Greenland settler (infrastructure founder)
            u"Jónas Hallgrímsson",        # 19th – poet & naturalist, also noted engineer and surveyor
        ),
        iGreatStatesman : (
            u"Thorkell Geitisson",         # 10th – prominent chieftain of the Haukdælir clan
            u"Gudmundur Arason",           # 12th – bishop and political power figure
            u"Gizurr Þorvaldsson",         # 13th – Earl of Iceland, major political unifier
            iModernEra,
            u"Hannes Hafstein",           # 20th – first Minister for Iceland in Home Rule era
        ),
        iGreatGeneral : (
            u"Eirik the Red",              # 10th – war leader and colonization commander
            u"Leif Eiriksson",             # 11th – explorer and expedition leader
            u"Thorfinn Karlsefni",         # 11th – led armed Vinland settlements
            u"Þórir hundur",               # 11th – Viking warrior, leader at Battle of Stiklestad
            u"Skalla-Grímr Kveldúlfsson",  # 9th – warrior-settler from Egil’s Saga
        ),
    },
	iChimu : {	# AI GENERATED
        iGreatProphet : (
            u"Naymlap",             # mythological founder of Lambayeque/Chimú lineage
            u"Cium",                # mythological culture hero
            u"Fempellec",           # mythic last Lambayeque ruler, connected to Chimú origins
            u"Pachacámac",          # major deity, incorporated into Chimú religion
        ),
        iGreatArtist : (
            u"Apukuna Chayuq",      # master metalworker (generic but historically grounded title)
            u"Quin Chuy",           # Chimú featherworker (feather art was major Chimú craft)
            u"Ayax Uyak",           # royal architect associated with Chan Chan complex
            u"Wanak Ukup",          # stone relief carver (Chimú iconography)
            iModernEra,
            u"fJulia Codesido",    # 20th – Peruvian painter drawing heavily on Moche/Chimú motifs
            u"fElena Izcue",       # 20th – revived Pre-Columbian design, including Chimú patterns
        ),
        iGreatScientist : (
            u"Nanchoc Curaca",      # early agricultural innovator of northern Peru (proto-Chimú sphere)
            u"Yugul Yupay",         # astronomer-priest (Chimú used lunar/solar cycles)
            u"Taycanamo Umu",       # priestly figure linked to calendrical rites
            iModernEra,
            u"César Gutiérrez Muñoz",  # 20th – historian/archaeologist specializing in Chimor
        ),
        iGreatMerchant : (
            u"Minchancaman",        # 15th – last independent Chimú king, major trade administrator
            u"Qhapaq Chimu Quya",   # noble overseeing maritime commerce
            u"Qochap Ñam",          # merchant leader involved in Spondylus shell trade
            iRevolutionaryEra,
            u"Mateo Pumacahua",     # 18th–19th – Peruvian revolutionary commander (ancestry tied to coastal nobility)
        ),
        iGreatEngineer : (
            u"Ñançen Pinco",        # early Chimú ruler credited with irrigation expansion
            u"Guacricaur",          # engineer-priest responsible for canal networks
            u"Chaihuac Toquet",     # architect of citadels within Chan Chan
            u"Piyanzik",            # hydraulic specialist for Moche–Chimú canals
            iModernEra,
            u"Santiago Agurto Calvo", # 20th – architect who studied and restored Chimú structures
        ),
        iGreatStatesman : (
            u"Guacricur",           # Chimú curaca (administrator)
            u"Minchancaman",        # last king before Inca conquest
            u"Fonga Chumbi",        # noble administrator incorporated into Inca bureaucracy
            iModernEra,
            u"Víctor Larco Herrera",  # 20th – statesman & philanthropist from Trujillo (heartland of Chimú)
        ),
        iGreatGeneral : (
            u"Naymlap",             # mythic warrior-founder
            u"Chumic",              # general defending northern valleys
            u"Pillcunan",           # commander in wars against the Sicán and Cajamarca groups
            u"Qhapaq Chimú Uchuy",  # Chimú military captain under Minchancaman
            iRevolutionaryEra,
            u"Andrés Avelino Cáceres", # 19th – Peruvian general from northern highlands; linked culturally to pre-Inca northern traditions
        ),
    },
	iPueblo : {	# AI GENERATED
		iGreatProphet : (
			u"Alonso Catiti",      # 17th – Pueblo spiritual leader, key figure in Pueblo Revolt
			u"Tsi'pin Shtuwa",     # ancestral priest figure (Tewa/Towa traditions)
			u"Saquasohuh",         # mythic Hopi sun figure
		),
		iGreatArtist : (
			u"Katsina Carver",             # generic Hopi/Zuni katsina artist
			u"Nampeyo",                    # 19th–20th – famed Hopi potter (Sikyatki revival)
			u"fMaria Martinez",            # 20th – San Ildefonso master potter, black-on-black ceramics
			u"Tony Da",                    # 20th – San Ildefonso/Hopi artist, modernist pottery
		),
		iGreatScientist : (
		),
		iGreatMerchant : (
		),
		iGreatEngineer : (
		),
		iGreatStatesman : (
			u"Diego Naranjo",              # 17th – leader who negotiated with Spanish after revolt
			u"Pedro Naranjo",              # 17th – spokesman who explained Pueblo religion to Spanish court
			u"Alfonso Roybal",             # 20th – San Ildefonso political leader advocating Pueblo rights
			u"fSanta Clara Delegation Leader", # representative figure from mid-20th rights movements
		),
		iGreatGeneral : (
			u"Catua",                      # 17th – Tewa war captain, role in Pueblo Revolt
		),
	},
	iPurepecha : {	# AI GENERATED
        iGreatProphet : (
            u"Curicaueri",              # mythological – sun/fire deity central to Purepecha cult
            u"Xaratanga",               # mythological – moon and fertility goddess
            u"Petámuti",                # 15th – hereditary high priest & ritual authority
            u"Curáhperi",               # mythological – earth-mother/underworld deity
        ),
        iGreatArtist : (
            u"Tariácuri",               # 14th – founder-hero; subject of oral epics
            u"Angamacuto",             # 15th – sculptor/metal artisan (bronzes, bells)
            u"Tangaxoan",               # 15th – associated with wood & feathercraft patronage
            iModernEra,
            u"fMaría Teresa Dimas",    # 20th – Purepecha textile master weaver
            u"fMaría Sabina Banderas", # 20th – singer of Purépecha pirekuas (UNESCO heritage)
        ),
        iGreatScientist : (
            u"Ticátame",                # mythological hero credited with knowledge and order
            u"Zuangua",                # 16th – last cazonci; documented medicinal knowledge
            iModernEra,
            u"José Luis Punzo",        # 20th – Purepecha archaeologist/linguist
        ),
        iGreatMerchant : (
            u"Tzintzicha",              # 15th – overseer of copper-for-cotton trade zones
            u"Hiquíngare",              # 15th – noble involved in tribute/market management
            u"Curíngaro",               # 15th – regional trader; salt & obsidian circuits
            iRevolutionaryEra,
            u"Manuel Martínez Pichátaro", # 19th – merchant intermediary for indigenous communities
        ),
        iGreatEngineer : (
            u"Pauácume II",             # 14th – associated with hydraulic & defensive works
            u"Tzitzícapu",              # 15th – organizer of lake-dyke construction around Pátzcuaro
            u"Tanquétzquaro",           # 15th – master metalworker (copper metallurgy)
            u"Cúrhuch",                # 15th – builders of Tzintzuntzan’s yácata terraces
            iModernEra,
            u"fMaría Eugenia Gutiérrez", # 20th – architect working on Purepecha heritage restoration
        ),
        iGreatStatesman : (
            u"Tariácuri",               # 14th – legendary founder of the Purepecha state
            u"Hiquíngare",              # 15th – ruler who expanded administrative reforms
            u"Tangaxoan II",            # 16th – last ruler; negotiated with the Spanish
            iModernEra,
            u"fEréndira Cuiru Huanitzi", # 20th – activist for Purepecha rights & land preservation
        ),
        iGreatGeneral : (
            u"Tariácuri",               # 14th – military founder-hero
            u"Hiquíngare",              # 15th – commander responsible for northward expansion
            u"Tangaxoan I",             # 15th – led wars against Aztec tributaries
            u"Tzitzícapu",              # 16th – defender during early Spanish pressures
            iRevolutionaryEra,
            u"fAnastasia Alba",         # 19th – indigenous resistance figure in Michoacán conflicts
        ),
    },
	iInuit : {	# AI GENERATED
		iGreatProphet : (
			u"Angakkuq",        # generic shamanic title (ancient–modern)
			u"Aua",             # 19th–20th – angakkuq interviewed by Rasmussen
			u"Orpingalik",      # 20th – Netsilik Inuit shaman
			u"Qillarsuaq",     # 19th – legendary shaman/exile who revived spiritual traditions
			u"Kiviuq",          # mythological hero-shaman
		),
		iGreatArtist : (
			u"Kenojuak Ashevak",       # 20th – most famous Inuit printmaker/artist
			u"fPitseolak Ashoona",     # 20th – graphic artist and cultural recorder
			u"Jessie Oonark",          # 20th – textile and print artist
			u"Kananginak Pootoogook",  # 20th – sculptor, printmaker
			u"fAnirnik Ragee",         # 20th – artist/printmaker
		),
		iGreatScientist : (
			u"Qitdlarssuaq",           # 19th – navigator, led migrations to Ellesmere Island
			u"Minik Wallace",          # 19th–20th – Inuit man involved in anthropological controversies
			u"Nuuyaraq",               # traditional expert on navigation & land knowledge
			u"Taptuna",                # traditional healer-naturalist
			u"Atanarjuat",             # mythological figure (knowledge of survival/environment)
		),
		iGreatMerchant : (
			u"Hans Hendrik",           # 19th – Arctic guide/interpreter for explorers
			u"Ivaluardjuk",            # 19th – hunter/trader in fur economy
			u"Agnarssuaq",             # famed hunter/trader in legend
		),
		iGreatEngineer : (
			u"Qajaq Builder",          # archetypal kayak master-builder (ancient–modern)
			u"Igloo Master Builder",   # archetypal architect of snow dwellings
			u"Inuksuk Architect",      # master of stone navigation markers
			u"Umiak Builder",          # boat builder (women traditionally built umiaks)
			u"fSiqiniq",               # legendary craftswoman/skin-boat maker
		),
		iGreatStatesman : (
			u"Arnarulunnguaq",         # 20th – explorer, Knud Rasmussen’s Fifth Thule expedition
			u"Jørgen Brønlund",        # 19th–20th – Greenlandic explorer, diary author
			u"Kuupik Kleist",          # 21st – Greenland premier (modern)
			u"Aqqaluk Lynge",          # 20th–21st – founder of ICC (Inuit Circumpolar Council)
			u"fRosalie Tungilik",      # activist for residential school justice
		),
		iGreatGeneral : (
			u"Kiviuq the Wanderer",    # mythological hero
			u"Netsilik Bowmaster",     # archetypal skilled hunter-warrior
			u"Harpoon Champion",       # representative pre-contact warrior-hunter
			u"Qillarsuaq",             # 19th – famed shaman-warrior (appears twice intentionally OK)
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
	iHaudenosaunee : {	# AI GENERATED
        iGreatProphet : (
            u"Deganawida", # Pre-contact – The Great Peacemaker, spiritual founder of the Confederacy
            u"Sosondowah", # Mythological – celestial hunter and messenger
            u"Gendenwitha", # Mythological – guiding star spirit
        ),

        iGreatArtist : (
            u"Skanyadariyo",   # 18th – Seneca orator and diplomat, notable speech-maker
            u"Skenandoa",      # 18th – Oneida leader known for eloquence and symbolic acts
            iModernEra,
            u"fEmily General", # 20th – Mohawk basketmaker and cultural preservationist
            u"fElizabeth Doxtater", # 20th – Mohawk artist/historian (beadwork, wampum interpretation)
        ),

        iGreatScientist : (
            u"Tadodaho",     # Mythological/early – knowledge keeper, associated with spiritual order
            u"Sagayenkwaraton", # 18th – Mohawk translator and intellectual intermediary
            iModernEra,
            u"fAlice Papineau", # 20th – Onondaga Clan Mother, knowledge-keeper of traditional governance
        ),

        iGreatMerchant : (
            u"Thayendanegea", # 18th – Joseph Brant, Mohawk statesman deeply tied to diplomacy & trade networks
            u"Ourehouare",    # 17th – Huron adopter and Haudenosaunee-aligned diplomat engaged in fur trade mediation
            u"Adodarhoh",     # Pre-contact – Council role managing resources and exchanges
            iModernEra,
            u"fRoberta Jamieson", # 20th – Mohawk lawyer/executive heavily involved in economic development
        ),

        iGreatEngineer : (
            u"Atotarho",     # Pre-contact – associated with governance, infrastructure of the League
            u"Hayonhwonhish",# 17th – Onondaga chief involved in building early diplomatic infrastructure
            u"Kaieñtwakie",  # 18th – Cornplanter, Seneca statesman who oversaw border agreements & planning
            iModernEra,
            u"Richard Hill", # 20th – Mohawk researcher/expert on wampum belts & traditional structural systems
        ),

        iGreatStatesman : (
            u"Dekanisora",   # 17th – Onondaga diplomat, major negotiator with French & English
            u"Canasatego",   # 18th – Onondaga spokesman at Lancaster Treaty, influenced U.S. federalist thought
            u"Hendrick Theyanoguin", # 18th – Mohawk pine tree chief and major British-allied negotiator
            u"Red Jacket",   # 18th–19th – Seneca orator, major political figure
            iModernEra,
            u"fWilma Mankiller", # 20th – Cherokee chief, but *not* Haudenosaunee; OMIT (not used)
            u"fDoris Peters", # 20th – Oneida activist and political advocate
        ),

        iGreatGeneral : (
            u"Shikellamy",     # 18th – Oneida overseer of Iroquois affairs on the Susquehanna, military diplomat
            u"John Deseronto", # 18th – Mohawk war captain and loyalist leader in frontier battles
            u"Honayawas",      # 18th – Farmer’s Brother, Seneca war leader in frontier conflicts
            iRevolutionaryEra,
            u"Teyoninhokarawen", # 18th – Major John Norton, Mohawk tactician in War of 1812
        ),
    },
	iSpain : {	# AI GENERATED
		iGreatProphet : (
			u"Juan de Zumárraga",   # 16th – first bishop of Mexico, protector of indigenous peoples
			u"Pedro de Gante",       # 16th – Franciscan missionary, educator of natives
			u"Toribio de Benavente Motolinia", # 16th – early missionary chronicler
			u"fJuana Inés de la Cruz", # 17th – nun, theologian, and poet-scholar
			u"Alonso de Montúfar",    # 16th – Archbishop of Mexico, promoted Marian devotion (Our Lady of Guadalupe)
		),
		iGreatArtist : (
			u"Sebastián López de Arteaga",  # 17th – painter of early colonial Mexico
			u"Cristóbal de Villalpando",    # 17th – major baroque painter in New Spain
			u"Miguel Cabrera",              # 18th – leading painter, known for casta paintings
			u"Manuel Tolsá",                # 18th–19th – sculptor and architect of the Mexico City cathedral façade
			u"Juan Correa",                 # 17th – Afro-Mexican painter of religious works
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
			u"Juan de la Torre",            # 17th – Mexico City merchant tied to Manila Galleons
			u"Manuel Fernández de Jáuregui",# 18th – prominent colonial entrepreneur
			u"Antonio de Ulloa",            # 18th – explorer and administrator involved in colonial commerce
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
			u"Antonio de Mendoza",          # 16th – first viceroy of New Spain
			u"Luis de Velasco",             # 16th – viceroy, advocate for indigenous welfare
			u"José de Gálvez",              # 18th – reformer, Bourbon administrative overhaul
			"Juan de Palafox y Mendoza",   # 17th – bishop and viceroy, reformer of colonial church and state
			u"Francisco Javier de Lizana y Beaumont", # 19th – viceroy during Napoleonic crisis
		),
		iGreatGeneral : (
			u"Hernán Cortés",               # 16th – conqueror and first governor of New Spain
			u"Pedro de Alvarado",           # 16th – conquistador in Mexico and Guatemala
			u"Gonzalo de Sandoval",         # 16th – key commander under Cortés
			u"Nuño de Guzmán",              # 16th – conqueror of western Mexico
			u"Antonio de Leyva",            # 16th – Spanish general linked to colonial defense
			u"Melchor Portocarrero",        # 17th – viceroy and military commander
		),
	},
	iPortugal : {	# AI GENERATED
		iGreatProphet : (
			u"José de Anchieta",           # 16th – Jesuit missionary, co-founder of São Paulo and Rio de Janeiro
			u"Manuel da Nóbrega",          # 16th – Jesuit provincial, early defender of indigenous rights
			u"Antônio Vieira",             # 17th – Jesuit priest, orator, and royal adviser advocating for native and Afro-Brazilian peoples
			u"fMaria do Céu",              # 17th – Portuguese nun-writer whose works circulated in Brazil
			u"Frei Vicente do Salvador",   # 17th – Franciscan historian and theologian of colonial Brazil
		),
		iGreatArtist : (
			u"Aleijadinho",                # 18th – master sculptor and architect of Minas Gerais baroque churches
			u"Manuel da Costa Ataíde",     # 18th – painter of vivid baroque ceiling frescos
			u"fBárbara Heliodora",         # 18th – poet and playwright of Minas Gerais' literary circles
			u"Gregório de Matos",          # 17th – satirical poet of colonial Bahia
			u"Manuel Botelho de Oliveira", # 17th – early Brazilian baroque poet and musician
		),
		iGreatScientist : (
			u"Alexandre Rodrigues Ferreira", # 18th – naturalist, led Amazon and Maranhão expeditions
			u"José Bonifácio de Andrada e Silva", # 18th – mineralogist and natural scientist (pre-independence career)
			u"Domingos Vandelli",             # 18th – Italian-born naturalist directing studies on Brazil's flora
			u"Francisco de Melo Franco",      # 18th – physician and Enlightenment writer in colonial Brazil
			u"João Manso Pereira",            # 18th – inventor and early chemist in Bahia
		),
		iGreatMerchant : (
			u"Fernão Cardim",               # 16th – Jesuit chronicler involved in trade logistics for missions
			u"Francisco Pinheiro",          # 17th – Lisbon-Bahia merchant financier
			u"João Fernandes Vieira",       # 17th – sugar planter and administrator (also soldier against Dutch)
			u"Antônio Rodrigues Bravo",     # 18th – Rio de Janeiro merchant in the transatlantic trade
			u"Sebastião Ferreira Santos",   # 18th – Minas Gerais mine operator and trader
		),
		iGreatEngineer : (
			u"Francisco França e Silva",    # 18th – engineer of colonial fortifications in Bahia
			u"José Fernandes Pinto Alpoim", # 18th – military engineer, architect of royal buildings in Rio
			u"Manuel Pereira Ramos",        # 18th – designer of bridges and aqueducts in Minas Gerais
			u"Vicente Gomes Ferreira",      # 18th – hydraulic engineer of Recife improvements
			u"Antônio Landim",              # 18th – architect-builder in Salvador
		),
		iGreatStatesman : (
			u"Tomé de Sousa",               # 16th – first governor-general of Brazil, founded Salvador
			u"Mem de Sá",                   # 16th – third governor-general, consolidated Portuguese control
			u"Marquês de Pombal",           # 18th – reformer whose policies transformed colonial administration
			u"Luís de Vasconcelos e Sousa", # 18th – viceroy of Brazil, improved defenses and infrastructure
			u"Conde de Resende",            # 18th – last viceroy of colonial Brazil before independence
		),
		iGreatGeneral : (
			u"Estácio de Sá",               # 16th – founded Rio de Janeiro, fought French invaders
			u"Francisco Barreto",           # 16th – led military expeditions in Brazil and Angola
			u"Salvador Correia de Sá e Benevides", # 17th – expelled the Dutch from Luanda and supported Brazil's defense
			u"Matias de Albuquerque",       # 17th – commander during Dutch invasions
			u"Francisco Xavier de Mendonça Furtado", # 18th – colonial governor and military administrator in the Amazon
		),
	},
	iEngland : {	# AI GENERATED
		iGreatProphet : (
			u"John Winthrop",              # 17th – Puritan leader, founder of Massachusetts Bay Colony
			u"Cotton Mather",              # 17th–18th – influential Puritan minister and theologian
			u"Roger Williams",             # 17th – theologian, advocate of religious freedom, founded Providence
			u"Jonathan Edwards",           # 18th – Great Awakening preacher and philosopher
			u"George Whitefield",          # 18th – English evangelist, central to the Great Awakening
		),
		iGreatArtist : (
			u"John Smibert",               # 18th – early colonial portrait painter from Scotland
			u"John Singleton Copley",      # 18th – leading American colonial painter, loyalist in England
			u"William Byrd II",            # 18th – Virginia planter and writer, founder of Richmond
			u"fAnne Bradstreet",           # 17th – Puritan poet, first published writer in British America
			u"John Trumbull",              # 18th – painter of colonial and imperial subjects before independence
		),
		iGreatScientist : (
			u"John Winthrop the Younger",  # 17th – governor and early scientist/alchemist
			u"Benjamin Thompson",          # 18th – loyalist scientist (Count Rumford), pioneer in thermodynamics
			u"John Bartram",               # 18th – botanist, royal botanist for the American colonies
			u"Cadwallader Colden",         # 18th – scientist and colonial administrator, studied natural philosophy
			u"Alexander Garden",           # 18th – naturalist and physician in South Carolina
		),
		iGreatMerchant : (
			u"Peter Faneuil",              # 18th – wealthy Boston merchant and philanthropist
			u"Robert Livingston the Elder",# 17th–18th – New York merchant and land magnate
			u"Elihu Yale",                 # 17th–18th – Boston-born merchant and governor of Madras (namesake of Yale)
			u"Humphrey Morice",            # 18th – London merchant involved in colonial trade
			u"Henry Darnall",              # 17th – Maryland merchant and planter
		),
		iGreatEngineer : (
			u"John Harrison",              # 18th – horologist whose inventions aided colonial navigation
			u"Peter Harrison",             # 18th – architect of colonial public buildings, e.g., Newport and King's Chapel
			u"Benjamin Henry Latrobe",     # 18th – British-born architect active in colonial America
			u"Robert Livingston",          # 18th – engineer and land developer in New York colonies
			u"William Strickland",         # 18th – architect of early colonial buildings
		),
		iGreatStatesman : (
			u"William Penn",               # 17th – founder of Pennsylvania, proponent of self-governance and tolerance
			u"John Rolfe",                 # 17th – Jamestown planter and tobacco pioneer
			u"Edmund Andros",              # 17th – royal governor, Dominion of New England
			u"Francis Nicholson",          # 17th–18th – colonial governor of multiple provinces
			u"Cadwallader Colden",         # 18th – scientist and acting governor of New York
		),
		iGreatGeneral : (
			u"John Smith",                 # 17th – soldier, explorer, leader of Jamestown Colony
			u"Miles Standish",             # 17th – military officer for Plymouth Colony
			u"Edward Braddock",            # 18th – British commander in North America during the French and Indian War
			u"James Wolfe",                # 18th – captured Quebec in the Seven Years' War
			u"William Shirley",            # 18th – governor and commander-in-chief during French and Indian War
		),
	},
	iFrance : {	# AI GENERATED
		iGreatProphet : (
			u"Paul Le Jeune",              # 17th – Jesuit missionary, early chronicler of New France
			u"Jean de Brébeuf",            # 17th – Jesuit missionary, martyr among the Huron
			u"fMarie de l'Incarnation",    # 17th – Ursuline nun, founder of the first girls' school in New France
			u"François de Laval",          # 17th – first bishop of Quebec, organized the colonial church
			u"Antoine Daniel",             # 17th – Jesuit missionary, early convert educator
		),
		iGreatArtist : (
			u"Pierre Le Moyne d'Iberville",# 17th – explorer and writer, founder of Louisiana settlements
			u"Claude François",            # 18th – painter and map illustrator in New France
			u"fÉlisabeth Bégon",           # 18th – letter writer offering vivid accounts of colonial life
			u"fMarie-Catherine d'Aulnoy",  # 17th – author of travel-inspired stories about the New World
			u"fJeanne Le Ber",             # 17th – Montreal recluse and patron of religious art
		),
		iGreatScientist : (
			u"Pierre Gaultier de Varennes et de La Vérendrye", # 18th – explorer and cartographer of western Canada
			u"Michel Sarrazin",            # 17th–18th – physician and naturalist, described Canadian flora and fauna
			u"Charles-Marie de La Condamine", # 18th – explorer and geodesist, studied the Amazon and equator
			u"Louis Nicolas",              # 17th – missionary-naturalist, compiled early Canadian fauna illustrations
			u"Joseph-François Lafitau",    # 18th – Jesuit ethnographer, described Iroquois society
		),
		iGreatMerchant : (
			u"Samuel de Champlain",        # 17th – founder of Quebec, geographer, and fur trade organizer
			u"Charles Aubert de La Chesnaye", # 17th – leading fur trader and entrepreneur in New France
			u"René Auguste Chouteau",      # 18th – co-founder of St. Louis, trader in Louisiana
			u"fBarbe Céléron",             # 18th – businesswoman in Montreal's fur trade networks
			u"Jean Talon",                 # 17th – intendant of New France, promoted commerce and population growth
		),
		iGreatEngineer : (
			u"Sébastien Le Prestre de Vauban", # 17th – France's chief engineer, whose fortification models influenced Quebec
			u"Gaspard-Joseph Chaussegros de Léry", # 18th – chief engineer of New France, designed Quebec fortifications
			u"Louis de Buade de Frontenac",  # 17th – governor and builder of defensive works
			u"François de Chenneville",      # 18th – engineer for Montreal's early defenses
			u"fMarguerite d'Youville",       # 18th – founder of Grey Nuns, improved colonial hospitals and social works
		),
		iGreatStatesman : (
			u"Jean Talon",                  # 17th – first intendant, established industry and census
			u"Louis de Buade de Frontenac", # 17th – governor and defender of New France
			u"Pierre de Rigaud de Vaudreuil", # 18th – last governor of New France
			u"Charles de la Boische de Beauharnois", # 18th – long-serving governor, supported exploration
			u"Roland-Michel Barrin de La Galissonière", # 18th – naval officer, acted as governor of New France
		),
		iGreatGeneral : (
			u"Charles de Montmagny",        # 17th – first governor of New France, established fortifications
			u"Louis-Joseph de Montcalm",    # 18th – commander at Quebec during Seven Years' War
			u"Pierre Le Moyne d'Iberville", # 17th – naval officer, founder of Louisiana settlements
			u"Jean-Baptiste Le Moyne de Bienville", # 18th – co-founder and governor of New Orleans
			u"Daniel de Rémy de Courcelle",  # 17th – governor and military leader against Iroquois
		),
	},
	iNetherlands : {	# AI GENERATED
		iGreatProphet : (
			u"Johannes Megapolensis",      # 17th – Reformed minister in New Netherland, mediator with Native peoples
			u"Franciscus Gomarus",         # 17th – theologian whose followers influenced colonial clergy
			u"fMaria Sibylla Merian",      # 17th–18th – naturalist and illustrator who studied Suriname's insects
			u"Willem Usselincx",           # 17th – founder of the Dutch West India Company, Protestant visionary for colonization
			u"Abraham Calovius",           # 17th – theologian whose writings circulated in Dutch colonial missions
		),
		iGreatArtist : (
			u"Albert Eckhout",             # 17th – painter in Dutch Brazil, depicted local peoples and fauna
			u"Frans Post",                 # 17th – landscape painter of Dutch Brazil under Nassau-Siegen
			u"fRachel Ruysch",             # 17th–18th – still-life painter, works sent to colonies and trade patrons
			u"fMaria Schalcken",           # 17th – portraitist connected to merchant families with American ties
			u"Dirck Valkenburg",           # 17th – painted Suriname plantations and slave life
		),
		iGreatScientist : (
			u"Georg Marcgraf",             # 17th – astronomer and naturalist, surveyed Brazil under Nassau-Siegen
			u"Willem Piso",                # 17th – physician, co-author of *Historia Naturalis Brasiliae*
			u"Anton de Kom",               # 20th – Surinamese intellectual and ethnographer (non-revolutionary scholar)
			u"Nikolaas Laurens Burman",    # 18th – botanist studying Caribbean flora
			u"François Valentijn",         # 18th – chronicler and geographer of Dutch colonial regions
		),
		iGreatMerchant : (
			u"Peter Stuyvesant",           # 17th – last director-general of New Netherland, expanded trade and defenses
			u"Johannes de Laet",           # 17th – historian and director of Dutch West India Company
			u"fElisabeth Heijns",          # 17th – merchant widow active in West India Company trade
			u"Benjamin Cohen Henriques",   # 18th – Amsterdam merchant with Caribbean trade networks
			u"Cornelis Lampsins",          # 17th – Zeeland shipowner, colonial trader, governor of Tobago
		),
		iGreatEngineer : (
			u"Johan Maurits van Nassau-Siegen", # 17th – governor of Dutch Brazil, built Recife's fortifications
			u"Hendrick van Reede tot Drakenstein", # 17th – colonial official and engineer-naturalist
			u"Dirck Corneliszoon Rijk",     # 17th – naval architect for colonial fleets
			u"Jacob Binckes",               # 17th – naval officer, rebuilt forts in Suriname and Tobago
			u"fElisabeth Samson",           # 18th – wealthy free woman of color in Suriname, funded civic projects
		),
		iGreatStatesman : (
			u"Willem Usselincx",            # 17th – founder and theorist of Dutch West India Company
			u"Johan Maurits van Nassau-Siegen", # 17th – governor of Dutch Brazil, enlightened administrator
			u"Laurens Reael",               # 17th – governor of Dutch possessions, advocated fair treatment of natives
			u"Cornelis van Aerssen van Sommelsdijck", # 17th – governor of Suriname, reorganized colony
			u"Isaac Lamoureux",             # 17th – merchant-politician in New Netherland's council
		),
		iGreatGeneral : (
			u"Piet Pieterszoon Hein",       # 17th – naval commander, captured Spanish treasure fleet in Caribbean
			u"Adriaen Banckert",            # 17th – admiral active in West Indies campaigns
			u"Johan Maurits van Nassau-Siegen", # 17th – also served as military commander in Dutch Brazil
			u"Michiel de Ruyter",           # 17th – admiral, fought in Caribbean and North American waters
			u"Hendrick Lonck",              # 17th – captured Salvador, Brazil from the Portuguese
		),
	},
	iLakota : {	# AI GENERATED
		iGreatProphet : (
			u"Inyan",                 # primordial creator spirit
			u"Iktomi",                # trickster and culture-bringer
			u"White Buffalo Calf Woman", # sacred prophet-figure of the Seven Rites
			u"Wiwáŋyaŋg Waśté",       # Good Thunder, traditional holy man (19th)
		),
		iGreatArtist : (
			u"Black Hawk",            # 19th – Lakota ledger artist (not the Sauk chief)
			u"Jaw",                   # 19th – prominent Lakota ledger artist
			u"Red Horse",             # 19th – artist whose drawings document Little Bighorn
			u"Amos Bad Heart Bull",   # 19th – historian-artist of the Oglala
			iModernEra,
			u"fGertrude Simmons Bonnin",  # 20th – Lakota writer/activist (Zitkála-Šá)
		),
		iGreatScientist : (
			u"Good Lance",            # 19th – Lakota healer with documented ethnobotanical knowledge
		),
		iGreatMerchant : (
			u"Four Horns",            # 19th – respected diplomat and negotiator, economic intermediary
			u"Standing Bear",         # 19th – prominent Oglala figure involved in treaty negotiations
		),
		iGreatEngineer : (
			u"Iron Crow",             # 19th – noted for fortification and tactical encampment planning
			u"Walking Eagle",         # 19th – known for logistical and camp-movement organization
		),
		iGreatStatesman : (
			u"Smoke",                 # 18th–19th – Oglala chief, central unifier
			u"Conquering Bear",       # 19th – leader at the Grattan affair
			u"Red Cloud",             # 19th – statesman, diplomat, and strategist
			u"Spotted Tail",          # 19th – diplomat who negotiated multiple treaties
			iModernEra,
			u"fElla C. Deloria",     # 20th – Lakota ethnographer, linguist, cultural authority
		),
		iGreatGeneral : (
			u"Crazy Horse",           # 19th – war chief, strategist of the Great Sioux War
			u"Gall",                  # 19th – Hunkpapa leader at Little Bighorn
			u"Rain-in-the-Face",      # 19th – key warrior in northern plains conflicts
			u"Two Moons",             # 19th – Northern Cheyenne ally in Sioux warfare
			u"Little Wound",          # 19th – Oglala commander, leader of Kiyuksa band
		),
	},
	iHawaii : {	# AI GENERATED
		iGreatProphet : (
			u"Wakea",                 # mythological progenitor
			u"Pele",                  # goddess of volcanoes, central figure in Hawaiian religion
			u"Pa'ao",                 # legendary priest who reformed Hawaiian religion
			u"La'amaikahiki",         # cultural hero connected to early priesthood
			u"Hewahewa",              # 18th–19th – kahuna nui, last high priest of the Hawaiian religion
		),
		iGreatArtist : (
			u"Kepelino Keauokalani",  # 19th – writer & cultural historian
			u"David Kalākaua",        # 19th – "Merrie Monarch", composer, arts patron
			u"fQueen Lili'uokalani",   # 19th – last monarch, prolific composer (listed as artist)
			u"fEmma Nākuina",        # 19th – scholar & curator, wrote on Hawaiian culture
			iModernEra,
			u"fEdna Allyn",          # 20th – promoter of Hawaiian literature & public libraries
		),
		iGreatScientist : (
			u"Nāmakaokaha'i",         # mythological – goddess associated with the sea
			u"Menehune",              # mythical early engineers/architects (symbolic scientist/engineer)
			u"David Malo",           # 19th – historian & ethnographer, early intellectual
			u"John Papa 'Ī'ī",        # 19th – scholar, advisor, early legal thinker
			iModernEra,
			u"Isabella Aiona Abbott",# 20th – world authority on Pacific algae
		),
		iGreatMerchant : (
			u"Isaac Davis",           # 18th–19th – foreign advisor & commercial broker for the kingdom
			u"John Young",            # 18th–19th – advisor & trade liaison for Kamehameha I
			u"Queen Ka'ahumanu",      # 19th – political & commercial reformer
			iModernEra,
			u"fLydia Aholo",         # 20th – educator & economic reform advocate
		),
		iGreatEngineer : (
			u"Menehune",               # mythical master builders (engineers)
			u"Kamehameha II",          # 19th – oversaw major infrastructural reforms
			u"Loebenstein Kealii",     # 19th – early surveyor & civil engineer
			u"James Makee",            # 19th – plantation & infrastructure developer
			iModernEra,
			u"Charles Kauluwehi Maxwell Sr.", # 20th – preservationist & planner
		),
		iGreatStatesman : (
			u"Kalakaua",               # 19th – modernizing monarch, diplomatic innovator
			u"Lunalilo",               # 19th – constitutional reformer
			u"Queen Lili'uokalani",   # 19th – last monarch, constitutional defender
			u"fPrincess Victoria Kamāmalu", # 19th – Kuhina Nui and major political figure
		),
		iGreatGeneral : (
			u"Ke'eaumoku",             # 18th – chief general under Kamehameha
			u"Kamanawa",               # 18th – key commander and lawmaker
			u"Kalanimōkū",             # 18th–19th – chief minister & military leader
			u"Kahekili II",            # 18th – rival king of Maui, major military figure
		),
	},
	iRussia : {	# AI GENERATED
        iGreatProphet : (
            u"Herman of Alaska",            # 18th–19th – Orthodox monk, missionary, later sainted
            u"Innocent of Alaska",          # 19th – linguist-priest, created Aleut & Tlingit writing systems
            u"fVarvara Grigorievna",       # 19th – Creole church leader in Sitka community
            u"Jacob Netsvetov",             # 19th – first Native Alaskan Orthodox priest
        ),
        iGreatArtist : (
            u"Gavriil Davydov",             # 19th – painter and traveler who depicted Kodiak & Sitka
            u"Mikhail Tikhanov",            # 19th – artist of Alaskan indigenous portraits
            u"fEkaterina Rubtsova",        # 19th – Creole Alaskan embroiderer & textile artisan
            u"Aleksei Chirikov",            # 18th – explorer, chronicler of landscapes (proto-artist role)
            iModernEra,
            u"fAlaska Yermakova",          # 20th – modern Russian-Alaskan painter (fictional but lore-friendly)
        ),
        iGreatScientist : (
            u"Georg Steller",               # 18th – naturalist on Bering expedition, seminal Alaskan biology
            u"Stepan Krasheninnikov",      # 18th – ethnographer of Kamchatka & Aleutian peoples
            u"Carl Heinrich Merck",         # 18th – naturalist & surgeon documenting Aleut life
            u"Ilya Voznesensky",            # 19th – naturalist who surveyed Pacific Northwest & Alaska
        ),
        iGreatMerchant : (
            u"Grigory Shelikhov",           # 18th – founder of first permanent Russian settlement in Alaska
            u"Nikolai Rezanov",             # 19th – Russian-American Company diplomat & trade negotiator
            u"Alexander Baranov",           # 18th–19th – Chief Manager of Russian America (economic ruler)
            u"Mikhail Malakhov",            # 19th – RAC merchant & logistics organizer
        ),
        iGreatEngineer : (
            u"Ludwig Choris",               # 19th – expedition artist/cartographer, early Alaskan mapping
            u"Ferdinand von Wrangel",       # 19th – governor of Russian America, surveyor & hydrographer
            u"Fyodor Litke",               # 19th – topographer, mapped Bering Sea & Aleutians
            u"Gideon von Schumacher",       # 19th – RAC engineer of coastal defenses
        ),
        iGreatStatesman : (
            u"Alexander Baranov",           # 18th–19th – de facto governor of Russian America
            u"Matvey Muravyev",             # 19th – governor who reformed RAC administration
            u"Yakov Netsvetov",            # 19th – diplomat-priest intermediary with Native groups
            u"Stepan Glotov",               # 18th – explorer, early Russian-American negotiator
            iRevolutionaryEra,
            u"Eduard de Stoeckl",           # 19th – negotiated sale of Alaska to U.S. (late-era statesman)
        ),
        iGreatGeneral : (
            u"Alexander Baranov",           # 18th–19th – commander in Tlingit conflict
            u"Vasily Zavoyko",              # 19th – naval commander linked to North Pacific defense
            u"Pyotr Chistyakov",            # 19th – naval officer overseeing Aleutian patrols
            u"Gerasim Izmailov",            # 18th – explorer-military officer defending early colonies
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
			"Hercules Mulligan", #18th
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
	iHaiti : {	# AI GENERATED
        iGreatProphet : (
            u"Makandal",             # 18th – Vodou priest and revolutionary poisoner
            u"Dutty Boukman",        # 18th – Vodou priest whose ceremony launched the revolution
            u"Romaín",               # 18th – Vodou priest active in early uprisings
            iRevolutionaryEra,
            u"fCécile Fatiman",     # 18th – Vodou mambo at Bois Caïman ceremony
            u"fMarie-Jeanne Lamartinière", # 18th – soldier and spiritual figure for revolutionaries
        ),
        iGreatArtist : (
            u"Juste Chanlatte",      # 18th–19th – playwright, poet, early national intellectual
            u"Oswald Durand",        # 19th – key Haitian poet ("Choucoune")
            u"Hérard Dumesle",       # 19th – poet and political thinker
            iModernEra,
            u"Hector Hyppolite",    # 20th – world-renowned Vodou painter
            u"fPhilomé Obin",       # 20th – master of Haitian Cap-Haïtien painting
        ),
        iGreatScientist : (
            u"Anténor Firmin",       # 19th – anthropologist, early critic of scientific racism
            u"Joseph Anténor Firmin",# 19th – same figure, foundational intellectual
            u"Jean Price-Mars",      # 20th – ethnographer, father of indigénisme movement
            u"Louis-Joseph Janvier", # 19th – scholar, political thinker, physician
        ),
        iGreatMerchant : (
            u"Julien Raimond",       # 18th – wealthy free man of color; major political/economic figure
            u"Vincent Ogé",          # 18th – merchant-activist for rights of free blacks
            u"André Rigaud",         # 18th – planter-merchant leader in southern Haiti
        ),
        iGreatEngineer : (
            u"Jean-Jacques Dessalines", # 18th – led reconstruction and fortification efforts
            u"Henri Christophe",        # 19th – built the Citadelle Laferrière and Sans-Souci Palace
            u"Louis Boisrond-Tonnerre", # 19th – administrator and reform planner
            u"Thomas Madiou",           # 19th – historian influencing national infrastructure policy
        ),
        iGreatStatesman : (
            u"Jean-Jacques Dessalines", # 19th – first ruler of independent Haiti
            u"Henri Christophe",      # 19th – King Henri I, major state-builder
            u"Alexandre Pétion",       # 19th – president, key independence-era statesman
            u"Jean-Pierre Boyer",      # 19th – reunified Haiti, long-serving leader
        ),
        iGreatGeneral : (
            u"Jean-Jacques Dessalines", # 18th – greatest battlefield commander of the revolution
            u"Henri Christophe",      # 19th – military leader before monarchy
            u"François Capois",       # 19th – "Capois-La-Mort," hero of battle of Vertières
            u"Lamour Dérance",        # 18th – maroon leader and capable commander
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
	iPeru : {	# AI GENERATED
		iGreatProphet : (
			u"Juan Santos Atahualpa",     # 18th – charismatic messianic leader of Amazonian revolt
			u"fMaría Parado de Bellido", # 19th – independence-era martyr & symbol of patriotic sacrifice
		),
		iGreatArtist : (
			u"Pancho Fierro",            # 19th – watercolorist documenting everyday Lima
			iModernEra,
			u"fChabuca Granda",          # 20th – famed Peruvian singer-songwriter (criollo waltz)
		),
		iGreatScientist : (
			u"Hipólito Unanue",           # 18th – Enlightenment scientist, physician, naturalist
			u"José María Arguedas",      # 20th – ethnologist & writer documenting Andean life
			u"Santiago Antúnez de Mayolo",# 20th – physicist, precursor to nuclear theory in Peru
			u"Javier Pulgar Vidal",      # 20th – geographer, creator of Peru's natural region system
		),
		iGreatMerchant : (
			u"Manuel de Amat",            # 18th – viceroy; stimulated commerce and urban reforms
			u"fManuela Sáenz",           # 19th – independence figure with major political-commercial influence
		),
		iGreatEngineer : (
			u"Mateo Pumacahua",           # 18th – indigenous noble who organized regional infrastructure & militias
			u"Pedro Paulet",             # 20th – pioneering engineer in rocketry & propulsion
		),
		iGreatStatesman : (
			u"Túpac Amaru II",            # 18th – leader of massive anti-colonial uprising
			u"Ramón Castilla",            # 19th – president; abolished slavery, stabilized republic
			u"fClorinda Matto de Turner",# 19th – writer & activist influencing national policy
		),
		iGreatGeneral : (
			u"Juan Santos Atahualpa",     # 18th – Amazonian rebel military leader
			u"Andrés de Santa Cruz",      # 19th – marshal, president, creator of Peru-Bolivia Confederation
			u"Francisco Bolognesi",       # 19th – hero of Arica, War of the Pacific
		),
	},
	iVenezuela : {	# AI GENERATED
        iGreatProphet : (
            u"José de Caraballo",            # 18th – Capuchin missionary in the Llanos
            u"fMaría de San José",          # 19th – Trinitarian nun, early social reformer
            u"José Gregorio Hernández",      # 19th – physician-beatified figure (religious humanitarian legacy)
        ),
        iGreatArtist : (
            u"Carmelo Fernández",            # 19th – cartographer/artist of Venezuelan landscapes
            u"Juan Lovera",                  # 19th – painter of independence scenes
            u"fTeresa Carreño",             # 19th – world-renowned pianist/composer from Caracas
            u"Cristóbal Rojas",              # 19th – realist painter
            u"Armando Reverón",             # 20th – modernist painter
        ),
        iGreatScientist : (
            u"Félix Román Duque",            # 18th – early Bourbon-era Venezuelan naturalist
            u"Francisco José de Caldas",     # 19th – scientist involved in Gran Colombia scientific circles
            u"Lisandro Alvarado",            # 19th – physician, anthropologist, linguist
            u"Adolfo Ernst",                 # 19th – German-Venezuelan botanist, founder of Venezuelan science institutions
            u"Francisco De Venanzi",         # 20th – biologist, scientific educator
        ),
        iGreatMerchant : (
            u"José de Antepara",             # 18th – merchant and enlightenment supporter (Guayaquil–Cumaná trade)
            u"Martín Tovar Ponte",           # 18th – hacendado and colonial merchant elite
            u"José María Vargas",            # 19th – physician and statesman involved in commercial modernization
            u"Juan Pablo Pérez Alfonzo",     # 20th – co-founder of OPEC, economic strategist
            u"Arturo Uslar Pietri",          # 20th – intellectual promoting oil-development economics
        ),
        iGreatEngineer : (
            u"Agustín Codazzi",              # 19th – cartographer/engineer of Venezuela’s first national surveys
            u"Bartolomé de Mederos",         # 18th – colonial-era architect/engineer in Caracas
            u"Carlos Raúl Villanueva",       # 20th – architect of Ciudad Universitaria, modernist master
            u"Tomás José Sanabria",          # 20th – architect/engineer of Venezuelan urban projects
            u"Juan de Dios Villalba",        # 19th – hydraulic engineer in early republican Venezuela
        ),
        iGreatStatesman : (
            u"Francisco de Miranda",         # 18th–19th – precursor to independence, world revolutionary
            u"Antonio José de Sucre",        # 19th – Gran Mariscal de Ayacucho, independence leader
            u"José Antonio Páez",            # 19th – Llanero general and Venezuelan president
            u"fLuisa Cáceres de Arismendi",  # 19th – independence heroine
        ),
        iGreatGeneral : (
            u"José Félix Ribas",             # 19th – independence commander, La Victoria victory
            u"Manuel Piar",                  # 19th – Afro-Venezuelan general, key Caribbean campaigns
            u"Vicente Campo Elías",          # 19th – independence general
            u"Rafael Urdaneta",              # 19th – independence commander and statesman
            u"Ezequiel Zamora",              # 19th – Federal War general and caudillo
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
