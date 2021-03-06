#!/usr/bin/env python

from __future__ import absolute_import
import visa
import logging
from sys import platform

class GPIBDetector ( object ) :
	def __init__ ( self ) :
		logger = logging.getLogger ( u'myLogger' )
		#if platform == "linux" or platform == "linux2" or platform == "darwin":
		#	self._rm = visa.ResourceManager('@py')
		#elif platform == "win32" or platform == "cygwin":
		#	self._rm = visa.ResourceManager()
		#resources = self._rm.list_resources()
		resources = [""] * 1
		try :
			self._rm1 = visa.ResourceManager ( )
			resources = self._rm1.list_resources ( )
		except :
			logger.debug ( u'  Failed to open ni-visa' )
		try :
			self._rm2 = visa.ResourceManager ( u'@py' )
			resources += self._rm2.list_resources ( )
		except :
			logger.debug ( u'  Failed to open pi-visa' )

		self.identifiers = {}
		logger.debug ( u'  Probing devices...' )
		for res in resources:
			logger.debug ( u'   Found %s', res )
			if not ( res.startswith ( u"ASRL" ) or res.startswith ( u"GPIB" ) ) :
				continue

			if res.startswith ( u"ASRL" ) :
				logger.debug ( u'   Opening serial connection to %s', res )
				dev = self._rm2.open_resource ( res, baud_rate = 19200, data_bits = 8, timeout = 10000 )
			if res.startswith ( u"GPIB" ) :
				logger.debug ( u'   Opening GPIB connection to %s', res )
				dev = self._rm1.open_resource ( res )
			idn = dev.query ( u"*IDN?" )
			self.identifiers[res] = idn
			dev.close ( )

	def get_resname_for ( self, search ) :
		for key, value in self.identifiers.items ( ) :
			if search in value :
				return key
		return None

if __name__ == u"__main__" :
	import pprint

	detector = GPIBDetector ( )

	pprint.pprint ( detector.identifiers )
