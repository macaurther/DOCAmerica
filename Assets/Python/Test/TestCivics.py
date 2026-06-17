from Civics import *
from unittest import *

# #MacAurther: Ported from base DoC to DOCAmerica.
# Civic categories: iCivicsExecutive, iCivicsAdministration, iCivicsLabor, iCivicsEconomy, iCivicsSociety, iCivicsExpansion
# Player 0 = Maya; default civics: iElders, iDecentralization, iTraditionalism, iReciprocity, iAnimism, iSettlement


class TestCivics(TestCase):

	def test_initial_values(self):
		gc.getPlayer(0).setCivics(iCivicsExecutive, iStateParty)
		gc.getPlayer(0).setCivics(iCivicsAdministration, iPoliceState)
		gc.getPlayer(0).setCivics(iCivicsSociety, iEgalitarianism)
		gc.getPlayer(0).setCivics(iCivicsEconomy, iPublicWelfare)
		gc.getPlayer(0).setCivics(iCivicsLabor, iMechanization)
		gc.getPlayer(0).setCivics(iCivicsExpansion, iManifestDestiny)

		civics = Civics.player(0)

		try:
			self.assertEqual(civics.iExecutive, iStateParty)
			self.assertEqual(civics.iAdministration, iPoliceState)
			self.assertEqual(civics.iSociety, iEgalitarianism)
			self.assertEqual(civics.iEconomy, iPublicWelfare)
			self.assertEqual(civics.iLabor, iMechanization)
			self.assertEqual(civics.iExpansion, iManifestDestiny)
		finally:
			gc.getPlayer(0).setCivics(iCivicsExecutive, iElders)
			gc.getPlayer(0).setCivics(iCivicsAdministration, iDecentralization)
			gc.getPlayer(0).setCivics(iCivicsSociety, iAnimism)
			gc.getPlayer(0).setCivics(iCivicsEconomy, iReciprocity)
			gc.getPlayer(0).setCivics(iCivicsLabor, iTraditionalism)
			gc.getPlayer(0).setCivics(iCivicsExpansion, iSettlement)

	def test_active(self):
		gc.getPlayer(0).setCivics(iCivicsExecutive, iStateParty)

		civics = Civics.player(0)

		try:
			self.assertEqual(civics.active(iStateParty), True)
			self.assertEqual(civics.active(iElders), False)
			self.assertEqual(civics.active(iAnimism), True)
			self.assertEqual(civics.active(iEgalitarianism), False)
		finally:
			gc.getPlayer(0).setCivics(iCivicsExecutive, iElders)

	def test_contains_single(self):
		gc.getPlayer(0).setCivics(iCivicsExecutive, iStateParty)

		civics = Civics.player(0)

		try:
			self.assertEqual(iStateParty in civics, True)
			self.assertEqual(iElders in civics, False)
			self.assertEqual(iAnimism in civics, True)
			self.assertEqual(iEgalitarianism in civics, False)
		finally:
			gc.getPlayer(0).setCivics(iCivicsExecutive, iElders)

	def test_contains_any(self):
		gc.getPlayer(0).setCivics(iCivicsExecutive, iStateParty)

		civics = Civics.player(0)

		try:
			self.assertEqual((iElders, iStateParty) in civics, True)
			self.assertEqual((iElders, iRepresentatives) in civics, False)
			self.assertEqual((iRepresentatives, iStateParty) in civics, True)
			self.assertEqual((iAnimism, iStateParty) in civics, True)
		finally:
			gc.getPlayer(0).setCivics(iCivicsExecutive, iElders)

	def test_contains_all(self):
		gc.getPlayer(0).setCivics(iCivicsExecutive, iStateParty)
		gc.getPlayer(0).setCivics(iCivicsEconomy, iPublicWelfare)

		civics = Civics.player(0)

		try:
			self.assertEqual((iStateParty, iPublicWelfare) in civics, True)
			self.assertEqual((iElders, iPublicWelfare) in civics, False)
			self.assertEqual((iStateParty, iRedistribution) in civics, False)
			self.assertEqual((iStateParty, iAnimism) in civics, True)
		finally:
			gc.getPlayer(0).setCivics(iCivicsExecutive, iElders)
			gc.getPlayer(0).setCivics(iCivicsEconomy, iReciprocity)

	def test_contain_combined(self):
		gc.getPlayer(0).setCivics(iCivicsExecutive, iStateParty)
		gc.getPlayer(0).setCivics(iCivicsEconomy, iPublicWelfare)

		civics = Civics.player(0)

		try:
			self.assertEqual((iStateParty, iPublicWelfare) in civics, True)
			self.assertEqual((iElders, iStateParty, iPublicWelfare) in civics, True)
			self.assertEqual((iElders, iPublicWelfare) in civics, False)
			self.assertEqual((iElders, iStateParty, iFreeEnterprise, iPublicWelfare) in civics, True)
			self.assertEqual((iStateParty, iFreeEnterprise) in civics, False)
		finally:
			gc.getPlayer(0).setCivics(iCivicsExecutive, iElders)
			gc.getPlayer(0).setCivics(iCivicsEconomy, iReciprocity)

	def test_not_contain(self):
		gc.getPlayer(0).setCivics(iCivicsExecutive, iStateParty)

		civics = Civics.player(0)

		try:
			self.assertEqual(iStateParty not in civics, False)
			self.assertEqual(iElders not in civics, True)
			self.assertEqual((iElders, iRepresentatives) not in civics, True)
			self.assertEqual((iElders, iStateParty) not in civics, False)
		finally:
			gc.getPlayer(0).setCivics(iCivicsExecutive, iElders)

	def test_of(self):
		civics = Civics.of(iStateParty, iPoliceState)

		self.assertEqual(iStateParty in civics, True)
		self.assertEqual(iPoliceState in civics, True)
		self.assertEqual(iAnimism in civics, False)
		self.assertEqual((iStateParty, iPoliceState) in civics, True)
		self.assertEqual((iElders, iStateParty) in civics, True)
		self.assertEqual((iMinarchy, iPoliceState) in civics, True)
		self.assertEqual(iAnimism not in civics, True)
		self.assertEqual(iElders not in civics, True)
		self.assertEqual(iStateParty not in civics, False)

	def test_notcivics_single(self):
		civics = notcivics(iElders)

		self.assertEqual(civics, (iChief, iDespot, iMonarch, iAristocrats, iGodKing, iCouncil,
			iCaptains, iProprietors, iViceroys, iTrustees, iGovernors, iColonialAssembly, iHomeRule,
			iStrongman, iJunta, iSovereign, iPlutocrats, iRepresentatives, iDictator, iStateParty))

	def test_notcivics_multiple(self):
		civics = notcivics(iDespot, iMonarch, iRepresentatives)

		self.assertEqual(civics, (iElders, iChief, iAristocrats, iGodKing, iCouncil,
			iCaptains, iProprietors, iViceroys, iTrustees, iGovernors, iColonialAssembly, iHomeRule,
			iStrongman, iJunta, iSovereign, iPlutocrats, iDictator, iStateParty))


test_cases = [
	TestCivics,
]

suite = TestSuite([makeSuite(case) for case in test_cases])
TextTestRunner(verbosity=2).run(suite)
