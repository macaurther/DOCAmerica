from Core import *
from Events import handler
	

def updateCore(iCivilization):
	coreArea = plots.core(iCivilization)
	for plot in plots.all():
		if plot.isWater() or (plot.isPeak() and location(plot) not in lPeakExceptions): continue
		plot.setCore(iCivilization, plot in coreArea)

@handler("GameStart")
def init():
	for iCivilization in civs.major():
		updateCore(iCivilization)
		
@handler("periodChange")
def updateCoreOnPeriodChange(iCivilization):
	updateCore(iCivilization)

# Show homewaters overlay
def displayHomewatersOverlay():
	engine = CyEngine()
	engine.fillAreaBorderPlotAlt(1, 1, 1003, "COLOR_GREEN", 0.7)

@handler("GameStart")
def homewatersGameStart():
	displayHomewatersOverlay()

@handler("OnLoad")
def homewatersOnLoad():
	displayHomewatersOverlay()