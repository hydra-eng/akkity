"""Explicit release smoke test; uses a temporary data folder, never personal chats."""
import json,os,tempfile,time
from pathlib import Path

def run(report_path):
    os.environ['AKKITY_TEST']='1'
    with tempfile.TemporaryDirectory(prefix='akkity-test-') as temp:
        # The entrypoint resolves DATA before importing this module.
        import __main__ as app_module
        app_module.DATA=Path(temp)
        app_module.tk.Tk.mainloop=lambda self:None
        a=app_module.Akkity()
        checks={}
        try:
            a.root.update()
            checks['interpolated_motion']=a.subframes==6 and len(a.animations['right'])==48
            a.chat();a.root.update()
            checks['greeting']=a.log.get('1.0','end').strip()=='AKKITY: enti papa'
            for w,h in [(260,200),(300,240),(480,440)]:
                a.config.update(bubble_width=w,bubble_height=h)
                a.close_chat();a.chat();a.root.update()
                checks[f'layout_{w}']=a.entry.winfo_ismapped() and a.log.winfo_height()>20 and a.entry.winfo_rooty()+a.entry.winfo_height()<a.dialog.winfo_rooty()+h
            a.entry.delete(0,'end');a.entry.insert(0,'Reply briefly: what is 2 plus 2?');a.send()
            deadline=time.monotonic()+120
            while a.pending and time.monotonic()<deadline:
                a.root.update();time.sleep(.02)
            response=a.messages[-1]['content'] if a.messages[-1]['role']=='assistant' else ''
            checks['offline_reply']='4' in response or 'four' in response.lower()
            checks['reply_text']=response
            a.close_chat();a.chat();a.root.update()
            checks['fresh_chat']=len(a.messages)==2
            a.quit();a.root.update();checks['hide']=a.hidden and a.root.state()=='withdrawn'
            a.show_pet();a.root.update();checks['reopen']=not a.hidden and a.root.state()=='normal'
            for action in a.animations:
                a.set_action(action,.2);a.animate();a.root.update()
            checks['all_actions']=True
            checks['passed']=all(v for k,v in checks.items() if k!='reply_text')
        except Exception as error:
            checks['passed']=False;checks['error']=repr(error)
        finally:
            a.exit_app()
            Path(report_path).write_text(json.dumps(checks,indent=2),encoding='utf-8')
        return checks['passed']
