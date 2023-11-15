#!/usr/bin/env python3
from os import getenv
from sys import exit
from argparse import ArgumentParser
from pathlib import Path
from urllib.request import urlopen
from shutil import copyfileobj

def die(msg):
    exit(f"[!] - {msg}")

def get_srcs(filename, path):
    if not Path(filename).is_file():
        die(f"File {filename} not found")
    with open(filename, "r") as f:
        urls = [x.rstrip() for x in f.readlines()]
    
    path.mkdir(parents=True, exist_ok=True)

    for url in urls:
        with urlopen(url) as dl, open(f"{path}/{url.split('/')[-1]}", 'wb') as out:
            copyfileobj(dl, out)


class FIDBIMPORTER:
    def __init__(self, args):
        self.file = args.file
        self.lib_folder = Path("libs/")
        self.src_folder = Path("srcs/")
    
    def importer(self):
        self.lib_folder.mkdir(parents=True, exist_ok=True)
        self.src_folder.mkdir(parents=True, exist_ok=True)

        if self.file.endswith('.txt'):
            _path = self.src_folder / ".".join(self.file.split(".")[:-1])
        else:
            _path = self.src_folder / self.file

        get_srcs(self.file, _path)


def get_args():
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', action='store', required=True, help='library URLs to load')
    return parser.parse_args()

def main():
    print("[*] - Starting FIDB importer...")
    if not getenv('GHIDRA_HOME') or not getenv('GHIDRA_PROJ'):
        die("GHIDRA_HOME or GHIDRA_PROJ environment variables not set")
    
    fidbimporter = FIDBIMPORTER(get_args())
    fidbimporter.importer()
    print("[*] - FIDB importer complete!")

if __name__ == "__main__":
    main()
