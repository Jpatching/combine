"""Authored evidence fixtures catch false acceptance; these do not prove play."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "synergy_diagnostic", Path(__file__).resolve().parents[1] / "scripts/check-synergy-diagnostic.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class DiagnosticTests(unittest.TestCase):
    def report(self):
        return {"exitCode": 0, "launched": True, "synergyEnabled": True,
                "binarySha256": "a" * 64, "orderedStream": "single runtime log", "sourceDiagnostics": [
            "SYNERGY_PROBE " + observation for observation in checker.REQUIRED]}

    def baseline(self):
        return dict(self.report(), synergyEnabled=False,
                    sourceDiagnostics=[checker.INHERITED_STATISTICS])

    def test_ordered_flow_and_post_close_shot(self):
        self.assertEqual(checker.failures(self.report(), {}), [])

    def test_pre_open_shot_cannot_prove_post_close_firing(self):
        report = self.report()
        report["sourceDiagnostics"].insert(0, report["sourceDiagnostics"].pop())
        self.assertTrue(checker.failures(report, {}))

    def test_menu_shot_is_rejected_even_when_flow_completes(self):
        report = self.report()
        report["sourceDiagnostics"].insert(2, "SYNERGY_PROBE shot menu_open=1")
        self.assertIn("Gameplay shot leaked while Synergy was open", checker.failures(report, {}))

    def test_statistics_only_exempt_with_matching_baseline(self):
        report = self.report()
        report["sourceDiagnostics"].append(checker.INHERITED_STATISTICS)
        self.assertTrue(checker.failures(report, {}))
        self.assertEqual(checker.failures(report, self.baseline()), [])
        report["sourceDiagnostics"].append("unresolved function new_fault")
        self.assertTrue(checker.failures(report, self.baseline()))

    def test_invalid_baseline_cannot_exempt_statistics(self):
        report = self.report()
        report["sourceDiagnostics"].append(checker.INHERITED_STATISTICS)
        for change in ({"binarySha256": "b" * 64}, {"exitCode": 1},
                       {"stoppedByDiagnostic": True}, {"synergyEnabled": True},
                       {"launched": False}):
            with self.subTest(change=change):
                self.assertTrue(checker.failures(report, dict(self.baseline(), **change)))

    def test_provenance_and_order_required(self):
        for change in ({"binarySha256": "bad"}, {"orderedStream": None},
                       {"launched": False}, {"synergyEnabled": False}):
            with self.subTest(change=change):
                self.assertTrue(checker.failures(dict(self.report(), **change), {}))

    def test_normal_exit_required(self):
        for changes in ({"exitCode": None}, {"exitCode": 1}, {"stoppedByDiagnostic": True}):
            with self.subTest(changes=changes):
                self.assertTrue(checker.failures(dict(self.report(), **changes), {}))


if __name__ == "__main__":
    unittest.main()
