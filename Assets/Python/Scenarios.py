from Core import *

from Scenario0AD import scenario0AD
from Scenario1500AD import scenario1500AD
from Scenario1750AD import scenario1750AD


SCENARIOS = {
	i0AD: scenario0AD,
	i1500AD: scenario1500AD,
	i1750AD: scenario1750AD,
}


def getScenario(iScenario=None):
	if iScenario is None:
		iScenario = scenario()
	
	return SCENARIOS[iScenario]
