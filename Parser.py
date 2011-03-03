from optparse import OptionParser
import pydefaults

class ServerParser(OptionParser):
	def __init__(self,domain='com.github.kfdm.gntp'):
		OptionParser.__init__(self)
		self.settings = pydefaults.database(domain)
		
		# Network Options		
		self.add_option("-a","--address",help="address to listen on",
					dest="host",default=self.settings['host'])
		self.add_option("-p","--port",help="port to listen on",
					dest="port",type="int",default=self.settings['port'])
		self.add_option("-P","--password",help="Network password",
					dest='password',default=self.settings['password'])
		
		# Debug Options
		self.add_option("-d","--debug",help="Print raw growl packets",
					dest='debug',action="store_true",default=False)
		self.add_option("-q","--quiet",help="Quiet mode",
					dest='debug',action="store_false")
	def parse_args(self, args=None, values=None):
		values, args = OptionParser.parse_args(self, args, values)
		return values, args
