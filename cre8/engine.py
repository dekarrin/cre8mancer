from .activities import OwnedActivities, Activity, Execution
from . import state, activities, layout
from .state import GameState
from typing import Tuple, Optional
import sys
import math


def seed_func(ex: Execution) -> float:
    """
    Generate additional seed based on the completion of an execution and current game
    state.
    """

    amount = 0.4 * (((ex.end - ex.start) / 3) ** 1.15)
    mon_factor = 0.1 * math.log(ex.money)
    cj_factor = 0.2 * math.log(ex.juice)
    # TODO: balance by current 'value'

    total = amount * mon_factor * cj_factor
    return total


class RulesViolationError(Exception):
    """Raised when a caller attempts to do something that is technically programatically
    valid but disallowed by the game rules."""
    def __init__(self, msg):
        super().__init__(msg)


class Advancement:
    """Contains info on AFK advancement after such is made"""
    def __init__(self, idle_seconds: float, money: int, juice: float, seeds: float):
        self.juice = juice
        self.money = money
        self.idle_seconds = idle_seconds
        self.seeds = seeds


def prepare_state(state_file: str) -> Tuple[GameState, Optional[Advancement]]:
    """Get a ready-to-use GameState. If loaded from disk, advancement is done so that the
    returned game state is updated with everything that needed to have been done since
    the last run.
    
    If no state file exists, a new one is created and returned.
    """
    gs = None
    idle_seconds = 0

    try:
        gs, idle_seconds = state.load(state_file)
    except state.SerializedStateError as e:
        print(str(e), file=sys.stderr)
        overwrite = input("Run anyways and overwrite the existing file (Y/N)? ")
        while overwrite.upper() != 'Y' and overwrite.upper() != 'N':
            overwrite = input("Please enter Y or N: ")
        if overwrite == 'N':
            raise

    if gs is None:
        gs = GameState()
        gs.jobs.append(OwnedActivities(1, 1, activities.from_id(0)))
        return gs, None
    else:
        adv = advance(gs, idle_seconds)
        return gs, adv


def advance(gs: GameState, idle_seconds: float) -> Advancement:
    """
    Advance the game state based on how much time has passed since shutdown.
    
    Advancements are applied to the game state and an object representing the
    advancement is returned in case the caller wishes to know.
    """
    adv = Advancement(idle_seconds, 0, 0, 0.0)
    for oa in gs.jobs + gs.outlets:
        if oa.execution is not None:
            if oa.execution.remaining(gs.time + idle_seconds).total_seconds() <= 0:
                adv.money += oa.execution.money
                adv.juice += oa.execution.juice
                adv.seeds += seed_func(oa.execution)
                
                # TODO if automated, calculate next execution(s).
                # for now, just stop the execution
                oa.execution = None
            
    gs.time += adv.idle_seconds
    gs.money += adv.money
    gs.juice += adv.juice
    gs.seeds += adv.seeds
    return adv
    
    
def deactivate(target_type: str, target_idx: int, amount: int = 1, state_file: str = 'st8cre8.p'):
    """
    Turn one or more items to deactive state.
    """
    gs, _ = prepare_state(state_file)
    
    if amount < 1:
        raise RulesViolationError("You can't deactivate less than 1 item!")
    
    target, act_def = find_target(gs, target_type, target_idx)
    if target is None:
        msg = "You don't own any of {!r}; buy at least one first".format(act_def.name)
        raise RulesViolationError(msg)
        
    amount = min(target.active, amount)
    if amount == 0:
        raise RulesViolationError("{!r} is already at 0 instances.".format(target.name))
    target.active -= amount
    
    msg = layout.bar() + '\n'
    msg += layout.make_act_card(target, gs.time)
    msg += '\n' + layout.bar() + '\n'
    
    state.save(state_file, gs)
    
    
def activate(target_type: str, target_idx: int, amount: int = 1, state_file: str = 'st8cre8.p'):
    """
    Turn one or more items to active state.
    """
    gs, _ = prepare_state(state_file)
    
    if amount < 1:
        raise RulesViolationError("You can't activate less than 1 item!")
    
    target, act_def = find_target(gs, target_type, target_idx)
    if target is None:
        msg = "You don't own any of {!r}; buy at least one first".format(act_def.name)
        raise RulesViolationError(msg)
        
    amount = min(target.count - target.active, amount)
    if amount == 0:
        raise RulesViolationError("{!r} is already at the maximum number of instances".format(target.name))
    
    target.active += amount
    if gs.free_juice < 0:
        msg = "You don't have enough juice to do that."
        raise RulesViolationError(msg)
    
    msg = layout.bar() + '\n'
    msg += layout.make_act_card(target, gs.time)
    msg += '\n' + layout.bar() + '\n'
    
    state.save(state_file, gs)


