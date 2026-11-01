"""Focus controls and a small live countdown perched above the pet."""
import tkinter as tk
from tkinter import ttk

class FocusUI:
    def __init__(self,app):
        self.app=app;self.clock=app.focus
        self.window=None;self.badge=None
        self.last_display=None
        self.tick()

    def open(self):
        if self.window and self.window.winfo_exists():self.window.lift();self.window.focus_force();return
        self.window=tk.Toplevel(self.app.root)
        w=self.window;w.title('Akkity · Focus');w.geometry('390x440');w.resizable(False,False)
        w.configure(bg='#202020');w.attributes('-topmost',True)
        frame=tk.Frame(w,bg='#202020');frame.pack(fill='both',expand=True,padx=22,pady=18)
        tk.Label(frame,text='One thing at a time.',bg='#202020',fg='white',font=('Segoe UI',17,'bold')).pack(anchor='w')
        tk.Label(frame,text='Akkity will keep you company, quietly.',bg='#202020',fg='#b9b9b9',font=('Segoe UI',10)).pack(anchor='w',pady=(5,15))
        tk.Label(frame,text='What are you working on?',bg='#202020',fg='white',font=('Segoe UI',10)).pack(anchor='w')
        self.task=tk.Entry(frame,bg='#333333',fg='white',insertbackground='white',font=('Segoe UI',11),relief='flat')
        self.task.pack(fill='x',ipady=8,pady=(6,10));self.task.insert(0,self.clock.task)
        row=tk.Frame(frame,bg='#202020');row.pack(fill='x')
        self.minutes=tk.StringVar(value='25')
        for value in (15,25,45):
            ttk.Button(row,text=f'{value} min',width=7,command=lambda v=value:self.minutes.set(str(v))).pack(side='left',padx=(0,5))
        ttk.Spinbox(row,from_=1,to=120,textvariable=self.minutes,width=5).pack(side='right')
        self.time_label=tk.Label(frame,text='',bg='#202020',fg='#cfeda9',font=('Segoe UI',34,'bold'));self.time_label.pack(pady=(15,0))
        self.state_label=tk.Label(frame,text='',bg='#202020',fg='#b9b9b9',font=('Segoe UI',10));self.state_label.pack(pady=(0,10))
        self.progress=ttk.Progressbar(frame,maximum=100);self.progress.pack(fill='x',pady=(0,12))
        controls=tk.Frame(frame,bg='#202020');controls.pack(fill='x')
        self.main_button=ttk.Button(controls,text='Start focus',command=self.primary);self.main_button.pack(side='left',expand=True,fill='x',padx=(0,5))
        self.extend_button=ttk.Button(controls,text='+5 min',command=self.extend);self.extend_button.pack(side='left',padx=5)
        self.stop_button=ttk.Button(controls,text='Stop',command=self.stop);self.stop_button.pack(side='left',padx=(5,0))
        self.break_button=ttk.Button(frame,text='Take a 5-minute break',command=lambda:self.start(5,'Take a little break','break'));self.break_button.pack(fill='x',pady=(12,5))
        self.note=tk.Label(frame,text='Your countdown stays beside Akkity when this panel closes. Drag the ◢ resize grip to change chat size.',wraplength=340,bg='#202020',fg='#aaa',font=('Segoe UI',9));self.note.pack(pady=6)
        self.update()

    def primary(self):
        if self.clock.state=='running':self.clock.pause();self.save()
        elif self.clock.state=='paused':self.clock.resume();self.save()
        else:
            try:self.start(int(self.minutes.get()),self.task.get())
            except ValueError:self.note.configure(text='Enter a duration from 1 to 120 minutes.');return
        self.update()

    def start(self,minutes,task,phase='focus'):
        self.clock.start(minutes,task,phase)
        self.app.special_queue=[];self.app.set_action('idle',0)
        self.save();self.update()

    def toggle(self):
        if self.clock.state=='running':self.clock.pause()
        elif self.clock.state=='paused':self.clock.resume()
        else:self.open()
        self.save();self.update()

    def extend(self):self.clock.extend();self.save();self.update()
    def stop(self):self.clock.stop();self.save();self.app.touch();self.update()
    def save(self):self.app.write_json('focus.json',self.clock.snapshot())

    def position(self):
        if self.badge and self.badge.winfo_exists():
            x=max(0,min(self.app.root.winfo_x()+1,self.app.root.winfo_screenwidth()-190))
            y=self.app.root.winfo_y()-76
            if y<0:y=self.app.root.winfo_y()+208
            self.badge.geometry(f'190x70+{x}+{max(0,min(y,self.app.root.winfo_screenheight()-70))}')

    def update(self):
        c=self.clock
        if self.window and self.window.winfo_exists():
            self.time_label.configure(text=c.display if c.state!='idle' else 'Ready?')
            status={'idle':'Choose a task and a duration.','running':'Break time' if c.phase=='break' else 'Focusing · wandering paused','paused':'Paused · resume when you are ready','complete':'Break complete. Ready for the next thing?' if c.phase=='break' else 'Nice work! Time for a little break.'}[c.state]
            self.state_label.configure(text=status)
            self.main_button.configure(text={'idle':'Start focus','running':'Pause','paused':'Resume','complete':'Start another focus'}[c.state])
            self.extend_button.configure(state='normal' if c.active else 'disabled')
            self.stop_button.configure(state='normal' if c.state!='idle' else 'disabled')
            self.break_button.configure(state='disabled' if c.active else 'normal')
            self.task.configure(state='disabled' if c.active else 'normal')
            self.progress['value']=100*(1-c.remaining/c.total) if c.total and c.state!='idle' else 0
        if c.state=='idle' or self.app.hidden:
            if self.badge and self.badge.winfo_exists():self.badge.withdraw()
            return
        if not self.badge or not self.badge.winfo_exists():
            self.badge=tk.Toplevel(self.app.root);self.badge.title('Akkity · Countdown');self.badge.overrideredirect(True);self.badge.attributes('-topmost',True)
            self.badge.configure(bg='#202020',highlightbackground='#7e9368',highlightthickness=1)
            self.badge_task=tk.Label(self.badge,bg='#202020',fg='#ccc',font=('Segoe UI',9),anchor='w');self.badge_task.pack(fill='x',padx=9,pady=(5,0))
            row=tk.Frame(self.badge,bg='#202020');row.pack(fill='x',padx=9)
            self.badge_time=tk.Label(row,bg='#202020',fg='#cfeda9',font=('Segoe UI',20,'bold'));self.badge_time.pack(side='left')
            self.badge_pause=tk.Button(row,text='Pause',command=self.toggle,bg='#333',fg='white',relief='flat',font=('Segoe UI',8));self.badge_pause.pack(side='right')
            for widget in (self.badge,self.badge_task,self.badge_time):widget.bind('<Button-1>',lambda e:self.open())
        self.badge.deiconify()
        label=c.task if c.active else ('Break complete!' if c.phase=='break' else 'Nice work! Take a break.')
        self.badge_task.configure(text=label if len(label)<=27 else label[:24]+'…')
        self.badge_time.configure(text=c.display if c.active else 'Done ♡')
        self.badge_pause.configure(text='Resume' if c.state=='paused' else 'Pause' if c.state=='running' else 'Open')
        self.position()

    def tick(self):
        if self.clock.tick():
            self.save();self.app.gesture('wave')
            if self.app.desktop:
                try:self.app.desktop.notify('Your focus session is complete. Take a little break.','Akkity')
                except Exception:pass
        self.update()
        self.app.root.after(250,self.tick)
