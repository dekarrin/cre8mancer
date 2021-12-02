from .timer import FrameClock
from .activities import OwnedActivities
from . import state
from .state import GameState
import random
import time
from typing import Tuple

class Advancement:
	"""Contains info on AFK advancement after such is made"""
	pass


def prepare_state(state_file: str) -> Tuple[GameState, Avancement]:
	"""Get a ready-to-use GameState. If loaded from disk, advancement is done so that the
	returned game state is updated with everything that needed to have been done since
	the last run.
	
	If no state file exists, a new one is created and returned.
	"""
	
	try:
		gs, shutdown_time = state.load(state_file)
	except state.SerializedStateError as e:
		print(str(e), file=sys.stderr)
		overwrite = input("Run anyways and overwrite the existing file (Y/N)? ")
		while overwrite.upper() != 'Y' and overwrite.upper() != 'N':
			overwrite = input("Please enter Y or N: ")
		if overwrite == 'N':
			return
	if gs is None:
		gs = GameState()
	else:
		# TODO: do advancement using shutdown_time and current time before continuing
		pass
	return gs, None
	


def status(state_file: str='cre8.p'):
	gs, _ = prepare_state(state_file)
	
	msg = "Game Time: {:d}".format(gs.time)
	msg += "\nMoney: ${:d}".format(gs.money)
	msg += "\nCreative Juice: {:.3f}".format(gs.juice)
	msg += "\n\nJobs:"
	for x in gs.jobs:
		
	
	
    clock = FrameClock(1.0)
    clock.start()
    for x in range(1000):
        print("FIRED! {:s} - NEXT: {!s}".format(datetime.today().strftime('%Y-%m-%d @ %H:%M:%S.%f'), clock._target()))
        if random.random() > 0.95:
        clock.tick()
    