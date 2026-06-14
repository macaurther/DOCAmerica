from Core import *
from RFCUtils import *
from Events import handler


@handler("buildingBuilt")
def yachaywasiEffect(city, iBuilding):
	if iBuilding == iYachaywasi:
		iNumPeaks = plots.city_radius(city).where(lambda plot: plot.isPeak()).count()
		city.setBuildingCommerceChange(infos.building(iYachaywasi).getBuildingClassType(), CommerceTypes.COMMERCE_RESEARCH, iNumPeaks)

# Mount Vernon effect: free Great Person whenever a Great General is born
@handler("greatPersonBorn")
def mountVernonEffect(unit, iPlayer):
	if infos.unit(unit).getLeaderExperience() > 0 and player(iPlayer).isHasBuildingEffect(iMountVernon):
		city = cities.owner(iPlayer).where(lambda city: city.getGreatPeopleProgress() > 0).maximum(lambda city: city.getGreatPeopleProgress())
		if city:
			iGreatPerson = find_max(range(iNumUnits), lambda iUnit: city.getGreatPeopleUnitProgress(iUnit)).result
			if iGreatPerson >= 0:
				player(iPlayer).createGreatPeople(iGreatPerson, False, False, city.getX(), city.getY())

# Empire State Building effect: +1 Gold per population
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
