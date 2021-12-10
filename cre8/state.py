import pickle
from datetime import datetime, timezone
from typing import Tuple, Optional, Dict, Any

from .activities import OwnedActivities


CurrentVersion = 1


class SerializedStateError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class History:
    """
    Contains historical data that is retained on prestige for record-keeping
    and prestige rate increase.
    """
    
    def __init__(self, time: float, money: int, juice: float, prestiges: int):
        self.time = time
        self.money = money
        self.juice = juice
        self.prestiges = prestiges
        
    def to_dict(self) -> Dict[str, Any]:
        d = {
            'time': self.time,
            'money': self.money,
            'juice': self.juice,
            'prestiges': self.prestiges
        }
        return d
        
    def copy(self) -> 'History':
        """
        Create a History that is a copy of this one.
        
        :return: A copy of this History.
        """
        return History(self.time, self.money, self.juice, self.prestiges)
        
    def __str__(self) -> str:
        msg = "History[{:.2f}s for ${:d} and ${:.4f}J over {:d} prestiges]"
        return msg.format(self.time, self.money, self.juice, self.prestiges)
        
    def __repr__(self) -> str:
        msg = "History(time={!r}, money={!r}, juice={!r}, prestiges={!r})"
        return msg.format(self.time, self.money, self.juice, self.prestiges)
        
    @staticmethod
    def from_dict(d: Dict) -> 'History':
        return History(d['time'], d['money'], d['juice'], d['prestiges'])
    


class GameState:
    def __init__(self):
        self.money = 0
        self.juice = 0.0
        self.jobs = []
        self.outlets = []
        self.time = 0.0
        self.ideas = 0  # prestiging gives you ideas on what to do
        self.seeds = 0.0  # seeds sprout into ideas on prestige
        self.history = History(time=0.0, money=0, juice=0, prestiges=0)
        
    @property
    def free_juice(self) -> float:
        total_used = 0.0
        for ao in self.jobs + self.outlets:
            if ao.execution is not None:
                total_used += ao.juice_cost
        return self.juice - total_used
    
    @property
    def status_line(self) -> str:
        line = "${:d} {:.4f}/{:.4f}J  {:d}S->{:d}i  T:{:.2f}"
        return line.format(self.money, self.free_juice, self.juice, int(self.seeds), self.ideas, self.time)
        
    def __str__(self):
        msg = "GameState<time: {:.2f}, money: {:d}, cj: {:.4f}"
        msg += ", ideas: {:d}, seeds: {:.2f}, history: {:s}"
        msg += ", jobs: {!s}, outlets: {!s}>"
        return msg.format(
            self.time,
            self.money,
            self.juice,
            self.ideas,
            self.seeds,
            str(self.history),
            self.jobs,
            self.outlets
        )
        
    def __repr__(self):
        msg = "GameState(time={!r}, money={!r}, juice={!r}, ideas={!r}, seeds={!r}, history={!r}"
        msg += ", jobs={!r}, outlets={!r})"
        return msg.format(
            self.time,
            self.money,
            self.juice,
            self.ideas,
            self.seeds,
            self.history,
            self.jobs,
            self.outlets
        )
        
    def copy(self) -> 'GameState':
        """
        Create a GameState that is an exact duplicate of this one. All properties are
        deeply copied; modifying anything in the returned GameState will not modify
        this one.
        
        :return: A GameState that is a copy of this one.
        """
        gs = GameState()
        gs.time = self.time
        gs.money = self.money
        gs.juice = self.juice
        gs.ideas = self.ideas
        gs.seeds = self.seeds
        gs.history = self.history
        gs.jobs = [j.copy() for j in self.jobs]
        gs.outlets = [o.copy() for o in self.outlets]
        return gs
        
    def prestiged(self) -> 'GameState':
        """
        Create a new GameState that is the result of applying a prestige on this one.
        Does not modify the GameState it was called on.
        
        A prestige grants the player additional flexibility by converting their 'seeds'
        (which have been generated over the course of gameplay via purchases and clicks)
        into 'ideas'. The current game time is saved to historical data and is then set
        to 0. All money and CJ are set to 0 and jobs and outlets (but not purchased
        boosts and automations) are reset.
        
        The 'initial activities' to reset to are determined by applying the following rules:
        * All outlets are reset to 0 instances.
        * All jobs except for the lowest-indexed job are reset to 0 instances. The lowest
        indexed job is set to a count of 1 instance with that instance also set to active.
        * All automations are turned off (and will require the player to turn them back on).
        
        :return: A GameState that is the same as this one but prestiged an additional
        time.
        """
        # only operate on a copy
        gs = self.copy()
        
        # copy current data to historical
        gs.history.money += gs.money
        gs.history.juice += gs.juice
        gs.history.time += gs.time
        gs.history.prestiges += 1
        
        # find the first job
        starting_job = None
            
        # sprout seeds into ideas
        gs.ideas += int(gs.seeds)
        
        # reset all the things!
        gs.money = 0
        gs.juice = 0.0
        for j in gs.jobs:
            j.execution = None
            j.active = 0
            j.count = 0
        if len(gs.jobs) > 0:
            gs.jobs[0].active = 1
            gs.jobs[0].count = 1
        for o in gs.outlets:
            o.execution = None
            o.active = 0
            o.count = 0
        gs.time = 0.0
        gs.seeds = 0
        
        return gs
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'money': self.money,
            'juice': self.juice,
            'jobs': [x.to_dict() for x in self.jobs],
            'outlets': [x.to_dict() for x in self.outlets],
            'time': self.time,
            'ideas': self.ideas,
            'seeds': self.seeds,
            'history': self.history.to_dict()
        }
    
    @staticmethod
    def from_dict(d):
        gs = GameState()
        gs.money = d['money']
        gs.juice = d['juice']
        gs.jobs = [OwnedActivities.from_dict(job) for job in d['jobs']]
        gs.outlets = [OwnedActivities.from_dict(outlet) for outlet in d['outlets']]
        gs.time = d['time']
        gs.ideas = d['ideas']
        gs.seeds = d['seeds']
        gs.history = History.from_dict(d['history'])
        return gs


