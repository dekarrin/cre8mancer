"""
Handy functions for both styles of launchers (CLI and GUI) to use.
"""

import logging
import argparse
import sys

from . import logutil, engine, gui, version

_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)


def execute(default_args=list()):
    parser = argparse.ArgumentParser(description="Create vast new worlds by idling")
    parser.add_argument('-s', '--state', default='st8cre8.p', help="Give location of state file")
    parser.add_argument('-t', '--log-trace', action='store_true', help="Include trace-level logs in logfile")
    subparsers = parser.add_subparsers(required=True, dest="command")
    
    gui_parser = subparsers.add_parser('gui', help="Start the game GUI")
    gui_parser.set_defaults(func=exec_gui)
    
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

    version_help = "Show the current version of cre8orforge and then exit."
    version_parser = subparsers.add_parser('version', help=version_help)
    version_parser.set_defaults(func=exec_version)

    if len(sys.argv) > 1:
        args = parser.parse_args()
    else:
        args = parser.parse_args(default_args)

    if args.log_trace:
        logging.getLogger('cre8').setLevel(logutil.TRACE)
    
    eng = engine.Engine(args.state)
    args.func(eng, args)


def exec_version(eng: engine.Engine, args):
    print(version.VERSION)


# noinspection PyUnusedLocal
def exec_gui(eng: engine.Engine, args):
    window = gui.Gui(eng)
    window.run()


def exec_debug_seeds(eng: engine.Engine, args):
    if args.amount is not None:
        print(eng.set_state(seeds=args.amount))
    else:
        seeds = eng.get_state('seeds')
        print("{:.6f}".format(seeds))
    
    
def exec_debug_ideas(eng: engine.Engine, args):
    if args.amount is not None:
        print(eng.set_state(ideas=args.amount))
    else:
        ideas = eng.get_state('ideas')
        print("{:d}".format(ideas))


def exec_debug_money(eng: engine.Engine, args):
    if args.amount is not None:
        print(eng.set_state(money=args.amount))
    else:
        money = eng.get_state('money')
        print("{:d}".format(money))


def exec_debug_juice(eng: engine.Engine, args):
    if args.amount is not None:
        print(eng.set_state(juice=args.amount))
    else:
        juice = eng.get_state('juice')
        print("{:.6f}".format(juice))
    

# noinspection PyUnusedLocal
def exec_prestige(eng: engine.Engine, args):
    print(eng.prestige())


# noinspection PyUnusedLocal
def exec_status(eng: engine.Engine, args):
    print(eng.status())
    eng.save()


def exec_click(eng: engine.Engine, args):
    print(eng.click(args.type, args.activity))


# noinspection PyUnusedLocal
def exec_store(eng: engine.Engine, args):
    print(eng.show_store())


def exec_buy(eng: engine.Engine, args):
    print(eng.buy(args.category, args.type, args.activity))
    
    
def exec_auto(eng: engine.Engine, args):
    if args.off:
        exec_deactivate(eng, args)
    else:
        exec_activate(eng, args)
    
    
def exec_activate(eng: engine.Engine, args):
    eng.activate(args.category, args.type, args.activity, args.count)
    
    
def exec_deactivate(eng: engine.Engine, args):
    eng.deactivate(args.category, args.type, args.activity, args.count)
