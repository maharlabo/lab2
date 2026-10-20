import sys
import json
from models import LoggingEntry

def json_parse(file_path: str) -> LoggingEntry:
    with open(file_path) as opened_file:
        f_str = opened_file.read(1)
        while f_str != "[":
            f_str = opened_file.read(1)
        while f_str != "":
            while f_str != "{" and f_str != "]" and f_str != "":
                f_str = opened_file.read(1)
            if f_str == "{":
                while f_str[-1] != "}" and f_str[-1] != "":
                    if f_str[-1] == '"':
                        f_str += opened_file.read(1)
                        while f_str[-1] != '"':
                            f_str += opened_file.read(1)
                    if f_str[-1] == "'":
                        f_str += opened_file.read(1)
                        while f_str[-1] != "'":
                            f_str += opened_file.read(1)
                    f_str += opened_file.read(1)
                if f_str == "":
                    sys.stderr.write("Error: Wrong format")
                    sys.exit(2)
                f_str_json = {}
                try:
                    f_str_json = json.loads(f_str)
                except:
                    sys.stderr.write("Error: Wrong format")
                    sys.exit(2)

                if not ("timestamp" in f_str_json and "level" in f_str_json and "source" in f_str_json and "message" in f_str_json):
                    sys.stderr.write("Error: Wrong format")
                    sys.exit(2)
                while f_str != "," and f_str != "]" and f_str != "":
                    f_str = opened_file.read(1)
                if f_str == "":
                    sys.stderr.write("Error: Wrong format")
                    sys.exit(2)
                log = LoggingEntry(timestamp=f_str_json["timestamp"], level=f_str_json["level"], source=f_str_json["source"], message=f_str_json["message"])
                yield log
                f_str = opened_file.read(1)
            elif f_str == "":
                sys.stderr.write("Error: Wrong format")
                sys.exit(2)


def csv_parse(file_path: str) -> LoggingEntry:
    with open(file_path) as opened_file:
        colums = opened_file.readline().split(",")
        if not (colums[0] == "timestamp" and colums[1] == "level" and colums[2] == "source" and colums[3].strip() == "message"):
            sys.stderr.write("Error: Wrong format")
            sys.exit(2)

        f_str = "_"
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
                        if f_str == "":
                            sys.stderr.write("Error: Wrong format")
                            sys.exit(2)
                    f_str = opened_file.read(1)
                else:
                    while f_str != ',' and f_str != "":
                        elements[i] += f_str
                        f_str = opened_file.read(1)
                        if f_str == "":
                            sys.stderr.write("Error: Wrong format")
                            sys.exit(2)
                if f_str == "":
                    sys.stderr.write("Error: Wrong format")
                    sys.exit(2)
            if f_str == '"':
                f_str = opened_file.read(1)
                while f_str != '"':
                    elements[3] += f_str
                    f_str = opened_file.read(1)
                    if f_str == "":
                        sys.stderr.write("Error: Wrong format")
                        sys.exit(2)
                f_str = opened_file.read(1)
            else:
                f_str = opened_file.read(1)
                while f_str != '\n' and f_str != "":
                    elements[3] += f_str
                    f_str = opened_file.read(1)
            log = LoggingEntry(timestamp=elements[0], level=elements[1], source=elements[2], message=elements[3])
            yield log