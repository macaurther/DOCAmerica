from Consts import *

# Peak that change to hills during the game, like Bogota
lPeakExceptions = []
	
### Capitals ###

dCapitals = CivDict({
iMaya :			(36, 58), # Tikal
iInca :			(49, 36), # Cuzco
iAztecs :		(30, 60), # Tenochtitlan
iSpain :		(54, 59), # Santo Domingo
iPortugal :		(67, 27), # Sao Paulo
iEngland :		(50, 77), # Jamestown
iFrance :		(58, 89), # Quebec
iNetherlands :	(56, 81), # New Amsterdam
iHawaii :		(14, 49), # Hilo
iRussia :		(15, 96), # Novo-Arkhangelsk
iAmerica :		(51, 79), # Washington
iArgentina :	(57, 16), # Buenos Aires
iMexico :		(30, 60), # Mexico City
iColombia :		(48, 49), # Bogota
iBrazil :		(70, 28), # Rio de Janeiro
iCanada :		(52, 87), # Ottawa
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
iInca : 		((47, 34), 	(51, 37)),
iAztecs : 		((29, 59), 	(31, 61)),
iSpain : 		((53, 58), 	(55, 60)),
iPortugal : 	((66, 26), 	(68, 28)),
iEngland : 		((49, 76), 	(51, 78)),
iFrance : 		((57, 88), 	(59, 90)),
iNetherlands :	((55, 82), 	(57, 82)),
iHawaii :		((12, 47), 	(14, 50)),
iRussia :		((14, 95), 	(16, 97)),
iAmerica : 		((46, 72), 	(63, 86)),
iArgentina : 	((52, 10), 	(59, 22)),
iMexico :		((15, 57), 	(38, 75)),
iColombia :		((45, 47), 	(49, 54)),
iBrazil : 		((62, 22), 	(77, 40)),
iCanada : 		((45, 83), 	(64, 97)),
})

dExtendedBirthArea = CivDict({
})

dBirthAreaExceptions = CivDict({
iSpain :		[],
}, [])

### Core Area ###

dCoreArea = CivDict({
iMaya : 		((34, 57), 	(37, 59)),
iInca : 		((46, 33), 	(52, 38)),
iAztecs : 		((27, 59), 	(31, 61)),
iSpain : 		((0, 0), 	(0, 0)),	#No core for colonies
iPortugal : 	((0, 0), 	(0, 0)),	#No core for colonies
iEngland : 		((0, 0), 	(0, 0)),	#No core for colonies
iFrance : 		((0, 0), 	(0, 0)),	#No core for colonies
iNetherlands :	((0, 0), 	(0, 0)),	#No core for colonies
iHawaii :		((12, 47), 	(14, 50)),
iRussia :		((0, 0), 	(0, 0)),	#No core for colonies
iAmerica : 		((48, 80), 	(64, 87)),
iArgentina : 	((53, 15), 	(58, 20)),
iMexico :		((26, 57), 	(32, 64)),
iColombia :		((46, 49), 	(49, 54)),
iBrazil : 		((65, 26), 	(72, 32)),
iCanada : 		((45, 83), 	(59, 90)),
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
iInca : 		((49, 36), 	(49, 36)),
iAztecs : 		((30, 60), 	(30, 60)),
iSpain : 		((54, 59), 	(54, 59)),
iPortugal : 	((67, 27), 	(67, 27)),
iEngland : 		((50, 77), 	(50, 77)),
iFrance : 		((58, 89), 	(58, 89)),
iNetherlands :	((56, 81), 	(56, 81)),
iHawaii :		((56, 81), 	(56, 81)),
iRussia :		((56, 81), 	(56, 81)),
iAmerica : 		((51, 79), 	(51, 79)),
iArgentina : 	((57, 16), 	(57, 16)),
iMexico :		((30, 60), 	(30, 60)),
iColombia :		((48, 49), 	(48, 49)),
iBrazil : 		((70, 28), 	(70, 28)),
iCanada : 		((52, 87), 	(52, 87)),
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
iInca : 		((49, 36), 	(49, 36)),
iAztecs : 		((30, 60), 	(30, 60)),
iSpain : 		((54, 59), 	(54, 59)),
iPortugal : 	((67, 27), 	(67, 27)),
iEngland : 		((50, 77), 	(50, 77)),
iFrance : 		((58, 89), 	(58, 89)),
iNetherlands :	((56, 81), 	(56, 81)),
iHawaii :		((56, 81), 	(56, 81)),
iRussia :		((56, 81), 	(56, 81)),
iAmerica : 		((51, 79), 	(51, 79)),
iArgentina : 	((57, 16), 	(57, 16)),
iMexico :		((30, 60), 	(30, 60)),
iColombia :		((48, 49), 	(48, 49)),
iBrazil : 		((70, 28), 	(70, 28)),
iCanada : 		((52, 87), 	(52, 87)),
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