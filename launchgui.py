"""
This module launches the GUI and sets up logging to never use a console.

It is unecessary for typical use. If you want a gui as a dev, you can just run
`cre8orforge.py gui`. However, python bundlers often need one single script
to launch and many are incapable of passing default cli arguments. This script
serves as the entrypoint for such bundlers as it allows for the use of other
arguments if passed, but will default to setting up cre8orforge for a GUI-only
execution.
"""

import logging
import sys

from cre8 import logutil, entrypoint


if __name__ == "__main__":
    _log = logging.getLogger('cre8')
else:
    _log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)


def main():
    logutil.setup_logging(console_output=False)

    # noinspection PyBroadException
    try:
        entrypoint.execute()
    except Exception:
        _log.exception("Uncaught problem occured during execution")
        sys.exit(2)


if __name__ == '__main__':
    main()
