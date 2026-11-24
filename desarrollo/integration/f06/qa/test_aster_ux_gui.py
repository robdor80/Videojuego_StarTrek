"""Real Tk/native UX verification; tick checks do not certify owner acceptance."""
import argparse
import json
from pathlib import Path
import time
import sys
import tkinter as tk
from tkinter import messagebox
from aster_gui import Panel


def visible_contacts(panel):
    return [cid for group in panel.contacts_table.get_children() for cid in panel.contacts_table.get_children(group)]


def verify_layout(panel, root):
    root.update()
    frames=panel.zone_frames
    assert [f.cget('highlightbackground') for f in frames]==['#b94343','#3b70bd','#32834d']
    assert all(int(f.cget('highlightthickness'))==3 for f in frames)
    assert frames[0].winfo_rootx()<frames[1].winfo_rootx()<frames[2].winfo_rootx()
    assert panel.map_canvas.winfo_rooty()<panel.main_text.winfo_rooty()
    widgets=[panel.footer,panel.notice_bar,panel.contacts_table,panel.map_canvas,panel.main_text,panel.detail_text,*panel.navigation_buttons.values()]
    widgets += [w for w in (panel.action_area,panel.contact_report_button,panel.voice_button,panel.science_transfer_button,
                           panel.tactical_report_button,panel.unfollow_button,panel.resume_button) if w.winfo_manager()]
    for w in widgets:
        assert w.winfo_viewable() and w.winfo_height()>=10 and w.winfo_width()>=15,(str(w),w.winfo_width(),w.winfo_height())
        assert root.winfo_rootx()<=w.winfo_rootx() and w.winfo_rootx()+w.winfo_width()<=root.winfo_rootx()+root.winfo_width()+1,str(w)
        assert w.winfo_rooty()+w.winfo_height()<=root.winfo_rooty()+root.winfo_height()+1,str(w)


def layout(runner):
    for geometry,scale in (('1460x825',1.33),('1150x700',1.33),('2560x1600',2.0),('1706x1066',2.0),('1280x800',1.67)):
        root=tk.Tk();panel=None
        try:
            root.tk.call('tk','scaling',scale)
            panel=Panel(root,runner,x1=True);panel.playing=False
            root.geometry(geometry);root.update()
            assert len(visible_contacts(panel))==16 and not panel.contacts_table.selection()
            canvas=panel.map_canvas
            assert (panel.ship_sources['top'].width(), panel.ship_sources['top'].height())==(1086,1448)
            assert (panel.ship_sources['side'].width(), panel.ship_sources['side'].height())==(1672,941)
            assert len(canvas.find_withtag('ship:top'))==len(canvas.find_withtag('ship:side'))==1
            assert len(panel.map_positions)>=20, 'overview must show multiple observed contacts in both views'
            for view in ('top','side'):
                box=canvas.bbox(canvas.find_withtag('ship:'+view)[0])
                assert 0<=box[0]<box[2]<=canvas.winfo_width() and 0<=box[1]<box[3]<=canvas.winfo_height()
            assert 'ENTORNO OBSERVADO' in panel.detail_text.get('1.0','end')
            for view in ('status','contacts','tracking','results'):
                panel.navigate(view);verify_layout(panel,root)
            panel.navigate('contacts')
            planet=next(str(c[0]) for c in panel.state['contacts'] if c[1]==13)
            panel._choose_contact(planet);root.update();verify_layout(panel,root)
            assert canvas.find_withtag('contact:'+planet)
            assert {canvas.gettags(item)[1] for item in canvas.find_withtag('contact:'+planet)
                    if len(canvas.gettags(item))>1}=={'view:top','view:side'}
            active=panel.contact_map[planet]
            panel.contact_map[planet]=active.copy();panel.contact_map[planet][2]=2
            panel._draw_map()
            assert all(canvas.type(item)=='line' for item in canvas.find_withtag('contact:'+planet)[:2])
            assert not canvas.find_withtag('trajectory')
            panel.contact_map[planet]=active
            panel._draw_map()
            assert any(canvas.type(item)=='oval' for item in canvas.find_withtag('contact:'+planet))
            assert panel.science_transfer_button.winfo_viewable() and len(visible_contacts(panel))==16
            print(f'PASS actual Tk {geometry}; scaling={scale}',flush=True)
        finally:
            if panel:panel.close()
            else:root.destroy()


