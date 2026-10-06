from jobs.scheduler import get_scheduler_interval_hours


def test_scheduler_interval_defaults_to_one_hour():
    assert get_scheduler_interval_hours() == 1


def test_scheduler_interval_reads_env_override(monkeypatch):
    monkeypatch.setenv("SCHEDULER_INTERVAL_HOURS", "2")
    assert get_scheduler_interval_hours() == 2
