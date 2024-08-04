import sys

scenario = sys.argv[1]

sourceFile = open(scenario + "_raw.CivBeyondSwordWBSave", "r")

# Erase dest file
destFile = open(scenario + "_proc.CivBeyondSwordWBSave", "w")
destFile.write("")
destFile.close()

# Open dest file as append
destFile = open(scenario + "_proc.CivBeyondSwordWBSave", "a")


keepTags = {
"RouteType=",
"ImprovementType=",
"BeginUnit",
"UnitType=",
"UnitOwner=",
"EndUnit",
"BeginCity",
"CityOwner=",
"CityName=",
"CityPopulation=",
"BuildingType=",
"ReligionType=",
"HolyCityReligionType=",
"FreeSpecialistType=",
"BeginCulture",
"Civilization=",
"EndCulture",
"YearFounded=",
"YearAcquired=",
"PreviousOwner=",
"EndCity",
}



startReached = False

line = "init"
block = ""
bBlockInProg = False
bBlockComplete = False
bKeepBlock = False

iLineCounter = 0

while line:
	line = sourceFile.readline()
	if not line:
		break
	
	if "### Plot Info ###" in line:
		startReached = True
		destFile.write(line)
		continue
	elif not startReached:
		continue
	elif "BeginPlot" in line:
		bBlockInProg = True
	elif "EndPlot" in line:
		bBlockComplete = True
	
	
	if bBlockInProg:
		if "x=" in line and "y=" in line:
			block += line
		elif "BeginPlot" in line or "EndPlot" in line:
			block += line
		for keepTag in keepTags:
			if keepTag in line:
				block += line
				bKeepBlock = True
				break
		
	
	if bBlockComplete:
		if bKeepBlock:
			destFile.write(block)
			bKeepBlock = False
		bBlockInProg = False
		bBlockComplete = False
		
		# clear block
		block = ""
	
	iLineCounter += 1
	if iLineCounter % 1000 == 0:
		print("Line " + str(iLineCounter))
	
	
destFile.close()
sourceFile.close()