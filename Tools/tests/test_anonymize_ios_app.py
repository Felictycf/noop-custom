import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "Tools"
    / "anonymize-ios-app.sh"
)


class AnonymizeIOSAppTests(unittest.TestCase):
    def test_succeeds_when_app_has_no_builder_home_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            app = Path(temp_dir) / "NOOP.app"
            app.mkdir()
            (app / "binary").write_bytes(b"no user path here")
            env = os.environ | {"HOME": "/Users/ci-runner"}

            result = subprocess.run(
                ["bash", str(SCRIPT), str(app)],
                env=env,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("residual home-path hits: 0", result.stdout)


if __name__ == "__main__":
    unittest.main()
