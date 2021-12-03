from cre8 import engine

import argparse

def run_from_cli():
    parser = argparse.ArgumentParser(description="Create vast new worlds by idling")
    parser.add_argument('-s', '--state', default='cre8.p', help="Give location of state file")
    subparsers = parser.add_subparsers(required=True, dest="command")
    
    status_parser = subparsers.add_parser('status', help="Show current status of the game")
    status_parser.set_defaults(func=exec_status)
    
    click_parser = subparsers.add_parser('click', help="Click on one of your many lovely items")
    click_parser.add_argument('type', help="The thing you want to target!", choices=[
    
    
    args = parser.parse_args()
    args.func(args)

def exec_status(args):
    engine.status(args.state)

if __name__ == '__main__':
    try:
        run_from_cli()
    except KeyboardInterrupt:
        pass
