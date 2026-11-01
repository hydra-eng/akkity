"""Explicit release smoke test; uses a temporary data folder, never personal chats."""
import json,os,tempfile,time
from pathlib import Path
from unittest.mock import patch

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
            checks['visible_settings']=a.settings_button.winfo_ismapped()
            checks['visible_file_button']=a.attach_button.winfo_ismapped()
            with tempfile.TemporaryDirectory(prefix='akkity-file-test-') as file_temp:
                sample=Path(file_temp)/'notes.txt';sample.write_text('The project codename is Moonberry.',encoding='utf-8')
                with patch.object(app_module.filedialog,'askopenfilename',return_value=str(sample)) as chooser:
                    a.attach_file()
                checks['file_picker']=chooser.call_count==1 and a.attachment and a.attachment['name']=='notes.txt'
                checks['attachment_visible']='notes.txt' in a.file_label.cget('text')
                a.entry.delete(0,'end');a.entry.insert(0,'What is the project codename in the file?')
                a.send()
                deadline=time.monotonic()+120
                while a.pending and time.monotonic()<deadline:a.root.update();time.sleep(.02)
                answer=a.messages[-1]['content'] if a.messages[-1]['role']=='assistant' else ''
                checks['file_context_reply']='moonberry' in answer.lower()
                checks['reply_text']=answer
                checks['attachment_cleared']=a.attachment is None
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
            a.close_chat();a.config.update(bubble_width=300,bubble_height=240);a.chat();a.root.update()
            checks['fresh_chat']=len(a.messages)==2
            event=type('ResizeEvent',(),{'x_root':10,'y_root':10})()
            a.resize_start(event)
            event=type('ResizeEvent',(),{'x_root':30,'y_root':55})()
            a.resize_drag(event);a.resize_end(event);a.root.update()
            checks['resize']=a.config['bubble_width']==320 and a.config['bubble_height']==285 and a.resize_handle.cget('text')=='◢ 320×285'
            a.close_chat()
            a.focus_ui.start(1,'Test focus')
            a.focus_ui.toggle();checks['focus_pause']=a.focus.state=='paused' and a.focus.task=='Test focus'
            a.focus_ui.toggle();checks['focus_resume']=a.focus.state=='running' and a.focus.remaining>0
            a.focus_ui.extend();checks['focus_extend']=a.focus.total==360
            a.focus_ui.start(1,'Break','break');checks['break_mode']=a.focus.phase=='break' and a.focus.state=='running'
            a.focus_ui.stop();checks['focus_stop']=a.focus.state=='idle'
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
