import math
from datetime import timedelta

def format_timer(remaining_duration: timedelta):
    remaining_secs = remaining_duration.total_seconds()
    hours = int(remaining_secs // 3600)
    remaining_secs -= (hours * 3600)
    mins = int(remaining_secs // 60)
    remaining_secs -= (mins * 60)
    secs = math.floor(remaining_secs)
    if hours > 0:
        text = '{:d}h{:d}m{:d}s'.format(hours, mins, secs)
    elif mins > 0:
        text = '{:d}m{:d}s'.format(mins, secs)
    else:
        text = '{:d}s'.format(secs)
        
    return text
