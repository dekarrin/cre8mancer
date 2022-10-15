from .activities import OwnedActivities, Activity, Execution
from . import state, activities, layout
from .logutil import TRACE
from .state import GameState
from .layout import format_timer
from datetime import datetime, timezone
from typing import Tuple, Optional, Any
import sys
import math
import logging

from cre8 import logutil


_log = logging.getLogger(__name__)


def seed_func(ex: Execution) -> float:
    """
    Generate additional seed based on the completion of an execution and current game
    state.
    """
    
    # using weibull "stretched exponential" function
    # f(x) = 1 - e^-(x/a)^b, (b > 2)
    # see accepted answer:
    # https://math.stackexchange.com/questions/3542734/alternatives-for-sigmoid-curve-starting-from-0-with-interpretable-parameters
    seed_xscale = 10000  # used as parameter "a", which sets x-scale
    seed_smooth = 3  # used as parameter "b", which sets steepness of sigmoid section
    
    def weibull_stretched(x):
        return 1 - (math.e ** -((x/seed_xscale)**seed_smooth))

    amount = ((max(ex.end - ex.start, 1) / 300) ** 1.15)
    mon_factor = seed_xscale * weibull_stretched(ex.money)
    cj_factor = seed_xscale * weibull_stretched(ex.juice)
    # TODO: balance by current 'value'

    total = amount + mon_factor + cj_factor
    msg = "Seed - amount, money, juice, total - {:.6f}, {:.6f}, {:.6f}, {:.6f}"
    _log.log(TRACE, msg.format(amount, mon_factor, cj_factor, total))
    return total
    

class RulesViolationError(Exception):
    """Raised when a caller attempts to do something that is technically programmatically
    valid but disallowed by the game rules."""
    def __init__(self, msg):
        _log.debug("RulesViolationError created - {!r}".format(msg))
        super().__init__(msg)


class Advancement:
    """Contains info on AFK advancement after such is made"""
    def __init__(self, idle_seconds: float, money: int, juice: float, seeds: float):
        self.juice = juice
        self.money = money
        self.idle_seconds = idle_seconds
        self.seeds = seeds

    def __str__(self):
        fmtstr = "Advancement<idle_seconds: {:.8f}, money: {:d}, juice: {:.6f}, seeds: {:.8f}>"
        return fmtstr.format(self.idle_seconds, self.money, self.juice, self.seeds)

    def __repr__(self):
        fmtstr = "Advancement(idle_seconds={!r}, money={!r}, juice={!r}, seeds={!r})"
        return fmtstr.format(self.idle_seconds, self.money, self.juice, self.seeds)


