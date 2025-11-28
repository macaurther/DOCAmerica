from Consts import *

# Peak that change to hills during the game, like Bogota
lPeakExceptions = []
	
### Capitals ### - MacAurther: The area where a civilization spawns

dCapitals = CivDict({
iMaya :			 (34, 65), # Tikal
iZapotec :		 (28, 64), # Danibaan
iTeotihuacan :	 (25, 69), # Teotihuacan
iTiwanaku :		 (52, 32), # Tiwanaku
iWari :			 (45, 39), # Huari
iMississippi :	 (32, 87), # Cahokia
iMuisca :		 (48, 50), # Bacata
iNorse :		 (64, 117), # Reykjavik
iChimu :		 (41, 41), # Chan Chan
iPueblo :		 (20, 83), # Chaco Canyon
iPurepecha :	 (20, 69), # Tzintzuntzan
iInuit :		 (9, 118), # North Alaska
iInca :			 (48, 35), # Cuzco
iAztec :		 (24, 67), # Tenochtitlan
iHaudenosaunee : (45, 93), # Onondaga
iSpain :		 (58, 66), # Santo Domingo
iPortugal :		 (69, 26), # Sao Paulo
iEngland :		 (45, 86), # Jamestown
iFrance :		 (49, 99), # Quebec
iNetherlands :	 (48, 91), # New Amsterdam
iLakota :		 (30, 95), # Southern Minnesota
iHawaii :		 (15, 48), # Hilo
iRussia :		 (11, 108), # Novo-Arkhangelsk
iAmerica :		 (46, 90), # Philadelphia
iHaiti :		 (54, 67), # Port-au-Prince
iArgentina :	 (58, 15), # Buenos Aires
iMexico :		 (24, 67), # Mexico City
iColombia :		 (48, 50), # Bogota
iPeru :			 (44, 36), # Lima
iBrazil :		 (73, 27), # Rio de Janeiro
iVenezuela :	 (55, 58), # Caracas
iCanada :		 (44, 97), # Ottawa
})

dPeriodCapitals = {
}

# new capital locations if changed during the game
dNewCapitals = CivDict({
})

# new capital locations on respawn
dRespawnCapitals = CivDict({
})

### Birth Area ### - MacAurther: The area that flips to a civ on spawn

dBirthArea = CivDict({
iMaya :		    ((33, 64),	(35, 66)),
iZapotec :		((27, 63),	(29, 65)),
iTeotihuacan :  ((24, 68),	(26, 70)),
iTiwanaku :	    ((51, 31),	(53, 33)),
iWari :		    ((44, 37),	(46, 42)),
iMississippi :  ((31, 84),	(36, 88)),
iMuisca :		((47, 49),	(49, 54)),
iNorse :		((61, 117),	(65, 120)),
iChimu :		((40, 39),	(42, 43)),
iPueblo :		((18, 80),	(21, 86)),
iPurepecha :	((18, 66),	(21, 70)),
iInuit :		((7, 117),	(15, 120)),
iInca :		    ((46, 34),	(49, 37)),
iAztec :		((23, 66),	(25, 68)),
iHaudenosaunee :((43, 92),	(46, 94)),
iSpain :		((57, 65),	(59, 67)),
iPortugal :	    ((68, 25),	(70, 27)),
iEngland :	    ((44, 85),	(46, 87)),
iFrance :		((48, 98),	(50, 100)),
iNetherlands :  ((47, 90),	(49, 92)),
iLakota :		((26, 93),	(31, 97)),
iHawaii :		((12, 46),	(15, 50)),
iRussia :		((10, 107),	(12, 109)),
iAmerica :	    ((40, 80),	(51, 97)),
iHaiti :		((52, 66),	(55, 68)),
iArgentina :	((50, 13),	(59, 19)),
iMexico :		((18, 63),	(29, 70)),
iColombia :	    ((44, 48),	(50, 59)),
iPeru :		    ((40, 32),	(47, 42)),
iBrazil :		((61, 17),	(75, 31)),
iVenezuela :	((48, 56),	(60, 59)),
iCanada :		((37, 93),	(56, 102)),
})

