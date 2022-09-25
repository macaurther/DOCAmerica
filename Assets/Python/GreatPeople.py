# coding: utf-8

from RFCUtils import *
from Events import handler
from Core import *

import BugCore

AlertOpt = BugCore.game.MoreCiv4lerts


lTypes = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral, iGreatSpy]

lGreatPeople = [[[] for j in lTypes] for i in range(iNumCivs)]
lOffsets = [[[0 for i in range(iNumEras)] for j in lTypes] for i in range(iNumCivs)]


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
		
		unit.setName(sName)
		
	# Leoreth: display notification
	if bAnnounceBirth:
		if not player(iPlayer).isMinorCiv() and not player(iPlayer).isBarbarian():
			text_key = 'TXT_KEY_MISC_GP_BORN'
			if city.isNone():
				text_key = 'TXT_KEY_MISC_GP_BORN_OUTSIDE'
				city = closestCity(unit)
		
			for iLoopPlayer in players.major().alive():
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

def getAlias(iCiv, iType, iEra):
	
	return iCiv
	
def getType(iUnit):
	iUnitType = base_unit(iUnit)
	if iUnitType in lTypes: return lTypes.index(iUnitType)
	return -1

def getAvailableNames(iPlayer, iType):
	pPlayer = player(iPlayer)
	iEra = pPlayer.getCurrentEra()
	iCiv = getAlias(civ(iPlayer), iType, iEra)
	
	return getEraNames(iCiv, iType, iEra)

def getEraNames(iCiv, iType, iEra):
	lNames = lGreatPeople[iCiv][iType]
	
	iOffset = lOffsets[iCiv][iType][iEra]
	iNextOffset = len(lNames)
	if iEra + 1 < iNumEras: iNextOffset = lOffsets[iCiv][iType][iEra+1]
	
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

def setup():
	for iCiv in dGreatPeople.keys():
		for iType in dGreatPeople[iCiv].keys():
			iOffsets = 0
			
			for i, entry in enumerate(dGreatPeople[iCiv][iType]):
				if entry in range(iNumEras): 
					lOffsets[iCiv][lTypes.index(iType)][entry] = i - iOffsets
					iOffsets += 1
				else: 
					lGreatPeople[iCiv][lTypes.index(iType)].append(entry)
				
			lCurrentOffsets = lOffsets[iCiv][lTypes.index(iType)]
			for i in range(1, len(lCurrentOffsets)):
				if lCurrentOffsets[i] < lCurrentOffsets[i-1]: lCurrentOffsets[i] = lCurrentOffsets[i-1]
				
			lCurrentOffsets[iDigital] = len(lGreatPeople[iCiv][lTypes.index(iType)])
				
	print lGreatPeople

		
