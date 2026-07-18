from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "secret-regression-scan.yml"


class SecretWorkflowCheckoutTests(unittest.TestCase):
    def test_checkout_is_bound_to_event_head(self):
        text = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn(
            "ref: ${{ github.event.pull_request.head.sha || github.sha }}",
            text,
        )
        self.assertIn("fetch-depth: 0", text)


if __name__ == "__main__":
    unittest.main()
