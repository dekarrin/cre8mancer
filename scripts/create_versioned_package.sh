#!/bin/bash

# Packages up the results of running pyinstaller into a nice archive.
#
# Pass in the path to the file to package.
# output is the file that was created

set -e

repo_root="$(dirname "$0")/.."

file_to_package="$repo_root/dist/cre8orforge"
if [[ "$#" -ge 1 ]]
then
  file_to_package="$1"
fi
os_arch="win"
if [[ "$#" -ge 2 ]]
then
  os_arch="$2"
fi

if ! [[ -f "$file_to_package" || -d "$file_to_package" ]]
then
  echo "$file_to_package doesn't appear to exist. Make sure to run run_pyinstaller.sh first." >&2
  exit 1
fi

caller_wd="$(pwd)"
cd "$repo_root"
cur_version="$(./cf.sh version)"

if [[ ! -d "$repo_root/dist" ]]
then
  mkdir "$repo_root/dist"
fi

rm -rf "$repo_root/dist/.package"
mkdir "$repo_root/dist/.package"
cd "$caller_wd"
cp -R "$file_to_package" "$repo_root/dist/.package/cre8"
cd "$repo_root/dist/.package"

full_folder="cre8orforge-v${cur_version}-${os_arch}"
rm -rf "$full_folder"
mkdir "$full_folder"
mv cre8 "$full_folder/cre8orforge"

cat << EOF > "$full_folder/TESTER-README.md"
Hey! Thanks for volunteering to help test cre8forge.

To start it, open the cre8orforge folder and run cre8orforge.exe.

You can launch a silly tutorial on how the game works using the 'Tutorial' button
on the main window that pops up.

To report a problem, please take the debug.log file and send it to @dekarrin#0413 on discord
or create a new issue on the [GitHub Issues Page](https://github.com/dekarrin/cre8orforge/issues/new)
for the project. Please be shore to include your operating system as well as what you did when
the issue happened.

Thanks again!
EOF

rm -rf "../$full_folder"
mv "$full_folder" "../$full_folder"
cd ".."
rm -rf .package

echo "$repo_root/dist/${full_folder}"
