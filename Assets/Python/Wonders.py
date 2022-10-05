from Core import *
from RFCUtils import *
from Events import handler

# Space Elevator effect: +1 commerce per satellite built
@handler("unitBuilt")
def spaceElevatorEffect(city, unit):
	if unit.getUnitType() == iSatellite:
		city = getBuildingCity(iSpaceElevator)
		if city:
			city.changeBuildingYieldChange(infos.building(iSpaceElevator).getBuildingClassType(), YieldTypes.YIELD_COMMERCE, 1)


# Space Elevator effect: +5 commerce per space projectBuilt
@handler("projectBuilt")
def spaceElevatorProjectEffect(city, iProject):
	if infos.project(iProject).isSpaceship():
		city = getBuildingCity(iSpaceElevator)
		if city:
			city.changeBuildingYieldChange(infos.building(iSpaceElevator).getBuildingClassType(), YieldTypes.YIELD_COMMERCE, 5)
			

@handler("cityGrowth")
def empireStateBuildingOnGrowth(city):
	if city.isHasBuildingEffect(iEmpireStateBuilding):
		empireStateBuildingEffect(city)
	

@handler("buildingBuilt")
def empireStateBuildingWhenBuilt(city, iBuilding):
	if iBuilding == iEmpireStateBuilding:
		empireStateBuildingEffect(city)

def empireStateBuildingEffect(city):
	city.setBuildingCommerceChange(infos.building(iEmpireStateBuilding).getBuildingClassType(), CommerceTypes.COMMERCE_GOLD, city.getPopulation())


@handler("buildingBuilt")
def machuPicchuEffect(city, iBuilding):
	if iBuilding == iMachuPicchu:
		iNumPeaks = plots.city_radius(city).where(lambda plot: plot.isPeak()).count()
		city.setBuildingCommerceChange(infos.building(iMachuPicchu).getBuildingClassType(), CommerceTypes.COMMERCE_GOLD, iNumPeaks * 2)