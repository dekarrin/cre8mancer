from typing import Callable, Union, Optional, Sequence

from datetime import timedelta
from .format import format_timer


class Activity:
    def __init__(
        self,
        id: int,
        name: str,
        duration: Union[timedelta, int, float],
        purchase_price: Union[int, Callable[[int], int]] = 0,
        money_cost: Union[int, Callable[[int], int]] = 0,
        juice_cost: Union[float, Callable[[int], float]] = 0,
        money_rate: Union[int, Callable[[int], int]] = 0,
        juice_rate: Union[float, Callable[[int], float]] = 0,
    ):
        """
        Create new Activity.
        
        :param id: The ID of the Activity. Must be unique across all instances
        of Activity.
        :param name: The display name of the Activity.
        :param duration: The amount of time that one execution takes. This can
        either be a number of seconds or a timedelta.
        :param purchase_price: How much an instance costs to buy from the
        store. This can be either a single number for a uniform price or a
        function that accepts the current number of owned instances and returns
        the price of purchasing the next one.
        :param money_cost: The amoutn of money needed to start an execution of a
        single instance of this Activity. This can be either a single number for
        a uniform cost or a function that accepts the current number of owned
        instances and returns the amount of additional money needed to power the
        execution of the next instance.
        :param juice_cost: The amount of juice needed to power an execution of a
        single instance of this Activity. This can be either a single number for
        a uniform cost or a function that accepts the current number of owned
        instances and returns the amount of additional juice needed to power the
        execution of the next instance.
        :param money_rate: The amount of money produced by an execution of a
        single instance of this Activity. This can be either a single number for
        a uniform production or a function that accepts the current number of
        owned instances and returns the amount of additional money that the next
        instance will produce.
        :param juice_rate: The amount of juice produced by an execution of a
        single instance of this Activity. This can be either a single number for
        a uniform production or a function that accepts the current number of
        owned instances and returns the amount of additional juice that the next
        instance will produce.
        """
        self.id = id
        self.name = name
        
        self.duration = duration
        if isinstance(duration, int) or isinstance(duration, float):
            self.duration = timedelta(seconds=duration)
        
        # money_cost
        if isinstance(money_cost, float) or isinstance(money_cost, int):
            def money_cost_func(_):
                return int(money_cost)
            self.money_cost = money_cost_func
        else:
            self.money_cost = money_cost
        
        # purchase_price
        if isinstance(purchase_price, float) or isinstance(purchase_price, int):
            def purchase_price_func(_):
                return int(purchase_price)
            self.purchase_price = purchase_price_func
        else:
            self.purchase_price = purchase_price
            
        # juice_cost
        if isinstance(juice_cost, float) or isinstance(juice_cost, int):
            def juice_cost_func(_):
                return float(juice_cost)
            self.juice_cost = juice_cost_func
        else:
            self.juice_cost = juice_cost
        
        # money_rate
        if isinstance(money_rate, float) or isinstance(money_rate, int):
            def money_func(_):
                return int(money_rate)
            self.money_rate = money_func
        else:
            self.money_rate = money_rate
            
        # juice_rate
        if isinstance(juice_rate, float) or isinstance(juice_rate, int):
            def juice_func(_):
                return float(juice_rate)
            self.juice_rate = juice_func
        else:
            self.juice_rate = juice_rate
    
    def __str__(self):
        msg = "Activity<{:s}({:d}), duration={:s}>"
        return msg.format(self.name, self.id, format_timer(self.duration))
        
    def __repr__(self):
        msg = "Activity(id={!r}, name={!r}, duration={!r})"
        return msg.format(self.id, self.name, self.duration)
            
            
# TODO: consistent order of args in Jobs and Outlets
Jobs = [
    Activity(0, 'Eat Bagels', 1, purchase_price=lambda x: round(19+(1.3**x)), money_rate=1),
    Activity(1, 'Data Entry', 10.0, juice_cost=0.05, purchase_price=100, money_rate=2),
    Activity(2, 'Create Spreadsheets', 100, juice_cost=0.17, purchase_price=10000, money_rate=27)
]


Outlets = [
    Activity(1024, 'Binge Netflix Show', 1, money_cost=5, purchase_price=200, juice_rate=0.02),
    Activity(1025, 'Write Fanfiction', 25, money_cost=25, purchase_price=10000, juice_cost=20.0, juice_rate=1.0),
    Activity(1026, 'Make Poetry', 200, money_cost=100, purchase_price=100000, juice_cost=420.0, juice_rate=5.0)
]


def from_id(id: int) -> Activity:
    for act in Jobs:
        if act.id == id:
            return act
    for act in Outlets:
        if act.id == id:
            return act
    raise ValueError("No activity exists with ID: {!s}".format(id))
    

class Execution:
    """
    Represent a particular 'click' of an OwnedActivities instance.
    """

    def __init__(self, start: float, end: float, money: int, juice: float):
        """
        Begin a new execution.
        
        :param start: The game time that this execution started at.
        :param end: The game time that this execution ends at.
        :param money: The amount of money that will be awarded to the player upon completion of this Execution.
        :param juice: The amount of creative juice that will be awarded to the player upon completion of this Execution.
        """
        self.start = start
        self.end = end
        self.juice = juice
        self.money = money
        
    def __str__(self):
        msg = "Execution<time: ({:f}, {:f}), produce: ${:d}/{:.4f}J>"
        return msg.format(self.start, self.end, self.money, self.juice)
        
    def __repr__(self):
        msg = "Execution(start={!r}, end={!r}, money={!r}, juice={!r})"
        return msg.format(self.start, self.end, self.money, self.juice)
        
    def remaining(self, game_time) -> timedelta:
        if game_time >= self.end:
            return timedelta(seconds=0)
        else:
            return timedelta(seconds=self.end-game_time)
        
    def progress(self, game_time) -> float:
        """Return current progress as percent, where 1.0 is fully complete."""
        if game_time >= self.end:
            return 1.0
        else:
            delta = game_time - self.start
            return delta / (self.end - self.start)
            
    def to_dict(self):
        d = {
            'start': self.start,
            'end': self.end,
            'juice': self.juice,
            'money': self.money
        }
        return d

    @staticmethod
    def from_dict(d):
        return Execution(d['start'], d['end'], d['money'], d['juice'])


