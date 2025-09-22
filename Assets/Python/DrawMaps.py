import os
import csv

from PIL import Image
from pathlib import Path


iWorldX = 85
iWorldY = 122

# MacAurther TODO: Update this alongside Consts
iNumCivs = 38
# 0				1				2				3				4				5				6				7				8				9
(iAmerica, 		iArgentina, 	iAztecs, 		iBrazil, 		iCanada, 		iChimu,			iColombia, 		iEngland, 		iFrance, 		iHaiti,			
iHaudenosaunee,	iHawaii,		iInca,			iInuit,			iLakota,		iMaya,			iMexico, 		iMississippi,	iMuisca,		iNetherlands, 	
iNorse,			iPeru,			iPortugal, 		iPuebloan,		iPurepecha,		iRussia,		iSpain, 		iTeotihuacan,	iTiwanaku,		iVenezuela,		
iWari,			iZapotec,		iIndependent, 	iIndependent2, 	iIndependent3,	iNative,		iMinor, 		iBarbarian) = tuple(Civ(i) for i in range(iNumCivs))

iNumRegions = 52
# 0				1				2				3				4				5				6				7				8				9
(rAlaska, 		rYukon,         rNunavut, 		rGreenland,     rIceland,       rNorthCascadia, rNorthPlains, 	rOntario, 		rQuebec, 		rNewFoundland, 	
rSouthCascadia, rCalifornia,    rRockies,       rSouthwest,     rTexas,         rGreatPlains,   rGreatLakes,    rNewEngland,    rMidAtlantic,   rMaryland,
rRiverValley,    rCoastalPlain,  rDeepSouth,     rFlorida,       rBajaCalifornia,rSierraMadres,  rBajio,         rVeracruz,      rOaxaca,        rYucatan,       
rMesoamerica,   rCaribbean, 	rHawaii, 		rColombia, 		rVenezuela, 	rGuyana, 		rPeru, 			rBolivia, 		rAmazonas, 		rPara,          
rBahia,         rMinasGerais,   rMatoGrosso,    rParana,        rChile, 		rParaguay, 		rUruguay, 		rChaco,         rCuyo,          rPampas, 		
rPatagonia, 	rOldWorld		) = range(iNumRegions)

iNumReligions = 10
(iJudaism, iOrthodoxy, iCatholicism, iProtestantism, iIslam, iHinduism, iBuddhism, iConfucianism, iTaoism, iZoroastrianism) = range(iNumReligions)

iNumReligionMapTypes = 5
(iNone, iMinority, iPeriphery, iHistorical, iCore) = range(iNumReligionMapTypes)


dCivNames = {
	iAmerica: "America",
	iArgentina: "Argentina",
	iAztecs: "Aztecs",
	iBrazil: "Brazil",
	iCanada: "Canada",
	iChimu: "Chimu",
	iColombia: "Colombia",
	iEngland: "England",
	iFrance: "France",
	iHaiti: "Haiti",
	iHaudenosaunee: "Haudenosaunee",
	iHawaii: "Hawaii",
	iInca: "Inca",
	iInuit: "Inuit",
	iLakota: "Lakota",
	iMaya: "Maya",
	iMexico: "Mexico",
	iMississippi: "Mississippi",
	iMuisca: "Muisca",
	iNetherlands: "Netherlands",
	iNorse: "Norse",
	iPeru: "Peru",
	iPortugal: "Portugal",
	iPuebloan: "Puebloan",
	iPurepecha: "Purepehca",
	iRussia: "Russia",
	iSpain: "Spain",
	iTeotihuacan: "Teotihuacan",
	iTiwanaku: "Tiwanaku",
	iVenezuela: "Venezuela",
	iWari: "Wari",
	iZapotec: "Zapotec",
}

dReligionNames = {
	iJudaism: "Judaism",
	iOrthodoxy: "Orthodoxy",
	iCatholicism: "Catholicism",
	iProtestantism: "Protestantism",
	iIslam: "Islam",
	iHinduism: "Hinduism",
	iBuddhism: "Buddhism",
	iConfucianism: "Confucianism",
	iTaoism: "Taoism",
	iZoroastrianism: "Zoroastrianism",
}


(LAND, WATER, PEAK, CORE, HISTORICAL, CONQUEST, FOREIGN, MINORITY, PERIPHERY) = range(9)

plot_colors = {
	LAND: (175, 175, 175),
	WATER: (50, 100, 100),
	PEAK: (50, 50, 50),
	CORE: (41, 249, 255),
	HISTORICAL: (8, 179, 69),
	CONQUEST: (250, 184, 56),
	FOREIGN: (240, 64, 102),
	PERIPHERY: (250, 184, 56),
	MINORITY: (255, 220, 115),
}


