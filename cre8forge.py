from cre8 import engine
from cre8.engine import RulesViolationError

import argparse


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
    buy_parser.set_defaults(func=exec_buy)
    
    act_parser = subparsers.add_parser('activate', help="Activate a job or outlet")
    act_type_help = "The kind of activity you want to activate"
    act_parser.add_argument('type', help=act_type_help, choices=['job', 'outlet'])
    act_activity_help = "The index of the item to activate from the full list of all of them"
    act_parser.add_argument('activity', help=act_activity_help, type=int)
    act_count_help = "The number of instances to activate"
    act_parser.add_argument('-c', '--count', help=act_count_help, type=int, default=1)
    act_parser.set_defaults(func=exec_activate)
    
    deact_parser = subparsers.add_parser('deactivate', help="Deactivate a job or outlet")
    deact_type_help = "The kind of activity you want to deactivate"
    deact_parser.add_argument('type', help=deact_type_help, choices=['job', 'outlet'])
    deact_activity_help = "The index of the item to deactivate from the full list of all of them"
    deact_parser.add_argument('activity', help=deact_activity_help, type=int)
    deact_count_help = "The number of instances to deactivate"
    deact_parser.add_argument('-c', '--count', help=deact_count_help, type=int, default=1)
    deact_parser.set_defaults(func=exec_deactivate)

    # debug stuff
    debug_parser = subparsers.add_parser('debug', help="execute debugging and testing commands")
    debug_subs = debug_parser.add_subparsers(required=True, dest="debug_command")
    debug_money = debug_subs.add_parser('money', help="Set current money")
    debug_money.add_argument('amount', help="Amount to set money to.", type=int)
    debug_money.set_defaults(func=exec_debug_money)
    debug_juice = debug_subs.add_parser('juice', help="Set current juice")
    debug_juice.add_argument('amount', help="Amount to set juice to", type=float)
    debug_juice.set_defaults(func=exec_debug_juice)
    
    args = parser.parse_args()
    args.func(args)


def exec_debug_money(args):
    engine.set_state(money=args.amount, state_file=args.state)


def exec_debug_juice(args):
    engine.set_state(juice=args.amount, state_file=args.state)


def exec_status(args):
    engine.status(args.state)


def exec_click(args):
    engine.click(args.type, args.activity, args.state)


def exec_store(args):
    engine.show_store(args.state)


def exec_buy(args):
    engine.buy(args.type, args.activity, args.state)
    
    
def exec_activate(args):
    engine.activate(args.type, args.activity, args.count, args.state)
    
    
def exec_deactivate(args):
    engine.deactivate(args.type, args.activity, args.count, args.state)


if __name__ == '__main__':
    try:
        run_from_cli()
    except KeyboardInterrupt:
        pass
    except RulesViolationError as e:
        print(str(e))
