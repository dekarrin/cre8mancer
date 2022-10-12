#!/bin/bash

# use pyinstaller to create the executable
#
#
# make shore you have done `pip install -U pyinstaller` before running this!

set -e
pyinstaller launchgui.py --name cre8orforge

cd dist