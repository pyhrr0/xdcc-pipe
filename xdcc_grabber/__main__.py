import argparse
import logging


def _parse_args():
    parser = argparse.ArgumentParser()
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
    _ = logging.getLogger(__name__)


if __name__ == "__main__":
    main()
