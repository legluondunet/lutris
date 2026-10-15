#!/usr/bin/env python3
"""Build only the test client and host bridge over the installed Flathub app."""

import configparser
import sys
from pathlib import Path

import yaml

manifest = Path(sys.argv[1])
metadata = configparser.ConfigParser(interpolation=None)
metadata.read(sys.argv[2])
application = metadata["Application"]
runtime, architecture, version = application["runtime"].split("/")
sdk, sdk_arch, sdk_version = application["sdk"].split("/")
if architecture != "x86_64" or sdk_arch != architecture or sdk_version != version:
    sys.exit("The installed Flathub app and SDK must use the same x86_64 runtime branch")

upstream = yaml.safe_load(manifest.read_text())
finish_args = upstream["finish-args"]
finish_args = [
    "--env=LD_LIBRARY_PATH=/app/lib:/usr/lib/extensions/vulkan/gamescope/lib"
    if arg.startswith("--env=LD_LIBRARY_PATH=")
    else arg
    for arg in finish_args
]
for permission in ("--talk-name=org.freedesktop.Flatpak", "--filesystem=~/Games"):
    if permission not in finish_args:
        finish_args.append(permission)

result = {
    "id": "net.lutris.Lutris",
    "runtime": runtime,
    "runtime-version": version,
    "sdk": sdk,
    "command": "lutris",
    "base": "net.lutris.Lutris",
    "base-version": "stable",
    "finish-args": finish_args,
    "inherit-extensions": [
        section.removeprefix("Extension ") for section in metadata.sections() if section.startswith("Extension ")
    ],
    "modules": [
        {
            "name": "flatpak-xdg-utils",
            "buildsystem": "meson",
            "sources": [
                {
                    "type": "git",
                    "url": "https://github.com/flatpak/flatpak-xdg-utils.git",
                    "commit": "3a6999168424174fcc620b6858985b05806cbdf6",
                }
            ],
        },
        {
            "name": "lutris",
            "buildsystem": "meson",
            "sources": [{"type": "dir", "path": "lutris-source"}],
        },
    ],
}
manifest.write_text(yaml.safe_dump(result, sort_keys=False, width=120))
print(f"Reusing Flathub Lutris with {runtime}/{architecture}/{version}; building only host bridge and client.")
