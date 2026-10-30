"""Produce archives with the pre-Valhalla DLL, restore/continue using new readers."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

def main():
    p=argparse.ArgumentParser(__doc__);p.add_argument('--previous-build',type=Path,required=True);p.add_argument('--new-build',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    folder=args.new_build.parent/'compatibility';folder.mkdir(exist_ok=True)
    producer=args.previous_build/'Release';reader=args.new_build/'Release';result={}
    for cls,exe in [('miranda','f04_organization_tests.exe'),('intrepid','f04_intrepid_tests.exe'),('sovereign','f04_sovereign_tests.exe'),('odyssey','f04_odyssey_tests.exe')]:
        archive=folder/(cls+'.f04')
        made=subprocess.run([str(producer/exe),'process_save',str(archive)],check=True,capture_output=True,text=True)
        loaded=subprocess.run([str(reader/exe),'process_load',str(archive)],check=True,capture_output=True,text=True)
        result[cls]={'archive_bytes':archive.stat().st_size,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'producer_dll_sha256':hashlib.sha256((producer/'TrekF04Bridge.dll').read_bytes()).hexdigest(),
          'reader_dll_sha256':hashlib.sha256((reader/'TrekF04Bridge.dll').read_bytes()).hexdigest(),'producer':made.stdout.strip(),'new_reader':loaded.stdout.strip(),'same_future':True}
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
