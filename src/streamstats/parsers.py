import json
from streamstats.models import LoggingEntry
from streamstats.errors import StreamStatsError
import logging
import sys


def csv_parse(file_path: str, files: int, skip_invalid: bool = False) -> LoggingEntry:
    with open(file_path, encoding='utf-8') as opened_file:
        colums = opened_file.readline().split(",")
        line_count = 2
        skipped_lines = 0
        if not (colums[0] == "timestamp" and colums[1] == "level" and colums[2] == "source" and colums[3].strip() == "message"):
            raise StreamStatsError("Wrong file")

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
            skipped = False
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
                            if not skip_invalid:
                                logging.warning(f"Wrong event. File: {files}, string: {line_count}")
                                sys.exit(2)
                            else:
                                logging.warning("Wrong event")
                                skipped_lines += 1
                    f_str = opened_file.read(1)
                else:
                    while f_str != ',' and f_str != "":
                        elements[i] += f_str
                        f_str = opened_file.read(1)
                        if f_str == "\n":
                            if not skip_invalid:
                                logging.warning(f"Wrong event. File: {files}, string: {line_count}")
                                sys.exit(2)
                            else:
                                logging.warning("Wrong event")
                                skipped_lines += 1
                                skipped = True
                                break
                        if f_str == "":
                            if not skip_invalid:
                                logging.warning(f"Wrong event. File: {files}, string: {line_count}")
                                sys.exit(2)
                            else:
                                logging.warning("Wrong event")
                                skipped_lines += 1
                if f_str == "":
                    if not skip_invalid:
                        logging.warning(f"Wrong event. File: {files}, string: {line_count}")
                        sys.exit(2)
                    else:
                        logging.warning("Wrong event")
                        skipped_lines += 1
            if skipped:
                continue
            f_str = opened_file.read(1)
            if f_str == '"':
                f_str = opened_file.read(1)
                while f_str != '"':
                    elements[3] += f_str
                    f_str = opened_file.read(1)
                    if f_str == "\n":
                        f_str = " "
                    if f_str == "":
                        if not skip_invalid:
                            logging.warning(f"Wrong event. File: {files}, string: {line_count}")
                            sys.exit(2)
                        else:
                            logging.warning("Wrong event")
                            skipped_lines += 1
                f_str = opened_file.read(1)
            else:
                while f_str != '\n' and f_str != "":
                    elements[3] += f_str
                    f_str = opened_file.read(1)
            try:
                log = LoggingEntry(timestamp=elements[0], level=elements[1], source=elements[2], message=elements[3])
            except:
                if not skip_invalid:
                    logging.warning(f"Wrong event. File: {files}, string: {line_count}")
                    sys.exit(2)
                else:
                    logging.warning("Wrong event")
                    skipped_lines += 1
            timestamp = int(log.timestamp.timestamp())
            if timestamp < latest_timestamp:
                if not skip_invalid:
                    logging.warning(f"Wrong timestamp. File: {files}, string: {line_count}")
                    sys.exit(2)
                else:
                    logging.warning("Wrong timestamp")
                    skipped_lines += 1
            latest_timestamp = timestamp
            line_count += 1
            yield log, skipped_lines


def jsonl_parse(file_path: str, files: int, skip_invalid: bool = False) -> LoggingEntry:
    with open(file_path, encoding="utf-8") as opened_file:
        f_str = opened_file.readline()
        skipped_lines = 0
        line_count = 1
        latest_timestamp = 0
        while f_str != "":
            f_str = f_str.strip()
            if f_str == "":
                f_str = opened_file.readline()
                continue
            try:
                f_str_json = json.loads(f_str)
            except:
                if not skip_invalid:
                    logging.warning(f"Wrong event. File: {files}, string: {line_count}")
                    sys.exit(2)
                else:
                    logging.warning("Wrong event")
                    skipped_lines += 1
                    f_str = opened_file.readline()
                    continue
            try:
                log = LoggingEntry(timestamp=f_str_json["timestamp"], level=f_str_json["level"], source=f_str_json["source"], message=f_str_json["message"])
            except:
                if not skip_invalid:
                    logging.warning(f"Wrong event. File: {files}, string: {line_count}")
                    sys.exit(2)
                else:
                    logging.warning("Wrong event")
                    skipped_lines += 1
                    f_str = opened_file.readline()
                    continue
            timestamp = int(log.timestamp.timestamp())
            if timestamp < latest_timestamp:
                if not skip_invalid:
                    logging.warning(f"Wrong timestamp. File: {files}, string: {line_count}")
                    sys.exit(2)
                else:
                    logging.warning("Wrong timestamp")
                    skipped_lines += 1
                    f_str = opened_file.readline()
                    continue
            latest_timestamp = timestamp
            yield log, skipped_lines
            f_str = opened_file.readline()
            line_count += 1