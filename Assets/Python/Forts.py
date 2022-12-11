from CvPythonExtensions import *
import CvUtil
import PyHelpers
from StoredData import data #edead
from Consts import *

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

class Forts:

	def obtainFortCulture(self, iX, iY, iFortOwner):
		print ("NEW Fort obtained by " + str(iFortOwner) + " through fort construction on : " + str(iX) + "," + str(iY))
		# If fort is already owned by the right player, return
		if data.dFortMap[iX][iY] == iFortOwner:
			return
		
		data.dFortMap[iX][iY] = iFortOwner
		teamFortOwner = gc.getTeam(iFortOwner)
		
		#  Default - 1 Tile Ring
		iRange = 1
		#  Imperialism Tech - Big Fat Cross
		if teamFortOwner.isHasTech(iImperialism):
			iRange = 2
		
		for iXLoop in range(iX-iRange, iX+iRange+1):
			for iYLoop in range(iY-iRange, iY+iRange+1):
				# Big Fat Cross does not have corners
				if (iXLoop == iX-2 or iXLoop == iX+2) and (iYLoop == iY-2 or iYLoop == iY+2): continue
				
				# Check for out-of-bounds
				if (iXLoop < 0 or iXLoop > iWorldX): continue
				if (iYLoop < 0 or iYLoop > iWorldY): continue
				
				pLoopPlot = gc.getMap().plot(iXLoop, iYLoop)
				
				if pLoopPlot.getOwner() == iFortOwner or pLoopPlot.getOwner() == -1:
					# If the tile is owned by the fort owner or unclaimed, give it to the fort owner
					data.dFortCulture[iXLoop][iYLoop] = iFortOwner
					pLoopPlot.setOwnerNoUnitCheck(iFortOwner)
	
	def loseFortCulture(self, iX, iY):
		iFortOwner = data.dFortMap[iX][iY]
		print ("OLD Fort owned by " + str(iFortOwner) + " lost on : " + str(iX) + "," + str(iY))
		
		data.dFortMap[iX][iY] = -1
		teamFortOwner = gc.getTeam(iFortOwner)
		
		#  Default - 1 Tile Ring
		iRange = 1
		#  Manifest Destiny Tech - Big Fat Cross
		if teamFortOwner.isHasTech(iManifestDestiny):
			iRange = 2
		
		for iXLoop in range(iX-iRange, iX+iRange+1):
			for iYLoop in range(iY-iRange, iY+iRange+1):
				# Big Fat Cross does not have corners
				if (iXLoop == iX-2 or iXLoop == iX+2) and (iYLoop == iY-2 or iYLoop == iY+2): continue
				
				# Check for out-of-bounds
				if (iXLoop < 0 or iXLoop > iWorldX): continue
				if (iYLoop < 0 or iYLoop > iWorldY): continue
				
				if not self.isFortInRange(iXLoop, iYLoop, iFortOwner, iRange):
					# If the tile is no longer within range of a fort of iPlayer, relinquish control of that tile
					data.dFortCulture[iXLoop][iYLoop] = -1
					gc.getMap().plot(iXLoop, iYLoop).setOwnerNoUnitCheck(-1)
	
	def isFortInRange(self, iX, iY, iPlayer, iRange):
		# Returns true if there is a fort owned by iPlayer in range of this tile
		for iXLoop in range(iX-iRange, iX+iRange+1):
			for iYLoop in range(iY-iRange, iY+iRange+1):
				# Big Fat Cross does not have corners
				if (iXLoop == iX-2 or iXLoop == iX+2) and (iYLoop == iY-2 or iYLoop == iY+2): continue
				
				# Check for out-of-bounds
				if (iXLoop < 0 or iXLoop > iWorldX): continue
				if (iYLoop < 0 or iYLoop > iWorldY): continue
				
				if data.dFortMap[iXLoop][iYLoop] == iPlayer:
					return True
		return False
	
	def updateAllFortCulture(self):
		for iXLoop in range(0, iWorldX):
			for iYLoop in range(0, iWorldY):
				if data.dFortCulture[iXLoop][iYLoop] > -1:
					gc.getMap().plot(iXLoop, iYLoop).setOwnerNoUnitCheck(data.dFortCulture[iXLoop][iYLoop])
	
	def wipeFortCultureInArea(self, tArea):
		for tPlot in tArea:
			data.dFortCulture[tPlot[0]][tPlot[1]] = -1
			data.dFortMap[tPlot[0]][tPlot[1]] = -1

forts = Forts()