def buy(target_type: str, target_idx: int, state_file: str = 'st8cre8.p'):
    """
    Purchase somefin from the shop, glu8!
    """
    gs, _ = prepare_state(state_file)

    if target_type == 'job':
        idx = activities.index_of_job(target_idx, gs.jobs)
        if idx < 0:
            # TODO: when buying a new one, make sure everyfin up to then is also added to make indexes
            # consistent w full job list glub
            target = OwnedActivities(0, 0, activities.Jobs[target_idx])
            gs.jobs.append(target)
        else:
            target = gs.jobs[idx]
    elif target_type == 'outlet':
        idx = activities.index_of_outlet(target_idx, gs.outlets)
        if idx < 0:
            # TODO: when buying a new one, make sure everyfin up to then is also added to make indexes
            # consistent w full outlets list glub
            target = OwnedActivities(0, 0, activities.Outlets[target_idx])
            gs.outlets.append(target)
        else:
            target = gs.jobs[idx]
    else:
        raise ValueError("target_type must be one of 'job' or 'outlet'")

    if target.price <= gs.money:
        gs.money -= target.price
        target.count += 1
        target.active += 1
        if gs.free_juice < 0:
            target.active -= 1
    else:
        raise RulesViolationError("You don't have enough money for that")

    state.save(state_file, gs)
    

def click(target_type: str, target_idx: int, state_file: str = 'st8cre8.p'):
    """
    Click on one of the things. target_idx is relative to global job and outlet list, NOT
    location in GameState, however GameState should match the ones available.
    """
    gs, _ = prepare_state(state_file)

    target, act_def = find_target(gs, target_type, target_idx)
    if target is None:
        msg = "You don't own any of {!r}; buy at least one first".format(act_def.name)
        raise RulesViolationError(msg)
            
    # we have the target, now check to make sure an execution isnt already running
    if target.execution is not None:
        msg = "You've already started {!r}!".format(target.name)
        msg += "\nWait for it to finish or stop it before clicking it again."
        raise RulesViolationError(msg)
        
    if target.active < 1:
        msg = "All of {!r} is deactivated! Activate at least one before clicking."
        raise RulesViolationError(msg.format(target.name))
        
    if target.money_cost > gs.money:
        raise RulesViolationError("You don't have enough money for that.")
        
    # okay, we can start an execution
    target.execute(gs.time)
    gs.money -= target.money_cost
    
    # but make sure we didnt just violate amount of free juice
    if gs.free_juice < 0:
        msg = "You don't have enough juice for that."
        if target.count > 1:
            msg += " Try deactivating some instances first."
        raise RulesViolationError(msg)
        
    msg = gs.status_line + '\n'
    msg += '\n' + layout.bar() + '\n'
    msg += layout.make_act_card(target, gs.time)
    msg += '\n' + layout.bar() + '\n'
    print(msg)
    
    state.save(state_file, gs)


def show_store(state_file: str = 'st8cre8.p'):
    gs, _ = prepare_state(state_file)
    
    msg = gs.status_line + '\n\n'
    msg += "Store:\n"
    msg += "\nJobs:\n"
    
    msg += layout.bar() + '\n'
    for j in activities.Jobs:
        # we need to get the current number of owned instances of the item
        # to calculate prices
        cur_idx = activities.index_of_job(j, gs.jobs)
        if cur_idx < 0:
            cur_count = 0
        else:
            cur_count = gs.jobs[cur_idx].count
    
        msg += layout.make_act_store_listing(j, cur_count)
        msg += '\n' + layout.bar() + '\n'
        
    msg += '\nOutlets:\n'
    msg += layout.bar() + '\n'
    for o in activities.Outlets:
        # we need to get the current number of owned instances of the item
        # to calculate prices
        cur_idx = activities.index_of_outlet(o, gs.outlets)
        if cur_idx < 0:
            cur_count = 0
        else:
            cur_count = gs.outlets[cur_idx].count
    
        msg += layout.make_act_store_listing(o, cur_count)
        msg += '\n' + layout.bar() + '\n'
        
    print(msg)
    
    state.save(state_file, gs)
    

def status(state_file: str = 'st8cre8.p'):
    gs, _ = prepare_state(state_file)
    
    msg = "Game Time: {:.2f}".format(gs.time)
    msg += "\nMoney: ${:d}".format(gs.money)
    msg += "\nCreative Juice: {:.4f}/{:.4f}".format(gs.free_juice, gs.juice)
    msg += "\n\nJobs:\n"
    
    msg += layout.bar() + '\n'
    for job in gs.jobs:
        msg += layout.make_act_card(job, gs.time)
        msg += '\n' + layout.bar() + '\n'
    
    msg += '\n\nOutlets:\n'
    msg += layout.bar() + '\n'
    for out in gs.outlets:
        msg += layout.make_act_card(out, gs.time)
        msg += '\n' + layout.bar() + '\n'
        
    print(msg)
    
    state.save(state_file, gs)
    

def find_target(gs: GameState, target_type: str, target_idx: int) -> Tuple[Optional[OwnedActivities], Activity]:
    if target_type == 'job':
        job_def = activities.Jobs[target_idx]
        idx = activities.index_of_job(target_idx, gs.jobs)
        if idx < 0:
            return None, job_def
        target = gs.jobs[idx]
        return target, job_def
    elif target_type == 'outlet':
        outlet_def = activities.Outlets[target_idx]
        idx = activities.index_of_outlet(target_idx, gs.outlets)
        if idx < 0:
            return None, outlet_def
        target = gs.outlets[idx]
        return target, outlet_def
    else:
        raise ValueError("target_type must be one of 'job' or 'outlet'") 