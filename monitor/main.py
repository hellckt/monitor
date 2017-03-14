# -*- encoding: utf-8 -*-
import sys

from mitmproxy import exceptions, options
from mitmproxy.tools.main import process_options
from mitmproxy.utils import version_check

from monitor import cmdline


def mitmmonitor(args=None):  # pragma: no cover
    import monitor

    version_check.check_pyopenssl_version()

    parser = cmdline.monitor()

    args = parser.parse_args(args)

    try:
        monitor_options = options.Options()
        monitor_options.load_paths(args.conf)
        monitor_options.merge(cmdline.get_common_options(args))
        server = process_options(parser, monitor_options, args)
        m = monitor.master.MonitorMaster(monitor_options, server)
    except exceptions.OptionsError as e:
        sys.exit(1)
    try:
        m.run()
    except (KeyboardInterrupt, RuntimeError):
        pass
