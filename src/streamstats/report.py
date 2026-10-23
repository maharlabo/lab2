from streamstats.analysis import analyse_file
import json
from datetime import datetime
from streamstats.errors import StreamStatsError
import os


def make_report(file_path: str, format: str, output: str = "report.json", *, skip_invalid: bool = False):
    if format != "csv" and format != "jsonl" and format != "csv|jsonl":
        raise StreamStatsError("Wrong Format")
    if format != file_path[-len(format):]:
        raise StreamStatsError("Wrong Format")
    analysed_file = analyse_file(file_path, format)
    if os.path.isfile(output):
        with open(output, "r") as f:
            json_report = json.loads(f.read())
    else:
        json_report = {
            "event_count": 0,
            "levels": {
                "DEBUG": 0,
                "INFO": 0,
                "WARNING": 0,
                "ERROR": 0,
                "CRITICAL": 0
            },
            "source_event_counts": {}
        }
    json_report["event_count"] += analysed_file["event_count"]
    for l in json_report["levels"]:
        json_report["levels"][l] += analysed_file["levels"][l]
    for source in analysed_file["source_event_counts"]:
        if source in json_report["source_event_counts"]:
            for l in json_report["source_event_counts"][source]:
                json_report["source_event_counts"][source][l] += analysed_file["source_event_counts"][source][l]
        else:
            json_report["source_event_counts"][source] = analysed_file["source_event_counts"][source]
    if not "first_timestamp" in json_report:
        json_report["first_timestamp"] = analysed_file["first_timestamp"]
    else:
        if int(datetime.fromisoformat(json_report["first_timestamp"]).timestamp()) > int(datetime.fromisoformat(analysed_file["first_timestamp"]).timestamp()):
            json_report["first_timestamp"] = analysed_file["first_timestamp"]
    if not "last_timestamp" in json_report:
        json_report["last_timestamp"] = analysed_file["last_timestamp"]
    else:
        if int(datetime.fromisoformat(json_report["last_timestamp"]).timestamp()) < int(datetime.fromisoformat(analysed_file["last_timestamp"]).timestamp()):
            json_report["last_timestamp"] = analysed_file["last_timestamp"]
    top_errors = sorted([source for source in json_report["source_event_counts"]], key=lambda x: json_report["source_event_counts"][x]["ERROR"]+json_report["source_event_counts"][x]["CRITICAL"])
    json_report["top_errors"] = top_errors[:5]

    with open(output, "w") as f:
        f.write(json.dumps(json_report))