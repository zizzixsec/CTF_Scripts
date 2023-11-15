#!/usr/bin/env python3
from os import getenv
from sys import exit
from argparse import ArgumentParser
from pathlib import Path
from urllib.request import urlopen
from shutil import copyfileobj

def die(msg):
    exit(f"[!] - {msg}")

def get_batch_urls(filename):
    path = Path(filename)
    if not path.is_file():
        die(f"File {filename} not found")
    with open(filename, "r") as f:
        return [x.rstrip() for x in f.readlines()]

def download_from_url(url, path):
    with urlopen(url) as r, open(f"srcs/{url.split('/')[-1]}", 'wb') as out:
        copyfileobj(r, out)


class FIDBIMPORTER:
    def __init__(self, args):
        self.args = args
        self.lib_folder = Path("libs/").mkdir(parents=True, exist_ok=True)
        self.src_folder = Path("srcs/").mkdir(parents=True, exist_ok=True)
    
    def importer(self):
        if self.args.url:
            download_from_url(self.args.url, self.src_folder)
        elif self.args.file:
            [download_from_url(url, self.src_folder) for url in get_batch_urls(self.args.file)]


def get_args():
    parser = ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url', action='store', help='library URL to load')
    group.add_argument('-f', '--file', action='store', help='library URLs to load(Batch)')

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
