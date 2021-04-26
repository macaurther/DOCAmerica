# coding: utf-8

from CvPythonExtensions import *
from Consts import *
from RFCUtils import utils

gc = CyGlobalContext()
localText = CyTranslator()

lTypes = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral, iGreatSpy]

lGreatPeople = [[[] for j in lTypes] for i in range(iNumCivilizations)]
lOffsets = [[[0 for i in range(iNumEras)] for j in lTypes] for i in range(iNumCivilizations)]

def testunit(iPlayer, iUnit):
	unit = gc.getPlayer(iPlayer).initUnit(utils.getUniqueUnit(iPlayer, iUnit), 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	print getName(unit)
	
def create(iPlayer, iUnit, (x, y)):
	gc.getPlayer(iPlayer).createGreatPeople(utils.getUniqueUnit(iPlayer, iUnit), True, True, x, y)

def getAlias(iCiv, iType, iEra):

	return iCiv
	
def getType(iUnit):
	iUnitType = utils.getBaseUnit(iUnit)
	if iUnitType in lTypes: return lTypes.index(iUnitType)
	return -1

def getAvailableNames(iPlayer, iType):
	pPlayer = gc.getPlayer(iPlayer)
	iEra = pPlayer.getCurrentEra()
	iCiv = getAlias(pPlayer.getCivilizationType(), iType, iEra)
	
	return getEraNames(iCiv, iType, iEra)

def getEraNames(iCiv, iType, iEra):
	lNames = lGreatPeople[iCiv][iType]
	
	iOffset = lOffsets[iCiv][iType][iEra]
	iNextOffset = len(lNames)
	if iEra + 1 < iNumEras: iNextOffset = lOffsets[iCiv][iType][iEra+1]
	
	iSpread = max(iNextOffset - iOffset, min(iEra+2, 5))
	
	lBefore = [sName for sName in lNames[:iOffset] if not gc.getGame().isGreatPersonBorn(sName)]
	lAfter = [sName for sName in lNames[iOffset:] if not gc.getGame().isGreatPersonBorn(sName)]
	
	if len(lAfter) >= iSpread:
		return lAfter[:iSpread]
	
	iSpread -= len(lAfter)
	return lBefore[-iSpread:] + lAfter
	
def getName(unit):
	iType = getType(unit.getUnitType())
	if iType < 0: return None
	
	lAvailableNames = getAvailableNames(unit.getOwner(), iType)
	if not lAvailableNames: return None
	
	return utils.getRandomEntry(lAvailableNames)
	
def onGreatPersonBorn(unit, iPlayer, city, bAnnounceBirth = True):
	sName = getName(unit)
	if sName:
		gc.getGame().addGreatPersonBornName(sName)
		
		# Leoreth: replace graphics for female GP names
		if sName[0] == "f":
			sName = sName[1:]
			unit = utils.replace(unit, dFemaleGreatPeople[utils.getBaseUnit(unit.getUnitType())])
			
		unit.setName(sName)
		
	# Leoreth: display notification
	if bAnnounceBirth:
		if iPlayer not in [iIndependent, iIndependent2, iBarbarian]:
			pDisplayCity = city
			if pDisplayCity.isNone(): pDisplayCity = gc.getMap().findCity(unit.getX(), unit.getY(), PlayerTypes.NO_PLAYER, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
				
			sCity = "%s (%s)" % (pDisplayCity.getName(), gc.getPlayer(pDisplayCity.getOwner()).getCivilizationShortDescription(0))
			sMessage = localText.getText("TXT_KEY_MISC_GP_BORN", (unit.getName(), sCity))
			sUnrevealedMessage = localText.getText("TXT_KEY_MISC_GP_BORN_SOMEWHERE", (unit.getName(),))
			
			if city.isNone(): sMessage = localText.getText("TXT_KEY_MISC_GP_BORN_OUTSIDE", (unit.getName(), sCity))
		
			for iLoopPlayer in range(iNumPlayers):
				if gc.getPlayer(iLoopPlayer).isAlive():
					if unit.plot().isRevealed(gc.getPlayer(iLoopPlayer).getTeam(), False):
						CyInterface().addMessage(iLoopPlayer, False, iDuration, sMessage, "AS2D_UNIT_GREATPEOPLE", InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, unit.getButton(), ColorTypes(gc.getInfoTypeForString("COLOR_UNIT_TEXT")), unit.getX(), unit.getY(), True, True)
					else:
						CyInterface().addMessage(iLoopPlayer, False, iDuration, sUnrevealedMessage, "AS2D_UNIT_GREATPEOPLE", InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, "", ColorTypes(gc.getInfoTypeForString("COLOR_UNIT_TEXT")), -1, -1, False, False)

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
				
			lCurrentOffsets[iInformationEra] = len(lGreatPeople[iCiv][lTypes.index(iType)])
				
	print lGreatPeople

	
	
# DoC USA Methodology:
# Great Prophets:
#	Preachers, Religious Leaders, Spiritual People
# Great Artists:
#	Writers, Painters, Artists, Musicians, Actors, Directors
# Great Scientists:
#	Teachers, People who contributed to knowledge, Civil Rights activists
# Great Merchants:
#	Businesspeople, CEOs, Economists, Advertisers, Brand Names
# Great Engineers:
#	People who contributed to how things are made, Inventors, Astronauts
# Great Statesmen:
#	Politicians, Judges, Presidents, Governors, Congresspeople
# Great Generals:
#	Generals, Admirals, Military Leaders
# Great Spies:
# 	Spies, Explorers, Underground railroad

dGreatPeople = {
iCivSpain : {
	iGreatProphet : [
		"Juan de Ortega", # 11th
		u"Domingo de Guzmán", # 12th
		iRevolutionaryEra,
		"Ignacio de Loyola", # 16th
		u"Juan de Sepúlveda", # 16th
		u"fTeresa de Ávila", # 16th
		u"Francisco Suárez", # 16th
		u"Bartolomé de Las Casas", # 16th
		iIndustrialEra,
		u"Junípero Serra", # 18th
		"fJoaquima de Vedruna", # 19th
		iAtomicEra, 
		u"Josemaría Escrivá", # 20th
	],
	iGreatArtist : [
		"Gonzalo de Berceo", # 13th
		"Juan Manuel", # 14th
		iRevolutionaryEra,
		"Miguel de Cervantes", # 16th
		"Garcilaso de la Vega", # 16th
		"Lope de Vega", # 17th
		u"Diego de Silva Velázquez", # 17th
		u"fJuana Inés de la Cruz", # 17th
		"Francisco de Goya", # 18th
		iIndustrialEra,
		u"fGertrudis Gómez de Avellaneda", # 19th
		u"Gustavo Adolfo Bécquer", # 19th
		u"fRosalía de Castro", # 19th
		u"Isaac Albéniz", # 19th
		u"Benito Pérez Galdós", # 19th
		iAtomicEra,
		"Pablo Picasso", # 20th
		u"Joan Miró", # 20th
		u"Luis Buñuel", # 20th
		u"Salvador Dalí", # 20th
	],
	iGreatScientist : [
		"Gerardo de Cremona", # 12th
		"Yehuda ben Moshe", # 13th
		"Ramon Llull", # 13th
		iRevolutionaryEra,
		"Miguel Serveto", # 16th
		u"Carlos de Sigüenza y Góngora", # 17th
		"Antonio de Ulloa", # 18th
		iIndustrialEra,
		u"José Celestino Mutis", # 18th
		u"Santiago Ramón y Cajal", # 19th
		iAtomicEra, 
		"Severo Ochoa", # 20th
	],
	iGreatMerchant : [
		u"Cristóbal Colón", # 15th
		"Fernando de Magallanes", # 15th
		u"Martín de Azpilcueta", # 16th
		"Hernando de Soto", # 16th
		u"José Penso de la Vega", # 17th
		iIndustrialEra,
		"Salvador Fidalgo", # 18th
		iAtomicEra,
		"Juan March Ordinas", # 20th
		"Amancio Ortega", # 20th
	],
	iGreatEngineer : [
		"Juan Bautista de Toledo", # 16th
		"Juan de Herrera", # 16th
		iIndustrialEra,
		u"Agustín de Betancourt", # 18th
		"Alberto de Palacio y Elissague", # 19th
		"Esteban Terradas i Illa", # 19th
		u"Antoni Gaudí", # 19th
		iAtomicEra,
		"Leonardo Torres y Quevedo", # 20th
		"Juan de la Cierva", # 20th
	],
	iGreatStatesman : [
		"Alfonso el Sabio", # 13th
		iRevolutionaryEra,
		u"Francisco Jiménez de Cisneros", # 15th
		"Francisco de Vitoria", # 16th
		iIndustrialEra,
		u"José de Gálvez", # 18th
		u"José Moniño", # 18th
		"Juan Prim", # 19th
		iAtomicEra, 
		u"Lluís Companys", # 20th
		u"fDolores Ibárruri", # 20th
	],
	iGreatGeneral : [
		"El Cid", # 11th
		"Alfonso el Bravo", # 11th
		"Jaume el Conqueridor", # 13th
		iRevolutionaryEra,
		"Francisco Coronado", # 16th
		u"Hernán Cortés", # 16th
		"Francisco Pizarro", # 16th
		u"Álvaro de Bazán", # 16th
		u"fMaría Pacheco", # 16th
		u"Fernando Álvarez de Toledo", # 16th
		u"Ambrosio Spínola Doria", # 17th
		u"Bernardo de Gálvez", # 18th
		iIndustrialEra, 
		u"fAgustina de Aragón", # 19th
		"Fernando Villaamil", # 19th
		iAtomicEra, 
		"Emilio Mola", # 20th
		"Vicente Rojo Lluch", # 20th
		"Mohamed ben Mizzian", # 20th
	],
	iGreatSpy : [
		u"Tomás de Torquemada", # 15th
		"Bernardino de Mendoza", # 17th
		u"fManuela Desvalls Vergós", # 18th
		"Ali Bey el Abbassi", # 18th 
		iAtomicEra,
		u"Juan Pujol García", # 20th
		u"Ramón Mercader", # 20th
	],
},
iCivFrance : {
	iGreatProphet : [
		u"Pierre Abélard", # 12th
		"Louis IX", # 13th
		"fJeanne d'Arc", # 15th
		iRevolutionaryEra,
		"Jean Calvin", # 16th
		"Vincent de Paul", # 17th
		"fJeanne Mance", # 17th
		"fMarguerite Bourgeoys", # 17th
		u"Jacques-Bénigne Bossuet", # 17th
		iIndustrialEra,
		u"fThérèse de Lisieux", # 19th
		"Auguste Comte", # 19th
		iAtomicEra,
		"Albert Schweitzer", # 20th
		u"Marcel Légaut", # 20th
		u"Henri Grouès", # 20th
	],
	iGreatArtist : [
		u"Pérotin", # 12th
		u"Chrétien de Troyes", # 12th
		"fChristine de Pizan", # 15th
		"Jean Fouquet", # 15th
		iRevolutionaryEra,
		u"François Rabelais", # 16th
		"Charles Le Brun", # 17th
		"Jean-Baptiste Lully", # 17th
		"Jean Racine", # 17th
		u"Molière", # 17th
		"Antoine Watteau", # 18th
		"Voltaire", # 18th
		u"fÉlisabeth Vigée Le Brun", # 18th
		iIndustrialEra,
		u"Honoré de Balzac", # 19th
		"Alexandre Dumas", # 19th
		"Victor Hugo", # 19th
		"fGeorge Sand", # 19th
		"Charles Baudelaire", # 19th
		"Auguste Rodin", # 19th
		"Claude Monet", # 19th
		"Claude Debussy", # 19th
		iAtomicEra,
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
		iRevolutionaryEra,
		"Marin Mersenne", # 17th
		u"René Descartes", # 17th
		"Pierre de Fermat", # 17th
		"Blaise Pascal", # 17th
		"Antoine Lavoisier", # 18th
		u"fÉmilie du Châtelet", # 18th
		iIndustrialEra,
		"Pierre-Simon Laplace", # 18th
		"Georges Cuvier", # 19th
		"Louis Pasteur", # 19th
		"fMarie-Sophie Germain", # 19th
		"fMarie Curie", # 19th
		"Antoine Henri Becquerel", # 19th
		iAtomicEra,
		"Jacques Monod", # 20th
		u"Benoît Mandelbrot", # 20th
	],
	iGreatMerchant : [
		u"Éloi de Noyon", # 7th
		u"fJeanne la Fouacière", # 13th
		iRevolutionaryEra,
		"Jacques Cartier", # 16th
		"Samuel de Champlain", # 17th
		"Antoine de Lamothe-Cadillac", # 18th
		u"fThérèse de Couagne", # 18th
		iIndustrialEra,
		u"Frédéric Bastiat", # 19th
		"Ferdinand de Lesseps", # 19th
		"Louis Vuitton", # 19th
		iAtomicEra,
		"fCoco Chanel", # 20th
		"Marcel Dessault", # 20th
		"fMarie Marvingt", # 20th
	],
	iGreatEngineer : [
		"Suger", # 12th
		"Villard de Honnecourt", # 13th
		"Pierre de Montreuil", # 13th
		iRevolutionaryEra,
		u"Sébastien Le Prestre de Vauban", # 17th
		"Jules Hardouin-Mansart", # 17th
		"Claude Perrault", # 17th
		"Charles-Augustin Coulomb", # 18th
		"Joseph-Michel Montgolfier", # 18th
		iIndustrialEra,
		"Joseph Marie Jacquard", # 18th
		"Sadi Carnot", # 19th
		"Louis Daguerre", # 19th
		"Norbert Rillieux", # 19th
		"Alexandre Gustave Eiffel", # 19th
		iAtomicEra,
		u"Louis Lumière", # 20th
		"Le Corbusier", # 20th
	],
	iGreatStatesman : [
		u"fAliénor d'Aquitaine", # 12th
		"Philippe de Beaumanoir", # 13th
		iRevolutionaryEra,
		"Jean Bodin", # 16th
		"Armand Jean du Plessis de Richelieu", # 17th
		"Jean-Baptiste Colbert", # 17th
		u"fAnne-Marie-Louise d'Orléans", # 17th
		u"Charles-Maurice de Talleyrand-Périgord", # 18th
		"Montesquieu", # 18th
		"Maximilien Robespierre", # 18th
		iIndustrialEra,
		"Adolphe Thiers", # 19th
		"Alexis de Tocqueville", # 19th
		"Pierre-Joseph Proudhon", # 19th
		iAtomicEra,
		u"Léon Blum", # 20th
		"fSimone de Beauvoir", # 20th
	],
	iGreatGeneral : [
		"Charles Martel", # 8th
		"Godefroy de Bouillon", # 11th
		"fJeanne de Flandre", # 14th
		"Charles V", # 14th
		"fJeanne d'Arc", # 15th
		iRevolutionaryEra,
		u"Louis de Bourbon-Condé", # 17th
		"Henri de la Tour d'Auvergne", # 17th
		"Louis-Joseph de Montcalm", # 18th
		u"Louis-René de Latouche-Tréville", # 18th
		iIndustrialEra,
		"Louis-Nicolas Davout", # 18th
		"Joachim Murat", # 18th
		"Louis-Alexandre Berthier", # 19th
		"Gilbert de Lafayette", # 19th
		"Patrice de MacMahon", # 19th
		iAtomicEra,
		"Ferdinand Foch", # 20th
		"Joseph Joffre", # 20th
		u"Philippe Pétain", # 20th
		"Philippe Leclerc de Hauteclocque", # 20th
	],
	iGreatSpy : [
		u"Bertrandon de la Broquière", # 15th
		iRevolutionaryEra,
		"fCharlotte de Sauve", # 16th
		u"fMarie Anne de La Trémoille", # 17th
		"fCharlotte Corday", # 18th
		"Pierre Beaumarchais", # 18th
		u"Chevalier d'Éon", # 18th
		iIndustrialEra,
		"fMichelle de Bonneuil", # 19th
		"Charles Schulmeister", # 19th
		iAtomicEra,
		u"fJoséphine Baker", # 20th
		"Gilbert Renault", # 20th
	],
},
iCivEngland : {
	iGreatProphet : [
		"Bede the Venerable", # 8th
		"Anselm of Canterbury", # 11th
		"Thomas Becket", # 12th
		iRevolutionaryEra,
		"Thomas More", # 16th
		"fAnne Hutchinson", # 17th
		"John Newton", # 18th
		"William Penn", # 18th
		"Jonathan Edwards", # 18th
		"fAnn Lee", # 18th
		"John Wesley", # 18th
		iIndustrialEra,
		"William Booth", # 19th
		"David Livingstone", # 19th
		iAtomicEra,
		"Gerald Gardner", # 20th
		"Aleister Crowley", # 20th
		"John Stott", # 20th
	],
	iGreatArtist : [
		"Geoffrey Chaucer", # 14th
		"Thomas Malory", # 15th
		iRevolutionaryEra,
		"William Shakespeare", # 17th
		"John Milton", # 17th
		"John Vanbrugh", # 17th
		"George Frideric Handel", # 18th
		"fJane Austen", # 18th
		iIndustrialEra,
		"William Blake", # 18th
		"fMary Shelley", # 19th
		"Alfred Tennyson", # 19th
		"Charles Dickens", # 19th
		"Arthur Conan Doyle", # 19th
		iAtomicEra,
		"James Joyce", # 20th
		"fAgatha Christie", # 20th
		"John R. R. Tolkien", # 20th
		"John Lennon", # 20th
	],
	iGreatScientist : [
		"Robert Grosseteste", # 13th
		"Roger Bacon", # 13th
		"William of Ockham", # 14th
		iRevolutionaryEra,
		"Francis Bacon", # 16th
		"Robert Boyle", # 17th
		"Isaac Newton", # 17th
		"David Hume", # 18th
		"William Herschel", # 18th
		iIndustrialEra,
		"John Dalton", # 19th
		"Michael Faraday", # 19th
		"fMary Anning", # 19th
		"Charles Darwin", # 19th
		"James Clerk Maxwell", # 19th
		iAtomicEra,
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
		iRevolutionaryEra,
		"Francis Drake", # 16th
		"William Petty", # 17th
		"James Cook", # 18th
		"Adam Smith", # 18th
		iIndustrialEra,
		"George Hudson", # 19th
		"Richard Francis Burton", # 19TH
		"Thomas Sutherland", # 19th
		"Cecil Rhodes", # 19th
		iAtomicEra,
		"John Maynard Keynes", # 20th
	],
	iGreatEngineer : [
		"Henry Yevele", # 14th
		iRevolutionaryEra,
		"Inigo Jones", # 17th
		"Robert Hooke", # 17th
		"Christopher Wren", # 17th
		"William Adam", # 18th
		"John Harrison", # 18th
		iIndustrialEra,
		"James Watt", # 18th
		"George Stephenson", # 19th
		"Isambard Kingdom Brunel", # 19th
		"Henry Bessemer", # 19th
		"Charles Babbage", # 19th
		"fAda Lovelace", # 19th
		iAtomicEra,
		"John Logie Baird", # 20th
		"fVictoria Drummond", # 20th
		"Frank Whittle", # 20th
		"Tim Berners-Lee", # 20th
	],
	iGreatStatesman : [
		"Thomas Becket", # 12th
		iRevolutionaryEra,
		"William Cecil", # 16th
		"John Locke", # 17th
		"Thomas Hobbes", # 17th
		"Robert Walpole", # 18th
		"William Pitt", # 18th
		"fMary Wollstonecraft", # 18th
		iIndustrialEra,
		"William Gladstone", # 19th
		"Benjamin Disraeli", # 19th
		"Robert Gascoyne-Cecil Salisbury", # 19th
		iAtomicEra,
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
		iRevolutionaryEra,
		"Oliver Cromwell", # 17th
		"John Churchill Marlborough", # 17th
		"Horatio Nelson", # 18th
		iIndustrialEra,
		"Arthur Wellesley Wellington", # 19th
		"Edmund Lyons", # 19th
		iAtomicEra,
		"Hugh Dowding", # 20th
		"Bernard Law Montgomery", # 20th
		"Harold Alexander", # 20th
	],
	iGreatSpy : [
		"Francis Walsingham", # 16th
		"Guy Fawkes", # 16th
		"Robert Poley", # 16th
		"fElizabeth Alkin", # 17th
		u"John André", # 18th
		"Edward Bancroft", # 18th
		iIndustrialEra,
		"William Wickham", # 19th
		"William Melville", # 19th
		"Mansfield Smith-Cumming", # 19th
		iAtomicEra,
		"Sidney Reilly", #, 20th
		"fVera Atkins", #, 20th
		"fLise de Baissac", # 20th
		"fMelita Norwood", # 20th
		"Ian Fleming", # 20th
		"Kim Philby", # 20th
	],
},
iCivVirginia : {
	iGreatProphet : [
		iColonialEra,
		"fPocahontas", # 17th
		"Samuel Davies", # 18th
		iExpansionEra,
		"Nat Turner", # 19th
		iIndustrialEra,
		"John Jasper", # 19th
	],
	iGreatArtist : [
		iColonialEra,
		"William Byrd II", # 18th
		iExpansionEra,
		"John Randolph", # 19th
		"William McGuffey", # 19th
		iIndustrialEra,
		"John A. Elder", # 19th
		"Sir Moses Ezekiel", # 19th
		"Thomas Nelson Page", # 19th
		iModernEra,
		"William Cabell Bruce", # 20th
		"James Branch Cabell", # 20th
		"fWilla Cather", # 20th
		"fEllen Glasgow", # 20th
		"fAnn Spencer", # 20th
		"fMaybelle Carter", # 20th
		"fElla Fitzgerald", # 20th
		"fKate Smith", # 20th
		iAtomicEra,
		"Russell Baker", # 20th
		"Earl Hamner Jr.", # 20th
		"James J. Kilpatrick", # 20th
		"William Styron", # 20th
		"Tom Wolfe", # 20th
		"fPatsy Cline", # 20th
		iInformationEra,
		"David Baldacci", # 20th
	],
	iGreatScientist : [
		iColonialEra,
		"William Stith", # 18th
		iRevolutionaryEra,
		"George Wythe", # 18th
		iExpansionEra,
		"Matthew Fontaine Maury", #19th
		"Ephraim McDowell", # 19th
		"Edmund Ruffin", # 19th
		iIndustrialEra,
		"Walter Reed", # 19th
		"Booker T. Washington", # 19th
		iModernEra,
		"Virginius Dabney", # 20th
		"Douglas Southall Freeman", # 20th
		iAtomicEra,
		"David J. Mays", # 20th
	],
	iGreatMerchant : [
		iColonialEra,
		"John Rolfe", # 17th
		"Robert Carter I", # 18th
		iIndustrialEra,
		"R. J. Reynolds", # 19th
		iModernEra,
		"Carter Glass", # 20th
		"fMaggie L. Walker", # 20th
		iAtomicEra,
		"Henry. H. Fowler", # 20th
	],
	iGreatEngineer : [
		iRevolutionaryEra,
		"James Rumsey", # 18th
		iExpansionEra,
		"Cyrus McCormick", # 19th
		iModernEra,
		"Richard E. Byrd", # 20th
		iInformationEra,
		"fWendy B. Lawrence", # 21st
		"John McAfee", #21st
		"Eric Schmidt", # 21st
	],
	iGreatStatesman : [
		iColonialEra,
		"George Mason", # 18th
		"John Smith", # 18th
		"Alexander Spotswood", # 18th
		iRevolutionaryEra,
		"George Washington", # 18th
		"Thomas Jefferson", # 18th
		"Patrick Henry", # 18th
		"Richard Henry Lee", # 18th
		"Peyton Randolph", # 18th
		iExpansionEra,
		"James Madison", # 19th
		"James Monroe", # 19th
		"William Henry Harrison", # 19th
		"John Tyler", # 19th
		"Henry Clay", # 19th
		"Charles Lee", # 19th
		"John Marshall", # 19th
		iIndustrialEra,
		"Fitzhugh Lee", # 19th
		iModernEra,
		"Woodrow Wilson", # 20th
		iAtomicEra,
		"Lewis F. Powell Jr.", # 20th
		"L. Douglas Wilder", # 20th
	],
	iGreatGeneral : [
		iRevolutionaryEra,
		"George Washington", # 18th
		"George Rogers Clark", # 18th
		"Henry Lee", # 18th
		"Daniel Morgan", # 18th
		iExpansionEra,
		"James Barbour", # 19th
		"Zachary Taylor", # 19th
		"Thomas W. Gilmer", # 19th
		"John Y. Mason", # 19th
		"Winfield Scott", # 19th
		"Abel P. Upshur", # 19th
		iIndustrialEra,
		"Robert E. Lee", # 19th
		"Jubal Early", # 19th
		"A. P. Hill", # 19th
		"Thomas J. 'Stonewall' Jackson", # 19th
		"Joseph Johnston", # 19th
		"John Singleton Mosby", # 19th
		"George Pickett", # 19th
		"J. E. B. Stuart", # 19th
		iModernEra,
		"Claude A. Swanson", # 20th
		"Matthew Ridgway", # 20th
		iAtomicEra,
		"John W. Warner", # 20th
		iInformationEra,
		"John O. Marsh Jr.", # 20th
	],
	iGreatSpy : [
		iColonialEra,
		"Nathaniel Bacon", # 17th
		iRevolutionaryEra,
		"James Armistead Lafayette", # 18th
		"John Champe", # 18th
		"Philip Mazzei", # 18th
		iExpansionEra,
		"William Clark", # 19th
		"Meriwether Lewis", # 19th
		"fElizabeth Van Lew", # 19th
	],
},
iCivMassachusetts : {
	iGreatProphet : [
		iColonialEra,
		"Cotton Mather", # 17th
		iRevolutionaryEra,
		"Johnny Appleseed", # 18th
		"Crispus Attucks", # 18th
		iAtomicEra,
		"Abbie Hoffman", # 20th
	],
	iGreatArtist : [
		iExpansionEra,
		"Edgar Allan Poe", # 19th
		"Nathaniel Hawthorne", # 19th
		iIndustrialEra,
		"Emily Dickinson", # 19th
		"James Abbott McNeill Whistler", # 19th
		iModernEra,
		"fBlack Dahlia", # 20th
		"Theodore Geisel", # 20th
		"fBette Davis", # 20th
		"Buckminster Fuller", # 20th
		"E. E. Cummings", # 20th
		iAtomicEra,
		"Kurt Russell", # 20th
		"Sylvia Plath", # 20th
		"Jack Lemmon", # 20th
		"fTammy Grimes", # 20th
		"Leonard Bernstein", # 20th
		iInformationEra,
		"John Krasinski", # 21st
		"Chris Evans", # 21st
		"Mark Wahlberg", # 21st
		"John Cena", # 21st
		"Steve Carell", # 21st
		"Matt Damon", # 21st
		"fMindy Kaling", # 21st
		"fAmy Poehler", # 21st
	],
	iGreatScientist : [
		iRevolutionaryEra,
		"Benjamin Franklin", # 18th
		iExpansionEra,
		"Henry David Thoreau", # 19th
		"Ralph Waldo Emerson", # 19th
		"fSusan B. Anthony", # 19th
		"fClara Barton", # 19th
		"William Lloyd Garrison", # 19th
		"fLucretia Mott", # 19th
		iIndustrialEra,
		"W. E. B. Du Bois", # 19th
		"fAnne Sullivan", # 19th
		"Charles Sanders Peirce", # 19th
		iModernEra,
		"William Moulton Marston", # 20th
		"Will Durant", # 20th
		"fFrances Perkins", # 20th
		iAtomicEra,
		"Leonard Nimoy", # 20th		# MacAurther TODO: Easter egg with the Sputnik quote?
		"fChirlane McCray", # 20th
		"Jared Diamond", # 20th
		"A. Bartlett Giamatti", # 20th
	],
	iGreatMerchant : [
		iIndustrialEra,
		"fHetty Green", # 19th
		"William C. Durant", # 19th
		iModernEra,
		"Jesse Livermore", # 20th
		iAtomicEra,
		"Sheldon Adelson", # 20th
		"Peter Navarro", # 20th
		"Robert Kraft", # 20th
		"fEunice Kennedy Shriver", # 20th
		"Jack Welch", # 20th
		iInformationEra,
		"Rob Zombie", # 21st
		"Reed Hastings", # 21st
		"f Abigail Johnson", # 21st
		"Peter R. Orszag", # 21st
	],
	iGreatEngineer : [
		iExpansionEra,
		"Samuel Morse", # 19th
		"Eli Whitney", # 19th
		iIndustrialEra,
		"Lewis Howard Latimer", # 19th
		iModernEra,
		"Robert H. Goddard", # 20th
		"Vannevar Bush", # 20th
	],
	iGreatStatesman : [
		iRevolutionaryEra,
		"John Adams", # 18th
		"Samuel Adams", # 18th
		"John Hancock", # 18th
		"Elbridge Gerry", # 18th
		"Jonathan L. Austin", # 18th
		iExpansionEra,
		"John Quincy Adams", # 19th
		"Charles Sumner", # 19th
		"Horace Mann", # 19th
		iIndustrialEra,
		"Oliver Wendell Holmes Jr.", # 19th
		iAtomicEra,
		"John F. Kennedy", # 20th
		"George H. W. Bush", # 20th
		"Robert F. Kennedy", # 20th
		"Ted Kennedy", # 20th
		iInformationEra,
		"Michael Bloomberg", # 21st
		"Adam Schiff", # 21st
	],
	iGreatGeneral : [
		iRevolutionaryEra,
		"Henry Knox", # 18th
		"Joseph Warren", # 18th
		iExpansionEra,
		"Robert Gould Shaw", # 19th
		"Albert Pike", # 19th
		iAtomicEra,
		"Creighton Abrams", # 20th
		iInformationEra,
		"John F. Kelly", # 21st
	],
	iGreatSpy : [
		iRevolutionaryEra,
		"Paul Revere", # 18th
		"Benjamin Edes", # 18th
		"David Henley", # 18th
		"Enoch Crosby", # 18th
		"John Brown", # 18th
		iExpansionEra,
		"Albert D. Richardson", # 19th
		"Genville M. Dodge", # 19th
	],
},
iCivNewHampshire : {
	iGreatProphet : [
		iExpansionEra,
		"fMary Baker Eddy", # 19th
	],
	iGreatArtist : [
		iExpansionEra,
		"Charles Dana", # 19th
		"Horace Creeley", # 19th
		"fSarah Joesepha Hale", # 19th
		iIndustrialEra,
		"Thomas Bailey Aldrich", # 19th
		"Daniel Chester French", # 19th
		"Robert Frost", # 19th
		"Edward McDowell", # 19th
		"Augustus Saint Gaudens", # 19th
		iModernEra,
		"fAmy Beach", # 20th
		iAtomicEra,
		"Donald Hall", # 20th
		"Grace Metalious", # 20th
		iInformationEra,
		"Benjamin Champney", # 20th
		"Ray LaMontagne", # 20th
		"fJodi Picoult", # 20th
	],
	iGreatScientist : [
		
	],
	iGreatMerchant : [
		
	],
	iGreatEngineer : [
		iAtomicEra,
		"Alan B. Shepard Jr", # 20th
	],
	iGreatStatesman : [
		iColonialEra,
		"Benning Wentworth", # 18th
		iRevolutionaryEra,
		"Josiah Bartlett", # 18th
		"John Langdon", # 18th
		iExpansionEra,
		"Franklin Pierce", # 19th
		"Daniel Webster", # 19th
		"Salmon Portland Chase", # 19th
		"Isaac Hill", # 19th
		"Levi Woodbury", # 19th
		iIndustrialEra,
		"Henry Wilson", # 19th
		iModernEra,
		"Harlan Fiske Stone", # 20th
		"John Gilbert Winant", # 20th
		iAtomicEra,
		"Sherman Adams", # 20th
		"Henry Styles Bridges", # 20th
		iInformationEra,
		"David Souter", # 20th
		"John Sununu", # 20th
	],
	iGreatGeneral : [
		iRevolutionaryEra,
		"John Stark", # 18th
		"John Sullivan", # 18th
		"Matthew Thornton", # 18th
		"Meschech Weare", # 18th
	],
	iGreatSpy : [
		
	],
},
iCivMaryland : {
	iGreatProphet : [
		iModernEra,
		"Sam Shoemaker", # 20th
	],
	iGreatArtist : [
		iExpansionEra,
		"Francis Scott Key", # 19th
		iModernEra,
		"Upton Sinclair", # 20th
		"James Brown", # 20th
		"Babe Ruth", # 20th
		"H. L. Mencken", # 20th
		iAtomicEra,
		"Frank Zappa", # 20th
		"David Hasselhoff", # 20th
		"fAdrienne Rich", # 20th
		iInformationEra,
		"Ta-Nehisi Coates", # 21st
		"Kevin Clash", # 21st
	],
	iGreatScientist : [
		iColonialEra,
		"Benjamin Banneker", # 18th
		iExpansionEra,
		"Frederick Douglass", # 19th
		iIndustrialEra,
		"Matthew Henson", # 19th
		iAtomicEra,
		"John Rawis", # 20th
		"Martin Rodbell", # 20th
	],
	iGreatMerchant : [
		iExpansionEra,
		"Johns Hopkins", # 19th
		iAtomicEra,
		"David Rubenstein", # 20th
		iInformationEra,
		"Mike Rowe", # 21st
		"Shane McMahon", # 21st
		"Daneil Snyder", # 21st
	],
	iGreatEngineer : [
		iModernEra,
		"fEdith Clarke", # 20th
	],
	iGreatStatesman : [
		iRevolutionaryEra,
		"John Dickinson", # 18th
		iModernEra,
		"Alger Hiss", # 20th
		iAtomicEra,
		"Spiro Agnew", # 20th
		"Thurgood Marshall", # 20th
		"Sargent Shriver", # 20th
		iInformationEra,
		"fNancy Pelosi", # 21st
		"Michael Steele", # 21st
		"Elijah Cummings", # 21st
	],
	iGreatGeneral : [
		iAtomicEra,
		"John Bolton", # 20th
		iInformationEra,
		"Michael Flynn", # 21st
	],
	iGreatSpy : [
		iExpansionEra,
		"fHarriet Tubman", # 19th
		"John Wilkes Booth", # 19th
		iModernEra,
		"fVirginia Hall", # 20th
		"fMarguerite Harrison", # 20th
	],
},
iCivConnecticut : {
	iGreatProphet : [
		iColonialEra,
		"Jonathan Edwards", # 17th
		iRevolutionaryEra,
		"Lyman Beecher", # 19th
		iExpansionEra,
		"Henry Ward Beecher", # 19th
		"Charles Grandison Finney", # 19th
	],
	iGreatArtist : [
		iExpansionEra,
		"Harriet Beecher Stowe", # 19th
		"Tom Thumb", # 19th
		iIndustrialEra,
		"Frederick Law Olmstead", # 19th
		"fCharlotte Perkins Gilman", # 19th
		"Charles Ives", # 19th
		iModernEra,
		"fKatharine Hepburn", # 20th
		"Ernest Borgnine", # 20th
		iAtomicEra,
		"fGlenn Close", # 20th
		"Christopher Lloyd", # 20th
		"Michael Bolton", # 20th
		iInformationEra,
		"fAlexandra Breckenridge", # 21st
		"fMeg Ryan", # 21st
		"John Mayer", # 21st
		"Paul Giamatti", # 21st
	],
	iGreatScientist : [
		iRevolutionaryEra,
		"Noah Webster", # 18th
		iExpansionEra,
		"Amos Bronson Alcott", # 19th
		iModernEra,
		"Benjamin Spock", # 20th
		"fBarbara McClintock", # 20th
		"Adwin H. Land", # 20th
		"Adam Clayton Powell Jr", # 20th
		"John Hasbrouck Van Vleck", # 20th
		"Edward Calvin Kendall", # 20th
		iAtomicEra,
		"Roger Wolcott Sperry", # 20th
		"Alfred G. Gilman", # 20th
		"August Coppola", # 20th
		iInformationEra,
		"fCandace Owens", # 21st
	],
	iGreatMerchant : [
		iIndustrialEra,
		"J. P. Morgan", # 19th
		iModernEra,
		"Alfred P. Sloan", # 20th
		iAtomicEra,
		"Peter Schiff", # 20th
		"John C. Malone", # 20th
		"Lawrence Summers", # 20th
		"George Akerlof", # 20th
		iInformationEra,
		"Seth MacFarlane", # 21st
		"Paul Lieberstein", # 21st
	],
	iGreatEngineer : [
		iColonialEra,
		"John Wilkinson", # 18th
		iExpansionEra,
		"Samuel Colt", # 19th
		iModernEra,
		"John Franklin Enders", # 20th
		iAtomicEra,
		"Vint Cerf", # 20th
	],
	iGreatStatesman : [
		iRevolutionaryEra,
		"Lyman Hall", # 18th
		iModernEra,
		"Adam Clayton Powell Jr", # 20th
		iAtomicEra,
		"Ralph Nader", # 20th
		"John Lieberman", # 20th
		iInformationEra,
		"George W. Bush", # 21st
		"Paul Manafort", # 21st
	],
	iGreatGeneral : [
		iRevolutionaryEra,
		"Benedict Arnold", # 18th
		"Ethan Allen", # 18th
		iExpansionEra,
		"John Brown", # 19th
		"Gideon Welles", # 19th
		iAtomicEra,
		"Roger Stone", # 20th
	],
	iGreatSpy : [
		iRevolutionaryEra,
		"Nathan Hale", # 18th
		"Daniel Bissell", # 18th
		"Silas Deane", # 18th
		iInformationEra,
		"Andrew McCabe", # 20th
	],
},
iCivRhodeIsland : {
	iGreatProphet : [
		iRevolutionaryEra,
		"fJemima Wilkinson", # 18th
	],
	iGreatArtist : [
		iIndustrialEra,
		"George M. Cohan", # 19th
		iModernEra,
		"H. P. Lovecraft", # 20th
		iInformationEra,
		"fMeredith Vieira", # 21st
	],
	iGreatScientist : [
		iIndustrialEra,
		"Dana C. Munro", # 19th
	],
	iGreatMerchant : [
		
	],
	iGreatEngineer : [
		iIndustrialEra,
		"Stephen Wilcox", # 19th
	],
	iGreatStatesman : [
		
	],
	iGreatGeneral : [
		iExpansionEra,
		"Matthew C. Perry", # 19th
	],
	iGreatSpy : [
		
	],
},
iCivNorthCarolina : {
	iGreatProphet : [
		iAtomicEra,
		"Billy Graham", # 20th
	],
	iGreatArtist : [
		iIndustrialEra,
		"O. Henry", # 19th
		iModernEra,
		"fAva Gardner", # 20th
		"Thelonious Monk", # 20th
		"Tomas Clayton Wolfe", # 20th
		iAtomicEra,
		"John Coltrane", # 20th
		"fNina Simone", # 20th
		"Charlie Daniels", # 20th
		iInformationEra,
		"fEvan Rachel Wood", # 21st
		"Clay Aiken", # 20th
		"Jermaine Dupri", # 21st
	],
	iGreatScientist : [
		iIndustrialEra,
		"fAnna Julia Cooper", # 19th
		iAtomicEra,
		"Kary B. Mullis", # 20th
	],
	iGreatMerchant : [
		iIndustrialEra,
		"James Buchanan Duke", # 19th
		iAtomicEra,
		"Daniel McFadden", # 20th
		iInformationEra,
		"Vincent McMahon", # 21st
		"Rick Harrison", # 21st
	],
	iGreatEngineer : [
		iInformationEra,
		"Chris Hughes", # 21st
	],
	iGreatStatesman : [
		iExpansionEra,
		"James K. Polk", # 19th
		iIndustrialEra,
		"Andrew Johnson", # 19th
		iAtomicEra,
		"Robert Byrd", # 20th
		"fLinda McMahon", # 20th
		iInformationEra,
		"Carolyn Maloney", # 20th
	],
	iGreatGeneral : [
		iExpansionEra,
		"Braxton Bragg", # 19th
	],
	iGreatSpy : [
		iInformationEra,
		"Edward Snowden", # 21st
	],
},
iCivSouthCarolina : {
	iGreatProphet : [
		
	],
	iGreatArtist : [
		iAtomicEra,
		"fAndie MacDowell", # 20th
		iInformationEra,
		"Chadwick Boseman", # 21st
		"fViola Davis", # 20th
		"Chris Rock", # 20th
		"Aziz Ansari", # 21st
	],
	iGreatScientist : [
		iExpansionEra,
		"J. Marion Sims", # 19th
		"John Snow", # 19th
		"fAngelina Grimke", # 19th
		iModernEra,
		"fMary McLeod Bethune", # 20th
		"John B. Watson", # 20th
		"Ernest Everett Just", # 20th
		"Robert F. Furchgott", # 20th
		iAtomicEra,
		"Jesse Jackson", # 20th
		"Charles H. Townes", # 20th
	],
	iGreatMerchant : [
		iModernEra,
		"Bernard Mannes Baruch", # 20th
		iInformationEra,
		"Brian Hickerson", # 21st
	],
	iGreatEngineer : [
		iAtomicEra,
		"Joseph L. Goldstein", # 20th
		"Charles Bolden", # 20th
	],
	iGreatStatesman : [
		iRevolutionaryEra,
		"Christopher Gadsden", # 18th
		"John Rutledge", # 18th
		iExpansionEra,
		"Andrew Jackson", # 19th
		"Preston Brooks", # 19th
		iIndustrialEra,
		"Robert Smalls", # 19th
		"Benjamin R. Tillman", # 19th
		iAtomicEra,
		"Strom Thurmond", # 20th
		"John Edwards", # 20th
		iInformationEra,
		"fNikki Haley", # 21st
		"Trey Gowdy", # 20th
		"Lindsey Graham", # 21st
		"Tom Scott", # 21st
	],
	iGreatGeneral : [
		iRevolutionaryEra,
		"Francis Marion", # 18th
		iExpansionEra,
		"James Longstreet", # 19th
		"William Barret Travis", # 19th
		iAtomicEra,
		"William Childs Westmoreland", # 20th
	],
	iGreatSpy : [
		iRevolutionaryEra,
		"John Laurens", # 18th
	],
},
iCivNewJersey : {
	iGreatProphet : [
		
	],
	iGreatArtist : [
		iExpansionEra,
		"James Fenimore Cooper", # 19th
		iIndustrialEra,
		"Alfred Stieglitz", # 19th
		iModernEra,
		"Frank Sinatra", # 20th
		"Jerry Lewis", # 20th
		"Norman Lloyd", # 20th
		iAtomicEra,
		"John Travolta", # 20th
		"fMeryl Streep", # 20th
		"Bruce Springsteen", # 20th
		"Jon Bon Jovi", # 20th
		iInformationEra,
		"fWhitney Houston", # 20th
		"George R. R. Martin", # 21st
		"fJane Krakowski", # 20th
		"Danny DeVito", # 21st
		"Peter Dinklage", # 21st
	],
	iGreatScientist : [
		iIndustrialEra,
		"Nicholas Murray Butler", # 19th
		iModernEra,
		"Paul Robeson", # 20th
		"fAlice Paul", # 20th
		"fVirginia Apgar", # 20th
	],
	iGreatMerchant : [
		iAtomicEra,
		"Michael Douglas", # 20th
		"Martha Stewart", # 20th
		"Lawrence Kudlow", # 20th
		"Wilbur Ross", # 20th
		iInformationEra,
		"Shaquille O'Neal", # 20th
		"Richard Thaler", # 21st
	],
	iGreatEngineer : [
		iModernEra,
		"fAnne Morrow Lindbergh", # 20th
		iAtomicEra,
		"Buzz Aldrin", # 20th
		iInformationEra,
		"Scott Kelly", # 21st
		"Mark Kelly", # 21st
	],
	iGreatStatesman : [
		iRevolutionaryEra,
		"Aaron Burr", # 18th
		"Luther Martin", # 18th
		iIndustrialEra,
		"Grover Cleveland", # 19th
		"Garret Hobart", # 19th
		iInformationEra,
		"Jared Kushner", # 21st
	],
	iGreatGeneral : [
		iModernEra,
		"William Halsey Jr", # 20th
		iAtomicEra,
		"Norman Schwarzkopf Jr", # 20th
	],
	iGreatSpy : [
		iRevolutionaryEra,
		"John Honeyman", # 18th
		iAtomicEra,
		"Louis J. Freeh", # 20th
	],
},
iCivNewYork : {
	iGreatProphet : [
		iModernEra,
		"Menachem Mendel Schneerson", # 20th
	],
	iGreatArtist : [
		iExpansionEra,
		"Herman Melville", # 19th
		iModernEra,
		"Herman J. Mankiewicz", # 20th
		"J. D. Salinger", # 20th
		"fLucille Ball", # 20th
		"Danny Kaye", # 20th
		"Humphrey Bogart", # 20th
		"fRita Hayworth", # 20th
		"fMarion Davies", # 20th
		"Jackie Gleason", # 20th
		iAtomicEra,
		"Billy Joel", # 20th
		"Stanley Kubrick", # 20th
		"Martin Scorsese", # 20th
		"John Williams", # 20th
		"Arthur Miller", # 20th
		"fJane Fonda", # 20th
		"Stan Lee", # 20th
		"James Baldwin", # 20th
		iInformationEra,
		"fLady Gaga", # 21st
		"fScarlett Johansson", # 21st
		"Whoopi Goldberg", # 21st
		"Tom Cruise", # 21st
		"Denzel Washington", # 21st
		"fJennifer Lopez", # 21st
		"Lin-Maneul Miranda", # 21st
		"The Notorious B. I. G.", # 21st
	],
	iGreatScientist : [
		iExpansionEra,
		"fSojourner Truth", # 19th
		iAtomicEra,
		"Carl Sagan", # 20th
		"fGrace Hopper", # 20th
		"Larry King", # 20th
		"Louis Farrakhan", # 20th
		iInformationEra,
		"Neil deGrasse Tyson", # 21st
		"Anderson Cooper", # 21st
		"Chris Cuomo", # 21st
	],
	iGreatMerchant : [
		iRevolutionaryEra,
		"fElizabeth Schuyler", # 18th
		"John Jacob Astor", # 19th
		iExpansionEra,
		"Cornelius Vanderbilt", # 19th
		"Daniel Drew", # 19th
		iIndustrialEra,
		"John D. Rockefeller", # 19th
		"James Fisk", # 19th
		"Henry Morrison Flagler", # 19th
		"Jay Gould", # 19th
		"E. H. Harriman", # 19th
		"Henry Huttleston Rogers", # 19th
		iModernEra,
		"fHelena Rubinstein", # 20th
		"Thomas Watson", # 20th
		iAtomicEra,
		"Mel Brooks", # 20th
		"Phil Spector", # 20th
		"Fred Trump", # 20th
		iInformationEra,
		"Michael Jordan", # 21st
		"Jordan Belfort", # 21st
		"Alec Baldwin", # 21st
		"Mike Tyson", # 21st
		"Joss Whedon", # 21st
		"Martin Shkreli", # 21st
		"Steven Mnuchin", # 21st
	],
	iGreatEngineer : [
		iRevolutionaryEra,
		"John Stevens", # 19th
		iModernEra,
		"Richard Feynman", # 20th
		"J. Robert Oppenheimer", # 20th
		iInformationEra,
		"Mark Zuckerberg", # 21st
		"Larry Ellison", # 20th
	],
	iGreatStatesman : [
		iRevolutionaryEra,
		"Thomas Paine", # 18th
		"Alexander Hamilton", # 18th
		iExpansionEra,
		"Martin Van Buren", # 19th
		"Millard Fillmore", # 19th
		iModernEra,
		"Theodore Roosevelt", # 20th
		"Franklin Delano Roosevelt", # 20th
		"fEleanor Roosevelt", # 20th
		"Alan Dershowitz", # 20th
		iAtomicEra,
		"Henry Kissinger", # 20th
		iInformationEra,
		"fRuth Bader Ginsburg", # 21st
		"Donald Trump", # 21st
		"Bernie Sanders", # 21st
		"Douglas Emhoff", # 21st
		"fSonia Sotomayor", # 21st
		"Andrew Cuomo", # 21st
		"Ronan Farrow", # 21st
		"Bill de Blasio", # 21st
	],
	iGreatGeneral : [
		iRevolutionaryEra,
		"Henry K. Van Rensselaer", # 18th
		iModernEra,
		"John Basilone", # 20th
		iInformationEra,
		"Colin Powell", # 21st
	],
	iGreatSpy : [
		iRevolutionaryEra,
		"Benjamin Tallmadge", # 18th
		"Hercules Mulligan", # 18th
		"Abraham Woodhull", # 18th
		"James Rivington", # 18th
		iExpansionEra,
		"George Curtis", # 19th
		"fKate Warne", # 19th
		"Lafayette C. Baker", # 19th
		iModernEra,
		"William J. Donovan", # 20th
		"Sidney Mashbir", # 20th
		iInformationEra,
		"James Comey", # 21st
	],
},
iCivPennsylvania : {
	iGreatProphet : [
		iIndustrialEra,
		"Charles Taze Russell", # 19th
		iInformationEra,
		"David Miscavige", # 20th
	],
	iGreatArtist : [
		iExpansionEra,
		"Louisa May Alcott", # 19th
		iIndustrialEra,
		"fMary Cassatt", # 19th
		iModernEra,
		"fBillie Holiday", # 20th
		"James Stewart", # 20th
		"Lionel Barrymore", # 20th
		iAtomicEra,
		"Andy Warhol", # 20th
		"Fred Rogers", # 20th
		"Bob Saget", # 20th
		iInformationEra,
		"fTaylor Swift", # 21st
		"Will Smith", # 21st
		"Kevin Hart", # 21st
		"fTina Fey", # 21st
	],
	iGreatScientist : [
		iModernEra,
		"B. F. Skinner", # 20th
		"Margaret Mead", # 20th
		iAtomicEra,
		"Noam Chomsky", # 20th
	],
	iGreatMerchant : [
		iIndustrialEra,
		"Andrew Carnegie", # 19th
		"Jay Cooke", # 19th
		"Henry Clay Frick", # 19th
		"Andrew Mellon", # 19th
		"Charles M. Schwab", # 19th
		iModernEra,
		"A. S. W. Rosenbach", # 20th
		iAtomicEra,
		"Lee Iacocca", # 20th
		"David Tepper", # 20th
		iInformationEra,
		"Mark Cuban", # 21st
	],
	iGreatEngineer : [
		iRevolutionaryEra,
		"John Sellers", # 18th
		iAtomicEra,
		"Amar Bose", # 20th
	],
	iGreatStatesman : [
		iRevolutionaryEra,
		"William Bingham", # 18th
		iExpansionEra,
		"James Buchanan", # 19th
		iAtomicEra,
		"Joe Biden", # 20th
		"Ron Paul", # 20th
		iInformationEra,
		"Rand Paul", # 21st
	],
	iGreatGeneral : [
		iExpansionEra,
		"George B. McClellan", # 19th
		iModernEra,
		"George Marshall", # 20th
		"Richard Winters", # 20th
		iInformationEra,
		"H. R. McMaster", # 21st
	],
	iGreatSpy : [
		iRevolutionaryEra,
		"John Clark", # 18th
		"fLydia Darragh", # 18th
		iModernEra,
		"Eliot Ness", # 20th
		"Sylvanus Morley", # 20th
	],
},
iCivDelaware : {
	iGreatProphet : [
		iColonialEra,
		"Samuel Davies", # 18th
		iExpansionEra,
		"George David Cummins", # 19th
	],
	iGreatArtist : [
		iExpansionEra,
		"Robert Montgomery Bird", # 19th
		iIndustrialEra,
		"Howard Pyle", # 19th
		iModernEra,
		"John P. Marquand", # 20th
		iAtomicEra,
		"Clifford Brown", # 20th
		iInformationEra,
		"Aubrey Plaza", # 21st
	],
	iGreatScientist : [
		iExpansionEra,
		"Mary Ann Shadd", # 19th
		iIndustrialEra,
		"Annie Jump Cannon", # 19th
		iModernEra,
		"Joseph H. Burchenal", # 20th
		iAtomicEra,
		"Henry Heimlich", # 20th
		"Alfred D. Chandler Jr", # 20th
		"Henry Stommel", # 20th
	],
	iGreatMerchant : [
		iIndustrialEra,
		"Pierre S. du Pont", # 19th
	],
	iGreatEngineer : [
		iRevolutionaryEra,
		"Oliver Evans", # 18th
		iExpansionEra,
		"E. R. Squibb", # 19th
		iModernEra,
		"Walter McCrone", # 20th
		iAtomicEra,
		"Harry Coover", # 20th
	],
	iGreatStatesman : [
		iRevolutionaryEra,
		"Caesar Rodney", # 18th
		iExpansionEra,
		"Thomas F. Bayard", # 19th
		"John M. Clayton", # 19th
	],
	iGreatGeneral : [
		iRevolutionaryEra,
		"Jacob Jones", # 18th
		iExpansionEra,
		"Thomas Macdonough", # 19th
	],
	iGreatSpy : [
		
	],
},
iCivGeorgia : {
	iGreatProphet : [
		iModernEra,
		"Elijah Muhammad", # 20th
		iAtomicEra,
		"Martin Luther King Jr", # 20th
		iInformationEra,
		"Alan Jackson", # 20th
	],
	iGreatArtist : [
		iModernEra,
		"fMargaret Mitchell", # 20th
		iAtomicEra,
		"Jackie Robinson", # 20th
		"Ray Charles", # 20th
		"Otis Redding", # 20th
		"Claude Akins", # 20th
		iInformationEra,
		"Kanye West", # 21st
		"Laurence Fishburne", # 21st
		"fJulia Roberts", # 21st
		"fDakota Fanning", # 21st
		"Hulk Hogan", # 21st
		"Wayne Brady", # 21st
		"2 Chainz", # 21st
		"Chris Tucker", # 21st
	],
	iGreatScientist : [
		iIndustrialEra,
		"Doc Holiday", # 19th
		iModernEra,
		"Alfred Blalock", # 20th
		iAtomicEra,
		"DeForest Kelley", # 20th
		"Hosea Williams", # 20th
		iInformationEra,
		"fNancy Grace", # 21st
	],
	iGreatMerchant : [
		iIndustrialEra,
		"Asa Griggs Candler", # 19th
		iAtomicEra,
		"fLaTanya Richardson", # 20th
		iInformationEra,
		"Ben Bernanke", # 21st
		"Spike Lee", # 21st
		"Ryan Seacrest", # 21st
	],
	iGreatEngineer : [
		iModernEra,
		"George P. Burdell", # 20th
	],
	iGreatStatesman : [
		iExpansionEra,
		"Alexander Stephens", # 19th
		iAtomicEra,
		"Jimmy Carter", # 20th
		"Clarence Thomas", # 20th
		"George Wallace", # 20th
		iInformationEra,
		"fSally Yates", # 21st
		"Nathan Deal", # 21st
	],
	iGreatGeneral : [
		iIndustrialEra,
		"Henry Ossian Flipper", # 19th
	],
	iGreatSpy : [
		
	],
},
iCivAmerica : {
	iGreatProphet : [
		"Joseph Smith", # 19th
		"fEllen G. White", # 19th
		iAtomicEra,
		"L. Ron Hubbard", # 20th
		"Malcolm Little", # 20th
	],
	iGreatArtist : [
		"Mark Twain", # 19th
		iAtomicEra,
		"Ernest Hemingway", # 20th
		"Elvis Presley", # 20th
		"fHarper Lee", # 20th
		"Miles Davis", # 20th
		"Jimi Hendrix", # 20th
	],
	iGreatScientist : [
		"fNettie Stevens", # 19th
		iAtomicEra,
		"Arthur Compton", # 20th
		"Edwin Hubble", # 20th
		"Glenn Seaborg", # 20th
	],
	iGreatMerchant : [
		iAtomicEra,
		"William Edward Boeing", # 20th
		"Walt Disney", # 20th
		"Ray Kroc", # 20th
		"Sam Walton", # 20th
		"Bill Gates", # 20th
	],
	iGreatEngineer : [
		"Thomas Edison", # 19th
		"Nikola Tesla", # 19th
		"Henry Ford", # 19th
		"Charles Goodyear", # 19th
		iAtomicEra,
		"Orville Wright", # 20th
		"Frank Lloyd Wright", # 20th
		"fLillian Moller Gilbreth", # 20th
		"fHedy Lamarr", # 20th
		"fMargaret Hutchinson Rousseau", # 20th
	],
	iGreatStatesman : [
		iIndustrialEra,
		"fVictoria Claflin Woodhull", # 19th
		"fJane Addams", # 19th
		iAtomicEra,
		"George Kennan", # 20th
		"Martin Luther King", # 20th
	],
	iGreatGeneral : [
		"Ulysses S. Grant", # 19th
		iAtomicEra,
		"John J. Pershing", # 20th
		"Dwight D. Eisenhower", # 20th
		"George Patton", # 20th
		"Douglas MacArthur", # 20th
	],
	iGreatSpy : [
		"Allan Pinkerton", # 19th
		"fBelle Boyd", # 19th
		iAtomicEra,
		"J. Edgar Hoover", # 20th
		"James Jesus Angleton", # 20th
		"fElizabeth Friedman", # 20th
	],
},
iCivCanada : {
	iGreatProphet : [
		"Ignace Bourget", # 19th
		u"André Bessette", # 20th
		iAtomicEra,
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
		iAtomicEra,
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
		iAtomicEra,
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
		iAtomicEra,
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
		iAtomicEra,
		"Ernest Cormier", # 20th
		"Joseph-Armand Bombardier", # 20th
		"fElsie MacGill", # 20th
	],
	iGreatStatesman : [
		u"George-Étienne Cartier", # 19th
		"Louis Riel", # 19th
		"Henri Bourassa", # 19th
		iAtomicEra,
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
