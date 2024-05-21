from Consts import *

# Peak that change to hills during the game, like Bogota
lPeakExceptions = []
	
### Capitals ### - MacAurther: The area where a civilization spawns

dCapitals = CivDict({
iMaya :			(22, 59), # Tikal
iZapotec :		(15, 61), # Danibaan
iTeotihuacan :	(14, 66), # Teotihuacan
iTiwanaku :		(26, 25), # Tiwanaku
iWari :			(23, 33), # Huari
iMississippi :	(33, 82), # Sunwatch
iPuebloan :		(16, 86), # Chaco Canyon
iMuisca :		(31, 42), # Hunza
iNorse :		(55, 114), # Reykjavik
iChimu :		(20, 36), # Chan Chan
iInuit :		(14, 119), # North Alaska
iInca :			(24, 29), # Cuzco
iPurepecha :	(10, 68), # Tzintzuntzan
iAztecs :		(13, 64), # Tenochtitlan
iIroquois :		(39, 85), # Onondaga
iSioux :		(28, 89), # Southern Minnesota
iSpain :		(40, 54), # Santo Domingo
iPortugal :		(39, 16), # Sao Paulo
iEngland :		(38, 77), # Jamestown
iFrance :		(46, 92), # Quebec
iNetherlands :	(42, 83), # New Amsterdam
iHawaii :		(14, 49), # Hilo
iRussia :		(12, 108), # Novo-Arkhangelsk
iAmerica :		(40, 81), # Philadelphia
iHaiti :		(37, 55), # Port-au-Prince
iArgentina :	(23, 10), # Buenos Aires
iMexico :		(13, 64), # Mexico City
iColombia :		(31, 42), # Bogota
iPeru :			(20, 32), # Lima
iBrazil :		(44, 16), # Rio de Janeiro
iVenezuela :	(39, 47), # Caracas
iCanada :		(40, 89), # Ottawa
})

dPeriodCapitals = {
}

# new capital locations if changed during the game
dNewCapitals = CivDict({
})

# new capital locations on respawn
dRespawnCapitals = CivDict({
iInca :		(36, 58),	# Lima
})

### Birth Area ### - MacAurther: The area that flips to a civ on spawn

dBirthArea = CivDict({
iMaya :		    ((20, 58),	(23, 61)),
iZapotec :		((12, 60), 	(16, 62)),
iTeotihuacan :  ((12, 64),	(16, 68)),
iTiwanaku :	    ((25, 21),	(29, 26)),
iWari :		    ((20, 29),	(24, 35)),
iMississippi :  ((29, 81),	(37, 83)),
iPuebloan :		((12, 85),	(18, 88)),
iMuisca :		((29, 41),	(33, 44)),
iNorse :		((52, 114),	(57, 120)),
iChimu :		((19, 35),	(25, 41)),
iInuit :		((10, 117),	(19, 121)),
iInca :		    ((20, 27),	(27, 31)),
iPurepecha :	((8, 64),	(11, 70)),
iAztecs :		((12, 63),	(14, 65)),
iIroquois :	    ((34, 84),	(41, 87)),
iSioux :		((21, 87),	(30, 92)),
iSpain :		((39, 54),	(41, 56)),
iPortugal :	    ((38, 15),	(46, 17)),
iEngland :	    ((37, 76),	(39, 78)),
iFrance :		((45, 91),	(49, 93)),
iNetherlands :  ((41, 82),	(43, 86)),
iHawaii :		((12, 46),	(15, 50)),
iRussia :		((3, 106),	(13, 113)),
iAmerica :	    ((33, 72),	(46, 89)),
iHaiti :		((36, 54),	(38, 57)),
iArgentina :	((19, 7),	(26, 18)),
iMexico :		((6, 58),	(25, 95)),
iColombia :	    ((26, 41),	(43, 49)),
iPeru :		    ((19, 26),	(30, 38)),
iBrazil :		((35, 15),	(58, 35)),
iVenezuela :	((34, 40),	(44, 49)),
iCanada :		((32, 86),	(52, 102)),
})

dExtendedBirthArea = CivDict({
})

