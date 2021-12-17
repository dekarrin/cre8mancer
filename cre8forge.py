from cre8 import engine
from cre8.engine import RulesViolationError

import sys
import argparse
import logging
import logging.handlers


_log = logging.getLogger('cre8forge')
_log.setLevel(logging.DEBUG)


def main():
    setup_logging()
    
    try:
        run_from_cli()
    except KeyboardInterrupt:
        pass
    except RulesViolationError as e:
        _log.debug("User-requested action violates the rules of the game.")
        _log.info(str(e))
        sys.exit(1)
    except Exception:
        _log.exception("Problem during execution")
        sys.exit(2)


def run_from_cli():
    parser = argparse.ArgumentParser(description="Create vast new worlds by idling")
    parser.add_argument('-s', '--state', default='st8cre8.p', help="Give location of state file")
    subparsers = parser.add_subparsers(required=True, dest="command")
    
    status_parser = subparsers.add_parser('status', help="Show current status of the game")
    status_parser.set_defaults(func=exec_status)
    
    click_parser = subparsers.add_parser('click', help="Click on one of your many lovely items")
    click_parser.add_argument('type', help="The kind of thing you want to click", choices=['job', 'outlet'])
    click_activity_help = "The index of the item to click from the full list of all of them"
    click_parser.add_argument('activity', help=click_activity_help, type=int)
    click_parser.set_defaults(func=exec_click)
    
    store_parser = subparsers.add_parser('store', help="Show the items available to buy")
    store_parser.set_defaults(func=exec_store)

    buy_parser = subparsers.add_parser('buy', help="Buy a job or outlet")
    buy_parser.add_argument('type', help="The kind of thing you want to buy", choices=['job', 'outlet'])
    buy_activity_help = "The index of the item to buy from the full list of all items in the store"
    buy_parser.add_argument('activity', help=buy_activity_help, type=int)
    buy_parser.set_defaults(func=exec_buy, category='instance')
    
    buyauto_parser = subparsers.add_parser('buyauto', help="Buy automation for a job or outlet")
    buyauto_type_help = "The kind of thing you want to buy for"
    buyauto_parser.add_argument('type', help=buyauto_type_help, choices=['job', 'outlet'])
    buyauto_activity_help = "The index of the item to buy for from the full list of all items in the store"
    buyauto_parser.add_argument('activity', help=buyauto_activity_help, type=int)
    buyauto_parser.set_defaults(func=exec_buy, category='automation')
    
    auto_parser = subparsers.add_parser('automate', help="Turn on automation for a job or outlet")
    auto_type_help = "The kind of activity you want to activate automation for."
    auto_parser.add_argument('type', help=auto_type_help, choices=['job', 'outlet'])
    auto_activity_help = "The index of the activity to activate automation for, from the full list"
    auto_parser.add_argument('activity', help=auto_activity_help, type=int)
    auto_off_help = "Turn automation off for the given activity instead of turning it on."
    auto_parser.add_argument('-o', '--off', help=auto_off_help, action='store_true')
    auto_parser.set_defaults(func=exec_auto, category='automation', count=1)
    
    act_parser = subparsers.add_parser('activate', help="Activate a job or outlet")
    act_type_help = "The kind of activity you want to activate"
    act_parser.add_argument('type', help=act_type_help, choices=['job', 'outlet'])
    act_activity_help = "The index of the item to activate from the full list of all of them"
    act_parser.add_argument('activity', help=act_activity_help, type=int)
    act_count_help = "The number of instances to activate"
    act_parser.add_argument('-c', '--count', help=act_count_help, type=int, default=1)
    act_parser.set_defaults(func=exec_activate, category='instance')
    
    deact_parser = subparsers.add_parser('deactivate', help="Deactivate a job or outlet")
    deact_type_help = "The kind of activity you want to deactivate"
    deact_parser.add_argument('type', help=deact_type_help, choices=['job', 'outlet'])
    deact_activity_help = "The index of the item to deactivate from the full list of all of them"
    deact_parser.add_argument('activity', help=deact_activity_help, type=int)
    deact_count_help = "The number of instances to deactivate"
    deact_parser.add_argument('-c', '--count', help=deact_count_help, type=int, default=1)
    deact_parser.set_defaults(func=exec_deactivate, category='instance')
    
    prest_help = "Go into deep meditation to reset progress (except for purchased boosts and automations)"
    prest_help += " and sprout seeds into ideas"
    prest_parser = subparsers.add_parser('meditate', help=prest_help)
    prest_parser.set_defaults(func=exec_prestige)


    # debug stuff
    debug_parser = subparsers.add_parser('debug', help="execute debugging and testing commands")
    debug_subs = debug_parser.add_subparsers(required=True, dest="debug_command")
    
    debug_money = debug_subs.add_parser('money', help="Set or get current money")
    debug_money.add_argument('-s', '--set', help="Set money to the given amount", type=int, dest='amount')
    debug_money.set_defaults(func=exec_debug_money)
    
    debug_juice = debug_subs.add_parser('juice', help="Set or get current juice")
    debug_juice.add_argument(
        '-s', '--set', help="Set juice to the given amount", type=float, dest='amount'
    )
    debug_juice.set_defaults(func=exec_debug_juice)
    
    debug_seeds = debug_subs.add_parser('seeds', help="Set or get current seeds")
    debug_seeds.add_argument('-s', '--set', help="Set seeds to the given value", type=float, dest='amount')
    debug_seeds.set_defaults(func=exec_debug_seeds)
    
    debug_ideas = debug_subs.add_parser('ideas', help="Set or get current ideas")
    debug_ideas.add_argument('-s', '--set', help="Set ideas to the given value", type=int, dest='amount')
    debug_ideas.set_defaults(func=exec_debug_ideas)
    
    
    args = parser.parse_args()
    args.func(args)
    
    
