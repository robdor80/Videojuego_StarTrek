#!/usr/bin/env python3
"""Install the versioned pre-commit guard only for this checkout."""
import subprocess
from pathlib import Path

def main():
 root=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
 current=subprocess.run(['git','config','--local','--get','core.hooksPath'],text=True,capture_output=True).stdout.strip()
 target='desarrollo/tools/git_hooks'
 if current and current!=target:
  raise SystemExit(f'Existing hooksPath must be integrated explicitly: {current}')
 default=Path(subprocess.check_output(['git','rev-parse','--git-path','hooks/pre-commit'],cwd=root,text=True).strip())
 if not default.is_absolute():default=root/default
 if not current and default.exists():
  raise SystemExit(f'Existing pre-commit must be integrated explicitly: {default}')
 subprocess.run(['git','config','--local','core.hooksPath',target],cwd=root,check=True)
 print('Installed locally: '+target)
if __name__=='__main__':main()
