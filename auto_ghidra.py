#!/usr/bin/env python
from os import path, system
from sys import stdin
from click import secho, command, argument, Path
from subprocess import check_output
from select import select

# This script was written by liba2k <3 (https://gist.github.com/liba2k/d522b4f20632c4581af728b286028f8f)
# The only thing I've changed is the path + delay, just added here to reduce the regular requests I get for it xD
# Personally, I set a shortcut alias for this in .bash_aliases, like:
# alias ghidra_auto='python3 /home/crystal/apps/auto_ghidra.py'

GHIDRA_PATH = '/opt/ghidra/'  # Set to your ghidra_path

def shouldRun():
    secho('Will run analysis in 1 second, press any key to cancel', fg='green')
    i, o, e = select([stdin], [], [], 1)

    if (i):
        return False
    else:
        return True


@command()
@argument('filename', type=Path(exists=True))
def main(filename):
    if path.isdir(filename):
        return system(f'{GHIDRA_PATH}ghidraRun')
    if '.gpr' in filename:
        system(f'{GHIDRA_PATH}ghidraRun "{path.abspath(filename)}"')
        return
    else:
        out_dir = f'{path.dirname(filename)}'
        out_dir = out_dir if out_dir != '' else './'
    file_output = check_output(f'file "{filename}"', shell=True).decode('utf8')
    secho(file_output, fg='yellow')
    r = shouldRun()
    if r:
        system(f'{GHIDRA_PATH}support/analyzeHeadless {out_dir} "{filename}" -import "{filename}"')
        system(f'{GHIDRA_PATH}ghidraRun "{path.abspath(filename)}.gpr"')


if __name__ == '__main__':
    main()
