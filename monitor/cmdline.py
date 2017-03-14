# -*- encoding: utf-8 -*-
import argparse

from mitmproxy.tools.cmdline import common_options, get_common_options


def monitor():
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")

    group = parser.add_argument_group("Mitmmonitor")
    group.add_argument(
        "--no-browser",
        action="store_false", dest="monitor_open_browser",
        help="Don't start a browser",
    )
    group.add_argument(
        "--monitor-port",
        action="store", type=int, dest="monitor_port",
        metavar="PORT",
        help="Mitmweb port."
    )
    group.add_argument(
        "--monitor-host",
        action="store", dest="monitor_host",
        metavar="HOST",
        help="Mitmmonitor host."
    )

    common_options(parser)
    return parser
