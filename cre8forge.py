from cre8.engine import RulesViolationError
from cre8 import logutil
from cre8 import entrypoint

import sys
import logging
import logging.handlers


if __name__ == "__main__":
    _log = logging.getLogger('cre8')
else:
    _log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)


def main():
    logutil.setup_logging()

    # noinspection PyBroadException
    try:
        entrypoint.execute()
    except KeyboardInterrupt:
        pass
    except RulesViolationError as e:
        _log.debug("User-requested action violates the rules of the game.")
        _log.info(str(e))
        sys.exit(1)
    except Exception:
        _log.exception("Problem during execution")
        sys.exit(2)



if __name__ == '__main__':
    main()