dGreatPeople = {

iMaya : {
	iGreatProphet : [
		"Junajpu", # mythological
		"Xb'alanke", # mythological
		"Kukulkan", # 10th, named after the god
		"Ce Acatl Topiltzin", # 10th toltec
	],
	iGreatArtist : [
		"Uaxaclajuun Ub'aah K'awiil", # 8th
		"Chakalte'", # 8th
		"Jun Nat Omootz", # 8th
		"Asan Winik Tu'ub", # 8th
		"Chan Ch'ok Wayib Xok", # 8th
		"Waj Tan Chak", # 8th
		iGlobal,
		"fMarisol Ceh Moo", # 20th
	],
	iGreatScientist : [
		"Itzamna", # mythological
		"Huematzin", # 8th toltec
		"Papantzin", # 9th toltec
	],
	iGreatMerchant : [
		"Ek Chuaj", # mythological
		"Apoxpalon", # 16th
		"Tabscoob", # 16th
	],
	iGreatEngineer : [
		"Chan Imix K'awiil", # 7th
		"fK'ab'al Xook", # 8th
		"Ha' K'in Xook", # 8th
		"Itzam K'an Ahk", # 8th
		"K'inich Yat Ahk", # 8th
	],
	iGreatStatesman : [
		"Yax Ehb Xook", # 1st
		"fYohl Ik'nal", # 6th
		"Yuknoom Ch'een", # 7th
		"Jasaw Chan K'awiil", # 8th
		iGlobal,
		u"fRigoberta Menchú", # 20th
	],
	iGreatGeneral : [
		"Siyaj K'ak'", # 4th teotihuacan
		"K'inich Yo'nal Ahk", # 7th
		"fXochitl", # 9th toltec
		"Hunac Ceel", # 12th
		iRenaissance,
		"Napuc Chi", # 16th
		"Tecun Uman", # 16th
	],
},
iSpain : {
	iGreatProphet : [
		"Juan de Ortega", # 11th
		u"Domingo de Guzmán", # 12th
		iRenaissance,
		"Ignacio de Loyola", # 16th
		u"Juan de Sepúlveda", # 16th
		u"fTeresa de Ávila", # 16th
		u"Francisco Suárez", # 16th
		u"Bartolomé de Las Casas", # 16th
		iIndustrial,
		u"Junípero Serra", # 18th
		"fJoaquima de Vedruna", # 19th
		iGlobal, 
		u"Josemaría Escrivá", # 20th
	],
	iGreatArtist : [
		"Gonzalo de Berceo", # 13th
		"Juan Manuel", # 14th
		iRenaissance,
		"Miguel de Cervantes", # 16th
		"Garcilaso de la Vega", # 16th
		"Lope de Vega", # 17th
		u"Diego de Silva Velázquez", # 17th
		u"fJuana Inés de la Cruz", # 17th
		"Francisco de Goya", # 18th
		iIndustrial,
		u"fGertrudis Gómez de Avellaneda", # 19th
		u"Gustavo Adolfo Bécquer", # 19th
		u"fRosalía de Castro", # 19th
		u"Isaac Albéniz", # 19th
		u"Benito Pérez Galdós", # 19th
		iGlobal,
		"Pablo Picasso", # 20th
		u"Joan Miró", # 20th
		u"Luis Buñuel", # 20th
		u"Salvador Dalí", # 20th
	],
	iGreatScientist : [
		"Gerardo de Cremona", # 12th
		"Yehuda ben Moshe", # 13th
		"Ramon Llull", # 13th
		iRenaissance,
		"Miguel Serveto", # 16th
		u"Carlos de Sigüenza y Góngora", # 17th
		"Antonio de Ulloa", # 18th
		iIndustrial,
		u"José Celestino Mutis", # 18th
		u"Santiago Ramón y Cajal", # 19th
		iGlobal, 
		"Severo Ochoa", # 20th
	],
	iGreatMerchant : [
		u"Cristóbal Colón", # 15th
		"Fernando de Magallanes", # 15th
		u"Martín de Azpilcueta", # 16th
		"Hernando de Soto", # 16th
		u"José Penso de la Vega", # 17th
		iIndustrial,
		"Salvador Fidalgo", # 18th
		iGlobal,
		"Juan March Ordinas", # 20th
		"Amancio Ortega", # 20th
	],
	iGreatEngineer : [
		"Juan Bautista de Toledo", # 16th
		"Juan de Herrera", # 16th
		iIndustrial,
		u"Agustín de Betancourt", # 18th
		"Alberto de Palacio y Elissague", # 19th
		"Esteban Terradas i Illa", # 19th
		u"Antoni Gaudí", # 19th
		iGlobal,
		"Leonardo Torres y Quevedo", # 20th
		"Juan de la Cierva", # 20th
	],
	iGreatStatesman : [
		"Alfonso el Sabio", # 13th
		iRenaissance,
		u"Francisco Jiménez de Cisneros", # 15th
		"Francisco de Vitoria", # 16th
		iIndustrial,
		u"José de Gálvez", # 18th
		u"José Moniño", # 18th
		"Juan Prim", # 19th
		iGlobal, 
		u"Lluís Companys", # 20th
		u"fDolores Ibárruri", # 20th
	],
	iGreatGeneral : [
		"El Cid", # 11th
		"Alfonso el Bravo", # 11th
		"Jaume el Conqueridor", # 13th
		iRenaissance,
		"Francisco Coronado", # 16th
		u"Hernán Cortés", # 16th
		"Francisco Pizarro", # 16th
		u"Álvaro de Bazán", # 16th
		u"fMaría Pacheco", # 16th
		u"Fernando Álvarez de Toledo", # 16th
		u"Ambrosio Spínola Doria", # 17th
		u"Bernardo de Gálvez", # 18th
		iIndustrial, 
		u"fAgustina de Aragón", # 19th
		"Fernando Villaamil", # 19th
		iGlobal, 
		"Emilio Mola", # 20th
		"Vicente Rojo Lluch", # 20th
		"Mohamed ben Mizzian", # 20th
	],
	iGreatSpy : [
		u"Tomás de Torquemada", # 15th
		"Bernardino de Mendoza", # 17th
		u"fManuela Desvalls Vergós", # 18th
		"Ali Bey el Abbassi", # 18th 
		iGlobal,
		u"Juan Pujol García", # 20th
		u"Ramón Mercader", # 20th
	],
},
iFrance : {
	iGreatProphet : [
		u"Pierre Abélard", # 12th
		u"Pierre Vaudès", # 12th
		"Louis IX", # 13th
		"fJeanne d'Arc", # 15th
		iRenaissance,
		"Jean Calvin", # 16th
		"Vincent de Paul", # 17th
		"fJeanne Mance", # 17th
		"fMarguerite Bourgeoys", # 17th
		u"Jacques-Bénigne Bossuet", # 17th
		iIndustrial,
		u"fThérèse de Lisieux", # 19th
		"Auguste Comte", # 19th
		iGlobal,
		"Albert Schweitzer", # 20th
		u"Marcel Légaut", # 20th
		u"Henri Grouès", # 20th
	],
	iGreatArtist : [
		u"Pérotin", # 12th
		u"Chrétien de Troyes", # 12th
		"fChristine de Pizan", # 15th
		"Jean Fouquet", # 15th
		iRenaissance,
		u"François Rabelais", # 16th
		"Charles Le Brun", # 17th
		"Jean-Baptiste Lully", # 17th
		"Jean Racine", # 17th
		u"Molière", # 17th
		"Antoine Watteau", # 18th
		"Voltaire", # 18th
		u"fÉlisabeth Vigée Le Brun", # 18th
		iIndustrial,
		u"Honoré de Balzac", # 19th
		"Alexandre Dumas", # 19th
		"Victor Hugo", # 19th
		"fGeorge Sand", # 19th
		"Charles Baudelaire", # 19th
		"Auguste Rodin", # 19th
		"Claude Monet", # 19th
		"Claude Debussy", # 19th
		iGlobal,
		"Henri Matisse", # 19th
		"Maurice Ravel", # 20th
		"Marcel Proust", # 20th
		u"fÉdith Piaf", # 20th
		"Albert Camus", # 20th
	],
	iGreatScientist : [
		"Gerbert d'Aurillac", # 10th
		"Guy de Chauliac", # 14th
		"Nicole Oresme", # 14th
		iRenaissance,
		"Marin Mersenne", # 17th
		u"René Descartes", # 17th
		"Pierre de Fermat", # 17th
		"Blaise Pascal", # 17th
		"Antoine Lavoisier", # 18th
		u"fÉmilie du Châtelet", # 18th
		iIndustrial,
		"Pierre-Simon Laplace", # 18th
		"Georges Cuvier", # 19th
		"Louis Pasteur", # 19th
		"fMarie-Sophie Germain", # 19th
		"fMarie Curie", # 19th
		"Antoine Henri Becquerel", # 19th
		iGlobal,
		u"fIrène Joliot-Curie", # 20th
		"Jacques Monod", # 20th
		u"Benoît Mandelbrot", # 20th
	],
	iGreatMerchant : [
		u"Éloi de Noyon", # 7th
		u"fJeanne la Fouacière", # 13th
		iRenaissance,
		"Jacques Cartier", # 16th
		"Samuel de Champlain", # 17th
		"Pierre Le Moyne d'Iberville", # 17th
		"Antoine de Lamothe-Cadillac", # 18th
		u"fThérèse de Couagne", # 18th
		iIndustrial,
		u"Frédéric Bastiat", # 19th
		"Ferdinand de Lesseps", # 19th
		"Louis Vuitton", # 19th
		iGlobal,
		"fCoco Chanel", # 20th
		"Marcel Dessault", # 20th
		"fMarie Marvingt", # 20th
	],
	iGreatEngineer : [
		"Suger", # 12th
		"Villard de Honnecourt", # 13th
		"Pierre de Montreuil", # 13th
		iRenaissance,
		u"Sébastien Le Prestre de Vauban", # 17th
		"Jules Hardouin-Mansart", # 17th
		"Claude Perrault", # 17th
		"Charles-Augustin Coulomb", # 18th
		"Joseph-Michel Montgolfier", # 18th
		iIndustrial,
		"Joseph Marie Jacquard", # 18th
		"Sadi Carnot", # 19th
		"Louis Daguerre", # 19th
		"Norbert Rillieux", # 19th
		"Alexandre Gustave Eiffel", # 19th
		iGlobal,
		u"Louis Lumière", # 20th
		"Le Corbusier", # 20th
	],
	iGreatStatesman : [
		u"fAliénor d'Aquitaine", # 12th
		"Philippe de Beaumanoir", # 13th
		iRenaissance,
		"Jean Bodin", # 16th
		"Armand Jean du Plessis de Richelieu", # 17th
		"Jean-Baptiste Colbert", # 17th
		u"fAnne-Marie-Louise d'Orléans", # 17th
		u"Charles-Maurice de Talleyrand-Périgord", # 18th
		"Montesquieu", # 18th
		"Maximilien Robespierre", # 18th
		iIndustrial,
		"Adolphe Thiers", # 19th
		"Alexis de Tocqueville", # 19th
		"Pierre-Joseph Proudhon", # 19th
		iGlobal,
		u"Léon Blum", # 20th
		"fSimone de Beauvoir", # 20th
	],
	iGreatGeneral : [
		"Charles Martel", # 8th
		"Godefroy de Bouillon", # 11th
		"fJeanne de Flandre", # 14th
		"Charles V", # 14th
		"fJeanne d'Arc", # 15th
		iRenaissance,
		u"Louis de Bourbon-Condé", # 17th
		"Turenne", # 17th
		"Maurice de Saxe", # 18th
		"Louis-Joseph de Montcalm", # 18th
		u"Louis-René de Latouche-Tréville", # 18th
		iIndustrial,
		u"André Masséna", # 18th
		"Louis-Nicolas Davout", # 18th
		"Joachim Murat", # 18th
		"Louis-Alexandre Berthier", # 19th
		"Gilbert de Lafayette", # 19th
		"Patrice de MacMahon", # 19th
		iGlobal,
		"Ferdinand Foch", # 20th
		"Joseph Joffre", # 20th
		u"Philippe Pétain", # 20th
		"Philippe Leclerc de Hauteclocque", # 20th
	],
	iGreatSpy : [
		u"Bertrandon de la Broquière", # 15th
		"fAntoinette de Maignelais", # 15th
		iRenaissance,
		"fCharlotte de Sauve", # 16th
		u"fMarie Anne de La Trémoille", # 17th
		"fCharlotte Corday", # 18th
		"Pierre Beaumarchais", # 18th
		u"Chevalier d'Éon", # 18th
		iIndustrial,
		"fMichelle de Bonneuil", # 19th
		"Charles Schulmeister", # 19th
		iGlobal,
		u"fJoséphine Baker", # 20th
		"Gilbert Renault", # 20th
	],
},
iEngland : {
	iGreatProphet : [
		"Bede the Venerable", # 8th
		"Anselm of Canterbury", # 11th
		"Thomas Becket", # 12th
		iRenaissance,
		"Thomas More", # 16th
		"fAnne Hutchinson", # 17th
		"John Newton", # 18th
		"William Penn", # 18th
		"Jonathan Edwards", # 18th
		"fAnn Lee", # 18th
		"John Wesley", # 18th
		iIndustrial,
		"William Booth", # 19th
		"David Livingstone", # 19th
		iGlobal,
		"Gerald Gardner", # 20th
		"Aleister Crowley", # 20th
		"John Stott", # 20th
	],
	iGreatArtist : [
		u"Ælfric of Eynsham", # 10th
		"Geoffrey Chaucer", # 14th
		"Thomas Malory", # 15th
		iRenaissance,
		"William Shakespeare", # 17th
		"John Milton", # 17th
		"John Vanbrugh", # 17th
		"George Frideric Handel", # 18th
		"fJane Austen", # 18th
		iIndustrial,
		"William Blake", # 18th
		"fMary Shelley", # 19th
		"Alfred Tennyson", # 19th
		"Charles Dickens", # 19th
		"fGeorge Eliot", # 19th
		"Arthur Conan Doyle", # 19th
		iGlobal,
		"fVirginia Woolf", # 20th
		"James Joyce", # 20th
		"fAgatha Christie", # 20th
		"John R. R. Tolkien", # 20th
		"Alfred Hitchcock", # 20th
		"John Lennon", # 20th
	],
	iGreatScientist : [
		"Byrhtferth", # 10th
		"Robert Grosseteste", # 13th
		"Roger Bacon", # 13th
		"William of Ockham", # 14th
		iRenaissance,
		"Francis Bacon", # 16th
		"Robert Boyle", # 17th
		"Isaac Newton", # 17th
		"David Hume", # 18th
		"William Herschel", # 18th
		iIndustrial,
		"John Dalton", # 19th
		"fMary Somerville", # 19th
		"Michael Faraday", # 19th
		"fMary Anning", # 19th
		"Charles Darwin", # 19th
		"fAda Lovelace", # 19th
		"James Clerk Maxwell", # 19th
		iGlobal,
		"Ernest Rutherford", # 20th
		"Alexander Fleming", # 20th
		"Alan Turing", # 20th
		"fRosalind Franklin", # 20th
		"Stephen Hawking", # 20th
	],
	iGreatMerchant : [
		"Alan Rufus", # 11th
		"Aaron of Lincoln", # 12th
		"William Caxton", # 15th
		iRenaissance,
		"Francis Drake", # 16th
		"William Petty", # 17th
		"James Cook", # 18th
		"Adam Smith", # 18th
		iIndustrial,
		"David Ricardo", # 18th
		"George Hudson", # 19th
		"Richard Francis Burton", # 19th
		"Thomas Sutherland", # 19th
		"Cecil Rhodes", # 19th
		iGlobal,
		"John Maynard Keynes", # 20th
	],
	iGreatEngineer : [
		"Henry Yevele", # 14th
		iRenaissance,
		"Inigo Jones", # 17th
		"Robert Hooke", # 17th
		"Christopher Wren", # 17th
		"William Adam", # 18th
		"John Harrison", # 18th
		iIndustrial,
		"James Watt", # 18th
		"George Stephenson", # 19th
		"Charles Babbage", # 19th
		"Isambard Kingdom Brunel", # 19th
		"Henry Bessemer", # 19th
		"William Thomson Kelvin", # 19th
		iGlobal,
		"John Logie Baird", # 20th
		"fVictoria Drummond", # 20th
		"Frank Whittle", # 20th
		"Tim Berners-Lee", # 20th
	],
	iGreatStatesman : [
		"Thomas Becket", # 12th
		iRenaissance,
		"William Cecil", # 16th
		"John Locke", # 17th
		"Thomas Hobbes", # 17th
		"Robert Walpole", # 18th
		"William Pitt", # 18th
		"fMary Wollstonecraft", # 18th
		iIndustrial,
		"Jeremy Bentham", # 18th
		"John Stuart Mill", # 19th
		"William Gladstone", # 19th
		"Benjamin Disraeli", # 19th
		"Robert Gascoyne-Cecil Salisbury", # 19th
		iGlobal,
		"Thomas Edward Lawrence", # 20th
		"fEmmeline Pankhurst", # 20th
		"Clement Atlee", # 20th
		"fDiana Spencer", # 20th
	],
	iGreatGeneral : [
		"William the Conqueror", # 11th
		"Richard the Lionheart", # 12th
		"Edward III", # 14th
		"fMargaret of Anjou", # 15th
		iRenaissance,
		"Oliver Cromwell", # 17th
		"John Churchill Marlborough", # 17th
		"Jeffery Amherst", # 18th
		"Horatio Nelson", # 18th
		iIndustrial,
		"John Jervis", # 18th
		"Arthur Wellesley Wellington", # 19th
		"Edmund Lyons", # 19th
		iGlobal,
		"Edmund Allenby", # 19th
		"Hugh Dowding", # 20th
		"Bernard Law Montgomery", # 20th
		"William Slim", # 20th
		"Harold Alexander", # 20th
	],
	iGreatSpy : [
		"Francis Walsingham", # 16th
		"Guy Fawkes", # 16th
		"Robert Poley", # 16th
		"fElizabeth Alkin", # 17th
		u"John André", # 18th
		"Edward Bancroft", # 18th
		iIndustrial,
		"William Wickham", # 19th
		"William Melville", # 19th
		"Mansfield Smith-Cumming", # 19th
		iGlobal,
		"Sidney Reilly", #, 20th
		"fVera Atkins", #, 20th
		"fLise de Baissac", # 20th
		"fMelita Norwood", # 20th
		"Ian Fleming", # 20th
		"Kim Philby", # 20th
	],
},
iPortugal : {
	iGreatProphet : [
		u"António de Lisboa", # 13th
		u"fIsabel de Aragão", # 14th
		iRenaissance,
		u"João de Deus", # 16th
		u"João de Brito", # 17th
		iIndustrial, 
		"fRita Lopes de Almeida", # 19th
		iGlobal, 
		"Agostinho da Silva", # 20th
	],
	iGreatArtist : [
		u"Fernão Lopes", # 15th
		u"Nuno Gonçalves", # 15th
		iRenaissance,
		u"Luís de Camões", # 16th
		u"António Ferreira", # 16th
		u"João de Barros", # 16th
		"Machado de Castro", # 18th
		iIndustrial, 
		"Antero de Quental", # 19th
		u"José Maria de Eça de Queirós", # 19th
		iGlobal,
		"Fernando Pessoa", # 20th
		u"fAmália Rodrigues", # 20th
		u"José Saramago", # 20th
	],
	iGreatScientist : [
		"Garcia de Orta", # 16th
		"Pedro Nunes", # 16th
		"Amato Lusitano", # 16th
		"Jacob de Castro Sarmento", # 18th
		iGlobal,
		"Froilano de Mello", # 20th
		"Abel Salazar", # 20th
		u"António Egas Moniz", # 20th
	],
	iGreatMerchant : [
		"Vasco da Gama", # 15th
		"Francisco de Almeida", # 15th
		"Henrique o Navegador", # 15th
		"Bartolomeu Dias", # 15th
		iRenaissance,
		u"Pedro Álvares Cabral", # 15th
		u"Fernão Pires de Andrade", # 16th
		"fGracia Mendes Nasi", # 16th
		u"Fernão Mendes Pinto", # 16th
		iIndustrial, 
		"fAntonia Ferreira", # 19th
		iGlobal, 
		u"António Champalimaud", # 20th
	],
	iGreatEngineer : [
		"Mateus Fernandes", # 15th
		iRenaissance,
		"Diogo de Arruda", # 16th
		"Diogo de Boitaca", # 16th
		u"João Antunes", # 17th
		u"Bartolomeu de Gusmão", # 18th
		iIndustrial,
		"Carlos Amarante", # 18th
		iGlobal,
		u"José Marques da Silva", # 20th
		u"Álvaro Siza Vieira", # 20th
	],
	iGreatStatesman : [
		"Henrique de Avis", # 15th
		iRenaissance,
		u"Tristão da Cunha", # 16th
		u"João o Restaurador", # 17th
		u"fLuisa de Guzmán", # 17th
		u"Alexandre de Gusmão", # 18th
		u"Sebastião José de Carvalho e Melo", # 18th
		iIndustrial,
		"Mouzinho da Silveira", # 19th
		u"António Luís de Seabra", # 19th
		iGlobal,
		"Afonso Costa", # 20th
		u"António de Oliveria Salazar", # 20th
		u"António Guterres", # 20th
	],
	iGreatGeneral : [
		"Geraldo sem Pavor", # 12th
		u"Nuno Álvares Pereira", # 14th
		u"Álvaro Vaz de Almada", # 15th
		iRenaissance,
		"Afonso de Albuquerque", # 15th
		"Matias de Albuquerque", # 17th
		iIndustrial, 
		u"António José Severim de Noronha", # 19th
		iGlobal,
		"Otelo Saraiva de Carvalho", # 20th
	],
	iGreatSpy : [
		"Roderigo Lopez", # 16th
		iGlobal,
		u"Agostinho Lourenço", # 20th
	],
},
iInca : {
	iGreatProphet : [
		"Yahuar Huacac", # 14th
		"fAsarpay", # 16th
	],
	iGreatArtist : [
		"Viracocha", # legendary
		"Ninan Cuyochi", # 16th
		"fPalla Chimpu Ocllo", # 16th
	],
	iGreatScientist : [
		"Sinchi Roca", # 12th
		"Mayta Qhapaq Inka", # 13th
		"Manqu Qhapaq", # 13th
		"Inka Roq'a", # 14th
		"Waskar Inka", # 16th
		"Titu Cusi", # 16th
	],
	iGreatMerchant : [
		"Tupaq Inka Yupanki", # 15th
		"Felipillo", # 16th
	],
	iGreatEngineer : [
		"Qhapaq Yunpanki Inka", # 14th
		"Sayri Tupaq Inka", # 16th
	],
	iGreatStatesman : [
		u"Mayta Cápac", # 14th
		iRenaissance,
		"Manco Inca Yupanqui", # 16th
		"fMama Huaco", # 16th
		u"Tápac Amaru", # 18th
	],
	iGreatGeneral : [
		"Pachakutiq Inka Yupanki", # 15th
		"Atawallpa", # 16th
		"Manqu Inka Yupanki", # 16th
		"Thupaq Amaru", # 16th
		"Chalcuchimaq", # 16th
		"Quisquis", # 16th
		iRenaissance,
		"fBartolina Sisa", # 18th
		u"Túpac Amaru", # 18th
		iIndustrial,
		"fJuana Azurduy de Padilla", # 19th
	],
},
iAztecs : {
	iGreatProphet : [
		"Tenoch", # 14th
		"Tlacateotl", # 15th
		"fPapantzin", # 15th
		"Ixtlilxochitl", # 15th
		"fYacotzin", # 16th
	],
	iGreatArtist : [
		"Cuacuauhtzin", # 15th
		"Nezahualcoyotl", # 15th
		"Xayacamach", # 15th
		"fMacuilxochitzin", # 15th
	],
	iGreatScientist : [
		"Axayacatl", # 15th
		"Ixtlilxochitl", # 16th
		"Coanacochtzin", # 16th
	],
	iGreatMerchant : [
		"Cuauhtemoc", # 16th
		"Tlacotzin", # 16th
		"fTecuichpoch Ixcaxochitzin", # 16th
	],
	iGreatEngineer : [
		"Itzcatl", # 15th
		"Tlacaelel", # 15th
		"Moquihuix", # 15th
	],
	iGreatStatesman : [
		"Acamapichtli", # 14th
		"Quaquapitzahuac", # 15th
		"Tezozomoctli", # 15th
		"Nezahualcoyotl", # 15th
		"Nezahualpilli", # 15th
	],
	iGreatGeneral : [
		"Tezozomoc", # 14th
		"Ahuitzotl", # 15th
		"Itzcoatl", # 15th
		"Maxtla", # 15th
		"Huitzilhuitl", # 15th
		"Chimalpopoca", # 15th
	],
},
iNetherlands : {
	iGreatProphet : [
		"Geert Grote", # 14th
		iRenaissance,
		"Desiderius Erasmus", # 16th
		"Menno Simons", # 16th
		"Jakob Hermanszoon", # 16th
		"Baruch Spinoza", # 17th
		iIndustrial,
		"Abraham Kuyper", # 19th
		iGlobal,
		"fAlida Bosshardt", # 20th
	],
	iGreatArtist : [
		"Hendrick de Keyser", # 16th
		"Rembrandt van Rijn", # 17th
		"Johannes Vermeer", # 17th
		"Pieter Corneliszoon Hooft", # 17th
		"fTitia Bergsma", # 18th
		iIndustrial,
		"Multatuli", # 19th
		"Vincent van Gogh", # 19th
		iGlobal,
		"Piet Mondrian", # 20th
		"Maurits Cornelis Escher", # 20th
		"fAnna Maria Geertruida Schmidt", # 20th
	],
	iGreatScientist : [
		"Willebrord Snel van Royen", # 16th
		"Christiaan Huygens", # 17th
		"Antonie van Leeuwenhoek", # 17th
		"Govert Bidloo", # 17th
		"fAnna Maria van Schurman", # 18th
		iIndustrial, 
		"Johannes Diderik van der Waals", # 19th
		"Hendrik Antoon Lorentz", # 19th
		iGlobal,
		"Jan Hendrik Oort", # 20th
		"Gerrit Pieter Kuiper", # 20th
		"Edsger Wybe Dijkstra", # 20th
		"Willem Johan Kolff", # 20th
	],
	iGreatMerchant : [
		"Willem Barentsz", # 16th
		"Cornelis de Houtman", # 16th
		"fKenau Simonsdochter Hasselaer", # 16th
		"Antony van Diemen", # 17th
		"Abel Tasman", # 17th
		"Pieter Stuyvesant", # 17th
		"Jan van Riebeeck", # 17th
		"Jan Coen", # 17th
		iIndustrial,
		"Clemens Brenninkmeijer", # 19th
		"August Kessler", # 19th
		iGlobal,
		"Jan Tinbergen", # 20th
		"Freddy Heineken", # 20th
	],
	iGreatEngineer : [
		"Simon Stevin", # 16th
		"Cornelis Corneliszoon", # 16th
		"Cornelis Drebbel", # 17th
		"Jan Leeghwater", # 17th
		"Menno van Coehoorn", # 17th
		iIndustrial,
		"Adolphe Sax", # 19th
		"Cornelis Lely", # 19th
		"Hendrik Petrus Berlage", # 19th
		"Anthony Fokker", # 19th
		iGlobal,
		"Anton Philips", # 20th
		"Gerrit Rietveld", # 20th
	],
	iGreatStatesman : [
		"Desiderius Erasmus", # 16th
		"Johan van Oldenbarnevelt", # 16th
		"Johan de Witt", # 17th
		"Adriaen van der Donck", # 17th
		"Hugo Grotius", # 17th
		"Cornelis de Graeff", # 17th
		iIndustrial,
		"Johan Thorbecke", # 19th
		"fAletta Jacobs", # 19th
		iGlobal,
		"Willem Drees", # 20th
	],
	iGreatGeneral : [
		"Maurits van Nassau", # 16th
		"Piet Pieterszoon Hein", # 16th
		"Michiel de Ruyter", # 17th
		"Frederik Hendrik", # 17th
		"Cornelis Tromp", # 17th
		iIndustrial,
		"Joannes Benedictus van Heutsz", # 19th
		"Henri Winkelman", # 20th
	],
	iGreatSpy : [
		"fSophie Harmansdochter", # 16th
		"fEtta Palm d'Aelders", # 18th
		iIndustrial,
		"fJohanna Brandt", # 19th
		"Christiaan Snouck Hurgronje", # 19th
		iGlobal,
		"fMata Hari", # 20th
		"Dirk Klop", # 20th
		u"François van 't Sant", # 20th
	],
},
iAmerica : {
	iGreatProphet : [
		"Joseph Smith", # 19th
		"fMary Baker Eddy", # 19th
		"fEllen G. White", # 19th
		"Charles Taze Russell", # 19th
		iGlobal,
		"Menachem Mendel Schneerson", # 20th
		"L. Ron Hubbard", # 20th
		"Billy Graham", # 20th
		"Malcolm Little", # 20th
	],
	iGreatArtist : [
		"Edgar Allan Poe", # 19th
		"Mark Twain", # 19th
		"fEmily Dickinson", # 19th
		"Herman Melville", # 19th
		"fMary Cassatt", # 19th
		iGlobal,
		"Howard Phillips Lovecraft", # 20th
		"Ernest Hemingway", # 20th
		"Charlie Chaplin", # 20th
		"Elvis Presley", # 20th
		"fHarper Lee", # 20th
		"Andy Warhol", # 20th
		"Miles Davis", # 20th
		"Jimi Hendrix", # 20th
	],
	iGreatScientist : [
		"Benjamin Franklin", # 18th
		"fNettie Stevens", # 19th
		iGlobal,
		"Arthur Compton", # 20th
		"Edwin Hubble", # 20th
		"John von Neumann", # 20th
		"Glenn Seaborg", # 20th
		"Robert Oppenheimer", # 20th
		"Richard Feynman", # 20th
		"fBarbara McClintock", # 20th
		"fGrace Hopper", # 20th
	],
	iGreatMerchant : [
		"Stephen Girard", # 18th
		"Nathaniel Bowditch", # 18th
		iIndustrial,
		"Cornelius Vanderbilt", # 19th
		"John D. Rockefeller", # 19th
		"Andrew Carnegie", # 19th
		"fHetty Green", # 19th
		"John Pierpont Morgan", # 19th
		iGlobal,
		"fHelena Rubinstein", # 20th
		"William Edward Boeing", # 20th
		"Walt Disney", # 20th
		"Ray Kroc", # 20th
		"Thomas Watson", # 20th
		"Sam Walton", # 20th
		"Bill Gates", # 20th
	],
	iGreatEngineer : [
		"Thomas Edison", # 19th
		"Nikola Tesla", # 19th
		"Henry Ford", # 19th
		"Charles Goodyear", # 19th
		iGlobal,
		"Orville Wright", # 20th
		"Frank Lloyd Wright", # 20th
		"fLillian Moller Gilbreth", # 20th
		"fHedy Lamarr", # 20th
		"fMargaret Hutchinson Rousseau", # 20th
	],
	iGreatStatesman : [
		"Thomas Paine", # 18th
		"Thomas Jefferson", # 18th
		"Benjamin Franklin", # 18th
		iIndustrial,
		"Andrew Jackson", # 19th
		"fSojourner Truth", # 19th
		"Frederick Douglass", # 19th
		"fVictoria Claflin Woodhull", # 19th
		"fSusan B. Anthony", # 19th
		"fJane Addams", # 19th
		iGlobal,
		"fEleanor Roosevelt", # 20th
		"George Kennan", # 20th
		"Martin Luther King", # 20th
		"Henry Kissinger", # 20th
	],
	iGreatGeneral : [
		"Andrew Jackson", # 19th
		"Winfield Scott", # 19th
		"Ulysses S. Grant", # 19th
		"Robert E. Lee", # 19th
		iGlobal,
		"John J. Pershing", # 20th
		"Dwight D. Eisenhower", # 20th
		"George Patton", # 20th
		"Douglas MacArthur", # 20th
		"Matthew Ridgway", # 20th
		"Norman Schwarzkopf", # 20th
	],
	iGreatSpy : [
		"Benjamin Tallmadge", # 18th
		"Allan Pinkerton", # 19th
		"fBelle Boyd", # 19th
		"fElizabeth Van Lew", # 19th
		iGlobal,
		"William J. Donovan", # 20th
		"J. Edgar Hoover", # 20th
		"James Jesus Angleton", # 20th
		"fVirginia Hall", # 20th
		"fElizabeth Friedman", # 20th
	],
},
iMexico : {
	iGreatProphet : [
		"Juan Diego", # 16th
		"Francisco Javier Clavijero", # 18th
		u"Cristóbal Magallanes Jara", # 19th
		iGlobal,
		u"Rafael Guízar Valencia", # 20th
		"Miguel Pro", # 20th
		"Samuel Ruiz", # 20th
		u"Javier Lozano Barragán", # 20th
	],
	iGreatArtist : [
		u"fÁngela Peralta", # 19th
		iGlobal,
		u"José Clemente Orozco", # 20th
		"Diego Rivera", # 20th
		"fFrida Kahlo", # 20th
		"Octavio Paz", # 20th
		"fRemedios Varo", # 20th
		u"fDolores del Río", # 20th
		"Pedro Infante", # 20th
		"Carlos Fuentes", # 20th
		u"Vicente Fernández", # 20th
	],
	iGreatScientist : [
		"Gabino Barreda", # 19th
		u"Lucas Alamán", # 19th
		iGlobal,
		"Manuel Sandoval Vallarta", # 20th
		"Ricardo Miledi", # 20th
		u"Mario José Molina", # 20th
		"Rodolfo Neri Vela", # 20th
	],
	iGreatMerchant : [
		u"Víctor Urquidi", # 20th
		u"Jerónimo Arango", # 20th
		"Carlos Slim", # 20th
		"Everardo Elizondo", # 20th
		u"Alberto Baillères", # 20th
		u"Emilio Azcárraga Jean", # 20th
	],
	iGreatEngineer : [
		u"José Villagrán García", # 20th
		u"Luis Barragán", # 20th
		"Juan O'Gorman", # 20th
		"Mario Pani", # 20th
		u"Pedro Ramírez Vázquez", # 20th
		"Bernardo Quintana Arrioja", # 20th
	],
	iGreatStatesman : [
		u"José María Pino Suárez", # 19th
		"Pascual Orozco", # 19th
		iGlobal,
		u"José Vasconcelos", # 20th
		"Octavio Paz", # 20th
		"fElvia Carrillo Puerto", # 20th
		"fRosario Castellanos", # 20th
		u"Alfonso García Robles", # 20th
		u"Gilberto Bosques Saldívar", # 20th
	],
	iGreatGeneral : [
		"Miguel Hidalgo", # 18th
		u"Agustín de Iturbide", # 19th
		u"fJosefa Ortiz de Domínguez", # 19th
		u"Porfirio Díaz", # 19th
		"Pancho Villa", # 19th
		"Emiliano Zapata Salazar", # 19th
	],
	iGreatSpy : [
		"fMargarita Ortega", # 19th
	],
},
iArgentina : {
	iGreatProphet : [
		"Gauchito Gil", # 19th
		iGlobal,
		"Enrique Angelelli", # 20th
		"Carlos Mugica", # 20th
		"Jorge Mario Bergoglio", # 20th
	],
	iGreatArtist : [
		u"José Hernández", # 19th
		"fLola Mora", # 19th
		iGlobal,
		"Carlos Gardel", # 20th
		"fGabriela Mistral", # 20th
		"Jorge Luis Borges", # 20th
		"Antonio Berni", # 20th
		"Daniel Barenboim", # 20th
		u"Juan José Campanella", # 20th
		"Gustavo Cerati", # 20th
	],
	iGreatScientist : [
		"Francisco Moreno", # 19th
		"Florentino Ameghino", # 19th
		iGlobal,
		"Luis Federico Leloir", # 20th
		u"László Bíró", # 20th
		u"René Favaloro", # 20th
	],
	iGreatMerchant : [
		"Juan Las Heras", # 19th
		"Otto Bemberg", # 19th
		"Ernesto Tornquist", # 19th
		iGlobal,
		u"José Ber Gelbard", # 20th
		"Roberto Alemann", # 20th
		"Jorge Wehbe", # 20th
		"Aldo Ferrer", # 20th
		"Antonio Cafiero", # 20th
	],
	iGreatEngineer : [
		"Luis Huergo", # 19th
		"Jorge Newbery", # 19th
		iGlobal,
		"Amancio Williams", # 20th
		"Livio Dante Porta", # 20th
		"Clorindo Testa", # 20th
		u"César Pelli", # 20th
	],
	iGreatStatesman : [
		"Juan Manuel de Rosas", # 19th
		"Domingo Faustino Sarmiento", # 19th
		"Estanislao Zeballos", # 19th
		iGlobal,
		"Carlos Saavedra Lamas", # 20th
		"Juan Atilio Bramuglia", # 20th
		u"fEva Perón", # 20th
		"Ernesto Guevara", # 20th
		u"fIsabel Martínez de Perón", # 20th
		"fEstela Barnes de Carlotto", # 20th
	],
	iGreatGeneral : [
		"Cornelio Saavedra", # 18th
		"Manuel Belgrano", # 18th
		u"Juan José Castelli", # 18th
		u"Martín Miguel de Güemes", # 18th
		u"José Gervasio Artigas", # 19th
		iGlobal, 
		u"Juan Carlos Onganía", # 20th
		"Jorge Rafael Videla", # 20th
		"Leopoldo Galtieri", # 20th
		"Jorge Anaya", # 20th
	],
	iGreatSpy : [
		"Emilio Eduardo Massera", # 20th
		"Guillermo Gaede", # 20th
	],
},
iColombia : {
	iGreatProphet : [
		"fLaura Montoya", # 20th
		u"Félix Restrepo Mejía", # 20th
		"Camilo Torres Restrepo", # 20th
		u"Alfonso López Trujillo", # 20th
		u"Julio Enrique Dávila", # 20th
		u"fMaría Luisa Piraquive", # 20th
		u"César Castellanos", # 20th
	],
	iGreatArtist : [
		"Jorge Isaacs", # 19th
		u"Andrés de Santa Maria", # 19th
		iGlobal,
		"Rodrigo Arenas", # 20th
		u"Álvaro Mutis", # 20th
		u"Gabriel García Márquez", # 20th
		"Fernando Botero", # 20th
		"Rafael Orozco", # 20th
		u"Rodrigo García", # 20th
		"fShakira", # 20th
	],
	iGreatScientist : [
		u"José Jéronimo Triana", # 19th
		"Julio Garavito Armero", # 19th
		iGlobal,
		u"Rodolfo Llinás", # 20th
		"Jorge Reynolds Pombo", # 20th
	],
	iGreatMerchant : [
		"James Martin Eder", # 19th
		iGlobal,
		"Julio Mario Santo Domingo", # 20th
		u"Carlos Ardila Lülle", # 20th
		"Luis Carlos Sarmiento Angulo", # 20th
		"Pablo Escobar", # 20th
	],
	iGreatEngineer : [
		u"Carlos Albán", # 19th
		iGlobal, 
		u"Carlos Raúl Villanueva", # 20th
		"Rogelio Salmona", # 20th
	],
	iGreatStatesman : [
		u"Tomás Cipriano de Mosquera", # 19th
		u"Rafael Núñez", # 19th
		iGlobal,
		u"Jorge Eliécer Gaitán", # 20th
		u"Nicolás Gómez Dávila", # 20th
		u"Mario Lanserna Pinzón", # 20th
	],
	iGreatGeneral : [
		"fAntonia Santos", # 19th
		u"Antonio Nariño", # 19th
		"Francisco de Paula Santander", # 19th
	],
	iGreatSpy :  [
		"fPolicarpa Salavarrieta", # 19th
		u"fManuela Sáenz", # 19th
	]
},
iBrazil : {
	iGreatProphet : [
		u"António Conselheiro", # 19th
		iGlobal,
		u"Hélder Câmara", # 20th
		u"fIrmã Dulce Pontes", # 20th
		"Chico Xavier", # 20th
		"Edir Macedo", # 20th
	],
	iGreatArtist : [
		"Aleijadinho", # 18th
		u"António Carlos Gomes", # 19th
		"Machado de Assis", # 19th
		iGlobal,
		"fTarsila do Amaral", # 20th
		"fCarmen Miranda", # 20th
		"Tom Jobim", # 20th
		"Romero Britto", # 20th
	],
	iGreatScientist : [
		"Oswaldo Cruz", # 19th
		"Carlos Chagas", # 19th
		iGlobal,
		"Alberto Santos-Dumont", # 20th
		"Urbano Ernesto Stumpf", # 20th
		u"Aziz Ab'Sáber", # 20th
		"Marcelo Gleiser", # 20th
	],
	iGreatMerchant : [
		"Roberto Marinho", # 20th
		"Jorge Lemann", # 20th
		"Eike Batista", # 20th
	],
	iGreatEngineer : [
		u"André Rebouças", # 19th
		iGlobal,
		u"Cândido Rondon", # 20th
		"Oscar Niemeyer", # 20th
		"Norberto Odebrecht", # 20th
	],
	iGreatStatesman : [
		u"José Bonifácio de Andrada", # 18th
		iIndustrial,
		"Rodrigo Augusto da Silva", # 19th
		u"José Paranhos", # 19th
		u"fIsabel Bragança", # 19th
		"Miguel Reale", # 19th
		iGlobal,
		"Roberto Mangabeira Unger", # 20th
	],
	iGreatGeneral : [
		u"Luís Alves de Lima e Silva", # 19th
		"Joaquim Marques Lisboa", # 19th
		u"fMaria Quitéria", # 19th
		iGlobal,
		u"João Baptista Mascarenhas de Morais", # 20th
		"Eurico Gaspar Dutra", # 20th
		"Artur da Costa e Silva", # 20th
	],
},
iCanada : {
	iGreatProphet : [
		"Ignace Bourget", # 19th
		u"André Bessette", # 20th
		iGlobal,
		"Lionel Groulx", # 20th
		"George C. Pidgeon", # 20th
		u"fRúhíyyih Khánum", # 20th
		"Marshall McLuhan", # 20th
	],
	iGreatArtist : [
		"Cornelius Krieghoff", # 19th
		u"Calixa Lavallée", # 19th
		"Tom Thomson", # 19th
		u"Émile Nelligan", # 19th
		iGlobal,
		"fLucy Maud Montgomery", # 20th
		"Lawren Harris", # 20th
		"fEmily Carr", # 20th
		"Jean-Paul Riopelle", # 20th
		"Neil Young", # 20th
		"fGabrielle Roy", # 20th
		"fAlice Munro", # 20th
	],
	iGreatScientist : [
		"John William Dawson", # 19th
		"fMaude Abbott", # 19th
		iGlobal,
		"Frederick Banting", # 20th
		"Norman Bethune", # 20th
		"Wilder Penfield", # 20th
		"Pierre Dansereau", # 20th
		"fShirley Tilghman", # 20th
		"David Suzuki", # 20th
	],
	iGreatMerchant : [
		"William McMaster", # 19th
		"Timothy Eaton", # 19th
		"Alphonse Desjardins", # 19th
		iGlobal,
		"fElizabeth Arden", # 20th
		"Max Aitken", # 20th
		"Ted Rogers", # 20th
		u"Guy Laliberté", # 20th
	],
	iGreatEngineer : [
		"Sandford Fleming", # 19th
		"William Cornelius Van Horne", # 19th
		"Alexander Graham Bell", # 19th
		"Reginald Fessenden", # 19th
		iGlobal,
		"Ernest Cormier", # 20th
		"Joseph-Armand Bombardier", # 20th
		"fElsie MacGill", # 20th
	],
	iGreatStatesman : [
		u"George-Étienne Cartier", # 19th
		"Louis Riel", # 19th
		"Henri Bourassa", # 19th
		iGlobal,
		"Lester B. Pearson", # 20th
		"fEmily Murphy", # 20th
		"fNellie McClung", # 20th
		"Tommy Douglas", # 20th
		u"René Lévesque", # 20th
		"fLouise Arbour", # 20th
	],
	iGreatGeneral : [
		"Arthur Currie", # 20th
		"Andrew McNaughton", # 20th
		"Billy Bishop", # 20th
		u"Roméo Dallaire", # 20th
	],
	iGreatSpy : [
		"William Stephenson", # 20th
		"Guy D'Artois", # 20th
		"Igor Gouzenko", # 20th
	],
},
}

setup()
