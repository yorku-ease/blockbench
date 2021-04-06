import argparse
import logging
import sys

from block_server.subscriber import Subscriber
from block_server.databaseImp import DatabaseImp
from block_server.event_handling import EventHandler

LOGGER = logging.getLogger(__name__)


def parse_args(args):
    parser = argparse.ArgumentParser(add_help=False)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '-v', '--verbose',
        action='count',
        default=0,
        help='Increase output sent to stderr')

    parser.add_argument(
        '-b', '--bind',
        help='identify host and port for api to run on',
        default='block-txt-rest-api:8001')

    parser.add_argument(
        '-C', '--connect',
        help='The url of the validator to subscribe to',
        default='tcp://localhost:4004')

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API',
        default='http://127.0.0.1:8008')

    return parser.parse_args(args)


def init_logger(level):
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    if level == 1:
        logger.setLevel(logging.INFO)
    elif level > 1:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARN)


def do_subscribe(opts):
    LOGGER.info('Starting block server...')
    subscriber = Subscriber(opts.connect)
    eventHandler = EventHandler(opts.url)
    subscriber.add_handler(eventHandler.get_events_handler())
    subscriber.listen_to_event()





def main():
    LOGGER.warning("###########")
    opts = parse_args(sys.argv[1:])
    init_logger(opts.verbose)
    try:
        host, port = opts.bind.split(":")
        port = int(port)
    except ValueError:
        print("Unable to parse binding {}: Must be in the format"
              " host:port".format(opts.bind))
        sys.exit(1)
    try:
        LOGGER.warning("## initialize db ##")
        DatabaseImp.initialize()
        do_subscribe(opts)


    except KeyboardInterrupt:
        pass


main()