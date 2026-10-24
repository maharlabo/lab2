import pytest
from typer.testing import CliRunner
from streamstats.__main__ import analyze
from streamstats.__main__ import app
import json

from streamstats.errors import StreamStatsError


def test_default_jsonl(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    file = tmp_path / "logs.jsonl"
    report = tmp_path / "REPORT.JSON"
    file.write_text("""{\"timestamp\": \"2026-10-13T12:00:00Z\", \"level\": \"DEBUG\", \"source\": \"auth.service\", \"message\": \"Starting authentication request.\"}
{\"timestamp\": \"2026-10-13T12:00:01Z\", \"level\": \"INFO\", \"source\": \"auth.service\", \"message\": \"User authentication completed successfully.\"}
{\"timestamp\": \"2026-10-13T12:00:02Z\", \"level\": \"WARNING\", \"source\": \"cache.worker\", \"message\": \"Cache response time exceeded the expected threshold.\"}
{\"timestamp\": \"2026-10-13T12:00:03Z\", \"level\": \"ERROR\", \"source\": \"database.client\", \"message\": \"Database query failed due to a connection timeout.\"}
{\"timestamp\": \"2026-10-13T12:00:04Z\", \"level\": \"CRITICAL\", \"source\": \"system.monitor\", \"message\": \"Service is unavailable after repeated health-check failures.\"}
{\"timestamp\": \"2026-10-13T12:00:05Z\", \"level\": \"INFO\", \"source\": \"file.reader\", \"message\": \"Log file was read successfully.\"}
{\"timestamp\": \"2026-10-13T12:00:06Z\", \"level\": \"DEBUG\", \"source\": \"parser\", \"message\": \"Parsed 128 log records.\"}
{\"timestamp\": \"2026-10-13T12:00:07Z\", \"level\": \"WARNING\", \"source\": \"disk.monitor\", \"message\": \"Available disk space is below 15 percent.\"}
{\"timestamp\": \"2026-10-13T12:00:08Z\", \"level\": \"ERROR\", \"source\": \"api.gateway\", \"message\": \"Upstream service returned HTTP 502.\"}
{\"timestamp\": \"2026-10-13T12:00:09Z\", \"level\": \"INFO\", \"source\": \"scheduler\", \"message\": \"Scheduled cleanup task completed.\"}""")
    result = runner.invoke(app, ["analyze", str(file), "--format", "jsonl", "--output", str(report)])
    assert report.read_text() == '{"files": 1, "event_count": 10, "skipped_lines": 0, "levels": {"DEBUG": 2, "INFO": 3, "WARNING": 2, "ERROR": 2, "CRITICAL": 1}, "source_event_counts": {"auth.service": {"all": 2, "DEBUG": 1, "INFO": 1, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}, "cache.worker": {"all": 1, "DEBUG": 0, "INFO": 0, "WARNING": 1, "ERROR": 0, "CRITICAL": 0}, "database.client": {"all": 1, "DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 1, "CRITICAL": 0}, "system.monitor": {"all": 1, "DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 1}, "file.reader": {"all": 1, "DEBUG": 0, "INFO": 1, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}, "parser": {"all": 1, "DEBUG": 1, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}, "disk.monitor": {"all": 1, "DEBUG": 0, "INFO": 0, "WARNING": 1, "ERROR": 0, "CRITICAL": 0}, "api.gateway": {"all": 1, "DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 1, "CRITICAL": 0}, "scheduler": {"all": 1, "DEBUG": 0, "INFO": 1, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}}, "first_timestamp": "2026-10-13T12:00:00+00:00", "last_timestamp": "2026-10-13T12:00:00+00:00", "top_errors": ["auth.service", "cache.worker", "file.reader", "parser", "disk.monitor"]}'

def test_default_csv(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    file = tmp_path / "logs.csv"
    report = tmp_path / "REPORT.JSON"
    file.write_text("""timestamp,level,source,message
2026-10-13T12:00:00Z,DEBUG,auth.service,Starting authentication request.
2026-10-13T12:00:01Z,INFO,auth.service,User authentication completed successfully.
2026-10-13T12:00:02Z,WARNING,cache.worker,Cache response time exceeded the expected threshold.
2026-10-13T12:00:03Z,ERROR,database.client,Database query failed due to a connection timeout.
2026-10-13T12:00:04Z,CRITICAL,system.monitor,Service is unavailable after repeated health-check failures.
2026-10-13T12:00:05Z,INFO,file.reader,Log file was read successfully.
2026-10-13T12:00:06Z,DEBUG,parser,Parsed 128 log records.
2026-10-13T12:00:07Z,WARNING,disk.monitor,Available disk space is below 15 percent.
2026-10-13T12:00:08Z,ERROR,api.gateway,Upstream service returned HTTP 502.
2026-10-13T12:00:09Z,INFO,scheduler,Scheduled cleanup task completed.""")
    result = runner.invoke(app, ["analyze", str(file), "--format", "csv", "--output", str(report)])
    assert report.read_text() == '{"files": 1, "event_count": 10, "skipped_lines": 0, "levels": {"DEBUG": 2, "INFO": 3, "WARNING": 2, "ERROR": 2, "CRITICAL": 1}, "source_event_counts": {"auth.service": {"all": 2, "DEBUG": 1, "INFO": 1, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}, "cache.worker": {"all": 1, "DEBUG": 0, "INFO": 0, "WARNING": 1, "ERROR": 0, "CRITICAL": 0}, "database.client": {"all": 1, "DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 1, "CRITICAL": 0}, "system.monitor": {"all": 1, "DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 1}, "file.reader": {"all": 1, "DEBUG": 0, "INFO": 1, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}, "parser": {"all": 1, "DEBUG": 1, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}, "disk.monitor": {"all": 1, "DEBUG": 0, "INFO": 0, "WARNING": 1, "ERROR": 0, "CRITICAL": 0}, "api.gateway": {"all": 1, "DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 1, "CRITICAL": 0}, "scheduler": {"all": 1, "DEBUG": 0, "INFO": 1, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}}, "first_timestamp": "2026-10-13T12:00:00+00:00", "last_timestamp": "2026-10-13T12:00:00+00:00", "top_errors": ["auth.service", "cache.worker", "file.reader", "parser", "disk.monitor"]}'


def test_void_csv(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    file = tmp_path / "logs.csv"
    file.touch()
    report = tmp_path / "REPORT.JSON"
    with pytest.raises(StreamStatsError) as e:
        result = runner.invoke(app, ["analyze", str(file), "--format", "csv", "--output", str(report)], catch_exceptions=False)
    assert str(e.value) == "Wrong file"


def test_void_jsonl(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    file = tmp_path / "logs.jsonl"
    file.touch()
    report = tmp_path / "REPORT.JSON"
    with pytest.raises(StreamStatsError) as e:
        result = runner.invoke(app, ["analyze", str(file), "--format", "jsonl", "--output", str(report)], catch_exceptions=False)
    assert str(e.value) == "Wrong file"


def test_broken_jsonl(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    file = tmp_path / "logs.jsonl"
    report = tmp_path / "REPORT.JSON"
    file.write_text("""{\"timestamp\": \"2026-10-13T12:00:00Z\", \"level\": \"DEBUG\", \"source\": \"auth.service\", \"message\": \"Starting authentication request.\"}
{\"timestamp\": \"2026-10-13T12:00:01Z\", 
\"level\": \"INFO\", \"source\": \"auth.service\", \"message\": \"User authentication completed successfully.\"}""")

    result = runner.invoke(app, ["analyze", str(file), "--format", "jsonl", "--output", str(report)], catch_exceptions=False)
    assert result.exit_code == 2


def test_broken_csv(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    file = tmp_path / "logs.csv"
    report = tmp_path / "REPORT.JSON"
    file.write_text("""timestamp,level,source,message
2026-10-13T12:00:00Z,DEBUG,auth.service,Starting 
authentication request.
2026-10-13T12:00:01Z,INFO,auth.service,User authentication completed successfully.""")
    result = runner.invoke(app, ["analyze", str(file), "--format", "csv", "--output", str(report)], catch_exceptions=False)
    assert result.exit_code == 2


def test_broken_jsonl_skip_invalid(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    file = tmp_path / "logs.jsonl"
    report = tmp_path / "REPORT.JSON"
    file.write_text("""{\"timestamp\": \"2026-10-13T12:00:00Z\", \"level\": \"DEBUG\", \"source\": \"auth.service\", \"message\": \"Starting authentication request.\"}
{\"timestamp\": \"2026-10-13T12:00:01Z\", 
\"level\": \"INFO\", \"source\": \"auth.service\", \"message\": \"User authentication completed successfully.\"}""")

    result = runner.invoke(app, ["analyze", str(file), "--format", "jsonl", "--skip-invalid"], catch_exceptions=False)
    assert result.exit_code == 0


def test_broken_csv_skip_invalid(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    file = tmp_path / "logs.csv"
    report = tmp_path / "REPORT.JSON"
    file.write_text("""timestamp,level,source,message
2026-10-13T12:00:00Z,DEBUG,auth.service,Starting 
authentication request.
2026-10-13T12:00:01Z,INFO,auth.service,User authentication completed successfully.""")
    result = runner.invoke(app, ["analyze", str(file), "--format", "csv", "--skip-invalid"], catch_exceptions=False)
    assert result.exit_code == 0



def test_unicode_jsonl(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    file = tmp_path / "logs.jsonl"
    report = tmp_path / "REPORT.JSON"
    file.write_text("""{\"timestamp\": \"2026-10-13T12:00:00Z\", \"level\": \"DEBUG\", \"source\": \"auth.service\", \"message\": \"Starting authentication request.\"} 
    {\"timestamp\": \"2026-10-13T12:00:01Z\", \"level\": \"INFO\", \"source\": \"Сервер_аутентификации\", \"message\": \"Аутентификация прошла успешно\"}""", encoding="utf-8")

    result = runner.invoke(app, ["analyze", str(file), "--format", "jsonl", "--output", str(report)], catch_exceptions=False)
    assert result.exit_code == 0


def test_unicode_csv(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    file = tmp_path / "logs.csv"
    report = tmp_path / "REPORT.JSON"
    file.write_text("""timestamp,level,source,message
2026-10-13T12:00:00Z,DEBUG,auth.service,Starting authentication request.
2026-10-13T12:00:01Z,INFO,Сервер_аутентификации,Аутентификация прошла успешно""", encoding="utf-8")
    result = runner.invoke(app, ["analyze", str(file), "--format", "csv", "--output", str(report)], catch_exceptions=False)
    assert result.exit_code == 0


def test_several_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    file = tmp_path / "logs.jsonl"
    report = tmp_path / "REPORT.JSON"
    file.write_text("""{\"timestamp\": \"2026-10-13T12:00:00Z\", \"level\": \"DEBUG\", \"source\": \"auth.service\", \"message\": \"Starting authentication request.\"}
{\"timestamp\": \"2026-10-13T12:00:01Z\", \"level\": \"INFO\", \"source\": \"auth.service\", \"message\": \"User authentication completed successfully.\"}
{\"timestamp\": \"2026-10-13T12:00:02Z\", \"level\": \"WARNING\", \"source\": \"cache.worker\", \"message\": \"Cache response time exceeded the expected threshold.\"}
{\"timestamp\": \"2026-10-13T12:00:03Z\", \"level\": \"ERROR\", \"source\": \"database.client\", \"message\": \"Database query failed due to a connection timeout.\"}
{\"timestamp\": \"2026-10-13T12:00:04Z\", \"level\": \"CRITICAL\", \"source\": \"system.monitor\", \"message\": \"Service is unavailable after repeated health-check failures.\"}
{\"timestamp\": \"2026-10-13T12:00:05Z\", \"level\": \"INFO\", \"source\": \"file.reader\", \"message\": \"Log file was read successfully.\"}
{\"timestamp\": \"2026-10-13T12:00:06Z\", \"level\": \"DEBUG\", \"source\": \"parser\", \"message\": \"Parsed 128 log records.\"}
{\"timestamp\": \"2026-10-13T12:00:07Z\", \"level\": \"WARNING\", \"source\": \"disk.monitor\", \"message\": \"Available disk space is below 15 percent.\"}
{\"timestamp\": \"2026-10-13T12:00:08Z\", \"level\": \"ERROR\", \"source\": \"api.gateway\", \"message\": \"Upstream service returned HTTP 502.\"}
{\"timestamp\": \"2026-10-13T12:00:09Z\", \"level\": \"INFO\", \"source\": \"scheduler\", \"message\": \"Scheduled cleanup task completed.\"}""")
    result = runner.invoke(app, ["analyze", str(file), "--format", "jsonl", "--output", str(report)])
    file = tmp_path / "logs.csv"
    file.write_text("""timestamp,level,source,message
2026-10-13T12:00:00Z,DEBUG,auth.service,Starting authentication request.
2026-10-13T12:00:01Z,INFO,auth.service,User authentication completed successfully.
2026-10-13T12:00:02Z,WARNING,cache.worker,Cache response time exceeded the expected threshold.
2026-10-13T12:00:03Z,ERROR,database.client,Database query failed due to a connection timeout.
2026-10-13T12:00:04Z,CRITICAL,system.monitor,Service is unavailable after repeated health-check failures.
2026-10-13T12:00:05Z,INFO,file.reader,Log file was read successfully.
2026-10-13T12:00:06Z,DEBUG,parser,Parsed 128 log records.
2026-10-13T12:00:07Z,WARNING,disk.monitor,Available disk space is below 15 percent.
2026-10-13T12:00:08Z,ERROR,api.gateway,Upstream service returned HTTP 502.
2026-10-13T12:00:09Z,INFO,scheduler,Scheduled cleanup task completed.""")
    result = runner.invoke(app, ["analyze", str(file), "--format", "csv", "--output", str(report)])
    assert report.read_text() == '{"files": 2, "event_count": 20, "skipped_lines": 0, "levels": {"DEBUG": 4, "INFO": 6, "WARNING": 4, "ERROR": 4, "CRITICAL": 2}, "source_event_counts": {"auth.service": {"all": 4, "DEBUG": 2, "INFO": 2, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}, "cache.worker": {"all": 2, "DEBUG": 0, "INFO": 0, "WARNING": 2, "ERROR": 0, "CRITICAL": 0}, "database.client": {"all": 2, "DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 2, "CRITICAL": 0}, "system.monitor": {"all": 2, "DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 2}, "file.reader": {"all": 2, "DEBUG": 0, "INFO": 2, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}, "parser": {"all": 2, "DEBUG": 2, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}, "disk.monitor": {"all": 2, "DEBUG": 0, "INFO": 0, "WARNING": 2, "ERROR": 0, "CRITICAL": 0}, "api.gateway": {"all": 2, "DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 2, "CRITICAL": 0}, "scheduler": {"all": 2, "DEBUG": 0, "INFO": 2, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}}, "first_timestamp": "2026-10-13T12:00:00+00:00", "last_timestamp": "2026-10-13T12:00:00+00:00", "top_errors": ["auth.service", "cache.worker", "file.reader", "parser", "disk.monitor"]}'
