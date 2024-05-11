TEMPLATE = \
"""#!/usr/bin/env fish

################################################################################

set VENV_NAME $(basename "$0")
set VENV_DIR __venv__

set GREEN "\e[42m"
set NORMAL "\e[0m"

################################################################################

function box
   echo -e "$GREEN################################################################################$NORMAL"
   echo -e "$GREEN# $argv$NORMAL"
   echo -e "$GREEN################################################################################$NORMAL"
end

################################################################################

box "Creating & activating $VENV_NAME virtual environment"

python3 -m venv $VENV_DIR

source $VENV_DIR/bin/activate.fish

if test -f requirements.txt
   box "Installing/Upgrading packages"

   python3 -m pip install -r requirements.txt
end

if test -f $VENV_NAME.py
    box "Running $VENV_NAME script"

    python3 ./$VENV_NAME.py $argv

    deactivate
end
"""
