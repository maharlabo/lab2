from errors import StreamStatsError
from parsers import jsonl_parse
from parsers import csv_parse


def analyse_file(file_path: str) -> dict:
    if file_path[-5:].lower() != "jsonl" and file_path[-3:].lower() != "csv":
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
    }
    if file_path[-5:].lower() == "jsonl":
        for log in jsonl_parse(file_path):
            result["event_count"] += 1
            result["levels"][log.level] += 1
            if log.source in result["source_event_counts"]:
                result["source_event_counts"][log.source] += 1
            else:
                result["source_event_counts"][log.source] = 1
            if "first_timestamp" in result:
                if int(result["first_timestamp"].timestamp()) > int(log.timestamp.timestamp()):
                    result["first_timestamp"] = log.timestamp
            else:
                result["first_timestamp"] = log.timestamp
            if "last_timestamp" in result:
                if int(result["last_timestamp"].timestamp()) > int(log.timestamp.timestamp()):
                    result["last_timestamp"] = log.timestamp
            else:
                result["first_timestamp"] = log.timestamp
    elif file_path[-3:] == "csv":
        for log in csv_parse(file_path):
            result["event_count"] += 1
            result["levels"][log.level] += 1
            if log.source in result["source_event_counts"]:
                result["source_event_counts"][log.source] += 1
            else:
                result["source_event_counts"][log.source] = 1
            if "first_timestamp" in result:
                if int(result["first_timestamp"].timestamp()) > int(log.timestamp.timestamp()):
                    result["first_timestamp"] = log.timestamp
            else:
                result["first_timestamp"] = log.timestamp
            if "last_timestamp" in result:
                if int(result["last_timestamp"].timestamp()) > int(log.timestamp.timestamp()):
                    result["last_timestamp"] = log.timestamp
            else:
                result["first_timestamp"] = log.timestamp
    return result