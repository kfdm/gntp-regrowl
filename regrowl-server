#!/usr/bin/env python

import SocketServer
import traceback
import time

import gntp_bridge as gntp

class GNTPServer(SocketServer.TCPServer):
	def run(self):
		if self.growl_debug:
			sa = self.socket.getsockname()
			print "Listening for GNTP on", sa[0], "port", sa[1], "..."
		self.serve_forever()

class GNTPHandler(SocketServer.StreamRequestHandler):
	def read(self):
		bufferLength = 2048
		buffer = ''
		while(1):
			data = self.request.recv(bufferLength)
			if self.server.growl_debug:
				print 'Reading',len(data)
			buffer = buffer + data
			if len(data) < bufferLength and buffer.endswith('\r\n\r\n'):
				break
		if self.server.growl_debug:
			print '<Reading>\n',buffer,'\n</Reading>'
		return buffer
	def write(self,msg):
		if self.server.growl_debug:
			print '<Writing>\n',msg,'\n</Writing>'
		self.request.sendall(msg)
	def handle(self):
		reload(gntp)
		self.data = self.read()
		
		try:
			message = gntp.parse_gntp(self.data,self.server.growl_password)
			
			response = gntp.GNTPOK(action=message.info['messagetype'])
			if message.info['messagetype'] == 'NOTICE':
				response.add_header('Notification-ID','')
			elif message.info['messagetype'] == 'SUBSCRIBE':
				raise gntp.UnsupportedError()
				#response.add_header('Subscription-TTL','10')
			self.write(response.encode())
		except gntp.BaseError, e:
			if self.server.growl_debug:
				traceback.print_exc()
			if e.gntp_error:
				self.write(e.gntp_error())
		except:
			error = gntp.GNTPError(errorcode=500,errordesc='Unknown server error')
			self.write(error.encode())
			raise
		
		message.send()
		
if __name__ == "__main__":
	from Parser import ServerParser
	
	(options,args) = ServerParser().parse_args()
	
	try:
		server = GNTPServer((options.host, options.port), GNTPHandler)
	except SocketServer.socket.error:
		print 'There is already a server running on port %d'%options.port
		exit(1)
	server.growl_debug = options.debug
	server.growl_password = options.password
	
	try: 
		import setproctitle
		setproctitle.setproctitle('ReGrowl:%d'%options.port)
	except ImportError:
		pass
	
	try:
		server.run()
	except KeyboardInterrupt:
		pass
