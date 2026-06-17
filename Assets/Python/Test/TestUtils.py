from Core import *
from unittest import *

from Slots import addPlayer

from Pickling import pickle


bSetupComplete = False


def setup():
	global bSetupComplete
	if bSetupComplete:
		return
		
	# #MacAurther: players 3-8; Mexico substitutes for Zapotec (already player 1)
	for iSlot, iCiv in enumerate([iAztec, iMexico, iInca, iCherokee, iNorse, iEngland]):
		addPlayer(3 + iSlot, iCiv, bAlive=True)
		data.dSlots[iCiv] = 3 + iSlot

	# #MacAurther: iIndependent1=38, iIndependent2=39, iIndigenous=41 in DOCAmerica
	for i in [38, 39, 41]:
		unit = makeUnit(i, iMilitia, (i, 0))
		player(i).verifyAlive()
		unit.kill(False, -1)
	
	bSetupComplete = True


class PickleTestCase(TestCase):

	def assertPickleable(self, object):
		print "assert pickle %s" % object.__class__.__name__
		self.tryPickle(object)
			
	def tryPickle(self, object):
		try:
			pickle.dumps(object)
		except:
			if hasattr(object, '__dict__'):
				for key, value in object.__dict__.iteritems():
					print "try pickle %s" % key
					self.tryPickle(value)
			raise