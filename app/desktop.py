"""Windows tray, global shortcut and duplicate-instance activation."""
import ctypes
from ctypes import wintypes
import threading
import pystray
from PIL import Image

class Desktop:
    def __init__(self, app, icon):
        self.app=app
        self.commands=app.desktop_commands
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
        # MOD_ALT | MOD_CONTROL | MOD_NOREPEAT
        if not user32.RegisterHotKey(None,1,0x4003,ord('A')):return
        msg=wintypes.MSG()
        try:
            while user32.GetMessageW(ctypes.byref(msg),None,0,0)>0:
                if msg.message==0x312:self.commands.put('show')
        finally:user32.UnregisterHotKey(None,1)

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
