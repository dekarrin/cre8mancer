#!/bin/bash

# use pyinstaller to create the executable
#
#
# make shore you have done `pip install -U pyinstaller` before running this!

set -e

repo_root="$(dirname "$0")/.."
cd "$repo_root"

# pyinstaller REQUIRES using the correct pathsep
on_windows=
case "$(uname -a)" in
  *CYGWIN*)
    on_windows=1
    ;;
  *MINGW64*)
    on_windows=1
    ;;
esac

if [[ -n "$on_windows" ]]
then
  pathsep=';'
else
  pathsep=':'
fi

pyinstaller launchgui.py --name cre8orforge -y \
  --add-data cre8/components/warning.png${pathsep}assets

echo "$repo_root/dist/cre8orforge"