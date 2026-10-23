from streamstats.errors import StreamStatsError
from streamstats.parsers import jsonl_parse
from streamstats.parsers import csv_parse
from datetime import datetime


def analyse_file(file_path: str, format:str, files: int, skip_invalid: bool = False) -> dict:
    if format != "jsonl" and format != "csv":
        raise StreamStatsError("Unsupported format. Use CSV or JSONL")
    result = {
        "event_count": 0,
        "levels": {
            "DEBUG": 0,
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0,
        },
        "source_event_counts": {},
        "skipped_lines": 0,
    }
    if format == "jsonl":
        for log, sl in jsonl_parse(file_path, files, skip_invalid):
            result["event_count"] += 1
            result["levels"][log.level] += 1



            if log.source in result["source_event_counts"]:
                result["source_event_counts"][log.source]["all"] += 1
                result["source_event_counts"][log.source][log.level] += 1
            else:
                result["source_event_counts"][log.source] = {
                    "all": 1,
                    "DEBUG": 0,
                    "INFO": 0,
                    "WARNING": 0,
                    "ERROR": 0,
                    "CRITICAL": 0,
                }
                result["source_event_counts"][log.source][log.level] += 1
            if "first_timestamp" in result:
                if int(datetime.fromisoformat(result["first_timestamp"]).timestamp()) > int(log.timestamp.timestamp()):
                    result["first_timestamp"] = log.timestamp.isoformat()
            else:
                result["first_timestamp"] = log.timestamp.isoformat()
            if "last_timestamp" in result:
                if int(datetime.fromisoformat(result["last_timestamp"]).timestamp()) > int(log.timestamp.timestamp()):
                    result["last_timestamp"] = log.timestamp.isoformat()
            else:
                result["last_timestamp"] = log.timestamp.isoformat()
            result["skipped_lines"] = sl
    elif format == "csv":
        for log, sl in csv_parse(file_path, files, skip_invalid):
            result["event_count"] += 1
            result["levels"][log.level] += 1
            if log.source in result["source_event_counts"]:
                result["source_event_counts"][log.source]["all"] += 1
                result["source_event_counts"][log.source][log.level] += 1
            else:
                result["source_event_counts"][log.source] = {
                    "all": 1,
                    "DEBUG": 0,
                    "INFO": 0,
                    "WARNING": 0,
                    "ERROR": 0,
                    "CRITICAL": 0,
                }
                result["source_event_counts"][log.source][log.level] += 1
            if "first_timestamp" in result:
                if int(datetime.fromisoformat(result["first_timestamp"]).timestamp()) > int(log.timestamp.timestamp()):
                    result["first_timestamp"] = log.timestamp.isoformat()
            else:
                result["first_timestamp"] = log.timestamp.isoformat()
            if "last_timestamp" in result:
                if int(datetime.fromisoformat(result["last_timestamp"]).timestamp()) > int(log.timestamp.timestamp()):
                    result["last_timestamp"] = log.timestamp.isoformat()
            else:
                result["last_timestamp"] = log.timestamp.isoformat()
            result["skipped_lines"] = sl
    return result