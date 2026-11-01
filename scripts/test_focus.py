from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
from focus import FocusClock

now=[100.0]
clock=FocusClock(lambda:now[0])
clock.start(25,'Finish science notes')
assert clock.state=='running' and clock.display=='25:00' and clock.task=='Finish science notes'
now[0]+=12.4
assert clock.display=='24:48'
clock.pause();paused=clock.remaining
now[0]+=300
assert clock.remaining==paused
clock.resume();now[0]+=8
assert clock.remaining==paused-8
clock.extend(300);assert clock.total==1800
clock.start(5,'Stretch','break');assert clock.phase=='break' and clock.total==300
now[0]+=301
assert clock.tick() and clock.state=='complete' and clock.display=='00:00'
clock.stop();assert clock.state=='idle'
clock.restore({'state':'running','total':1200,'left':300,'task':'Read','phase':'focus'})
assert clock.state=='paused' and clock.remaining==300 and clock.task=='Read'
print('PASS: focus countdown, pause/resume, +5, break, completion, and safe restart')
