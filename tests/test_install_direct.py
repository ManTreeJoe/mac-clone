"""Exercise installer copies and failure handling in temporary directories only."""
import hashlib
import json
import os
from pathlib import Path
import plistlib
import subprocess
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class DirectInstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='mac-clone-test-')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.dest = self.base / 'Applications with spaces'
        self.manifest = self.base / 'manifest.tsv'
        self.bin = self.base / 'bin'
        self.bin.mkdir()
        self.archive = self.base / 'app.zip'
        with zipfile.ZipFile(self.archive, 'w') as z:
            z.writestr('Test App.app/Contents/Info.plist', plistlib.dumps({
                'CFBundleIdentifier': 'dev.example.test',
                'CFBundleShortVersionString': '1.0',
            }))
        self.sha = hashlib.sha256(self.archive.read_bytes()).hexdigest()
        self.env = {**os.environ, 'PATH': str(self.bin) + ':' + os.environ['PATH'],
                    'MAC_CLONE_APP_DIR': str(self.dest),
                    'MAC_CLONE_DIRECT_MANIFEST': str(self.manifest),
                    'FIXTURE': str(self.archive), 'CURL_LOG': str(self.base / 'curl.log')}
        self.command('curl', '''#!/usr/bin/env python3
import json,os,pathlib,shutil,sys
args=sys.argv[1:]; url=next(a for a in args if a.startswith('https://'))
with open(os.environ['CURL_LOG'],'a') as f: f.write(url+'\\n')
if '/fail' in url: sys.exit(22)
out=args[args.index('-o')+1]
if '/api?' in url:
 pathlib.Path(out).write_text(json.dumps({'data':{'linkData':{'tempUrl':os.environ.get('SIGNED_URL','https://dl-us.ugreennas.com/fixture.dmg?signature=fresh')}}}))
else: shutil.copyfile(os.environ['FIXTURE'],out)
''')
        self.command('hdiutil', '''#!/usr/bin/env python3
import sys,zipfile
if sys.argv[1]=='attach':
 with zipfile.ZipFile(sys.argv[2]) as z: z.extractall(sys.argv[sys.argv.index('-mountpoint')+1])
''')

    def command(self, name, text):
        path = self.bin / name
        path.write_text(text)
        path.chmod(0o755)

    def row(self, **changes):
        row = dict(name='Test App', bundle='dev.example.test', version='1.0',
                   type='zip', url='https://example.test/app.zip', sha=self.sha, arch='any')
        row.update(changes)
        return '\t'.join(row.values())

    def run_installer(self, *rows):
        self.manifest.write_text('\n'.join(rows) + '\n')
        return subprocess.run(['/bin/bash', str(ROOT / 'scripts/install-direct.sh')],
                              env=self.env, text=True, errors='replace', capture_output=True)

    def test_install_and_rerun_preserves_existing(self):
        first = self.run_installer(self.row())
        self.assertEqual(first.returncode, 0, first.stderr)
        marker = self.dest / 'Test App.app/keep-me'
        marker.write_text('existing')
        calls = (self.base / 'curl.log').read_text()
        again = self.run_installer(self.row())
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertIn('Already installed', again.stdout)
        self.assertTrue(marker.exists())
        self.assertEqual(calls, (self.base / 'curl.log').read_text())

    def test_checksum_mismatch_does_not_install(self):
        result = self.run_installer(self.row(sha='0' * 64))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Checksum mismatch', result.stderr)
        self.assertFalse((self.dest / 'Test App.app').exists())

    def test_wrong_bundle_does_not_install(self):
        result = self.run_installer(self.row(bundle='wrong.app'))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('identity mismatch', result.stderr)
        self.assertFalse((self.dest / 'Test App.app').exists())

    def test_failure_does_not_skip_later_apps(self):
        result = self.run_installer(self.row(name='Failed App', url='https://example.test/fail'), self.row())
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('FAILED: Failed App', result.stderr)
        self.assertTrue((self.dest / 'Test App.app').exists())

    def test_ugreen_resolves_fresh_link_and_mounts(self):
        result = self.run_installer(self.row(type='ugreen-dmg', url='https://api-us.ugnas.com/api?appType=client&id=423'))
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = (self.base / 'curl.log').read_text()
        self.assertIn('&_=', calls)
        self.assertIn('https://dl-us.ugreennas.com/fixture.dmg?signature=fresh', calls)
        self.assertTrue((self.dest / 'Test App.app').exists())

    def test_ugreen_rejects_unexpected_host(self):
        self.env['SIGNED_URL'] = 'https://other.example/app.dmg'
        result = self.run_installer(self.row(type='ugreen-dmg', url='https://api-us.ugnas.com/api?appType=client&id=423'))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('no valid official download link', result.stderr)
        self.assertFalse((self.dest / 'Test App.app').exists())

    def test_existing_wrong_app_is_not_overwritten(self):
        target = self.dest / 'Test App.app'
        target.mkdir(parents=True)
        marker = target / 'keep-me'
        marker.write_text('existing')
        result = self.run_installer(self.row())
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(marker.exists())
        self.assertFalse((self.base / 'curl.log').exists())


if __name__ == '__main__':
    unittest.main()
