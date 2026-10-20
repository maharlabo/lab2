import sys
from errors import StreamStatsError

def analyse_file(file_path: str):
    if file_path[-4:].lower() != "json" and file_path[-3:].lower() != "csv":
        raise StreamStatsError("Unsupported format")