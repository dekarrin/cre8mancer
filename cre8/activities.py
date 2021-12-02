from typing import Callable, Union

from time import timedelta


# for activity pass the rates either a single number that is "rate per click per item" or a function that
# takes the number of that activity and returns the rate per click, for those which have varying value
# of each successive item.
#
# juice_price follows same rule, either "price per item" or a function that gives the total based on
# the current count.
#
# money_price accepts the current count and returns how much the next one costs.
#
# cost_per_run is different and specifically gives dollars it takes for each run *per item*.
class Activity:
    def __init__(
        self,
        id: int,
        name: str,
        duration: timedelta,
        money_price: Union[float, Callable[[int], float]]=0,
        juice_price: Union[float, Callable[[int], float]]=0,
        money_rate: Union[float, Callable[[int], float]]=0,
        juice_rate: Union[float, Callable[[int], float]]=0,
        cost_per_run: Union[float, Callable[[int], float]]=0,
    ):
    
        self.name = name
        
        self.duration = duration
        if isinstance(duration, int) or isinstance(duration, float):
            self.duration = timedelta(seconds=duration)
        
        # cost_per_run
        if isinstance(cost_per_run, float) or isinstance(cost_per_run, int):
            def cpr_func(count):
                return float(cost_per_run) * count
            self.cost_per_run = cpr_func
        else:
            self.cost_per_run = cost_per_run
        
        # money_price
        if isinstance(money_price, float) or isinstance(money_price, int):
            def money_price_func(count):
                return float(money_price)
            self.money_price = money_price_func
        else:
            self.money_price = money_price
            
        # juice_price
        if isinstance(juice_price, float) or isinstance(juice_price, int):
            def juice_price_func(count):
                return float(juice_price)
            self.juice_price = juice_price_func
        else:
            self.juice_price = juice_price
        
        # money_rate
        if isinstance(money_rate, float) or isinstance(money_rate, int):
            def money_func(count):
                return count * float(money_rate)
            self.money_rate = money_func
        else:
            self.money_rate = money_rate
            
        # juice_rate
        if isinstance(juice_rate, float) or isinstance(juice_rate, int):
            def juice_func(count):
                return count * float(juice_rate)
            self.juice_rate = juice_func
        else:
            self.juice_rate = juice_rate
            
Jobs = [
    Activity(0, 'Eat Bagels', 1.0, money_price=20.0, money_rate=1.0),
    Activity(1, 'Data Entry', 10.0, juice_price=0.05, money_price=100.0, money_rate=2.0),
    Activity(2, 'Create Spreadsheets', 100, juice_price=0.17, money_price=10000, money_rate=27.0)
]


Outlets = [
    Activity(1024, 'Binge Netflix Show', 1, cost_per_run=5.0, money_price=200.0, juice_rate=0.02),
    Activity(1025, 'Write Fanfiction', 25, cost_per_run=25, money_price=10000.0, juice_price=20.0, juice_rate=1.0),
    Activity(1026, 'Make Poetry', 200, cost_per_run=100, money_price=100000.0, juice_price=420.0, juice_rate=5.0)
]

def from_id(id: int) -> Activity:
    for act in Jobs:
        if act.id == id:
            return act
    for act in Outlets:
        if act.id == id:
            return act
    return ValueError("No activity with exists with ID: {!s}".format(id))

class OwnedActivities:
    """
    A set of Activities that also contains the number of that activity that a user owns as well as the number
    of that activity that are currently active. Can be directly queried for production numbers given a time delta.
    """
    def __init__(self, count: int, activity: Activity):
        self.activity = activity
        self._count = count
        self.execution: Optional[Execution] = None
    
    def execute(self, game_time: float):
        if self.execution is not None:
            raise TypeError("Can't start an execution when one is already running!")
        self.execution = Execution(
            game_time,
            game_time + self.activity.duration.total_seconds(),
            self.activity.juice_rate(self.count),
            self.activity.money_rate(self.count),
        )
         
    @property
    def name(self) -> str:
        return self.activity.name
        
    @property
    def money_production(self) -> int:
        return self.activity.money_rate(self.count)
        
    @property
    def juice_production(self) -> int:
        return self.activity.juice_rate(self.count)
        
    @property
    def juice_price(self) -> float:
        return self.action.juice_price(self.count)
    
    @property
    def cost_per_run(self) -> int:
        return self.action.cost_per_run(self.count)
         
    @property
    def next_price(self) -> int:
        return self.activity.money_price(self.count)
    
    @property  
    def count(self) -> int:
        return self._count
        
    @count.setter
    def count(self, new_count: int):
        self._count = new_count
        if self.execution is not None:
            self.execution.juice = self.activity.juice_rate(self.count)
            self.execution.money = self.activity.money_rate(self.count)
            
    def to_dict(self):
        d = {
            'activity': self.activity.id,
            'count': self.count
        }
        if self.execution is not None:
            d['execution'] = self.execution.to_dict()
        
    @classmethod
    def from_dict(self, d):
        act = from_id(d['activity'])
        oa = OwnedActivities(d['count'], act)
        if 'execution' in d:
            oa.execution = Execution.from_dict(d['execution'])
        


class Execution:
    """
    Represent a particular 'click' of an OwnedActivities instance.
    """

    def __init__(self, start, end, juice, money):
        """
        Begin a new execution.
        
        :param start: The game time that this execution started at.
        :param end: The game time that this execution ends at.
        :param juice: The amount of creative juice that will be awarded to the player upon completion of this Execution.
        :param money: The amount of money that will be awarded to the player upon completion of this Execution.
        """
        self.start = start
        self.end = end
        self.juice = juice
        self.money = money
        
    def remaining(self, game_time) -> timedelta:
        now = self.start + game_time
        if now >= self.end:
            return timedelta(seconds=0)
        else:
            return timedelta(seconds=self.end-now)
        
    def progress(self, game_time) -> float:
        """Return current progress as percent, where 1.0 is fully complete."""
        now = self.start + game_time
        if now >= self.end:
            return 1.0
        else:
            delta = game_time - self.start
            return delta / (self.end - self.start)
            
    def to_dict(self):
        return {
            'start': self.start,
            'end': self.end,
            'juice': self.juice,
            'money': self.money
        }

    @classmethod
    def from_dict(self, d):
        return Execution(d['start'], d['end'], d['juice'], d['money'])