def run(runner,output,realtime=False):
    output.mkdir(parents=True,exist_ok=True)
    def unexpected(*args,**kwargs):raise AssertionError(args)
    messagebox.showwarning=unexpected;messagebox.showerror=unexpected
    root=tk.Tk();panel=None
    try:
        panel=Panel(root,runner,x1=True,telemetry=output/'latency.jsonl');root.update()
        assert panel.speed.get()=='×1' and panel.playing and panel.state['automatic']==1
        if realtime:
            started=time.monotonic();checked=set();followed=False
            while panel.state['tick']<540:
                root.update();tick=panel.state['tick']
                for due in (60,150,240,390):
                    if tick>=due and due not in checked:
                        checked.add(due)
                        assert any(e['tick']==due for e in panel.state['equipment']),due
                        print(f'Automatic sheet t={due}, real elapsed={time.monotonic()-started:.3f}s',flush=True)
                if tick>=155 and not followed:
                    rom=next(c for c in panel.state['contacts'] if c[1]==1 and c[3]==8)
                    panel.navigate('contacts');panel._choose_contact(str(rom[0]));panel.contact_action('PRIORITY');followed=True
                assert time.monotonic()-started<570,'real-time watch stalled'
                time.sleep(.03)
            elapsed=time.monotonic()-started;assert 538<=elapsed<=550,elapsed
            arrivals=[json.loads(line) for line in (output/'latency.jsonl').read_text().splitlines() if json.loads(line)['tick'] in (60,150,240,390)]
            assert len(arrivals)==4 and all(r['realtime'] and r['source_to_gui_s']<=3 and r['native_latency_s']<=3 for r in arrivals),arrivals
            assert len([d for d in panel.state['deliveries'] if d[4]==2])>10
            (output/'realtime-summary.json').write_text(json.dumps({'status':'PASS','environment':'Actual Tk/native; MSI owner acceptance pending','elapsed_s':elapsed,'arrivals':arrivals},indent=2))
            print(f'PASS real-time x1 watch: {elapsed:.3f}s; MSI acceptance pending');return
        panel.playing=False;panel.navigate('contacts')
        planet=next(str(c[0]) for c in panel.state['contacts'] if c[1]==13)
        panel._choose_contact(planet);root.update()
        assert 'Temperatura:' in panel.detail_text.get('1.0','end')
        panel.contact_action('SCAN');root.update()
        assert panel.current_view=='results' and visible_contacts(panel)==[planet]
        text=panel.detail_text.get('1.0','end')
        assert 'Presión parcial de O₂' in text and 'Temperatura:' not in text
        assert not panel.scan_progress.winfo_manager()
        panel.transfer_contact('SCIENCE_SEND');assert panel.state['deliveries'][-1][4:]==[3,1]
        panel.detail_text.yview_moveto(.4);scroll=panel.detail_text.yview()[0]
        panel.apply(panel.command('STEP 60'));root.update()
        assert panel.current_view=='results' and panel.contacts_table.selection()==(planet,),'routine cargo interrupted study'
        assert panel.detail_text.yview()[0]==scroll
        panel.apply(panel.command('STEP 90'));root.update()
        rom=next(str(c[0]) for c in panel.state['contacts'] if c[1]==1 and c[3]==8)
        assert panel.current_view=='contacts' and panel.contacts_table.selection()==(rom,)
        assert panel.interrupted['view']=='results' and panel.interrupted['selected']==planet
        assert '8 detectados' in panel.detail_text.get('1.0','end') and panel.detail_text.yview()[0]==0
        assert panel.detail_text.tag_ranges('ÁMBAR') and panel.resume_button.winfo_viewable()
        panel.resume_study();root.update()
        assert panel.current_view=='results' and panel.contacts_table.selection()==(planet,)
        assert abs(panel.detail_text.yview()[0]-scroll)<.02
        panel.navigate('contacts');panel._choose_contact(rom);panel.report_contact_to_officer()
        panel.contact_action('PRIORITY');root.update()
        assert panel.current_view=='tracking' and visible_contacts(panel)==[rom]
        n=len(panel.state['deliveries']);panel.apply(panel.command('STEP 10'));root.update()
        assert len(panel.state['deliveries'])>n and 'Velocidad relativa:' in panel.detail_text.get('1.0','end')
        assert panel.map_canvas.find_withtag('trajectory'), 'tracking map requires archived position trace'
        assert not panel.tactical_report_button.winfo_manager()
        panel.contact_action('SCAN');root.update();assert 'Extensión angular' in panel.detail_text.get('1.0','end')
        panel.checkpoint('SAVE');panel.apply(panel.command('STEP 5'));panel.checkpoint('LOAD');root.update()
        assert rom in panel.followed_ids and rom in panel.analyzed_ids
        path=output/'context.aster';panel.checkpoint_file(path,False);view=panel.current_view
        panel.close();panel=None
        root=tk.Tk();panel=Panel(root,runner,x1=True);panel.playing=False
        panel.checkpoint_file(path,True);root.update()
        assert panel.current_view==view and panel.contacts_table.selection()==(rom,)
        assert rom in panel.followed_ids and planet in panel.analyzed_ids
        sidecar=path.with_suffix(path.suffix+'.ui.json');original=sidecar.read_text(encoding='utf-8')
        corrupt=json.loads(original);corrupt['core_sha256']='0'*64
        sidecar.write_text(json.dumps(corrupt),encoding='utf-8')
        state_before=panel.state
        try:panel.checkpoint_file(path,True)
        except ValueError:pass
        else:raise AssertionError('mismatched UI/Core pair accepted')
        assert panel.state is state_before, 'mismatched context must not mutate Core'
        sidecar.write_text(original,encoding='utf-8')
        panel.open_report_dialog();root.update()
        pending=next(w for w in root.winfo_children() if isinstance(w,tk.Toplevel))
        pending_chooser=next(w for w in pending.winfo_children() if w.winfo_class()=='TCombobox')
        pending_chooser.set('Ciencia')
        panel.apply(panel.command(f'STEP {240-panel.state["tick"]}'));root.update()
        unknown=next(str(c[0]) for c in panel.state['contacts'] if c[1]==1 and c[3]==0)
        assert panel.contacts_table.selection()==(unknown,)
        next(w for w in pending.winfo_children() if w.winfo_class()=='TButton').invoke()
        assert panel.state['deliveries'][-1][1]==int(rom), 'open report must keep its original subject'
        text=panel.detail_text.get('1.0','end');assert 'no observable' in text and 'sin referencia' in text and 'Blindaje: 1' not in text
        panel.apply(panel.command('STEP 60'));root.update()
        assert panel.contacts_table.selection()==(rom,) and 'Emisión ofensiva' in panel.alert_description.cget('text')
        assert panel.interrupted['selected']==unknown and panel.interrupted_stack[-1]['selected']==rom
        panel.report_contact_to_officer()
        assert len([d for d in panel.state['deliveries'] if d[1]==int(rom) and d[4]==1])==2
        panel.open_report_dialog();root.update()
        dialog=next(w for w in root.winfo_children() if isinstance(w,tk.Toplevel))
        chooser=next(w for w in dialog.winfo_children() if w.winfo_class()=='TCombobox')
        assert len(chooser.cget('values'))==3
        chooser.set('Ciencia')
        next(w for w in dialog.winfo_children() if w.winfo_class()=='TButton').invoke()
        assert panel.state['deliveries'][-1][4:]==[3,1]
        for geometry in ('1460x825','1150x700'):
            root.geometry(geometry);root.attributes('-topmost',True);root.update();verify_layout(panel,root)
            deadline=time.monotonic()+.25
            while time.monotonic()<deadline:root.update();time.sleep(.01)
            try:
                from PIL import ImageGrab
                capture = (ImageGrab.grab(window=int(root.wm_frame(),0)) if sys.platform=='win32' else
                           ImageGrab.grab(bbox=(root.winfo_rootx(),root.winfo_rooty(),root.winfo_rootx()+root.winfo_width(),root.winfo_rooty()+root.winfo_height())))
                capture.save(output/f'layout-{geometry}.png')
            except (ImportError,OSError):pass
        panel.apply(panel.command('STEP 120'));root.update();assert not panel.alert_bar.winfo_viewable(),'offensive alert must retire'
        panel.resume_study();root.update();assert panel.contacts_table.selection()==(unknown,)
        assert panel.resume_button.winfo_viewable()
        panel.resume_study();root.update();assert panel.current_view=='results' and panel.contacts_table.selection()==(rom,)
        n=len(panel.state['deliveries']);panel.communicate_voice();root.update()
        voice=[w for w in root.winfo_children() if isinstance(w,tk.Toplevel)]
        assert voice and 'guion QA' in voice[-1].title() and len(panel.state['deliveries'])==n
        for window in voice:window.destroy()
        panel.apply(panel.command('STEP 30'));root.update();assert panel.state['offline'] and not panel.alert_bar.winfo_viewable()
        panel.apply(panel.command('STEP 15'));root.update();panel.navigate('tracking');panel._choose_contact(rom)
        assert 'suspendido' in panel.detail_text.get('1.0','end')
        (output/'gui-summary.json').write_text(json.dumps({'status':'PASS','owner_acceptance':'PENDING'}))
        print('PASS actual Tk: frames, four views, physics, interrupts, queues, restore, alert lifecycle')
    finally:
        if panel:panel.close()
        else:
            try:root.destroy()
            except tk.TclError:pass


def main():
    p=argparse.ArgumentParser();p.add_argument('--runner',required=True,type=Path)
    p.add_argument('--output-dir',type=Path);p.add_argument('--realtime',action='store_true');p.add_argument('--layout',action='store_true')
    a=p.parse_args()
    if a.layout:layout(a.runner.resolve())
    else:run(a.runner.resolve(),a.output_dir,a.realtime)


if __name__=='__main__':main()
