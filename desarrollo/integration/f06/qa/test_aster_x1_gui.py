"""Actual Tk + native Core checks. --realtime runs a full nine-minute watch."""
import argparse
import json
from pathlib import Path
import time
import tkinter as tk
from aster_gui import Panel


def run(runner, output, realtime=False):
    output.mkdir(parents=True, exist_ok=True)
    root=tk.Tk();panel=None
    try:
        panel=Panel(root,runner,x1=True,telemetry=output/'latency.jsonl')
        root.update();assert panel.speed.get()=='×1' and panel.playing
        assert panel.state['automatic']==1
        if realtime:
            started=time.monotonic();delivered=False;checked=set()
            while panel.state['tick']<540:
                root.update()
                tick=panel.state['tick']
                for due in (60,150,240,390):
                    if tick>=due and due not in checked:
                        checked.add(due)
                        assert any(e['tick']==due for e in panel.state['equipment']), (due,panel.state)
                        print(f'Observed automatic ficha t={due}, real elapsed={time.monotonic()-started:.3f}s',flush=True)
                if tick>=420 and not delivered:
                    panel.navigate('status')
                    subject=next(c for c in panel.state['contacts'] if c[3]==0)
                    panel._choose_contact(str(subject[0]));root.update()
                    panel.report_contact_to_officer();panel.send_analysis_to_tactical()
                    panel.transfer_contact('SCIENCE_SEND')
                    assert len(panel.state['deliveries'])==3
                    delivered=True
                assert time.monotonic()-started<570,'real-time watch stalled'
                time.sleep(.03)
            elapsed=time.monotonic()-started
            assert 538<=elapsed<=550,elapsed
            records=[json.loads(l) for l in (output/'latency.jsonl').read_text().splitlines()]
            arrivals=[r for r in records if r['tick'] in (60,150,240,390)]
            assert len(arrivals)==4,arrivals
            assert all(r['realtime'] and r['source_to_gui_s']<=3 and r['native_latency_s']<=3 for r in arrivals),arrivals
            (output/'realtime-summary.json').write_text(json.dumps({'status':'PASS',
                'environment':'Cloud Linux Tk; not MSI acceptance','elapsed_s':elapsed,
                'arrivals':arrivals},indent=2))
            print(f'PASS Cloud real-time ×1 watch: {elapsed:.3f}s; MSI acceptance remains pending')
            return
        panel.playing=False
        assert 'FICHA AUTOMÁTICA' in panel.auto_brief.cget('text')
        first=panel.contacts_table.selection()
        for target in (60,150,210,240,300,360,390):
            panel.apply(panel.command(f'STEP {target-panel.state["tick"]}'));root.update()
            if target==60:
                assert panel.contacts_table.selection()==first,'routine arrival must preserve selection'
                assert 'Transporte civil' in panel.auto_brief.cget('text')
            if target==150:
                assert panel.alert_bar.winfo_viewable()
                assert 'EQUIPAMIENTO' in panel.alert_title.cget('text')
                panel.open_alert_contact();root.update()
                text=panel.detail_text.get('1.0','end')
                assert '8 detectados' in text and 'catálogo 6' in text and 'ÁMBAR' in text,text
                assert panel.detail_text.tag_ranges('ÁMBAR')
            if target==240:
                unknown=next(c for c in panel.state['contacts'] if c[3]==0)
                panel.navigate('status');panel._choose_contact(str(unknown[0]));root.update()
                text=panel.detail_text.get('1.0','end')
                assert 'no disponible' in text and 'GRIS' in text and 'Clase de nave no catalogada' not in text,text
                assert 'Blindaje: 1' not in text,'private armour must stay unobservable'
                assert panel.tactical_report_button.winfo_viewable() and panel.science_transfer_button.winfo_viewable()
                panel.report_contact_to_officer();panel.send_analysis_to_tactical();panel.transfer_contact('SCIENCE_SEND')
                assert len(panel.state['deliveries'])==3
                assert panel.state['deliveries'][0][2] in {e['id'] for e in panel.state['equipment']}
            if target==300:
                rom=next(c for c in panel.state['contacts'] if c[3]==8)
                panel.navigate('status');panel._choose_contact(str(rom[0]));root.update()
                assert 'ROJO' in panel.detail_text.get('1.0','end')
        for geometry in ('1460x825','1150x700'):
            root.geometry(geometry);root.update()
            try:
                from PIL import ImageGrab
                ImageGrab.grab().save(output/f'layout-{geometry}.png')
            except ImportError:
                pass
            for widget in (panel.footer,panel.notice_bar,panel.detail_text,
                           panel.tactical_report_button,panel.science_transfer_button,
                           *panel.equipment_brief_lines):
                assert widget.winfo_viewable(),widget
                assert widget.winfo_rootx()+widget.winfo_width()<=root.winfo_rootx()+root.winfo_width()+1
                assert widget.winfo_rooty()+widget.winfo_height()<=root.winfo_rooty()+root.winfo_height()+1
        try:
            from PIL import ImageGrab
            ImageGrab.grab().save(output/'aster-x1.png')
        except ImportError:
            pass
        print('PASS real Tk ASTER_X1: 3 zones, equipment colors, receipts, selection, scroll, 1150x700')
    finally:
        if panel:panel.close()
        else:root.destroy()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--runner',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--realtime',action='store_true')
    a=p.parse_args();run(a.runner.resolve(),a.output_dir,a.realtime)
