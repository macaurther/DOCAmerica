from Core import *
from RFCUtils import *
from Events import handler

# Space Elevator effect: +1 commerce per satellite built
@handler("unitBuilt")
def spaceElevatorEffect(city, unit):
	if unit.getUnitType() == iSatellite:
		city = getBuildingCity(iNASA)
		if city:
			city.changeBuildingYieldChange(infos.building(iNASA).getBuildingClassType(), YieldTypes.YIELD_COMMERCE, 1)


# Space Elevator effect: +5 commerce per space projectBuilt
@handler("projectBuilt")
def spaceElevatorProjectEffect(city, iProject):
	if infos.project(iProject).isSpaceship():
		city = getBuildingCity(iNASA)
		if city:
			city.changeBuildingYieldChange(infos.building(iNASA).getBuildingClassType(), YieldTypes.YIELD_COMMERCE, 5)
			

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
		
# Mount Vernon effect: free Great Person whenever a Great General is born
@handler("greatPersonBorn")
def mountVernonEffect(unit, iPlayer):
	if infos.unit(unit).getLeaderExperience() > 0 and player(iPlayer).isHasBuildingEffect(iMountVernon):
		city = cities.owner(iPlayer).where(lambda city: city.getGreatPeopleProgress() > 0).maximum(lambda city: city.getGreatPeopleProgress())
		if city:
			iGreatPerson = find_max(range(iNumUnits), lambda iUnit: city.getGreatPeopleUnitProgress(iUnit)).result
			if iGreatPerson >= 0:
				player(iPlayer).createGreatPeople(iGreatPerson, False, False, city.getX(), city.getY())

# West Point effect: Great General threshold is reset when one of your Greneals dies in battle
@handler("combatResult")
def westPointEffect(winningUnit, losingUnit):
	if player(losingUnit).isHasBuildingEffect(iWestPoint):
		if any(infos.promotion(iPromotion).isLeader() and losingUnit.isHasPromotion(iPromotion) for iPromotion in infos.promotions()):
			player(losingUnit).restoreGeneralThreshold()