def exec_debug_seeds(args):
    if args.amount is not None:
        engine.set_state(seeds=args.amount, state_file=args.state)
    else:
        seeds = engine.get_state('seeds', state_file=args.state)
        print("{:.6f}".format(seeds))
    
    
def exec_debug_ideas(args):
    if args.amount is not None:
        engine.set_state(ideas=args.amount, state_file=args.state)
    else:
        ideas = engine.get_state('ideas', state_file=args.state)
        print("{:d}".format(ideas))


def exec_debug_money(args):
    if args.amount is not None:
        engine.set_state(money=args.amount, state_file=args.state)
    else:
        money = engine.get_state('money', state_file=args.state)
        print("{:d}".format(money))


def exec_debug_juice(args):
    if args.amount is not None:
        engine.set_state(juice=args.amount, state_file=args.state)
    else:
        juice = engine.get_state('juice', state_file=args.state)
        print("{:.6f}".format(juice))
    
    
def exec_prestige(args):
    engine.prestige(args.state)


def exec_status(args):
    engine.status(args.state)


def exec_click(args):
    engine.click(args.type, args.activity, args.state)


def exec_store(args):
    engine.show_store(args.state)


def exec_buy(args):
    engine.buy(args.category, args.type, args.activity, args.state)
    
    
def exec_auto(args):
    if args.off:
        exec_deactivate(args)
    else:
        exec_activate(args)
    
    
def exec_activate(args):
    engine.activate(args.category, args.type, args.activity, args.count, args.state)
    
    
def exec_deactivate(args):
    engine.deactivate(args.category, args.type, args.activity, args.count, args.state)


class _ExactLevelFilter(object):
    """
    Only allows log records through that are particular levels.
    """

    def __init__(self, levels):
        """
        Creates a new exact level filter.
        :type levels: ``list[int|str]``
        :param levels: The levels that should pass through the filter; all others are filtered out. Each item is either
        one of the predefined level names or an integer level.
        """
        self._levels = set()
        for lev in levels:
            is_int = False
            try:
                lev = lev.upper()
            except AttributeError:
                is_int = True
            if not is_int:
                if lev == 'DEBUG':
                    self._levels.add(logging.DEBUG)
                elif lev == 'INFO':
                    self._levels.add(logging.INFO)
                elif lev == 'WARNING' or lev == 'WARN':
                    self._levels.add(logging.WARNING)
                elif lev == 'ERROR':
                    self._levels.add(logging.ERROR)
                elif lev == 'CRITICAL':
                    self._levels.add(logging.CRITICAL)
                else:
                    raise ValueError("bad level name in levels list: " + lev)
            else:
                self._levels.add(int(lev))

    def num_levels(self):
        """
        Gets the number of levels that are allowed through the filter.
        :rtype: ``int``
        :return: The number of levels.
        """
        return len(self._levels)

    def min_level(self):
        """
        Gets the minimum level that is allowed through the filter.
        :rtype: ``int``
        :return: The minimum leel
        """
        return min(self._levels)

    def filter(self, record):
        """
        Check whether to include the given log record in the output.
        :type record: ``logging.LogRecord``
        :param record: The record to check.
        :rtype: ``int``
        :return: 0 indicates the log record should be discarded; non-zero indicates that the record should be
        logged.
        """
        if record.levelno in self._levels:
            return 1
        else:
            return 0
    

def setup_logging():
    file_handler = logging.handlers.RotatingFileHandler('debug.log', maxBytes=25*1024*1024, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
    logging.getLogger().addHandler(file_handler)

    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logging.getLogger().addHandler(stderr_handler)

    lev_filter = _ExactLevelFilter(['INFO'])
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setLevel(lev_filter.min_level())
    stdout_handler.setFormatter(logging.Formatter("%(message)s"))
    stdout_handler.addFilter(lev_filter)
    logging.getLogger().addHandler(stdout_handler)
    

if __name__ == '__main__':
    main()
