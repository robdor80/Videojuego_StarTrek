"""Measure the real DLL and export auditable Core projections, never manufacture saves."""
from collect_odyssey_evidence import (C, U, W, P, Ref, Population, Stats, Handles, Request,
    Result, Position, Section, Duty, Gap, Person, Candidate, Coverage, struct, row, ok)
import argparse
import csv
import hashlib
import json
import time
from collections import Counter, defaultdict
from pathlib import Path

Resident = struct('Resident', 'person category residence area related_person agenda_kind agenda_start agenda_end', [('present', W), ('agenda_active', W)])
Specialist = struct('Specialist', 'person group section administrative_ship operational_ship superior', [('available', W), ('on_duty', W)])
Auxiliary = struct('Auxiliary', 'entity parent identity', [('docked', W), ('reserved', W)])

def memory():
    class Counters(C.Structure):
        _fields_ = [('cb', W), ('faults', W)] + [(s, C.c_size_t) for s in ['peak_working_set', 'working_set', 'peak_paged', 'paged', 'peak_nonpaged', 'nonpaged', 'pagefile', 'peak_pagefile']]
    data = Counters();data.cb=C.sizeof(data)
    process=C.windll.kernel32.GetCurrentProcess;process.restype=P
    fn=C.windll.psapi.GetProcessMemoryInfo;fn.argtypes=[P,C.POINTER(Counters),W]
    assert fn(process(),C.byref(data),data.cb)
    return {'working_set_bytes':data.working_set,'process_peak_working_set_bytes':data.peak_working_set}

