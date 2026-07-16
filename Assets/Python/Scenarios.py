from Core import *

from scenario1AD import scenario1AD
from Scenario1500AD import scenario1500AD
from Scenario1750AD import scenario1750AD


SCENARIOS = {
	i1AD: scenario1AD,
	i1500AD: scenario1500AD,
	# i1750AD: scenario1750AD, # MacAurther TODO: Scenarios
}


def getScenario(iScenario=None):
	if iScenario is None:
		iScenario = scenario()
	
	return SCENARIOS[iScenario]
