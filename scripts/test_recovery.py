"""Exercise model-server recovery against a prepared Windows dist folder."""
import sys,os,tempfile,time,tkinter as tk
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'app'))
with tempfile.TemporaryDirectory(prefix='akkity-recovery-') as temp:
    os.environ['AKKITY_TEST']='1';os.environ['AKKITY_DATA_DIR']=temp
    import akkity
    akkity.INSTALL=root/'dist'/'Akkity'
    tk.Tk.mainloop=lambda self:None
    app=akkity.Akkity()
    try:
        if not app.server_process:raise RuntimeError('Stop the existing Akkity instance before this isolated recovery test.')
        app.server_process.terminate();app.server_process.wait(timeout=5)
        app.chat();app.root.update()
        app.entry.delete(0,'end');app.entry.insert(0,'What is 2 plus 2?');app.send()
        deadline=time.monotonic()+90
        while app.pending and time.monotonic()<deadline:app.root.update();time.sleep(.02)
        answer=app.messages[-1]['content']
        assert not app.pending and ('4' in answer or 'four' in answer.lower()),answer
        assert app.server_process.poll() is None
        print('PASS: stopped model server restarted automatically and returned a real reply')
    finally:app.exit_app()
