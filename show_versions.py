"""
show_versions.py - prints what data.txt contained in every version,
without changing any file in the folder.

It asks Git for the list of tags (v1.0, v2.0, ...) and then asks DVC
for data.txt exactly as it was at each tag.

    python show_versions.py
"""
import subprocess

import dvc.api

tags = subprocess.run(["git", "tag", "--list", "v*", "--sort=v:refname"],
                      capture_output=True, text=True, check=True).stdout.split()

for tag in tags:
    content = dvc.api.read("data.txt", rev=tag).strip()
    print(f"{tag}: data.txt says -> {content!r}")
