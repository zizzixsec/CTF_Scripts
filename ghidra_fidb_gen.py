#!/usr/bin/env python3
from os import getenv
from sys import exit
from argparse import ArgumentParser
from pathlib import Path
from urllib.request import urlopen
from shutil import copyfileobj
from re import compile
from tempfile import TemporaryDirectory

def die(msg):
    exit(f"[!] - {msg}")


class FIDBIMPORTER:
    def __init__(self, args):
        self.file = args.file
        self.distro = args.dist
        self.lib_folder = Path("libs/")
        self.src_folder = Path("srcs/")

    def get_srcs(self, path):
        if not Path(self.file).is_file():
            die(f"File {self.file} not found")
        with open(self.file, "r") as f:
            urls = [x.rstrip() for x in f.readlines()]
        
        path.mkdir(parents=True, exist_ok=True)

        for url in urls:
            fn = path / url.split('/')[-1]
            if not fn.is_file():
                with urlopen(url) as r, open(fn, 'wb') as f:
                    copyfileobj(r, f)

    def extract_debs(self, path, dist):
        name_pattern = compile(r'^([^_]+)_([^_]+)-([^_]+)_(.+)\.deb$')
        for debfile in path.iterdir():
            pkg = debfile.name.split('/')[-1]
            m = name_pattern.match(pkg)
            name = m.group(1)
            version = m.group(2)
            release = f"{m.group(3)}_{m.group(4)}"
            
            dest = self.lib_folder / dist / name / version / release
            dest.mkdir(parents=True, exist_ok=True)

            with TemporaryDirectory() as tmpdir:
                print(f'created tempdir: {tmpdir}')
                print(debfile.absolute())
            

    def importer(self):
        self.lib_folder.mkdir(parents=True, exist_ok=True)
        self.src_folder.mkdir(parents=True, exist_ok=True)

        if self.file.endswith('.txt'):
            _path = self.src_folder / ".".join(self.file.split(".")[:-1])
        else:
            _path = self.src_folder / self.file

        self.get_srcs(_path)
        self.extract_debs(_path, self.distro)


def get_args():
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', action='store', required=True, help='library URLs to load')
    parser.add_argument('-d', '--dist', action='store', required=True, help='Distro libraries are from')
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
