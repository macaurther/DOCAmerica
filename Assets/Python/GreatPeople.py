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
				
			lCurrentOffsets[iDigital] = len(lGreatPeople[iCiv][lTypes.index(iType)])
				
	print lGreatPeople

		
dGreatPeople = {
iCivSpain : {
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
iCivFrance : {
	iGreatProphet : [
		u"Pierre Abélard", # 12th
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
		"Jacques Monod", # 20th
		u"Benoît Mandelbrot", # 20th
	],
	iGreatMerchant : [
		u"Éloi de Noyon", # 7th
		u"fJeanne la Fouacière", # 13th
		iRenaissance,
		"Jacques Cartier", # 16th
		"Samuel de Champlain", # 17th
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
		"Henri de la Tour d'Auvergne", # 17th
		"Louis-Joseph de Montcalm", # 18th
		u"Louis-René de Latouche-Tréville", # 18th
		iIndustrial,
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
iCivEngland : {
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
		"Arthur Conan Doyle", # 19th
		iGlobal,
		"James Joyce", # 20th
		"fAgatha Christie", # 20th
		"John R. R. Tolkien", # 20th
		"John Lennon", # 20th
	],
	iGreatScientist : [
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
		"Michael Faraday", # 19th
		"fMary Anning", # 19th
		"Charles Darwin", # 19th
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
		"George Hudson", # 19th
		"Richard Francis Burton", # 19TH
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
		"Isambard Kingdom Brunel", # 19th
		"Henry Bessemer", # 19th
		"Charles Babbage", # 19th
		"fAda Lovelace", # 19th
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
		"Horatio Nelson", # 18th
		iIndustrial,
		"Arthur Wellesley Wellington", # 19th
		"Edmund Lyons", # 19th
		iGlobal,
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
#MacAurther TODO : All states great people
iCivVirginia : {
	iGreatProphet : [
		"Joseph Smith", # 19th
	],
	iGreatArtist : [
		"Edgar Allan Poe", # 19th
	],
	iGreatScientist : [
		"Benjamin Franklin", # 18th
	],
	iGreatMerchant : [
		"Cornelius Vanderbilt", # 19th
	],
	iGreatEngineer : [
		"Thomas Edison", # 19th
	],
	iGreatStatesman : [
		"Thomas Paine", # 18th
	],
	iGreatGeneral : [
		"Andrew Jackson", # 19th
	],
	iGreatSpy : [
		"Benjamin Tallmadge", # 18th
	],
},
iCivMassachusetts : {
	iGreatProphet : [
		"Joseph Smith", # 19th
	],
	iGreatArtist : [
		"Edgar Allan Poe", # 19th
	],
	iGreatScientist : [
		"Benjamin Franklin", # 18th
	],
	iGreatMerchant : [
		"Cornelius Vanderbilt", # 19th
	],
	iGreatEngineer : [
		"Thomas Edison", # 19th
	],
	iGreatStatesman : [
		"Thomas Paine", # 18th
	],
	iGreatGeneral : [
		"Andrew Jackson", # 19th
	],
	iGreatSpy : [
		"Benjamin Tallmadge", # 18th
	],
},
iCivNewHampshire : {
	iGreatProphet : [
		"Joseph Smith", # 19th
	],
	iGreatArtist : [
		"Edgar Allan Poe", # 19th
	],
	iGreatScientist : [
		"Benjamin Franklin", # 18th
	],
	iGreatMerchant : [
		"Cornelius Vanderbilt", # 19th
	],
	iGreatEngineer : [
		"Thomas Edison", # 19th
	],
	iGreatStatesman : [
		"Thomas Paine", # 18th
	],
	iGreatGeneral : [
		"Andrew Jackson", # 19th
	],
	iGreatSpy : [
		"Benjamin Tallmadge", # 18th
	],
},
iCivMaryland : {
	iGreatProphet : [
		"Joseph Smith", # 19th
	],
	iGreatArtist : [
		"Edgar Allan Poe", # 19th
	],
	iGreatScientist : [
		"Benjamin Franklin", # 18th
	],
	iGreatMerchant : [
		"Cornelius Vanderbilt", # 19th
	],
	iGreatEngineer : [
		"Thomas Edison", # 19th
	],
	iGreatStatesman : [
		"Thomas Paine", # 18th
	],
	iGreatGeneral : [
		"Andrew Jackson", # 19th
	],
	iGreatSpy : [
		"Benjamin Tallmadge", # 18th
	],
},
iCivConnecticut : {
	iGreatProphet : [
		"Joseph Smith", # 19th
	],
	iGreatArtist : [
		"Edgar Allan Poe", # 19th
	],
	iGreatScientist : [
		"Benjamin Franklin", # 18th
	],
	iGreatMerchant : [
		"Cornelius Vanderbilt", # 19th
	],
	iGreatEngineer : [
		"Thomas Edison", # 19th
	],
	iGreatStatesman : [
		"Thomas Paine", # 18th
	],
	iGreatGeneral : [
		"Andrew Jackson", # 19th
	],
	iGreatSpy : [
		"Benjamin Tallmadge", # 18th
	],
},
iCivRhodeIsland : {
	iGreatProphet : [
		"Joseph Smith", # 19th
	],
	iGreatArtist : [
		"Edgar Allan Poe", # 19th
	],
	iGreatScientist : [
		"Benjamin Franklin", # 18th
	],
	iGreatMerchant : [
		"Cornelius Vanderbilt", # 19th
	],
	iGreatEngineer : [
		"Thomas Edison", # 19th
	],
	iGreatStatesman : [
		"Thomas Paine", # 18th
	],
	iGreatGeneral : [
		"Andrew Jackson", # 19th
	],
	iGreatSpy : [
		"Benjamin Tallmadge", # 18th
	],
},
iCivNorthCarolina : {
	iGreatProphet : [
		"Joseph Smith", # 19th
	],
	iGreatArtist : [
		"Edgar Allan Poe", # 19th
	],
	iGreatScientist : [
		"Benjamin Franklin", # 18th
	],
	iGreatMerchant : [
		"Cornelius Vanderbilt", # 19th
	],
	iGreatEngineer : [
		"Thomas Edison", # 19th
	],
	iGreatStatesman : [
		"Thomas Paine", # 18th
	],
	iGreatGeneral : [
		"Andrew Jackson", # 19th
	],
	iGreatSpy : [
		"Benjamin Tallmadge", # 18th
	],
},
iCivSouthCarolina : {
	iGreatProphet : [
		"Joseph Smith", # 19th
	],
	iGreatArtist : [
		"Edgar Allan Poe", # 19th
	],
	iGreatScientist : [
		"Benjamin Franklin", # 18th
	],
	iGreatMerchant : [
		"Cornelius Vanderbilt", # 19th
	],
	iGreatEngineer : [
		"Thomas Edison", # 19th
	],
	iGreatStatesman : [
		"Thomas Paine", # 18th
	],
	iGreatGeneral : [
		"Andrew Jackson", # 19th
	],
	iGreatSpy : [
		"Benjamin Tallmadge", # 18th
	],
},
iCivNewJersey : {
	iGreatProphet : [
		"Joseph Smith", # 19th
	],
	iGreatArtist : [
		"Edgar Allan Poe", # 19th
	],
	iGreatScientist : [
		"Benjamin Franklin", # 18th
	],
	iGreatMerchant : [
		"Cornelius Vanderbilt", # 19th
	],
	iGreatEngineer : [
		"Thomas Edison", # 19th
	],
	iGreatStatesman : [
		"Thomas Paine", # 18th
	],
	iGreatGeneral : [
		"Andrew Jackson", # 19th
	],
	iGreatSpy : [
		"Benjamin Tallmadge", # 18th
	],
},
iCivNewYork : {
	iGreatProphet : [
		"Joseph Smith", # 19th
	],
	iGreatArtist : [
		"Edgar Allan Poe", # 19th
	],
	iGreatScientist : [
		"Benjamin Franklin", # 18th
	],
	iGreatMerchant : [
		"Cornelius Vanderbilt", # 19th
	],
	iGreatEngineer : [
		"Thomas Edison", # 19th
	],
	iGreatStatesman : [
		"Thomas Paine", # 18th
	],
	iGreatGeneral : [
		"Andrew Jackson", # 19th
	],
	iGreatSpy : [
		"Benjamin Tallmadge", # 18th
	],
},
iCivPennsylvania : {
	iGreatProphet : [
		"Joseph Smith", # 19th
	],
	iGreatArtist : [
		"Edgar Allan Poe", # 19th
	],
	iGreatScientist : [
		"Benjamin Franklin", # 18th
	],
	iGreatMerchant : [
		"Cornelius Vanderbilt", # 19th
	],
	iGreatEngineer : [
		"Thomas Edison", # 19th
	],
	iGreatStatesman : [
		"Thomas Paine", # 18th
	],
	iGreatGeneral : [
		"Andrew Jackson", # 19th
	],
	iGreatSpy : [
		"Benjamin Tallmadge", # 18th
	],
},
iCivDelaware : {
	iGreatProphet : [
		"Joseph Smith", # 19th
	],
	iGreatArtist : [
		"Edgar Allan Poe", # 19th
	],
	iGreatScientist : [
		"Benjamin Franklin", # 18th
	],
	iGreatMerchant : [
		"Cornelius Vanderbilt", # 19th
	],
	iGreatEngineer : [
		"Thomas Edison", # 19th
	],
	iGreatStatesman : [
		"Thomas Paine", # 18th
	],
	iGreatGeneral : [
		"Andrew Jackson", # 19th
	],
	iGreatSpy : [
		"Benjamin Tallmadge", # 18th
	],
},
iCivGeorgia : {
	iGreatProphet : [
		"Joseph Smith", # 19th
	],
	iGreatArtist : [
		"Edgar Allan Poe", # 19th
	],
	iGreatScientist : [
		"Benjamin Franklin", # 18th
	],
	iGreatMerchant : [
		"Cornelius Vanderbilt", # 19th
	],
	iGreatEngineer : [
		"Thomas Edison", # 19th
	],
	iGreatStatesman : [
		"Thomas Paine", # 18th
	],
	iGreatGeneral : [
		"Andrew Jackson", # 19th
	],
	iGreatSpy : [
		"Benjamin Tallmadge", # 18th
	],
},
iCivAmerica : {
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
iCivCanada : {
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
