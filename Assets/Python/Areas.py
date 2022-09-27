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
iInca :		(36, 49),	# Lima
})

### Birth Area ###

dBirthArea = CivDict({
iMaya : 		((36, 49), 	(36, 49)),
iInca : 		((36, 49), 	(36, 49)),
iAztecs : 		((36, 49), 	(36, 49)),
iSpain : 		((36, 49), 	(36, 49)),
iPortugal : 	((36, 49), 	(36, 49)),
iEngland : 		((36, 49), 	(36, 49)),
iFrance : 		((36, 49), 	(36, 49)),
iNetherlands :	((36, 49), 	(36, 49)),
iAmerica : 		((36, 49), 	(36, 49)),
iArgentina : 	((36, 49), 	(36, 49)),
iMexico :		((36, 49), 	(36, 49)),
iColombia :		((36, 49), 	(36, 49)),
iBrazil : 		((36, 49), 	(36, 49)),
iCanada : 		((36, 49), 	(36, 49)),
})

dExtendedBirthArea = CivDict({
iInca : 	((36, 49), 	(36, 49)),
iSpain : 	((36, 49), 	(36, 49)), 	# includes Catalonia
iArgentina :((36, 49), 	(36, 49)), 	# includes Chile
})

dBirthAreaExceptions = CivDict({
iSpain :		[],
}, [])

### Core Area ###

dCoreArea = CivDict({
iMaya : 		((36, 49), 	(36, 49)),
iInca : 		((36, 49), 	(36, 49)),
iAztecs : 		((36, 49), 	(36, 49)),
iSpain : 		((36, 49), 	(36, 49)),
iPortugal : 	((36, 49), 	(36, 49)),
iEngland : 		((36, 49), 	(36, 49)),
iFrance : 		((36, 49), 	(36, 49)),
iNetherlands :	((36, 49), 	(36, 49)),
iAmerica : 		((36, 49), 	(36, 49)),
iArgentina : 	((36, 49), 	(36, 49)),
iMexico :		((36, 49), 	(36, 49)),
iColombia :		((36, 49), 	(36, 49)),
iBrazil : 		((36, 49), 	(36, 49)),
iCanada : 		((36, 49), 	(36, 49)),
})

dPeriodCoreArea = {
}

dCoreAreaExceptions = CivDict({
iSpain :	[],
}, [])

dPeriodCoreAreaExceptions = appenddict({
})

### Normal Area ###

dNormalArea = CivDict({
iMaya : 		((36, 49), 	(36, 49)),
iInca : 		((36, 49), 	(36, 49)),
iAztecs : 		((36, 49), 	(36, 49)),
iSpain : 		((36, 49), 	(36, 49)),
iPortugal : 	((36, 49), 	(36, 49)),
iEngland : 		((36, 49), 	(36, 49)),
iFrance : 		((36, 49), 	(36, 49)),
iNetherlands :	((36, 49), 	(36, 49)),
iAmerica : 		((36, 49), 	(36, 49)),
iArgentina : 	((36, 49), 	(36, 49)),
iMexico :		((36, 49), 	(36, 49)),
iColombia :		((36, 49), 	(36, 49)),
iBrazil : 		((36, 49), 	(36, 49)),
iCanada : 		((36, 49), 	(36, 49)),
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
iMaya : 		((36, 49), 	(36, 49)),
iInca : 		((36, 49), 	(36, 49)),
iAztecs : 		((36, 49), 	(36, 49)),
iSpain : 		((36, 49), 	(36, 49)),
iPortugal : 	((36, 49), 	(36, 49)),
iEngland : 		((36, 49), 	(36, 49)),
iFrance : 		((36, 49), 	(36, 49)),
iNetherlands :	((36, 49), 	(36, 49)),
iAmerica : 		((36, 49), 	(36, 49)),
iArgentina : 	((36, 49), 	(36, 49)),
iMexico :		((36, 49), 	(36, 49)),
iColombia :		((36, 49), 	(36, 49)),
iBrazil : 		((36, 49), 	(36, 49)),
iCanada : 		((36, 49), 	(36, 49)),
})

dPeriodBroaderArea = {
}

### Expansion area ###

dExpansionArea = CivDict({
iSpain :		((36, 49), 	(36, 49)),
})

dExpansionAreaExceptions = CivDict({
}, [])

### Respawn area ###

dRespawnArea = CivDict({
iInca :		((36, 49), 	(36, 49)),
})