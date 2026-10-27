#!/usr/bin/env python3
"""Recreate reserved empty folders without modifying any existing file."""
import json
from pathlib import Path

def main():
 root=Path(__file__).resolve().parents[2]
 data=json.loads((root/'desarrollo/manifests/project_structure.json').read_text(encoding='utf-8'))
 for relative in data['directories']:
  target=(root/relative).resolve()
  if not target.is_relative_to(root):raise ValueError('Path outside project: '+relative)
  target.mkdir(parents=True,exist_ok=True)
 print(f"Estructura preparada: {len(data['directories'])} directorios.")
if __name__=='__main__':main()
