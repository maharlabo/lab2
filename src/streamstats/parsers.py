import json
from models import LoggingEntry
from errors import StreamStatsError


def csv_parse(file_path: str, skip_invalid: bool = False) -> LoggingEntry:
    with open(file_path) as opened_file:
        colums = opened_file.readline().split(",")
        if not (colums[0] == "timestamp" and colums[1] == "level" and colums[2] == "source" and colums[3].strip() == "message"):
            raise StreamStatsError("Wrong event")

        f_str = "_"
        latest_timestamp = 0
        while f_str != "":
            while (f_str == " " or f_str == "\n") and f_str != "":
                f_str = opened_file.read(1)
            if f_str == "":
                break
            else:
                opened_file.seek(opened_file.tell()-1)
            elements = ["", "", "", ""]
            for i in range(3):
                f_str = opened_file.read(1)
                while (f_str == " " or f_str == "\n") and f_str != "":
                    f_str = opened_file.read(1)
                if f_str == '"':
                    f_str = opened_file.read(1)
                    while f_str != '"' and f_str != "":
                        elements[i] += f_str
                        f_str = opened_file.read(1)
                        if f_str == "\n":
                            f_str = " "
                        if f_str == "":
                            raise StreamStatsError("Wrong event")
                    f_str = opened_file.read(1)
                else:
                    while f_str != ',' and f_str != "":
                        elements[i] += f_str
                        f_str = opened_file.read(1)
                        if f_str == "":
                            raise StreamStatsError("Wrong event")
                if f_str == "":
                    raise StreamStatsError("Wrong event")
            if f_str == '"':
                f_str = opened_file.read(1)
                while f_str != '"':
                    elements[3] += f_str
                    f_str = opened_file.read(1)
                    if f_str == "\n":
                        f_str = " "
                    if f_str == "":
                        raise StreamStatsError("Wrong event")
                f_str = opened_file.read(1)
            else:
                f_str = opened_file.read(1)
                while f_str != '\n' and f_str != "":
                    elements[3] += f_str
                    f_str = opened_file.read(1)
            try:
                log = LoggingEntry(timestamp=elements[0], level=elements[1], source=elements[2], message=elements[3])
            except:
                if not skip_invalid:
                    raise StreamStatsError("Wrong event")
            timestamp = int(log.timestamp.timestamp())
            if timestamp < latest_timestamp:
                raise StreamStatsError("Wrong timestamp")
            latest_timestamp = timestamp
            yield log


def jsonl_parse(file_path: str, skip_invalid: bool = False) -> LoggingEntry:
    with open(file_path) as opened_file:
        f_str = opened_file.readline()
        while f_str != "":
            f_str = f_str.strip()
            if f_str == "":
                f_str = opened_file.readline()
                continue
            try:
                f_str_json = json.loads(f_str)
            except:
                if skip_invalid:
                    continue
                raise StreamStatsError("Wrong event")
            try:
                log = LoggingEntry(timestamp=f_str_json["timestamp"], level=f_str_json["level"], source=f_str_json["source"], message=f_str_json["message"])
            except:
                if skip_invalid:
                    continue
                raise StreamStatsError("Wrong event")
            yield log
            f_str = opened_file.readline()