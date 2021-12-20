import argparse
import logging

from .pipe import run_client, run_server


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'mode', choices=['server', 'client'], help="mode")
    parser.add_argument(
        '-f', '--output-file', default='/dev/stdout', type=str)
    parser.add_argument(
        '-n', '--network', type=str, help='network to connect to')
    parser.add_argument(
        '-c', '--channel', type=str, help='channel(s) to join')
    parser.add_argument(
        '-b', '--bot', type=str, help='bot to request pack from')
    parser.add_argument(
        '-p', '--pack-num', type=int, help='pack number to request')
    parser.add_argument(
        '-u', '--ws-url', default='ws://localhost:1234', type=str,
        help='address to serve on / connect to')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose output')

    args = parser.parse_args()
    if args.mode == 'client':
        required = ('network', 'channel', 'bot', 'pack_num')
        if any(not getattr(args, arg) for arg in required):
            parser.print_usage()
            exit(1)

    return vars(parser.parse_args())


def main():
    args = _parse_args()

    level = logging.INFO
    if args['verbose']:
        level = logging.DEBUG

    logging.basicConfig(
        format='[%(asctime)s] %(levelname)-8s %(message)s', level=level)

    if args['mode'] == 'client':
        run_client(**args)
    else:
        run_server(**args)


if __name__ == "__main__":
    main()
