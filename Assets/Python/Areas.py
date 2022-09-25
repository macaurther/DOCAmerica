from Consts import *

# Peak that change to hills during the game, like Bogota
lPeakExceptions = []
	
### Capitals ###

dCapitals = CivDict({
iMaya :			(36, 49), # Tikal
iInca :			(36, 49), # Cuzco
iAztecs :		(36, 49), # Tenochtitlan
iSpain :		(36, 49), # Santo Domingo
iPortugal :		(36, 49), # Sao Paulo
iEngland :		(36, 49), # Jamestown
iFrance :		(36, 49), # Quebec
iNetherlands :	(36, 49), # New Amsterdam
iAmerica :		(36, 49), # Washington
iArgentina :	(36, 49), # Buenos Aires
iMexico :		(36, 49), # Mexico City
iColombia :		(36, 49), # Bogota
iBrazil :		(36, 49), # Rio de Janeiro
iCanada :		(36, 49), # Montreal
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