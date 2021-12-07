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

    args = parser.parse_args()
    args.func(args)


def exec_status(args):
    engine.status(args.state)


def exec_click(args):
    engine.click(args.type, args.activity, args.state)


def exec_store(args):
    engine.show_store(args.state)


def exec_buy(args):
    engine.buy(args.type, args.activity, args.state)


if __name__ == '__main__':
    try:
        run_from_cli()
    except KeyboardInterrupt:
        pass
    except RulesViolationError as e:
        print(str(e))
