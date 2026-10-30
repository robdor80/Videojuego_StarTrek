"""Run the three real PIE suites sequentially in one GPU editor process."""
import unreal as u,pathlib,json,time,traceback
ROOT=pathlib.Path(__file__).parent
JOBS=['runtime_quinn.py','runtime_doors.py','runtime_stations.py'];STATE={'index':-1,'started':time.monotonic(),'results':[]};ACTIVE={}
def launch():
    STATE['index']+=1
    if STATE['index']>=len(JOBS):
        (ROOT/'Data/final_suite_verified.json').write_text(json.dumps(STATE,indent=2));u.unregister_slate_post_tick_callback(master);u.SystemLibrary.quit_editor();return
    path=ROOT/JOBS[STATE['index']];source=path.read_text(encoding='utf-8')
    source=source.replace('u.SystemLibrary.quit_editor()','None').replace('limited_runtime_check.json','quinn_verified.json').replace('doors_pbr_validation.json','doors_verified.json').replace('stations_runtime.json','stations_verified.json').replace('.png','_Verificada.png')
    ACTIVE.clear();ACTIVE.update({'__file__':str(path),'__name__':'__main__'})
    exec(compile(source,str(path),'exec'),ACTIVE)
def monitor(dt):
    try:
        if STATE['index']==-1:launch();return
        state=ACTIVE.get('S',{})
        if state.get('phase') in ['end','done'] and time.monotonic()-state.get('ended',time.monotonic())>3:
            STATE['results'].append({'job':JOBS[STATE['index']],'ok':state['ok'],'checks':len(state['checks']),'error':state.get('error')});launch()
        if time.monotonic()-STATE['started']>300:raise RuntimeError('Final suite timeout')
    except Exception:
        STATE['error']=traceback.format_exc();(ROOT/'Data/final_suite_verified.json').write_text(json.dumps(STATE,indent=2));u.unregister_slate_post_tick_callback(master);u.SystemLibrary.quit_editor()
master=u.register_slate_post_tick_callback(monitor)
