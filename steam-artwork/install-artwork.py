#!/usr/bin/env python3
"""Give the Blyx shortcut its artwork in Steam.

Steam does not read artwork out of an application — a non-Steam shortcut has
none until someone puts it there. What it does read is a folder of PNGs named
after the shortcut's own id, which is what this writes.

Run it on the Deck in Desktop Mode, after adding Blyx to Steam:

    python3 install-artwork.py

Then restart Steam. Nothing here touches the shortcut itself; the worst case is
four files in a cache folder that Steam ignores.
"""

from __future__ import annotations

import shutil
import struct
import sys
import zlib
from pathlib import Path

#: Where Steam keeps its per-user configuration, per platform and install shape.
STEAM_ROOTS = [
    Path.home() / ".steam" / "steam",
    Path.home() / ".local" / "share" / "Steam",
    Path.home() / ".var" / "app" / "com.valvesoftware.Steam" / ".local" / "share" / "Steam",
    Path.home() / "Library" / "Application Support" / "Steam",
]

#: Which generated file belongs in which slot Steam reads.
ARTWORK = {
    "grid-portrait-600x900.png": "{appid}p.png",
    "grid-landscape-920x430.png": "{appid}.png",
    "hero-1920x620.png": "{appid}_hero.png",
    "logo.png": "{appid}_logo.png",
}


def parse_binary_vdf(data: bytes, offset: int = 0) -> tuple[dict, int]:
    """Reads Valve's binary key-value format.

    Small on purpose: shortcuts.vdf uses three of the type bytes and nothing
    else, and a general parser would be more code to get wrong.

    :param data: The file's bytes.
    :param offset: Where to start reading.
    :returns: The parsed map and the offset just past it.
    """
    result: dict = {}

    while offset < len(data):
        kind = data[offset]
        offset += 1

        if kind == 0x08:  # end of this map
            return result, offset

        end = data.index(b"\x00", offset)
        key = data[offset:end].decode("utf-8", "replace")
        offset = end + 1

        if kind == 0x00:  # a nested map
            result[key], offset = parse_binary_vdf(data, offset)
        elif kind == 0x01:  # a string
            end = data.index(b"\x00", offset)
            result[key] = data[offset:end].decode("utf-8", "replace")
            offset = end + 1
        elif kind == 0x02:  # a 32-bit integer
            result[key] = struct.unpack("<i", data[offset : offset + 4])[0]
            offset += 4
        else:  # something this file was not supposed to contain
            raise ValueError(f"unexpected type byte {kind:#x} at {offset - 1}")

    return result, offset


def shortcut_appid(exe: str, name: str) -> int:
    """Works out the id Steam gives a shortcut, when the file does not say.

    :param exe: The command Steam runs, quotes and all.
    :param name: The name shown in the library.
    :returns: The unsigned 32-bit id used for artwork filenames.
    """
    return zlib.crc32((exe + name).encode("utf-8")) | 0x80000000


def find_shortcuts() -> list[tuple[Path, dict]]:
    """Finds every user's shortcuts file.

    :returns: Pairs of config directory and parsed contents.
    """
    found = []

    for root in STEAM_ROOTS:
        for path in sorted(root.glob("userdata/*/config/shortcuts.vdf")):
            try:
                parsed, _ = parse_binary_vdf(path.read_bytes())
            except (OSError, ValueError) as error:
                print(f"  ! could not read {path}: {error}")
                continue

            found.append((path.parent, parsed))

    return found


def main() -> int:
    """Copies the artwork into place for every Blyx shortcut found."""
    here = Path(__file__).resolve().parent
    missing = [name for name in ARTWORK if not (here / name).exists()]

    if missing:
        print("These artwork files are missing next to the script:", ", ".join(missing))
        return 1

    installs = find_shortcuts()

    if not installs:
        print("No Steam shortcuts file found. Add Blyx to Steam first, then run this again.")
        return 1

    written = 0

    for config_dir, parsed in installs:
        shortcuts = parsed.get("shortcuts", {})

        for entry in shortcuts.values():
            name = str(entry.get("AppName") or entry.get("appname") or "")

            # Either name: a shortcut added before the rename is still called
            # GameDex in Steam until somebody renames it by hand, and its
            # artwork should land on it all the same.
            if not any(part in name.lower() for part in ("blyx", "gamedex")):
                continue

            appid = entry.get("appid")
            exe = str(entry.get("Exe") or entry.get("exe") or "")
            # The stored id is signed; the filenames use the unsigned form.
            appid = appid & 0xFFFFFFFF if isinstance(appid, int) else shortcut_appid(exe, name)

            grid = config_dir / "grid"
            grid.mkdir(parents=True, exist_ok=True)

            for source, pattern in ARTWORK.items():
                shutil.copyfile(here / source, grid / pattern.format(appid=appid))
                written += 1

            print(f"  {name}  ->  {grid}  (id {appid})")

    if written == 0:
        print("Found Steam, but no shortcut whose name contains 'Blyx'.")
        print("Add the AppImage to Steam, rename it to Blyx, and run this again.")
        return 1

    print(f"\nWrote {written} files. Restart Steam to see them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
