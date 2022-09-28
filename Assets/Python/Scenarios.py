from Core import *

from Scenario250AD import scenario250AD
from Scenario1500AD import scenario1500AD
from Scenario1770AD import scenario1770AD


SCENARIOS = {
	i250AD: scenario250AD,
	i1500AD: scenario1500AD,
	i1770AD: scenario1770AD,
}


def getScenario(iScenario=None):
	if iScenario is None:
		iScenario = scenario()
	
	return SCENARIOS[iScenario]
