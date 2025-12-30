from Definitions import *
from Locations import *


# city descriptors
CAPITAL = "TXT_KEY_VICTORY_NAME_CAPITAL"

# building descriptors
CATHEDRALS = "TXT_KEY_VICTORY_NAME_CATHEDRALS"
SHRINES = "TXT_KEY_VICTORY_NAME_SHRINES"

# goal descriptors
FIRST_SECULAR_GOAL = "TXT_KEY_VICTORY_GOAL_SECULAR_1"
PESEDJET_GOAL = "TXT_KEY_VICTORY_GOAL_PESEDJET"


dGoals = {
	iHinduism: (
		CityDifferentGreatPeopleCount(holy_city(iHinduism), 5),
		GoldenAges(3),
		BestPopulationCities(5, subject=STATE_RELIGION, iReligion=iHinduism)
	),
	iJudaism: (
		SpecialistCount(sum(iSpecialistGreatProphet, iSpecialistGreatScientist, iSpecialistGreatStatesman), 15, subject=STATE_RELIGION, iReligion=iJudaism),
		CityCultureLevel(holy_city(iJudaism), iCultureLevelLegendary),
		AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 6, iReligion=iJudaism),
	),
	iBuddhism: (
		PeaceTurns(100),
		HappiestTurns(100),
		AllAttitude(AttitudeTypes.ATTITUDE_CAUTIOUS),
	),
	iOrthodoxy: (
		BuildingCount(iOrthodoxCathedral, 4),
		BestCultureCities(5, subject=STATE_RELIGION, iReligion=iOrthodoxy),
		NoStateReligion(iCatholicism),
	),
	iCatholicism: (
		PopeTurns(100),
		All(
			BuildingCount(iCatholicShrine, 1),
			SpecialistCount(iSpecialistGreatProphet, 12, subject=STATE_RELIGION, iReligion=iCatholicism),
		),
		LandPercent(50, subject=STATE_RELIGION, iReligion=iCatholicism),
	),
	iIslam: (
		ReligionSpreadPercent(iIslam, 40),
		CitySpecialistCount(holy_city(iIslam), great_people(), 7, subject=STATE_RELIGION),
		BuildingCount(religious_buildings(shrine).named(SHRINES), 5),
	),
	iProtestantism: (
		FirstDiscover(iCivilLiberties, iSocialContract, iEconomics),
		SpecialistCount((iSpecialistGreatMerchant, 5), (iSpecialistGreatEngineer, 5), subject=STATE_RELIGION, iReligion=iProtestantism),
		StateReligionPercent(iProtestantism, 50, bSecular=True),
	),
	iPaganVictory: (
		BuildingCount(iPaganTemple, 25, subject=WORLD),
		NoReligionPercent(50),
	),
	iSecularVictory: (
		BuildingCount(religious_buildings(cathedral).named(CATHEDRALS), 7, desc_key=FIRST_SECULAR_GOAL),
		All(
			BuildingCount(iUniversity, 25, subject=SECULAR),
			SpecialistCount(
				(iSpecialistGreatScientist, 10),
				(iSpecialistGreatStatesman, 10),
				subject=SECULAR,
			),
		),
		BestTechPlayers(5, subject=SECULAR),
	),
}

dAdditionalPaganGoal = {
	iAngakkuq: FeatureCount(iSeaIce, 20),
	iAsatru: UnitLevelCount(5, 5),
	iAtua: All(
		ResourceCount(iPearls, 4),
		TerrainCount(iOcean, 50),
	),
	iDruidism: FeatureCount(sum(iForest, iBog), 20),
	iGaiwiio: FeatureCount(iForest, 20),
	iInti: GoldPercent(75),
	iKachina: FeatureCount(sum(iForest, iBog), 20),
	iMidewiwin: All(
		ResourceCount(iCorn, 4),
		ImprovementCount(iFarm, 20),
	),
	iRodnovery: ResourceCount(iFur, 7),
	iTeotlMaya: CombatFood(500),
	iTeotlAztec: SacrificeGoldenAges(30),
	iWocekiya: ResourceCount(iBison, 7),
	iYoruba: ResourceCount((iBison, 8), (iGems, 6)),
}


for iReligion in range(iNumReligions):
	for index, goal in enumerate(dGoals[iReligion]):
		title_key = "TXT_KEY_VICTORY_TITLE_%s%s" % (infos.religion(iReligion).getText().upper()[:4], index+1)
		goal.options["title_key"] = title_key


def descriptions(iReligion):
	for goal in dGoals[iReligion]:
		print goal.description()

def pagans():
	for iPaganReligion in sorted(dAdditionalPaganGoal.keys()):
		print dAdditionalPaganGoal[iPaganReligion].description()