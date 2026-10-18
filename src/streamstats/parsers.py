from io import TextIOWrapper
import sys
import json
from models import LoggingEntry

def json_parse_element(opened_file: TextIOWrapper) -> LoggingEntry:
    f_str = opened_file.read(1)
    while f_str.strip() == "{" and f_str != "":
        f_str = opened_file.read(1)
    if f_str != "{":
        sys.stderr.write("Error: Wrong format")
        sys.exit(2)
    while f_str[-1] != "}" and f_str != "":
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

    if not( "timestamp" in f_str_json and "level" in f_str_json and "source" in f_str_json and "message" in f_str_json):
        sys.stderr.write("Error: Wrong format")
        sys.exit(2)
    log = LoggingEntry(timestamp=f_str_json["timestamp"], level=f_str_json["level"], source=f_str_json["source"], message=f_str_json["message"])
    return log