dBirthAreaExceptions = CivDict({
iMaya :		    [(20, 58), (23, 61)],
iTeotihuacan :  [(14, 64)],
iWari :		    [(24, 29)],
iChimu :		[(23, 35), (24, 36), (25, 35), (25, 36), (25, 37)],
iInca :		    [(27, 31)],
iNetherlands :  [(43, 84), (43, 86), (43, 85)],
iAmerica :	    [(35, 88), (39, 84), (37, 86), (40, 88), (34, 83), (33, 89), (36, 83), (33, 80), (36, 88), (39, 88), (33, 81), (34, 87), (35, 80), (36, 87), (38, 88), (38, 86), (37, 84), (35, 84), (35, 85), (41, 88), (40, 89), (34, 80), (33, 88), (37, 83), (33, 87), (35, 87), (44, 89), (34, 84), (37, 88), (39, 87), (42, 88), (33, 83), (36, 89), (37, 85), (39, 89), (38, 87), (39, 86), (36, 84), (34, 81), (35, 83), (38, 83), (33, 86), (35, 86), (33, 78), (34, 85), (36, 81), (42, 89), (33, 82), (38, 84), (35, 82), (35, 89), (34, 89), (34, 88), (36, 85), (43, 89), (33, 85), (39, 85), (34, 82), (36, 82), (38, 89), (38, 85), (33, 79), (37, 89), (34, 86), (36, 86), (37, 87), (35, 81), (41, 89), (33, 84)],
iMexico :       [(10, 95), (25, 93), (19, 92), (20, 86), (24, 92), (25, 82), (17, 94), (22, 81), (24, 79), (25, 71), (21, 94), (24, 66), (18, 85), (23, 88), (14, 93), (23, 69), (15, 89), (20, 88), (25, 88), (22, 58), (19, 91), (24, 89), (25, 77), (22, 82), (12, 94), (24, 76), (17, 90), (21, 81), (23, 82), (18, 86), (23, 95), (21, 59), (23, 72), (20, 93), (25, 91), (23, 59), (16, 87), (19, 86), (24, 86), (25, 72), (17, 95), (22, 95), (24, 73), (21, 84), (23, 81), (18, 91), (23, 66), (14, 91), (23, 79), (20, 82), (25, 86), (15, 94), (22, 85), (16, 90), (24, 83), (25, 75), (21, 90), (22, 88), (11, 94), (24, 70), (24, 59), (21, 87), (22, 79), (20, 90), (23, 84), (13, 92), (18, 92), (23, 65), (25, 64), (25, 92), (19, 95), (20, 87), (15, 88), (25, 81), (22, 86), (24, 80), (25, 70), (21, 93), (24, 67), (23, 91), (13, 95), (23, 68), (20, 89), (25, 95), (22, 59), (19, 90), (20, 84), (15, 95), (25, 76), (24, 90), (22, 83), (16, 89), (12, 95), (24, 77), (25, 65), (21, 80), (16, 88), (18, 87), (23, 94), (14, 95), (24, 71), (23, 75), (24, 88), (20, 94), (25, 90), (19, 89), (24, 87), (17, 87), (22, 92), (19, 85), (24, 74), (17, 89), (23, 80), (18, 88), (23, 93), (14, 88), (23, 78), (20, 83), (9, 95), (25, 85), (19, 84), (24, 84), (25, 74), (21, 89), (22, 89), (24, 64), (16, 95), (17, 85), (21, 86), (23, 87), (13, 91), (18, 93), (23, 64), (24, 95), (16, 94), (23, 77), (15, 92), (19, 94), (20, 80), (24, 94), (25, 80), (22, 87), (24, 81), (25, 69), (21, 92), (22, 90), (24, 68), (25, 66), (23, 90), (13, 94), (21, 58), (18, 94), (23, 71), (15, 87), (25, 58), (25, 94), (17, 92), (19, 93), (20, 85), (24, 91), (25, 83), (22, 80), (16, 86), (17, 88), (21, 95), (25, 84), (24, 65), (17, 86), (23, 89), (14, 92), (23, 74), (15, 91), (16, 93), (20, 95), (25, 89), (19, 88), (15, 93), (25, 78), (22, 93), (24, 75), (25, 67), (21, 82), (25, 59), (23, 83), (17, 91), (18, 89), (23, 92), (14, 89), (14, 94), (23, 73), (20, 92), (23, 58), (17, 93), (19, 87), (24, 85), (25, 73), (21, 88), (22, 94), (24, 72), (21, 85), (23, 86), (25, 79), (13, 90), (24, 78), (18, 90), (23, 67), (14, 90), (18, 95), (16, 91), (23, 76), (24, 93), (16, 92), (20, 81), (15, 90), (25, 87), (22, 84), (24, 82), (25, 68), (21, 91), (22, 91), (11, 95), (24, 69), (24, 58), (22, 78), (23, 85), (13, 93), (21, 79), (23, 70), (21, 83), (20, 91)],
iArgentina :	[(25, 10), (25, 11), (26, 9), (25, 9), (26, 8), (26, 11), (26, 10), (26, 7), (25, 8), (25, 7), (26, 12)],
iPeru :		    [(29, 38), (27, 26), (30, 26), (30, 32), (28, 29), (29, 28), (28, 34), (30, 31), (28, 26), (29, 27), (30, 27), (30, 33), (27, 33), (26, 32), (29, 31), (25, 26), (30, 28), (29, 34), (28, 27), (27, 28), (30, 38), (27, 32), (28, 31), (26, 26), (29, 30), (30, 34), (30, 29), (29, 33), (28, 32), (29, 29), (26, 27), (27, 27), (29, 26), (28, 28), (29, 32), (28, 33), (30, 30)],
iVenezuela :	[(34, 41), (34, 40), (41, 40), (34, 43), (35, 43), (34, 42), (34, 45), (34, 44), (44, 42), (44, 41), (35, 42), (34, 49), (44, 40)],
iCanada :		[(52, 90), (47, 87), (45, 89), (32, 88), (43, 86), (44, 88), (34, 87), (38, 86), (47, 88), (42, 86), (46, 87), (39, 87), (33, 89), (32, 86), (47, 86), (45, 88), (47, 89), (32, 89), (46, 88), (42, 87), (34, 88), (39, 86), (44, 86), (32, 87), (45, 87), (33, 86), (32, 90), (40, 86), (46, 89), (33, 88), (41, 87), (34, 89), (44, 87), (45, 86), (32, 91), (40, 87), (33, 90), (33, 87), (41, 86), (43, 87), (47, 102), (34, 86), (43, 88), (34, 90), (46, 86)],
}, [])

### Core Area ### - MacAurther: The core area of a civ

