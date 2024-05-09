#!/usr/bin/env python3

"""
CLI Arguments
"""

import argparse

from . import __version__


def parse_arguments():
    """Argument parser"""
    parser = argparse.ArgumentParser(
        description="d2cd - Docker Compose Continuous Delivery",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-c",
        "--config-file",
        type=str,
        required=True,
        help="Config file location",
    )

    parser.add_argument(
        "-s",
        "--sleep-time",
        type=int,
        default=600,
        help="Sleep time for each reconciliation",
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enale debug mode",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s v{__version__}",
        help="Show d2cd version",
    )

    return parser.parse_args()
