from optparse import OptionParser,OptionGroup
import logging
import pydefaults
import sys
import os

def store_path(option,opt,value,parser):
	setattr(parser.values, option.dest, os.path.realpath(value))

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
		self.add_option('-l','--log',dest='log',default=self.settings['serverlog'],
					action='callback',callback=store_path,type=str)
		self.add_option('-v','--verbose',dest='verbose',default=logging.INFO,
					action='store_const',const=logging.DEBUG)
		self.add_option("-d","--debug",help="Print raw growl packets",
					dest='debug',action="store_true",default=False)
		self.add_option("-q","--quiet",help="Quiet mode",
					dest='debug',action="store_false")
	def parse_args(self, args=None, values=None):
		values, args = OptionParser.parse_args(self, args, values)
		return values, args

class ClientParser(OptionParser):
	def __init__(self,domain='com.github.kfdm.gntp'):
		OptionParser.__init__(self)
		self.settings = pydefaults.database(domain)
		
		#Network
		group = OptionGroup(self,'Network')
		group.add_option("-H","--host",help="Specify a hostname to which to send a remote notification. [%default]",
						dest="host",default=self.settings['host'])
		group.add_option("--port",help="port to listen on",
						dest="port",type="int",default=self.settings['port'])
		group.add_option("-P","--password",help="Network password",
						dest='password',default=self.settings['password'])
		self.add_option_group(group)
		
		#Required (Needs Defaults)
		group = OptionGroup(self,'Growl')
		group.add_option("-n","--name",help="Set the name of the application [%default]",
						dest="app",default='ReGrowl Client')
		group.add_option("-N","--notification",help="Set the notification name [%default]",
						dest="name",default='ReGrowl Message')
		group.add_option("-t","--title",help="Set the title of the notification [Default :%default]",
						dest="title",default=None)
		group.add_option("-m","--message",help="Sets the message instead of using stdin",
						dest="message",default=None)
		self.add_option_group(group)
		
		#Optional (Does not require Default)
		group = OptionGroup(self,'Extra')
		group.add_option("-d","--debug",help="Print raw growl packets",
						dest='debug',action="store_true",default=False)
		group.add_option('-v','--verbose',help="Debug level",
						dest='verbose',action='store_const',const=logging.DEBUG,default=logging.INFO)
		group.add_option("-s","--sticky",help="Make the notification sticky [%default]",
						dest='sticky',action="store_true",default=False)
		group.add_option("-p","--priority",help="-2 to 2 [%default]",
						dest="priority",type="int",default=0)
		group.add_option("--image",help="Icon for notification (Only supports URL currently)",
						dest="icon",default=None)
		self.add_option_group(group)
	def parse_args(self, args=None, values=None):
		values, args = OptionParser.parse_args(self, args, values)
		
		if values.message is None:
			print 'Enter a message followed by Ctrl-D'
			try: message = sys.stdin.read()
			except KeyboardInterrupt: exit()
		else:
			message = values.message
		
		if values.title is None:
			values.title = ' '.join(args)
		
		# If we still have an empty title, use the 
		# first bit of the message as the title
		if values.title == '':
			values.title = message[:20]
		
		return values, message