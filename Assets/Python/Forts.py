from CvPythonExtensions import *
import CvUtil
import PyHelpers
from StoredData import data #edead
from Consts import *

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

class Forts:

	def obtainFortCulture(self, iX, iY, iPlayer):
		if iPlayer == -1:
			return
		print ("NEW Fort obtained by " + str(iPlayer) + " through fort construction on : " + str(iX) + "," + str(iY))
		# If fort is already owned by the right player, return
		if data.dFortMap[iX][iY] == iPlayer:
			return
		
		data.dFortMap[iX][iY] = iPlayer
		
		iRange = self.getFortRange(iPlayer)
		
		for iXLoop in range(-iRange, iRange+1):
			for iYLoop in range(-iRange, iRange+1):
				# Check tile validity
				if not self.isInRange(iXLoop, iYLoop, iRange): continue
				if not self.isInBounds(iX, iY, iXLoop, iYLoop): continue
				
				pLoopPlot = gc.getMap().plot(iX + iXLoop, iY + iYLoop)
				
				if pLoopPlot.getOwner() == iPlayer or pLoopPlot.getOwner() == -1:
					# If the tile is owned by the fort owner or unclaimed, give it to the fort owner
					data.dFortCulture[iX + iXLoop][iY + iYLoop] = iPlayer
					#pLoopPlot.setOwnerNoUnitCheck(iPlayer)
		
		# Update all Fort culture, otherwise tile updates cause culture to go away
		self.updateAllFortCulture()


	def loseFortCulture(self, iX, iY):
		iPlayer = data.dFortMap[iX][iY]
		if iPlayer == -1:
			return
		print ("OLD Fort owned by " + str(iPlayer) + " lost on : " + str(iX) + "," + str(iY))
		
		data.dFortMap[iX][iY] = -1
		
		iRange = self.getFortRange(iPlayer)
		
		for iXLoop in range(-iRange, iRange+1):
			for iYLoop in range(-iRange, iRange+1):
				# Check tile validity
				if not self.isInRange(iXLoop, iYLoop, iRange): continue
				if not self.isInBounds(iX, iY, iXLoop, iYLoop): continue
				
				# Make sure the tile to remove is actually controlled by a fort of the player losing the fort
				if not data.dFortCulture[iX + iXLoop][iY + iYLoop] == iPlayer: continue
				
				# Check that the player losing the fort doesn't control the tile anyway
				if gc.getMap().plot(iX + iXLoop, iY + iYLoop).getCulture(iPlayer) > 0: continue
				
				# Check if the tile is in range of another Fort owned by this player
				if self.isFortInRange(iX + iXLoop, iY + iYLoop, iPlayer, iRange): continue

				# If the tile passes all checks, relinquish control of that tile
				data.dFortCulture[iX + iXLoop][iY + iYLoop] = -1
				gc.getMap().plot(iX + iXLoop, iY + iYLoop).setOwnerNoUnitCheck(-1)
		
		# Update all Fort culture, otherwise tile updates cause culture to go away
		self.updateAllFortCulture()


	def isFortInRange(self, iX, iY, iPlayer, iRange):
		# Returns true if there is a fort owned by iPlayer in range of this tile
		for iXLoop in range(-iRange, iRange+1):
			for iYLoop in range(-iRange, iRange+1):
				# Check tile validity
				if not self.isInRange(iXLoop, iYLoop, iRange): continue
				if not self.isInBounds(iX, iY, iXLoop, iYLoop): continue
				
				if data.dFortMap[iX + iXLoop][iY + iYLoop] == iPlayer:
					return True
		return False


	def getFortRange(self, iPlayer):
		teamFortOwner = gc.getTeam(iPlayer)
		iCiv = gc.getPlayer(iPlayer).getCivilizationType()
		
		# Default - 1 Tile Ring
		iRange = 1
		# Imperialism Tech - Big Fat Cross
		if teamFortOwner.isHasTech(iImperialism):
			iRange += 1
		# French UP
		if iCiv == iFrance:
			iRange += 1
		
		return iRange


	def isInRange(self, iXLoop, iYLoop, iRange):
		# Big Fat Cross does not have corners
		if iRange == 2:
			if (iXLoop == -2 or iXLoop == 2) and (iYLoop == -2 or iYLoop == 2): return False
		# Bigger Big Fat Cross is rounded
		if iRange == 3:
			if (iXLoop == -3 or iXLoop == 3) and (iYLoop == -3 or iYLoop == 3): return False
			if (iXLoop == -2 or iXLoop == 2) and (iYLoop == -3 or iYLoop == 3): return False
			if (iXLoop == -3 or iXLoop == 3) and (iYLoop == -2 or iYLoop == 2): return False
		
		return True


	def isInBounds(self, iX, iY, iXLoop, iYLoop):
		if (iX + iXLoop < 0 or iX + iXLoop > iWorldX): return False
		if (iY + iYLoop < 0 or iY + iYLoop > iWorldY): return False
		
		return True


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