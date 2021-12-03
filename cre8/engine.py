from .timer import FrameClock
from .activities import OwnedActivities
from . import state, activities, layout
from .state import GameState
import random
import time
from typing import Tuple
from datetime import datetime


class RulesViolationError(Exception):
    """Raised when a caller attempts to do something that is technically programatically
    valid but disallowed by the game rules."""
    def __init__(self, msg):
        super().__init__(msg)

class Advancement:
    """Contains info on AFK advancement after such is made"""
    def __init__(self, idle_seconds: int, money: int, juice: float):
        self.juice = juice
        self.money = money
        self.idle_seconds = idle_seconds


def prepare_state(state_file: str) -> Tuple[GameState, Advancement]:
    """Get a ready-to-use GameState. If loaded from disk, advancement is done so that the
    returned game state is updated with everything that needed to have been done since
    the last run.
    
    If no state file exists, a new one is created and returned.
    """
    
    try:
        gs, idle_seconds = state.load(state_file)
    except state.SerializedStateError as e:
        print(str(e), file=sys.stderr)
        overwrite = input("Run anyways and overwrite the existing file (Y/N)? ")
        while overwrite.upper() != 'Y' and overwrite.upper() != 'N':
            overwrite = input("Please enter Y or N: ")
        if overwrite == 'N':
            return
    if gs is None:
        gs = GameState()
        gs.jobs.append(OwnedActivities(1, activities.from_id(0)))
        return gs, None
    else:
        adv = advance(gs, idle_seconds)
        return gs, adv


def advance(gs: GameState, idle_seconds: float) -> Advancement:
    """
    Advance the gamestate based on how much time has passed since shutdown.
    
    Advancements are applied to the game state and an object representing the
    advancement is returned in case the caller wishes to know.
    """
    adv = Advancement(idle_seconds, 0, 0)
    for oa in gs.jobs + gs.outlets:
        if oa.execution is not None:
            if oa.execution.remaining(gs.time + idle_seconds) <= 0:
                adv.money += oa.execution.money
                adv.juice += oa.execution.juice
            
            # TODO if automated, calculate next execution(s).
            # for now, just stop the execution
            oa.execution = None
            
    gs.time += adv.idle_seconds
    gs.money += adv.money
    gs.juice += adv.juice
    return adv
    

def click(target_type: str, target_idx: int, state_file: str='cre8.p'):
    """
    Click on one of the things. target_idx is relative to global job and outlet list, NOT
    location in GameState, however GameState should match the ones available.
    """
    gs, _ = prepare_state(state_file)
    
    target = None
    if target_type == 'job':
        job_def = activities.Jobs[target_idx].id
        for j in self.jobs:
            if j.activity.id == job_def.id:
                target = j
        if target is None:
            msg = "You don't own any of {!r}; buy at least one first".format(job_def.name)
            raise RulesViolationError(msg)
    elif target_type == 'outlet':
        outlet_def = activities.Outlets[target_idx].id
        for o in self.outlets:
            if o.activity.id == outlet_def.id:
                target = o
        if target is None:
            msg = "You don't own any of {!r}; buy at least one first".format(outlet_def.name)
            raise RulesViolationError(msg)            
    else:
        raise ValueError("target_type must be one of 'job' or 'outlet'")
            
    # we have the target, now check to make sure an execution isnt already running
    if target.execution is not None:
        msg = "You've already started {!r}!".format(target.name)
        msg += "\nWait for it to finish or stop it before clicking it again."
        raise RulesViolationError(msg)
        
    # okay, we can start an execution
    target.execute(gs.time)
    
    state.save(state_file, gs)

def status(state_file: str='cre8.p'):
    gs, _ = prepare_state(state_file)
    
    msg = "Game Time: {:.2f}".format(gs.time)
    msg += "\nMoney: ${:d}".format(gs.money)
    msg += "\nCreative Juice: {:.3f}".format(gs.juice)
    msg += "\n\nJobs:\n"
    
    width = 50
    bar = '+' + ('-' * (width - 2)) + '+'
    msg += bar + '\n'
    for job in gs.jobs:
        if job.execution is not None:
            exec_prog = job.execution.progress(gs.time)
            exec_rem = job.execution.remaining(gs.time)
        else:
            exec_prog = None
            exec_rem = job.activity.duration
            
        msg += layout.make_act_card(
            job.name,
            job.next_price,
            job.count,
            job.count,
            job.cost_per_run,
            job.juice_price,
            job.money_production,
            job.juice_production,
            exec_prog,
            exec_rem,
            card_width=width
        )
        msg += '\n' + bar + '\n'
    
    msg += '\n\nOutlets:\n'
    msg += bar + '\n'
    for out in gs.outlets:
        if out.execution is not None:
            exec_prog = out.execution.progress(gs.time)
            exec_rem = out.execution.remaining(gs.time)
        else:
            exec_prog = None
            exec_rem = out.activity.duration
            
        msg += layout.make_act_card(
            out.name,
            out.next_price,
            out.count,
            out.count,
            out.cost_per_run,
            out.juice_price,
            out.money_production,
            out.juice_production,
            exec_prog,
            exec_rem,
            card_width=width
        )
        msg += '\n' + bar + '\n'
        
    print(msg)
    
    state.save(state_file, gs)
    