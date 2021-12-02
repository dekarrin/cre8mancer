from datetime import timedelta
import time
import math


class FrameClock:
    """
    FrameClock tracks frames and inserts delay to allow proper tick time.
    
    Create a FrameClock by providing a timedelta, then use start() to begin
    it. Perform an operation, than call tick() to wait until the start of the
    next frame.
    """
    
    def __init__(self, period: timedelta):
        """Create a new PeriodTimer. It will not start counting until start() or
        tick() is called.
        
        period can be either a timedelta type or a float represnting a number of seconds.
        """
        if isinstance(period, int) or isinstance(period, float):
            period = timedelta(seconds=period)
        self.period: timedelta = period
        self._running: bool = False
        self._last_called: float = 0

    @property
    def running(self) -> bool:
        """Return whether the timer is currently running. This will be true from
        the first call to either tick() or start() up until stop() is called."""
        return self._running

    def start(self):
        """Begin the timer. If it has already been started, this method has no
        effect."""
        if self.running:
            return
        self._last_called = time.monotonic()
        self._running = True

    def tick(self):
        """Wait until the start of the next period. If the timer has not yet
        been started with a call to start(), it is started automatically and
        tick() immediately returns."""
        if not self.running:
            self.start()
            return
        
        now = time.monotonic()
        wait_time = self._target() - now
        
        missed_frames = 0
        if wait_time > 0:
            time.sleep(wait_time)
        elif abs(wait_time) > self.period.total_seconds():
            # we missed frames. set new target time as if we called it correctly and
            # move on
            missed_frames = math.floor(abs(wait_time))
            
        self._last_called = self._target() + (self.period.total_seconds() * missed_frames)

    def stop(self):
        """Stop the running timer."""
        self._running = False

    def _target(self) -> float:
        return self._last_called + self.period.total_seconds()