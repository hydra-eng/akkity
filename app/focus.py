"""Deadline-based focus clock; independent of Tk and testable without waiting."""
import time
import math

class FocusClock:
    def __init__(self, now=time.monotonic):
        self.now=now
        self.state='idle'
        self.task=''
        self.phase='focus'
        self.total=0
        self.left=0
        self.deadline=0

    @property
    def remaining(self):
        return max(0,self.deadline-self.now()) if self.state=='running' else self.left

    @property
    def active(self):return self.state in ('running','paused')

    @property
    def display(self):
        seconds=math.ceil(self.remaining)
        return f'{seconds//60:02d}:{seconds%60:02d}'

    def start(self,minutes,task,phase='focus'):
        if not 1<=int(minutes)<=120:raise ValueError('Choose 1–120 minutes.')
        self.total=int(minutes)*60
        self.left=self.total
        self.deadline=self.now()+self.total
        self.task=task.strip()[:80] or ('Take a little break' if phase=='break' else 'One thing at a time')
        self.phase=phase
        self.state='running'

    def pause(self):
        if self.state=='running':self.left=self.remaining;self.state='paused'

    def resume(self):
        if self.state=='paused':self.deadline=self.now()+self.left;self.state='running'

    def extend(self,seconds=300):
        if self.active:
            self.total+=seconds
            if self.state=='running':self.deadline+=seconds
            else:self.left+=seconds

    def tick(self):
        if self.state=='running' and self.remaining<=0:
            self.state='complete';self.left=0;return True
        return False

    def stop(self):self.state='idle';self.left=0

    def snapshot(self):
        return {'state':self.state,'task':self.task,'phase':self.phase,'total':self.total,'left':self.remaining}

    def restore(self,data):
        if data.get('state') not in ('running','paused','complete'):return
        self.total=max(0,min(86400,float(data.get('total',0))))
        self.left=max(0,min(self.total,float(data.get('left',0))))
        self.task=str(data.get('task',''))[:80]
        self.phase='break' if data.get('phase')=='break' else 'focus'
        self.state='paused' if self.left>0 else 'complete'
