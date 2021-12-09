import pickle
from datetime import datetime, timezone
from typing import Tuple, Optional

from .activities import OwnedActivities


CurrentVersion = 1


class SerializedStateError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class GameState:
    def __init__(self):
        self.money = 0
        self.juice = 0.0
        self.jobs = []
        self.outlets = []
        self.time = 0.0
        
    @property
    def free_juice(self) -> float:
        total_used = 0.0
        for ao in self.jobs + self.outlets:
            if ao.execution is not None:
                total_used += ao.juice_cost
        return self.juice - total_used
    
    @property
    def status_line(self) -> str:
        line = "${:d} {:.4f}/{:.4f}J T:{:.2f}"
        return line.format(self.money, self.free_juice, self.juice, self.time)
        
    def __str__(self):
        msg = "GameState<time: {:.2f}, money: {:d}, cj: {:.4f}, jobs: {!s}, outlets: {!s}>"
        return msg.format(self.time, self.money, self.juice, self.jobs, self.outlets)
        
    def __repr__(self):
        msg = "GameState(time={!r}, money={!r}, juice={!r}, jobs={!r}, outlets: {!r})"
        return msg.format(self.time, self.money, self.juice, self.jobs, self.outlets)
        
    def to_dict(self):
        return {
            'money': self.money,
            'juice': self.juice,
            'jobs': [x.to_dict() for x in self.jobs],
            'outlets': [x.to_dict() for x in self.outlets],
            'time': self.time
        }
    
    @staticmethod
    def from_dict(d):
        gs = GameState()
        gs.money = d['money']
        gs.juice = d['juice']
        gs.jobs = [OwnedActivities.from_dict(job) for job in d['jobs']]
        gs.outlets = [OwnedActivities.from_dict(outlet) for outlet in d['outlets']]
        gs.time = d['time']
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
