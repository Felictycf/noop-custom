from pathlib import Path
import unittest


WORKFLOW = (
    Path(__file__).resolve().parents[2]
    / ".github"
    / "workflows"
    / "ios-sideload-build.yml"
)


class IOSSideLoadWorkflowTests(unittest.TestCase):
    def test_manual_or_source_push_builds_unsigned_ipa_as_artifact(self):
        workflow = WORKFLOW.read_text()

        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("push:", workflow)
        self.assertIn("xcodegen generate", workflow)
        self.assertIn("generic/platform=iOS", workflow)
        self.assertIn("CODE_SIGNING_ALLOWED=NO", workflow)
        self.assertIn("Tools/prepare-ios-sideload-app.sh", workflow)
        self.assertIn("actions/upload-artifact@", workflow)
        self.assertIn("NOOP-custom-ios-unsigned.ipa", workflow)
        self.assertNotIn("${{ secrets.", workflow)


if __name__ == "__main__":
    unittest.main()
