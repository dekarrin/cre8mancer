from cre8 import engine

import argparse

def run_from_cli():
    parser = argparse.ArgumentParser(description="Create vast new worlds by idling")
    parser.add_argument('-s', '--state', default='cre8.p', help="Give location of state file")
    subparsers = parser.add_subparsers(required=True, dest="command")
    
    status_parser = subparsers.add_parser('status', help="Show current status of the game")
    status_parser.set_defaults(func=exec_status)
    
    click_parser = subparsers.add_parser('click', help="Click on one of your many lovely items")
    click_parser.add_argument('type', help="The kind of thing you want to target", choices=['job', 'outlet'])
    click_parser.add_argument('activity', help="The index in of the item to click from the full list of all of them", type=int)
    click_parser.set_defaults(func=exec_click)
    
    
    args = parser.parse_args()
    args.func(args)

def exec_status(args):
    engine.status(args.state)
    
def exec_click(args):
    engine.click(args.type, args.activity, args.state)

if __name__ == '__main__':
    try:
        run_from_cli()
    except KeyboardInterrupt:
        pass