dCoreArea = CivDict({
iMaya :		    ((20, 59),	(22, 60)),
iZapotec :		((12, 60), 	(16, 62)),
iTeotihuacan :  ((13, 65),	(15, 67)),
iTiwanaku :	    ((25, 21),	(29, 26)),
iWari :		    ((22, 32),	(24, 35)),
iMississippi :  ((27, 81),	(35, 85)),
iPuebloan :		((12, 85),	(18, 88)),
iMuisca :		((30, 41),	(33, 44)),
iNorse :		((0, 0), 	(0, 0)),	# No core for Europeans
iChimu :		((19, 35),	(22, 38)),
iInuit :		((10, 117),	(19, 121)),
iInca :		    ((20, 27),	(27, 31)),
iPurepecha :	((8, 66),	(11, 69)),
iAztecs :		((12, 62),	(17, 65)),
iIroquois :	    ((36, 84),	(40, 87)),
iSioux :		((25, 89),	(28, 92)),
iSpain : 		((0, 0), 	(0, 0)),	# No core for Europeans
iPortugal : 	((0, 0), 	(0, 0)),	# No core for Europeans
iEngland : 		((0, 0), 	(0, 0)),	# No core for Europeans
iFrance : 		((0, 0), 	(0, 0)),	# No core for Europeans
iNetherlands :	((0, 0), 	(0, 0)),	# No core for Europeans
iHawaii :		((12, 46),	(15, 50)),
iRussia :		((0, 0), 	(0, 0)),	# No core for Europeans
iAmerica :	    ((35, 79),	(46, 89)),
iHaiti :		((36, 54),	(38, 57)),
iArgentina :	((19, 7),	(24, 16)),
iMexico :		((9, 59),	(18, 70)),
iColombia :	    ((27, 41),	(33, 47)),
iPeru :		    ((19, 26),	(25, 38)),
iBrazil :		((35, 15),	(49, 25)),
iVenezuela :	((34, 44),	(44, 49)),
iCanada :		((35, 86),	(51, 94)),
})

dPeriodCoreArea = {
iSioux :		((21, 90),	(25, 95)),
}

dCoreAreaExceptions = CivDict({
iMaya :			[(34, 57), (37, 57)],
iWari :		    [(22, 35), (24, 35), (24, 32), (24, 34), (22, 32)],
iMississippi :  [(33, 85), (32, 85), (30, 85), (32, 84), (30, 84), (34, 85), (35, 84), (34, 84), (35, 85), (31, 84), (31, 85), (33, 84)],
iPuebloan :	    [(19, 80)],
iInca :		    [(27, 31)],
iIroquois :	    [(37, 86), (36, 87), (37, 87), (38, 87), (36, 86)],
iAmerica :	    [(35, 88), (40, 88), (39, 88), (37, 89), (38, 89), (36, 88), (37, 86), (41, 88), (40, 89), (35, 87), (44, 89), (37, 88), (42, 88), (37, 79), (36, 89), (38, 87), (38, 88), (35, 86), (42, 89), (43, 89), (35, 89), (36, 87), (39, 89), (36, 86), (37, 87), (41, 89)],
iPeru :		    [(25, 37), (25, 35), (25, 38), (25, 36)],
iBrazil :		[(35, 24), (35, 22), (40, 22), (38, 22), (42, 25), (41, 23), (38, 20), (37, 20), (42, 20), (36, 21), (43, 25), (35, 25), (40, 23), (42, 24), (41, 22), (40, 19), (38, 21), (35, 21), (43, 23), (42, 21), (38, 24), (38, 23), (37, 23), (41, 25), (36, 22), (39, 20), (40, 24), (37, 21), (41, 21), (35, 20), (43, 22), (40, 20), (37, 25), (36, 23), (39, 21), (36, 24), (37, 22), (41, 24), (42, 22), (41, 19), (39, 23), (40, 25), (41, 20), (35, 23), (40, 21), (38, 25), (37, 24), (39, 25), (36, 25), (35, 19), (42, 23), (39, 22), (36, 20), (39, 24)],
iVenezuela :	[(34, 45), (34, 44), (34, 49)],
iCanada :		[(47, 87), (45, 89), (43, 86), (44, 88), (38, 86), (42, 86), (46, 87), (39, 87), (47, 86), (45, 88), (47, 89), (46, 88), (42, 87), (39, 86), (44, 86), (45, 87), (47, 88), (40, 86), (46, 89), (41, 87), (44, 87), (45, 86), (40, 87), (41, 86), (43, 87), (43, 88), (46, 86)],
}, [])

dPeriodCoreAreaExceptions = appenddict({
})

### Normal Area ### - MacAurther: Used for UHVs and Dynamic Civs. Basically means area they would normally inhabit I think???
# TODO
dNormalArea = CivDict({
iMaya :		    ((19, 56),	(25, 63)),
iZapotec :		((12, 60), 	(16, 62)),
iTeotihuacan :  ((12, 62),	(18, 68)),
iTiwanaku :	    ((23, 21),	(29, 29)),
iWari :		    ((20, 28),	(26, 35)),
iMississippi :  ((24, 75),	(37, 90)),
iPuebloan :	    ((10, 80),	(19, 88)),
iMuisca :		((29, 41),	(35, 46)),
iNorse :		((52, 100),	(57, 120)),
iChimu :		((19, 32),	(25, 41)),
iInuit :		((5, 109),	(27, 121)),
iInca :		    ((20, 19),	(29, 41)),
iPurepecha :	((10, 65), 	(12, 68)),
iAztecs :		((9, 59),	(19, 69)),
iIroquois :		((33, 84),	(41, 88)),
iSioux :		((20, 88),	(28, 95)),
iSpain :		((40, 54),  (40, 54) ),
iPortugal :		((39, 16),  (39, 16) ),
iEngland :		((38, 77),  (38, 77) ),
iFrance :		((46, 92),  (46, 92) ),
iNetherlands :	((42, 83),  (42, 83) ),
iHawaii :		((0, 46),	(15, 56)),
iRussia :		((12, 108), (12, 108)),
iAmerica :		((40, 81),  (40, 81) ),
iHaiti :		((36, 54),	(38, 57)),
iArgentina :	((23, 10),  (23, 10) ),
iMexico :		((13, 64),  (13, 64) ),
iColombia :		((31, 42),  (31, 42) ),
iPeru :			((20, 32),  (20, 32) ),
iBrazil :		((44, 16),  (44, 16) ),
iVenezuela :	((39, 47),  (39, 47) ),
iCanada :		((40, 89),  (40, 89) ),
})

