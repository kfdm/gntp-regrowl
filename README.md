# ReGrowl Server

Server for *regrowling* GNTP messages using various bridge classes

Initial support for:

* local - Regrowl to legacy versions of growl using [legacy python bindings](http://pypi.python.org/pypi/growl-py/0.0.7)
* udp - Regrowl using legacy udp protocol
* echo - Echo incoming growl messages to the terminal (used for debugging)

Read documentation for each bridge in the bridge classes themselves

## Installing

	python setup.py install
	
## Running
```
$ regrowl -h
Usage: regrowl [options]

Options:
  -h, --help            show this help message and exit
  -a HOST, --address=HOST
                        address to listen on
  -p PORT, --port=PORT  port to listen on
  -P PASSWORD, --password=PASSWORD
                        Network password
  -v, --verbose         
```

## Config File

Regrowl bridges can be controled through a simple config file in `~/.regrowl`

```
[regrowl.server]
port = 12345
password = mypassword

[regrowl.bridge.local]
enabled = false

[regrowl.bridge.subscribe]
enabled = false
```

Config file sections are defined by the package name.

## See Also

* [Python GNTP Library](https://github.com/kfdm/gntp) Used to decode incoming growl messages