dCoreArea = CivDict({
iMaya :		    ((21, 58),	(23, 60)),
iZapotec :		((12, 60), 	(16, 62)),
iTeotihuacan :  ((13, 65),	(15, 67)),
iTiwanaku :	    ((25, 22),	(28, 26)),
iWari :		    ((22, 32),	(24, 35)),
iMississippi :  ((27, 81),	(35, 85)),
iPuebloan :		((12, 85),	(18, 88)),
iMuisca :		((30, 41),	(33, 44)),
iNorse :		((0, 0), 	(0, 0)),	# No core for Europeans
iChimu :		((19, 35),	(22, 38)),
iInuit :		((10, 117),	(19, 121)),
iInca :		    ((20, 27),	(27, 31)),
iPurepecha :	((8, 66),	(11, 69)),
iAztecs :		((12, 63),	(16, 66)),
iHaudenosaunee :	    ((36, 84),	(40, 87)),
iLakota :		((25, 89),	(28, 92)),
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
iMexico :		((8, 59),	(18, 70)),
iColombia :	    ((27, 41),	(33, 47)),
iPeru :		    ((19, 26),	(25, 37)),
iBrazil :		((35, 15),	(49, 25)),
iVenezuela :	((34, 44),	(44, 49)),
iCanada :		((35, 86),	(51, 94)),
})


dCoreAreaExceptions = CivDict({
iChimu :		[(22, 35)],
iMississippi :  [(33, 85), (32, 85), (30, 85), (32, 84), (30, 84), (34, 85), (35, 84), (34, 84), (35, 85), (31, 84), (31, 85), (33, 84)],
iPuebloan :	    [(19, 80)],
iInca :		    [(27, 31)],
iHaudenosaunee :	    [(37, 86), (36, 87), (37, 87), (38, 87), (36, 86)],
iAmerica :	    [(35, 88), (40, 88), (39, 88), (37, 89), (38, 89), (36, 88), (37, 86), (41, 88), (40, 89), (35, 87), (44, 89), (37, 88), (42, 88), (37, 79), (36, 89), (38, 87), (38, 88), (35, 86), (42, 89), (43, 89), (35, 89), (36, 87), (39, 89), (36, 86), (37, 87), (41, 89)],
iPeru :		    [(25, 37), (25, 35), (25, 38), (25, 36)],
iBrazil :		[(35, 24), (35, 22), (40, 22), (38, 22), (42, 25), (41, 23), (38, 20), (37, 20), (42, 20), (36, 21), (43, 25), (35, 25), (40, 23), (42, 24), (41, 22), (40, 19), (38, 21), (35, 21), (43, 23), (42, 21), (38, 24), (38, 23), (37, 23), (41, 25), (36, 22), (39, 20), (40, 24), (37, 21), (41, 21), (35, 20), (43, 22), (40, 20), (37, 25), (36, 23), (39, 21), (36, 24), (37, 22), (41, 24), (42, 22), (41, 19), (39, 23), (40, 25), (41, 20), (35, 23), (40, 21), (38, 25), (37, 24), (39, 25), (36, 25), (35, 19), (42, 23), (39, 22), (36, 20), (39, 24)],
iVenezuela :	[(34, 45), (34, 44), (34, 49), (35, 44), (35, 49)],
iCanada :		[(47, 87), (45, 89), (43, 86), (44, 88), (38, 86), (42, 86), (46, 87), (39, 87), (47, 86), (45, 88), (47, 89), (46, 88), (42, 87), (39, 86), (44, 86), (45, 87), (47, 88), (40, 86), (46, 89), (41, 87), (44, 87), (45, 86), (40, 87), (41, 86), (43, 87), (43, 88), (46, 86)],
}, [])

tSpreadFactors = (
# Judaism
{
	iCore :			[rOldWorld],
	iHistorical :	[],
	iPeriphery :	[],
	iMinority :		[rOntario, rNewEngland, rMidAtlantic, rCalifornia, rBahia, rPampas],
},
# Orthodoxy
{
	iCore :			[rOldWorld],
	iHistorical : 	[rAlaska],
	iPeriphery : 	[rNorthPlains],
	iMinority :		[rMidAtlantic],
},
# Catholicism
{
	iCore :			[rBajio, rColombia, rPeru, rParaguay, rOldWorld],
	iHistorical :	[rQuebec, rFlorida, rTexas, rSierraMadres, rYucatan, rOaxaca, rVeracruz, rBajaCalifornia, rMesoamerica, rCaribbean, rVenezuela, rGuyana, rBolivia, rGuyana, rAmazonas, rBahia, rPara, rMinasGerais, rMatoGrosso, rParana, rChile, rUruguay, rChaco, rCuyo, rPampas, rPatagonia, rMaryland],
	iPeriphery :	[rOntario, rNewEngland, rMidAtlantic, rSouthwest, rCalifornia, rRockies, rSouthCascadia, rDeepSouth],
	iMinority :		[],
},
# Protestantism
{
	iCore :			[rOntario, rNewEngland, rMidAtlantic, rCoastalPlain, rTexas, rDeepSouth, rGreatLakes, rOldWorld],
	iHistorical :	[rAlaska, rNunavut, rNorthPlains, rNewFoundland, rSouthwest, rGreatPlains, rCalifornia, rRockies, rSouthCascadia, rNorthCascadia, rHawaii, rGuyana, rMaryland],
	iPeriphery :	[rQuebec, rMesoamerica, rPeru, rChile, rMinasGerais, rGreenland, rIceland],
	iMinority :		[],
},
# Islam
{
	iCore :			[rOldWorld],
	iHistorical :	[],
	iPeriphery :	[],
	iMinority : 	[rOntario, rMidAtlantic, rGuyana],
},
# Hinduism
{
	iCore :			[rOldWorld],
	iHistorical :	[],
	iPeriphery :	[rGuyana],
	iMinority :		[],
},
# Buddhism
{
	iCore :			[rOldWorld],
	iHistorical :	[],
	iPeriphery :	[],
	iMinority :		[rCalifornia],
},
# Confucianism
{
	iCore :			[rOldWorld],
	iHistorical :	[],
	iPeriphery :	[],
	iMinority :		[],
},
# Taoism
{
	iCore :			[rOldWorld],
	iHistorical :	[],
	iPeriphery :	[],
	iMinority :		[],
},
# Zoroastrianism
{
	iCore :			[rOldWorld],
	iHistorical :	[],
	iPeriphery :	[],
	iMinority :		[],
},
)


