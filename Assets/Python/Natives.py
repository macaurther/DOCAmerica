from CvPythonExtensions import *
import CvUtil
import PyHelpers	# LOQ
#import Popup
#import cPickle as pickle
from RFCUtils import utils
from Consts import *
from StoredData import data


class Natives:

    def checkTurn(self, iGameTurn):
            print ("turn")

    def changeNativeAttitudeForPlayer(self, iPlayer, iValue):
        data.players[iPlayer].iNativeAttitude = max(iValue + data.players[iPlayer].iNativeAttitude,
                                                    self.getMinNativeAttitudeForPlayer(iPlayer))

    def getNumNativeSpawnsFromAttitude(self, iPlayer):
        iValue = data.getTotalNativeAttitude(iPlayer)
        if iValue > 0:
            return 0
        elif iValue > -3:
            return 1
        elif iValue > -7:
            return 2
        return 3

    def adjustNativeAttitudeForGameTurn(self, iGameTurn, iPlayer):
        if iGameTurn % 10 == 5:
            iMaxValue = self.getMaxNativeAttitudeForPlayer(iPlayer)
            # FoB - don't adjust attitude if over limit from events
            if data.players[iPlayer].iNativeAttitude >= iMaxValue:
                return;
            data.players[iPlayer].iNativeAttitude = min(data.players[iPlayer].iNativeAttitude + 1, iMaxValue)
            print("FOB Native attutide adjusted to: " + str(data.players[iPlayer].iNativeAttitude))

    def getMinNativeAttitudeForPlayer(self, iPlayer):
        return -10;

    def getMaxNativeAttitudeForPlayer(self, iPlayer):
        if gc.getTeam(iPlayer).isHasTech(iManifestDestiny):
            return 5;
        return 0;

    def handleNativeVillageDestroyed(self, iPlayer, iX, iY, bPillage):
        print("FOB Native Village Destroyed at " + str(iX) + "," + str(iY))
        if iPlayer > 0:
            if bPillage:
                self.changeNativeAttitudeForPlayer(iPlayer, -iNativeVillagePillageAnger) #If pillaged, update attitude before to ensure anger
            if not bPillage and data.getTotalNativeAttitude(iPlayer) > 0:
                self.assimilateVillageIntoLocalCity(iPlayer, iX, iY)
                self.changeNativeAttitudeForPlayer(iPlayer, -iNativeVillageAssimilateCost)
                if utils.getHumanID() == iPlayer:
                    CyInterface().addMessage(iPlayer, False, iDuration,
                                             CyTranslator().getText("TXT_KEY_NATIVE_ASSIMILATION", ("",)),
                                             "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                                             gc.getUnitInfo(iSettler).getButton(), ColorTypes(iGreen), iX,
                                             iY, True, True)
            else:
                if utils.getHumanID() == iPlayer:
                    CyInterface().addMessage(iPlayer, False, iDuration,
                                             CyTranslator().getText("TXT_KEY_NATIVE_UPRISING", ("",)),
                                             "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                                             gc.getUnitInfo(iWarrior).getButton(), ColorTypes(iRed), iX,
                                             iY, True, True)
                self.trySpawnNativePartisans(iX, iY, iPlayer)
            return
        self.trySpawnNativePartisans(iX, iY)

    def assimilateVillageIntoLocalCity(self, iPlayer, iX, iY):
        pCity = gc.getMap().findCity(iX, iY, iPlayer, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
        if pCity:
            pCity.changePopulation(1)
            iCultureChange = pCity.getCulture(iPlayer) / pCity.getPopulation()
            #targetPlot.changeCulture(iNative, iCultureChange, False)
            pCity.changeCulture(iNative, iCultureChange, True)
        else:
            print("FoB Assimilation: Could not find valid city")

    # TODO - redo to provide greater unit variation based on era and location
    def trySpawnNativePartisans(self, iX, iY, iPlayer=None):
        plot = (iX, iY)
        if not self.possibleTile(plot, bWater=False, bTerritory=True, bBorder=True, bImpassable=False, bNearCity=True,
                                 bNextToCity=True):
            lPlots = self.possibleTiles((iX - 1, iY - 1), (iX + 1, iY + 1), bWater=False, bTerritory=True, bBorder=True,
                                        bImpassable=False, bNearCity=True, bNextToCity=True)
            plot = utils.getRandomEntry(lPlots)
        if plot == None: return
        iNumUnits = iNativePillagePartisans
        if iPlayer:
            iNumUnits = self.getNumNativeSpawnsFromAttitude(iPlayer)
        utils.makeUnitAI(iWarrior, iNative, plot, UnitAITypes.UNITAI_ATTACK, 1, "Hostile")
        if iNumUnits > 1:
            utils.makeUnitAI(iSkirmisher, iNative, plot, UnitAITypes.UNITAI_ATTACK, iNumUnits-1, "Hostile")
        utils.setUnitsHaveMoved(iNative, (plot[0], plot[1]))

    def possibleTiles(self, tTL, tBR, bWater=False, bTerritory=False, bBorder=False, bImpassable=False, bNearCity=False, bNextToCity=False):
        return [tPlot for tPlot in utils.getPlotList(tTL, tBR) if
                self.possibleTile(tPlot, bWater, bTerritory, bBorder, bImpassable, bNearCity, bNextToCity)]

    def possibleTile(self, tPlot, bWater, bTerritory, bBorder, bImpassable, bNearCity, bNextToCity=False):
        x, y = tPlot
        plot = gc.getMap().plot(x, y)
        lSurrounding = utils.surroundingPlots(tPlot)

        # never on peaks
        if plot.isPeak(): return False

        # only land or water
        if bWater != plot.isWater(): return False

        # only inside territory if specified
        if not bTerritory and plot.getOwner() >= 0: return False

        # directly next to cities
        if not bNextToCity and [(i, j) for (i, j) in lSurrounding if gc.getMap().plot(i, j).isCity()]: return False

        # never on tiles with units
        if plot.isUnit(): return False

        # never in marsh (impassable)
        if plot.getFeatureType() == iMarsh: return False

        # allow other impassable terrain (ocean, jungle)
        if not bImpassable:
            if plot.getTerrainType() == iOcean: return False
            if plot.getFeatureType() == iJungle: return False

        # restrict to borders if specified
        if bBorder and not [(i, j) for (i, j) in lSurrounding if
                            gc.getMap().plot(i, j).getOwner() != plot.getOwner()]: return False

        # near a city if specified (next to cities excluded above)
        if bNearCity and not [(i, j) for (i, j) in utils.surroundingPlots(tPlot, 2,
                                                                          lambda (a, b): not gc.getMap().plot(a,
                                                                                                              b).isCity())]: return False
        # not on landmasses without cities
        if not bWater and gc.getMap().getArea(plot.getArea()).getNumCities() == 0: return False

        return True