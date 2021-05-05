#!/usr/bin/env python3
"""
Copyright (C) 2021 Kunal Mehta <legoktm@debian.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import json
import sys

from collections import OrderedDict
from pathlib import Path

I18N = Path(__file__).parent / 'i18n'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("action")
    parser.add_argument("--destdir", type=Path)
    return parser.parse_args()


def path_to_key(path: Path) -> str:
    """colons to dashes, remove .txt suffix"""
    return path.name.replace(":", "-")[:-4]


def key_to_filename(key: str) -> str:
    """turn a message key into the filename"""
    # Keys with dashes in them
    if key == "domain-admin-notice-new-list":
        return "domain:admin:notice:new-list.txt"
    elif key == "list-user-notice-no-more-today":
        return "list:user:notice:no-more-today.txt"
    return key.replace("-", ":") + ".txt"


def sync():
    """copy en txt files into en.json"""
    en_dir = Path(__file__).parent / 'en'
    i18n_en = I18N / 'en.json'
    data = []
    for template in en_dir.iterdir():
        data.append((path_to_key(template), template.read_text().rstrip()))
    data.sort()
    i18n_en.write_text(json.dumps(OrderedDict(data), indent="\t"))


def export(destdir: Path):
    """export all JSON messages into txt files"""
    dest = destdir / 'usr/share/mailman-templates'
    for lang in I18N.iterdir():
        code = lang.name[:-5]
        if code == 'qqq':
            continue
        langdir = dest / code
        langdir.mkdir(parents=True, exist_ok=True)
        data = json.loads(lang.read_text())
        for key, val in data.items():
            if key.startswith("@"):
                continue
            path = langdir / key_to_filename(key)
            val = val.strip()
            if val != "":
                # Add trailing newline to non-empty files
                val += "\n"
            path.write_text(val)
            print(f"Wrote to {path}")


def test():
    """quick n dirty banana-checker"""
    en = json.loads((I18N / 'en.json').read_text())
    qqq = json.loads((I18N / 'qqq.json').read_text())
    assert set(en) == set(qqq)


def main():
    args = parse_args()
    if args.action == "sync":
        sync()
    elif args.action == "export":
        if args.destdir is None:
            print("Error: --destdir is required for export")
            sys.exit(1)
        export(args.destdir)
    elif args.action == "test":
        test()
    else:
        print("Unknown action")
        sys.exit(1)


if __name__ == "__main__":
    main()
