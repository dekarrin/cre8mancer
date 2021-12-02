from .timer import FrameClock
from .activities import OwnedActivities
from datetime import datetime
import random
import time
from datetime import datetime


class GameState:
    def __init__(self):
        self.money = 0
        self.juice = 0.0
        self.jobs = {}
        self.outlets = {}
        self.time = 0.0
		self.shutdown_time = None
		
	@classmethod
	def from_dict(d):
		gs = type(self)()
		gs.money = d['money']
		gs.juice = d['juice']
		gs.jobs = {OwnedActivities.from_dict(job) for job in d['jobs']}
		gs.outlets = {OwnedActivities.from_dict(outlet) for outlet in d['outlets']}
		gs.time = time
		gs.shutdown_time = d['shutdown_time']
		return gs
        
    def to_dict(self):
        return {
            'money': self.money,
            'juice': self.juice,
            'jobs': [x.to_dict() for x in self.jobs],
            'outlets': [x.to_dict() for x in self.outlets],
            'time': self.time,
            'shutdown_time': datetime.today()
        }

def start():
    state = GameState()
    clock = FrameClock(1.0)
    clock.start()
    for x in range(1000):
        print("FIRED! {:s} - NEXT: {!s}".format(datetime.today().strftime('%Y-%m-%d @ %H:%M:%S.%f'), clock._target()))
        if random.random() > 0.95:
        clock.tick()
    

def load_state(file_name):
