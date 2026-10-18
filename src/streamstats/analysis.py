import sys

def analyse_file(file_path: str):
    with open(file_path, "r") as f:
        f_str = f.read(1)
        while f_str != "[" and f_str != "t" and f_str != "":
            f_str = f.read(1)
        if f_str == "":
            sys.stderr.write("Error: Wrong format")
            sys.exit(2)
        if f_str == "[":
            f.seek(-1, 1)