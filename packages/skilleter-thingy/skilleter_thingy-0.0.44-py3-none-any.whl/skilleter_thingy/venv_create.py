#!/usr/bin/env python3

import os
import stat
import argparse

################################################################################

TEMPLATE = \
"""#!/usr/bin/env bash

set -e

################################################################################

VENV_NAME=$(basename "$0")
VENV_DIR=__venv__

GREEN="\e[42m"
NORMAL="\e[0m"

################################################################################

function box()
{
   echo -e "${GREEN}################################################################################${NORMAL}"
   echo -e "${GREEN}# $@${NORMAL}"
   echo -e "${GREEN}################################################################################${NORMAL}"
}

################################################################################

box "Creating & activating $VENV_NAME virtual environment"

python3 -m venv $VENV_DIR

source $VENV_DIR/bin/activate

if [[ -f requirements.txt ]]
then
   box "Installing/Upgrading packages"

   python3 -m pip install -r requirements.txt
fi

box "Running ${VENV_NAME} script"

python3 ./${VENV_NAME}.py "$@"

deactivate
"""

################################################################################

def main():
    """Create the venv script and make it executable"""

    parser = argparse.ArgumentParser(description='Create a script to run Python code in a virtual environment')
    parser.add_argument('name', nargs=1, help='Name of the script to create')

    args = parser.parse_args()

    with open(args.name[0], 'wt') as scriptfile:
        scriptfile.write(TEMPLATE)

    statinfo = os.stat(args.name[0])

    os.chmod(args.name[0], statinfo.st_mode|stat.S_IXUSR|stat.S_IXGRP|stat.S_IXOTH)

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