dExtendedBirthArea = CivDict({
})

dBirthAreaExceptions = CivDict({
iHaudenosaunee :[(43, 94)],
iAmerica :	    [(40, 83), (40, 84), (40, 85), (40, 86), (40, 88), (40, 89), (40, 90), (40, 91), (40, 93), (40, 94), (40, 96), (40, 97), (41, 84), (41, 85), (41, 86), (41, 87), (41, 89), (41, 90), (41, 91), (41, 93), (41, 94), (41, 95), (41, 96), (41, 97), (42, 85), (42, 86), (42, 87), (42, 88), (42, 90), (42, 91), (42, 93), (42, 94), (42, 95), (42, 96), (42, 97), (43, 87), (43, 88), (43, 89), (43, 90), (43, 91), (43, 92), (43, 94), (43, 95), (43, 96), (43, 97), (44, 89), (44, 90), (44, 91), (44, 92), (44, 95), (44, 96), (44, 97), (45, 91), (45, 92), (45, 93), (45, 95), (45, 96), (45, 97), (46, 93), (46, 94), (46, 96), (46, 97), (47, 92), (47, 93), (47, 94), (47, 95), (47, 97), (48, 94), (48, 95), (48, 96), (49, 96), (49, 97), (51, 97)],
iArgentina :    [(59, 16), (59, 17), (59, 18)],
iColombia :     [(48, 55), (48, 56), (48, 57), (48, 58), (48, 59), (49, 54), (49, 55), (49, 56), (50, 54), (50, 55), (50, 56), (50, 57), (50, 58)],
iPeru :         [(44, 40), (44, 41), (44, 42), (45, 37), (45, 39), (45, 40), (45, 41), (45, 42), (46, 35), (46, 36), (46, 37), (46, 38), (46, 39), (46, 40), (46, 41), (46, 42), (47, 35), (47, 36), (47, 37), (47, 38), (47, 39), (47, 40), (47, 41), (47, 42)],
iVenezuela :    [(48, 59)],
iBrazil :       [(61, 17), (61, 18), (61, 21), (61, 22), (61, 23), (61, 24), (61, 25), (61, 26), (61, 27), (61, 28), (61, 29), (61, 30), (61, 31), (62, 17), (62, 21), (62, 22), (62, 23), (62, 24), (62, 25), (62, 26), (62, 27), (62, 28), (62, 29), (62, 30), (62, 31), (63, 22), (63, 23), (63, 24), (63, 25), (63, 26), (63, 27), (63, 28), (63, 29), (63, 30), (63, 31), (64, 26), (64, 27), (64, 28), (64, 29), (64, 30), (64, 31), (65, 27), (65, 28), (65, 29), (65, 30), (65, 31), (66, 29), (66, 30), (66, 31), (67, 30), (67, 31), (68, 31)],
iCanada :       [(37, 93), (37, 94), (37, 95), (38, 93), (38, 94), (39, 93), (45, 93), (46, 93), (46, 94), (47, 93), (47, 94), (48, 93), (48, 94), (48, 95), (49, 93), (49, 94), (49, 95), (50, 95), (50, 96), (50, 97), (51, 95), (51, 96), (56, 102)],
}, [])

dExtendedBirthAreaExceptions = CivDict({
}, [])

### Core Area ### - MacAurther: The core area of a civ

