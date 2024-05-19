### Areas ###

# Colonists
# The first tuple is where the player will spawn, the second is where the AI will spawn
#  Norse
tColonistReykjavik = 	((58, 117), (55, 114))
#  Spain
tColonistCaribbean = 	((47, 57), (40, 54))
tColonistCuba = 		((37, 62), (30, 62))
tColonistBermuda = 		((40, 69), (32, 70))
tColonistArgentina = 	((30, 5), (23, 10))
#  Portugal
tColonistBrazil1 = 		((42, 11), (38, 16))
tColonistBrazil2 = 		((58, 21), (55, 24))
#  England
tColonistVirginia = 	((46, 77), (38, 77))
tColonistMassachusetts = ((36, 51), (44, 85))
tColonistNovaScotia = 	((56, 85), (49, 87))
tColonistCarolina = 	((44, 71), (36, 73))
tColonistPennsylvania = ((44, 79), (40, 81))
#  France
tColonistQuebec = 		((55, 95), (46, 92)) #(x2)
tColonistLouisiana = 	((27, 67), (25, 72))
#  Netherlands
tColonistNewNetherlands =((49, 79), (42, 83))
tColonistSuriname = 	((52, 45), (47, 40))
#  Russia
tColonistAlaska = 		((4, 106), (12, 108))
# Companies

# Congresses

# Revolutions/Expeditionaries
tExpeditionaryAmerica =		(44, 85)	# Boston
tExpeditionaryHaiti = 		(37, 55)	# Port au Prince
tExpeditionaryArgentina = 	(23, 10)	# Buenos Aires
tExpeditionaryMexico = 		(17, 63)	# Caribbean Coast
tExpeditionaryColombia = 	(32, 49)	# Caribbean Coast
tExpeditionaryPeru = 		(20, 32)	# Lima

# DynamicCivs

# Tribe respawns
tTribeRespawnArea =			((5, 5), (51, 112))

# Religions
tHolyCity = (58, 0)	# MacAurther: faux city to be the Holy City for all old world religions (in the bottom left of the map surrounded by peaks)

## Victory

# first Mississippi goal: Control the Mississippi and Ohio Rivers by 500 AD
tMississippiRiver = ((27, 79), (29, 85))
lMississippiRiverAdditional = [
(27, 91), (28, 91), 
(27, 90), (29, 90), 
(28, 89), (30, 89), 
(28, 88), (30, 88), 
(28, 87), (30, 87), 
(28, 86), (30, 86), 
(26, 79), 
(25, 78), (27, 78), 
(24, 77), (26, 77), 
(24, 76), (26, 76), 
(23, 75), (25, 75), 
(24, 74), (26, 74), 
(24, 73), (26, 73), 
(25, 72), 
]

tOhioRiver = ((29, 80), (35, 82))
lOhioRiverExceptions = [(32, 80), (35, 80)]
lOhioRiverAdditional = [(32, 83), (35, 83)]

# second Norse goal: Settle Vinland by 1100 AD
tVinland = ((52, 92), (55, 95))
# third Norse goal: Settle Delaware by 1640 AD
tDelaware = ((39, 79), (40, 82))

# first Inuit goal: Settle Kivalliq (Western Hudson Bay), Qikiqtaaluk (Baffin Island), Nunavik (Eastern Hudson Bay), and Kalaallit (Greenland) by 1100 AD
tKivalliq = ((31, 98), (34, 103))
tQikiqtaaluk = ((35, 104), (43, 111))
lQikiqtaalukExceptions = [(36, 104), (35, 106), (36, 106), (36, 107)]
tNunavik = ((39, 96), (40, 100))

# first Incan goal: build five Tambos and a road along the Andean coast by 1500 AD
lAndeanCoast = [(15, 16), (16, 17), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (23, 24), (23, 25), (24, 26), (23, 27), (21, 29), (20, 30), (21, 31), (20, 32), (20, 33)]

# third Iroquois goal: control the Great Lakes in 1750 AD
tLakeSuperior = ((30, 90), (35, 93))
lLakeSuperiorExceptions = [(35, 93), (30, 90), (32, 90)]
lLakeSuperiorAdditional = [(29, 92), (33, 94)]
tLakeMichigan = ((31, 86), (33, 89))
lLakeMichiganExceptions = [(31, 89)]
lLakeMichiganAdditional = [(32, 85), (34, 88)]
tLakeHuron = ((35, 87), (37, 90))
lLakeHuronExceptions = [(37, 87), (37, 90)]
lLakeHuronAdditional = [(34, 87)]
tLakeErie = ((35, 84), (37, 86))
lLakeErieAdditional = [(34, 85)]
tLakeOntario = ((38, 85), (40, 87))
lLakeOntarioExceptions = [(40, 85)]
lLakeOntarioAdditional = [(39, 88)]

# first Canadian goal: connect your capital to an Atlantic and a Pacific port by 1920 AD
lAtlanticCoast = [
(48, 86), (49, 87), (50, 87), (51, 88), 
(47, 88), (48, 88), (48, 89), (49, 89), (49, 90), (48, 91), (49, 92),
(49, 94), (50, 94), (51, 94), (51, 95), (52, 95), (52, 96), (51, 96), 
(52, 96), (50, 97), (49, 97), (49, 98), (48, 98), (48, 99), (48, 100), 
]
lPacificCoast = [(10, 102), (11, 103), (12, 102), (11, 104), (10, 105), ]

### Tiles ###
tTenochtitlan = (13, 64)
tCahokia = (28, 84)
tNewAmsterdam = (42, 83)