dPeriodNormalArea = {
}

dNormalAreaExceptions = CivDict({
iMaya :		[(20, 56), (19, 58), (19, 56), (24, 56), (19, 57), (25, 56), (21, 56)],
iTiwanaku :	[(29, 28), (29, 29)],
iWari :		[(26, 32), (25, 35), (26, 35), (26, 33), (26, 34)],
iMississippi :[(35, 88), (25, 82), (27, 83), (24, 79), (36, 87), (30, 79), (28, 75), (37, 75), (35, 87), (25, 88), (36, 78), (37, 88), (24, 89), (36, 89), (37, 85), (36, 84), (26, 83), (32, 87), (32, 90), (34, 85), (31, 90), (37, 78), (31, 87), (24, 86), (26, 89), (33, 85), (26, 84), (32, 84), (33, 90), (29, 76), (34, 86), (31, 89), (28, 77), (25, 86), (27, 87), (24, 83), (26, 90), (27, 88), (25, 81), (27, 82), (24, 80), (30, 76), (35, 86), (36, 79), (24, 90), (36, 90), (37, 84), (36, 85), (37, 77), (35, 85), (25, 90), (31, 86), (36, 76), (37, 90), (24, 87), (37, 87), (33, 84), (26, 85), (32, 85), (33, 89), (32, 88), (29, 75), (34, 87), (31, 88), (25, 85), (31, 85), (27, 86), (24, 84), (33, 87), (26, 86), (27, 76), (29, 78), (34, 88), (35, 90), (36, 75), (25, 80), (27, 85), (24, 81), (27, 75), (30, 77), (35, 89), (25, 83), (36, 86), (26, 81), (30, 78), (37, 76), (35, 84), (25, 89), (36, 77), (37, 89), (24, 88), (36, 88), (37, 86), (26, 82), (32, 86), (33, 88), (32, 89), (34, 84), (30, 75), (37, 79), (25, 84), (31, 84), (24, 85), (26, 88), (27, 90), (33, 86), (26, 87), (29, 77), (34, 89), (28, 76), (25, 87), (27, 84), (24, 82), (27, 89), (34, 90)],
iInuit :		[(8, 110), (5, 112), (9, 111), (12, 109), (7, 109), (5, 110), (12, 113), (9, 113), (6, 109), (7, 113), (8, 112), (6, 112), (8, 111), (11, 109), (9, 110), (12, 110), (10, 109), (5, 109), (9, 112), (7, 112), (8, 113), (6, 113), (6, 110), (9, 109), (11, 113), (7, 111), (10, 112), (10, 110), (11, 111), (6, 111), (11, 112), (7, 110), (8, 109), (10, 113), (5, 113), (10, 111), (5, 111), (11, 110), (12, 112)],
iInca :		[(28, 37), (29, 38), (29, 28), (25, 39), (29, 40), (29, 19), (29, 35), (28, 41), (28, 34), (26, 40), (29, 32), (27, 37), (26, 39), (28, 40), (28, 38), (28, 19), (27, 33), (25, 36), (26, 32), (29, 31), (28, 35), (25, 41), (29, 34), (26, 36), (27, 36), (28, 39), (25, 35), (25, 40), (27, 32), (28, 31), (26, 33), (29, 30), (26, 35), (25, 38), (28, 36), (29, 33), (26, 37), (29, 39), (28, 32), (27, 40), (27, 31), (27, 35), (29, 37), (28, 30), (27, 41), (29, 29), (27, 39), (25, 37), (27, 38), (26, 34), (28, 33), (29, 41), (26, 41), (29, 36), (27, 34), (26, 38)],
}, [])

dPeriodNormalAreaExceptions = appenddict({
})

### Broader Area ### - MacAurther: No idea what this is for
# TODO
dBroaderArea = CivDict({
iMaya :			((22, 59),  (22, 59)),
iZapotec :		((12, 60), 	(16, 62)),
iTeotihuacan :	((14, 66),  (14, 66)),
iTiwanaku :		((26, 25),  (26, 25)),
iWari :			((23, 33),  (23, 33)),
iMississippi :	((33, 82),  (33, 82)),
iPuebloan :		((18, 84),  (18, 84)),
iMuisca :		((31, 42),  (31, 42)),
iNorse :		((55, 114), (55, 114)),
iChimu :		((20, 36),  (20, 36)),
iInuit :		((14, 111), (14, 111)),
iInca :			((24, 29),  (24, 29)),
iPurepecha :	((10, 65), 	(12, 68)),
iAztecs :		((13, 64),  (13, 64)),
iSpain :		((40, 54),  (40, 54)),
iIroquois :		((39, 85),  (39, 85)),
iSioux :		((20, 88),	(28, 95)),
iPortugal :		((39, 16),  (39, 16)),
iEngland :		((38, 77),  (38, 77)),
iFrance :		((46, 92),  (46, 92)),
iNetherlands :	((42, 83),  (42, 83)),
iHawaii :		((15, 48),  (15, 48)),
iRussia :		((12, 108), (12, 108)),
iAmerica :		((40, 81),  (40, 81)),
iHaiti :		((37, 55),  (37, 55)),
iArgentina :	((23, 10),  (23, 10)),
iMexico :		((13, 64),  (13, 64)),
iColombia :		((31, 42),  (31, 42)),
iPeru :			((20, 32),  (20, 32)),
iBrazil :		((44, 16),  (44, 16)),
iVenezuela :	((39, 47),  (39, 47)),
iCanada :		((40, 89),  (40, 89)),
})

dPeriodBroaderArea = {
}

### Expansion area ### - MacAurther: Extra units are received to conquer specified area on spawn