def save(file_name: str, gs: GameState):
    """
    Saves state to persistence so it can be read later with a call to load().
    Additionally, the shutdown time is recorded so that the monotonic game
    clock can be advanced by the correct number of seconds once state has been
    loaded.
    """
    
    # TODO: sign the rest of the data and put it in the meta dict
    # (similar to JWT method of signing)
    
    formatted_data = {
        'meta': {
            'shutdown_time': datetime.now(timezone.utc),
            'version': CurrentVersion
        },
        'game': gs.to_dict()
    }
    
    with open(file_name, 'wb') as fp:
        try:
            pickle.dump(formatted_data, fp)
        except pickle.PickleError as e:
            raise SerializedStateError("Could not write state file: {!s}".format(str(e)))


def load(file_name: str) -> Tuple[Optional[GameState], float]:
    """
    Loads state. Returns (None, None) when a file does not yet exist, and raises
    SerializedStateError if there is an issue loading an existing state
    file. If running in interactive mode and there is an issue loading the
    existing state file, the user will be prompted to select whether to
    overwrite the unreadable state file. If they select not to, SerializedStateError
    is raised; otherwise, (None, None) is returned as though the state file does not
    yet exist at all.
    
    :param file_name: The state file to load relative to the working directory.
    :return: A tuple containing the loaded GameState and the number of seconds that have passed
    since the game was last shut down (distinct from the in-game monotonic clock). If
    no state file was located in file_name, then the tuple will be None, None.
    """
    
    try:
        with open(file_name, 'rb') as fp:
            try:
                unpickled_data = pickle.load(fp)
            except pickle.PickleError as e:
                raise SerializedStateError("Could not decode state data: {!s}".format(str(e)))
                
            if 'meta' not in unpickled_data:
                raise SerializedStateError("Missing 'meta' key in decoded state file")
            metadata = unpickled_data['meta']
            if 'version' not in metadata:
                raise SerializedStateError("Missing 'version' key in decoded state metadata")
            version = metadata['version']
            if version == CurrentVersion:
                shutdown_time = metadata['shutdown_time']
                gs_data = unpickled_data['game']
                gs = GameState.from_dict(gs_data)
                
                now_time = datetime.now(timezone.utc)
                if shutdown_time > now_time:
                    errmsg = "Serialized state was last shut down in the future, the system clock may"
                    errmsg += " have been tampered with."
                    raise SerializedStateError(errmsg)
                seconds_since_shutdown = (now_time - shutdown_time).total_seconds()
                
                return gs, seconds_since_shutdown
            else:
                raise SerializedStateError("state file's version ({!r}) is invalid".format(version))
            
    except FileNotFoundError:
        # This is okay, it just means the file isnt there yet. Return None to indicate this.
        return None, 0.0
