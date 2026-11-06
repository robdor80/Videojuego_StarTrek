"""Check the runtime report, including the side-jump safety invariant.

Usage: python check_v07_closure_report.py <report.json>
The existing probe's final look-ahead can point at a jamb after a jump. Require
observed contact with B08 and that Quinn never crosses its protected plane,
rather than requiring the final look-ahead to keep pointing at the panel.
"""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('report', type=Path)
    args = parser.parse_args()
    plan = json.loads(Path(__file__).with_name('v07_closure_plan.json').read_text(encoding='utf8'))
    report = json.loads(args.report.read_text(encoding='utf8'))
    rows = report['results']
    assert [r['name'] for r in rows] == [c['name'] for c in plan['cases']], 'Missing, repeated or unexpected cases'
    assert report['capsule_radius_cm'] == 35 and report['capsule_half_height_cm'] == 90
    assert 'Quinn' in report['mesh'] and 'EnhancedPlayerInput' in report['player_input_class']
    for row in rows:
        assert row['passed'] and row['walkable_floor'] and not row['falling'], row['name']
        assert row['waypoints_reached'] == 0, row['name']
        if row['name'].startswith('B08_'):
            samples = row['trace'] + [row]
            assert row['trace'], row['name']
            assert all(t['feet_cm'][1] >= -25 and t['feet_cm'][2] >= 36 for t in samples), row['name']
            assert any(t.get('ahead_actor', '').startswith('V07_B08') for t in samples), row['name']
            if row['name'].endswith('_salto'):
                assert max(t['feet_cm'][2] for t in samples) >= 50, row['name']
    print(f'{len(rows)}/{len(rows)} runtime cases; B08 protected plane retained in all recorded samples')


if __name__ == '__main__':
    main()