dExpansionArea = CivDict({
iAmerica :	((33, 65),	(63, 90)),
iArgentina :((46, 1),	(62, 38)),
iColombia :	((34, 33),	(57, 54)),
iPeru :		((34, 29),	(58, 46)),
})

dExpansionAreaExceptions = CivDict({
iAmerica :	[(35, 88), (61, 82), (59, 78), (39, 70), (36, 68), (63, 76), (48, 86), (61, 76), (51, 74), (52, 68), (40, 66), (42, 88), (55, 78), (56, 75), (44, 86), (60, 81), (57, 81), (58, 65), (35, 65), (62, 75), (59, 71), (60, 79), (36, 67), (61, 69), (39, 85), (54, 87), (51, 83), (52, 67), (49, 71), (63, 83), (53, 73), (54, 73), (49, 89), (42, 67), (55, 71), (47, 90), (41, 85), (46, 82), (57, 90), (58, 72), (33, 74), (60, 70), (37, 68), (34, 70), (48, 68), (62, 84), (36, 80), (51, 88), (52, 74), (50, 70), (63, 88), (48, 90), (38, 90), (40, 86), (56, 89), (44, 68), (46, 85), (33, 67), (57, 69), (45, 90), (37, 77), (34, 65), (35, 85), (59, 75), (50, 65), (63, 65), (51, 71), (55, 85), (53, 69), (44, 67), (47, 86), (58, 90), (56, 70), (44, 89), (33, 68), (60, 84), (57, 78), (58, 68), (45, 83), (35, 90), (61, 80), (62, 70), (52, 88), (63, 78), (48, 72), (61, 74), (52, 70), (63, 84), (40, 68), (55, 72), (56, 77), (43, 78), (47, 69), (60, 83), (57, 87), (58, 79), (35, 67), (62, 73), (59, 89), (60, 73), (37, 89), (61, 67), (62, 83), (51, 85), (52, 77), (49, 69), (53, 87), (54, 79), (42, 65), (55, 65), (57, 88), (33, 72), (57, 66), (37, 66), (34, 68), (48, 70), (62, 90), (38, 70), (36, 82), (51, 90), (50, 68), (63, 90), (54, 70), (40, 88), (58, 81), (56, 65), (33, 65), (59, 87), (57, 75), (45, 88), (37, 75), (59, 77), (39, 69), (36, 89), (63, 67), (48, 83), (61, 79), (53, 89), (54, 89), (51, 73), (49, 73), (50, 89), (55, 87), (53, 67), (41, 69), (55, 77), (58, 88), (56, 72), (57, 76), (58, 66), (62, 68), (59, 66), (60, 76), (39, 66), (52, 90), (63, 72), (61, 72), (49, 66), (53, 76), (54, 74), (41, 78), (42, 68), (55, 74), (47, 89), (56, 79), (44, 82), (47, 71), (58, 77), (35, 69), (62, 79), (60, 75), (36, 79), (48, 65), (61, 65), (62, 81), (38, 77), (51, 87), (55, 67), (40, 83), (56, 86), (41, 89), (46, 86), (59, 80), (60, 66), (34, 66), (61, 90), (38, 68), (39, 78), (52, 86), (50, 66), (63, 68), (54, 68), (51, 66), (49, 86), (55, 88), (40, 90), (41, 66), (46, 89), (47, 85), (56, 67), (33, 71), (46, 67), (60, 89), (57, 73), (45, 86), (37, 73), (61, 83), (62, 67), (59, 79), (63, 77), (48, 85), (61, 77), (50, 87), (40, 65), (53, 65), (55, 79), (56, 74), (44, 85), (60, 80), (62, 74), (59, 68), (60, 78), (36, 66), (34, 78), (63, 74), (61, 70), (39, 90), (54, 86), (52, 66), (63, 80), (53, 74), (54, 72), (49, 90), (42, 66), (55, 68), (43, 66), (41, 86), (58, 75), (43, 88), (33, 75), (62, 77), (60, 69), (34, 73), (48, 67), (38, 67), (51, 89), (52, 73), (50, 73), (63, 89), (48, 89), (54, 67), (56, 88), (46, 84), (45, 65), (33, 76), (57, 70), (59, 72), (63, 70), (54, 90), (51, 68), (50, 90), (55, 90), (53, 70), (44, 66), (47, 87), (56, 69), (44, 88), (33, 69), (46, 65), (57, 79), (58, 71), (45, 84), (61, 81), (62, 65), (59, 65), (39, 65), (63, 79), (48, 87), (61, 75), (52, 69), (50, 85), (63, 85), (40, 67), (42, 89), (55, 73), (56, 76), (44, 87), (41, 83), (58, 78), (62, 72), (59, 70), (60, 72), (37, 90), (61, 68), (62, 82), (49, 70), (63, 82), (53, 72), (49, 88), (55, 70), (43, 68), (41, 84), (46, 83), (57, 89), (58, 73), (43, 90), (33, 73), (60, 71), (57, 67), (37, 67), (34, 71), (48, 69), (62, 85), (38, 65), (39, 77), (36, 81), (52, 75), (50, 71), (54, 65), (51, 65), (56, 90), (44, 69), (46, 90), (35, 78), (33, 66), (57, 68), (45, 89), (37, 76), (35, 84), (59, 74), (36, 88), (53, 90), (54, 88), (51, 70), (50, 88), (53, 68), (56, 71), (44, 90), (57, 77), (58, 69), (45, 82), (62, 71), (59, 67), (39, 67), (52, 89), (63, 73), (61, 73), (39, 89), (52, 71), (49, 67), (40, 69), (53, 77), (55, 75), (56, 78), (43, 65), (58, 76), (35, 66), (62, 78), (59, 88), (60, 74), (37, 88), (61, 66), (62, 80), (36, 84), (52, 78), (49, 68), (53, 86), (54, 76), (42, 78), (40, 82), (41, 90), (58, 87), (59, 81), (60, 65), (57, 65), (37, 65), (34, 69), (48, 71), (36, 83), (50, 69), (63, 69), (38, 89), (54, 71), (51, 67), (49, 87), (55, 89), (40, 89), (41, 67), (46, 88), (56, 66), (60, 88), (57, 74), (45, 87), (37, 74), (61, 84), (62, 66), (59, 76), (39, 68), (36, 90), (63, 66), (48, 84), (61, 78), (53, 88), (51, 72), (49, 72), (50, 86), (55, 86), (53, 66), (41, 68), (42, 90), (55, 76), (47, 83), (58, 89), (56, 73), (60, 87), (58, 67), (62, 69), (59, 69), (60, 77), (36, 65), (63, 75), (61, 71), (52, 65), (49, 65), (63, 81), (53, 75), (54, 75), (42, 69), (55, 69), (47, 88), (56, 80), (43, 67), (47, 70), (58, 74), (43, 89), (35, 68), (62, 76), (59, 90), (60, 68), (34, 72), (48, 66), (38, 66), (51, 86), (52, 72), (50, 72), (48, 88), (40, 78), (54, 66), (55, 66), (40, 84), (56, 87), (41, 88), (42, 86), (46, 87), (45, 66), (60, 67), (57, 71), (34, 67), (61, 89), (62, 89), (59, 73), (52, 87), (50, 67), (63, 71), (54, 69), (51, 69), (49, 85), (53, 71), (44, 65), (41, 65), (47, 84), (56, 68), (43, 87), (33, 70), (60, 90), (57, 72), (58, 70), (45, 85), (37, 72)],
iArgentina :[(49, 37), (55, 5), (62, 15), (61, 29), (60, 11), (50, 34), (47, 35), (46, 25), (62, 2), (61, 10), (48, 2), (47, 28), (46, 12), (59, 36), (58, 36), (47, 9), (46, 3), (57, 9), (62, 38), (61, 38), (52, 4), (48, 37), (56, 7), (60, 29), (59, 15), (49, 32), (55, 8), (62, 8), (60, 8), (47, 38), (46, 26), (62, 31), (61, 13), (56, 38), (47, 8), (46, 9), (62, 18), (59, 35), (61, 22), (56, 9), (60, 36), (49, 28), (59, 12), (62, 35), (53, 1), (52, 8), (58, 3), (48, 34), (55, 2), (49, 24), (60, 2), (51, 34), (49, 35), (46, 32), (62, 5), (61, 3), (60, 13), (47, 37), (46, 23), (62, 24), (47, 22), (55, 37), (55, 10), (61, 35), (56, 6), (46, 2), (52, 1), (58, 9), (57, 7), (54, 4), (53, 4), (59, 4), (58, 4), (48, 30), (52, 32), (60, 7), (59, 9), (48, 31), (46, 29), (62, 6), (61, 6), (47, 24), (46, 16), (62, 21), (46, 24), (48, 26), (56, 37), (47, 21), (46, 7), (60, 35), (51, 5), (56, 3), (58, 38), (61, 34), (52, 6), (59, 30), (58, 10), (57, 2), (54, 1), (53, 7), (59, 3), (49, 36), (62, 12), (61, 28), (60, 4), (50, 35), (51, 38), (47, 34), (46, 30), (62, 3), (61, 9), (57, 38), (47, 31), (46, 13), (62, 22), (48, 25), (49, 26), (58, 37), (49, 3), (48, 21), (60, 32), (58, 16), (57, 8), (48, 24), (61, 37), (59, 29), (48, 38), (61, 31), (60, 30), (59, 14), (47, 33), (55, 11), (62, 9), (55, 1), (60, 9), (50, 36), (49, 30), (56, 36), (46, 27), (62, 28), (61, 12), (53, 8), (47, 18), (46, 14), (62, 19), (59, 34), (49, 31), (48, 29), (56, 10), (47, 15), (60, 37), (57, 11), (62, 32), (58, 6), (48, 35), (61, 21), (60, 3), (59, 13), (49, 34), (46, 33), (62, 10), (61, 2), (60, 14), (47, 36), (46, 20), (62, 25), (61, 15), (49, 4), (47, 17), (46, 11), (59, 33), (47, 2), (56, 4), (52, 2), (46, 36), (57, 6), (54, 5), (53, 3), (60, 21), (59, 7), (58, 5), (48, 32), (54, 8), (54, 2), (59, 8), (46, 34), (62, 7), (61, 5), (47, 27), (46, 17), (62, 26), (47, 20), (46, 4), (51, 4), (50, 4), (57, 12), (48, 28), (61, 33), (52, 7), (58, 11), (49, 25), (54, 6), (53, 6), (59, 2), (50, 30), (55, 7), (62, 13), (57, 1), (60, 5), (46, 31), (61, 8), (57, 37), (48, 3), (46, 18), (62, 23), (59, 38), (58, 34), (48, 22), (46, 1), (61, 7), (60, 33), (51, 3), (47, 19), (56, 1), (62, 36), (61, 36), (46, 38), (58, 12), (54, 3), (60, 31), (52, 38), (49, 38), (46, 37), (62, 14), (61, 30), (60, 10), (50, 37), (47, 32), (48, 27), (62, 29), (61, 11), (47, 29), (46, 15), (62, 16), (59, 37), (48, 19), (61, 27), (60, 38), (57, 10), (62, 33), (58, 1), (48, 36), (61, 20), (54, 38), (51, 36), (49, 33), (55, 9), (62, 11), (61, 1), (48, 18), (50, 38), (47, 10), (46, 21), (62, 30), (61, 14), (51, 37), (47, 16), (46, 8), (60, 15), (59, 32), (56, 8), (57, 4), (52, 3), (59, 21), (57, 5), (48, 20), (62, 34), (53, 2), (60, 22), (59, 6), (58, 2), (48, 33), (55, 3), (54, 9), (61, 23), (60, 1), (59, 11), (46, 35), (62, 4), (61, 4), (60, 12), (47, 30), (47, 26), (46, 22), (62, 27), (47, 23), (46, 5), (51, 7), (50, 5), (59, 1), (56, 5), (56, 11), (61, 32), (59, 16), (58, 8), (47, 1), (54, 7), (53, 5), (59, 5), (58, 7), (55, 6), (61, 26), (60, 6), (50, 33), (46, 28), (62, 1), (55, 38), (57, 36), (47, 25), (46, 19), (62, 20), (58, 35), (59, 10), (48, 23), (60, 34), (51, 2), (56, 2), (62, 37), (49, 29), (52, 5), (59, 31), (49, 27), (61, 16)],
iColombia :	[(56, 51), (34, 52), (55, 35), (35, 41), (36, 34), (34, 46), (37, 35), (44, 34), (38, 40), (45, 35), (39, 45), (50, 39), (51, 34), (52, 37), (35, 46), (40, 35), (36, 41), (34, 41), (41, 34), (37, 44), (35, 52), (38, 35), (43, 52), (39, 42), (37, 54), (45, 54), (52, 44), (56, 39), (53, 33), (57, 38), (40, 42), (41, 43), (40, 48), (39, 35), (52, 43), (56, 46), (46, 33), (53, 42), (57, 47), (54, 33), (41, 44), (55, 36), (35, 34), (42, 43), (36, 37), (43, 34), (41, 54), (44, 37), (42, 53), (39, 54), (50, 42), (56, 53), (57, 48), (34, 50), (35, 43), (36, 44), (34, 44), (37, 33), (35, 49), (38, 46), (45, 33), (43, 49), (39, 47), (52, 39), (56, 34), (53, 38), (57, 35), (40, 37), (34, 39), (37, 42), (35, 54), (42, 39), (38, 33), (36, 49), (43, 54), (39, 36), (37, 52), (44, 49), (45, 52), (50, 54), (51, 45), (52, 46), (56, 41), (57, 36), (40, 44), (54, 44), (41, 41), (55, 41), (42, 46), (40, 50), (43, 47), (41, 51), (38, 50), (56, 48), (53, 40), (57, 45), (54, 39), (55, 38), (35, 36), (42, 41), (36, 39), (43, 36), (37, 38), (44, 39), (42, 51), (38, 53), (39, 48), (50, 40), (51, 33), (57, 54), (34, 48), (35, 45), (36, 46), (37, 47), (35, 51), (38, 44), (36, 52), (39, 41), (51, 38), (52, 33), (56, 36), (53, 36), (57, 33), (40, 39), (54, 43), (34, 37), (41, 38), (37, 40), (42, 37), (38, 39), (36, 51), (43, 40), (39, 38), (37, 50), (44, 51), (48, 54), (45, 50), (50, 52), (52, 40), (56, 43), (46, 34), (53, 45), (57, 42), (40, 46), (54, 34), (41, 47), (55, 43), (35, 33), (42, 44), (43, 33), (41, 49), (42, 54), (38, 48), (49, 40), (39, 53), (53, 54), (54, 37), (35, 38), (36, 33), (43, 38), (37, 36), (44, 33), (42, 49), (38, 43), (45, 36), (39, 50), (51, 35), (52, 36), (35, 47), (40, 34), (36, 40), (34, 40), (41, 35), (37, 45), (35, 53), (38, 34), (36, 54), (43, 53), (39, 43), (44, 54), (51, 40), (47, 54), (52, 35), (56, 38), (55, 54), (53, 34), (57, 39), (40, 41), (54, 41), (34, 35), (41, 36), (55, 44), (42, 35), (38, 37), (37, 48), (48, 40), (45, 48), (52, 42), (56, 45), (53, 43), (57, 40), (41, 45), (55, 37), (35, 35), (42, 42), (40, 54), (36, 36), (43, 35), (44, 36), (38, 54), (51, 54), (47, 34), (34, 53), (55, 34), (35, 40), (36, 35), (34, 47), (37, 34), (44, 35), (38, 41), (45, 34), (49, 39), (39, 44), (52, 38), (56, 33), (53, 39), (40, 36), (36, 42), (34, 38), (41, 33), (37, 43), (42, 38), (36, 48), (39, 37), (37, 53), (44, 48), (45, 53), (46, 53), (51, 42), (54, 53), (52, 45), (56, 40), (55, 48), (57, 37), (40, 43), (34, 33), (41, 42), (55, 46), (42, 33), (40, 49), (39, 34), (44, 47), (56, 47), (53, 41), (57, 46), (54, 38), (55, 39), (35, 37), (42, 40), (36, 38), (43, 37), (37, 39), (44, 38), (42, 50), (48, 33), (38, 52), (39, 49), (56, 54), (34, 51), (35, 42), (36, 45), (34, 45), (35, 48), (38, 47), (43, 48), (39, 46), (50, 34), (51, 39), (56, 35), (53, 37), (57, 34), (40, 38), (54, 42), (34, 36), (41, 39), (37, 41), (42, 36), (38, 38), (36, 50), (39, 39), (37, 51), (44, 50), (56, 42), (57, 43), (40, 45), (54, 45), (41, 40), (55, 40), (42, 47), (40, 51), (43, 46), (41, 50), (38, 51), (49, 41), (52, 54), (57, 44), (47, 33), (54, 36), (34, 54), (55, 33), (35, 39), (43, 39), (37, 37), (42, 48), (38, 42), (45, 37), (39, 51), (50, 41), (57, 53), (34, 49), (35, 44), (40, 33), (36, 47), (37, 46), (35, 50), (38, 45), (36, 53), (43, 50), (39, 40), (44, 53), (46, 54), (51, 41), (54, 54), (52, 34), (56, 37), (53, 35), (40, 40), (54, 40), (34, 34), (41, 37), (55, 45), (42, 34), (38, 36), (43, 43), (39, 33), (37, 49), (45, 49), (50, 53), (51, 46), (52, 41), (56, 44), (46, 35), (53, 44), (57, 41), (40, 47), (54, 35), (41, 46), (55, 42), (42, 45), (40, 53), (41, 48), (38, 49), (39, 52)],
iPeru :		[(51, 40), (39, 46), (50, 34), (56, 38), (58, 41), (57, 39), (40, 41), (54, 41), (35, 41), (34, 35), (58, 36), (41, 36), (55, 44), (36, 34), (34, 46), (42, 35), (56, 30), (38, 37), (37, 35), (44, 34), (34, 29), (39, 32), (38, 40), (45, 35), (51, 39), (49, 32), (39, 45), (53, 40), (52, 32), (50, 39), (57, 45), (40, 45), (54, 39), (58, 42), (40, 38), (55, 38), (54, 42), (35, 36), (34, 36), (42, 41), (41, 39), (37, 41), (36, 39), (43, 36), (42, 36), (41, 45), (37, 38), (44, 39), (34, 30), (39, 39), (52, 42), (51, 34), (46, 35), (40, 29), (46, 32), (53, 43), (50, 40), (57, 40), (50, 44), (37, 29), (35, 46), (35, 35), (42, 31), (57, 29), (40, 35), (55, 37), (36, 41), (43, 30), (34, 41), (42, 42), (41, 34), (48, 30), (37, 44), (36, 36), (43, 35), (49, 31), (38, 35), (44, 36), (39, 37), (39, 42), (49, 46), (56, 42), (46, 29), (36, 29), (51, 31), (50, 45), (57, 43), (56, 29), (54, 45), (35, 45), (56, 37), (41, 40), (40, 32), (38, 31), (53, 29), (43, 29), (40, 42), (39, 30), (58, 46), (44, 30), (43, 46), (38, 44), (45, 31), (51, 43), (39, 41), (55, 42), (55, 40), (52, 44), (49, 41), (56, 39), (46, 30), (53, 44), (50, 46), (57, 38), (47, 31), (54, 46), (35, 40), (34, 32), (58, 37), (41, 43), (36, 35), (34, 40), (42, 32), (39, 29), (37, 34), (42, 45), (44, 35), (39, 35), (38, 41), (48, 33), (45, 34), (51, 38), (49, 39), (39, 44), (57, 44), (56, 36), (51, 44), (58, 43), (40, 39), (41, 37), (54, 43), (35, 39), (34, 37), (58, 38), (41, 38), (37, 40), (36, 32), (43, 39), (42, 37), (55, 45), (38, 39), (37, 37), (44, 32), (43, 40), (39, 38), (55, 29), (45, 37), (52, 43), (35, 31), (56, 46), (46, 33), (53, 42), (52, 38), (50, 41), (41, 31), (53, 39), (58, 44), (41, 44), (40, 36), (36, 42), (35, 34), (48, 40), (42, 43), (41, 33), (48, 31), (37, 43), (36, 37), (43, 34), (42, 38), (49, 30), (38, 32), (44, 37), (50, 29), (48, 32), (36, 30), (47, 46), (52, 40), (49, 45), (56, 43), (46, 34), (53, 45), (51, 30), (50, 42), (57, 42), (40, 46), (37, 31), (35, 44), (41, 29), (40, 33), (55, 43), (35, 33), (42, 44), (37, 46), (44, 31), (43, 33), (47, 30), (38, 45), (45, 30), (51, 42), (50, 30), (48, 45), (52, 45), (49, 40), (56, 40), (46, 31), (51, 29), (57, 37), (40, 43), (35, 43), (34, 33), (36, 46), (41, 42), (55, 46), (36, 44), (34, 44), (42, 33), (37, 33), (57, 31), (39, 34), (38, 46), (45, 33), (51, 41), (39, 40), (47, 32), (34, 31), (48, 46), (47, 29), (54, 40), (35, 38), (34, 34), (58, 39), (57, 46), (40, 40), (36, 33), (43, 38), (42, 34), (38, 36), (37, 36), (38, 42), (44, 33), (43, 43), (39, 33), (38, 43), (45, 36), (40, 31), (53, 41), (52, 39), (41, 30), (35, 30), (54, 38), (53, 46), (42, 29), (38, 30), (40, 37), (58, 45), (35, 37), (34, 39), (42, 40), (41, 32), (37, 42), (36, 38), (40, 30), (42, 39), (49, 29), (38, 33), (37, 39), (44, 38), (51, 46), (55, 39), (39, 36), (58, 30), (52, 41), (49, 44), (56, 44), (34, 38), (36, 31), (57, 41), (47, 33), (37, 30), (42, 30), (57, 30), (40, 34), (38, 29), (36, 40), (35, 32), (43, 31), (58, 29), (41, 35), (48, 29), (37, 45), (43, 32), (44, 29), (38, 34), (45, 29), (51, 45), (50, 31), (39, 43), (41, 46), (58, 34), (52, 46), (58, 40), (56, 41), (47, 34), (57, 36), (40, 44), (54, 44), (35, 42), (43, 37), (58, 35), (41, 41), (55, 41), (36, 45), (34, 45), (42, 46), (39, 31), (37, 32), (35, 29), (56, 45), (38, 38), (45, 32)],
}, [])

### Respawn area ### - The area a civ respawns into

dRespawnArea = CivDict({
})