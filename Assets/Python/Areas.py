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
iHawaii :		(56, 81), # Hilo
iRussia :		(56, 81), # Novo-Arkhangelsk
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

dExtendedBirthArea = CivDict({
iInca : 		((49, 36), 	(49, 36)),
iSpain : 		((54, 59), 	(54, 59)), 	# includes Catalonia
iArgentina : 	((57, 16), 	(57, 16)), 	# includes Chile
})

dBirthAreaExceptions = CivDict({
iSpain :		[],
}, [])

### Core Area ###

dCoreArea = CivDict({
iMaya : 		((34, 57), 	(37, 59)),
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

dPeriodCoreArea = {
}

dCoreAreaExceptions = CivDict({
iMaya :	[(34, 57), (37, 57)],
}, [])

dPeriodCoreAreaExceptions = appenddict({
})

### Normal Area ###

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
iInca : 		((49, 36), 	(49, 36)),
})