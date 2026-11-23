"""Compatibility entry point for actual Tk layout acceptance."""
import argparse
from pathlib import Path
from test_aster_ux_gui import layout

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--runner', type=Path, required=True)
    args = parser.parse_args()
    layout(args.runner.resolve())
