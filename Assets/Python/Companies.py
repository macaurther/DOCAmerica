from CvPythonExtensions import *

from Core import *
from Locations import *
from Events import handler


dCompanyTechs = {
	iFurTrade         : [iExploration],
	iTradingCompany   : [iExploration],
	iCerealIndustry   : [iEconomics, iBiology],
	iFishingIndustry  : [iEconomics],
	iTextileIndustry  : [iEconomics, iThermodynamics],
	iSteelIndustry    : [iEconomics, iMetallurgy],
	iOilIndustry      : [iEconomics],
	iLuxuryIndustry   : [iEconomics],
}

tCompaniesLimit = (10, 12, 16, 10, 12, 12, 6, 10) # kind of arbitrary currently, see how this plays out

dCompanyExpiry = defaultdict({
	iFurTrade : 1900,
	iTradingCompany : 1800,
	iTextileIndustry : 1920,
}, 2020)
					
	
@handler("cityAcquired")
def verifyCorporations(iOwner, iPlayer, city):
	for iCorporation in range(iNumCorporations):
		if city.isHasCorporation(iCorporation):
			if getCityValue(city, iCorporation) < 0:
				city.setHasCorporation(iCorporation, False, True, True)


@handler("BeginGameTurn")
def checkCompanies(iGameTurn):
	for iCompany in infos.corporations().periodic_iter(iNumCorporations / 2):
		checkCompany(iCompany, iGameTurn)


def isCompanyValid(iCompany):
	return turn() <= year(dCompanyExpiry[iCompany])


def getCompanyLimit(iCompany):
	if not isCompanyValid(iCompany):
		return 0
	
	return tCompaniesLimit[iCompany]
	
	
def canHaveCompany(iCompany, iPlayer):
	return all(team(iPlayer).isHasTech(iTech) for iTech in dCompanyTechs[iCompany])
	

def checkCompany(iCompany, iGameTurn):
	iMaxCompanies = getCompanyLimit(iCompany)
		
	# count the number of companies
	iCompanyCount = players.major().alive().sum(lambda p: player(p).countCorporations(iCompany))
			
	# return if gameturn is beyond company fall date and removed from all cities
	if iMaxCompanies == 0 and iCompanyCount == 0:
		return
	
	# select all cities for players that can have the company
	positiveCities, negativeCities = players.major().where(lambda p: canHaveCompany(iCompany, p)).cities().split(lambda city: getCityValue(city, iCompany) > player(city).countCorporations(iCompany) * 2)
	
	# remove from cities with negative value
	for city in negativeCities.corporation(iCompany).sort(lambda city: getCityValue(city, iCompany), True):
		if getCityValue(city, iCompany) <= player(city).countCorporations(iCompany) * 2:
			city.setHasCorporation(iCompany, False, True, True)
	
	companyCities, availableCities = positiveCities.split(lambda city: city.isHasCorporation(iCompany))
	
	# if company can still spread, select the most attractive city without the company
	if iCompanyCount < iMaxCompanies:
		city = availableCities.maximum(lambda city: getCityValue(city, iCompany) * 10 + rand(10))
		if city:
			city.setHasCorporation(iCompany, True, True, True)
	
	# if too many cities have the company, remove it from the least attractive city that has it
	elif iCompanyCount > iMaxCompanies:
		city = companyCities.minimum(lambda city: getCityValue(city, iCompany) * 10 + rand(10))
		if city:
			city.setHasCorporation(iCompany, False, True, True)