def iterate_map(file_path):
	full_file_path = Path.cwd() / "Assets/Maps" / file_path
	
	with open(full_file_path) as file:
		for y, line in enumerate(csv.reader(file)):
			for x, value in enumerate(line):
				if not value:
					yield (x, y), 0
				else:
					yield (x, y), int(value)


def is_core(iCiv, tile):
	x, y = tile
	
	(tBLx, tBLy), (tTRx, tTRy) = dCoreArea[iCiv]
	lExceptions = dCoreAreaExceptions.get(iCiv, [])
	
	return tBLx <= x <= tTRx and tBLy <= y <= tTRy and (x, y) not in lExceptions


def iterate_plot_types(iCiv):
	civ_name = dCivNames[iCiv]

	settler_values = iterate_map(f"Settler/{civ_name}.csv")
	war_values = iterate_map(f"War/{civ_name}.csv")
	terrain_values = iterate_map("Export/BaseTerrain.csv")
	
	for ((x, y), iSettlerValue), (_, iWarValue), (_, iTerrainValue) in zip(settler_values, war_values, terrain_values):
		if iTerrainValue == 2:
			yield (x, y), PEAK
			
		elif iTerrainValue != 0 and is_core(iCiv, (x, iWorldY-1-y)):
			yield (x, y), CORE
		
		elif iSettlerValue > 0:
			yield (x, y), HISTORICAL
		
		elif iWarValue > 1:
			yield (x, y), CONQUEST
		
		elif iTerrainValue == 0:
			yield (x, y), WATER
		
		else:
			yield (x, y), LAND


def draw_stability_map(iCiv):
	civ_name = dCivNames[iCiv]

	image = Image.new("RGB", (iWorldX, iWorldY), "white")
	pixels = image.load()

	for (x, y), plot_type in iterate_plot_types(iCiv):
		pixels[x, y] = plot_colors[plot_type]
	
	image = image.resize((iWorldX * 4, iWorldY * 4))
	
	image_path = Path.cwd() / "Maps" / f"{civ_name}.png"
	image.save(image_path)


def getSpreadFactor(iReligion, iRegion):
	if iRegion < 0: 
		return -1
	
	return next((iFactor for iFactor, lRegions in tSpreadFactors[iReligion].items() if iRegion in lRegions), iNone)


def iterate_religion_spread_factors(iReligion):
	region_values = iterate_map("Regions.csv")
	terrain_values = iterate_map("Export/BaseTerrain.csv")
	
	for ((x, y), iRegion), (_, iTerrain) in zip(region_values, terrain_values):
		iSpreadFactor = getSpreadFactor(iReligion, iRegion)
	
		if iTerrain == 0:
			yield (x, y), WATER
	
		elif iTerrain == 2:
			yield (x, y), PEAK
		
		elif iSpreadFactor == iCore:
			yield (x, y), CORE
		
		elif iSpreadFactor == iHistorical:
			yield (x, y), HISTORICAL
		
		elif iSpreadFactor == iPeriphery:
			yield (x, y), PERIPHERY
		
		elif iSpreadFactor == iMinority:
			yield (x, y), MINORITY
		
		else:
			yield (x, y), LAND
			


def draw_religion_map(iReligion):
	image = Image.new("RGB", (iWorldX, iWorldY), "white")
	pixels = image.load()
	
	for (x, y), spread_factor_type in iterate_religion_spread_factors(iReligion):
		pixels[x, y] = plot_colors[spread_factor_type]
	
	image = image.resize((iWorldX * 4, iWorldY * 4))
	
	image_path = Path.cwd() / "Maps/Religions" / f"{dReligionNames[iReligion]}.png"
	image.save(image_path)


def draw_maps():
	for iCiv in dCivNames:
		draw_stability_map(iCiv)
	
	for iReligion in range(iNumReligions):
		draw_religion_map(iReligion)


if __name__ == "__main__":
	draw_maps()