"""Windows tray, global shortcut and duplicate-instance activation."""
import ctypes
from ctypes import wintypes
import threading
import pystray
from PIL import Image

HOTKEY_CANDIDATES=((1,0x4003,'Ctrl+Alt+A'),(2,0x4007,'Ctrl+Alt+Shift+A'))

def register_hotkeys(user32):
    """Use the requested shortcut, with a fallback if another app owns it."""
    registered=[]
    for identifier,modifiers,label in HOTKEY_CANDIDATES:
        if user32.RegisterHotKey(None,identifier,modifiers,ord('A')):
            registered.append((identifier,label))
            if identifier==1:break
    return registered

class Desktop:
    def __init__(self, app, icon):
        self.app=app
        self.commands=app.desktop_commands
        self.shortcut_text='Ctrl+Alt+A'
        self.icon=pystray.Icon('Akkity',Image.open(icon),'Akkity · Ctrl+Alt+A to reopen',pystray.Menu(
            pystray.MenuItem('Open Akkity',lambda:self.commands.put('show'),default=True),
            pystray.MenuItem('Chat',lambda:self.commands.put('chat')),
            pystray.MenuItem('Settings',lambda:self.commands.put('settings')),
            pystray.MenuItem('Hide pet',lambda:self.commands.put('hide')),
            pystray.MenuItem('Quit completely',lambda:self.commands.put('exit'))))
        self.icon.run_detached()
        self.thread_id=None
        threading.Thread(target=self.hotkey,daemon=True).start()

    def notify(self,message,title='Akkity'):
        try:self.icon.notify(message,title)
        except Exception:pass

    def hotkey(self):
        self.thread_id=ctypes.windll.kernel32.GetCurrentThreadId()
        user32=ctypes.windll.user32
        self.registered_hotkeys=register_hotkeys(user32)
        if self.registered_hotkeys:
            labels=' or '.join(label for _,label in self.registered_hotkeys)
            self.shortcut_text=labels
            self.icon.title=f'Akkity · Reopen with {labels}'
            if self.registered_hotkeys[0][0]!=1:self.notify(f'Ctrl+Alt+A is already in use. Reopen with {labels}, or use the tray menu.')
        else:
            self.shortcut_text='tray menu'
            self.icon.title='Akkity · Reopen from the tray menu'
            self.notify('Windows could not reserve either shortcut. Reopen Akkity from the tray menu.')
        msg=wintypes.MSG()
        try:
            while user32.GetMessageW(ctypes.byref(msg),None,0,0)>0:
                if msg.message==0x312 and any(msg.wParam==identifier for identifier,_ in self.registered_hotkeys):self.commands.put('show')
        finally:
            for identifier,_ in self.registered_hotkeys:user32.UnregisterHotKey(None,identifier)

    def stop(self):
        self.icon.stop()
        if self.thread_id:ctypes.windll.user32.PostThreadMessageW(self.thread_id,0x12,0,0)

def single_instance():
    kernel=ctypes.windll.kernel32
    kernel.CreateMutexW.restype=wintypes.HANDLE
    kernel.CreateEventW.restype=wintypes.HANDLE
    mutex=kernel.CreateMutexW(None,False,'Local\\AkkityDesktopV1')
    exists=kernel.GetLastError()==183
    event=kernel.CreateEventW(None,False,False,'Local\\AkkityShowV1')
    if exists:
        kernel.SetEvent(wintypes.HANDLE(event))
        return None
    # Keep handles alive until process exit.
    return mutex,event
