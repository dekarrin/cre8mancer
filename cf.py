from cre8 import engine

import argparse

def parse_cli(argv):
	parser = argparse.ArgumentParser(description="Create vast new worlds by idling")
	parser.add_argument('-s', '--state', default='cre8.p', help="Give location of state file")
	
	subparsers = parser.add_subparsers(required=True)
	status_parser = subparsers.add_parser('status', help="Show current status of the game")
	status_parser.set_defaults(func=exec_status)
	
	args = parser.parse_args()
	args.func(args)

def execute_status(args):
	engine.status(args.state)

if __name__ == '__main__':
    try:
        engine.start()
    except KeyboardInterrupt:
        pass
