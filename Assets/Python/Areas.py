from Consts import *

# Peak that change to hills during the game, like Bogota
lPeakExceptions = []
	
### Capitals ###

dCapitals = CivDict({
iMaya :			(36, 58), # Tikal
iTeotihuacan :	(29, 61), # Teotihuacan
iTiwanaku :		(52, 33), # Tiwanaku
iWari :			(46, 39), # Huari
iMississippi :	(36, 78), # Cahokia
iPuebloan :		(25, 73), # Pueblo Bonito
iMuisca :		(49, 49), # Hunza
iNorse :		(77, 104), # Reykjavik
iChimu :		(43, 43), # Chan Chan
iInuit :		(6, 104), # North Alaska
iInca :			(49, 36), # Cuzco
iAztecs :		(30, 60), # Tenochtitlan
iSpain :		(55, 59), # Santo Domingo
iIroquois :		(53, 84), # Onondaga
iPortugal :		(67, 27), # Sao Paulo
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
iPeru :			(46, 36), # Lima
iVenezuela :	(52, 53), # Caracas
iBrazil :		(70, 28), # Rio de Janeiro
iCanada :		(52, 87), # Ottawa
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
iTeotihuacan :	((28, 60), 	(30, 62)),
iTiwanaku :		((51, 32), 	(53, 34)),
iWari :			((46, 35), 	(48, 39)),
iMississippi :	((35, 75), 	(40, 79)),
iPuebloan :		((24, 72), 	(26, 76)),
iMuisca :		((48, 48), 	(49, 51)),
iNorse :		((0, 0), 	(0, 0)),
iChimu :		((43, 40), 	(44, 44)),
iInuit :		((4, 103), 	(17, 105)),
iInca : 		((47, 34), 	(51, 37)),
iAztecs : 		((29, 59), 	(31, 61)),
iIroquois :		((50, 83), 	(53, 85)),
iSpain : 		((53, 58), 	(55, 60)),
iPortugal : 	((66, 26), 	(68, 28)),
iEngland : 		((49, 76), 	(51, 78)),
iFrance : 		((57, 88), 	(59, 90)),
iNetherlands :	((55, 82), 	(57, 82)),
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
iSpain :		[],
}, [])

### Core Area ###

dCoreArea = CivDict({
iMaya : 		((34, 57), 	(37, 59)),
iTeotihuacan :	((28, 60), 	(30, 62)),
iTiwanaku :		((51, 32), 	(53, 34)),
iWari :			((46, 35), 	(48, 39)),
iMississippi :	((35, 75), 	(40, 79)),
iPuebloan :		((24, 72), 	(26, 76)),
iMuisca :		((48, 48), 	(49, 51)),
iNorse :		((0, 0), 	(0, 0)),	#No core for colonies
iChimu :		((43, 40), 	(44, 44)),
iInuit :		((4, 103), 	(17, 105)),
iInca : 		((46, 33), 	(52, 38)),
iAztecs : 		((27, 59), 	(31, 61)),
iIroquois :		((50, 83), 	(53, 85)),
iSpain : 		((0, 0), 	(0, 0)),	#No core for colonies
iPortugal : 	((0, 0), 	(0, 0)),	#No core for colonies
iEngland : 		((0, 0), 	(0, 0)),	#No core for colonies
iFrance : 		((0, 0), 	(0, 0)),	#No core for colonies
iNetherlands :	((0, 0), 	(0, 0)),	#No core for colonies
iHawaii :		((12, 47), 	(14, 50)),
iRussia :		((0, 0), 	(0, 0)),	#No core for colonies
iAmerica : 		((48, 80), 	(64, 87)),
iHaiti :		((51, 58), 	(53, 60)),
iBolivia :		((51, 32), 	(55, 35)),
iArgentina : 	((53, 15), 	(58, 20)),
iMexico :		((26, 57), 	(32, 64)),
iColombia :		((46, 49), 	(49, 54)),
iChile :		((48, 15), 	(50, 23)),
iPeru :			((45, 34), 	(49, 38)),
iVenezuela :	((50, 50), 	(54, 53)),
iBrazil : 		((65, 26), 	(72, 32)),
iCanada : 		((45, 83), 	(59, 90)),
iCuba : 		((41, 60), 	(50, 62)),
})

dPeriodCoreArea = {
}

dCoreAreaExceptions = CivDict({
iMaya :	[(34, 57), (37, 57)],
}, [])

dPeriodCoreAreaExceptions = appenddict({
})

### Normal Area ###
#TODO
dNormalArea = CivDict({
iMaya : 		((36, 58), 	(36, 58)),
iTeotihuacan :	((28, 60), 	(30, 62)),
iTiwanaku :		((51, 32), 	(53, 34)),
iWari :			((46, 35), 	(48, 39)),
iMississippi :	((35, 75), 	(40, 79)),
iPuebloan :		((24, 72), 	(26, 76)),
iMuisca :		((48, 48), 	(49, 51)),
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
iTeotihuacan :	((28, 60), 	(30, 62)),
iTiwanaku :		((51, 32), 	(53, 34)),
iWari :			((46, 35), 	(48, 39)),
iMississippi :	((35, 75), 	(40, 79)),
iPuebloan :		((24, 72), 	(26, 76)),
iMuisca :		((48, 48), 	(49, 51)),
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