dCoreArea = CivDict({
iMaya :		    ((32, 64),	(36, 66)),
iZapotec :		((27, 63),	(29, 65)),
iTeotihuacan :  ((25, 69),	(25, 69)),
iTiwanaku :	    ((52, 32),	(52, 32)),
iWari :		    ((44, 39),	(45, 40)),
iMississippi :  ((31, 83),	(36, 88)),
iMuisca :		((48, 50),	(49, 53)),
iNorse :		((0, 0), 	(0, 0)),	# No core for Europeans
iChimu :		((40, 41),	(42, 43)),
iPueblo :		((19, 82),	(21, 86)),
iPurepecha :	((19, 68),	(21, 69)),
iInuit :		((7, 117),	(15, 120)),
iInca :		    ((46, 34),	(49, 37)),
iAztec :		((24, 67),	(24, 67)),
iHaudenosaunee :((43, 92),	(46, 94)),
iSpain : 		((0, 0), 	(0, 0)),	# No core for Europeans
iPortugal : 	((0, 0), 	(0, 0)),	# No core for Europeans
iEngland : 		((0, 0), 	(0, 0)),	# No core for Europeans
iFrance : 		((0, 0), 	(0, 0)),	# No core for Europeans
iNetherlands :	((0, 0), 	(0, 0)),	# No core for Europeans
iLakota :		((27, 94),	(30, 97)),
iHawaii :		((12, 46),	(15, 50)),
iRussia :		((0, 0), 	(0, 0)),	# No core for Europeans
iAmerica :	    ((45, 88),	(50, 94)),
iHaiti :		((52, 66),	(55, 68)),
iArgentina :	((53, 12),	(59, 18)),
iMexico :		((18, 63),	(29, 70)),
iColombia :	    ((45, 49),	(48, 58)),
iPeru :		    ((43, 32),	(47, 37)),
iBrazil :		((67, 25),	(75, 31)),
iVenezuela :	((50, 57),	(60, 59)),
iCanada :		((40, 93),	(50, 99)),
})

dCoreAreaExceptions = CivDict({
iMississippi :  [(31, 83), (31, 84), (31, 85), (32, 83), (32, 84), (32, 85), (33, 83), (33, 84), (35, 88), (36, 88)],
iHaudenosaunee :[(43, 94)],
iAmerica :	    [(45, 91), (45, 92), (45, 93), (46, 93), (46, 94), (47, 94)],
iArgentina :    [(59, 16), (59, 17), (59, 18)],
iColombia :     [(47, 56), (47, 57), (47, 58), (48, 56), (48, 57), (48, 58)],
iPeru :		    [(45, 37), (46, 35), (46, 36), (46, 37), (47, 35), (47, 36), (47, 37)],
iCanada :		[(45, 93), (46, 93), (46, 94), (47, 93), (47, 94), (48, 93), (48, 94), (48, 95), (49, 93), (49, 94), (49, 95), (50, 95), (50, 96), (50, 97)],
}, [])
# MacAurther TODO: America core expansion
dPeriodCoreArea = {
iLakota :		((24, 92),	(28, 98)),
iAmerica :	    ((39, 80),	(51, 97)),
}

dPeriodCoreAreaExceptions = appenddict({
iAmerica :	    [(39, 97), (40, 93), (40, 94), (40, 96), (40, 97), (41, 93), (41, 94), (41, 95), (41, 96), (41, 97), (42, 93), (42, 94), (42, 95), (42, 96), (42, 97), (43, 94), (43, 95), (43, 96), (43, 97), (44, 95), (44, 96), (44, 97), (45, 95), (45, 96), (45, 97), (46, 96), (46, 97), (47, 95), (47, 97), (48, 96), (49, 96), (49, 97), (51, 97)],
})

### Respawn area ### - The area a civ respawns into

dRespawnArea = CivDict({
})

dRespawnAreaExceptions = CivDict({
}, [])

dHomelandDefaultUnitSpawn = dict({
    iHomelandNorthEurope : (68, 93),
    iHomelandSouthEurope : (71, 73),
    iHomelandAfrica : (82, 53),
    iHomelandSiberia : (0, 102),
    iHomelandAsia : (0, 63),
})