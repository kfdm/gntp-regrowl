from setuptools import setup

setup(
    name='regrowl',
    description='Regrowl server',
    author='Paul Traylor',
    url='https://github.com/kfdm/gntp-regrowl',
    version='0.0.1',
    packages=[
        'regrowl',
        'regrowl.bridge',
        'regrowl.extras',
    ],
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'gntp',
        ],
    entry_points={
        'console_scripts': [
            'regrowl = regrowl.cli:main'
        ],
        'regrowl.bridge': [
            'echo = regrowl.bridge.echo:EchoNotifier',
            'forward = regrowl.bridge.forward:ForwardNotifier',
            'local = regrowl.bridge.local:LocalNotifier',
            'subscribe = regrowl.bridge.subscribe:SubscribelNotifier',
            'udp = regrowl.bridge.udp:UDPNotifier',
        ]
    }
)
