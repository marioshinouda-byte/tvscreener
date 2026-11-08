import hashlib
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from scripts.forex_scan_schedule import decide_scan, read_json, record_success


class HourlyScanScheduleTest(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 8, 10, 27, tzinfo=timezone.utc)
        self.report = b"# Completed scanner report\n"
        self.source_sha256 = "unchanged-scanner-source"
        self.health = {
            "status": "completed",
            "completed_at": "2026-11-08T10:17:00+00:00",
            "report_sha256": hashlib.sha256(self.report).hexdigest(),
            "source_sha256": self.source_sha256,
        }

    def decision(self, event_name="push", *, request=None,
                 health=None, report=None):
        return decide_scan(
            event_name, request or {},
            self.health if health is None else health,
            self.report if report is None else report, self.source_sha256, self.now,
        )[0]

    def test_request_and_cron_skip_an_already_published_current_hour(self):
        self.assertFalse(self.decision())
        self.assertFalse(self.decision("schedule"))

    def test_previous_hour_is_due_even_when_less_than_sixty_minutes_old(self):
        self.health["completed_at"] = "2026-11-08T09:58:00+00:00"
        self.assertTrue(self.decision())

    def test_missing_bad_and_future_success_records_trigger_recovery(self):
        for health in ({}, {"completed_at": "bad"},
                       {**self.health, "completed_at": "2026-11-08T10:40:00+00:00"},
                       {**self.health, "completed_at": "2026-11-08T10:17:00"},
                       {**self.health, "status": "failed"}):
            with self.subTest(health=health):
                self.assertTrue(self.decision(health=health))

    def test_stale_or_empty_report_cannot_be_hidden_by_a_recent_record(self):
        self.assertTrue(self.decision(report=b"# Old report\n"))
        self.assertTrue(self.decision(report=b""))

    def test_manual_and_explicit_recovery_requests_can_run_again(self):
        self.assertTrue(self.decision("workflow_dispatch"))
        self.assertTrue(self.decision(request={"force": True}))
        self.assertFalse(self.decision(request={"force": "false"}))

    def test_code_changes_are_validated_even_when_this_hour_was_scanned(self):
        self.source_sha256 = "updated-scanner-source"
        self.assertTrue(self.decision())

    def test_utc_hour_comparison_handles_athens_and_dst_repeated_hours(self):
        self.health["completed_at"] = "2026-11-08T12:17:00+02:00"
        self.assertFalse(self.decision())
        self.health["completed_at"] = "2026-10-25T03:17:00+03:00"
        now = datetime(2026, 10, 25, 1, 27, tzinfo=timezone.utc)
        self.assertTrue(decide_scan("schedule", {}, self.health,
                                    self.report, self.source_sha256, now)[0])

    def test_success_record_binds_completion_to_the_published_report(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.md"
            state = Path(directory) / "health.json"
            report.write_bytes(self.report)
            health = record_success(state, report, self.now, self.source_sha256)
            self.assertEqual(read_json(state), health)
            self.assertFalse(self.decision(health=health))

    def test_empty_report_does_not_create_a_success_record(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.md"
            state = Path(directory) / "health.json"
            report.write_bytes(b"")
            with self.assertRaises(ValueError):
                record_success(state, report, self.now, self.source_sha256)
            self.assertFalse(state.exists())


if __name__ == "__main__":
    unittest.main()
