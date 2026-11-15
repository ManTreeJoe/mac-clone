"""Check orchestration without running Homebrew or touching real applications."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def test_status_aggregates_brew_and_direct_failures(self):
        for brew_status, direct_status in [(0, 0), (1, 0), (0, 1), (1, 1)]:
            with self.subTest(brew=brew_status, direct=direct_status), tempfile.TemporaryDirectory() as temp:
                base = Path(temp)
                (base / 'scripts').mkdir()
                shutil.copyfile(ROOT / 'scripts/install.sh', base / 'scripts/install.sh')
                (base / 'MANUAL-INSTALL.md').write_text('Sign into your apps.\n')
                (base / 'Brewfile.selected').write_text('# fixture\n')
                (base / 'scripts/install-direct.sh').write_text(
                    '#!/bin/bash\necho direct-stage-ran\nexit "$DIRECT_STATUS"\n')
                (base / 'bin').mkdir()
                brew = base / 'bin/brew'
                brew.write_text('#!/bin/bash\nprintf "%s\\n" "$*"\nexit "$BREW_STATUS"\n')
                brew.chmod(0o755)
                env = {**os.environ, 'PATH': str(base / 'bin') + ':' + os.environ['PATH'],
                       'BREW_STATUS': str(brew_status), 'DIRECT_STATUS': str(direct_status)}
                result = subprocess.run(['/bin/bash', str(base / 'scripts/install.sh')],
                                        env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, int(bool(brew_status or direct_status)))
                self.assertIn('direct-stage-ran', result.stdout)
                self.assertIn('--no-upgrade', result.stdout)
                self.assertEqual('All selected app installation steps finished.' in result.stdout,
                                 not (brew_status or direct_status))


if __name__ == '__main__':
    unittest.main()
