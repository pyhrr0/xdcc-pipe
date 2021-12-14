import asyncio
import argparse
import logging

from pipe import XDCCPipe


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--output-file', default='/dev/stdout', type=str)
    parser.add_argument('-n', '--network', type=str)
    parser.add_argument('-c', '--channel', type=str)
    parser.add_argument('-b', '--bot', type=str)
    parser.add_argument('-p', '--pack-num', type=int)
    parser.add_argument(
        '-u', '--ws-url', default='ws://localhost:1234/', type=str)
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose output')

    return parser.parse_args()


def main():
    args = _parse_args()

    level = logging.INFO
    if args.verbose:
        level = logging.DEBUG

    logging.basicConfig(
        format='[%(asctime)s] %(levelname)-8s %(message)s', level=level)

    asyncio.run(
        XDCCPipe.receive_pack(
            args.ws_url, args.output_file,
            args.network, args.channel, args.bot, args.pack_num))


if __name__ == "__main__":
    main()