def main():
    parser=argparse.ArgumentParser(__doc__);parser.add_argument('--build-root',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    dll=args.build_root/'native/Release/TrekF04Bridge.dll';lib=C.CDLL(str(dll.resolve()))
    signatures={
      'f04_create_population':[W,C.c_char_p,C.POINTER(Population),C.POINTER(P)],
      'f04_handles':[P,C.POINTER(Handles)],'f04_stats':[P,C.POINTER(Stats)],
      'f04_execute':[P,C.POINTER(Request),C.POINTER(Result)],'f04_destroy':[P],
      'f04_advance':[P,U,U,C.POINTER(U)],'f04_save':[P,P,U,C.POINTER(U)],'f04_load':[P,P,U],
      'f04_service_coverage':[P,Ref,U,U,C.POINTER(Coverage),U,C.POINTER(U)],
      'f04_relief_candidates_page':[P,Ref,U,U,U,U,C.POINTER(Candidate),U,C.POINTER(U),C.POINTER(U)],
      'f04_auxiliary':[P,Ref,C.POINTER(Auxiliary)]}
    pages={'positions':Position,'duties':Duty,'roster_gaps':Gap,'residents':Resident,'specialists':Specialist,'manifest':Person}
    for key,cls in pages.items():signatures['f04_'+key+'_page']=[P,Ref,U,C.POINTER(cls),U,C.POINTER(U),C.POINTER(U)]
    for key,sig in signatures.items():getattr(lib,key).argtypes=sig
    def dump(name,data):(args.output/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    def csvfile(name,data):
        with (args.output/name).open('w',encoding='utf-8',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=data[0].keys());writer.writeheader();writer.writerows(data)
    summaries=[];perf=[]
    for days in [1,7,14,28]:
        s=P();begin=time.perf_counter();ok(lib.f04_create_population(1,b'valhalla',C.byref(Population(69001,404,1800,400,0,0)),C.byref(s)));created=time.perf_counter()
        handles=Handles();ok(lib.f04_handles(s,C.byref(handles)));observer=Ref(handles.ship.scope,3)
        def stats():
            x=Stats();ok(lib.f04_stats(s,C.byref(x)));return x
        def op(kind,aux=0,start=0,end=0,value=0,target=0,expected=0):
            state=stats();result=Result();code=lib.f04_execute(s,C.byref(Request(Ref(observer.scope,state.commander),state.revision,kind,value,target,aux,start,end,40401)),C.byref(result));assert code==expected,(kind,code,expected)
        def page(key,capacity=137):
            result=[];offset=0;n=U();total=U();cls=pages[key]
            while True:
                data=(cls*capacity)();ok(getattr(lib,'f04_'+key+'_page')(s,observer,offset,data,capacity,C.byref(n),C.byref(total)));result.extend(row(data[i]) for i in range(n.value));offset+=n.value
                if offset==total.value:return result
        def coverage(start,end):
            data=(Coverage*8)();n=U();ok(lib.f04_service_coverage(s,observer,start,end,data,8,C.byref(n)));assert n.value==8;return [row(x) for x in data]
        def save():
            size=U();assert lib.f04_save(s,None,0,C.byref(size))==15;data=(C.c_uint8*size.value)();ok(lib.f04_save(s,data,size,C.byref(size)));return data
        try:
            op(25,aux=8191,value=5);installed=time.perf_counter();op(26);seeded=time.perf_counter()
            manifest=page('manifest');queried=time.perf_counter();assert len(manifest)==len({p['id'] for p in manifest})==2200
            op(31,aux=int(days!=1),end=days*86400,value=1 if days==1 else 2);planned=time.perf_counter()
            full=coverage(0,days*86400);covered=time.perf_counter();assert all(c['covered'] and c['first_gap']==c['end'] for c in full)
            duties=page('duties',4096);gaps=page('roster_gaps');positions=page('positions');specialists=page('specialists');residents=page('residents')
            group={p['person']:p['group'] for p in specialists};people=defaultdict(list)
            for d in duties:people[d['person']].append(d)
            assert not set(people)&{r['person'] for r in residents}
            max7=0;min_rest=None;changed=0
            for p,work in people.items():
                work.sort(key=lambda d:d['start']);assert len({d['start']//86400 for d in work})==len(work);changed+=len({d['start']%86400 for d in work})>1
                for i,d in enumerate(work):
                    max7=max(max7,sum(0<=d['start']-x['start']<604800 for x in work))
                    if i:min_rest=min(min_rest if min_rest is not None else 10**12,d['start']-work[i-1]['end'])
            assert max7<=5 and (min_rest is None or min_rest>=43200)
            windows=[]
            for i in range(days*3):
                checks=coverage(i*28800,(i+1)*28800);assert all(c['covered'] and group[c['person']]==1 for c in checks);windows.extend(checks)
            dump(f'critical-windows-{days}-days.json',windows)
            state=stats();summary={'days':days,'shifts':len(duties),'target_shifts':1185*days,'quota_missing':sum(g['missing'] for g in gaps if not g['station']),
              'critical_windows_verified':sum(c['covered'] for c in windows),'critical_windows_expected':days*24,'critical_gap_records':sum(bool(g['station']) for g in gaps),
              'max_rolling7':max7,'min_rest_seconds':min_rest,'people_changing_watch':changed,'captain_shifts':len(people[3]),'core_entities_after_plan':state.entities}
            summaries.append(summary)
            if days==1:
                byslot={d['slot']:['Gamma','Alpha','Beta'][d['start']//28800] for d in duties}
                oracle=[list(map(int,line.split())) for line in (Path(__file__).parent/'tests/fixtures/valhalla_approved.tsv').read_text().splitlines()]
                for section,t,a,b,g,o in oracle:
                    members=[p for p in positions if p['section']==section];counts=Counter(byslot.get(p['id'],'Fuera') for p in members)
                    assert len(members)==t and [counts[k] for k in ['Alpha','Beta','Gamma','Fuera']]==[a,b,g,o]
                csvfile('positions-1800.csv',[dict(p,reference_watch=byslot.get(p['id'],'Fuera')) for p in positions]);csvfile('census-400.csv',residents)
                csvfile('defiant-naval-40.csv',[p for p in specialists if p['group']==2]);csvfile('odin-marines-60.csv',[p for p in specialists if p['group']==3])
                aux=Auxiliary();ok(lib.f04_auxiliary(s,observer,C.byref(aux)));dump('auxiliary.json',row(aux))
            if days==28:csvfile('roster-28-days.csv',duties);dump('gaps-28-days.json',gaps)
            before_save=time.perf_counter();archive=save();saved=time.perf_counter();ok(lib.f04_load(s,archive,len(archive)));loaded=time.perf_counter()
            ok(lib.f04_handles(s,C.byref(handles)));observer=Ref(handles.ship.scope,3);processed=U();ok(lib.f04_advance(s,days*86400-1,4096,C.byref(processed)));advanced=time.perf_counter()
            measure={'days':days,'create_2200_ms':(created-begin)*1000,'install_1800_ms':(installed-created)*1000,'bootstrap_ms':(seeded-installed)*1000,
              'manifest_paged_ms':(queried-seeded)*1000,'plan_ms':(planned-queried)*1000,'coverage_ms':(covered-planned)*1000,'save_ms':(saved-before_save)*1000,
              'load_ms':(loaded-saved)*1000,'advance_ms':(advanced-loaded)*1000,'archive_bytes':len(archive),**memory()}
            persistent=args.build_root/f'valhalla-{days}-days.f04';persistent.write_bytes(bytes(archive));measure['persistent_file_bytes']=persistent.stat().st_size
            assert measure['persistent_file_bytes']==len(archive);perf.append(measure)
            if days==1:
                tick=86399;outgoing=coverage(tick,tick+1)[2]['person'];target=next(d['id'] for d in duties if d['person']==outgoing and d['start']<=tick<d['end'])
                t0=time.perf_counter();op(5,start=tick,end=tick+1,value=2,target=outgoing);t1=time.perf_counter();assert not coverage(tick,tick+1)[2]['covered']
                candidates=(Candidate*1800)();n=U();total=U();t2=time.perf_counter();ok(lib.f04_relief_candidates_page(s,observer,target,tick,tick+1,0,candidates,1800,C.byref(n),C.byref(total)));t3=time.perf_counter();assert n.value>0
                op(32,target=target,aux=candidates[0].person,start=tick,end=tick+1);t4=time.perf_counter();assert coverage(tick,tick+1)[2]['covered']
                dump('incident-performance.json',{'absence_ms':(t1-t0)*1000,'candidate_query_ms':(t3-t2)*1000,'cover_ms':(t4-t3)*1000,'candidates':n.value,'crew':stats().crew,'civilians':stats().civilians,'historical_gaps':page('roster_gaps')})
            if days==28:
                initial=stats();count=len(duties);retained=save();op(31,start=28*86400,end=56*86400,value=2,expected=15)
                assert len(page('duties',4096))==count and stats().crew==1800 and stats().civilians==400
                dump('capacity.json',{'retained_days':28,'rejected_end_day':56,'code':'F04_CAPACITY','entities_before_rejection':initial.entities,'entities_after_rejection':stats().entities,
                  'archive_bytes_retained':len(retained),'archive_bytes_after_rejection':len(save()),'duties_retained':count,'partial_duties_published':0,'limit_entities':65536,'limit_archive_bytes':67108864})
        finally:ok(lib.f04_destroy(s))
        print(json.dumps(summary));print(json.dumps(measure))
    dump('simulations.json',summaries);dump('performance.json',perf);dump('dll-provenance.json',{'sha256':hashlib.sha256(dll.read_bytes()).hexdigest(),'measurement':'single MSI run; process memory includes Python/ctypes and transient transactions, not isolated Core allocation'})

if __name__=='__main__':main()
