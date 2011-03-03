#!/usr/bin/env python

import sys
from gntp.notifier import GrowlNotifier



if __name__ == "__main__":
	from Parser import ClientParser
	
	(options,message) = ClientParser().parse_args()
	
	growl = GrowlNotifier(
		applicationName = options.app,
		notifications = [options.name],
		defaultNotifications = [options.name],
		hostname = options.host,
		password = options.password,
		port = options.port,
		debug = options.debug,
	)
	result = growl.register()
	if result is not True: exit(result)
	
	result = growl.notify(
		noteType = options.name,
		title = options.title,
		description = message,
		icon = options.icon,
		sticky = options.sticky,
		priority = options.priority,
	)
	if result is not True: exit(result)

