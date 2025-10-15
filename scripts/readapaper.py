#!/usr/bin/python

import os
import random
import json
import subprocess
from pathlib import Path


def main():
    dir = Path(os.path.realpath(__file__)).parent
    cachepath = Path.joinpath(dir, "cache.json")
    if cachepath.exists():
        with open(cachepath) as cachefile:
            cache = json.load(cachefile)
    else:
        cache = {}
    if "read" not in cache:
        cache["read"] = []
    if "reading" not in cache:
        cache["reading"] = ""

    if cache["reading"] == "":
        try:
            cache["reading"] = str(find_a_paper(dir.parent, cache))
        except FileNotFoundError as e:
            os.error(e)

    
    print(f"Reading: {cache["reading"]}")
    subprocess.run(["evince", cache["reading"]])

    finished = input("Did you finish this paper? (y/N): ")
    if (finished.strip() == 'y' or finished.strip() == 'Y'):
        cache["read"].append(str(cache["reading"]))
        cache["reading"] = ""
    else:
        skip = input("Do you want to skip this paper? (y/N): ")
        if (skip.strip() == 'y' or skip.strip() == 'Y'):
            print("Skipping this paper for now...")
            cache["reading"] = ""
        else:
            print("Saving your progress...")

    with open(cachepath, "w") as cachefile:
        json.dump(cache, cachefile)

        


def find_a_paper(dir: Path, cache: dict) -> Path:
    items = [item for item in dir.iterdir()]
    for _ in range(len(items)):
        selected = items[random.randint(0, len(items) - 1)]
        dirs = []
        if selected.is_dir():
            if selected in dirs:
                continue
            dirs.append(selected)
            try:
                return find_a_paper(selected, cache)
            except FileNotFoundError:
                continue
        if selected.is_file() and selected.suffix == ".pdf":
            if str(selected) not in cache["read"]:
                return selected

    raise FileNotFoundError("Couldn't find an unread paper to read")


main()