class Engine:
    def __init__(self, state_file: Optional[str] = 'st8cre8.p'):
        self.state_file = state_file
        self.game = GameState()
        
        _ = self._load_or_create_state()
        _log.debug("t={:.4f} - Engine initialized".format(self.game.time))
        
    def update(self):
        """
        Update the engine state but do not save automatically.
        """
        
        now_time = datetime.now(timezone.utc)
        if self.game.last_advancement > now_time:
            errmsg = "Game state was last advanced in the future, the system clock may"
            errmsg += " have been tampered with."
            raise ValueError(errmsg)
        
        seconds_since_adv = (now_time - self.game.last_advancement).total_seconds()
        self._advance(seconds_since_adv)

    def prestige(self) -> str:
        """
        Set everyfin over and convert seeds to ideas. Called 'meditate' in the parlance of the game.
        
        Returns message for user.
        """
        gs = self.game
        msg = ""

        _log.debug("t={:.4f} - Action 'prestige'".format(self.game.time))
        
        if gs.seeds < 1:
            raise RulesViolationError("You can't prestige until you have at least 1 seed.")
            
        amount = int(gs.seeds)
        self.game = gs.prestiged()
        
        s = 's' if amount != 1 else ''
        idea_count = str(amount) if amount != 1 else 'an'
        msg += "{:d} seed{:s} sprouted into {:s} (i)dea{:s}!\n".format(amount, s, idea_count, s)
        
        s = 's' if gs.ideas != 1 else ''
        msg += "You now have {:d} total (i)dea{:s}... Imagine the possibilities.".format(gs.ideas, s)
        
        self.save()
        return msg

    def get_state(self, attribute: str) -> Any:
        """
        Directly obtain an attribute from the user state. Does not apply any advancement. Useful for testing/debugging.
        
        :param attribute: The state attribute to obtain. Can be one of "money", "juice", "seeds", or "ideas".
        """
        gs = self.game

        _log.log(TRACE, "t={:.4f} - Action 'get_state' for {!r}".format(self.game.time, attribute))
        
        if attribute not in ('money', 'juice', 'seeds', 'ideas'):
            raise ValueError("attribute is not an allowed value for get_state: {!s}".format(attribute))
        
        if gs is None:
            raise RulesViolationError("There is no state file at the given location.")
        
        if attribute == 'money':
            return gs.money
        elif attribute == 'juice':
            return gs.juice
        elif attribute == 'seeds':
            return gs.seeds
        elif attribute == 'ideas':
            return gs.ideas
        else:
            raise ValueError("should never happen")
        
    def set_state(
        self,
        money: Optional[int] = None,
        juice: Optional[float] = None,
        seeds: Optional[float] = None,
        ideas: Optional[int] = None
    ) -> str:
        """
        Directly set a property on the user state. Useful for testing/debugging.

        :param money: New amount for money.
        :param juice: New amount for cj.
        :param seeds: New amount for seeds.
        :param ideas: New amount for ideas.
        """
        # TODO: need to find way to set as "non-updating" for debug cases (doing debug should not cause actual game
        # functions to take place)
        gs = self.game

        logged_values = "values (money={!r}, juice={!r}, seeds={!r}, ideas={!r})".format(money, juice, seeds, ideas)
        _log.debug("t={:.4f} - Action 'set_state'; ".format(self.game.time) + logged_values)

        if money is not None:
            gs.money = money
        if juice is not None:
            gs.juice = juice
        if seeds is not None:
            gs.seeds = seeds
        if ideas is not None:
            gs.ideas = ideas

        self.save()
        return gs.status_line

    def deactivate(self, category: str, target_type: str, target_idx: int, amount: int = 1) -> str:
        """
        Turn one or more items to deactive state.
        """    
        gs = self.game
        msg = ""

        logged_values = "x{!r} for {!r} in {!r}[{!r}]".format(amount, category, target_type, target_idx)
        _log.debug("t={:.4f} - Action 'deactivate'; ".format(self.game.time) + logged_values)
        
        if category not in ('instance', 'automation'):
            raise ValueError("category must be one of 'instance' or 'automation'")
        if target_type not in ('job', 'outlet'):
            raise ValueError("target_type must be one of 'job' or 'outlet'")
        
        if amount < 1:
            raise RulesViolationError("You can't deactivate less than 1 item!")
        
        target, act_def = self._find_target(target_type, target_idx)
        if target is None:
            msg = "You don't own any of {!r}; buy at least one first".format(act_def.name)
            raise RulesViolationError(msg)
        
        if category == 'instance':
            amount = min(target.active, amount)
            if amount == 0:
                raise RulesViolationError("{!r} is already at 0 instances.".format(target.name))
            target.active -= amount
        elif category == 'automation':
            if amount != 1:
                msg = "Automation deactivation is all-or-nothing; you can't deactivate more than one."
                raise RulesViolationError(msg)
            if target.automations < 1:
                msg = "You haven't bought any automations for {!r} yet; buy some first.".format(target.name)
                raise RulesViolationError(msg)
            if not target.automated:
                msg = "Automation is already off for {!r}.".format(target.name)
                raise RulesViolationError(msg)
                
            target.automated = False
        else:
            raise ValueError("should never happen")
        
        msg += layout.bar() + '\n'
        msg += layout.make_act_card(target, gs.time)
        msg += '\n' + layout.bar() + '\n'
        
        self.save()
        return msg
        
    def activate(
        self,
        category: str,
        target_type: str,
        target_idx: int,
        amount: int = 1,
    ) -> str:
        """
        Turn one or more items to active state.
        """
        gs = self.game
        msg = ""

        logged_values = "x{!r} for {!r} in {!r}[{!r}]".format(amount, category, target_type, target_idx)
        _log.debug("t={:.4f} - Action 'activate'; ".format(self.game.time) + logged_values)
        
        if category not in ('instance', 'automation'):
            raise ValueError("category must be one of 'instance' or 'automation'")
        if target_type not in ('job', 'outlet'):
            raise ValueError("target_type must be one of 'job' or 'outlet'")
        
        if amount < 1:
            raise RulesViolationError("You can't activate less than 1 item!")
        
        target, act_def = self._find_target(target_type, target_idx)
        if target is None:
            msg = "You don't own any of {!r}; buy at least one first".format(act_def.name)
            raise RulesViolationError(msg)
        
        if category == 'instance':
            amount = min(target.count - target.active, amount)
            if amount == 0:
                msg = "{!r} is already at the maximum number of instances".format(target.name)
                raise RulesViolationError(msg)
            
            target.active += amount
            if gs.free_juice < 0:
                msg = "You don't have enough juice to do that."
                raise RulesViolationError(msg)
        elif category == 'automation':
            if amount != 1:
                msg = "Automation activation is all-or-nothing; you can't activate more than one."
                raise RulesViolationError(msg)
            if target.automations < 1:
                msg = "You haven't bought any automations for {!r} yet; buy some first.".format(target.name)
                raise RulesViolationError(msg)
            if target.automated:
                msg = "Automation is already on for {!r}.".format(target.name)
                raise RulesViolationError(msg)
                
            if target.execution is not None:
                # one is already running, so juice check is not needed
                # just set automated to True so next advancement handles starting next executions
                target.automated = True
            else:
                if gs.free_juice < target.juice_cost:
                    msg = "You don't have enough juice for the first auto-execution.\n"
                    msg += "Try freeing up some juice or deactivating some instances first."
                    raise RulesViolationError(msg)
                if gs.money < target.money_cost:
                    msg = "You don't have enough money for the first auto-execution.\n"
                    msg += "Try saving up some money or deactivating some instances first."
                    raise RulesViolationError(msg)
                    
                target.automated = True
                target.execute(gs.time)
                gs.money -= target.money_cost        
        else:
            raise ValueError("should never happen")
        
        msg += layout.bar() + '\n'
        msg += layout.make_act_card(target, gs.time)
        msg += '\n' + layout.bar() + '\n'
        
        self.save()
        return msg

    def buy(self, category: str, target_type: str, target_idx: int) -> str:
        """
        Purchase somefin from the shop, glu8!
        
        :param category: The type of item being purchased. This can be either
        "instance" or "automation". If it is "instance", an instance of the
        targeted activity will be purchased using dollars. If it is "automation", an
        automation for the targeted activity will be purchased using ideas.
        :param target_type: Either "job" or "outlet" - the type of activity that the
        target of the purchased item is.
        :param target_idx: The index from the store in the target_type group that
        points to the specific target of the purchase.
        """
        gs = self.game
        msg = ""

        logged_values = "{!r} in {!r}[{!r}]".format(category, target_type, target_idx)
        _log.debug("t={:.4f} - Action 'buy'; ".format(self.game.time) + logged_values)
        
        if category not in ('instance', 'automation'):
            raise ValueError("category must be one of 'instance' or 'automation'")
        if target_type not in ('job', 'outlet'):
            raise ValueError("target_type must be one of 'job' or 'outlet'")
        
        if category == 'instance':
            if target_type == 'job':
                idx = activities.index_of_job(target_idx, gs.jobs)
                if idx < 0:
                    # TODO: when buying a new one, make sure everyfin up to then is also added to make indexes
                    # consistent w full job list glub
                    target = OwnedActivities(activities.Jobs[target_idx], 0, 0, 0)
                    gs.jobs.append(target)
                else:
                    target = gs.jobs[idx]
            elif target_type == 'outlet':
                idx = activities.index_of_outlet(target_idx, gs.outlets)
                if idx < 0:
                    # TODO: when buying a new one, make sure everyfin up to then is also added to make indexes
                    # consistent w full outlets list glub
                    target = OwnedActivities(activities.Outlets[target_idx], 0, 0, 0)
                    gs.outlets.append(target)
                else:
                    target = gs.outlets[idx]
            else:
                raise ValueError("should never happen")

            if target.price > gs.money:
                raise RulesViolationError("You don't have enough money for that")
            
            gs.money -= target.price
            target.count += 1
            target.active += 1
            if gs.free_juice < 0:
                target.active -= 1
            msg += "Bought {!r}; you now have {:d} of them.".format(target.name, target.count)
                
        elif category == 'automation':
            target, act_def = self._find_target(target_type, target_idx)
            if target is None:
                msg = "You don't own any of {!r}; buy at least one first".format(act_def.name)
                raise RulesViolationError(msg)
                
            if target.auto_price > gs.ideas:
                raise RulesViolationError("You don't have enough (i)deas for that")
                
            gs.ideas -= target.auto_price
            target.automations += 1
            
            # if possible, turn it on immediately
            if not target.automated:
                if target.execution is not None:
                    # one is already running, so juice check is not needed
                    # just set automated to True so next advancement handles starting next executions
                    target.automated = True
                elif gs.free_juice >= target.juice_cost and gs.money >= target.money_cost:
                    target.automated = True
                    target.execute(gs.time)
                    gs.money -= target.price
                # otherwise, don't activate the execution
            
            msg += "Bought automation for {!r}".format(target.name)
        else:
            raise ValueError("should never happen")

        self.save()
        return msg
        
    def click(self, target_type: str, target_idx: int) -> str:
        """
        Click on one of the things. target_idx is relative to global job and outlet list, NOT
        location in GameState, however GameState should match the ones available.
        """
        gs = self.game
        msg = ""

        logged_values = "{!r}[{!r}]".format(target_type, target_idx)
        _log.debug("t={:.4f} - Action 'click'; ".format(self.game.time) + logged_values)

        target, act_def = self._find_target(target_type, target_idx)
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
        
        # but make sure we didnt just violate amount of free juice
        if gs.free_juice < target.juice_cost:
            msg = "You don't have enough juice for that."
            if target.count > 1:
                msg += " Try deactivating some instances first."
            raise RulesViolationError(msg)
            
        # okay, we can start an execution
        ex = target.execute(gs.time)
        gs.money -= target.money_cost
        
        msg += gs.status_line + '\n'

        formatted_time = format_timer(ex.remaining(gs.time))
        msg_line = "Okay! {!r} started, you'll get ${:d} and {:.4f}J in {:s}."
        msg += msg_line.format(target.name, target.money_production, target.juice_production, formatted_time)
        
        self.save()
        return msg

    def get_active_count(self, target_type: str, target_idx: int) -> int:
        """
        Return the number of active instances of the targeted activity.
        """
        if target_type not in ('job', 'outlet'):
            raise ValueError("target_type must be one of 'job' or 'outlet'")

        target, _ = self._find_target(target_type, target_idx)
        if target is None:
            return 0
        return target.active

    def get_automated(self, target_type: str, target_idx: int) -> bool:
        """
        Return whether the given target is currently automated.
        """
        if target_type not in ('job', 'outlet'):
            raise ValueError("target_type must be one of 'job' or 'outlet'")

        target, _ = self._find_target(target_type, target_idx)
        if target is None:
            return False
        return target.automated

    def show_store(self) -> str:
        gs = self.game
        msg = ""

        _log.debug("t={:.4f} - Action 'store'".format(self.game.time))
        
        msg += gs.status_line + '\n\n'
        msg += "Store:\n"
        msg += "\nJobs:\n"
        
        msg += layout.bar() + '\n'
        for j in activities.Jobs:
            # we need to get the current number of owned instances of the item
            # to calculate prices
            cur_idx = activities.index_of_job(j, gs.jobs)
            if cur_idx < 0:
                cur_count = 0
                auto_count = 0
            else:
                cur_count = gs.jobs[cur_idx].count
                auto_count = gs.jobs[cur_idx].automations
        
            msg += layout.make_act_store_listing(j, cur_count, auto_count)
            msg += '\n' + layout.bar() + '\n'
            
        msg += '\nOutlets:\n'
        msg += layout.bar() + '\n'
        for o in activities.Outlets:
            # we need to get the current number of owned instances of the item
            # to calculate prices
            cur_idx = activities.index_of_outlet(o, gs.outlets)
            if cur_idx < 0:
                cur_count = 0
                auto_count = 0
            else:
                cur_count = gs.outlets[cur_idx].count
                auto_count = gs.outlets[cur_idx].count
        
            msg += layout.make_act_store_listing(o, cur_count, auto_count)
            msg += '\n' + layout.bar() + '\n'
            
        self.save()
        return msg

    def status(self) -> str:
        gs = self.game
        msg = ""

        _log.log(TRACE, "t={:.4f} - Action 'status'".format(self.game.time))
        
        msg += gs.status_line
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
        
        return msg
        
    def save(self):
        if self.state_file is not None:
            state.save(self.state_file, self.game)
    
    def _load_or_create_state(self) -> Optional[Advancement]:
        """Get a ready-to-use GameState. If loaded from disk, advancement is done so that the
        returned game state is updated with everything that needed to have been done since
        the last run.
        
        Once loaded, state loaded from self.state_file is set as value of self.game
        If no state file exists, a new one is created and set as value of self.game.
        
        Will print to stdout if needs confirmation from user to override.
        """
        self.game = None
        
        idle_seconds = 0

        if self.state_file is not None:
            try:
                self.game, idle_seconds = state.load(self.state_file)
            except state.SerializedStateError as e:
                print(str(e), file=sys.stderr)
                overwrite = input("Run anyways and overwrite the existing file (Y/N)? ")
                while overwrite.upper() != 'Y' and overwrite.upper() != 'N':
                    overwrite = input("Please enter Y or N: ")
                if overwrite == 'N':
                    raise

        if self.game is None:
            self.game = GameState()
            self.game.jobs.append(OwnedActivities(activities.from_id(0), 1, 1, 0))
            return None
        else:
            adv = self._advance(idle_seconds)
            return adv

    def _advance(self, idle_seconds: float) -> Advancement:
        """
        Advance the game state based on how much time has passed since shutdown.
        
        Advancements are applied to the game state and an object representing the
        advancement is returned in case the caller wishes to know.
        """
        adv = Advancement(idle_seconds, 0, 0, 0.0)
        now = self.game.time + idle_seconds
        _log.log(logutil.TRACE, "Starting advance")
        for oa in self.game.jobs + self.game.outlets:
            _log.log(logutil.TRACE, "ADV: Checking OA {!r}".format(oa))
            while oa.execution is not None and oa.execution.remaining(now).total_seconds() <= 0:
                cur_exec = oa.execution
                _log.log(logutil.TRACE, "ADV->OA: Completing Execution: {!r}".format(cur_exec))
                
                adv.money += cur_exec.money
                adv.juice += cur_exec.juice
                adv.seeds += seed_func(cur_exec)
                
                oa.execution = None
                
                # if automated, get set up to calculate next execution.
                if oa.automated:
                    _log.log(logutil.TRACE, "ADV->OA: is automated so starting new execution".format(cur_exec))
                    # make sure running the next execution doesn't violate constraints
                    
                    free_juice = self.game.free_juice + adv.juice
                    free_money = self.game.money + adv.money
                    _log.log(logutil.TRACE, "ADV->OA: free money: {:d}, free juice: {:.8f}".format(free_money, free_juice))
                    if free_juice >= oa.juice_cost and free_money >= oa.money_cost:
                        _log.log(logutil.TRACE, "ADV->OA: requirements met, starting auto-execution")
                        oa.execute(cur_exec.end)
                        self.game.money -= oa.money_cost
                        _log.log(logutil.TRACE, "ADV->OA: subtracted price: {!s}".format(oa.price))
                    else:
                        _log.log(logutil.TRACE, "ADV->OA: requirements not met, halting auto")
                        oa.automation = False
                else:
                    _log.log(logutil.TRACE, "ADV->OA: not automated so cleared execution".format(cur_exec))
            _log.log(logutil.TRACE, "ADV: Done with OA".format(oa))
                
        self.game.time += adv.idle_seconds
        self.game.money += adv.money
        self.game.juice += adv.juice
        self.game.seeds += adv.seeds
        self.game.last_advancement = datetime.now(timezone.utc)
        _log.log(logutil.TRACE, "Ending advance, calculated: {!r}".format(adv))
        return adv
    
    def _find_target(self, target_type: str, target_idx: int) -> Tuple[Optional[OwnedActivities], Activity]:
        gs = self.game
        
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

        