def getCityValue(city, iCompany):
	iValue = 2
	
	iOwner = city.getOwner()
	iOwnerCiv = civ(iOwner)
	owner = player(city)
	ownerTeam = team(city)

	# Trade Company Civic increases likeliness for trading company
	if iCompany == iTradingCompany and has_civic(owner, iTradeCompany):
		iValue += 4

	# Free Enterprise increases likeliness for all companies
	if has_civic(owner, iFreeEnterprise):
		iValue += 1

	# Dutch UP
	if iOwnerCiv == iNetherlands:
		if iCompany == iTradingCompany:
			iValue += 5
		else:
			iValue += 3
			
	elif iCompany == iTradingCompany:
		if city not in cities.region(rCaribbean) and not city.isHasRealBuilding(unique_building(city.getOwner(), iTradingCompanyBuilding)):
			return -1
		if city in cities.region(rCaribbean):
			iValue += 1
	
	# trade companies and fishing industry - coastal cities only
	if iCompany in [iTradingCompany, iFishingIndustry]:
		if not city.isCoastal(20):
			return -1
	
	# various bonuses	
	if iCompany == iFurTrade:
		if city.hasBuilding(unique_building(iOwner, iTradingPost)): iValue += 3

	elif iCompany == iTradingCompany:
		if city.hasBuilding(unique_building(iOwner, iHarbor)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iCustomsHouse)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iBank)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iWarehouse)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iTradingCompanyBuilding)): iValue += 2

	elif iCompany == iCerealIndustry:
		if city.hasBuilding(unique_building(iOwner, iGranary)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iSewer)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iEstate)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iSupermarket)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iVerticalFarm)): iValue += 1

	elif iCompany == iFishingIndustry:
		if city.hasBuilding(unique_building(iOwner, iLighthouse)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iHarbor)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iWharf)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iSupermarket)): iValue += 1
		
	elif iCompany == iTextileIndustry:
		if city.hasBuilding(unique_building(iOwner, iMarket)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iWeaver)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iWarehouse)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iTextileMill)): iValue += 3
		if city.hasBuilding(unique_building(iOwner, iManufactory)): iValue += 2

	elif iCompany == iSteelIndustry:
		if city.hasBuilding(unique_building(iOwner, iFactory)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iCoalPlant)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iRailwayStation)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iSteelMill)): iValue += 3
		if city.hasBuilding(unique_building(iOwner, iIronworks)): iValue += 3

	elif iCompany == iOilIndustry:
		if city.hasBuilding(unique_building(iOwner, iBank)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iDistillery)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iIndustrialPark)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iContainerTerminal)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iStockExchange)): iValue += 3

	elif iCompany == iLuxuryIndustry:
		if city.hasBuilding(unique_building(iOwner, iFactory)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iTavern)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iDepartmentStore)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iHotel)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iNationalGallery)): iValue += 3
	
	# needs at least a few requirements
	if iValue <= 0:
		return -1

	# trade routes
	iValue += city.getTradeRoutes() - 1
	
	# resources
	iTempValue = 0
	bFound = False
	for i in range(6):
		iBonus = infos.corporation(iCompany).getPrereqBonus(i)
		if iBonus > -1:
			if city.getNumBonuses(iBonus) > 0: 
				bFound = True
				if iCompany in [iFishingIndustry, iCerealIndustry, iTextileIndustry]:
					iTempValue += city.getNumBonuses(iBonus)
				elif iCompany in [iFurTrade, iOilIndustry]:
					iTempValue += city.getNumBonuses(iBonus) * 4
				else:
					iTempValue += city.getNumBonuses(iBonus) * 2
	
	# Brazilian UP: sugar counts as oil for Oil Industry
	if iOwnerCiv == iBrazil and iCompany == iOilIndustry:
		if city.getNumBonuses(iSugar) > 0:
			bFound = True
			iTempValue += city.getNumBonuses(iSugar) * 3
				
	if not bFound: 
		return -1
	
	iValue += iTempValue
	
	# competition
	if not iOwnerCiv == iNetherlands:	# Netherlands UP
		if iCompany == iCerealIndustry and city.isHasCorporation(iFishingIndustry): iValue /= 2
		elif iCompany == iFishingIndustry and city.isHasCorporation(iCerealIndustry): iValue /= 2
		elif iCompany == iSteelIndustry and city.isHasCorporation(iTextileIndustry): iValue /= 2
		elif iCompany == iTextileIndustry and city.isHasCorporation(iSteelIndustry): iValue /= 2
	
	# threshold
	if iValue < 4:
		return -1
		
	iCompanyCount = player(iOwner).countCorporations(iCompany)
	iCompanyLimit = getCompanyLimit(iCompany)
	
	if iCompanyCount > iCompanyLimit / 4: iValue -= 1
	if iCompanyCount > iCompanyLimit / 2: iValue -= 1
	
	return iValue