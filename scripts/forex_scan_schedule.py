"""Deduplicate hourly scan requests and record successfully published reports."""

import argparse
import hashlib
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUEST_FILE = "SCAN_REQUEST.json"
SOURCE_FILES = (
    "forex_scanner.py", "requirements.txt", ".github/workflows/forex-scanner.yml",
    "scripts/forex_scan_schedule.py", "tests/unit/test_forex_scan_schedule.py",
    "tests/unit/test_forex_scanner_reliability.py",
)


def read_json(path):
    try:
        value = Path(path).read_text(encoding="utf-8")
        result = json.loads(value)
        return result if isinstance(result, dict) else {}
    except (OSError, ValueError):
        return {}


def source_digest(root=ROOT):
    digest = hashlib.sha256()
    for name in SOURCE_FILES:
        digest.update(name.encode("utf-8") + b"\0")
        digest.update((root / name).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def decide_scan(event_name, request, health, report, source_sha256, now):
    """Return whether this event needs a scan, using UTC hour boundaries."""
    if event_name == "workflow_dispatch":
        return True, "Manual scan requested"
    if event_name == "push" and request.get("force") is True:
        return True, "Explicit recovery scan requested"
    # Actions push payloads can omit changed paths. Compare the actual sources
    # instead, including when an older queued event checks out a newer main.
    if health.get("source_sha256") != source_sha256:
        return True, "Scanner code or configuration changed, or not yet recorded"

    try:
        completed_at = datetime.fromisoformat(health["completed_at"].replace("Z", "+00:00"))
        if completed_at.tzinfo is None or health.get("status") != "completed":
            raise ValueError("No trustworthy completion time")
        completed_at = completed_at.astimezone(timezone.utc)
    except (KeyError, TypeError, ValueError, AttributeError):
        return True, "No successful scan record"

    if not report or health.get("report_sha256") != hashlib.sha256(report).hexdigest():
        return True, "Published report does not match the successful scan record"

    now = now.astimezone(timezone.utc)
    if completed_at > now + timedelta(minutes=2):
        return True, "Successful scan record has a future timestamp"
    current_hour = now.replace(minute=0, second=0, microsecond=0)
    if completed_at < current_hour:
        return True, "No successful scan in the current hour"
    return False, "A successful scan is already published for the current hour"


def record_success(state_path, report_path, now, source_sha256):
    # Called only after the scanner exits successfully. Health and report are
    # then committed together; a failed publish cannot advance remote health.
    report = report_path.read_bytes()
    if not report:
        raise ValueError("Cannot record success for an empty report")
    health = {
        "schema_version": 1,
        "status": "completed",
        "completed_at": now.astimezone(timezone.utc).isoformat(),
        "run_id": os.getenv("GITHUB_RUN_ID"),
        "trigger": os.getenv("GITHUB_EVENT_NAME"),
        "report_sha256": hashlib.sha256(report).hexdigest(),
        "source_sha256": source_sha256,
    }
    state_path.write_text(json.dumps(health, indent=2) + "\n", encoding="utf-8")
    return health


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record-success", action="store_true")
    parser.add_argument("--state-file", type=Path, default=ROOT / "FOREX_SCAN_HEALTH.json")
    parser.add_argument("--report-file", type=Path, default=ROOT / "LATEST_FOREX_SCAN.md")
    parser.add_argument("--request-file", type=Path, default=ROOT / REQUEST_FILE)
    args = parser.parse_args()
    now = datetime.now(timezone.utc)
    source_sha256 = source_digest()
    if args.record_success:
        health = record_success(args.state_file, args.report_file, now, source_sha256)
        print(f"Recorded successful scan: {health['completed_at']}")
        return

    report = args.report_file.read_bytes() if args.report_file.exists() else b""
    should_run, reason = decide_scan(
        os.getenv("GITHUB_EVENT_NAME", "workflow_dispatch"),
        read_json(args.request_file), read_json(args.state_file), report, source_sha256, now,
    )
    if output_path := os.getenv("GITHUB_OUTPUT"):
        with open(output_path, "a", encoding="utf-8") as output:
            output.write(f"should_run={str(should_run).lower()}\n")
    print(f"{'RUN' if should_run else 'SKIP'}: {reason}")


if __name__ == "__main__":
    main()
