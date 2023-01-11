from Consts import *

# Peak that change to hills during the game, like Bogota
lPeakExceptions = []
	
### Capitals ###

dCapitals = CivDict({
iMaya :			(36, 58), # Tikal
iTeotihuacan :	(28, 61), # Teotihuacan
iTiwanaku :		(52, 33), # Tiwanaku
iWari :			(46, 39), # Huari
iMississippi :	(44, 79), # Sunwatch
iPuebloan :		(25, 73), # Pueblo Bonito
iMuisca :		(50, 48), # Hunza
iNorse :		(77, 104), # Reykjavik
iChimu :		(43, 41), # Chan Chan
iInuit :		(6, 104), # North Alaska
iInca :			(49, 36), # Cuzco
iAztecs :		(30, 60), # Tenochtitlan
iSpain :		(55, 59), # Santo Domingo
iIroquois :		(51, 84), # Onondaga
iPortugal :		(67, 26), # Sao Paulo
iEngland :		(50, 77), # Jamestown
iFrance :		(58, 89), # Quebec
iNetherlands :	(56, 81), # New Amsterdam
iHawaii :		(14, 49), # Hilo
iRussia :		(15, 96), # Novo-Arkhangelsk
iAmerica :		(51, 79), # Washington
iHaiti :		(53, 58), # Port-au-Prince
iBolivia :		(52, 34), # La Paz
iArgentina :	(57, 16), # Buenos Aires
iMexico :		(30, 60), # Mexico City
iColombia :		(48, 49), # Bogota
iChile :		(49, 17), # Santiago
iPeru :			(47, 36), # Lima
iVenezuela :	(52, 53), # Caracas
iBrazil :		(70, 28), # Rio de Janeiro
iCanada :		(52, 88), # Ottawa
iCuba : 		(43, 62), # Havana
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

### Birth Area ###

dBirthArea = CivDict({
iMaya : 		((35, 57), 	(37, 59)),
iTeotihuacan :	((27, 60), 	(29, 62)),
iTiwanaku :		((51, 32), 	(53, 34)),
iWari :			((45, 36), 	(47, 40)),
iMississippi :	((43, 78), 	(45, 79)),
iPuebloan :		((24, 72), 	(26, 76)),
iMuisca :		((49, 47), 	(51, 49)),
iNorse :		((75, 103), (77, 106)),
iChimu :		((43, 40), 	(44, 44)),
iInuit :		((4, 103), 	(17, 105)),
iInca : 		((47, 34), 	(51, 37)),
iAztecs : 		((29, 59), 	(31, 61)),
iIroquois :		((50, 83), 	(53, 85)),
iSpain : 		((54, 58), 	(56, 60)),
iPortugal : 	((66, 26), 	(68, 28)),
iEngland : 		((49, 76), 	(51, 78)),
iFrance : 		((57, 88), 	(59, 90)),
iNetherlands :	((55, 80), 	(57, 82)),
iHawaii :		((12, 47), 	(14, 50)),
iRussia :		((14, 95), 	(16, 97)),
iAmerica : 		((46, 72), 	(63, 86)),
iHaiti :		((51, 58), 	(53, 60)),
iBolivia :		((51, 32), 	(55, 35)),
iArgentina : 	((52, 10), 	(59, 22)),
iMexico :		((15, 57), 	(38, 75)),
iColombia :		((45, 47), 	(49, 54)),
iChile :		((48, 15), 	(50, 23)),
iPeru :			((45, 34), 	(49, 38)),
iVenezuela :	((50, 50), 	(54, 53)),
iBrazil : 		((62, 22), 	(77, 40)),
iCanada : 		((45, 83), 	(64, 97)),
iCuba : 		((41, 60), 	(50, 62)),
})

dExtendedBirthArea = CivDict({
})

dBirthAreaExceptions = CivDict({
iAmerica :		[(46, 86), (48, 86), (49, 86), (50, 86), (52, 86), (53, 86), (54, 86), (55, 86), (56, 86), (46, 85), (47, 85), (48, 85), (46, 84), (47, 84), (48, 84)],
iArgentina :	[(58, 17), (59, 17), (59, 18), (59, 19), (59, 20), (59, 21)],
iCanada :		[(49, 83), (50, 83), (51, 83), (52, 83), (53, 83), (54, 83), (55, 83), (56, 83), (57, 83), (58, 83), (59, 83), 
				(49, 84), (50, 84), (51, 84), (52, 84), (53, 84), (54, 84), (55, 84), (56, 84), (57, 84), (58, 84), (59, 84), 
				(52, 85), (53, 85), (54, 85), (55, 85), (56, 85), (57, 85), (58, 85), (59, 85), (60, 85), (61, 85), 
				(58, 86), (59, 86), (60, 86), (61, 86), (62, 86), (63, 86), 
				(61, 87), (62, 87), (63, 87), 
				(61, 88)],
}, [])

### Core Area ###

dCoreArea = CivDict({
iMaya : 		((34, 57), 	(37, 59)),
iTeotihuacan :	((27, 60), 	(29, 62)),
iTiwanaku :		((51, 32), 	(53, 34)),
iWari :			((45, 36), 	(47, 40)),
iMississippi :	((34, 77), 	(31, 46)),# fix pagan religion
iPuebloan :		((24, 72), 	(26, 76)),# fix pagan religion
iMuisca :		((49, 47), 	(50, 49)),
iNorse :		((0, 0), 	(0, 0)),	#No core for Europeans
iChimu :		((43, 40), 	(44, 44)),
iInuit :		((4, 103), 	(17, 105)),# fix pagan religion
iInca : 		((46, 33), 	(52, 38)),
iAztecs : 		((27, 59), 	(31, 61)),
iIroquois :		((50, 83), 	(53, 86)),# fix pagan religion
iSpain : 		((0, 0), 	(0, 0)),	#No core for Europeans
iPortugal : 	((0, 0), 	(0, 0)),	#No core for Europeans
iEngland : 		((0, 0), 	(0, 0)),	#No core for Europeans
iFrance : 		((0, 0), 	(0, 0)),	#No core for Europeans
iNetherlands :	((0, 0), 	(0, 0)),	#No core for Europeans
iHawaii :		((12, 47), 	(14, 50)),
iRussia :		((0, 0), 	(0, 0)),	#No core for Europeans
iAmerica : 		((47, 79), 	(60, 84)),
iHaiti :		((51, 58), 	(53, 60)),
iBolivia :		((51, 32), 	(55, 35)),
iArgentina : 	((53, 15), 	(58, 20)),
iMexico :		((26, 57), 	(32, 64)),#TODO
iColombia :		((46, 49), 	(49, 54)),#TODO
iChile :		((48, 15), 	(50, 23)),#TODO
iPeru :			((45, 34), 	(49, 38)),#TODO
iVenezuela :	((49, 50), 	(54, 53)),#TODO
iBrazil : 		((65, 26), 	(72, 32)),#TODO
iCanada : 		((45, 83), 	(59, 90)),#TODO
iCuba : 		((41, 60), 	(50, 62)),#TODO
})

dPeriodCoreArea = {
}

dCoreAreaExceptions = CivDict({
iMaya :			[(34, 57), (37, 57)],
iInca :			[(51, 38), (52, 38), (52, 37), (52, 33)],
iIroquois :		[(50,86)],
iAmerica :		[(47, 84), (48, 84)],
iArgentina :	[(58, 17)],
iColombia :		[(49, 53), (49, 52), (49, 51)],
iVenezuela :	[(49, 50), (50, 50)],
iCanada :		[(49, 83), (50, 83), (52, 83), (54, 83), (55, 83), (57, 83), (58, 83), (59, 83), 
				(49, 84), (50, 84), (51, 84), (52, 84), (53, 84), (54, 84), (55, 84), (57, 84), (58, 84), (59, 84), 
				(52, 85), (53, 85), (56, 85), (57, 85), (59, 85), 
				(58, 86), (59, 86)],
}, [])

dPeriodCoreAreaExceptions = appenddict({
})

### Normal Area ###
#TODO
dNormalArea = CivDict({
iMaya : 		((36, 58), 	(36, 58)),
iTeotihuacan :	((27, 60), 	(29, 62)),
iTiwanaku :		((51, 32), 	(53, 34)),
iWari :			((46, 35), 	(48, 39)),
iMississippi :	((35, 75), 	(40, 79)),
iPuebloan :		((24, 72), 	(26, 76)),
iMuisca :		((49, 47), 	(51, 49)),
iNorse :		((0, 0), 	(0, 0)),
iChimu :		((43, 40), 	(44, 44)),
iInuit :		((4, 103), 	(17, 105)),
iInca : 		((49, 36), 	(49, 36)),
iAztecs : 		((30, 60), 	(30, 60)),
iIroquois :		((50, 83), 	(53, 85)),
iSpain : 		((54, 59), 	(54, 59)),
iPortugal : 	((67, 27), 	(67, 27)),
iEngland : 		((50, 77), 	(50, 77)),
iFrance : 		((58, 89), 	(58, 89)),
iNetherlands :	((56, 81), 	(56, 81)),
iHawaii :		((56, 81), 	(56, 81)),
iRussia :		((56, 81), 	(56, 81)),
iAmerica : 		((51, 79), 	(51, 79)),
iHaiti :		((51, 58), 	(53, 60)),
iBolivia :		((51, 32), 	(55, 35)),
iArgentina : 	((57, 16), 	(57, 16)),
iMexico :		((30, 60), 	(30, 60)),
iColombia :		((48, 49), 	(48, 49)),
iChile :		((48, 15), 	(50, 23)),
iPeru :			((45, 34), 	(49, 38)),
iVenezuela :	((50, 50), 	(54, 53)),
iBrazil : 		((70, 28), 	(70, 28)),
iCanada : 		((52, 87), 	(52, 87)),
iCuba : 		((41, 60), 	(50, 62)),
})

dPeriodNormalArea = {
}

dNormalAreaExceptions = CivDict({
iAztecs :	[],
}, [])

dPeriodNormalAreaExceptions = appenddict({
})

### Broader Area ###
#TODO
dBroaderArea = CivDict({
iMaya : 		((36, 58), 	(36, 58)),
iTeotihuacan :	((27, 60), 	(29, 62)),
iTiwanaku :		((51, 32), 	(53, 34)),
iWari :			((46, 35), 	(48, 39)),
iMississippi :	((35, 75), 	(40, 79)),
iPuebloan :		((24, 72), 	(26, 76)),
iMuisca :		((49, 47), 	(51, 49)),
iNorse :		((0, 0), 	(0, 0)),
iChimu :		((43, 40), 	(44, 44)),
iInuit :		((4, 103), 	(17, 105)),
iInca : 		((49, 36), 	(49, 36)),
iAztecs : 		((30, 60), 	(30, 60)),
iIroquois :		((50, 83), 	(53, 85)),
iSpain : 		((54, 59), 	(54, 59)),
iPortugal : 	((67, 27), 	(67, 27)),
iEngland : 		((50, 77), 	(50, 77)),
iFrance : 		((58, 89), 	(58, 89)),
iNetherlands :	((56, 81), 	(56, 81)),
iHawaii :		((56, 81), 	(56, 81)),
iRussia :		((56, 81), 	(56, 81)),
iAmerica : 		((51, 79), 	(51, 79)),
iHaiti :		((51, 58), 	(53, 60)),
iBolivia :		((51, 32), 	(55, 35)),
iArgentina : 	((57, 16), 	(57, 16)),
iMexico :		((30, 60), 	(30, 60)),
iColombia :		((48, 49), 	(48, 49)),
iChile :		((48, 15), 	(50, 23)),
iPeru :			((45, 34), 	(49, 38)),
iVenezuela :	((50, 50), 	(54, 53)),
iBrazil : 		((70, 28), 	(70, 28)),
iCanada : 		((52, 87), 	(52, 87)),
iCuba : 		((41, 60), 	(50, 62)),
})

dPeriodBroaderArea = {
}

### Expansion area ###

dExpansionArea = CivDict({
})

dExpansionAreaExceptions = CivDict({
}, [])

### Respawn area ###

dRespawnArea = CivDict({
iInca : 		((45, 31), 	(53, 39)),
})