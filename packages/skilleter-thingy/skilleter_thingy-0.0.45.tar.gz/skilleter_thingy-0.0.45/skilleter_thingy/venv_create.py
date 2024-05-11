#!/usr/bin/env python3

import os
import stat
import argparse

import thingy.bash_venv as bash_venv
import thingy.fish_venv as fish_venv

################################################################################

def main():
    """Create the venv script and make it executable"""

    parser = argparse.ArgumentParser(description='Create a script to run Python code in a virtual environment')
    parser.add_argument('name', nargs=1, help='Name of the script to create')

    args = parser.parse_args()

    shell = os.getenv('SHELL').split('/')[-1]

    if shell == 'fish':
        template = fish_venv.TEMPLATE
    else:
        if shell != 'bash':
            print(f'Warning: Unknown shell: {shell} - using Bash template by default')

        template = bash_venv.TEMPLATE

    with open(args.name[0], 'wt') as scriptfile:
        scriptfile.write(template)

    statinfo = os.stat(args.name[0])

    os.chmod(args.name[0], statinfo.st_mode|stat.S_IXUSR|stat.S_IXGRP|stat.S_IXOTH)

    print(f'Created virtual environment: {args.name[0]}')

################################################################################

def venv_create():
    """Entry point"""

    try:
        main()

    except KeyboardInterrupt:
        sys.exit(1)
    except BrokenPipeError:
        sys.exit(2)

################################################################################

if __name__ == '__main__':
    venv_create()
