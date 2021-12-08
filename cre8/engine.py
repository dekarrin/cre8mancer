from .activities import OwnedActivities, Activity
from . import state, activities, layout
from .state import GameState
from typing import Tuple, Optional
import sys


class RulesViolationError(Exception):
    """Raised when a caller attempts to do something that is technically programatically
    valid but disallowed by the game rules."""
    def __init__(self, msg):
        super().__init__(msg)


class Advancement:
    """Contains info on AFK advancement after such is made"""
    def __init__(self, idle_seconds: float, money: int, juice: float):
        self.juice = juice
        self.money = money
        self.idle_seconds = idle_seconds


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
            if oa.execution.remaining(gs.time + idle_seconds).total_seconds() <= 0:
                adv.money += oa.execution.money
                adv.juice += oa.execution.juice
                
                # TODO if automated, calculate next execution(s).
                # for now, just stop the execution
                oa.execution = None
            
    gs.time += adv.idle_seconds
    gs.money += adv.money
    gs.juice += adv.juice
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
    
    if target.execution is not None:
        exec_prog = target.execution.progress(gs.time)
        exec_rem = target.execution.remaining(gs.time)
    else:
        exec_prog = None
        exec_rem = target.activity.duration
    msg = layout.bar() + '\n'
    msg += layout.make_act_card(
        target.name,
        target.next_price,
        target.count,
        target.active,
        target.cost_per_run,
        target.juice_price,
        target.money_production,
        target.juice_production,
        exec_prog,
        exec_rem
    )
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
        
    if target.execution is not None:
        exec_prog = target.execution.progress(gs.time)
        exec_rem = target.execution.remaining(gs.time)
    else:
        exec_prog = None
        exec_rem = target.activity.duration
    msg = layout.bar() + '\n'
    msg += layout.make_act_card(
        target.name,
        target.next_price,
        target.count,
        target.active,
        target.cost_per_run,
        target.juice_price,
        target.money_production,
        target.juice_production,
        exec_prog,
        exec_rem
    )
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
            target = OwnedActivities(0, activities.Jobs[target_idx])
            gs.jobs.append(target)
        else:
            target = gs.jobs[idx]
    elif target_type == 'outlet':
        idx = activities.index_of_outlet(target_idx, gs.outlets)
        if idx < 0:
            # TODO: when buying a new one, make sure everyfin up to then is also added to make indexes
            # consistent w full outlets list glub
            target = OwnedActivities(0, activities.Outlets[target_idx])
            gs.outlets.append(target)
        else:
            target = gs.jobs[idx]
    else:
        raise ValueError("target_type must be one of 'job' or 'outlet'")

    if target.next_price <= gs.money:
        gs.money -= target.next_price
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
        
    # okay, we can start an execution
    target.execute(gs.time)
    
    # but make sure we didnt just violate amount of free juice
    if gs.free_juice < 0:
        msg = "You don't have enough juice for that."
        if target.count > 1:
            msg += " Try deactivating some instances first."
        raise RulesViolationError(msg)
    
    state.save(state_file, gs)


def show_store(state_file: str = 'st8cre8.p'):
    gs, _ = prepare_state(state_file)
    
    msg = "Store:\n"
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
    
        msg += layout.make_act_store_listing(
            j.name,
            j.purchase_price(cur_count),
            j.money_cost(cur_count),
            j.juice_cost(cur_count),
            j.money_rate(cur_count),
            j.juice_rate(cur_count),
            j.duration
        )
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
    
        msg += layout.make_act_store_listing(
            o.name,
            o.purchase_price(cur_count),
            o.money_cost(cur_count),
            o.juice_cost(cur_count),
            o.money_rate(cur_count),
            o.juice_rate(cur_count),
            o.duration
        )
        msg += '\n' + layout.bar() + '\n'
        
    print(msg)
    
    state.save(state_file, gs)
    

def status(state_file: str = 'st8cre8.p'):
    gs, _ = prepare_state(state_file)
    
    msg = "Game Time: {:.2f}".format(gs.time)
    msg += "\nMoney: ${:d}".format(gs.money)
    msg += "\nCreative Juice: {:.3f}".format(gs.juice)
    msg += "\n\nJobs:\n"
    
    msg += layout.bar() + '\n'
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
            job.active,
            job.cost_per_run,
            job.juice_price,
            job.money_production,
            job.juice_production,
            exec_prog,
            exec_rem
        )
        msg += '\n' + layout.bar() + '\n'
    
    msg += '\n\nOutlets:\n'
    msg += layout.bar() + '\n'
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
            out.active,
            out.cost_per_run,
            out.juice_price,
            out.money_production,
            out.juice_production,
            exec_prog,
            exec_rem
        )
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
            return None, out_def
        target = gs.outlets[idx]
        return target, out_def
    else:
        raise ValueError("target_type must be one of 'job' or 'outlet'") 