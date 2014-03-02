import logging
from gntp.notifier import GrowlNotifier

TEST_OPTIONS = ['registration', 'notification', 'subscription', 'all']


def test_client(config, options):
    logging.basicConfig(level=options.verbose)
    notifier = GrowlNotifier(
        hostname=config.get('regrowl.server', 'hostname', '127.0.0.1'),
        port=config.getint('regrowl.server', 'port'),
        password=config.get('regrowl.server', 'password'),
        notifications=['Test']
    )
    if options.test in ['registration', 'all']:
        notifier.register()
    if options.test in ['notification', 'all']:
        notifier.notify(
            noteType='Test',
            title='Testing',
            description='ReGrowl Test',
        )
    if options.test in ['subscription', 'all']:
        notifier.subscribe(
            'TestId',
            'TestName',
            1337,
        )
