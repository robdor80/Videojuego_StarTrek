"""Integrity, provenance, compatibility and real campaign divergence tests."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import history_reference as reference

CORE = '89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98'
BIN = None


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        scratch = os.environ.get('F04_TEST_TEMP_ROOT')
        if not scratch:
            raise RuntimeError('Set F04_TEST_TEMP_ROOT to a disposable output directory before running tests')
        scratch = Path(scratch)
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        manifest = json.loads((reference.REPO / reference.MANIFEST).read_bytes())
        names = {reference.MANIFEST, *manifest['contract_files'], *manifest['provenance_files']}
        for entry in manifest['campaigns'].values():
            names.update((entry['oracle'], entry['acceptance']))
        for name in names:
            destination = self.root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(reference.REPO / name, destination)
        self.manifest = manifest
        self.source = self.root / manifest['campaigns']['5-730']['oracle']

    def verify(self, path=None, profile=5, days=730, core=CORE):
        return reference.verify(path or self.source, profile, days, core, self.root)

    def test_valid_reference(self):
        data, metadata = self.verify()
        self.assertEqual(reference.sha256(data), '4f5b5b096e07e4e9fc2b504cb8b4e86d898655d60e99a678b567ded58140f204')
        self.assertTrue(metadata['reference_contract_verified'])

    def test_all_six_registered_references(self):
        for entry in self.manifest['campaigns'].values():
            with self.subTest(profile=entry['profile'], days=entry['days']):
                self.verify(self.root / entry['oracle'], entry['profile'], entry['days'])

    def test_bad_sha256(self):
        data = self.source.read_bytes()
        self.source.write_bytes(data.replace(b'5afa9577', b'0afa9577', 1))
        with self.assertRaisesRegex(reference.ReferenceError, 'SHA-256 mismatch'):
            self.verify()

    def test_missing(self):
        with self.assertRaisesRegex(reference.ReferenceError, 'Missing/unreadable'):
            self.verify(self.root / 'missing/campaign-5-730.oracle')

    def test_truncated(self):
        self.source.write_bytes(self.source.read_bytes()[:-20])
        with self.assertRaises(reference.ReferenceError):
            self.verify()

    def test_other_profile(self):
        other = self.root / self.manifest['campaigns']['4-365']['oracle']
        self.source.write_bytes(other.read_bytes())
        with self.assertRaises(reference.ReferenceError):
            self.verify()

    def test_other_duration(self):
        other = self.root / self.manifest['campaigns']['5-365']['oracle']
        self.source.write_bytes(other.read_bytes())
        with self.assertRaises(reference.ReferenceError):
            self.verify()

    def test_unregistered_profile_duration(self):
        with self.assertRaisesRegex(reference.ReferenceError, 'No audited reference'):
            self.verify(profile=4)

    def test_incompatible_core(self):
        with self.assertRaisesRegex(reference.ReferenceError, 'Incompatible Core'):
            self.verify(core='0' * 40)

    def test_changed_contract(self):
        path = self.root / 'desarrollo/integration/f04/include/f04_bridge.h'
        path.write_bytes(path.read_bytes() + b'\n// Changed contract\n')
        with self.assertRaisesRegex(reference.ReferenceError, 'Incompatible source/contract'):
            self.verify()

    def test_changed_provenance(self):
        path = self.root / self.manifest['campaigns']['5-730']['acceptance']
        path.write_bytes(b'{}')
        with self.assertRaisesRegex(reference.ReferenceError, 'provenance SHA-256 mismatch'):
            self.verify()

    def test_unknown_manifest_schema(self):
        self.manifest['schema'] = 2
        (self.root / reference.MANIFEST).write_text(json.dumps(self.manifest))
        with self.assertRaisesRegex(reference.ReferenceError, 'Unsupported reference manifest'):
            self.verify()

    def test_row_schema_horizon_and_watermarks(self):
        data = self.source.read_bytes()
        for invalid in (data.splitlines()[0], data + b'1 2 bogus\n',
                        data.replace(b'7 12532 ', b'8 12532 ', 1),
                        data.replace(b'14 21024 ', b'14 12532 ', 1)):
            with self.subTest(invalid=invalid[:30]):
                with self.assertRaises(reference.ReferenceError):
                    reference.validate_rows(invalid, 730)

    def test_copy_and_original_are_unchanged(self):
        original = self.source.read_bytes(), self.source.stat().st_mtime_ns
        destination = self.root / 'staged/campaign-5-730.oracle'
        reference.copy_verified(self.source, destination, 5, 730, CORE, self.root)
        self.assertEqual(destination.read_bytes(), original[0])
        self.assertEqual((self.source.read_bytes(), self.source.stat().st_mtime_ns), original)

    def test_never_overwrites_original_or_existing_file(self):
        original = self.source.read_bytes()
        with self.assertRaisesRegex(reference.ReferenceError, 'Cannot overwrite original'):
            reference.copy_verified(self.source, self.source, 5, 730, CORE, self.root)
        destination = self.root / 'campaign-5-730.oracle'
        destination.write_bytes(b'preexisting backup')
        with self.assertRaises(FileExistsError):
            reference.copy_verified(self.source, destination, 5, 730, CORE, self.root)
        self.assertEqual(destination.read_bytes(), b'preexisting backup')
        self.assertEqual(self.source.read_bytes(), original)

    def test_rejects_without_modifying_original(self):
        original = self.source.read_bytes(), self.source.stat().st_mtime_ns
        with self.assertRaises(reference.ReferenceError):
            reference.copy_verified(self.source, self.root / 'new.oracle', 5, 365, CORE, self.root)
        self.assertEqual((self.source.read_bytes(), self.source.stat().st_mtime_ns), original)

    def test_real_campaign_detects_divergence(self):
        if BIN is None:
            self.skipTest('Native campaign executable required')
        # The unchanged native comparator must reject an actual generated block.
        # No fake campaign output, patched product, or altered original fixture.
        save = self.root / 'divergence'
        rows = self.source.read_text().splitlines()[:2]
        fields = rows[0].split()
        fields[2] = '0' * 64
        rows[0] = ' '.join(fields)
        Path(str(save) + '.oracle').write_text('\n'.join(rows) + '\n')
        result = subprocess.run([str(BIN / 'f04_history_campaign.exe'), 'run', '5', '7', str(save)],
                                capture_output=True, text=True, timeout=120)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('future assignments, events, original facts, RNG and time equal complete-history oracle',
                      result.stderr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bin', type=Path)
    args, remaining = parser.parse_known_args()
    BIN = args.bin
    unittest.main(argv=[__file__, *remaining], verbosity=2)