class OwnedActivities:
    """
    A set of Activities that also contains the number of that activity that a user owns as well as the number
    of that activity that are currently active. Can be directly queried for production numbers given a time delta.
    """
    def __init__(self, count: int, active: int, activity: Activity, execution: Optional[Execution] = None):
        self.activity = activity
        self._count = count
        self._active = active
        self.execution: Optional[Execution] = execution
    
    def execute(self, game_time: float):
        if self.execution is not None:
            raise TypeError("Can't start an execution when one is already running!")
        ex = Execution(
            game_time,
            game_time + self.activity.duration.total_seconds(),
            sum(self.activity.money_rate(c) for c in range(self.active)),
            sum(self.activity.juice_rate(c) for c in range(self.active))
        )
        self.execution = ex
        
    def __str__(self):
        msg = "OwnedActivities<{:d}/{:d}x {:s}, ".format(self.active, self.count, self.name)
        msg += "next_click: {prod: (${:d}, {:.4f}J), ".format(self.money_production, self.juice_production)
        msg += "cost: (${:d}, {:.4f}J)}, ".format(self.cost_per_run, self.juice_price)
        msg += "next_price: ${:d}, ".format(self.next_price)
        msg += "exec_time: {:s} ".format(format_timer(self.activity.duration))
        if self.execution is not None:
            msg += "(Running)"
        else:
            msg += "(Not Running)"
        msg += ">"
        return msg
        
    def __repr__(self):
        msg = "OwnedActivities(count={!r}, active={!r}, activity={!r}, execution={!r})"
        return msg.format(self.count, self.active, self.activity, self.execution)
         
    @property
    def name(self) -> str:
        return self.activity.name
        
    # TODO: Refactor these names to better match the property names in Activity.
    @property
    def money_production(self) -> int:
        total = sum(self.activity.money_rate(c) for c in range(self.active))
        return total
        
    @property
    def juice_production(self) -> float:
        total = sum(self.activity.juice_rate(c) for c in range(self.active))
        return total
        
    @property
    def juice_price(self) -> float:
        total = sum(self.activity.juice_cost(c) for c in range(self.active))
        return total
    
    @property
    def cost_per_run(self) -> int:
        total = sum(self.activity.money_cost(c) for c in range(self.active))
        return total
         
    @property
    def next_price(self) -> int:
        return self.activity.purchase_price(self.count)
    
    # TODO: with introduction of active, count no longer needs to be a @property
    @property  
    def count(self) -> int:
        return self._count
        
    @count.setter
    def count(self, new_count: int):
        self._count = new_count
            
    @property
    def active(self) -> int:
        return self._active
        
    @active.setter
    def active(self, new_amount: int):
        if new_amount > self.count:
            msg = "Can't set active instances to value higher than the total count: {:d}"
            raise ValueError(msg.format(new_amount))
        
        self._active = new_amount
        if self.execution is not None:
            self.execution.money = sum(self.activity.money_rate(c) for c in range(self.active))
            self.execution.juice = sum(self.activity.juice_rate(c) for c in range(self.active))
        
            
    def to_dict(self):
        d = {
            'activity': self.activity.id,
            'count': self.count,
            'active': self.active
        }
        if self.execution is not None:
            d['execution'] = self.execution.to_dict()
        return d
        
    @staticmethod
    def from_dict(d):
        act = from_id(d['activity'])
        oa = OwnedActivities(d['count'], d['active'], act)
        if 'execution' in d:
            oa.execution = Execution.from_dict(d['execution'])
        return oa


def index_of_job(store_item: Union[int, Activity], jobs: Sequence[OwnedActivities]) -> int:
    """Get the index of a job within a given Sequence that matches the
    job definition given by the store_item.
    
    :param store_item: Either the index in Jobs of the job to be found or the Activity
    object itself from Jobs.
    :param jobs: The list of jobs to search.
    :return: The index within jobs of the matching item, or -1 if the item
    is not found in the given sequence.
    """
    global Jobs
    
    if isinstance(store_item, Activity):
        job_def = store_item
    else:
        job_def = Jobs[store_item]
    
    for idx, j in enumerate(jobs):
        if j.activity.id == job_def.id:
            return idx
    return -1
    
    
def index_of_outlet(store_item: Union[int, Activity], outlets: Sequence[OwnedActivities]) -> int:
    """Get the index of an outlet within a given Sequence that matches the
    Outlet definition given by the store_item.
    
    :param store_item: Either the index in Outlets of the outlet to be found or the Activity
    object itself from Outlets.
    :param outlets: The list of outlets to search.
    :return: The index within outlet of the matching item, or -1 if the item
    is not found in the given sequence.
    """
    global Outlets
    
    if isinstance(store_item, Activity):
        outlet_def = store_item
    else:
        outlet_def = Outlets[store_item]
    
    for idx, o in enumerate(outlets):
        if o.activity.id == outlet_def.id:
            return idx
    return -1
